import pytest

from django.contrib.gis.geos import Point

from geolocation.geo_utils import CoordinatesNotFound, GeoCoder
from geolocation.models import Address
from geolocation.tasks import add_coordinates_to_address


def test_convert_full_address_to_coordinates():
    address = "Plaça del Vi 27, Girona, Girona, Catalonia, 17001, Spain"

    geodata = GeoCoder()
    geodata.get_coordinates(address)

    assert all([hasattr(geodata, "lat"), hasattr(geodata, "lon")])
    assert geodata.lat == 41.9828528
    assert geodata.lon == 2.8244397
    assert isinstance(geodata.geo_point, Point)


def test_raise_exception_when_fail_get_coordinates_from_address():
    with pytest.raises(CoordinatesNotFound):
        geodata = GeoCoder(user_agent="Testing 'nem per feina'")
        geodata.get_coordinates("Gironaa, Catalunya")


@pytest.mark.django_db
def test_add_new_address(address_factory):
    address = address_factory(county="Girona", city="Girona")
    assert address.county == "Girona"
    assert address.city == "Girona"


@pytest.mark.django_db
def test_set_coordinates_to_address(address_factory):
    address = "Plaça del Vi, 27, Girona, Girona, Catalonia, 17001, Spain"
    street, number, city, county, state, postalcode, country = address.split(",")
    new_address_entry = address_factory(
        street=street,
        number=number,
        county=county,
        city=city,
        state=state,
        postalcode=postalcode,
        country=country,
    )

    assert all((new_address_entry.lat is None, new_address_entry.lat is None))
    lat = 41.9828528
    lon = 2.8244397
    new_address_entry.set_coordinates(lat, lon)
    assert all((new_address_entry.lat == lat, new_address_entry.lon == lon))


@pytest.mark.django_db
def test_get_coordinates_from_address_record_full_address(address_factory):
    address = "Plaça del Vi, 27, Girona, Girona, Catalonia, 17001, Spain"
    street, number, city, county, state, postalcode, country = address.split(",")
    new_address = address_factory(
        street=street,
        number=number,
        city=city,
        county=county,
        state=state,
        postalcode=postalcode,
        country=country,
    )
    lat = 41.9828528
    lon = 2.8244397
    location = GeoCoder()
    location.get_coordinates(address=new_address.full_address)
    assert all((location.lat == lat, location.lon == lon))


from django.db import connection
from django.test.utils import CaptureQueriesContext


@pytest.mark.django_db
@pytest.mark.now
def test_convert_address_records_to_geojson(complete_address_records):

    with CaptureQueriesContext(connection):
        geojson = Address.objects.geojson()
        print(len(connection.queries))
    #     breakpoint()

    # assert geojson["features"][0]["geometry"] is not None
    # assert isinstance(geojson, dict)
    # assert len(geojson["features"]) == 2
    # # test chaining query
    # single_geometry = Address.objects.filter(pk=1).geojson()
    # assert ["city", "country", "company_name", "opening_positions"] == list(
    #     single_geometry["features"][0]["properties"].keys()
    # )


@pytest.mark.django_db
def test_celery_task_add_coordinates_to_address(address_factory):
    # Integration
    address = address_factory()
    assert all((address.lat is None, address.lat is None))
    # get the result object from celery task
    address = add_coordinates_to_address.apply_async(kwargs={"pk": address.pk}).result
    assert all((address.lat is not None, address.lat is not None))


# @pytest.mark.django_db
def print_total_queries(fn, *args, **kwargs):
    from django.db import connection

    def wrap(cims_list, routes_list, *args, **kwargs):
        with CaptureQueriesContext(connection):
            fn(cims_list, routes_list, *args, **kwargs)
            print(len(connection.queries))

    return wrap

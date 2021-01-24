import datetime

import pytest

from django.contrib.gis.geos import Point

from geolocation.geo_utils import CoordinatesNotFound, GeoCoder
from geolocation.models import Address
from geolocation.tasks import add_coordinates_to_address
from jobsapp.models import Job


@pytest.mark.django_db
def print_total_queries(fn, *args, **kwargs):
    from django.db import connection

    def wrap(cims_list, routes_list, *args, **kwargs):
        with CaptureQueriesContext(connection):
            fn(cims_list, routes_list, *args, **kwargs)
            print(len(connection.queries))

    return wrap


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


from django.db import connection, transaction
from django.test.utils import CaptureQueriesContext


@pytest.mark.django_db
def test_convert_address_records_to_geojson(complete_address_records):

    with CaptureQueriesContext(connection):
        geojson = Address.objects.geojson()
        assert len(connection.queries) == 2
    assert geojson["features"][0]["geometry"] is not None
    assert isinstance(geojson, dict)


@pytest.mark.django_db
def test_celery_task_add_coordinates_to_address(address_factory):
    # Integration
    address = address_factory()
    assert all((address.lat is None, address.lat is None))
    # get the result object from celery task
    address = add_coordinates_to_address.apply_async(kwargs={"pk": address.pk}).result
    assert all((address.lat is not None, address.lat is not None))


@pytest.mark.django_db(transaction=True)
def test_create_new_job(user_factory):
    user = user_factory()
    test_data = {
        "user_id": user.id,
        "title": "Title 1",
        "description": "Description 1",
        "location": "Ronda Florinda Sala 31 Apt. 78 Cuenca, 79838",
        "type": "1",
        "category": "web-design",
        "company_name": "Villegas-Campoy",
        "company_description": "Natus illo officiis facere deleniti illo. Facilis repellat optio commodi.Nostrum maxime hic aspernatur distinctio quod dolorem. Quibusdam impedit dolor doloremque perferendis tempora ducimus ut.",
        "website": "https://www.lujan.es/",
        "last_date": datetime.datetime.now() + datetime.timedelta(days=30),
        "filled": False,
        "salary": None,
        "remote": "2",
        "apply_url": "",
        "geo_location": {"city": "Girona"},
    }
    job = Job.save_job_with_address(test_data)
    address = Address.objects.first()
    assert address.jobs.first().pk == job.pk
    assert address.lat is not None

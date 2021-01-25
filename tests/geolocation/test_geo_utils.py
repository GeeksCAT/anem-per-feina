import datetime

import pytest

from django.contrib.gis.geos import Point
from django.db import connection
from django.test.utils import CaptureQueriesContext

from geolocation.geo_utils import CoordinatesNotFound, GeoCoder, _add_coordinates_to_address
from geolocation.models import Address, Map
from geolocation.tasks import add_coordinates_to_address
from jobsapp.models import Job


def test_convert_full_address_to_coordinates():
    address = "Plaça del Vi 27, Girona, Girona, Catalonia, 17001, Spain"

    geodata = GeoCoder()
    geodata.get_coordinates(address)

    assert all([hasattr(geodata, "lat"), hasattr(geodata, "lon")])
    assert geodata.lat == 41.9828528
    assert geodata.lon == 2.8244397
    assert isinstance(geodata.geo_point, Point)


@pytest.mark.django_db
def test_set_coordinates_to_address_record(address_factory):
    address = "Plaça del Vi 27, Girona, Girona, Catalonia, 17001, Spain"
    street, city, county, state, postalcode, country = address.split(",")
    new_address_entry = address_factory(
        street=street,
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
def test_raise_exception_when_fail_get_coordinates_from_address(address_factory):
    address = address_factory(street="Carrer Mignit", city="Girona", county="Girona")
    with pytest.raises(CoordinatesNotFound):
        geodata = GeoCoder(user_agent="Testing 'nem per feina'")
        geodata.get_coordinates(address.full_address)


@pytest.mark.django_db
@pytest.mark.now
def test_get_coordinates_when_fail_get_coordinates_from_original_address(address_factory):
    address = address_factory(street="Carrer Mignit", city="Girona", county="Girona")
    location = _add_coordinates_to_address(pk=address.pk)
    assert all([hasattr(location, "lat"), hasattr(location, "lon")])
    assert all([isinstance(location.lat, float), isinstance(location.lon, float)])


@pytest.mark.django_db
def test_convert_address_records_to_geojson(complete_address_records):
    with CaptureQueriesContext(connection):
        geojson = Map.objects.geojson()
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

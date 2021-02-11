import datetime
from types import SimpleNamespace
from typing import NamedTuple

import pytest

from django.contrib.gis.geos import Point
from django.db import connection, transaction
from django.db.models.fields import TimeField
from django.test.utils import CaptureQueriesContext

from geolocation.geo_utils import CoordinatesNotFound, GeoCoder, check_duplicated_coordinates
from geolocation.models import Address, Map, User
from jobsapp.models import Job


# unit
def test_offset_coordinates():
    """Test that if there is duplicated coordinates, we offset them"""
    run_check = check_duplicated_coordinates()
    original_coordinates = [(41.9793006, 2.8199439), (41.979, 2.2343), (41.9793006, 2.8199439)]
    final_coordinates = [run_check(*coord) for coord in original_coordinates]
    assert original_coordinates != final_coordinates
    assert len(original_coordinates) == len(final_coordinates)


def test_convert_full_address_to_coordinates(mocker):
    """Get coordinates from a string address."""
    lat = 41.9828528
    lon = 2.8244397
    geodata = GeoCoder()
    geodata._get_coordinates(address="Plaça del Vi 27, Girona, Girona, Catalonia, 17001, Spain")

    assert all(
        [hasattr(geodata, "lat"), hasattr(geodata, "lon"), isinstance(geodata.geo_point, Point)]
    )
    assert geodata.lat == lat
    assert geodata.lon == lon


def test_from_address_to_coordinates(mocker):
    """Get coordinates from an Address object instance."""

    def coordinates(self, address):
        """Mock geocoder response."""
        self.lat = lat
        self.lon = lon
        self.geo_point = Point(lon, lat)
        return self

    lat = 41.9828528
    lon = 2.8244397

    location = GeoCoder()
    mocker.patch("geolocation.geo_utils.GeoCoder._get_coordinates", coordinates)
    address = Address(city="Girona", country="Spain")
    location.from_address_to_coordinates(address=address)

    assert all(
        (
            isinstance(location.lat, float),
            isinstance(location.lon, float),
            location.lat == lat,
            location.lon == lon,
        )
    )


def test_raise_exception_when_fail_get_coordinates_from_address(mocker):
    mocker.patch("geolocation.geo_utils.GeoCoder._get_coordinates", side_effect=CoordinatesNotFound)
    geodata = GeoCoder(user_agent="Testing 'nem per feina'")
    address = "Carrer Mignit, Girona, Girona"
    with pytest.raises(CoordinatesNotFound):
        geodata._get_coordinates(address)


def test_add_address_instance_to_job(mocker):
    mocker.patch("jobsapp.models.Job.save", return_value=Job)
    user = User(email="tester@tester.cat", password="nemperfeina")
    address = Address(user=user, lat=41.00, lon=-9.1234)
    job = Job(user=user)
    assert job.address is None
    job.set_address(address)
    assert job.address.lat == 41.00
    assert job.address.lon == -9.1234


# integration
@pytest.mark.django_db(transaction=True)
def test_add_coordinates_to_address(address_factory):
    """Test that coordinates is automatically added once we save the new address entry."""
    address = address_factory()
    assert not all(
        (
            isinstance(address.lat, float),
            isinstance(address.lon, float),
            isinstance(address.geo_point, Point),
        )
    )
    # After the transaction ends, we will have the coordinates and the geo point
    address.refresh_from_db()
    assert all(
        (
            isinstance(address.lat, float),
            isinstance(address.lon, float),
            isinstance(address.geo_point, Point),
        )
    )


@pytest.mark.django_db
def test_convert_address_records_to_geojson(complete_address_records):
    """Test geojson data conversion.
    Also ensures that using preftech_related we can get all data needed from database with
    only two queires.
    """
    with CaptureQueriesContext(connection):
        geojson = Map.objects.geojson()
        assert len(connection.queries) == 2
    assert geojson["features"][0]["geometry"] is not None
    assert isinstance(geojson, dict)


@pytest.mark.django_db(transaction=True)
def test_convert_to_geojson_only_unfilled_offers(complete_address_records):
    # Current there is 4 jobs availables
    assert Job.objects.count() == 4
    # Turn one job as filled
    job = Job.objects.first()
    job.filled = True
    job.save()
    # Now should be only 3 opening positions on the geojson response
    geojson = Map.objects.geojson()
    total_opening_positions = sum(
        [job["properties"]["opening_positions"] for job in geojson["features"]]
    )
    assert total_opening_positions == 3

    """
    Instead of saving the address information on a background task, we now save it at the same time than we save the job offer.
    Also:
    - Add tests for HTTP job form create and update offer
    - Clean up some tests
    """

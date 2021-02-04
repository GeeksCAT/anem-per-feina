import datetime

import pytest

from django.contrib.gis.geos import Point
from django.db import connection, transaction
from django.test.utils import CaptureQueriesContext

from geolocation.geo_utils import (
    CoordinatesNotFound,
    GeoCoder,
    add_address_to_job,
    check_duplicated_coordinates,
)
from geolocation.models import Address, Map
from jobsapp.models import Job
from tests.conftest import create_job


def test_offset_coordinates():
    """Test that if there is duplicated coordinates, we offset them"""
    run_check = check_duplicated_coordinates()
    original_coordinates = [(41.9793006, 2.8199439), (41.979, 2.2343), (41.9793006, 2.8199439)]
    final_coordinates = [run_check(*coord) for coord in original_coordinates]
    assert original_coordinates != final_coordinates
    assert len(original_coordinates) == len(final_coordinates)


def test_convert_full_address_to_coordinates():
    address = "Plaça del Vi 27, Girona, Girona, Catalonia, 17001, Spain"

    geodata = GeoCoder()
    geodata._get_coordinates(address)

    assert all(
        [hasattr(geodata, "lat"), hasattr(geodata, "lon"), isinstance(geodata.geo_point, Point)]
    )
    assert geodata.lat == 41.9828528
    assert geodata.lon == 2.8244397


def test_from_address_to_coordinates():
    address = Address(city="Girona", country="Spain")
    location = GeoCoder()
    location.from_address_to_coordinates(address=address)

    assert all((isinstance(location.lat, float), isinstance(location.lon, float)))


@pytest.mark.django_db  # TODO: Maybe can be removed
def test_add_address_instance_to_job(address_factory, create_job, user_factory):
    user = user_factory()
    address = address_factory(user=user)
    address.set_coordinates(41.00, -9.1234)
    job = create_job(user=user)
    assert job.address is None
    job.set_address(address)
    assert job.address.lat == 41.00
    assert job.address.lon == -9.1234


@pytest.mark.django_db
def test_raise_exception_when_fail_get_coordinates_from_address(address_factory):
    address = address_factory(street="Carrer Mignit", city="Girona", county="Girona")
    with pytest.raises(CoordinatesNotFound):
        geodata = GeoCoder(user_agent="Testing 'nem per feina'")
        geodata._get_coordinates(address.full_address)


@pytest.mark.django_db(transaction=True)
def test_job_with_same_location_from_same_user_are_merge(user_factory, create_user_job):
    """
    Ensures that if the same company post two jobs to the same location,
    we just end up with one address on the database but containing two jobs positions.
    """
    user = user_factory()
    address = {"city": "Girona", "country": "Spain"}

    job = create_user_job(user=user)
    job2 = create_user_job(user=user)

    address_job_1 = add_address_to_job(job_id=job.pk, address=address)
    address_job_2 = add_address_to_job(job_id=job2.pk, address=address)
    address_job_1.refresh_from_db()
    address_job_2.refresh_from_db()

    assert address_job_1.lat == address_job_2.lat
    assert address_job_1.lon == address_job_2.lon
    address = Address.objects.all()
    assert address.count() == 1
    assert address[0].jobs.count() == 2


@pytest.mark.django_db(transaction=True)
def test_jobs_from_different_user_with_same_location_get_same_coordinates(create_user_job):
    job = create_user_job()
    job2 = create_user_job()
    address = {"city": "Girona", "country": "Spain"}

    address_job_1 = add_address_to_job(job_id=job.pk, address=address)
    address_job_2 = add_address_to_job(job_id=job2.pk, address=address)

    address_job_1.refresh_from_db()
    address_job_2.refresh_from_db()
    assert address_job_1.lat == address_job_2.lat
    assert address_job_1.lon == address_job_2.lon


@pytest.mark.django_db(transaction=True)
def test_update_job_address(create_user_job, user_factory):

    user = user_factory()
    address = {"city": "Girona", "country": "Spain"}
    # Create jobs offers
    job = create_user_job(user=user)
    job2 = create_user_job(user=user)
    # Add address to job offer
    add_address_to_job(job.pk, address)
    add_address_to_job(job2.pk, address)

    # Update one job address
    update_job = Job.objects.first()
    new_address = {"city": "Barcelona", "country": "Spain"}
    add_address_to_job(job_id=update_job.pk, address=new_address)

    # Check that now there is two addresses with coordinates and job offer
    assert Address.objects.count() == 2
    for address in Address.objects.all():
        assert address.has_coordinates()
    geojson = Map.objects.geojson()
    assert len(geojson["features"]) == 2


@pytest.mark.django_db(transaction=True)
def test_add_address_to_job(create_user_job):
    job = create_user_job()
    address = add_address_to_job(job.pk, {"city": "Girona", "country": "Spain"})
    address.refresh_from_db()

    assert all(
        [
            isinstance(address.lat, float),
            isinstance(address.lon, float),
            isinstance(address.geo_point, Point),
        ]
    )
    job.refresh_from_db()
    assert job.address == address


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

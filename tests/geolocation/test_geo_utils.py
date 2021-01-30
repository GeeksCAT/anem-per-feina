import datetime

import pytest

from django.contrib.gis.geos import Point
from django.db import connection
from django.test.utils import CaptureQueriesContext

from geolocation.geo_utils import (
    CoordinatesNotFound,
    GeoCoder,
    add_address_to_job,
    check_duplicated_coordinates,
)
from geolocation.models import Address, Map
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
def test_raise_exception_when_fail_get_coordinates_from_address(address_factory):
    address = address_factory(street="Carrer Mignit", city="Girona", county="Girona")
    with pytest.raises(CoordinatesNotFound):
        geodata = GeoCoder(user_agent="Testing 'nem per feina'")
        geodata.get_coordinates(address.full_address)


@pytest.mark.django_db(transaction=True)
def test_job_with_same_location_from_same_user_are_merge(
    address_factory, user_factory, job_factory
):
    """
    Ensures that if the same company post two jobs to the same location,
    we just end up with one address on the database but containing two jobs positions.
    """
    user = user_factory()
    address = address_factory(user=user, city="Girona", country="Spain")
    address2 = address_factory(user=user, city="Girona", country="Spain")

    job = job_factory(user=user)
    job2 = job_factory(user=user)

    address_job_1 = add_address_to_job(address_id=address.pk, job_id=job.pk)
    address_job_2 = add_address_to_job(address_id=address2.pk, job_id=job2.pk)

    assert Address.objects.count() == 1
    assert address_job_1.lat == address_job_2.lat
    assert address_job_1.lon == address_job_2.lon
    assert address.jobs.count() == 2


@pytest.mark.django_db(transaction=True)
def test_jobs_from_different_user_with_same_location_get_same_coordinates(
    job_factory, address_factory, user_factory
):
    user1 = user_factory()
    user2 = user_factory()

    user1_address = address_factory(user=user1, city="Girona", country="Spain")
    user2_address = address_factory(user=user2, city="Girona", country="Spain")

    job = job_factory(user=user1)
    job2 = job_factory(user=user2)

    address_job_1 = add_address_to_job(address_id=user1_address.pk, job_id=job.pk)
    address_job_2 = add_address_to_job(address_id=user2_address.pk, job_id=job2.pk)

    assert address_job_1.lat == address_job_2.lat
    assert address_job_1.lon == address_job_2.lon


@pytest.mark.django_db(transaction=True)
def test_update_job_address(job_factory, address_factory, user_factory):
    user = user_factory()
    address = address_factory(city="Girona", user=user)
    updated_address = address_factory(city="Barcelona", user=user)

    # create jobs offers
    job = job_factory(user=user)
    job2 = job_factory(user=user)

    # create 2 jobs
    for job in [(address.pk, job.pk), (address.pk, job2.pk)]:
        add_address_to_job(*job)

    # Update one job address
    updated_job = Job.objects.first()
    add_address_to_job(address_id=updated_address.pk, job_id=updated_job.pk)

    assert Address.objects.count() == 2
    for address in Address.objects.all():
        assert address.has_coordinates()

    geojson = Map.objects.geojson()
    assert len(geojson["features"]) == 2


@pytest.mark.django_db
def test_add_address_instance_to_job(address_factory, job_factory, user_factory):
    user = user_factory()
    address = address_factory(user=user)
    address.set_coordinates(41.00, -9.1234)
    job = job_factory(user=user)
    assert job.address is None
    job.set_address(address)
    assert job.address.lat == 41.00
    assert job.address.lon == -9.1234


@pytest.mark.django_db
def test_add_address_instance_to_job(address_factory, job_factory, user_factory):
    user = user_factory()
    address = address_factory(user=user)
    address.set_coordinates(41.00, -9.1234)
    job = job_factory(user=user)
    assert job.address is None
    job.set_address(address)
    assert job.address.lat == 41.00
    assert job.address.lon == -9.1234


@pytest.mark.django_db
def test_convert_address_records_to_geojson(complete_address_records):
    with CaptureQueriesContext(connection):
        geojson = Map.objects.geojson()
        assert len(connection.queries) == 2
    assert geojson["features"][0]["geometry"] is not None
    assert isinstance(geojson, dict)


@pytest.mark.django_db(transaction=True)
@pytest.mark.now
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


def test_offset_coordinates():
    """Test that if there is duplicated coordinates, we offset them"""
    run_check = check_duplicated_coordinates()
    original_coordinates = [(41.9793006, 2.8199439), (41.979, 2.2343), (41.9793006, 2.8199439)]
    final_coordinates = [run_check(*coord) for coord in original_coordinates]
    assert original_coordinates != final_coordinates
    assert len(original_coordinates) == len(final_coordinates)

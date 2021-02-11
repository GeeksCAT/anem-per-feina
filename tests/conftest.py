import factory
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from django.conf import settings
from django.contrib.gis.geos import Point

from tests.factories import AddressFactory, JobFactory, UserFactory

# Register factories to pytest global namespace.
# They can be access as normal fixtures using user_factory or job_factory.
register(UserFactory)
register(JobFactory)
register(AddressFactory)


def pytest_configure():
    """
    Use for override default settings
    https://pytest-django.readthedocs.io/en/latest/configuring_django.html#using-django-conf-settings-configure
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    settings.STATICFILES_STORAGE = ""


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_authenticate(db, user_factory, api_client):
    def _api_client(user=None):
        """Allows pass custom user object."""
        if user is None:
            user = user_factory()
        api_client.force_authenticate(user=user)
        return api_client

    yield _api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def create_job(db, job_factory):
    return job_factory


@pytest.fixture
def create_user_job(db, job_factory, user_factory):
    def _create_user_job(user=None):
        return job_factory(user=user if user else user_factory())

    return _create_user_job


@pytest.fixture
def create_job_as_dict(db, job_factory) -> dict:
    return factory.build(dict, FACTORY_CLASS=JobFactory)


@pytest.fixture
def create_jobs(db, job_factory):
    def _create_jobs(size=10):
        return job_factory.simple_generate_batch(create=True, size=size)

    return _create_jobs


@pytest.fixture
def create_users(db, user_factory):
    def _create_users(size=5):
        return user_factory.simple_generate_batch(create=True, size=size)

    return _create_users


@pytest.fixture
def complete_address_records(address_factory, job_factory):
    address_list = [
        address_factory(
            city="Girona", lat=41.9828528, lon=2.8244397, geo_point=Point(2.8244397, 41.9828528)
        ),
        address_factory(
            city="Barcelona", lat=40.9828528, lon=2.8244397, geo_point=Point(2.8244397, 40.9828528)
        ),
    ]
    for _ in range(2):
        job_factory(address=address_list[0])
        job_factory(address=address_list[1])

    return address_list


@pytest.fixture
def mock_geocoder_get_coordinates(mocker):
    def coordinates(self, address):
        """Mock geocoder response.

        address = {"city": "Girona", "country": "Spain"}
        """

        self.lat = 41.9828528
        self.lon = 2.8244397
        return self

    return mocker.patch("geolocation.geo_utils.GeoCoder._get_coordinates", coordinates)

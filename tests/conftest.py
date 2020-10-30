import factory
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from django.conf import settings

from tests.factories import JobFactory, UserFactory

# Register factories to pytest global namespace.
# They can be access as normal fixtures using user_factory or job_factory.
register(UserFactory)
register(JobFactory)


def pytest_configure():
    """
    Use for override default settings
    https://pytest-django.readthedocs.io/en/latest/configuring_django.html#using-django-conf-settings-configure
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_authenticate(db, user_factory, api_client):
    user = user_factory()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def create_job(db, job_factory):
    return job_factory


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

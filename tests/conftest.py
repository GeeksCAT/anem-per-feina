import pytest
from rest_framework.test import APIClient

from django.conf import settings

from tests.factories import UserFactory

CONTENT_TYPE_JSON = "application/json"
PASSWORD = "SuperPasswordSecret4"
EMAIL = "hi@geeks.cat"


def pytest_configure():
    """
    Use for override default settings
    https://pytest-django.readthedocs.io/en/latest/configuring_django.html#using-django-conf-settings-configure
    """
    pass


@pytest.fixture
def create_user() -> UserFactory:
    user = UserFactory(email=EMAIL, is_active=True)
    user.set_password(PASSWORD)
    user.save()
    return user


@pytest.fixture
def client() -> APIClient:
    api_client = APIClient()
    return api_client

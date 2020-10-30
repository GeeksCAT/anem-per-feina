import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


def test_contact_us(api_client):
    resp = api_client.get("/api/contact-us")
    assert resp.status_code == 405
    from django.core import mail

    data = {
        "name": "test",
        "from_email": "test@tester.cat",
        "subject": "Testing",
        "message": "tests",
    }
    resp = api_client.post("/api/contact-us", data=data)
    assert len(mail.outbox) == 1
    assert resp.status_code == 202


@pytest.mark.django_db
def test_about_us(api_client):
    resp = api_client.get("/api/about-us")
    assert resp.status_code == 200

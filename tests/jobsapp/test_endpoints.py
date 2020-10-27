import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


def test_about_us(api_client):
    resp = api_client.get("/api/about-us")
    expected_keys = [
        "name",
        "web_page",
        "email",
        "contact_phone",
        "location",
        "lead_description",
        "text_description",
    ]
    assert resp.status_code == 200
    assert expected_keys == list(resp.data.keys())


def test_contact_us(api_client):
    resp = api_client.get("/api/contact-us")
    assert resp.status_code == 405
    data = {"name": "test", "email": "test@tester.cat", "subject": "Testing", "message": "tests"}
    resp = api_client.post("/api/contact-us", data=data)
    assert resp.status_code == 202

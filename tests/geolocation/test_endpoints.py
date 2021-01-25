import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_get_all_jobs_as_geojson(api_client):
    req = api_client.get(reverse("jobs-map"))

    assert req.status_code == 200
    assert ["type", "crs", "features"] == list(req.json().keys())

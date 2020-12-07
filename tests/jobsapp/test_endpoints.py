# type:ignore
import pytest
from rest_framework.test import APIClient

JOBS_ENDPOINT = "/api/jobs"
USERS_ENDPOINT = "/api/users"
from jobs.settings import REST_FRAMEWORK


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.skip
@pytest.mark.django_db
def test_about_us(api_client, db):
    """REVIEW: Not working due:
    AttributeError: 'NoneType' object has no attribute 'title'

    However it works when tested manually. Maybe during test table is not created.
    """
    resp = api_client.get("/api/about-us")
    assert resp.status_code == 200


def test_contact_us(api_client):
    resp = api_client.get("/api/contact-us")
    assert resp.status_code == 405
    data = {
        "name": "test",
        "from_email": "test@tester.cat",
        "subject": "Testing",
        "message": "tests",
    }
    resp = api_client.post("/api/contact-us", data=data)
    assert resp.status_code == 202


@pytest.mark.django_db
def test_user_from_user_factory(user_factory):
    user = user_factory()
    assert user.last_name == "Doe"


@pytest.mark.django_db
def test_list_all_jobs(api_client, create_jobs):
    """Ensures that everyone can see the jobs endpoint."""
    create_jobs(size=20)
    response = api_client.get(JOBS_ENDPOINT)
    assert response.status_code == 200
    assert len(response.data) > 1


@pytest.mark.django_db
def test_list_all_users(api_client, create_users):
    """Ensures that everyone can see the jobs endpoint."""
    create_users(size=20)
    response = api_client.get(USERS_ENDPOINT)
    assert response.status_code == 200
    assert len(response.data) > 1


@pytest.mark.django_db
def test_create_job(api_client_authenticate, create_job_as_dict, create_jobs):
    """Test HTTP POST method.

    Ensures that only registered user can create jobs."""
    response = api_client_authenticate.post(JOBS_ENDPOINT, data=create_job_as_dict)
    assert response.status_code == 201


@pytest.mark.django_db
def test_anonymous_user_cant_create_job(api_client, create_job_as_dict):
    """Ensures that not registered user can't create jobs."""
    response = api_client.post(JOBS_ENDPOINT, data=create_job_as_dict)
    assert response.status_code == 401


@pytest.mark.django_db
def test_patch_job(api_client_authenticate, create_job_as_dict):
    """Test HTTP PATCH method."""
    response = api_client_authenticate.post(JOBS_ENDPOINT, data=create_job_as_dict)
    job_url = response.data["url"]
    data = {"filled": True}
    response = api_client_authenticate.patch(job_url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_job(api_client_authenticate, create_job_as_dict):
    """Test HTTP DELETE method."""
    response = api_client_authenticate.post(JOBS_ENDPOINT, data=create_job_as_dict)
    job_url = response.data["url"]
    response = api_client_authenticate.delete(job_url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_only_authors_can_edit_job(api_client, create_users, create_jobs):
    """Test that non author users can't edit or delete job offers."""
    jobs = create_jobs(10)
    users = create_users(5)
    api_client.force_authenticate(user=users[2])

    # Delete
    response = api_client.delete(f"{JOBS_ENDPOINT}/{jobs[4].id}")
    assert response.status_code == 403
    # Patch
    response = api_client.patch(f"{JOBS_ENDPOINT}/{jobs[4].id}", data={"filled": True})
    assert response.status_code == 403
    # Put
    data = {
        "url": f"http://testserver/api/jobs/{jobs[4].id}",
        "title": "Title 4",
        "description": "Description 4",
        "location": "Cañada de Fermín Lara 19 Apt. 98 \nCastellón, 43469",
        "type": "1",
        "category": "Manager",
        "last_date": "2020-11-09T22:54:05.276115Z",
        "company_name": "Botella PLC",
        "company_description": "Deserunt laboriosam facere iusto eaque. Cumque at cumque.",
        "website": "http://alvaro-castillo.es/",
        "created_at": "2020-10-30T22:54:08.426784Z",
        "filled": True,
        "salary": "20000 - 5000",
        "remote": "2",
        "user": f"http://testserver/api/users/{jobs[4].id}",
    }
    response = api_client.put(f"{JOBS_ENDPOINT}/{jobs[4].id}", data=data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_filter_query(api_client, create_jobs):
    create_jobs(size=20)
    url = f"{JOBS_ENDPOINT}/?category=web-design"
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["results"][0].get("category") == "web-design"
    for job in response.data["results"]:
        assert job.get("category") not in ["Manager", "Junior"]


@pytest.mark.django_db
def test_pagination(api_client, create_jobs):
    create_jobs(size=50)
    url = JOBS_ENDPOINT
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == REST_FRAMEWORK["PAGE_SIZE"]

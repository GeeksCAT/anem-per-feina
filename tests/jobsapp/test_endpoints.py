# type:ignore
import pytest

JOBS_ENDPOINT = "/api/jobs"


@pytest.mark.django_db
def test_user_from_user_factory(user_factory):
    user = user_factory()
    assert user.first_name == "John"


@pytest.mark.django_db
def test_list_all_jobs(api_client, create_jobs):
    """Ensures that everyone can see the jobs endpoint."""
    create_jobs(size=20)
    response = api_client.get(JOBS_ENDPOINT)
    assert response.status_code == 200
    assert len(response.data) > 1
    print(response.data)


@pytest.mark.django_db
def test_create_job(api_client_authenticate, create_job_as_dict, create_jobs):
    """Test HTTP POST method.

    Ensures that only registered user can create jobs."""
    response = api_client_authenticate.post(JOBS_ENDPOINT, data=create_job_as_dict)
    assert response.status_code == 201
    assert response.data["message"] == "New job created."


@pytest.mark.django_db
def test_anonymous_user_cant_create_job(api_client, create_job_as_dict):
    """Ensures that not registered user can't create jobs."""
    response = api_client.post(JOBS_ENDPOINT, data=create_job_as_dict)
    assert response.status_code == 401


@pytest.mark.django_db
def test_patch_job(api_client_authenticate, create_job_as_dict):
    """Test HTTP PATCH method."""
    response = api_client_authenticate.post(JOBS_ENDPOINT, data=create_job_as_dict)
    job_url = response.data["data"]["url"]
    data = {"filled": True}
    response = api_client_authenticate.patch(job_url, data=data)

    print(response.data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_job(api_client_authenticate, create_job_as_dict):
    """Test HTTP DELETE method."""
    response = api_client_authenticate.post(JOBS_ENDPOINT, data=create_job_as_dict)
    job_url = response.data["data"]["url"]
    response = api_client_authenticate.delete(job_url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_filter_query(api_client, create_jobs):
    create_jobs(size=20)
    url = f"{JOBS_ENDPOINT}/?category=Manager"
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["results"][0].get("category") == "Manager"
    for job in response.data["results"]:
        assert job.get("category") not in ["Senior", "Junior"]


@pytest.mark.django_db
def test_pagination(api_client, create_jobs):
    create_jobs(size=50)
    url = JOBS_ENDPOINT
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 25

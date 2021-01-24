# type:ignore
import pytest
from rest_framework.reverse import reverse

from jobs.settings import REST_FRAMEWORK


@pytest.mark.django_db
def test_user_from_user_factory(user_factory):
    user = user_factory()
    assert user.last_name == "Doe"


@pytest.mark.django_db
def test_list_all_jobs(api_client, create_jobs):
    """Ensures that everyone can see the jobs endpoint."""
    create_jobs(size=20)
    response = api_client.get(reverse("jobs-list"))
    assert response.status_code == 200
    assert len(response.data) > 1


@pytest.mark.django_db
def test_list_all_users(api_client, create_users):
    """Ensures that everyone can see the jobs endpoint."""
    create_users(size=20)
    response = api_client.get(reverse("users-list"))
    assert response.status_code == 200
    assert len(response.data) > 1


@pytest.mark.django_db
def test_create_job(api_client_authenticate, create_job_as_dict):
    """Test HTTP POST method.

    Ensures that only registered user can create jobs."""
    create_job_as_dict.pop("user")
    create_job_as_dict["geo_location"] = {"city": "Girona", "country": "Catalunya"}
    response = api_client_authenticate().post(
        reverse("jobs-list"), data=create_job_as_dict, format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_anonymous_user_cant_create_job(api_client, create_job_as_dict):
    """Ensures that not registered user can't create jobs."""
    response = api_client.post(reverse("jobs-list"), data=create_job_as_dict)
    assert response.status_code == 401


@pytest.mark.django_db
def test_patch_job(api_client_authenticate, user_factory, job_factory):
    """Test HTTP PATCH method."""
    user = user_factory()
    new_job = job_factory(filled=False, user=user)

    response = api_client_authenticate(user).patch(
        reverse("job-detail", kwargs={"pk": new_job.pk}), data={"filled": True}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_job(api_client_authenticate, user_factory, job_factory):
    """Test HTTP DELETE method."""
    user = user_factory()
    new_job = job_factory(filled=False, user=user)

    response = api_client_authenticate(user=user).delete(
        reverse("job-detail", kwargs={"pk": new_job.pk})
    )
    assert response.status_code == 204


test_data = (
    ("delete", ""),
    ("patch", {"filled": True}),
    (
        "put",
        {
            "title": "Title 4",
            "description": "Description 4",
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
        },
    ),
)


@pytest.mark.parametrize("method, data", test_data)
@pytest.mark.django_db
def test_only_authors_can_edit_job(
    api_client_authenticate, create_users, job_factory, method, data
):
    """Test that non author users can't edit or delete job offers."""
    author, no_author = create_users(2)
    new_job = job_factory(user=author)
    client = api_client_authenticate(user=no_author)
    url = reverse("job-detail", kwargs={"pk": new_job.pk})

    if method == "delete":  # don't pass data kwarg
        response = getattr(client, method)(url)
    else:
        response = getattr(client, method)(url, data=data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_filter_query(api_client, create_jobs):
    create_jobs(size=20)
    url = f"{reverse('jobs-list')}/?category=web-design"
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["results"][0].get("category") == "web-design"
    for job in response.data["results"]:
        assert job.get("category") not in ["Manager", "Junior"]


@pytest.mark.django_db
def test_pagination(api_client, create_jobs):
    create_jobs(size=50)
    response = api_client.get(reverse("jobs-list"))
    assert response.status_code == 200
    assert len(response.data["results"]) == REST_FRAMEWORK["PAGE_SIZE"]

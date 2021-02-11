import pytest

from django.urls import reverse

from geolocation.models import Address
from jobsapp.forms import CreateJobForm
from jobsapp.models import Job


def model_to_dict(item):
    """Convert a database model to a dictionary so we can test post requests."""
    item = vars(item)
    item.pop("_state")
    return {k: str(v) for k, v in item.items() if v is not None}


@pytest.mark.django_db
def test_create_job_form(user_factory, address_factory, job_factory):
    """Test Form class without HTTP request"""
    user = user_factory()
    address = address_factory()

    job_dict = model_to_dict(job_factory(user=user))
    job_dict["policies"] = True
    form = CreateJobForm(data=job_dict)
    form.instance.address = address
    form.instance.user = user
    assert form.is_valid()
    assert form.save()


@pytest.mark.django_db
def test_form_create_new_job_offer(create_job_as_dict, client, user_factory):
    """Test the HTTP form post."""
    # Create job offer dictionary
    job_offer = create_job_as_dict
    # Add job location
    job_offer["city"] = "Girona"
    job_offer["country"] = "Spain"
    job_offer["policies"] = True

    # POST to form
    client.force_login(user_factory())
    resp = client.post(reverse("jobs:employer-jobs-create"), data=job_offer)
    # Check response
    assert resp.status_code == 302
    # Check if data was added to database
    assert Job.objects.count() == 1
    assert Address.objects.count() == 1
    import time


@pytest.mark.django_db
def test_form_update_job_offer(client, create_user_job, address_factory):
    """Form update job offer .

    HTTP POST request to update the address city field."""
    job = create_user_job()
    user = job.user
    original_job_city = "Girona"
    job.address = address_factory(city=original_job_city)
    job.save()

    # Update job address data
    job_update = model_to_dict(job)
    job_update["city"] = "Barcelona"
    job_update["country"] = "Spain"
    # Sent new updated job offer to server
    client.force_login(user=user)
    resp = client.post(reverse("jobs:employer-jobs-update", kwargs={"pk": job.pk}), data=job_update)

    # Ensures that job offers was updated
    updated_job = Job.objects.get(pk=job.pk)
    assert resp.status_code == 302
    assert updated_job.address.city != original_job_city

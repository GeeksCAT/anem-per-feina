import pytest

from geolocation.models import Address
from jobsapp.forms import CreateJobForm
from jobsapp.models import Job


def job_as_dict(item):
    item = vars(item)
    item.pop("_state")
    return {k: str(v) for k, v in item.items() if v is not None}


@pytest.mark.django_db
def test_create_job_form(user_factory, address_factory, job_factory):
    user = user_factory()
    address = address_factory()

    job_dict = job_as_dict(job_factory(user=user))
    job_dict["policies"] = True
    form = CreateJobForm(data=job_dict)
    form.instance.address = address
    form.instance.user = user
    assert form.is_valid()
    assert form.save()


@pytest.mark.django_db
def test_job_form_post():
    pass

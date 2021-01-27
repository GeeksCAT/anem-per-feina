from celery import shared_task

from django.conf import settings
from django.db import IntegrityError

from geolocation.geo_utils import add_address_to_job

ASYNC_QUEUE_NAME = getattr(settings, "CELERY_HIGH_QUEUE_NAME", "default")


@shared_task(
    bind=True,
    queue=ASYNC_QUEUE_NAME,
    name="geolocation.tasks._add_address_to_job",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def _add_address_to_job(self, address_id, job_id):
    """Celery task to be run after a new address entry is added to the database."""
    return add_address_to_job(address_id, job_id)

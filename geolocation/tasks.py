from typing import Callable

from celery import shared_task

from django.conf import settings
from django.db import IntegrityError

from geolocation.geo_utils import add_address_to_job, add_coordinates_to_address

ASYNC_QUEUE_NAME = getattr(settings, "CELERY_HIGH_QUEUE_NAME", "default")


@shared_task(
    bind=True,
    queue=ASYNC_QUEUE_NAME,
    name="geolocation.tasks._add_address_to_job",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def _add_address_to_job(self, job_id: int, address: dict) -> Callable:
    return add_address_to_job(job_id, address)


@shared_task(
    queue=ASYNC_QUEUE_NAME,
    name="geolocation.tasks._add_coordinates_to_address",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def _add_coordinates_to_address(pk: int) -> Callable:
    """Celery task that runs after a new address entry is added to the database."""
    return add_coordinates_to_address(pk)

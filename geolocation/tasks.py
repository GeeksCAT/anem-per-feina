from celery import shared_task

from django.conf import settings

from .geo_utils import _add_coordinates_to_address

ASYNC_QUEUE_NAME = getattr(settings, "CELERY_HIGH_QUEUE_NAME", "default")


@shared_task(
    name="geolocation.tasks.add_coordinates_to_address",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def add_coordinates_to_address(pk: int):
    """Celery task to be run after a new address entry is added to the database."""
    return _add_coordinates_to_address(pk=pk)

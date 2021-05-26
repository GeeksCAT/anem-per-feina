from typing import Callable

from celery import shared_task

from django.conf import settings

from geolocation.geo_utils import add_coordinates_to_address

ASYNC_QUEUE_NAME = getattr(settings, "CELERY_HIGH_QUEUE_NAME", "default")


@shared_task(
    queue=ASYNC_QUEUE_NAME,
    name="geolocation.tasks._add_coordinates_to_address",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def _add_coordinates_to_address(pk: int) -> Callable:
    """Celery task that runs after a new address entry is added to the database.

    Is responsable to talk with the geocoder service in order to get the address coordinates.
    """
    return add_coordinates_to_address(pk)

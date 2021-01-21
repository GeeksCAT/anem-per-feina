# from jobsapp.models import Job

import ujson

from django.db import models, transaction

from geolocation.tasks import add_coordinates_to_address

from .geo_utils import serializer


class AddressQuerySet(models.QuerySet):
    def geojson(self) -> dict:
        """Convert query to a valid geojson format.

        It allows to be pass as an api response to populate a map.
        """
        queryset = self.prefetch_related("jobs").all()

        return ujson.loads(
            serializer.serialize(
                queryset,
                geometry_field="geo_point",
                fields=("jobs_info", "city", "country"),
                use_natural_foreign_keys=True,
                use_natural_primary_keys=True,
            )
        )

    @transaction.atomic
    def create(self, *args, **kwargs):
        """Create a new address entry on the the database using a transaction.

        Ensures that background tasks will be called only after the new entry is saved.
        """
        new_entry = super().create(*args, **kwargs)
        transaction.on_commit(
            lambda: add_coordinates_to_address.apply_async(kwargs={"pk": new_entry.pk})
        )
        return new_entry

import ujson

from django.core.serializers import serialize
from django.db import models, transaction

from .tasks import add_coordinates_to_address


class AddressQuerySet(models.QuerySet):
    def geojson(self) -> dict:
        """Convert query to a valid geojson format.

        It allows to be pass as an api response to populate a map.
        """
        return ujson.loads(
            serialize(
                "geojson",
                self.all(),
                geometry_field="geo_point",
                fields=(
                    "city",
                    "country",
                ),
            )
        )

    @transaction.atomic
    def create(self, *args, **kwargs):
        """Create a new address entry on the the database using a transaction.

        Ensures that background tasks will be called only after the new entry is saved.
        """
        new_entry = super().create(*args, **kwargs)
        transaction.on_commit(lambda: add_coordinates_to_address.apply_async(new_entry.pk))
        return new_entry

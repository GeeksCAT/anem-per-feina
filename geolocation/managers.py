import ujson

from django.core.serializers import serialize
from django.db import models


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

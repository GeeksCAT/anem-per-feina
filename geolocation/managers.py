import ujson

from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Prefetch

from .geo_utils import geojson_serializer


class AddressQuerySet(models.QuerySet):
    def geojson(self) -> dict:
        """Convert query to a valid geojson format.

        It can be pass as an api response to populate the jobs map.
        """
        from jobsapp.models import Job

        unfilled_jobs = Prefetch("jobs", queryset=Job.objects.unfilled())
        queryset = self.prefetch_related(unfilled_jobs).all()

        return ujson.loads(
            geojson_serializer.serialize(
                queryset,
                geometry_field="geo_point",
                srid=settings.SRID,
                fields=("jobs_info", "city", "country"),
                use_natural_foreign_keys=True,
                use_natural_primary_keys=True,
            )
        )

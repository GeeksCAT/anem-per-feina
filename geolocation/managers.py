import ujson

from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Prefetch

from .geo_utils import geojson_serializer

POPUP_FIELDS = ("jobs_info", "city", "country")


class AddressQuerySet(models.QuerySet):
    def geojson(self) -> dict:
        """Convert query to a valid geojson format.

        It can be pass as an api response to populate the jobs map.
        """
        from jobsapp.models import Job

        # Only the unfilled jobs will be displayed on map.
        unfilled_jobs = Prefetch("jobs", queryset=Job.objects.unfilled())
        queryset = self.prefetch_related(unfilled_jobs).all()

        return ujson.loads(
            geojson_serializer.serialize(
                queryset,
                geometry_field="geo_point",
                srid=settings.SRID,
                fields=POPUP_FIELDS,
            )
        )

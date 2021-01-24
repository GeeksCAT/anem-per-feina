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

        jobs_list = []
        for pt in queryset:
            try:
                # Address without jobs will raise an IndexError. This could be remove at some point as we should enforce all jobs to have some address with
                # coordinates
                job_info = pt.jobs.all()[0]
            except IndexError:
                # Add to logging if some address don't have a job
                continue
            else:
                jobs_list.append(
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [pt.lon, pt.lat]},
                        "properties": {
                            "company_name": job_info.company_name,
                            "opening_positions": pt.jobs.count(),
                            "city": pt.city,
                            "country": pt.country,
                        },
                    }
                )

        return {"type": "FeatureCollection", "features": jobs_list}

        # return ujson.loads(
        #     serializer.serialize(
        #         queryset,
        #         geometry_field="geo_point",
        #         # srid=3857,
        #         fields=("jobs_info", "city", "country"),
        #         use_natural_foreign_keys=True,
        #         use_natural_primary_keys=True,
        #     )
        # )

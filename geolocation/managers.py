from django.db import models
from django.db.models import Count, Prefetch

from geolocation.geo_utils import check_coordinates


class AddressQuerySet(models.QuerySet):
    def geojson(self) -> dict:
        """Convert query to a valid geojson format.

        It can be pass as an api response to populate the jobs map.

        TODO: Add cache to geojson response
        """
        from jobsapp.models import Job

        run_check = check_coordinates()

        # Only the unfilled jobs will be displayed on map.
        unfilled_jobs = Prefetch("jobs", queryset=Job.objects.unfilled())
        jobs_offers = self.prefetch_related(unfilled_jobs).all()
        jobs_list = []
        for offer in jobs_offers:
            try:
                # Address without jobs will raise an IndexError.
                job_info = offer.jobs.all()[0]
            except IndexError:
                # So we skip companies without jobs offers.
                continue
            else:
                jobs_list.append(
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [*run_check(offer.lon, offer.lat)],
                        },
                        "properties": {
                            "company_name": job_info.company_name,
                            "opening_positions": offer.jobs.count(),
                            "city": offer.city,
                            "country": offer.country,
                        },
                    }
                )

        return {"type": "FeatureCollection", "features": jobs_list}

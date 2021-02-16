from django.db import models
from django.db.models import Count, Q

from geolocation.geo_utils import check_duplicated_coordinates


class AddressQuerySet(models.QuerySet):
    def geojson(self) -> dict:
        """Convert query to a valid geojson format.

        It can be pass as an api response to populate the jobs map with open positions.
        """
        # Check for duplicated coordinates
        run_check = check_duplicated_coordinates()

        # Only companies with job offers and unfilled jobs will be present on geojson.
        jobs_offers = (
            self.prefetch_related("jobs")
            .annotate(opening_positions=Count("jobs", filter=(Q(jobs__filled=False))))
            .filter(opening_positions__gte=1)
        )
        jobs_list = []
        for offer in jobs_offers:
            # allows get company information
            company_info = offer.jobs.all()[0]
            jobs_list.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [*run_check(*offer.geo_point.coords)],
                    },
                    "properties": {
                        "company_name": company_info.company_name,
                        "opening_positions": offer.opening_positions,
                        "city": offer.city,
                        "country": offer.country,
                    },
                }
            )

        return {"type": "FeatureCollection", "features": jobs_list}

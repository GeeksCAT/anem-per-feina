from geopy.geocoders import Nominatim

from django.contrib.gis.geos import Point

CoordinatesNotFound = AttributeError
from functools import lru_cache

from django.contrib.gis.serializers.geojson import Serializer


class GeoCoder:
    def __init__(self, user_agent="nem per feina", **kwargs) -> None:
        self.lon: float
        self.coordinates: list
        self.lat: float
        self.geo_point: Point
        self.geolocator: "Nominatim" = Nominatim(user_agent=user_agent, **kwargs)
        self.address: str

    @lru_cache()
    def get_coordinates(self, address, **kwargs) -> None:
        """
        Get address coordinates using OSM Nominatim.

        Search API fields: https://nominatim.org/release-docs/develop/api/Search/
        """

        # build address with as much information as possible using OSM address structure
        # address = f"{street}, {city}, {county}, {state}, {postalcode}, {country}".strip()
        location = self.geolocator.geocode(address, **kwargs)
        try:
            self.lat = location.latitude
            self.lon = location.longitude
            self.geo_point = Point(location.latitude, location.longitude)
        except CoordinatesNotFound:
            raise CoordinatesNotFound(f"Was not possible find coordinates for address:{address}")


def _add_coordinates_to_address(pk: int):
    """Helper function do generate coordinates to an new address entry.

    TODO Use it as a celery task
    """
    from geolocation.models import Address

    address = Address.objects.get(pk=pk)
    location = GeoCoder()
    location.get_coordinates(address=address.full_address)
    address.set_coordinates(location.lat, location.lon)
    return address


class GeoJSONSerializer(Serializer):
    def end_object(self, obj):
        for field in self.selected_fields:
            if field == "pk" or field in self._current.keys():
                continue
            # elif field in self._current.keys():
            #     continue
            if field == "jobs_info":
                try:
                    # select only the first job entry to company information
                    job_info = obj.jobs.all()[0]
                    self._current["company_name"] = job_info.company_name
                    self._current["opening_positions"] = obj.jobs.count()
                # FIXME: Remove IndexError. It happens when there is a address without
                # job. It should not happen, as we are forcing create address and job at the same time inside a transaction
                except (IndexError, AttributeError):
                    continue
        super().end_object(obj)


serializer = GeoJSONSerializer()

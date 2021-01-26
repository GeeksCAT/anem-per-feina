import random
from functools import lru_cache

from geopy.geocoders import Nominatim

from django.contrib.gis.geos import Point
from django.contrib.gis.serializers.geojson import Serializer
from django.db import IntegrityError

CoordinatesNotFound = AttributeError


class GeoCoder:
    def __init__(self, user_agent="nem per feina", **kwargs) -> None:
        """
        user_agent: should be our app name
        **kwargs: Any valid key word argument to be passed to Nominatim.
        https://geopy.readthedocs.io/en/stable/#geopy.geocoders.Nominatim
        """
        self.lon: float
        self.coordinates: list
        self.lat: float
        self.geo_point: Point
        self.geolocator = Nominatim(user_agent=user_agent, **kwargs)

    @lru_cache()
    def get_coordinates(self, address, **kwargs) -> None:
        """
        Get address coordinates using OSM Nominatim.

        **kwargs: Any Nominatim.geocode valid keyword argument.
        https://geopy.readthedocs.io/en/stable/#geopy.geocoders.Nominatim.geocode

        Search API fields: https://nominatim.org/release-docs/develop/api/Search/
        """
        try:
            location = self.geolocator.geocode(address, **kwargs)
            self.lat = location.latitude
            self.lon = location.longitude
            self.geo_point = Point(location.latitude, location.longitude)
        except CoordinatesNotFound:
            raise CoordinatesNotFound(f"Was not possible find coordinates for address:{address}")
        else:
            return self

    @classmethod
    def coordinates_offset(cls, lat, lon):
        """Add a small value to the current latitude and longitude.

        Used when there is already an address with the same coordinates on the database.
        """
        lat += random.uniform(0.0001, 0.001)
        lon += random.uniform(0.0001, 0.001)
        return lat, lon


def add_coordinates_to_address(pk: int):
    """Helper function do generate coordinates from a new address entry."""
    from geolocation.models import Address

    location = GeoCoder()

    address = Address.objects.get(pk=pk)
    try:
        location.get_coordinates(address=address.full_address)
    except CoordinatesNotFound:
        # If it fails to get the coordinates from the original address, we try again but only
        # using the city and country.
        # We lose precision, but still possible get some geographic information about the job offer.
        location.get_coordinates(address=f"{address.city}, {address.country}")
    lat = location.lat
    lon = location.lon
    while True:
        try:
            address._set_coordinates(lat, lon)
            break
        except IntegrityError:
            lat, lon = GeoCoder.coordinates_offset(lat, lon)
    return address


class GeoJSONSerializer(Serializer):
    def end_object(self, obj):
        for field in self.selected_fields:
            if field == "pk" or field in self._current.keys():
                continue
            if field == "jobs_info":
                try:
                    # select only the first job entry to get company information
                    job_info = obj.jobs.all()[0]
                    self._current["company_name"] = job_info.company_name
                    self._current["opening_positions"] = obj.jobs.count()

                except (IndexError, AttributeError):
                    # FIXME: IndexError: Is raised when there is an address without a job.
                    # TODO: Delete address if there isn't any job realted with it.
                    continue
        super().end_object(obj)


geojson_serializer = GeoJSONSerializer()

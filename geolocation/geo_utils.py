import random
from functools import lru_cache
from typing import Callable

from geopy.geocoders import Nominatim

from django.contrib.gis.geos import Point
from django.db import models, transaction

CoordinatesNotFound = AttributeError


class GeoCoder:
    def __init__(self, user_agent="nem per feina", **kwargs) -> None:
        """
        user_agent: Should be our app name
        **kwargs: Any valid key word argument to be passed to Nominatim.
        https://geopy.readthedocs.io/en/stable/#geopy.geocoders.Nominatim
        """
        self.lon: float
        self.coordinates: list
        self.lat: float
        self.geo_point: Point
        self.geolocator = Nominatim(user_agent=user_agent, **kwargs)

    @lru_cache()
    def _get_coordinates(self, address: str, **kwargs) -> None:
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

    def from_address_to_coordinates(self, address: "models.Model", _retring=False):
        """Convert a address to coordinates.

        Retring by default is false, as it used to check if we are calling the service
        for first time.

        """
        default_coordinates = (41.98, 2.82)
        try:
            self._get_coordinates(address=address.full_address)
        except CoordinatesNotFound:
            if _retring:
                return default_coordinates
            # If it fails to get the coordinates from the original address, we try again but
            # only using the city and country values.
            # We set 'retring' to True to ensure that if it fails again to get the coordinates, it will fallback to a default position.
            # We lose precision, but is still possible display the job on map.
            self._get_coordinates(address=f"{address.city}, {address.country}", retring=True)

        return self.lat, self.lon


def add_coordinates_to_address(pk: int):
    """Helper function do generate coordinates to an new address entry."""
    from geolocation.models import Address

    address = Address.objects.get(pk=pk)
    location = GeoCoder()
    location.from_address_to_coordinates(address=address)
    address.set_coordinates(location.lat, location.lon)
    return address


def check_duplicated_coordinates() -> Callable:
    # keep track of the previous analyzed coordinates
    coords_list = set()

    def offset_if_needed(lon: float, lat: float) -> tuple:
        """Offset duplicated coordinates.

        This allows display on map jobs from more than one company if they have the same
        coordinates without one overlap the other.
        """
        nonlocal coords_list
        if (lon, lat) in coords_list:
            # we offset to avoid overlay of points on map
            lon += random.uniform(0.0001, 0.001)
            lat += random.uniform(0.0001, 0.001)
        coords_list.add((lon, lat))
        return lon, lat

    return offset_if_needed

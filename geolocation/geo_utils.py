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
    def get_coordinates(self, address: str, **kwargs) -> None:
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
            self.get_coordinates(address=address.full_address)
        except CoordinatesNotFound:
            if _retring:
                return default_coordinates
            # If it fails to get the coordinates from the original address, we try again but
            # only using the city and country values.
            # We set 'retring' to True to ensure that if it fails again to get the coordinates, it will fallback to a default position.
            # We lose precision, but is still possible display the job on map.
            self.get_coordinates(address=f"{address.city}, {address.country}", retring=True)

        return self.lat, self.lon


def _address_resolver(new_address: "models.Model", db_address: "models.Model") -> "models.Model":
    """Compare the last address from a job post with the one returned from the database.

    Returns a database address to be add to the new job offer.
    """
    # Will happen when is new address on the database
    # Or is a job form update without change the address information
    if new_address == db_address:
        return db_address

    # If all condition are True, we are dealing with a new job
    # from a company which is address is already in our database
    if all(
        [
            new_address.has_coordinates(),
            new_address.user == db_address.user,
            new_address.full_address == db_address.full_address,
        ]
    ):
        # we delete the new address entry because it's already on the database
        with transaction.atomic():
            new_address.delete()
        return db_address
    # is a new address from a different user
    return new_address


def add_address_to_job(address_id: int, job_id: int):
    from geolocation.models import Address
    from jobsapp.models import Job

    location = GeoCoder()
    new_address = Address.objects.get(pk=address_id)
    job = Job.objects.get(pk=job_id)
    lat, lon = location.from_address_to_coordinates(new_address)
    job_address = new_address.set_coordinates(lat, lon)
    address = _address_resolver(new_address, job_address)
    # They can be the same in case of a job form update without change job address
    # Or when is a new address
    with transaction.atomic():
        job.set_address(address)
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

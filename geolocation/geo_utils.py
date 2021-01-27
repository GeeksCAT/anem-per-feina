import random
from functools import lru_cache

from geopy.geocoders import Nominatim

from django.contrib.gis.geos import Point
from django.db import IntegrityError, transaction

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


def add_address_to_job(address_id, job_id):
    """Helper function do add address to a new job entry."""
    from geolocation.models import Address
    from jobsapp.models import Job

    location = GeoCoder()

    address = Address.objects.get(pk=address_id)

    job = Job.objects.get(pk=job_id)
    try:
        location.get_coordinates(address=address.full_address)
    except CoordinatesNotFound:
        # If it fails to get the coordinates from the original address, we try again but
        # only using the city and country values.
        # We lose precision, but is still possible get some geographic information about the job offer.
        location.get_coordinates(address=f"{address.city}, {address.country}")

    lat = location.lat
    lon = location.lon

    try:
        with transaction.atomic():
            address.set_coordinates(lat, lon)

    # Will be raised if user with same coordinates already exist on the database
    except IntegrityError:
        # Get record with same coordinates from database
        db_address = Address.objects.get(lat=lat, lon=lon, user=address.user)

        # They can be the same in case of a job form update
        if db_address == address:
            return address

        # Otherwise we simply add the new job offer to the address from database
        with transaction.atomic():
            db_address.add_job(job)
            # remove the 'new address' because it's already on the database
            address.delete()
        return db_address

    else:
        with transaction.atomic():
            job.set_address(address)
    return address


def check_coordinates() -> object:
    # keep track of the previous analyzed coordinates
    coords_list = []

    def offset_if_needed(lon: float, lat: float) -> tuple:
        """Offset duplicated coordinates.

        This allows display on map jobs from more than one company if they have the same coordinates
        without one overlap the other.
        """
        nonlocal coords_list
        if (lon, lat) in coords_list:
            # we offset to avoid overlay of points on map
            lon += random.uniform(0.0001, 0.001)
            lat += random.uniform(0.0001, 0.001)
        coords_list.append((lon, lat))
        return lon, lat

    return offset_if_needed

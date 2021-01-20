from geopy.geocoders import Nominatim

from django.contrib.gis.geos import Point

CoordinatesNotFound = AttributeError


class GeoCoder:
    def __init__(self, user_agent="nem per feina", **kwargs) -> None:
        self.lon: float
        self.coordinates: list
        self.lat: float
        self.geo_point: Point
        self.geolocator: "Nominatim" = Nominatim(user_agent=user_agent, **kwargs)
        self.address: str

    def get_coordinates(
        self,
        *,
        city: str,
        country: str,
        street: str = "",
        county: str = "",
        state: str = "",
        postalcode: str = "",
    ) -> None:
        """
        Get address coordinates using OSM Nominatim.

        Search API fields: https://nominatim.org/release-docs/develop/api/Search/
        """

        # build address with as much information as possible using OSM address structure
        address = f"{street}, {city}, {county}, {state}, {postalcode}, {country}".strip()
        location = self.geolocator.geocode(address)
        try:
            self.lat = location.latitude
            self.lon = location.longitude
            self.geo_point = Point(location.latitude, location.longitude)
        except CoordinatesNotFound:
            raise CoordinatesNotFound(f"Was not possible find coordinates for address {address}")

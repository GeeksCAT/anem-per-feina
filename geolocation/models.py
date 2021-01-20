from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


class Address(geo_models.Model):
    street = geo_models.CharField(verbose_name=_("Street"), max_length=128, null=True, blank=True)
    number = geo_models.CharField(
        verbose_name=_("Door Number"), max_length=16, null=True, blank=True
    )
    city = geo_models.CharField(verbose_name=_("City"), max_length=128, db_index=True)
    # comarca
    county = geo_models.CharField(verbose_name=_("County"), max_length=128, null=True, blank=True)
    # CCAA
    state = geo_models.CharField(verbose_name=_("State"), max_length=64, null=True, blank=True)
    country = geo_models.CharField(verbose_name=_("Country"), max_length=64, db_index=True)
    postalcode = geo_models.CharField(
        verbose_name=_("Postal Code"), max_length=16, null=True, blank=True
    )
    lat = geo_models.FloatField(verbose_name=_("Latitude"), null=True)
    lon = geo_models.FloatField(verbose_name=_("Longitude"), null=True)
    geo_point = geo_models.PointField(null=True)

    @property
    def full_address(self) -> str:
        """Return a valid complete address that can be used to get coordinates points."""
        return f"{self.street} {self.number}, {self.city}, {self.county}, {self.state}, {self.postalcode}, {self.country}".replace(
            "None", ""
        )

    def __str__(self) -> str:
        return f"{self.street} {self.number}, {self.city}, {self.country}"

    def set_coordinates(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.geo_point = Point(lat, lon)
        self.save()

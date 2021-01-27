from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.db import models, transaction
from django.utils.translation import gettext as _

from geolocation.managers import AddressQuerySet

User = get_user_model()


class Address(geo_models.Model):
    user = geo_models.ForeignKey(
        User,
        on_delete=geo_models.CASCADE,
        verbose_name=_("User"),
        help_text=_("User address."),
        related_name="addresses",
        blank=True,
        null=True,
    )
    street = geo_models.CharField(verbose_name=_("Street"), max_length=128, null=True, blank=True)
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
    geo_point = geo_models.PointField(null=True, srid=settings.SRID)
    objects = AddressQuerySet.as_manager()

    class Meta:
        unique_together = ("lat", "lon", "user")

    def __str__(self) -> str:
        return ", ".join(
            [
                field
                for field in (self.street, self.city, self.county, self.country)
                if field is not None
            ]
        )

    @property
    def full_address(self) -> str:
        """Return a valid address that can be used to get coordinates points.

        We keep the empty places which may help on the coordinates lookup.
        """
        return f"{self.street}, {self.city}, {self.county}, {self.state}, {self.postalcode}, {self.country}".replace(
            "None", ""
        )

    def set_coordinates(self, lat, lon) -> None:
        """Add coordinates to database record.

        It will raise an IntegrityError if there is already an address with the same coordinates.
        """
        self.lat = lat
        self.lon = lon
        self.geo_point = Point(lon, lat)
        self.save()

    def add_job(self, job_instance):
        self.jobs.add(job_instance)
        return self

    def has_coordinates(self) -> bool:
        """Helper method to check if address is valid by ensuring if it has or not coordinates."""
        return all(
            [
                isinstance(self.lat, float),
                isinstance(self.lon, float),
                isinstance(self.geo_point, Point),
            ]
        )


class Map(Address):
    class Meta:
        proxy = True

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.db import transaction
from django.db.models import fields
from django.utils.translation import _gettext as _

from geolocation.managers import AddressQuerySet
from geolocation.tasks import add_coordinates_to_address

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
    objects = AddressQuerySet.as_manager()

    def __str__(self) -> str:
        return ", ".join(
            [
                field
                for field in (self.street, self.number, self.city, self.county, self.country)
                if field is not None
            ]
        )

    @property
    def full_address(self) -> str:
        """Return a valid address that can be used to get coordinates points.

        We keep the empty places which may help on the coordinates lookup.
        """
        return f"{self.street} {self.number}, {self.city}, {self.county}, {self.state}, {self.postalcode}, {self.country}".replace(
            "None", ""
        )

    def set_coordinates(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.geo_point = Point(lat, lon)
        self.save()

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Save a new address record to the database."""
        if self._state.adding:
            super().save(*args, **kwargs)
            # We run a background task to add coordinates information the address record.
            transaction.on_commit(
                lambda: add_coordinates_to_address.apply_async(kwargs={"pk": self.pk})
            )
            return self

        super().save(*args, **kwargs)


class Map(Address):
    class Meta:
        proxy = True

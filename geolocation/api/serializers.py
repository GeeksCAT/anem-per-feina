from rest_framework import serializers

from django.db.models import fields

from ..models import Address

# from jobsapp.api.serializers import JobSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ("geo_point",)

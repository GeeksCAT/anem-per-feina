from rest_framework import serializers

from django.db.models import fields

from ..models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

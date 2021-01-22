from rest_framework import serializers

from django.db.models import fields

from jobsapp.api.serializers import JobSerializer

from ..models import Address


class AddressSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True)

    class Meta:
        model = Address
        fields = "__all__"

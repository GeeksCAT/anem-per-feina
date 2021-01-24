from rest_framework import serializers

from django.utils.translation import _gettext as _

from accounts.api.serializers import UserSerializer
from geolocation.api.serializers import AddressSerializer
from geolocation.models import Address

from ..models import Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    geo_location = AddressSerializer()

    class Meta:
        model = Job
        fields = "__all__"

    def create(self, validated_data):
        address = validated_data.pop("geo_location")
        geo_location = Address.objects.create(**address)
        job = Job.objects.create(**validated_data, geo_location=geo_location)
        return job


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128, help_text=_("Please insert your name"))
    from_email = serializers.EmailField(max_length=256, help_text=_("Please insert your email"))
    subject = serializers.CharField(max_length=256, help_text=_("Reason why you are contact us"))
    message = serializers.CharField(help_text=_("Your message"))

from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from ..models import Job


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

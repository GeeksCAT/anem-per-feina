from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from ..models import Job


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


class ApplicantSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Applicant
        fields = "__all__"


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128, help_text="Please insert your name")
    email = serializers.EmailField(max_length=256, help_text="Please insert your email")
    subject = serializers.CharField(max_length=256, help_text="Reason why you are contact us")
    message = serializers.CharField(help_text="Your message")

from rest_framework import serializers

from django.utils.translation import ugettext as _

from accounts.api.serializers import UserSerializer

from ..models import Job


class JobSerializer(serializers.ModelSerializer):
    # FIXME: Do we need this?
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128, help_text=_("Please insert your name"))
    from_email = serializers.EmailField(max_length=256, help_text=_("Please insert your email"))
    subject = serializers.CharField(max_length=256, help_text=_("Reason why you are contact us"))
    message = serializers.CharField(help_text=_("Your message"))

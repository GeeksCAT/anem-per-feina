from django_bleach.models import BleachField
from tinymce.models import HTMLField

from django.conf import settings
from django.core.validators import URLValidator
from django.db.models import URLField
from django.forms.fields import URLField as FormURLField

################
# JobsURLField #
################

JobsURLValidator = URLValidator(schemes=settings.URL_SCHEMES)


class JobsURLFormField(FormURLField):
    """Form URLField with custom SCHEMES from settings.URL_SCHEMES"""

    default_validators = [JobsURLValidator]


class JobsURLField(URLField):
    """URLField with custom SCHEMES from settings.URL_SCHEMES"""

    default_validators = [JobsURLValidator]

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": JobsURLFormField,
            }
        )


######################
# SanitizedHTMLField #
######################


class SanitizedHTMLField(HTMLField, BleachField):
    description = "Sanitized HTML field"

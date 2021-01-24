from django import forms
from django.core import validators
from django.utils.translation import _gettext_lazy as _

from jobsapp.models import Job

from .utils import contact_us_email


class CreateJobForm(forms.ModelForm):
    policies = forms.BooleanField()

    class Meta:
        model = Job
        exclude = ("user", "created_at", "location")
        labels = {
            "last_date": _("Last Date"),
            "company_name": _("Company Name"),
            "company_description": _("Company Description"),
        }


class EditJobForm(CreateJobForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["policies"]


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=128,
        help_text=_("Please insert your name"),
    )
    email = forms.EmailField(
        label=_("Email"),
        max_length=256,
        help_text=_("Please insert your email"),
        validators=[validators.validate_email],
    )
    subject = forms.CharField(
        label=_("Subject"),
        max_length=256,
        help_text=_("Reason why you are contact us"),
    )
    message = forms.CharField(
        label=_("Message"),
        max_length=2048,
        widget=forms.Textarea,
        help_text=_("Your message"),
    )

    def send_email(self) -> None:
        # send email using the self.cleaned_data dictionary
        contact_us_email(self.cleaned_data)

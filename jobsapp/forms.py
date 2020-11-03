from django import forms
from django.core import validators
from django.utils.translation import gettext as _

from jobsapp.models import Job

from .utils import contact_us_email


class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ("user", "created_at")


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = (
            "user",
            "created_at",
        )
        labels = {
            "last_date": _("Last Date"),
            "company_name": _("Company Name"),
            "company_description": _("Company Description"),
        }

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class ContactForm(forms.Form):
    name = forms.CharField(max_length=128, help_text=_("Please insert your name"))
    email = forms.EmailField(
        max_length=256,
        help_text=_("Please insert your email"),
        validators=[validators.validate_email],
    )
    subject = forms.CharField(max_length=256, help_text=_("Reason why you are contact us"))
    message = forms.CharField(max_length=2048, widget=forms.Textarea, help_text=_("Your message"))

    def send_email(self) -> None:
        # send email using the self.cleaned_data dictionary
        contact_us_email(self.cleaned_data)

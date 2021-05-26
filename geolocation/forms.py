from django import forms
from django.db.models import fields

from .models import Address


class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street", "city", "postalcode", "county", "state", "country"]

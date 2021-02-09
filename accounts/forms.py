from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

from accounts.models import User

GENDER_CHOICES = (("male", "Male"), ("female", "Female"))


class EmployerRegistrationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = _("Company Name")
        self.fields["last_name"].label = _("Company Address")
        self.fields["password1"].label = _("Password")
        self.fields["password2"].label = _("Confirm Password")

        self.fields["first_name"].widget.attrs.update(
            {
                "placeholder": _("Enter Company Name"),
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "placeholder": _("Enter Company Address"),
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": _("Enter Email"),
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": _("Enter Password"),
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": _("Confirm Password"),
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]
        error_messages = {
            "first_name": {
                "required": _("First name is required"),
                "max_length": _("Name is too long"),
            },
            "last_name": {
                "required": _("Last name is required"),
                "max_length": _("Last Name is too long"),
            },
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields["email"].widget.attrs.update({"placeholder": _("Enter Email")})
        self.fields["password"].widget.attrs.update({"placeholder": _("Enter Password")})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError(_("User Does Not Exist."))
            if not self.user.check_password(password):
                raise forms.ValidationError(_("Password Does not Match."))
            if not self.user.is_active:
                raise forms.ValidationError(_("User is not Active."))

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user

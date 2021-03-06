from typing import List, Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from accounts.managers import UserManager

GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_CHOICES: Tuple[Tuple[str, str], ...]
GENDER_CHOICES = (("male", "Male"), ("female", "Female"))


class User(AbstractUser):
    username = None
    gender = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="",
        verbose_name=_("Gender"),
        help_text=_("User gender."),
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
        verbose_name=_("Email"),
        help_text=_("User email, also used as username."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    def __str__(self) -> str:
        return self.email

    # TODO: Solve mypy error
    objects = UserManager()  # type: ignore

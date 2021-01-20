import datetime

import factory
from factory import fuzzy
from faker import Faker

from django.views.generic.dates import timezone_today

from accounts.models import User
from geolocation.models import Address
from jobsapp.models import Job

faker = Faker("es_ES")


# List of factories
class UserFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = User
        django_get_or_create = ("first_name", "last_name")

    first_name = factory.Faker("first_name", locale="es_ES")
    last_name = "Doe"
    email = factory.Faker("email", locale="es_ES")


class JobFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = Job

    user = factory.SubFactory("tests.factories.UserFactory")
    title = factory.Sequence(lambda n: f"Title {n}")
    location = factory.Faker("address", locale="es_ES")
    company_name = factory.Faker("company", locale="es_ES")
    company_description = factory.Faker("text", locale="es_ES")
    description = factory.Sequence(lambda n: f"Description {n}")
    last_date = timezone_today() + datetime.timedelta(days=10)
    website = factory.Faker("url", locale="es_ES")
    type = "1"
    category = fuzzy.FuzzyChoice([Job.CATEGORY_WEB_DESIGN, Job.CATEGORY_GRAPHIC_DESIGN])
    remote = fuzzy.FuzzyChoice([Job.REMOTE, Job.NO_REMOTE, Job.PARTIAL_REMOTE])


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    city = factory.Faker("city", locale="es_ES")
    country = "Spain"

import datetime
import random

import factory
from factory import fuzzy
from faker import Faker

from accounts.models import User
from jobsapp.models import NO_REMOTE, PARTIAL_REMOTE, REMOTE, Job

faker = Faker("es_ES")

# List of factories
class UserFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = User
        django_get_or_create = ("first_name", "last_name")

    first_name = "John"
    last_name = "Doe"
    email = factory.Sequence(lambda n: f"anem{n}@anem.cat")


class JobFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = Job

    user = factory.SubFactory("tests.factories.UserFactory")
    title = factory.Sequence(lambda n: f"Title {n}")
    location = faker.address()
    company_name = faker.company()
    company_description = faker.text()
    description = factory.Sequence(lambda n: f"Description {n}")
    last_date = datetime.datetime.now() + datetime.timedelta(days=10)
    website = faker.url()
    type = "1"
    category = fuzzy.FuzzyChoice(["Senior", "Junior", "Manager"])
    remote = fuzzy.FuzzyChoice([REMOTE, NO_REMOTE, PARTIAL_REMOTE])

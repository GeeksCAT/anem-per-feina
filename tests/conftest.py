from pytest_factoryboy import register

from django.conf import settings

from tests.factories import JobFactory, UserFactory

# Register factories to pytest global namespace.
# They can be access as normal fixtures using user_factory or job_factory.
register(UserFactory)
register(JobFactory)


def pytest_configure():
    """
    Use for override default settings
    https://pytest-django.readthedocs.io/en/latest/configuring_django.html#using-django-conf-settings-configure
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

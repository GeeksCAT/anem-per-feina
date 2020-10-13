import os
from datetime import timedelta

import environ
from collections import OrderedDict

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = "@pzqp#x^+#(olu#wy(6=mi9&a8n+g&x#af#apn07@j=5oin=xb"

DEBUG = env.bool("DEBUG", default=False)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_elasticsearch_dsl",
    "drf_yasg",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "jobsapp",
    "accounts",
    "constance",
    "constance.backends.database",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "jobs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "jobs.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": env.db(),
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
# ALLOWED_HOSTS = ['django-portal.herokuapp.com', .backends.database'localhost', 'jobs.manjurulhoque.com', '127.0.0.1', 'localhost:3000']
# cors config
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ["*"]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "accounts.user"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.authentication.TokenAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "EXCEPTION_HANDLER": "jobsapp.api.custom_exception.custom_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "when": "D",  # this specifies the interval
            "interval": 1,  # defaults to 1, only necessary for other values
            "backupCount": 100,  # how many backup file to keep, 10 days
        }
    },
    "loggers": {
        "django": {"handlers": ["file"], "level": "INFO", "propagate": True},
        "project": {"handlers": ["file"], "level": "INFO", "propagate": True},
        "": {"handlers": ["file"], "level": "INFO", "propagate": True},
    },
}


ELASTIC_HOST_NAME = env.str("ELASTIC_HOST_NAME", default="localhost")
ELASTIC_HOST_PORT = env.str("ELASTIC_HOST_PORT", default="9200")


ELASTICSEARCH_DSL = {
    "default": {
        "hosts": f"{ELASTIC_HOST_NAME}:{ELASTIC_HOST_PORT}",
    },
}

# Documentation
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}},
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


CONSTANCE_CONFIG = {
    'SITE_NAME': ('My Title', 'Website title'),
    'SITE_DESCRIPTION': ('', 'Website description'),
    'JOBS_URL': ('', 'URL Jobs'),
}
CONSTANCE_CONFIG_FIELDSETS = {
    'General Configuration Service': {
        'fields': ('SITE_NAME', 'SITE_DESCRIPTION'),
    },
    'Jobs Configuration Service': {
        'fields': ('JOBS_URL',),
    }
}
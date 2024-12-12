from .base import *
from django.core.management.utils import get_random_secret_key
import environ
import os

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env.str("DJANGO_SECRET_KEY", get_random_secret_key())
DEBUG = env.bool("DJANGO_DEBUG", True)

INSTALLED_APPS += [
    "rest_framework",
    "rest_framework.authtoken",
    "silk",
    "drf_spectacular",
]

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.postgresql"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project Name",
    "DESCRIPTION": "Your Project Description",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": "/api/",
}

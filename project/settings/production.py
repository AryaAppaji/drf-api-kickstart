from .base import *

import environ
import os

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

TIME_ZONE = env.str("TIME_ZONE", "Asia/Kolkata")
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", False)

INSTALLED_APPS += [
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "django_sonar",
    "drf_spectacular",
    "custom_commands",
]

MIDDLEWARE += [
    "django_sonar.middlewares.requests.RequestsMiddleware",
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",  # Capture all logs from DEBUG and above
            "class": "logging.FileHandler",
            "filename": "django.log",
            "formatter": "verbose",  # Use the detailed formatter
        },
    },
    "root": {
        "handlers": ["file"],  # Attach the file handler to capture all logs
        "level": "DEBUG",  # Capture all logs starting from DEBUG
    },
    "loggers": {
        "django": {
            "handlers": [
                "file"
            ],  # Attach the file handler for Django-specific logs
            "level": "DEBUG",  # Capture all logs starting from DEBUG
            "propagate": True,
        },
    },
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

DJANGO_SONAR = {
    "excludes": [
        "/sonar/",
        "/admin/",
        "/__reload__/",
    ],
}

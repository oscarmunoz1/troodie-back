"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from dotenv import load_dotenv
from decouple import config
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [config("ALLOWED_HOSTS")]

CSRF_TRUSTED_ORIGINS = [config("CSRF_TRUSTED_ORIGINS")]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework_simplejwt",
    "whitenoise.runserver_nostatic",
    "corsheaders",
    "users",
    "company",
    "product",
    "history",
    "reviews",
    "common",
    # django-allauth apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",  # for Google OAuth 2.0
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

AUTH_USER_MODEL = "users.User"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("users.auth.CustomAuthentication",),
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

GEOIP_PATH = os.path.join(Path(__file__).resolve().parent.parent.parent, "geoip_data")

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DATABASE_NAME"),
#         "USER": config("DATABASE_USER"),
#         "PASSWORD": config("DATABASE_PASSWORD"),
#         "HOST": config("DATABASE_HOST"),
#         "PORT": config("DATABASE_PORT"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "traceitdb",
        "USER": "postgres",
        "PASSWORD": "PlazaFlores_",
        "HOST": "traceit-database.cox3o9tj0v96.us-east-2.rds.amazonaws.com",
        "PORT": "5432",
    }
}

AWS_ACCESS_KEY_ID = "AKIAQGLIFETF2HN67DMN "
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "traceit-bucket"
AWS_S3_SIGNATURE_NAME = ("s3v4",)
AWS_S3_REGION_NAME = "us-east-2"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


LOGGING = {
    # Version del logging
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s | %(name)s | "
            "%(module)s | %(funcName)s | %(lineno)d | %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    # Se definen dos handlers para develop: Console y File.
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    # Se redefinen dos loggers para satisfacer los requisitos
    "loggers": {
        "backend": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        "": {
            "handlers": [
                "console",
            ],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR.parent / "static"

# The URL to use when referring to static files (where they will be served from)
STATIC_URL = "/static/"

# STATICFILES_DIRS = [os.path.join(BASE_DIR.parent, "static")]

# Simplified static file serving.
# https://pypi.org/project/whitenoise/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CORS settings

CORS_ALLOW_CREDENTIALS = True

# django-allauth settings

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1
LOGIN_REDIRECT_URL = "/"


# Additional configuration settings
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

JWT_EXPIRATION_DELTA = timedelta(seconds=20)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    # custom
    "AUTH_COOKIE": "access",  # Cookie name. Enables cookies if value is set.
    "AUTH_COOKIE_DOMAIN": None,  # A string like "example.com", or None for standard domain cookie.
    "AUTH_COOKIE_SECURE": True,  # Whether the auth cookies should be secure (https:// only).
    "AUTH_COOKIE_HTTP_ONLY": True,  # Http only cookie flag.It's not fetch by javascript.
    "AUTH_COOKIE_PATH": "/",  # The path of the auth cookie.
    "AUTH_COOKIE_SAMESITE": "None",  # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
}

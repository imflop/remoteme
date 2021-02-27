"""
Django settings for remoteme project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

import environ
import sentry_sdk
from celery.schedules import crontab
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

PROJECT_DIR = environ.Path(__file__) - 1
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
env.read_env(os.path.join(PROJECT_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Sitemap
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'taggit',
    'django_select2',
    'django_filters',
]

LOCAL_APPS = [
    'settings',
    'jobs',
    'users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'remoteme.urls'

TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [f'{BASE_DIR}/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': '',
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'remoteme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# ------------------------------------------------------------------------------
DATABASES = {
    'default': env.db()
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# ------------------------------------------------------------------------------

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


EMPTY_CHOICE_LABEL = 'Не выбрано'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
# ------------------------------------------------------------------------------

STATIC_URL = '/assets/'

STATIC_ROOT = f'{BASE_DIR}/staticfiles'

STATICFILES_DIRS = [f'{BASE_DIR}/assets']


# DJANGO DEBUG TOOLBAR
# ------------------------------------------------------------------------------
if DEBUG:
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)
else:
    # Sentry CONFIGURATION
    # ------------------------------------------------------------------------------
    sentry_sdk.init(
        dsn=env.str('SENTRY_DSN', default=''),
        integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )


# TAGGIT
# ------------------------------------------------------------------------------
TAGGIT_CASE_INSENSITIVE = True


# CACHE
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': env.CACHE_SCHEMES['rediscache'],
        'LOCATION': f'{env.str("REDIS_URL")}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PICKLE_VERSION': -1
        },
        'KEY_PREFIX': 'remoteme'
    },
    'select2': {
        'BACKEND': env.CACHE_SCHEMES['rediscache'],
        'LOCATION': f'{env.str("REDIS_URL")}/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PICKLE_VERSION': -1
        },
        'KEY_PREFIX': 'select2'
    },
}


# SELECT2
# ------------------------------------------------------------------------------
SELECT2_CACHE_BACKEND = "select2"


# CELERY
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = f'{env.str("REDIS_URL")}/0'
result_backend = f'{env.str("REDIS_URL")}/0'
accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'
timezone = TIME_ZONE
# TODO: move to celery.py
CELERY_BEAT_SCHEDULE = {
    'parser-5-min-after-midnight': {
        'task': 'jobs.tasks.load_hh_data',
        'schedule': crontab(minute=5, hour=0),
    },
}


# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] [%(funcName)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'remoteme': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

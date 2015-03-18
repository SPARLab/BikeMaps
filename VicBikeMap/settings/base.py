"""
Django settings for VicBikeMap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Import all forum settings
from spirit.settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'minidetector.Middleware'
)

ROOT_URLCONF = 'VicBikeMap.urls'

WSGI_APPLICATION = 'VicBikeMap.wsgi.application'

LOGIN_REDIRECT_URL = 'mapApp:index'

POSTGIS_VERSION = (2,1,3)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Application definitions
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # forum
    'spirit',
    'haystack',
    'djconfig',

    # mapApp requirements
    'compressor',
    'minidetector', # Mobile detector
    'django_cron', # Cron tasks
    'django.contrib.gis',
    'djgeojson',
    'crispy_forms',
    'mapApp'
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SERIALIZATION_MODULES = {
    'geojson' : 'djgeojson.serializers'
}

CRON_CLASSES = [
    "mapApp.cron.UserAlertEmails",
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

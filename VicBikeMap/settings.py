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
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$e05l@n&nv*zh@m=4dgx8j-rj^$w2ugj%$&*99=p$vwd5%ya53'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = []


# Application definition

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
    'django.contrib.gis',
    'crispy_forms',
    'mapApp'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)

ROOT_URLCONF = 'VicBikeMap.urls'

WSGI_APPLICATION = 'VicBikeMap.wsgi.application'

LOGIN_REDIRECT_URL = 'spirit:profile-update'

# Database
DATABASES = {
    'default': {
        # PostgreSQL database connection on Taylor's Windows computer
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'OPTIONS': {'charset': 'utf8mb4'},
        'NAME': 'bikeDB',
        'USER': 'postgres'
        # 'PASSWORD': 'SUPER_SECRET'

        
    }
}

POSTGIS_VERSION = (2,1,3)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = (
    STATIC_PATH,

)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bikemaps.org@gmail.com'
EMAIL_HOST_PASSWORD = 'secret'

SERIALIZATION_MODULES = {
    'geojson' : 'djgeojson.serializers'
}
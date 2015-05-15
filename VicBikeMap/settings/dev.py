"""
Django settings for VicBikeMap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from VicBikeMap.settings.base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$e05l@n&nv*zh@m=4dgx8j-rj^$w2ugj%$&*99=p$vwd5%ya53'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

COMPRESS_ENABLED = False

# Database
DATABASES = {
    'default': {
        # PostgreSQL database connection on Taylor's Windows computer
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'bikeDB',
        'USER': 'postgres'
        # 'PASSWORD': 'SUPER_SECRET'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #Dummy backend for development that writes to stdout

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Enable logging to console with Django Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '../BikeMaps.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'mapApp': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'blogApp': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    },
}

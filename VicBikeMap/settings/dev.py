"""
Django settings for VicBikeMap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from VicBikeMap.settings.base import *
import os
if os.name == 'nt':
    import platform
    OSGEO4W = r"C:\OSGeo4W"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$e05l@n&nv*zh@m=4dgx8j-rj^$w2ugj%$&*99=p$vwd5%ya53'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        # PostgreSQL database connection on Taylor's Windows computer
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'bikemap_db',
        'USER': 'postgres',
        'PASSWORD': 'Spi9dlee6'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #Dummy backend for development that writes to stdout

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

RECAPTCHA_SECRET = '6LcFewcTAAAAADHaBcrGZ7jN16fXxPIEtB24s-gQ'

FORECAST_IO_API_KEY = 'debug'

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
        'userApp': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'blogApp': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    },
}

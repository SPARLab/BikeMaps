"""
Django settings for VicBikeMap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from VicBikeMap.settings.base import *

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
        # 'OPTIONS': {'charset': 'utf8mb4'},
        'NAME': 'bikeDB',
        'USER': 'postgres'
        # 'PASSWORD': 'SUPER_SECRET'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #Dummy backend for development that writes to stdout

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Cross Origin Access Control
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    )

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'X-CSRFToken'
)


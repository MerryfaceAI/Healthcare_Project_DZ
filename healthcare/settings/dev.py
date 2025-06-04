import os
from .base import *

#
# SECURITY
#

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-z&p9jj)575nzilby10^$g3e59shl)u(us++8+lr*v8dsr%#v#)'
)
DEBUG = True
ALLOWED_HOSTS = []

#
# Database (development)
#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ROOT_DIR / 'db.sqlite3',
    }
}

#
# CORS (development)
#

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]

#
# Cookie security (development)
#

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

#
# Security hardening (can be relaxed in dev)
#

SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# healthcare/settings/base.py

import os
from pathlib import Path

# ROOT_DIR is the folder that holds manage.py
ROOT_DIR = Path(__file__).resolve().parents[2]

# BASE_DIR is still your Django module folder
BASE_DIR = ROOT_DIR / 'healthcare'

#
# Application definition
#

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'django_apscheduler',
    'django_extensions',
    'django_filters',
]

LOCAL_APPS = [
    'patients',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',           # CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'healthcare.middleware.CurrentUserAndAuditMiddleware',
]

ROOT_URLCONF = 'healthcare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ROOT_DIR / 'patients' / 'templates',
            ROOT_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'healthcare.wsgi.application'

#
# REST Framework
#

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My Healthcare API',
    'DESCRIPTION': 'REST API for patient records, scheduling, notifications, and more',
    'VERSION': '1.0.0',
}

#
# Internationalization & Timezone
#

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

#
# Static files
#

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    ROOT_DIR / 'static',
    # Comment out the React build folder until you run `npm run build`
    # ROOT_DIR / 'my-healthcare-ui' / 'dist',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# DEBUG printout
print("BASE_DIR =", BASE_DIR)

#
# Default primary key field type
#

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#
# Redirects
#

LOGIN_REDIRECT_URL = '/patients/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

#
# Logging (common)
#

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {module}:{lineno} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': ROOT_DIR / 'logs' / 'app.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'patients': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

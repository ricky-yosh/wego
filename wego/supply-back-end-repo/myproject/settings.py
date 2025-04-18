"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import config
import os
from pymongo import MongoClient

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.DEBUG

ALLOWED_HOSTS = [
    'team-12.seuswe.rocks',
    'www.team-12.seuswe.rocks',
    'team-12.supply.seuswe.rocks',
    'www.team-12.supply.seuswe.rocks',
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
    #"supply-back-end-repo-map-services-1",
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.decorators',
    'rest_framework_swagger',
    'drf_yasg',
    'corsheaders',
    'django.contrib.gis',

    # Django Apps
    'fleet',
    'dispatcher',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

client = MongoClient('mongodb://localhost:27017/')
db = client['fleetdb']

ENV = os.getenv('DJANGO_ENV', 'production')

if ENV == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'fleetdb',  # MongoDB database name
            'ENFORCE_SCHEMA': False,
            'CLIENT': {
                'host': os.getenv('DATABASE_HOST', 'mongodb://localhost:27017'),  # Your MongoDB host, change if different
                'username': 'fleet_admin',  # Optional: Your MongoDB username, if auth is enabled
                'password': config.DATABASE_PASSWORD,  # Optional: Your MongoDB password, if auth is enabled
                'authSource': 'admin',  # MongoDB authentication database, adjust if different
                'authMechanism': 'SCRAM-SHA-1',  # Optional: Your MongoDB auth mechanism
            },
        },
    }
elif ENV == 'development':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    "https://team-12.supply.seuswe.rocks", # Supply Fe
    "http://localhost:9000", # Supply Backend
]
CORS_ALLOW_ALL_ORIGINS = True 


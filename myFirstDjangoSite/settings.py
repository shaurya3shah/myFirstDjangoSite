"""
Django settings for myFirstDjangoSite project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os

import boto3
import environ
import sqlalchemy as db
from pathlib import Path

from myFirstDjangoSite.createDBModels import DBModels
from myFirstDjangoSite.constants import TABLE_NAME_GUESS_NUMBER, TABLE_NAME_NUMBERDLE, TABLE_NAME_CRAZYLIBS, \
    TABLE_NAME_USAGE, TABLE_NAME_FEEDBACK, TABLE_NAME_COUNTRIESCONNECTION

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r+^giro05+2efa(vtd11ayj8w&9dt!nkhfsmwtf^kuz#qk^x+i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sns.pythonanywhere.com', '127.0.0.1', 'www.snsfungames.com', 'snsfungames.com', 'https://www.snsfungames.com']

CSRF_TRUSTED_ORIGINS = ['sns.pythonanywhere.com', '127.0.0.1', 'www.snsfungames.com', 'snsfungames.com', 'https://www.snsfungames.com']

SESSION_COOKIE_DOMAIN = '.snsfungames.com'
# Application definition

INSTALLED_APPS = [
    'fun.apps.funConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'myFirstDjangoSite.urls'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

SESSION_SAVE_EVERY_REQUEST = True

CSRF_USE_SESSIONS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'myFirstDjangoSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

client = boto3.client(
    'dynamodb',
    aws_access_key_id=env("KEY_ID"),
    aws_secret_access_key=env("SECRET_ACCESS_KEY"),
    region_name="us-west-2"
)
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=env("KEY_ID"),
    aws_secret_access_key=env("SECRET_ACCESS_KEY"),
    region_name="us-west-2"
)

ddb_exceptions = client.exceptions

createDB = DBModels()

# createDB.createSimpleTimestampDB(TABLE_NAME_GUESS_NUMBER, client, ddb_exceptions)
# createDB.createSimpleTimestampDB(TABLE_NAME_NUMBERDLE, client, ddb_exceptions)
# createDB.createSimpleTimestampDB(TABLE_NAME_CRAZYLIBS, client, ddb_exceptions)
# createDB.createSimpleTimestampDB(TABLE_NAME_USAGE, client, ddb_exceptions)
# createDB.createSimpleTimestampDB(TABLE_NAME_FEEDBACK, client, ddb_exceptions)
# createDB.createSimpleTimestampDB(TABLE_NAME_COUNTRIESCONNECTION, client, ddb_exceptions)

if env("ENV") == "PROD":
    engine = db.create_engine("mysql://sns:connectdb@sns.mysql.pythonanywhere-services.com/sns$stocks")
else:
    engine = db.create_engine("mysql://root:Hello123!@localhost/stocks")


connection = engine.connect()

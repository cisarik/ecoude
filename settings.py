import os
import sys
from django import template

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(PROJECT_ROOT, 'lib'))

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('admin', 'cisary@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'ecoude'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'Gaia3bdsitat'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '3306'

TIME_ZONE = 'Europe/Bratislava'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')

MEDIA_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '04imt(&$ig13f-*7l*25*83-p2(1g%zn8-8qrmk&jf-45_0g)r'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'jsonrpcserver.JSONRPCServerMiddleware',
)

ROOT_URLCONF = 'ecoude_cooking.urls'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_ROOT, 'templates'),'.'
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.admin',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'ecoude_cooking.system',
)

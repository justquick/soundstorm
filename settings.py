import os,sys
WORKING_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(WORKING_DIR,'lib'))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Justin Quick', 'justquick@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'       
DATABASE_NAME = 'ss.db'         

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = os.path.join(WORKING_DIR, 'media')

MEDIA_URL =  '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bladeblabla'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'soundstorm.urls'

TDIR = os.path.join(WORKING_DIR,'templates')
if sys.platform.startswith('win'):
    TEMPLATE_DIRS = (TDIR.replace('\\','/'),)
else:
    TEMPLATE_DIRS = (TDIR,)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'song',
    'pagination',
    'audioplayer',
)

try:
    from song_settings import *
except ImportError:
    pass

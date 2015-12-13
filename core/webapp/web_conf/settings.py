"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e^#&p%z+4+e13#g8h#bk-6l0h)mj6i#u34)xk3cn1dv0g)@m^f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web_apps.home',
    'web_apps.user',
    'web_apps.node',
    'web_lib',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'web_conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'web_lib.context.base',
            ],
        },
    },
]

WSGI_APPLICATION = 'web_conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    STATIC_ROOT,
)

LOGIN_URL = '/user/login/'


# import sys
# WEBAPP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# FABFILE_DIR = os.path.dirname(os.path.dirname(os.path.join(BASE_DIR)))
# CORE_DIR = os.path.join(FABFILE_DIR, 'core')
# REPO_DIR = os.path.dirname(FABFILE_DIR)
# sys.path.extend([
#     WEBAPP_DIR,
#     CORE_DIR,
# ])

# from fabkit.conf import conf_base, conf_web  # noqa
# conf_base.init(FABFILE_DIR, REPO_DIR)

# REPO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.join(BASE_DIR))))
# INIFILE = os.path.join(REPO_DIR, 'fabfile.ini')

# CONFIG = ConfigParser.SafeConfigParser()
# CONFIG.read(INIFILE)
# NODE_DIR = os.path.join(REPO_DIR, CONFIG.get('common', 'node_dir'))
# NODE_META_PICKLE = os.path.join(NODE_DIR, 'meta.pickle')
# MAX_RECENT_CLUSTERS = CONFIG.getint('common', 'max_recent_clusters')
# FABSCRIPT_MODULE = os.path.join(REPO_DIR, CONFIG.get('common', 'fabscript_module'))
# MY_HOST = CONFIG.get('web', 'my_host')

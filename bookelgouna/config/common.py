# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Django settings for bookelgouna project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import join, dirname, abspath
import dj_database_url

BASE_DIR = dirname(dirname(__file__))

# Application definition

DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'allauth.socialaccount.providers.facebook',  # registration
    # 'floppyforms',
    'widget_tweaks',
    'rosetta',
    'easy_thumbnails',
    'image_cropping',
    'ckeditor',
    'hvad',
    'haystack',
    'adminsortable',
    'django_countries'
    # 'djcelery',
    # 'djcelery_email'
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'users',  # custom users app
    'core',
    'common',
    'hotels',
    'apartments',
    'excursions',
    'sports',
    'transport',
    'entertainment',
    'booking',
    'blog',
    'flatpages_i18n',
    'weatherapi',
    'email_templates'
    # Your stuff: custom apps go here
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # this position of LocaleDetectionMiddleware is important now cause it determines locale if not specified by user
    'users.middleware.LocaleDetectionMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'booking.middleware.CartMiddleware',
)
# END MIDDLEWARE CONFIGURATION

# MIGRATIONS CONFIGURATION
MIGRATION_MODULES = {
    'sites': 'contrib.sites.migrations',
    'socialaccount': 'allauth_socialaccount.migrations'
}
# END MIGRATIONS CONFIGURATION

# DEBUG
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
# END DEBUG

# SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = 'CHANGEME!!!'
# END SECRET CONFIGURATION

# FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    join(BASE_DIR, 'fixtures'),
)
# END FIXTURE CONFIGURATION

# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# END EMAIL CONFIGURATION

# MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("Andrii Bespalko", "bespalko@steelkiwi.com"),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
ALLOW_ROBOTS = False
# END MANAGER CONFIGURATION

# DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {'default': dj_database_url.config(default='sqlite:///db.sqlite3')}
# END DATABASE CONFIGURATION

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# Required for django-allauth work with Django >= 1.6
# http://stackoverflow.com/questions/19300876/django-allauth-session-json-serializable-error-after-login
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# CACHING
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '127.0.0.1:11211',
        ],
    },
}
# END CACHING

# GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Egypt'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ar', 'Arabic'),
    ('de', 'German'),
    ('ru', 'Russian'),
    ('it', 'Italian'),
    ('fr', 'French'),
)

LANGUAGES_DICT = {code: name for code, name in LANGUAGES}

LOCALE_PATHS = (
    join(BASE_DIR, 'locale', ''),
    join(BASE_DIR, 'common', 'locale', ''),
    join(BASE_DIR, 'users', 'locale', ''),
    join(BASE_DIR, 'hotels', 'locale', ''),
    join(BASE_DIR, 'apartments', 'locale', ''),
    join(BASE_DIR, 'excursions', 'locale', ''),
    join(BASE_DIR, 'sports', 'locale', ''),
    join(BASE_DIR, 'transport', 'locale', ''),
    join(BASE_DIR, 'things_to_do', 'locale', ''),
)

# Rosetta settings:
ENABLE_ROSETTA = True
ROSETTA_MESSAGES_PER_PAGE = 20
ROSETTA_UWSGI_AUTO_RELOAD = True
ROSETTA_EXCLUDED_APPLICATIONS = ('rosetta', 'hvad')

# Haystack settings:
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/en',
    },
    'en': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/en',
    },
    'ar': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/ar',
    },
    'de': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/de',
    },
    'ru': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/ru',
    },
    'it': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/it',
    },
    'fr': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/fr',
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5

IMAGE_CROPPING_JQUERY_URL = "js/lib/jquery-1.11.2.js"
# END GENERAL CONFIGURATION

# TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',

    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",

    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'common.context_processors.travel_dates',
    'common.context_processors.robots_directives',
    'common.context_processors.google_analytics',
    'common.context_processors.default_fb_image',
    'common.context_processors.enabled_languages',
    'booking.context_processors.cart_info',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    join(BASE_DIR, 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
# END TEMPLATE CONFIGURATION

# STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = join(dirname(BASE_DIR), 'staticfiles')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
# STATICFILES_DIRS = (
# )

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# END STATIC FILE CONFIGURATION

# MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = join(BASE_DIR, 'media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
# END MEDIA CONFIGURATION

# CKEDITOR CONFIGURATION
CKEDITOR_UPLOAD_PATH = 'ck/'
# ENDCKEDITOR CONFIGURATION

# URL Configuration
ROOT_URLCONF = 'urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
# End URL Configuration

# AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
    'users.backend.TravelAgencyAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ADMIN_LOGIN_URL = 'admin:login'

# Different user types support
ACCOUNT_ADAPTER = 'users.adapter.AccountAdapter'
ACCOUNT_FORMS = {
    'signup': 'users.forms.EndUserSignupForm',
    'login': 'users.forms.EndUserLoginForm',
}
# End Different user types support

# Some really nice defaults
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = 'index'  # end user redirect logout url
OWNER_LOGOUT_REDIRECT_URL = 'business'  # business owner redirect logout url
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/accounts/choose_profile/'
LOGIN_URL = 'account_login'
# END Custom user app defaults

# SOCIALACCOUNT SETTINGS
DEFAULT_FB_IMAGE = 'images/logo_200x200.jpg'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_ADAPTER = 'users.adapter.SocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'js_sdk',
        # 'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.3'
    }
}
# END AUTHENTICATION CONFIGURATION

# LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOG_DIR = abspath(join(BASE_DIR, '..', '..', 'log'))
LOGFILE_SIZE = 10 * 1024 * 1024
LOGFILE_COUNT = 5
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(filename)s:%(lineno)s] %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'booking': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(LOG_DIR, 'booking.log'),
            'maxBytes': LOGFILE_SIZE,
            'backupCount': LOGFILE_COUNT,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'booking': {
            'level': 'DEBUG',
            'handlers': ['mail_admins', 'booking'],
        },
    }
}
# END LOGGING CONFIGURATION

# google analytics start
USE_GOOGLE_ANALYTICS = False
# google analytics end

# weatherapi app conf start
WUNDERGROUND_API_KEY = 'ad415f912392e402'
WUNDERGROUND_LOCATION = 'HEGN'
WUNDERGROUND_ROOT_URL = 'http://api.wunderground.com/api/'
# weatherapi app conf end

from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS
THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)
THUMBNAIL_ALIASES = {
    '': {
        'business_owner_page_image_preview': {'size': (280, 145), 'crop': 'smart', 'autocrop': True, 'upscale': True},
        'service_detail_page_big_image': {'size': (1000, 600), 'crop': 'smart', 'autocrop': True, 'upscale': True},
        'service_detail_page_small_image': {'size': (138, 135), 'crop': 'smart', 'autocrop': True, 'upscale': True},
        'service_detail_page_item_image': {'size': (170, 120), 'crop': 'smart', 'autocrop': True, 'upscale': True},
        'cart_item_image': {'size': (170, 120), 'crop': 'smart', 'autocrop': True, 'upscale': True},
        'avatar_image': {'size': (118, 118), 'crop': 'smart', 'autocrop': True, 'upscale': True},
        'blog_category_icon': {'size': (18, 18), 'crop': 'smart', 'autocrop': True, 'upscale': True},
        'blog_post_image': {'size': (1000, 400), 'crop': 'smart', 'autocrop': True, 'upscale': True},
    },
}
THUMBNAIL_BASEDIR = 'thumbs'
THUMBNAIL_DEBUG = DEBUG
ORPHANED_CONF_FOR_APPS = {
    'root': MEDIA_ROOT,
    'skip': (
        join(MEDIA_ROOT, THUMBNAIL_BASEDIR),
        join(MEDIA_ROOT, 'ck'),
    )
}
ORPHANED_APPS_MEDIABASE_DIRS = {
    'hotels': ORPHANED_CONF_FOR_APPS,
    'apartments': ORPHANED_CONF_FOR_APPS,
    'transport': ORPHANED_CONF_FOR_APPS,
    'sports': ORPHANED_CONF_FOR_APPS,
    'excursions': ORPHANED_CONF_FOR_APPS,
    'entertainment': ORPHANED_CONF_FOR_APPS,
    'blog': ORPHANED_CONF_FOR_APPS,
    'common': ORPHANED_CONF_FOR_APPS,
    'users': ORPHANED_CONF_FOR_APPS,
}

# booking app settings start
BOOKING_REJECT_AFTER_HOURS_OF_INACTIVITY = 72
# booking app settings end

TEMP_IMAGE_SHOULD_BE_DELETED_AFTER_HOURS = 72

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

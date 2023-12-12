"""
Django settings for aceapp project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import dotenv
import os

from pathlib import Path
from datetime import timedelta
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2o-@s7b_e8_ulwvm6@i*j22v1ei&e_ugx2ry1)9nukr0xwvhp-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'simple_history',
    'accounts',
    'storages',
    'corsheaders',
    'django_db_logger',
    'course',
    'searchall',
    'student',
    'webpush',
    'django.contrib.postgres',
    'MobileApp',
    'finance',
    'django_celery_beat'


]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config("REDIS_HOST")],
        },
    },
}


# from celery import Celery
# app = Celery('aceapp')

# # Load task modules from all registered Django app configs.
# app.config_from_object('django.conf.settings', namespace='CELERY')

# # Auto-discover tasks in all installed apps
# app.autodiscover_tasks()

CELERY_BROKER_URL = config("REDIS_HOST")
CELERY_RESULT_BACKEND = config("REDIS_HOST")

CELERY_BEAT_SCHEDULE = {
    # 'my-periodic-task': {
    #     'task': 'student.tasks.my_celery_task',
    #     'schedule': timedelta(seconds=20),  # Run every 20 seconds
    #     'args': (1, 2),  # Pass your task arguments here
    # },
}
    
ENCRYPTION_URL = config('DECRYPTURL_KEY')
# CELERY_LOG_LEVEL = 'INFO'  # Set the desired log level
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'INFO',  # Adjust the log level as needed
#     },
#     'loggers': {
#         'celery': {
#             'handlers': ['console'],
#             'level': 'INFO',  # Adjust the log level as needed
#             'propagate': False,
#         },
#     },
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'accounts.middleware.CustomUserMiddlewarebody',
    # 'accounts.middleware.CustomUserMiddlewarebody2',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'aceapp.urls'

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

WSGI_APPLICATION = 'aceapp.wsgi.application'
ASGI_APPLICATION = "aceapp.asgi.application"
AUTH_USER_MODEL = 'accounts.User'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# shamil email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")


############ GETTING LOG ##########


############ GETTING LOG ENDS ##########
# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format':
            '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': [],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'development_logfile': {
            'level': 'INFO',
            'filters': [],
            'class': 'logging.FileHandler',
            'filename': 'logs/app_dev.log',
            'formatter': 'verbose'
        },
        'production_logfile': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 1024 * 1024 * 100,    # 100MB
            'backupCount': 5,
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers':
            ['development_logfile', 'production_logfile', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers':
            ['development_logfile', 'production_logfile', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'development_logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['development_logfile'],
        },
    }
}
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ]
# }

# from aceapp.utils import TestStorages
######### AWS S3 BUCKET #########
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_STORAGE_BUCKET_NAME_PUBLIC = config("AWS_STORAGE_BUCKET_NAME_PUBLIC")
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


######### AWS S3 BUCKET END #########

DATA_UPLOAD_MAX_MEMORY_SIZE=5242880


####vimeo access token#####
vimeo_access_token=config("vimeo_access_token")

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'accounts.handlers.custom_exception_handler',
    # Other DRF settings...
}

RAZORPAY_API_KEY = config("razor_pay_key")
RAZORPAY_API_SECRET = config("razor_pay_secret")


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_HOST_CACHE'),  # Replace with your Redis configuration
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
sentry_sdk.init(
# dsn="https://40393f5e0dbd8a42e822331578dd14b6@o4505718837608448.ingest.sentry.io/4505718844424192",
dsn=config('SENTRY'),
integrations=[DjangoIntegration()],
environment=config('SENTRY_ENV'),
# If you wish to associate users to errors (assuming you are using
# django.contrib.auth) you may enable sending PII data.
send_default_pii=True,
# Set traces_sample_rate to 1.0 to capture 100%
# of transactions for performance monitoring.
# We recommend adjusting this value in production.
traces_sample_rate=1.0,
# To set a uniform sample rate
# Set profiles_sample_rate to 1.0 to profile 100%
# of sampled transactions.
# We recommend adjusting this value in production,
profiles_sample_rate=1.0,
)

# SENTRY_DSN = "https://40393f5e0dbd8a42e822331578dd14b6@o4505718837608448.ingest.sentry.io/4505718844424192"
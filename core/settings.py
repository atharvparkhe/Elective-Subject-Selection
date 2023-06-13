from datetime import timedelta
from decouple import config
from pathlib import Path
import os
# import pymysql, os
# pymysql.install_as_MySQLdb()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

# __local
DEBUG = True

# __production
# DEBUG = False

# ALLOWED_HOSTS = ["34.226.180.160"]
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'base.apps.BaseConfig',
    'authentication.apps.AuthenticationConfig',
    'app.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES_DIRS = [
    os.path.join(BASE_DIR, "templates")
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
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

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_USER_MODEL = 'base.BaseUser'


# __local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# __production
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config("DB_NAME"),
#         'USER': config("DB_USER"),
#         'PASSWORD': config("DB_PASSWORD"),
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S' 
USE_I18N = False
USE_L10N = False
USE_TZ = False


# __local
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join("static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = '/data/'
MEDIA_ROOT = os.path.join("data")

# __production
# AWS Config
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_DEFAULT_ACL = None

# AWS Static Files Config
# STATIC_LOCATION = 'static'
# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
# STATICFILES_STORAGE = 'core.storages.StaticStore'

# AWS Media Files Config
# PUBLIC_MEDIA_LOCATION = 'media'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
# DEFAULT_FILE_STORAGE = 'core.storages.MediaStore'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cache
CACHE_TTL = 60
DEFAULT_TIMEOUT = 60
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# __production
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Email Service Setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Utils
BASE_URL = "http://127.0.0.1:8000/"
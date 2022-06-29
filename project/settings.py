
import os
import dotenv
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from project.aws_conf import (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
                              AWS_STORAGE_BUCKET_NAME, AWS_STATIC_DIR, session)


dotenv.read_dotenv()

# Binaries
BINARY_LOC = os.getenv('BINARY_LOC')  # binary ccextractor path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("DEBUG") == '1' or os.getenv(
    "DEBUG") == 'True' else False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin', # Admin not required in this
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles', #
    'video',
    'storages'
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
DB_TABLE_NAME = os.getenv('DB_TABLE_NAME')
DB_ENDPOINT = None

# mq-broker
CELERY_BROKER_URL = 'pyamqp://localhost:5672'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = str(BASE_DIR)+'/static_root'
README_PATH = BASE_DIR / 'README.md'


# storages
TEMP_ROOT = BASE_DIR/'temp'
TEMP_URL = '/temp/'
temporary_storage = FileSystemStorage(location=TEMP_ROOT, base_url=TEMP_URL)


# debug or not debug

if DEBUG:
    INSTALLED_APPS = ['django.contrib.staticfiles'] + INSTALLED_APPS
    # DB_ENDPOINT = 'http://localhost:8' # local dynamodb container

# aws

# enable only when 'collectstatic' required
STATICFILES_STORAGE = 'project.aws_conf.StaticStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

dynamodb = session.resource('dynamodb', endpoint_url=DB_ENDPOINT)

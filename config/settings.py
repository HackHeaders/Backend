from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-e0h4%b!nv24feq&^vhedqmawyt@z$dgr%a0cyc1exj73pequ7j'
DEBUG = True
ALLOWED_HOSTS = ["*"]
APPEND_SLASH=False
MODE = os.getenv("MODE", "DEVELOPMENT")
DATABASE_URL = urlparse(os.getenv("DATABASE_URL"))

CELERY_BROKER_URL = os.getenv('CLOUDAMQP_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
TASK_ALWAYS_EAGER = False



# CELERY_BROKER_URL = 'amqp://localhost'  
# CELERY_BROKER_URL = f'amqp://{os.getenv("RABBITMQ_USER")}:{os.getenv("RABBITMQ_PASSWORD")}@{os.getenv("RABBITMQ_HOST")}:{os.getenv("RABBITMQ_PORT")}//'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    'core.authUser',
    'core.carrier',
    'core.populate',
    "django_extensions",
    "corsheaders",
    "drf_spectacular",
    'django_celery_results',
    'django_filters',
]

AUTH_USER_MODEL = "authUser.User"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'core/templates',
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

WSGI_APPLICATION = 'config.wsgi.application'

if MODE in ["PRODUCTION", "MIGRATE"]:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_URL.path.replace('/', ''),
        'USER': DATABASE_URL.username,
        'PASSWORD': DATABASE_URL.password,
        'HOST': DATABASE_URL.hostname,
        'PORT': 5432,
    }
}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authUser.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        
    ),
    # "DEFAULT_PERMISSION_CLASSES": (
    #     "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    # ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    # ],
}

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

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PASSAGE_APP_ID = os.getenv("PASSAGE_APP_ID")
PASSAGE_API_KEY = os.getenv("PASSAGE_API_KEY")
PASSAGE_AUTH_STRATEGY = 2

CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOW_CREDENTIALS = True  

CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-requested-with',
    'accept',
    'origin',
    'x-csrftoken',
]  

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]  
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
SPECTACULAR_SETTINGS = {
    "TITLE": "FEX API",
    "DESCRIPTION": "API for manage FEX, including endpoints and documentation.",
    "VERSION": "1.0.0",
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")

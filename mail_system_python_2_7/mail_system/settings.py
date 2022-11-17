import os

from dotenv import load_dotenv
from split_settings.tools import include
from urlparse import urljoin

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = str(os.getenv('SECRET_KEY'))

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    "testserver",
    "backend",
]

WEB_HOST = os.getenv('WEB_HOST', 'http://127.0.0.1:80/')
UNSUB_BASE_LINK = os.getenv('UNSUB_BASE_LINK', 'unsubscribe/')
READ_MAIL_BASE_LINK = os.getenv('READ_MAIL_BASE_LINK', 'read_mail/')
UNSUB_LINK = urljoin(WEB_HOST, UNSUB_BASE_LINK)
READ_MAIL_LINK = urljoin(WEB_HOST, READ_MAIL_BASE_LINK)

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'guest')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', 'guest')
RABBITMQ_DEFAULT_VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST', '/')
RABBITMQ_DEFAULT_PORT = os.getenv('RABBITMQ_DEFAULT_PORT', '5672')
CELERY_BROKER_URL = 'amqp://{}:{}@rabbit:{}'.format(
    RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_DEFAULT_PORT
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '...@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'password')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mail_sender'
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

ROOT_URLCONF = 'mail_system.urls'


WSGI_APPLICATION = 'mail_system.wsgi.application'


AUTH_USER_MODEL = 'mail_sender.User'

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

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

include(
    "components/database.py",
    "components/templates.py",
)

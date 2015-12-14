"""
Django settings for eRSA's password reset project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'drip5dm-*6i=ej6g&+o(bb*z*5_4kvjh^-j=70j3(dd3(^ihk_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ersaauth',
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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Adelaide'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

EMAIL_HOST = smtp.ersa.edu.au

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] [%(module)s] [%(levelname)s]: %(message)s'
        },
    },
    'handlers': {
        'stream_to_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/lib/django-pwd-reset/django-pwd-reset.log',
            'formatter':'simple',
        },
    },
    'loggers': {
        'django-pwd-reset': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

#Name to be referenced in the application. Should match one of above defined loggers
APP_LOGGER = 'django-pwd-reset'

# Password reset token timeout: currently the unit is hour
PASSWORD_RESET_TIMEOUT = 10
# Salt used in generating password reset token
PASSWORD_RESET_TOKEN_SALT = 'SOME_RANDOM_THING'

FIM_URL = 'http://ersafim'

# AD connection
# Has to be TLS enabled
AD_SERVER = ersa.edu.au
AD_DOMAIN = domain
AD_BASE = OU_TO_MAN_ersa.edu.au
# Account used for reseting password
AD_RESETER = SERVICE_ACCOUNT
AD_RESETER_PWD = SERVICE_ACCOUNT_PWD
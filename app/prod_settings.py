"""
Django settings for eRSA's password reset project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = REPLACE_WITH_PROD_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.ersa.edu.au',]

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True

SECURE_HSTS_SECONDS = 3600 # 1hour, if works fine, set to a longer value: 31536000 seconds, i.e. 1 year, is common
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

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
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
           'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.app_directories.Loader',
                ]),
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
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/lib/django-pwd-reset/django-pwd-reset.log',
            'formatter':'simple',
        },
    },
    'loggers': {
        'django-pwd-reset': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

APP_LOGGER = 'django-pwd-reset'

APP_LOGGER = 'django-pwd-reset'

# Password reset token timeout: currently the unit is hour
PASSWORD_RESET_TIMEOUT = 10
# Salt used in generating password reset token
PASSWORD_RESET_TOKEN_SALT = 'SOME_RANDOM_THING'

FIM_URL = 'http://ersafim'

AD_SERVER = ersa.edu.au
AD_DOMAIN = domain
AD_BASE = OU_TO_MAN_ersa.edu.au
# Account used for reseting password
AD_RESETER = SERVICE_ACCOUNT
AD_RESETER_PWD = SERVICE_ACCOUNT_PWD

# Default password strength checking pattern used in forms.py is
#REG_PWD_ STRENGTH = '^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*[!@#\$%\^&\*]).{8,}'
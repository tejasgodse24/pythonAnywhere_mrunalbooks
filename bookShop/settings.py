
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True
# DEBUG = False


# ALLOWED_HOSTS = ['mrunalbooks.com', 'www.mrunalbooks.com']
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products.apps.ProductsConfig',
    'accounts.apps.AccountsConfig',
    'home.apps.HomeConfig',
    'dealer.apps.DealerConfig',
    'custom_admin.apps.CustomAdminConfig',
    'mathfilters',
    'import_export', 
    'django_extensions',
    'django_celery_results',
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

ROOT_URLCONF = 'bookShop.urls'

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

WSGI_APPLICATION = 'bookShop.wsgi.application'


DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("postgresql_name"),
        "USER": os.environ.get("postgresql_user"),
        "PASSWORD": os.environ.get("postgresql_password"),
        "HOST": os.environ.get("postgresql_host"),
        "PORT": os.environ.get("postgresql_port"),
    }
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# store cookies for one day
# SESSION_COOKIE_AGE = 60 * 60 * 24


# STATIC_ROOT = "/var/www/mrunalbooks/static/"
# STATIC_URL = '/static/'
# MEDIA_ROOT =  "/var/www/mrunalbooks/media/" 
# MEDIA_URL = '/media/'

# localhost
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')
STATIC_URL = '/static/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'public/media') 
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")



RAZORPAY_KEY = os.environ.get("RAZORPAY_KEY")
RAZORPAY_SECRET = os.environ.get("RAZORPAY_SECRET")


# # django logger
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": "INFO",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/django/django.log"),
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "INFO",
#             "propagate": True,
#         },
#     },
# }

# Celery settings
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND = 'django-db'

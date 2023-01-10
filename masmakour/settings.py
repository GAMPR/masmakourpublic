"""
Django settings for masmakour project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import dotenv #hidden keys 

from pathlib import Path
#for secrete key hiding 
from django.core.management.utils import get_random_secret_key 
import dj_database_url 
#heroku
#import django_heroku 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR=Path(__file__).resolve().parent.parent

#dotenv
dotenv_file = os.path.join(BASE_DIR, ".env") 
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file) 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())  

#RECAPTCHA KEYS 
RECAPTCHA_PUBLIC_KEY='6LdWNMQfAAAAACDvJkaFrNS9ogDDUebqW0qLfld3'
RECAPTCHA_PRIVATE_KEY=os.environ['RECAPTCHA_PRIVATE_KEY'] 

#CUSTOM USER MODEL

AUTH_USER_MODEL='blog.User' 

#EMAIL CONFIG 

EMAIL_FROM_USER='masmakourwebhelper@gmail.com' 
EMAIL_HOST='smtp.gmail.com' 
EMAIL_HOST_USER='masmakourwebhelper@gmail.com'  
EMAIL_HOST_PASSWORD=os.environ['EMAIL_HOST_KEY'] 
EMAIL_USE_TLS=True
EMAIL_PORT=587 

#STRIPE
STRIPE_PUBLISHABLE_KEY='pk_live_51Kz3g9Jpl9jpF0rnWIuFXpOsDqQ0tGk3GGIEDyla9Kk4sUzQU75pIcE0bGTEL380N8IKCAE5P75jJ0vZiFuj4dHb00wo1DkYjN'
STRIPE_SECRET_KEY=os.environ['STRIPE_SECRET_KEY'] 

STRIPE_PRICE_ID='price_1L31BUJpl9jpF0rnUgTLo4Vx' #updated 
STRIPE_PRICE_ID_DONATE='price_1L3R7rJpl9jpF0rn7ZZvdiDE'#updated 

#local host webhook STRIPE_ENDPOINT_SECRET='whsec_c17d1cfc75429fa2561dd875c050008c7406fbd386ce71c0e912355817943f8a'
STRIPE_ENDPOINT_SECRET=os.environ['STRIPE_ENDPOINT_SECRET'] 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=False  

#IF SITE LIVE SSL AND DEBUG force ssl redirect 
if os.getcwd() == '/app':
    DEBUG=False
    SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT=True 

#ALLOWED HOSTS 
ALLOWED_HOSTS=["127.0.0.1","localhost","masmakour.com","www.masmakour.com", "web-production-c1f1.up.railway.app", "railway.app"]

#TRUSTED ORIGINS
CSRF_TRUSTED_ORIGINS=['https://masmakour.com','https://127.0.0.1', 'https://www.masmakour.com', "web-production-c1f1.up.railway.app"]


# Application definition

INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        #custom apps after this point 
        'blog', 
        'django_summernote',
        'django.contrib.sitemaps',
        'crispy_forms',
        'captcha', 
        'hitcount', 
        ]

MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

ROOT_URLCONF='masmakour.urls'

TEMPLATES=[
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

WSGI_APPLICATION='masmakour.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

#sqlite way
#DATABASES={
#        'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#            'NAME': BASE_DIR / 'db.sqlite3',
#            }
#       }


DATABASE_URL="//postgres:X64uFIw9KWvEWZrkH87O@containers-us-west-66.railway.app:6890/railway" 

DATABASES = {"default": dj_database_url}




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS=[
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

LANGUAGE_CODE='en-us'

#keep America/New_York instead of EST for dailite savings to work 
TIME_ZONE='America/New_York'

USE_I18N=True

USE_TZ=True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL='static/'
#Added STATICFILES_DIRS
STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static'),]
#ADDED STATIC_ROOT
STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles') 

#MEDIA FILES
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'media/') 

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'

#heroku thing
#django_heroku.settings(locals())

#error 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

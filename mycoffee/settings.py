"""
Django settings for mycoffee project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from dotenv import load_dotenv
import environ

# Initialize environment variables
load_dotenv()
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'. #yla rak baghi dir paths fl projects dir hak : BASE_DIR / 'subdir' 
BASE_DIR = Path(__file__).resolve().parent.parent  #hada lpath li fih lmelef


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x+n==&6#-yxqt)c8_eaphey+o664d725!8_$s2+&_y%#+7b8%e'
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'orders.apps.OrdersConfig',
    'pages.apps.PagesConfig', #ki zedna app ta3 pages zednaha hna
    'accounts.apps.AccountsConfig', #ki zedna app ta3 accounts zednaha hna
    'products.apps.ProductsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'mycoffee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], #templates hada folder li zednah dernaleh directory ta3eh
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

WSGI_APPLICATION = 'mycoffee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mycoffeedb', #hadi ism database li drnaha fl pgAdmin 4
        'USER' : 'postgres', #username ta3 database li drnaha mycoffeedb
        'PASSWORD' : 'ASTARFIROLAH',
        'HOST' : 'localhost',
        'PORT' : '5432', #bach tet2eked mn port li nekhedmo bih ro7 lel pgAdmin 4->PostgreSQL15->right click->properties->connection->Port
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us' #kon ndiro ar nidam al idara yweli 3arabi 

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
#STATIC_URL = 'static/'   
#STATICFILES_DIRS = [
    #BASE_DIR /'mycoffee / static', #hna golnaleh mycoffee->static file li zednah w jeme3na fih imges js css howa lmenbe3 li site ta3na yedi mneh files w yekhdem bihom
    #BASE_DIR /'mycoffee / static / fonts'
#] 
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/' #lmassar ta3 ki ycrée a folder static kharej mycoffee/static w yedi ga3 file ta3 'mycoffee' / 'static' li copinahom b yedina
STATICFILES_DIRS = [
    BASE_DIR / 'mycoffee' / 'static', # Corrected path, removed extra space here
]

#Media Folder
MEDIA_ROOT = BASE_DIR / 'media' 
MEDIA_URL = '/media/' #ki tebghi taffichi photo m database yweli yediha mn had folder li smoh media





# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Custom Messages
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "danger", #psq f bootstrap danger hiya error
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

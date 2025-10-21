import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'place_reviews',  # Register the app
    #'accounts',
]
#AUTH_USER_MODEL = 'accounts.CustomUser'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vendorvision.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'place_reviews/templates')],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    },
]

WSGI_APPLICATION = 'vendorvision.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [...]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

#STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'place_reviews/static')]
# settings.py

# URL for accessing static files
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'place_reviews' / 'static']  # Adjust for the nested static folder




import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\mnsra\OneDrive\Desktop\project\New folder (2)\eng-blade-429110-m8-367dbc3c94a9.json"


# Google API Key
API_KEY = 'AIzaSyDW7HdfpSgoLchJyvAddX70gdnram8qHYg'
# import os
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\Users\mnsra\OneDrive\Desktop\New folder\plasma-air-439413-q1-7e8a07d64df2.json'
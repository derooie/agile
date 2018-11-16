import os

DEBUG = True

ALLOWED_HOSTS = ['*', ]

# DATABASE INFO
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'agile.sqlite3',
        'HOST': 'localhost',
    }
}

PRODUCTION_DB = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agile',
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        # 'USER': 'agile',
        # 'PASSWORD': 'agile',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# Indicate which database you want to use in your development
PRODUCTION_DATABASE = False

if PRODUCTION_DATABASE:
    DATABASES = PRODUCTION_DB

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = 'static/'

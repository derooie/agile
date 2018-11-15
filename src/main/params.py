DEBUG = True

ALLOWED_HOSTS = ['*',]

# DATABASE INFO
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'agile.sqlite3',
        'HOST': 'localhost',
    }
}

PRODUCTION_DATABASE = {
    'default': {
        # If you are using Cloud SQL for MySQL rather than PostgreSQL, set
        # 'ENGINE': 'django.db.backends.mysql' instead of the following.
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agile',
        # 'USER': os.getenv('DATABASE_USER'),
        # 'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'USER': 'agile',
        'PASSWORD': 'agile',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# Indicate which database you want to use in your development
PRODUCTION_DATABASE=False

if PRODUCTION_DATABASE:
    DATABASES = PRODUCTION_DATABASE


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = 'static/'

DEBUG=True

DATABASES = {
    'default': {
        # If you are using Cloud SQL for MySQL rather than PostgreSQL, set
        # 'ENGINE': 'django.db.backends.mysql' instead of the following.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'agile',
        'HOST': 'localhost',
    }
}

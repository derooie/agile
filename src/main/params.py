DEBUG = True

ALLOWED_HOSTS = ['*',]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'agile.sqlite3',
#         'HOST': 'localhost',
#     }
# }


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = 'static/'


# For local development use params.py to overwrite settings
try:
    from main.params import *
except ImportError:
    pass

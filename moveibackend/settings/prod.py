from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'sathish',
        'PASSWORD': 'postgres',
        'HOST': 'host.docker.internal',
        'PORT': '5432',
    }
}

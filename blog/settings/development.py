from blog.settings.base import *


DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'development.sqlite'
    },
    # Use SQLITE for testing
    'TEST': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testing.sqlite'
    }
}


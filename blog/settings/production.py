import dj_database_url
import django_heroku

from blog.settings.base import *

DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = [
    "damiankuriatablog.herokuapp.com"
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Load database settings from DATABASE_URL envvar
db_from_env = dj_database_url.config(conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)
django_heroku.settings(locals())

# Media files serving using Amazon S3
AWS_STORAGE_BUCKET_NAME = 'myblog-bucket-production'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
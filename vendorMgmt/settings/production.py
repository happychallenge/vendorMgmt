from .common import *

DEBUG = False

import dj_database_url

INSTALLED_APPS += [ 'raven.contrib.django.raven_compat', ]
import os
import raven

RAVEN_CONFIG = {
    'dsn': 'https://06b29b78f8b649dc88c79a43e2cde322:3963bb734e594f0ea84e030b15d9d0e9@sentry.io/195825',
    'release': raven.fetch_git_sha(BASE_DIR),
}

DATABASES = {
    'default': dj_database_url.parse('postgres://vendorMgmt:Wjdgml00@localhost:5432/vendorMgmt')
}

ALLOWED_HOSTS = ['*']

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATIC_URL = '/static/'
STATICFILES_DIRS = [ join(BASE_DIR, 'staticfiles'),]
STATIC_ROOT = join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

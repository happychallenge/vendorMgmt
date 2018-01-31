from .common import *

DEBUG = False

import dj_database_url

# INSTALLED_APPS += [ 'raven.contrib.django.raven_compat', ]
# import os
# import raven

# RAVEN_CONFIG = {
#     'dsn': 'https://67dc96306e1c43ed90d90c80d74691eb:0cd1f84292a943f2b689a3b164776e44@sentry.io/268717',
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
#     'release': raven.fetch_git_sha(BASE_DIR),
# }

# DATABASES = {
#     'default': dj_database_url.parse('postgres://vendorMgmt:Wjdgml00@localhost:5432/vendorMgmt')
# }

ALLOWED_HOSTS = ['*']

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATIC_URL = '/static/'
STATICFILES_DIRS = [ join(BASE_DIR, 'staticfiles'),]
STATIC_ROOT = join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

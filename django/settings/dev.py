from settings.settings import *

DEBUG = True
ALLOWED_HOSTS = []

# Django Debug Toolbar Config
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

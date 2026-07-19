from .settings_base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# База данных: SQLite (относительный путь)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# django-debug-toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# Под вопросом: при разработке можно отключить проверку безопасности
# (не включать в prod.py)
SECURE_BROWSER_XSS_FILTER = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
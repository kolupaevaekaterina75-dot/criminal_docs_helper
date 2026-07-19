from .settings_base import *

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOSTS', 'your-domain.com')]

# Пример для PostgreSQL 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ['DB_NAME'],
#         'USER': os.environ['DB_USER'],
#         'PASSWORD': os.environ['DB_PASSWORD'],
#         'HOST': os.environ['DB_HOST'],
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

# Пока для совместимости с текущей структурой можно оставить SQLite,
# но помни: для продакшена SQLite не рекомендуется.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_prod.sqlite3',
    }
}

# Безопасность
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
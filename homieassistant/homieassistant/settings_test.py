from .settings import *  # NOQA

TEST = True
DEBUG = False

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
STATICFILES_STORAGE = "inmemorystorage.InMemoryStorage"

CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = "memory://"
CELERY_BACKEND = "memory"

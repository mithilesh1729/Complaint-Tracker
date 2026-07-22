from .base import *

# -------------------------
# Development settings
# -------------------------

DEBUG = True

# SECRET_KEY = "dev-secret-key-change-later"
SECRET_KEY = os.getenv("SECRET_KEY", "dev-fallback-key")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "testserver",
]

# -------------------------
# Database (LOCAL MySQL)
# -------------------------



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "complaint_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# -------------------------
# CORS & CSRF (LOCAL)
# -------------------------

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

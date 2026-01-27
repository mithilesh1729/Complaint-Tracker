from .base import *
import os

# -------------------------
# Production settings
# -------------------------

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# -------------------------
# Database (PostgreSQL on Render)
# -------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

# -------------------------
# CORS (Frontend domain)
# -------------------------

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    os.getenv("FRONTEND_URL"),
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# backend/backend/settings_production.py
import os
import dj_database_url

# Import base settings FIRST
from .settings import *

# ============================================================================
# CRITICAL: Override ALLAUTH settings (Must come right after import)
# ============================================================================
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_METHODS = {'email'}  # Modern way instead of AUTHENTICATION_METHOD
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ['email*']  # Only email, no username

# Make sure REST_AUTH uses the custom serializer
REST_AUTH = {
    'REGISTER_SERIALIZER': 'core.serializers.CustomRegisterSerializer',
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,
    'SESSION_LOGIN': False,
    'LOGIN_SERIALIZER': 'dj_rest_auth.serializers.LoginSerializer',
}

# ============================================================================
# PRODUCTION SECURITY
# ============================================================================
DEBUG = False

# Backend host configuration
BACKEND_HOST = os.getenv('BACKEND_HOST', 'advision-backend.onrender.com')

# Parse additional hosts from environment (comma-separated)
ADDITIONAL_HOSTS = os.getenv('ADDITIONAL_HOSTS', '').split(',')
ADDITIONAL_HOSTS = [host.strip() for host in ADDITIONAL_HOSTS if host.strip()]

# Combine all allowed hosts
ALLOWED_HOSTS = [
    BACKEND_HOST,
    '.onrender.com',  # Allow all Render subdomains
    'localhost',
    '127.0.0.1',
] + ADDITIONAL_HOSTS

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Proxy settings for Render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# ============================================================================
# DATABASE - PostgreSQL on Render
# ============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ============================================================================
# STATIC FILES (WhiteNoise)
# ============================================================================
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

os.makedirs(STATIC_ROOT, exist_ok=True)

# ============================================================================
# FRONTEND URL CONFIGURATION (FROM ENV VARIABLE)
# ============================================================================
# Primary frontend URL from environment variable
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://advision-frontend.vercel.app')

# Additional allowed origins (for backwards compatibility)
ADDITIONAL_FRONTEND_URLS = os.getenv('ADDITIONAL_FRONTEND_URLS', '').split(',')
ADDITIONAL_FRONTEND_URLS = [url.strip() for url in ADDITIONAL_FRONTEND_URLS if url.strip()]

# Combine all frontend URLs
ALL_FRONTEND_URLS = [FRONTEND_URL] + ADDITIONAL_FRONTEND_URLS

# ============================================================================
# CORS CONFIGURATION
# ============================================================================
CORS_ALLOWED_ORIGINS = list(set(ALL_FRONTEND_URLS))

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = list(set(ALL_FRONTEND_URLS + [
    "https://advision-backend.onrender.com",
]))

# ============================================================================
# GOOGLE OAUTH SETTINGS
# ============================================================================
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')

# OAuth Redirect URI (uses FRONTEND_URL)
GOOGLE_OAUTH_REDIRECT_URI = f"{FRONTEND_URL}/auth/google/callback"

# ============================================================================
# API ENCRYPTION KEY
# ============================================================================
API_ENCRYPTION_KEY = os.getenv('API_ENCRYPTION_KEY', SECRET_KEY)

# ============================================================================
# CLOUDINARY CONFIGURATION
# ============================================================================
import cloudinary

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

USE_CLOUDINARY = True

# ============================================================================
# AI API KEYS
# ============================================================================
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', '')

# ============================================================================
# LOGGING
# ============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ============================================================================
# REPORT STORAGE PATH
# ============================================================================
REPORT_STORAGE_PATH = os.path.join(BASE_DIR, 'reports')
os.makedirs(REPORT_STORAGE_PATH, exist_ok=True)
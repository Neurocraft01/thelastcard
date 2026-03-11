"""
Django settings for NFC Card Management Platform.

Security-hardened configuration following enterprise best practices.
"""

import os
from pathlib import Path
from decouple import config, Csv
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# SECURITY SETTINGS
# =============================================================================

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-this-in-production-minimum-50-characters-required-here')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# CSRF Protection
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000,http://127.0.0.1:8000', cast=Csv())

# Security Headers (Enable in production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
else:
    # Ensure no HTTPS redirect in local development
    SECURE_SSL_REDIRECT = False

# Clickjacking protection
X_FRAME_OPTIONS = 'DENY'

# Cookie Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Session Settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# Site Configuration
SITE_ID = 1
SITE_NAME = config('SITE_NAME', default='NFC Platform')


# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for allauth

    # Allauth
    'allauth',
    'allauth.account',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'accounts.apps.AccountsConfig',
    'organizations.apps.OrganizationsConfig',
    'cards.apps.CardsConfig',
    'profiles.apps.ProfilesConfig',
    'orders.apps.OrdersConfig',
    'landing',
    'api',
    'analytics.apps.AnalyticsConfig',
    'themes.apps.ThemesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files in production
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'nfc_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.auth_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'nfc_platform.wsgi.application'


# =============================================================================
# DATABASE - PostgreSQL (Supabase) / SQLite fallback
# =============================================================================

# Set DATABASE_URL in .env:
# Supabase session pooler (IPv4-safe, port 6543):
#   postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
# Render PostgreSQL (auto-injected via render.yaml fromDatabase property)

DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,        # Persistent connection reuse (10 min)
            conn_health_checks=True,  # Discard unhealthy connections automatically
            # ssl_require is intentionally omitted: include ?sslmode=require in
            # DATABASE_URL itself so it is not applied to SQLite fallback and
            # does not conflict with Supabase session-pooler SSL negotiation.
        )
    }
else:
    # Local development fallback: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# =============================================================================
# AUTHENTICATION
# =============================================================================

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Login/Logout settings
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard_redirect'
LOGOUT_REDIRECT_URL = 'landing:home'

# Allauth Configuration (compatible with both v0.61 and v65+)
import allauth
_allauth_version = tuple(int(x) for x in allauth.__version__.split('.')[:2])
if _allauth_version >= (65, 0):
    ACCOUNT_LOGIN_METHODS = {'email'}
    ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
else:
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True
# Use HTTP in development so allauth doesn't generate https:// redirect URLs
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http' if DEBUG else 'https'

# Password reset token expiry (in seconds) - 1 hour
PASSWORD_RESET_TIMEOUT = 3600


# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =============================================================================
# STATIC FILES
# =============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration for efficient static file serving
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # CompressedStaticFilesStorage avoids 500 errors when hashed refs go missing
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# =============================================================================
# MEDIA FILES
# =============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024   # 2 MB in-memory buffer
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 MB total form data


# =============================================================================
# CLOUDFLARE R2 STORAGE (S3-Compatible)
# =============================================================================
#
# Required .env keys:
#   USE_R2_STORAGE=True
#   R2_ACCOUNT_ID      — found in Cloudflare dashboard → R2 → Overview
#   R2_ACCESS_KEY_ID   — R2 API token (S3 access key)
#   R2_SECRET_ACCESS_KEY — R2 API token (S3 secret)
#   R2_BUCKET_NAME     — name of your R2 bucket
#
# Optional:
#   R2_CUSTOM_DOMAIN   — e.g. media.thelastcard.in (set in R2 → Custom Domains)
#                        Required for public file serving without presigned URLs.
#
# If R2_CUSTOM_DOMAIN is not set, ensure the bucket has "Public Access" enabled
# in the Cloudflare R2 dashboard so the r2.dev public URL works.

USE_R2_STORAGE = config('USE_R2_STORAGE', default=False, cast=bool)

if USE_R2_STORAGE:
    if 'storages' not in INSTALLED_APPS:
        INSTALLED_APPS += ['storages']

    R2_ACCOUNT_ID = config('R2_ACCOUNT_ID')
    AWS_ACCESS_KEY_ID = config('R2_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('R2_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('R2_BUCKET_NAME', default='thelastcard')

    # S3-compatible write endpoint (used by boto3 for uploads/downloads)
    AWS_S3_ENDPOINT_URL = f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com'

    # R2-specific settings
    AWS_S3_REGION_NAME = 'auto'          # R2 only supports the 'auto' region
    AWS_S3_SIGNATURE_VERSION = 's3v4'    # Must use Signature Version 4
    AWS_DEFAULT_ACL = None               # R2 has no per-object ACL support
    AWS_QUERYSTRING_AUTH = False         # Serve files via plain URLs (no presigned)
    AWS_S3_FILE_OVERWRITE = False        # Never silently overwrite existing uploads
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',  # CDN / browser cache: 1 day
    }

    # Public serve URL — use custom domain if configured, else the r2.dev URL
    R2_CUSTOM_DOMAIN = config('R2_CUSTOM_DOMAIN', default='')
    if R2_CUSTOM_DOMAIN:
        AWS_S3_CUSTOM_DOMAIN = R2_CUSTOM_DOMAIN
        MEDIA_URL = f'https://{R2_CUSTOM_DOMAIN}/media/'
    else:
        # No custom domain: rely on the bucket's public r2.dev URL.
        # Enable public access in Cloudflare R2 → your bucket → Settings → Public Access.
        AWS_S3_CUSTOM_DOMAIN = f'pub-{R2_ACCOUNT_ID}.r2.dev'
        MEDIA_URL = f'https://pub-{R2_ACCOUNT_ID}.r2.dev/media/'

    # Route all media uploads through the R2 storage backend
    STORAGES["default"] = {
        "BACKEND": "nfc_platform.storages.R2MediaStorage",
    }


# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@nfcplatform.com')


# =============================================================================
# REST FRAMEWORK
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}


# =============================================================================
# CORS SETTINGS
# =============================================================================

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:8000,http://127.0.0.1:8000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True


# =============================================================================
# SITE SETTINGS
# =============================================================================

SITE_NAME = config('SITE_NAME', default='NFC Card Platform')
SITE_URL = config('SITE_URL', default='http://localhost:8000')


# =============================================================================
# RAZORPAY PAYMENT GATEWAY
# =============================================================================

RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='')


# =============================================================================
# SUPABASE CLIENT SDK
# =============================================================================
# Used for Supabase Auth, Storage, Realtime, and Edge Functions via supabase-py.
# The database connection (PostgreSQL) uses DATABASE_URL separately.
# SUPABASE_KEY is the publishable anon key — safe to use server-side.

SUPABASE_URL = config('SUPABASE_URL', default='')
SUPABASE_KEY = config('SUPABASE_KEY', default='')


# =============================================================================
# LOGGING
# =============================================================================

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
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

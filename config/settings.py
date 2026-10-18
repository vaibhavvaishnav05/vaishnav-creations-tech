"""Settings for the Vaishnav Creations Technologies website.

Everything environment-specific comes from environment variables, so the same
code runs locally (SQLite, DEBUG on) and in production (Postgres, DEBUG off).
See README.md for the full list.
"""
import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    return [x.strip() for x in os.environ.get(name, default).split(",") if x.strip()]


# Hosting platform detection (both set these automatically)
ON_VERCEL = os.environ.get("VERCEL") == "1"
ON_RENDER = bool(os.environ.get("RENDER"))
HOSTED = ON_VERCEL or ON_RENDER

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = env_bool("DJANGO_DEBUG", not HOSTED)   # off by default on Vercel/Render
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,.vercel.app,.onrender.com")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "https://*.vercel.app,https://*.onrender.com")

# Render sets these automatically for every web service.
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST and RENDER_HOST not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_HOST)

# Public site URL, used in canonical tags, sitemap, schema and llms.txt.
# Set SITE_URL once you connect your own domain; until then the Render URL is used.
_vercel_prod = os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")  # e.g. my-site.vercel.app
SITE_URL = (os.environ.get("SITE_URL") or os.environ.get("RENDER_EXTERNAL_URL")
            or (f"https://{_vercel_prod}" if _vercel_prod else "")
            or "http://localhost:8000").rstrip("/")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
#  • Local:                      SQLite file (db.sqlite3)
#  • Vercel + Neon connected:    Postgres. The direct (unpooled) URL is preferred — simplest and
#                                safest with Django on a low-traffic site.
#  • Vercel, no database:        "no-database mode" — a temporary SQLite copy in /tmp, rebuilt from
#                                core/seed.py on every cold start. Pages work; nothing is saved.
_db_url = os.environ.get("DATABASE_URL_UNPOOLED") or os.environ.get("DATABASE_URL")
NO_DB_MODE = ON_VERCEL and (not _db_url or env_bool("DJANGO_NO_DB"))

if NO_DB_MODE:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "/tmp/vc-site.sqlite3"}}
elif _db_url:
    DATABASES = {"default": dj_database_url.parse(
        _db_url, conn_max_age=0 if ON_VERCEL else 600, conn_health_checks=True)}
else:
    DATABASES = {"default": dj_database_url.parse(f"sqlite:///{BASE_DIR / 'db.sqlite3'}")}

# On Vercel the site prepares its own database when it starts (see core/bootstrap.py):
# creates tables, loads the starting content and creates the admin login from
# DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_EMAIL / DJANGO_SUPERUSER_PASSWORD.
AUTO_PREPARE_DB = ON_VERCEL

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        # Vercel collects static files at build time and serves them from its CDN.
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage" if (DEBUG or ON_VERCEL)
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    },
}

# Uploaded client logos. In production point MEDIA_ROOT at a persistent disk.
MEDIA_URL = "/media/"
# Vercel's filesystem is read-only except /tmp (temporary), so use logo files in static/ instead.
MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", "/tmp/media" if ON_VERCEL else BASE_DIR / "media"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email — new enquiries are emailed to the address in Site settings (admin).
# Without SMTP settings, emails are printed to the console instead.
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
if EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "website@vaishnavcreations.com")

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # Vercel already forces HTTPS at its edge; redirecting again in Django can loop.
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SSL_REDIRECT", not ON_VERCEL)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

LOGGING = {
    "version": 1,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

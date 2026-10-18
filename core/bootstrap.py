"""Prepares the database automatically when the site starts on Vercel.

Runs once per server start (cold start), before the first request:
  1. `migrate` — creates any missing tables and loads the starting content (migration 0002).
     When everything is already applied this is a quick check.
  2. Creates the admin login from DJANGO_SUPERUSER_USERNAME / _EMAIL / _PASSWORD
     if those are set and that user doesn't exist yet.

Errors are logged, never raised: a database hiccup shows up in Vercel → Logs instead of
taking the whole site down at import time.
"""
import logging
import os
import time

from django.conf import settings
from django.core.management import call_command
from django.db import connection

log = logging.getLogger(__name__)
_LOCK_ID = 727301  # any constant; serialises migrations between instances on Postgres


def prepare_database():
    started = time.monotonic()
    try:
        if connection.vendor == "postgresql":
            with connection.cursor() as cur:
                cur.execute("SELECT pg_advisory_lock(%s)", [_LOCK_ID])
            try:
                _setup()
            finally:
                with connection.cursor() as cur:
                    cur.execute("SELECT pg_advisory_unlock(%s)", [_LOCK_ID])
        else:
            _setup()
        log.info("Database ready in %.1fs (%s)", time.monotonic() - started,
                 "no-database mode" if settings.NO_DB_MODE else connection.vendor)
    except Exception:
        log.exception("Automatic database setup failed — check DATABASE_URL in Vercel settings")
    finally:
        connection.close()


def _setup():
    call_command("migrate", interactive=False, verbosity=0)
    if not settings.NO_DB_MODE:
        _ensure_admin_user()


def _ensure_admin_user():
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
    if not (username and password):
        return
    from django.contrib.auth import get_user_model

    User = get_user_model()
    if User.objects.filter(username=username).exists():
        return
    User.objects.create_superuser(
        username=username, email=os.environ.get("DJANGO_SUPERUSER_EMAIL", ""), password=password)
    log.info("Created admin user %s", username)

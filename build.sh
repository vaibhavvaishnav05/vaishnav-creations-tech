#!/usr/bin/env bash
# Build step for Render (or any host): install, collect static files, migrate.
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Creates your admin login on the first deploy (Render's free plan has no Shell).
# Uses DJANGO_SUPERUSER_USERNAME / _EMAIL / _PASSWORD; skipped if the user already exists.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --noinput || echo "Admin user already exists — skipping."
fi

# Vaishnav Creations Technologies — website

Django 5 website for the agency: home, services (8 detail pages), client work, about and contact.
Clean white design, mobile-first, with every piece of content editable in Django admin.

## What's inside

| Area | Where |
|---|---|
| Pages & routing | `core/views.py`, `core/urls.py` |
| Content models | `core/models.py` — Site settings, Services, Industries, Client work, FAQs, Leads |
| Admin | `core/admin.py` → `/admin/` |
| Templates | `core/templates/core/` |
| Design system | `core/static/css/site.css` (colours and fonts at the top) |
| Starting content | `core/seed.py` (loaded once by migration `0002`) |
| Tests | `core/tests.py` |

**Built-in SEO / GEO / AEO:** per-page titles and descriptions, canonical URLs, Open Graph tags,
`ProfessionalService`, `Service` and `FAQPage` schema, `/sitemap.xml`, `/robots.txt`, and
`/llms.txt` (a plain-text summary for AI assistants, generated from your admin content).

**Leads:** the contact form saves every enquiry in admin → *Leads* (with status and notes)
and emails it to the address in *Site settings*. It has spam protection (hidden honeypot field +
5 submissions per hour per connection).

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate          # creates the database and loads the starting content
python manage.py createsuperuser  # your admin login
python manage.py runserver
```
Open http://127.0.0.1:8000 and http://127.0.0.1:8000/admin/

Run the tests: `python manage.py test core`

## Managing content (admin)

- **Site settings** — headline, client/country figures, contact details, WhatsApp number, the email that receives enquiries.
- **Client work** — add/remove clients. A project shows on the site **only when "Client approved" is ticked**.
  For a logo, put the file in `core/static/img/clients/`, push to GitHub, and type its name in
  *Logo file name* (e.g. `silver-lake.svg`). It replaces the text name automatically.
  *Show in hero* puts it in the homepage "Client sites we've built" panel (up to 6).
  Testimonials appear only when *verified* is ticked — use real, approved quotes only.
- **Services / Industries / FAQs** — edit text, reorder, or hide with *Is published*.
- **Leads** — every enquiry, with a status you can update.

## Deploy

### Vercel (free) — recommended setup
`vercel.json` pins the **Django** framework preset. The site prepares its own database when it
starts (`core/bootstrap.py`), so there are no commands to run on your laptop.

1. **Push** this folder to GitHub.
2. **Vercel → Add New → Project →** import the repo. *Framework Preset* must say **Django**.
3. **Environment Variables** (Settings → Environment Variables, all environments):
   | Key | Value |
   |---|---|
   | `DJANGO_SECRET_KEY` | long random string — `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
   | `DJANGO_SUPERUSER_USERNAME` | your admin username |
   | `DJANGO_SUPERUSER_EMAIL` | your email |
   | `DJANGO_SUPERUSER_PASSWORD` | a strong password |
4. **Database (optional but recommended):** Storage → Create Database → **Neon** (Free) → connect
   with prefix **`DATABASE`**, both "create database branch" boxes **unticked**.
5. **Deploy / Redeploy.** On first start the site creates its tables, loads the starting content
   and creates your admin login. Open `https://<project>.vercel.app` and `/admin/`.

**Without a database ("no-database mode"):** if no `DATABASE_URL` is set, the site still runs.
All pages work with the content from `core/seed.py`; `/admin/` is switched off; the contact form
opens WhatsApp with the visitor's details filled in (and also emails you if `EMAIL_*` is set).
To edit content in this mode, change `core/seed.py` (or `SiteSettings` defaults in `core/models.py`)
and push. Add a Neon database any time and redeploy — the site switches over automatically.

**Custom domain:** Settings → Domains, then add `SITE_URL=https://www.yourdomain.com` and add the
domain to `DJANGO_ALLOWED_HOSTS` / `DJANGO_CSRF_TRUSTED_ORIGINS` (keep `.vercel.app` in the list).

Notes: add client logos as files in `core/static/img/clients/` (admin → *Logo file name*); uploads
don't survive on Vercel. The first visit after a quiet period may take a second or two.
Problems? Vercel → your project → **Logs** shows lines starting with "Database ready" or
"Automatic database setup failed".

### Render — free (alternative)
1. **Free database:** sign up at https://neon.tech → create a project → copy the connection string
   (starts with `postgresql://`, ends with `?sslmode=require`).
2. Push this folder to a GitHub repo.
3. Render → **New → Blueprint** → select the repo. When asked, fill in:
   - `DATABASE_URL` — the Neon connection string
   - `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` — your admin login
     (created automatically on the first deploy)
4. Click **Apply**. In a few minutes the site is live at `https://<service-name>.onrender.com`.
5. Later, add your domain in Render → Settings → Custom domains, then add an environment variable
   `SITE_URL=https://www.yourdomain.com` (and add the domain to `DJANGO_ALLOWED_HOSTS` and
   `DJANGO_CSRF_TRUSTED_ORIGINS`).
6. Submit `https://yourdomain/sitemap.xml` in Google Search Console.

Free-plan notes: the site sleeps after ~15 minutes without visitors and takes up to a minute to wake
on the next visit (upgrade to Starter to avoid this). Put client logos in `core/static/img/clients/`
and type the file name in admin → Client work → *Logo file name*; admin uploads don't survive restarts
on the free plan.

### Any other host
Set the variables in `.env.example`, run `./build.sh`, start with
`gunicorn config.wsgi`. `Procfile` is included for Railway/Heroku-style hosts.

Once the site is permanently on HTTPS for your domain and all subdomains, you can also set
`SECURE_HSTS_INCLUDE_SUBDOMAINS` and `SECURE_HSTS_PRELOAD` in `config/settings.py`.

## Fonts
Bricolage Grotesque and Instrument Sans are self-hosted from `core/static/fonts/`
under the SIL Open Font License (licence files included).

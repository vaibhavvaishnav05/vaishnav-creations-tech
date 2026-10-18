from django.conf import settings

from .models import Service, SiteSettings


def site(request):
    s = SiteSettings.load()
    org = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": s.agency_name,
        "alternateName": s.short_name,
        "url": settings.SITE_URL + "/",
        "description": s.meta_description,
        "email": s.email,
        "telephone": s.phone,
        "address": {"@type": "PostalAddress", "addressCountry": "IN"},
        "knowsAbout": ["Website development", "Django", "SEO", "Generative engine optimisation",
                       "Answer engine optimisation", "n8n automation", "WhatsApp chatbots",
                       "AI and machine learning", "CRM and ERP development"],
        "sameAs": [u for u in [s.linkedin_url, s.instagram_url] if u],
    }
    return {
        "site": s,
        "nav_services": Service.objects.filter(is_published=True),
        "SITE_URL": settings.SITE_URL,
        "NO_DB_MODE": settings.NO_DB_MODE,
        "org_schema": org,
    }

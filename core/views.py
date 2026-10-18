import logging

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import LeadForm
from .models import FAQ, ClientWork, Industry, Service, SiteSettings

log = logging.getLogger(__name__)


def _published_work():
    return ClientWork.objects.filter(is_published=True).select_related("industry")


def home(request):
    work = _published_work()
    return render(request, "core/home.html", {
        "hero_work": work.filter(show_in_hero=True).exclude(project_type="whatsapp_bot")[:6],
        "clients": work.exclude(project_type="whatsapp_bot"),
        "bots": work.filter(project_type="whatsapp_bot"),
        "services": Service.objects.filter(is_published=True),
        "industries": Industry.objects.filter(is_published=True),
        "faqs": FAQ.objects.filter(show_on_home=True),
        "form": LeadForm(),
    })


def services(request):
    return render(request, "core/services.html", {
        "services": Service.objects.filter(is_published=True),
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_published=True)
    return render(request, "core/service_detail.html", {
        "service": service,
        "faqs": service.faqs.all(),
        "related_work": _published_work().filter(services=service)[:6],
        "other_services": Service.objects.filter(is_published=True).exclude(pk=service.pk),
        "form": LeadForm(initial={"service": service}),
    })


def work(request):
    items = _published_work()
    industries = Industry.objects.filter(clientwork__in=items).distinct()
    return render(request, "core/work.html", {"items": items, "industries": industries})


def about(request):
    return render(request, "core/about.html", {
        "industries": Industry.objects.filter(is_published=True),
        "services": Service.objects.filter(is_published=True),
    })


def contact(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")).split(",")[0]
        key = f"lead-rate:{ip}"
        if cache.get(key, 0) >= 5:
            form.add_error(None, "Too many messages from this connection. Please try again in an hour or message us on WhatsApp.")
        elif form.is_valid() and settings.NO_DB_MODE:
            # Nowhere to store it: email it if SMTP is set up, and hand it to WhatsApp.
            lead = form.save(commit=False)
            lead.source_page = request.POST.get("source", "")[:200]
            cache.set(key, cache.get(key, 0) + 1, 3600)
            _notify(request, lead, admin_link=False)
            return redirect(_whatsapp_enquiry_url(lead))
        elif form.is_valid():
            lead = form.save(commit=False)
            lead.source_page = request.POST.get("source", "")[:200]
            lead.save()
            cache.set(key, cache.get(key, 0) + 1, 3600)
            _notify(request, lead)
            return redirect("contact_thanks")
        return render(request, "core/contact.html", {"form": form}, status=400)
    initial = {}
    if slug := request.GET.get("service"):
        initial["service"] = Service.objects.filter(slug=slug).first()
    return render(request, "core/contact.html", {"form": LeadForm(initial=initial)})


def contact_thanks(request):
    return render(request, "core/thanks.html")


def _whatsapp_enquiry_url(lead):
    from urllib.parse import quote
    site = SiteSettings.load()
    lines = [f"Hi, I'm {lead.name}. I'd like to discuss a project."]
    if lead.service:
        lines.append(f"Service: {lead.service.title}")
    if lead.company:
        lines.append(f"Business: {lead.company}")
    if lead.website:
        lines.append(f"Website: {lead.website}")
    lines.append(f"Email: {lead.email}")
    if lead.phone:
        lines.append(f"Phone: {lead.phone}")
    lines += ["", lead.message]
    return f"https://wa.me/{site.whatsapp_number}?text={quote(chr(10).join(lines))}"


def _notify(request, lead, admin_link=True):
    site = SiteSettings.load()
    if not site.notification_email:
        return
    if not settings.EMAIL_HOST and settings.NO_DB_MODE:
        return  # no SMTP configured; the enquiry goes to WhatsApp instead
    admin_url = (request.build_absolute_uri(reverse("admin:core_lead_change", args=[lead.pk]))
                 if admin_link else "")
    body = render_to_string("core/email/new_lead.txt", {"lead": lead, "admin_url": admin_url})
    try:
        send_mail(f"New enquiry: {lead.name}", body, settings.DEFAULT_FROM_EMAIL,
                  [site.notification_email], fail_silently=False)
    except Exception:  # the lead is already saved; never lose it over email trouble
        log.exception("Could not send lead notification email")


@require_GET
def robots_txt(request):
    lines = ["User-agent: *", "Disallow: /admin/", "Allow: /", "",
             f"Sitemap: {settings.SITE_URL}/sitemap.xml"]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def llms_txt(request):
    """Plain-language summary for AI assistants (GEO). See llmstxt.org."""
    return render(request, "core/llms.txt", {
        "services": Service.objects.filter(is_published=True),
        "industries": Industry.objects.filter(is_published=True),
        "work": _published_work().exclude(project_type="whatsapp_bot"),
        "faqs": FAQ.objects.all(),
    }, content_type="text/plain; charset=utf-8")


def page_not_found(request, exception):
    return render(request, "core/404.html", status=404)

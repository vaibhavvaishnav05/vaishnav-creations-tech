from django.core import mail
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import ClientWork, Lead, Service


class PagesTest(TestCase):
    def test_public_pages_load(self):
        for name in ["home", "services", "work", "about", "contact", "contact_thanks"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)
        for s in Service.objects.all():
            self.assertEqual(self.client.get(s.get_absolute_url()).status_code, 200, s.slug)
        for url in ["/robots.txt", "/llms.txt", "/sitemap.xml"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_seeded_content(self):
        self.assertEqual(Service.objects.count(), 8)
        home = self.client.get("/").content.decode()
        for name in ["advocatekvsoni.in", "silverlakepremium.com", "homiestays.in", "50+"]:
            self.assertIn(name, home)

    def test_unapproved_client_is_hidden(self):
        ClientWork.objects.create(client_name="Secret Client Ltd", summary="x", is_published=False)
        for url in ["/", "/work/", "/llms.txt"]:
            self.assertNotIn("Secret Client Ltd", self.client.get(url).content.decode())

    def test_unverified_testimonial_is_hidden(self):
        c = ClientWork.objects.filter(is_published=True).first()
        c.testimonial_quote, c.testimonial_author = "Great work, unverified", "Someone"
        c.save()
        self.assertNotIn("Great work, unverified", self.client.get("/work/").content.decode())
        c.testimonial_verified = True
        c.save()
        self.assertIn("Great work, unverified", self.client.get("/work/").content.decode())


class LeadFormTest(TestCase):
    def setUp(self):
        cache.clear()

    def payload(self, **kw):
        d = {"name": "Asha", "email": "asha@example.com", "message": "Need a website", "source": "test"}
        d.update(kw)
        return d

    def test_lead_saved_and_emailed(self):
        r = self.client.post(reverse("contact"), self.payload())
        self.assertRedirects(r, reverse("contact_thanks"))
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Asha", mail.outbox[0].subject)

    def test_validation_errors(self):
        r = self.client.post(reverse("contact"), self.payload(email="not-an-email", message=""))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Lead.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        self.client.post(reverse("contact"), self.payload(nickname="spam"))
        self.assertEqual(Lead.objects.count(), 0)

    def test_rate_limit(self):
        for _ in range(6):
            self.client.post(reverse("contact"), self.payload())
        self.assertEqual(Lead.objects.count(), 5)


class AdminTest(TestCase):
    def test_admin_requires_login(self):
        r = self.client.get("/admin/core/lead/")
        self.assertEqual(r.status_code, 302)


class LogoFileTest(TestCase):
    def test_static_logo_file_is_used(self):
        c = ClientWork.objects.filter(is_published=True, project_type="website").first()
        c.logo_file = "README.txt"   # any file that exists in static/img/clients/
        c.save()
        self.assertIn("/static/img/clients/README.txt", self.client.get("/").content.decode())

    def test_no_logo_shows_name(self):
        c = ClientWork.objects.filter(is_published=True, project_type="website").first()
        self.assertEqual(c.logo_url, "")
        self.assertIn(c.client_name, self.client.get("/").content.decode())

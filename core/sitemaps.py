from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Service


class StaticSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return ["home", "services", "work", "about", "contact"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "home" else 0.7


class ServiceSitemap(Sitemap):
    protocol = "https"
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_published=True)

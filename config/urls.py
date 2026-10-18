from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from core.sitemaps import ServiceSitemap, StaticSitemap

handler404 = "core.views.page_not_found"

urlpatterns = [] if settings.NO_DB_MODE else [path("admin/", admin.site.urls)]
urlpatterns += [
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": StaticSitemap, "services": ServiceSitemap}},
         name="django.contrib.sitemaps.views.sitemap"),
    path("", include("core.urls")),
    # Uploaded logos. Fine for a small site; use a CDN/object storage if traffic grows.
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

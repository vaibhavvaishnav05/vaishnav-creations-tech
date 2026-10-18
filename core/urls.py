from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("work/", views.work, name="work"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/thanks/", views.contact_thanks, name="contact_thanks"),
    path("robots.txt", views.robots_txt),
    path("llms.txt", views.llms_txt),
]

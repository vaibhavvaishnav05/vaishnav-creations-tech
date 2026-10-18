from django.contrib import admin
from django.utils.html import format_html

from .models import FAQ, ClientWork, Industry, Lead, Service, SiteSettings

admin.site.site_header = "Vaishnav Creations — website admin"
admin.site.site_title = "Vaishnav Creations admin"
admin.site.index_title = "Manage the website"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Brand", {"fields": ["agency_name", "short_name", "meta_description"]}),
        ("Homepage", {"fields": ["hero_title", "hero_subtitle", "clients_count",
                                 "countries_count", "countries_text", "about_text"]}),
        ("Contact", {"fields": ["email", "phone", "whatsapp_number", "whatsapp_message",
                                "address", "linkedin_url", "instagram_url", "notification_email"]}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "order", "is_published"]
    list_editable = ["order", "is_published"]
    prepopulated_fields = {"slug": ["name"]}


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 0
    fields = ["question", "answer", "show_on_home", "order"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "billing", "order", "is_published"]
    list_editable = ["order", "is_published"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [FAQInline]


@admin.register(ClientWork)
class ClientWorkAdmin(admin.ModelAdmin):
    list_display = ["logo_preview", "client_name", "project_type", "industry", "is_published",
                    "show_in_hero", "order"]
    list_display_links = ["logo_preview", "client_name"]
    list_editable = ["is_published", "show_in_hero", "order"]
    list_filter = ["is_published", "project_type", "industry"]
    search_fields = ["client_name", "summary", "location"]
    filter_horizontal = ["services"]
    prepopulated_fields = {"slug": ["client_name"]}
    fieldsets = [
        (None, {"fields": ["client_name", "slug", "project_type", "industry", "location",
                           "summary", "services"]}),
        ("Links & logo", {"fields": ["live_url", "link_label", "logo_file", "logo", "logo_on_light_plate"]}),
        ("Visibility", {"fields": ["is_published", "show_in_hero", "order"]}),
        ("Proof (only with written client approval)", {
            "classes": ["collapse"],
            "fields": ["case_study_url", "testimonial_quote", "testimonial_author",
                       "testimonial_role", "testimonial_verified"],
        }),
    ]

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if obj.logo_url:
            return format_html('<img src="{}" style="max-height:28px;max-width:90px">', obj.logo_url)
        return "—"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "service", "show_on_home", "order"]
    list_editable = ["show_on_home", "order"]
    list_filter = ["service", "show_on_home"]


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["created_at", "name", "email", "phone", "service", "status"]
    list_editable = ["status"]
    list_filter = ["status", "service", "created_at"]
    search_fields = ["name", "email", "company", "message"]
    readonly_fields = ["name", "email", "phone", "company", "website", "service", "message",
                       "source_page", "created_at"]
    fields = readonly_fields + ["status", "notes"]

    def has_add_permission(self, request):
        return False

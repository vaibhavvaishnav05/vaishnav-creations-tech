from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

ICON_CHOICES = [
    ("globe", "Globe / website"), ("search", "Search"), ("spark", "AI sparkle"),
    ("flow", "Workflow"), ("chat", "Chat"), ("users", "People / team"),
    ("chart", "Chart"), ("megaphone", "Megaphone"), ("database", "Database"),
    ("hotel", "Hotel"), ("scale", "Law / scales"), ("bank", "Finance / bank"),
    ("moon", "Astrology / moon & star"), ("bag", "Retail bag"), ("chip", "SaaS / chip"),
    ("car", "Automobile"), ("sofa", "Furniture / sofa"), ("home", "Home / stays"),
]


class SiteSettings(models.Model):
    """One row of editable, site-wide content. Edit it in admin → Site settings."""
    agency_name = models.CharField(max_length=120, default="Vaishnav Creations Technologies")
    short_name = models.CharField(max_length=60, default="Vaishnav Creations")
    hero_title = models.CharField(
        max_length=200,
        default="Websites, automation and search that bring customers to your business",
    )
    hero_subtitle = models.TextField(
        default="We design and build websites, set up n8n automations and WhatsApp chatbots, "
                "and run monthly SEO, GEO and AEO so you're found on Google and in AI answers.",
    )
    clients_count = models.CharField("Clients figure", max_length=20, default="50+")
    countries_count = models.CharField("Countries figure", max_length=20, default="3+")
    countries_text = models.CharField(
        max_length=200, blank=True, default="",
        help_text="Optional, e.g. 'India, USA, UAE'. Leave blank to show only the count.",
    )
    about_text = models.TextField(
        default="Vaishnav Creations Technologies is a software and digital growth agency. "
                "We build websites and web apps, automate operations with n8n and AI, and run "
                "search marketing on a monthly basis — for hotels, law practices, furniture and "
                "interior brands, finance, retail, SaaS and more.",
    )
    email = models.EmailField(default="contact@vaishnavcreations.com")
    phone = models.CharField(max_length=30, default="+91 93584 59213")
    whatsapp_number = models.CharField(
        max_length=20, default="919358459213", help_text="Digits only, with country code."
    )
    whatsapp_message = models.CharField(
        max_length=200, default="Hi, I'd like to discuss a project with Vaishnav Creations."
    )
    linkedin_url = models.URLField(
        blank=True, default="https://www.linkedin.com/in/creations-agency-online-48b1a3375/"
    )
    instagram_url = models.URLField(blank=True, default="")
    address = models.CharField(max_length=200, blank=True, default="India")
    notification_email = models.EmailField(
        blank=True, default="contact@vaishnavcreations.com",
        help_text="New enquiries from the contact form are emailed here.",
    )
    meta_description = models.CharField(
        max_length=170,
        default="Website development, n8n automation, WhatsApp chatbots and monthly SEO, GEO & AEO "
                "for growing businesses. 50+ clients across 3+ countries.",
    )

    class Meta:
        verbose_name = verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def whatsapp_link(self):
        from urllib.parse import quote
        return f"https://wa.me/{self.whatsapp_number}?text={quote(self.whatsapp_message)}"


class Industry(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="globe")
    blurb = models.CharField(max_length=220, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "industries"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    BILLING = [
        ("monthly", "Monthly retainer"),
        ("project", "Per project"),
        ("project_monthly", "Project + monthly support"),
        ("team", "Dedicated team"),
    ]
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="globe")
    summary = models.CharField(max_length=220, help_text="One sentence shown in lists.")
    intro = models.TextField(help_text="Opening paragraph(s) on the service page.")
    deliverables = models.TextField(help_text="One item per line.")
    tools = models.CharField(max_length=250, blank=True, help_text="Comma separated, e.g. Django, Shopify")
    billing = models.CharField(max_length=20, choices=BILLING, default="project")
    meta_description = models.CharField(max_length=170, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("service_detail", args=[self.slug])

    @property
    def deliverable_list(self):
        return [x.strip() for x in self.deliverables.splitlines() if x.strip()]

    @property
    def tool_list(self):
        return [x.strip() for x in self.tools.split(",") if x.strip()]


class ClientWork(models.Model):
    """A client project shown on the site. Only rows with 'Client approved' ticked appear."""
    TYPES = [
        ("website", "Website"), ("ecommerce", "E-commerce"), ("whatsapp_bot", "WhatsApp chatbot"),
        ("automation", "Automation"), ("seo", "SEO / GEO / AEO"), ("webapp", "Web app"),
        ("other", "Other"),
    ]
    client_name = models.CharField(max_length=120, help_text="Exact brand name of the client.")
    slug = models.SlugField(unique=True, blank=True)
    project_type = models.CharField(max_length=20, choices=TYPES, default="website")
    industry = models.ForeignKey(Industry, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=120, blank=True)
    summary = models.CharField(max_length=240, help_text="One line: what you built or did.")
    services = models.ManyToManyField(Service, blank=True)
    live_url = models.URLField(blank=True, help_text="Live website, or WhatsApp link for a chatbot.")
    link_label = models.CharField(max_length=40, blank=True, help_text="Optional, e.g. 'Try the bot'.")
    logo_file = models.CharField(
        "Logo file name", max_length=120, blank=True,
        help_text="Recommended. Put the logo in core/static/img/clients/ in the project, push to GitHub, "
                  "and type the file name here (e.g. silver-lake.svg). Survives every redeploy.",
    )
    logo = models.ImageField(
        "Or upload a logo", upload_to="clients/", blank=True,
        help_text="Only keeps working on hosting with a persistent disk. On Render's free plan uploads "
                  "disappear after a restart — use 'Logo file name' instead.",
    )
    logo_on_light_plate = models.BooleanField(
        default=False, help_text="Not needed on this white site; kept for very light logos (adds a soft grey plate).",
    )
    is_published = models.BooleanField(
        "Client approved", default=False,
        help_text="Tick only once the client has agreed to be shown on the website.",
    )
    show_in_hero = models.BooleanField(default=False, help_text="List in the homepage 'recent work' panel.")
    order = models.PositiveIntegerField(default=0)

    # Optional proof — only with the client's written approval.
    case_study_url = models.URLField(blank=True)
    testimonial_quote = models.TextField(blank=True, help_text="Client's own words, unedited.")
    testimonial_author = models.CharField(max_length=100, blank=True)
    testimonial_role = models.CharField(max_length=100, blank=True)
    testimonial_verified = models.BooleanField(
        default=False, help_text="Tick only if you hold the client's written approval for this quote.",
    )

    class Meta:
        ordering = ["order", "client_name"]
        verbose_name = verbose_name_plural = "client work"

    def __str__(self):
        return f"{self.client_name} — {self.get_project_type_display()}"

    def clean(self):
        if self.testimonial_verified and not (self.testimonial_quote and self.testimonial_author):
            raise ValidationError("A verified testimonial needs both the quote and the author's name.")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.client_name}-{self.project_type}")[:45] or "client"
            slug, n = base, 2
            while ClientWork.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def domain(self):
        from urllib.parse import urlparse
        if not self.live_url or "whatsapp.com" in self.live_url or "wa.me" in self.live_url:
            return ""
        return urlparse(self.live_url).netloc.removeprefix("www.")

    @property
    def logo_url(self):
        if self.logo_file:
            from django.templatetags.static import static
            try:
                return static(f"img/clients/{self.logo_file}")
            except ValueError:  # file missing from the build → fall back to the text name
                return ""
        return self.logo.url if self.logo else ""

    @property
    def is_bot(self):
        return self.project_type == "whatsapp_bot"

    @property
    def has_verified_testimonial(self):
        return self.testimonial_verified and bool(self.testimonial_quote and self.testimonial_author)


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    service = models.ForeignKey(
        Service, null=True, blank=True, on_delete=models.SET_NULL, related_name="faqs",
        help_text="Leave empty for a general FAQ.",
    )
    show_on_home = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"

    def __str__(self):
        return self.question


class Lead(models.Model):
    STATUS = [("new", "New"), ("contacted", "Contacted"), ("proposal", "Proposal sent"),
              ("won", "Won"), ("lost", "Lost")]
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=150, blank=True)
    website = models.CharField(max_length=200, blank=True)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)
    message = models.TextField()
    source_page = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="new")
    notes = models.TextField(blank=True, help_text="Internal notes.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"

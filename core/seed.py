"""Initial website content. Loaded once by migration 0002; edit everything in admin afterwards.

Client entries come from the agency's own list of delivered projects. Nothing here is a
testimonial, case study or result figure — add those in admin only with client approval.
"""

INDUSTRIES = [
    # name, icon, blurb
    ("Hotels & Hospitality", "hotel", "Booking-focused hotel and stay websites, local SEO and guest enquiry automation."),
    ("Advocates & Law Firms", "scale", "Professional practice websites, practice-area pages and local search visibility."),
    ("Finance", "bank", "Trust-first websites, lead capture and CRM workflows for finance businesses."),
    ("Astrology", "moon", "Consultation booking, WhatsApp enquiries and content that ranks for local searches."),
    ("Retail", "bag", "Store websites, product catalogues and e-commerce on Shopify or custom builds."),
    ("SaaS Products", "chip", "Product sites, web apps, AI features and search visibility for software products."),
    ("Automobiles", "car", "Dealer and service websites, inventory pages and lead follow-up automation."),
    ("Interiors & Furniture", "sofa", "Showroom websites, catalogue pages and WhatsApp assistants for furniture and interior brands."),
]

SERVICES = [
    {
        "title": "Website Development", "slug": "website-development", "icon": "globe",
        "billing": "project", "order": 1,
        "summary": "Fast, mobile-first business websites, e-commerce stores and web apps built to bring in enquiries.",
        "intro": "Your website is usually the first conversation a customer has with your business. We design and build sites that load quickly, read clearly on a phone and make it easy to call, message or book.\n\nWe build on Django and Python for custom sites and web apps, Shopify for online stores and WordPress where your team wants to edit pages themselves.",
        "deliverables": "Business and corporate websites\nE-commerce stores on Shopify or custom builds\nLanding pages for ads and launches\nBooking, enquiry and catalogue features\nAdmin panels so your team can update content\nTechnical SEO built in from day one\nHosting setup, SSL and handover",
        "tools": "Django, Python, React, Shopify, WordPress, Vercel",
        "meta": "Custom website development in Django, Shopify and WordPress — fast, mobile-first sites built for enquiries.",
    },
    {
        "title": "SEO, GEO & AEO", "slug": "seo-geo-aeo", "icon": "search",
        "billing": "monthly", "order": 2,
        "summary": "Monthly search work so you're found on Google, quoted in AI answers and picked for direct answers.",
        "intro": "Customers now find businesses in three places: Google results, AI assistants like ChatGPT, Gemini and Perplexity, and direct answers such as featured snippets and voice search. We work on all three every month.\n\nSEO (search engine optimisation) improves your rankings on Google. GEO (generative engine optimisation) makes your business easy for AI assistants to understand and recommend. AEO (answer engine optimisation) structures your content so it is chosen as the direct answer to a question.",
        "deliverables": "Technical SEO audit and fixes\nKeyword and question research for your market\nOn-page optimisation of key pages\nGoogle Business Profile and local SEO\nStructured data (schema) for rich results\nContent written to answer real customer questions\nAI-visibility checks across ChatGPT, Gemini and Perplexity\nMonthly report of rankings, traffic and enquiries",
        "tools": "Google Search Console, Google Analytics 4, Google Business Profile, Semrush, Schema.org",
        "meta": "Monthly SEO, GEO and AEO services — rank on Google and get recommended in ChatGPT, Gemini and Perplexity answers.",
    },
    {
        "title": "n8n Automation", "slug": "n8n-automation", "icon": "flow",
        "billing": "project_monthly", "order": 3,
        "summary": "Complete n8n services — setup, hosting, workflows and support — to take repetitive work off your team.",
        "intro": "n8n connects the tools you already use — forms, WhatsApp, email, Google Sheets, your CRM — and moves information between them automatically. We handle everything from installing n8n to building and maintaining your workflows.\n\nTypical first projects: send every website enquiry to your CRM and WhatsApp, follow up leads automatically, generate reports, and sync orders between systems.",
        "deliverables": "n8n installation — self-hosted or n8n Cloud\nWorkflow design around your real process\nLead capture to CRM, WhatsApp and email\nAI steps inside workflows (summaries, replies, classification)\nIntegrations with Google Workspace, Shopify, CRMs and APIs\nError alerts, logging and documentation\nMonthly maintenance and new workflows on request",
        "tools": "n8n, Docker, Google Workspace, WhatsApp Business API, OpenAI, REST APIs",
        "meta": "Complete n8n automation services — installation, self-hosting, custom workflows, AI steps and monthly support.",
    },
    {
        "title": "WhatsApp & AI Chatbots", "slug": "whatsapp-ai-chatbots", "icon": "chat",
        "billing": "project", "order": 4,
        "summary": "Chatbots that answer customer questions, recommend products and capture leads on WhatsApp and your website.",
        "intro": "Most of your customers would rather send a message than fill in a form. We build WhatsApp and website chatbots that reply instantly, answer common questions, help people choose the right product and hand serious enquiries to your team.",
        "deliverables": "WhatsApp chatbot on your business number\nWebsite chat assistant\nProduct and service guidance flows\nLead capture into your CRM or Google Sheet\nHand-over to a human when needed\nAI answers trained on your own information",
        "tools": "WhatsApp Business API, n8n, OpenAI, Claude, Python",
        "meta": "WhatsApp and AI chatbots that answer customers, recommend products and capture leads automatically.",
    },
    {
        "title": "AI & Machine Learning", "slug": "ai-machine-learning", "icon": "spark",
        "billing": "project", "order": 5,
        "summary": "Practical AI for your business — LLM apps, document assistants, predictions and data analysis.",
        "intro": "We build AI features that solve a specific problem in your business, rather than AI for its own sake. That can be an assistant that answers questions from your documents, a model that predicts demand, or an analysis that shows where your revenue comes from.",
        "deliverables": "LLM and generative AI apps\nAssistants that answer from your own documents (RAG)\nMachine learning models for prediction and classification\nData analysis and dashboards\nAI integration into existing software",
        "tools": "Python, LangChain, FastAPI, scikit-learn, OpenAI, Claude, PostgreSQL",
        "meta": "AI and machine learning development — LLM apps, document assistants, predictive models and data analysis.",
    },
    {
        "title": "CRM, ERP & Admin Panels", "slug": "crm-erp-admin-panels", "icon": "database",
        "billing": "project_monthly", "order": 6,
        "summary": "Custom CRM, ERP and admin systems that fit how your business actually runs.",
        "intro": "Off-the-shelf software rarely matches your process exactly. We build and customise CRM, ERP and admin systems in Django so your team manages leads, orders, stock and staff in one place.",
        "deliverables": "Custom CRM for leads and customers\nERP modules for orders, inventory and billing\nAdmin panels for websites and apps\nRole-based access for your team\nReports and exports\nIntegrations with your website and automations",
        "tools": "Django, Python, PostgreSQL, REST APIs, n8n",
        "meta": "Custom CRM, ERP and admin panel development in Django, built around your business process.",
    },
    {
        "title": "Digital Marketing", "slug": "digital-marketing", "icon": "megaphone",
        "billing": "monthly", "order": 7,
        "summary": "Social media, paid ads and content managed monthly, tied to enquiries rather than likes.",
        "intro": "We plan and run your social media and paid campaigns each month, and track them through to enquiries so you can see what your budget is doing.",
        "deliverables": "Social media management for Instagram, Facebook and LinkedIn\nGoogle Ads and Meta Ads campaigns\nContent and creative planning\nLanding pages for campaigns\nConversion tracking setup\nMonthly performance report",
        "tools": "Meta Ads, Google Ads, LinkedIn, Google Analytics 4",
        "meta": "Monthly digital marketing — social media management, Google Ads and Meta Ads tracked to real enquiries.",
    },
    {
        "title": "Tech Staffing for Projects", "slug": "tech-staffing", "icon": "users",
        "billing": "team", "order": 8,
        "summary": "Developers and specialists who join your project for a set period, for a specific service.",
        "intro": "When your project needs more hands, we provide skilled people for the specific service you need — a Django developer, an automation engineer, an SEO specialist — for as long as the project needs them. They work to your process and report to your team.",
        "deliverables": "Python and Django developers\nFrontend and website developers\nn8n and automation engineers\nAI / ML developers\nSEO and digital marketing specialists\nFlexible monthly engagement",
        "tools": "",
        "meta": "Tech staffing for projects — Django, automation, AI and SEO specialists who join your team for a set period.",
    },
]

CLIENTS = [
    # client_name, type, industry, location, summary, url, show_in_hero
    ("The Roundtree, Amagansett", "website", "Hotels & Hospitality", "Amagansett, New York, USA",
     "Website for a boutique hotel in the Hamptons with rooms, cottages and guest experiences.",
     "https://www.theroundtreehotels.com/", True),
    ("Adv. K. V. Soni", "website", "Advocates & Law Firms", "Navi Mumbai, India",
     "Practice website for an advocate covering criminal, civil, family, cyber and property law.",
     "https://advocatekvsoni.in/", True),
    ("Silver Lake Premium", "website", "Interiors & Furniture", "Jaipur, India",
     "Website for a premium furniture showroom with living, bedroom, dining and office ranges.",
     "https://www.silverlakepremium.com/", True),
    ("FixKart Interio", "website", "Interiors & Furniture", "Jaipur, India",
     "Website for an interior design studio offering modular kitchens, wardrobes and turnkey interiors.",
     "https://www.fixkartinterio.online/", True),
    ("Fine & Shine Furnishers", "website", "Interiors & Furniture", "Ludhiana, India",
     "Website for a luxury furniture showroom with sofas, beds, dining sets and custom pieces.",
     "https://fine-and-shine.vercel.app/", True),
    ("Homiestays", "website", "Hotels & Hospitality", "Delhi, India",
     "Website for a staycation platform listing villas and farmhouses across India.",
     "https://www.homiestays.in/", True),
]

BOTS = [
    # client_name, industry, summary, url
    ("Furniture store assistant", "Interiors & Furniture",
     "WhatsApp chatbot that helps shoppers choose the right furniture for home or office.",
     "https://api.whatsapp.com/send?phone=917300052827&text=Hi%20there!%20Do%20you%20need%20assistance%20in%20choosing%20the%20right%20furniture%20for%20your%20home/office?"),
    ("Customer enquiry assistant", None,
     "WhatsApp chatbot that answers common customer questions and collects enquiries.",
     "https://api.whatsapp.com/send/?phone=919251151330&text&type=phone_number&app_absent=0"),
]

FAQS = [
    ("What services does Vaishnav Creations Technologies offer?",
     "We build websites, web apps, CRM and ERP systems; set up n8n automations and WhatsApp or AI chatbots; run SEO, GEO and AEO and digital marketing every month; and provide developers and specialists for tech projects.", None),
    ("What is the difference between SEO, GEO and AEO?",
     "SEO improves your ranking in Google search results. GEO (generative engine optimisation) helps AI assistants like ChatGPT, Gemini and Perplexity understand and recommend your business. AEO (answer engine optimisation) shapes your content so it is chosen as the direct answer in featured snippets and voice search. We work on all three in one monthly plan.", "seo-geo-aeo"),
    ("How long does SEO take to show results?",
     "Technical fixes and Google Business Profile improvements can show within weeks. Ranking for competitive searches usually takes three to six months of consistent monthly work. We report progress every month so you can see what changed.", "seo-geo-aeo"),
    ("What can n8n automate for my business?",
     "Anything that moves information between tools: sending website enquiries to your CRM and WhatsApp, following up leads, creating invoices, syncing orders and stock, and sending daily or weekly reports. We can host n8n on your own server or use n8n Cloud.", "n8n-automation"),
    ("Can you provide developers for our project?",
     "Yes. We provide skilled people for a specific service — for example a Django developer, an automation engineer or an SEO specialist — for the duration of your project, billed monthly.", "tech-staffing"),
    ("Which industries do you work with?",
     "Hotels and hospitality, advocates and law firms, finance, astrology, retail, SaaS products, automobiles, and interiors and furniture — and other growing businesses.", None),
    ("Do you work with clients outside India?",
     "Yes. We have worked with 50+ clients across 3+ countries and work remotely with clients wherever they are.", None),
    ("How do we get started?",
     "Send us a message on WhatsApp or through the contact form. We'll have a short call to understand your business, then send a clear proposal with scope, timeline and price.", None),
]


def run(apps):
    Industry = apps.get_model("core", "Industry")
    Service = apps.get_model("core", "Service")
    ClientWork = apps.get_model("core", "ClientWork")
    FAQ = apps.get_model("core", "FAQ")
    SiteSettings = apps.get_model("core", "SiteSettings")

    SiteSettings.objects.get_or_create(pk=1)

    ind = {}
    for i, (name, icon, blurb) in enumerate(INDUSTRIES):
        from django.utils.text import slugify
        ind[name], _ = Industry.objects.get_or_create(
            slug=slugify(name), defaults={"name": name, "icon": icon, "blurb": blurb, "order": i})

    svc = {}
    for s in SERVICES:
        svc[s["slug"]], _ = Service.objects.get_or_create(slug=s["slug"], defaults={
            "title": s["title"], "icon": s["icon"], "billing": s["billing"], "order": s["order"],
            "summary": s["summary"], "intro": s["intro"], "deliverables": s["deliverables"],
            "tools": s["tools"], "meta_description": s["meta"]})

    for i, (name, ptype, industry, loc, summary, url, hero) in enumerate(CLIENTS):
        from django.utils.text import slugify
        cw, created = ClientWork.objects.get_or_create(slug=slugify(name)[:45], defaults={
            "client_name": name, "project_type": ptype, "industry": ind.get(industry),
            "location": loc, "summary": summary, "live_url": url, "show_in_hero": hero,
            "is_published": True, "order": i})
        if created:
            cw.services.add(svc["website-development"])

    for i, (name, industry, summary, url) in enumerate(BOTS):
        from django.utils.text import slugify
        cw, created = ClientWork.objects.get_or_create(slug=slugify(name)[:45], defaults={
            "client_name": name, "project_type": "whatsapp_bot", "industry": ind.get(industry),
            "summary": summary, "live_url": url, "link_label": "Try the bot",
            "is_published": True, "order": 20 + i})
        if created:
            cw.services.add(svc["whatsapp-ai-chatbots"])

    for i, (q, a, slug) in enumerate(FAQS):
        FAQ.objects.get_or_create(question=q, defaults={
            "answer": a, "service": svc.get(slug) if slug else None, "order": i})

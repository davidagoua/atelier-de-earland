"""Génère les pages HTML du site.

Usage (depuis la racine du projet) : python3 tools/build.py .
Les fichiers .html sont régénérés : faire les modifications ici, pas dans le HTML.
"""
import datetime, html as htmllib, json, os, re, sys, urllib.parse
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

# Adresse du site, sans "/" final. À changer le jour où un nom de domaine est acheté.
SITE_URL = "https://ccq9a2md4vm6u5vbu8qilqpv.songon.shop"
SITE_NAME = "Les Ateliers de Earland"
TODAY = datetime.date.today().isoformat()
TEL = "+2250759471517"
TEL_TXT = "+225 07 59 47 15 17"
WA_MSG = urllib.parse.quote("Bonjour Les Ateliers de Earland, je souhaite échanger sur mon projet événementiel.")
WA = f"https://wa.me/2250759471517?text={WA_MSG}"
IG = "https://www.instagram.com/les_ateliers_de_earland_/"

NAV = [
    ("index.html", "Accueil"),
    ("a-propos.html", "À propos"),
    ("expertises.html", "Expertises"),
    ("realisations.html", "Réalisations"),
    ("journal.html", "Journal"),
    ("contact.html", "Contact"),
]

ICON = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11zM12 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/></svg>',
    "user": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
    "building": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 21V5l8-2v18M12 7h8v14M8 9h0M8 13h0M8 17h0M16 11h0M16 15h0M2 21h20"/></svg>',
    "rings": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="14" r="5"/><circle cx="15" cy="14" r="5"/><path d="M9 6l1.5-2h3L15 6"/></svg>',
    "home": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11l9-7 9 7M5 9.5V20h14V9.5M10 20v-5h4v5"/></svg>',
    "glass": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h14l-7 8zM12 12v7m-4 1h8M16 4l2-2"/></svg>',
    "mic": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/></svg>',
}

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.7c-2 0-4-.5-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7zm5.9-8c-.3-.2-1.9-1-2.2-1-.3-.2-.5-.2-.7.1l-1 1.3c-.2.2-.4.2-.7 0-.3-.1-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6.3-.5v-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6 0-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5 .8.4 1.4.6 1.9.7.8.3 1.5.2 2.1.1.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5l-.6-.4z"/></svg>'


def url_for(filename):
    return f"{SITE_URL}/" if filename == "index.html" else f"{SITE_URL}/{filename}"


def breadcrumb(filename, label):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": url_for("index.html")},
            {"@type": "ListItem", "position": 2, "name": label, "item": url_for(filename)},
        ],
    }


IMG_SIZES = {}


def add_image_sizes(html):
    """Ajoute width/height aux images locales (évite les décalages de mise en page)."""
    def fix(match):
        tag = match.group(0)
        if " width=" in tag:
            return tag
        src = match.group(1)
        if not os.path.exists(os.path.join(OUT, src)):
            return tag
        if src not in IMG_SIZES:
            with Image.open(os.path.join(OUT, src)) as im:
                IMG_SIZES[src] = im.size
        w, h = IMG_SIZES[src]
        return tag.replace(f'src="{src}"', f'src="{src}" width="{w}" height="{h}"')
    return re.sub(r'<img src="(images/[^"]+)"[^>]*>', fix, html)


PAGES = []


def page(filename, title, description, body, extra_end="", schemas=(), indexable=True):
    nav = "\n".join(
        f'        <a href="{href}"{" aria-current=\"page\"" if href == filename else ""}>{label}</a>'
        for href, label in NAV
    )
    title = htmllib.escape(title, quote=False).replace('"', "&quot;")
    description = htmllib.escape(description, quote=False).replace('"', "&quot;")
    canonical = url_for(filename)
    robots = "index, follow, max-image-preview:large" if indexable else "noindex, follow"
    jsonld = "\n".join(
        '  <script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
        for data in schemas
    )
    if indexable:
        PAGES.append(filename)
    footer_nav = "\n".join(f'          <li><a href="{href}">{label}</a></li>' for href, label in NAV)
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#141110">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}/images/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="L'équipe des Ateliers de Earland lors d'un événement">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE_URL}/images/og-image.jpg">
  <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
  <link rel="apple-touch-icon" href="images/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Allura&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
{jsonld}
</head>
<body>

  <header class="header" id="header">
    <div class="container header__inner">
      <a href="index.html" class="header__logo">
        <img src="images/logo.jpg" alt="Logo Les Ateliers de Earland">
        <span>Les Ateliers <strong>de Earland</strong></span>
      </a>
      <nav class="nav" id="nav" aria-label="Navigation principale">
{nav}
      </nav>
      <a href="contact.html" class="btn btn--small header__cta">Parlons de votre projet</a>
      <button class="nav-toggle" id="navToggle" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="nav">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <main>
{body}
  </main>

  <footer class="footer">
    <div class="container footer__inner">
      <div class="footer__brand">
        <img src="images/logo.jpg" alt="Logo Les Ateliers de Earland">
        <p class="script">Créer. Recevoir. Célébrer.</p>
        <p>Structure événementielle portée par Earland : event planning, wedding planning, gastronomie événementielle, chef privé, cocktails et mignardises. Abidjan et partout en Côte d'Ivoire.</p>
      </div>
      <div>
        <h4>Navigation</h4>
        <ul>
{footer_nav}
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{TEL}">{TEL_TXT}</a></li>
          <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
          <li>Abidjan, Côte d'Ivoire</li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <p>© <span id="year"></span> Les Ateliers de Earland. Tous droits réservés.</p>
    </div>
  </footer>

  <a href="{WA}" class="wa-float" target="_blank" rel="noopener" aria-label="Échanger sur WhatsApp">
    {WA_SVG}
  </a>
{extra_end}
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
  <script src="js/main.js" defer></script>
  <script src="js/animations.js" defer></script>
</body>
</html>
"""
    with open(f"{OUT}/{filename}", "w") as f:
        f.write(add_image_sizes(html))


def page_hero(eyebrow, title, text, image):
    return f"""    <section class="page-hero">
      <div class="page-hero__bg" aria-hidden="true"><img src="images/galerie/{image}" alt="" fetchpriority="high"></div>
      <div class="container">
        <p class="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p>{text}</p>
      </div>
    </section>
"""


CTA_BAND = """    <section class="cta-band">
      <div class="container">
        <p class="script">Créer. Recevoir. Célébrer.</p>
        <h2>Parlons de votre projet</h2>
        <p>Mariage, événement d'entreprise, dîner privé ou célébration : racontez-nous votre histoire, nous imaginons l'expérience qui vous ressemble.</p>
        <a href="contact.html" class="btn">Parlons de votre projet</a>
      </div>
    </section>
"""

EXPERTISES = [
    ("event-planner", "01", "Event Planner", "Concevoir. Organiser. Coordonner.",
     "Événements privés, professionnels, célébrations, lancements, anniversaires, soirées."),
    ("wedding-planner", "02", "Wedding Planner", "Imaginer votre histoire. Orchestrer votre journée.",
     "Organisation, coordination du jour J, gestion des prestataires et expérience invités."),
    ("chef-executif", "03", "Chef Exécutif Événementiel", "Créer une expérience gastronomique adaptée à votre événement.",
     "Menus, buffets, cocktails, mignardises et scénographie culinaire."),
    ("chef-prive", "04", "Chef Privé", "Faire entrer l'expérience gastronomique dans votre intimité.",
     "Dîners privés, réception à domicile, menus sur mesure."),
    ("cocktails-mignardises", "05", "Cocktails &amp; Mignardises", "Une offre gastronomique transversale.",
     "Cocktails signature, mocktails, mignardises et créations personnalisées."),
]

VALUES = [
    ("Sur mesure", "Chaque événement est pensé selon l'histoire, les besoins et le budget du client."),
    ("Créativité", "Transformer une idée en concept, puis un concept en expérience."),
    ("Rigueur", "Planning, coordination, logistique et suivi : chaque détail compte."),
    ("Art de recevoir", "Créer une expérience dont les invités se souviennent."),
]

AUDIENCES = [
    ("user", "Particuliers", "Mariages, anniversaires, baptêmes, dîners privés, célébrations."),
    ("building", "Entreprises", "Séminaires, cocktails, lancements, team building, cérémonies."),
    ("rings", "Couples", "Organisation, coordination et expérience invités."),
    ("home", "Hôtes &amp; particuliers", "Chef privé, réception à domicile, dîner sur mesure."),
]


def values_html():
    items = "\n".join(
        f"""          <div class="value">
            <span class="value__num">0{i}</span>
            <h3>{name}</h3>
            <p>{text}</p>
          </div>""" for i, (name, text) in enumerate(VALUES, 1))
    return f'        <div class="values" data-stagger>\n{items}\n        </div>'


def audiences_section(cls="section section--cream"):
    items = "\n".join(
        f"""          <article class="audience">
            <div class="audience__icon">{ICON[icon]}</div>
            <h3>{name}</h3>
            <p>{text}</p>
          </article>""" for icon, name, text in AUDIENCES)
    return f"""    <section class="{cls}" id="pour-qui">
      <div class="container">
        <div class="section__head" data-reveal>
          <p class="eyebrow">Pour qui ?</p>
          <h2>Nous accompagnons</h2>
          <p>Particuliers, entreprises et institutions : chaque projet est conçu pour celles et ceux qui le vivent.</p>
        </div>
        <div class="audiences" data-stagger>
{items}
        </div>
      </div>
    </section>
"""


# ===================== DONNÉES STRUCTURÉES =====================
SERVICE_NAMES = ["Event planning", "Wedding planning", "Chef exécutif événementiel", "Chef privé", "Cocktails et mignardises"]

BUSINESS = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": f"{SITE_URL}/#entreprise",
    "name": SITE_NAME,
    "slogan": "Créer. Recevoir. Célébrer.",
    "description": "Structure événementielle à Abidjan : event planner, wedding planner, chef exécutif événementiel, chef privé, cocktails et mignardises.",
    "url": f"{SITE_URL}/",
    "logo": f"{SITE_URL}/images/logo.jpg",
    "image": f"{SITE_URL}/images/og-image.jpg",
    "telephone": TEL,
    "address": {"@type": "PostalAddress", "addressLocality": "Abidjan", "addressCountry": "CI"},
    "areaServed": {"@type": "Country", "name": "Côte d'Ivoire"},
    "sameAs": [IG],
    "founder": {"@type": "Person", "name": "Earland"},
    "knowsAbout": ["Organisation d'événements", "Organisation de mariages", "Traiteur événementiel", "Chef à domicile", "Cocktails", "Mignardises"],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Expertises",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name}} for name in SERVICE_NAMES
        ],
    },
}

WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": SITE_NAME,
    "url": f"{SITE_URL}/",
    "inLanguage": "fr",
    "publisher": {"@id": f"{SITE_URL}/#entreprise"},
}

# ===================== ACCUEIL =====================
expertise_cards = "\n".join(
    f"""          <article class="expertise-card">
            <span class="expertise-card__num">{num}</span>
            <h3>{name}</h3>
            <strong>{tagline}</strong>
            <p>{text}</p>
            <a href="expertises.html#{slug}" class="link">Découvrir →</a>
          </article>""" for slug, num, name, tagline, text in EXPERTISES)

home = f"""    <section class="hero">
      <div class="hero__bg" aria-hidden="true"><img src="images/galerie/buffet-plats.jpg" alt="" fetchpriority="high"></div>
      <div class="hero__content">
        <p class="script">Créer. Recevoir. Célébrer.</p>
        <h1>Les Ateliers de Earland</h1>
        <p class="hero__tagline">L'art de créer des moments qui restent.</p>
        <p class="hero__lead">De l'organisation d'un événement à la création de son expérience gastronomique, Les Ateliers de Earland imaginent, coordonnent et donnent vie à des événements qui vous ressemblent, à Abidjan et partout en Côte d'Ivoire.</p>
        <div class="hero__actions">
          <a href="#univers" class="btn btn--ghost">Découvrir notre univers</a>
          <a href="contact.html" class="btn">Parlons de votre projet</a>
        </div>
        <ul class="hero__expertises">
          <li>Event Planner</li>
          <li>Wedding Planner</li>
          <li>Chef Exécutif Événementiel</li>
          <li>Chef Privé</li>
          <li>Cocktails &amp; Mignardises</li>
        </ul>
      </div>
    </section>

    <section class="section" id="univers">
      <div class="container split">
        <div class="split__media split__media--frame" data-reveal-media>
          <img src="images/galerie/equipe-bar-mobile.jpg" alt="L'équipe des Ateliers de Earland lors d'un événement" loading="lazy">
        </div>
        <div class="split__text" data-stagger>
          <p class="eyebrow">Notre univers</p>
          <h2>Un événement, c'est une histoire que l'on partage</h2>
          <p class="lead">Un événement ne se résume pas à une belle décoration ou à un bon repas. C'est une atmosphère, une attention, une émotion et une histoire que l'on raconte et que l'on partage.</p>
          <p>Les Ateliers de Earland sont nés de cette conviction. La marque accompagne particuliers, entreprises et institutions dans la conception, l'organisation et la réalisation de leurs événements, en associant coordination, créativité, gastronomie et art de recevoir.</p>
          <a href="a-propos.html" class="link">Découvrir Earland →</a>
        </div>
      </div>
    </section>

    <section class="section section--cream" id="savoir-faire">
      <div class="container">
        <div class="section__head" data-reveal>
          <p class="eyebrow">Nos savoir-faire</p>
          <h2>Organisation, gastronomie et art de recevoir</h2>
          <p>Organisation d'événements, wedding planning, traiteur événementiel, chef à domicile, cocktails et mignardises : cinq expertises réunies sous une même signature, à Abidjan et partout en Côte d'Ivoire.</p>
        </div>
        <div class="expertises" data-stagger>
{expertise_cards}
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container">
        <div class="section__head" data-reveal>
          <p class="eyebrow">L'expérience Earland</p>
          <h2>Quatre engagements, à chaque événement</h2>
        </div>
{values_html()}
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head" data-reveal>
          <p class="eyebrow">Réalisations</p>
          <h2>Chaque événement est une preuve</h2>
          <p>Mariages, réceptions, soirées cocktails : découvrez les événements que nous avons imaginés et orchestrés.</p>
        </div>
        <div class="showcase" data-stagger>
          <a href="realisations.html" class="showcase__item"><img src="images/galerie/equipe-service.jpg" alt="L'équipe de service lors d'une réception" loading="lazy"><span>Réceptions</span></a>
          <a href="realisations.html" class="showcase__item"><img src="images/galerie/mojito.jpg" alt="Mojito signature" loading="lazy"><span>Cocktails</span></a>
          <a href="realisations.html" class="showcase__item"><img src="images/galerie/buffet-salades.jpg" alt="Buffet événementiel" loading="lazy"><span>Gastronomie</span></a>
        </div>
        <p class="center" data-reveal><a href="realisations.html" class="btn btn--dark">Voir nos réalisations</a></p>
      </div>
    </section>

{audiences_section()}
{CTA_BAND}"""

page("index.html",
     "Les Ateliers de Earland | Event & wedding planner à Abidjan",
     "Organisation d'événements et de mariages, traiteur événementiel, chef privé, cocktails et mignardises à Abidjan et en Côte d'Ivoire. Demandez un devis.",
     home, schemas=[BUSINESS, WEBSITE])

# ===================== À PROPOS =====================
about = page_hero("À propos", "Earland, l'art de recevoir",
                  "Une vision de l'événement où l'organisation, la gastronomie et l'attention portée à chaque invité ne font qu'un.",
                  "equipe-service.jpg") + f"""
    <section class="section">
      <div class="container split">
        <div class="split__media" data-reveal-media>
          <!-- Remplacer par une photo d'Earland : <img src="images/earland.jpg" alt="Earland"> -->
          <div class="placeholder"><span class="script">Earland</span>Photo à venir</div>
        </div>
        <div class="split__text" data-stagger>
          <p class="eyebrow">À propos d'Earland</p>
          <h2>Faire de chaque événement une expérience à vivre</h2>
          <p class="lead">Passionné par l'univers de l'événementiel, de la gastronomie et de l'expérience client, Earland accompagne particuliers, entreprises et institutions dans la création de moments pensés dans les moindres détails.</p>
          <p>De la coordination d'un mariage à la création d'un cocktail, de la conception d'un événement à l'élaboration d'une expérience gastronomique, son approche repose sur une même ambition : faire de chaque événement une expérience à vivre, à partager et à retenir.</p>
          <p>Les Ateliers de Earland sont le prolongement de cette vision.</p>
        </div>
      </div>
    </section>

    <section class="section section--cream">
      <div class="container">
        <div class="section__head" data-reveal>
          <p class="eyebrow">L'expérience Earland</p>
          <h2>Ce qui guide chacun de nos projets</h2>
          <p>Concevoir, coordonner et donner vie à des expériences événementielles sur mesure.</p>
        </div>
{values_html()}
      </div>
    </section>

    <section class="section">
      <div class="container split split--reverse">
        <div class="split__media split__media--frame" data-reveal-media>
          <img src="images/galerie/equipe-bar-mobile.jpg" alt="L'équipe des Ateliers de Earland" loading="lazy">
        </div>
        <div class="split__text" data-stagger>
          <p class="eyebrow">Les Ateliers</p>
          <h2>Une équipe au service de vos invités</h2>
          <p>Autour d'Earland, Les Ateliers réunissent les compétences nécessaires à un événement réussi : coordination, cuisine, service et bar. Une seule équipe, un seul interlocuteur, du premier rendez-vous jusqu'au dernier invité.</p>
          <p class="todo">Texte provisoire : présentation de l'équipe à compléter (nombre de personnes, métiers, années d'expérience, chiffres clés).</p>
          <a href="expertises.html" class="link">Découvrir nos expertises →</a>
        </div>
      </div>
    </section>

{CTA_BAND}"""

page("a-propos.html", "À propos d'Earland | Les Ateliers de Earland, Abidjan",
     "Découvrez Earland et Les Ateliers de Earland, structure événementielle à Abidjan qui réunit organisation, gastronomie et art de recevoir.",
     about, schemas=[breadcrumb("a-propos.html", "À propos")])

# ===================== EXPERTISES =====================
DETAILS = {
    "event-planner": (["Conception événementielle", "Organisation", "Coordination", "Gestion des prestataires", "Planning et rétroplanning", "Logistique", "Coordination jour J"],
                      "Event planner à Abidjan, nous organisons vos événements privés et professionnels partout en Côte d'Ivoire : du lancement de produit à la soirée d'anniversaire, votre idée devient un événement maîtrisé de bout en bout.",
                      '<img src="images/galerie/equipe-service.jpg" alt="Équipe de service en place pour un événement" loading="lazy">'),
    "wedding-planner": (["Organisation complète", "Coordination jour J", "Direction de cérémonie", "Gestion des prestataires", "Concept et timeline", "Comité d'organisation", "Expérience invités"],
                        "Votre mariage raconte votre histoire. Wedding planner à Abidjan, nous l'imaginons avec vous, puis nous orchestrons chaque instant pour que vous viviez pleinement votre journée.",
                        '<div class="placeholder placeholder--emerald"><span class="script">Mariages</span>Photo à venir</div>'),
    "chef-executif": (["Cocktails et mignardises", "Buffets", "Menus événementiels", "Brunchs", "Cuisine africaine contemporaine", "Cuisine sur mesure", "Scénographie culinaire"],
                      "Traiteur événementiel à Abidjan, nous créons une cuisine pensée pour votre événement : le menu, la présentation et le service s'accordent à votre thème et à vos invités.",
                      '<img src="images/galerie/buffet-plats.jpg" alt="Buffet de plats chauds" loading="lazy">'),
    "chef-prive": (["Dîner privé", "Réception à domicile", "Menu personnalisé", "Expérience gastronomique"],
                   "Chef à domicile à Abidjan : le chef vient chez vous avec un menu composé pour vous, préparé et servi dans l'intimité de votre maison.",
                   '<img src="images/galerie/assiette-salade.jpg" alt="Assiette servie lors d\'une réception" loading="lazy">'),
    "cocktails-mignardises": (["Cocktails signature", "Mocktails", "Mignardises", "Bar à cocktails mobile", "Créations personnalisées"],
                              "Une offre transversale qui accompagne tous nos événements, ou se réserve seule pour vos réceptions.",
                              '<img src="images/galerie/mojito.jpg" alt="Mojito signature" loading="lazy">'),
}

detail_blocks = []
for i, (slug, num, name, tagline, _) in enumerate(EXPERTISES):
    items, text, media = DETAILS[slug]
    lis = "".join(f"<li>{it}</li>" for it in items)
    reverse = " split--reverse" if i % 2 else ""
    detail_blocks.append(f"""        <article class="expertise-detail split{reverse}" id="{slug}">
          <div class="split__media" data-reveal-media>
            {media}
          </div>
          <div class="split__text" data-stagger>
            <span class="expertise-detail__num">{num}</span>
            <h2>{name}</h2>
            <p class="tagline">{tagline}</p>
            <p>{text}</p>
            <ul class="checklist">{lis}</ul>
            <a href="contact.html" class="btn btn--dark">Parlons de votre projet</a>
          </div>
        </article>""")

SERVICES_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Expertises des Ateliers de Earland",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "Service",
                "name": htmllib.unescape(name),
                "description": htmllib.unescape(DETAILS[slug][1]),
                "url": f"{SITE_URL}/expertises.html#{slug}",
                "areaServed": {"@type": "Country", "name": "Côte d'Ivoire"},
                "provider": {"@id": f"{SITE_URL}/#entreprise"},
            },
        }
        for i, (slug, _, name, _, _) in enumerate(EXPERTISES, 1)
    ],
}

FAQ = [
    ("Dans quelles villes intervenez-vous ?",
     "Nous sommes basés à Abidjan et nous intervenons partout en Côte d'Ivoire, pour les mariages, les événements d'entreprise, les réceptions privées et les dîners à domicile."),
    ("Proposez-vous un menu fixe ?",
     "Non. Chaque menu est composé sur mesure selon votre événement, vos goûts, votre budget et votre nombre d'invités : cuisine africaine contemporaine, buffets, menus servis, brunchs, cocktails et mignardises."),
    ("Peut-on réserver seulement le bar à cocktails ou le chef privé ?",
     "Oui. Chaque expertise peut être réservée seule ou combinée aux autres : event planning, wedding planning, chef exécutif événementiel, chef privé, cocktails et mignardises."),
    ("Combien de temps à l'avance faut-il vous contacter ?",
     "Le plus tôt possible, surtout pour un mariage ou un grand événement : cela laisse le temps de construire le concept, le rétroplanning et de réserver les prestataires. Pour un dîner privé, quelques jours peuvent suffire selon nos disponibilités."),
    ("Comment obtenir un devis ?",
     "Remplissez le formulaire de la page Contact ou écrivez-nous sur WhatsApp au +225 07 59 47 15 17. Nous revenons vers vous avec une proposition personnalisée."),
]

FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ
    ],
}

faq_items = "\n".join(
    f"""          <details class="faq__item">
            <summary>{q}</summary>
            <p>{a}</p>
          </details>""" for q, a in FAQ)

anchors = "\n".join(f'          <a href="#{slug}">{name}</a>' for slug, _, name, _, _ in EXPERTISES)

COCKTAILS = [
    ("Mojito", "Citron vert, menthe fraîche, sucre de canne. Le classique rafraîchissant."),
    ("Piña Colada", "Ananas et noix de coco, onctueux et ensoleillé."),
    ("Tropical", "Un mélange de fruits exotiques, pour une note festive et colorée."),
    ("Bora Bora", "Ananas, fruit de la passion et grenadine, en version mocktail."),
]
cocktail_cards = "\n".join(
    f"""          <article class="cocktail">
            {ICON['glass']}
            <h3>{name}</h3>
            <p>{text}</p>
          </article>""" for name, text in COCKTAILS)

expertises = page_hero("Expertises", "Nos savoir-faire",
                       "Event planning, wedding planning, gastronomie événementielle, chef privé, cocktails et mignardises : une même exigence, du concept au dernier invité.",
                       "equipe-bar-mobile.jpg") + f"""
    <section class="section section--white section--tight">
      <div class="container">
        <nav class="anchors" aria-label="Expertises" data-reveal>
{anchors}
        </nav>
      </div>
    </section>

    <section class="section">
      <div class="container">
{chr(10).join(detail_blocks)}
      </div>
    </section>

    <section class="section section--dark" id="carte-cocktails">
      <div class="container">
        <div class="section__head" data-reveal>
          <p class="eyebrow">Cocktails &amp; mignardises</p>
          <h2>Des créations signature, une carte à votre image</h2>
          <p>Nous concevons une carte adaptée au thème, aux couleurs, à l'histoire du couple, à l'entreprise, à la saison ou au type d'événement, accompagnée de mignardises sucrées et salées.</p>
        </div>
        <div class="cocktails" data-stagger>
{cocktail_cards}
          <article class="cocktail cocktail--custom">
            {ICON['glass']}
            <h3>Votre création</h3>
            <p>Un cocktail personnalisé, imaginé pour votre événement et baptisé à votre nom.</p>
          </article>
        </div>
      </div>
    </section>

{audiences_section()}
    <section class="section" id="faq">
      <div class="container faq">
        <div class="section__head" data-reveal>
          <p class="eyebrow">Questions fréquentes</p>
          <h2>Vos questions, nos réponses</h2>
        </div>
        <div class="faq__list" data-stagger>
{faq_items}
        </div>
      </div>
    </section>

{CTA_BAND}"""

page("expertises.html", "Wedding planner, event planner et chef privé à Abidjan",
     "Wedding planner, event planner, traiteur événementiel, chef à domicile, cocktails et mignardises à Abidjan : découvrez nos savoir-faire et nos prestations.",
     expertises, schemas=[breadcrumb("expertises.html", "Expertises"), SERVICES_SCHEMA, FAQ_SCHEMA])

# ===================== RÉALISATIONS =====================
TODO = '<span class="todo">À compléter</span>'
PROJECTS = [
    ("mariages", ["Mariage"], "Émeraude &amp; Éternité",
     '<div class="placeholder placeholder--emerald"><span class="script">Émeraude &amp; Éternité</span>Photos à venir</div>'),
    ("mariages", ["Mariage"], "Dieu peut organiser ton mariage",
     '<div class="placeholder"><span class="script">Mariage</span>Photos à venir</div>'),
    ("cocktails evenements", ["Cocktails", "Événement"], "Bar à cocktails mobile",
     '<img src="images/galerie/equipe-bar-mobile.jpg" alt="L\'équipe derrière le bar à cocktails mobile" loading="lazy">'),
    ("cocktails evenements", ["Cocktails", "Soirée"], "Soirée cocktails",
     '<img src="images/galerie/bar-cocktails-invites.jpg" alt="Invités servis au bar à cocktails" loading="lazy">'),
    ("gastronomie", ["Gastronomie"], "Buffet événementiel",
     '<img src="images/galerie/buffet-plats.jpg" alt="Buffet de plats chauds" loading="lazy">'),
    ("evenements gastronomie", ["Événement", "Gastronomie"], "Réception &amp; service",
     '<img src="images/galerie/equipe-service.jpg" alt="L\'équipe de service en tenue" loading="lazy">'),
]
project_cards = "\n".join(
    f"""          <article class="project" data-cat="{cats}">
            <div class="project__media">{media}</div>
            <div class="project__body">
              <div class="project__tags">{''.join(f'<span>{t}</span>' for t in tags)}</div>
              <h3>{title}</h3>
              <dl class="project__meta">
                <dt>Lieu</dt><dd>{TODO}</dd>
                <dt>Date</dt><dd>{TODO}</dd>
                <dt>Invités</dt><dd>{TODO}</dd>
                <dt>Prestations</dt><dd>{TODO}</dd>
              </dl>
              <details>
                <summary>Concept, rôle et résultat</summary>
                <p><strong>Concept :</strong> {TODO}</p>
                <p><strong>Rôle des Ateliers :</strong> {TODO}</p>
                <p><strong>Résultat :</strong> {TODO}</p>
              </details>
            </div>
          </article>""" for cats, tags, title, media in PROJECTS)

GALLERY = [
    ("mojito.jpg", "Mojito maison au citron vert et à la menthe", "tall"),
    ("buffet-salades.jpg", "Service d'un buffet de salades fraîches", ""),
    ("buffet-plats.jpg", "Buffet de plats chauds : riz et viandes rôties", ""),
    ("equipe-bar-mobile.jpg", "L'équipe des Ateliers de Earland derrière le bar à cocktails mobile", "wide"),
    ("bar-cocktails-invites.jpg", "Invités servis au bar à cocktails lors d'une soirée", "tall"),
    ("assiette-salade.jpg", "Assiette servie lors d'un buffet", ""),
    ("equipe-service.jpg", "L'équipe de service en tenue, prête pour un grand événement", "wide"),
    ("bar-cocktails-service.jpg", "Cocktail servi à un invité au bar mobile", ""),
]
gallery_items = "\n".join(
    f"""          <button class="gallery__item{' gallery__item--' + size if size else ''}" type="button">
            <img src="images/galerie/{img}" alt="{alt}" loading="lazy">
            <span>{alt}</span>
          </button>""" for img, alt, size in GALLERY)

LIGHTBOX = """
  <div class="lightbox" id="lightbox" hidden>
    <button class="lightbox__close" type="button" aria-label="Fermer">×</button>
    <button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="Photo précédente">‹</button>
    <figure>
      <img alt="">
      <figcaption></figcaption>
    </figure>
    <button class="lightbox__nav lightbox__nav--next" type="button" aria-label="Photo suivante">›</button>
  </div>
"""

realisations = page_hero("Réalisations", "Nos événements, nos preuves",
                         "Chaque événement réalisé raconte une histoire et témoigne de notre savoir-faire : concept, coordination, gastronomie et expérience invités.",
                         "bar-cocktails-invites.jpg") + f"""
    <section class="section">
      <div class="container">
        <div class="filters" role="group" aria-label="Filtrer les réalisations" data-reveal>
          <button class="filter is-active" type="button" data-filter="all" aria-pressed="true">Tout</button>
          <button class="filter" type="button" data-filter="mariages" aria-pressed="false">Mariages</button>
          <button class="filter" type="button" data-filter="evenements" aria-pressed="false">Événements</button>
          <button class="filter" type="button" data-filter="gastronomie" aria-pressed="false">Gastronomie</button>
          <button class="filter" type="button" data-filter="cocktails" aria-pressed="false">Cocktails</button>
        </div>
        <div class="projects" id="projects">
{project_cards}
        </div>
      </div>
    </section>

    <section class="section section--cream">
      <div class="container">
        <div class="section__head" data-reveal>
          <p class="eyebrow">En images</p>
          <h2>Dans les coulisses des Ateliers</h2>
        </div>
        <div class="gallery" id="gallery" data-stagger>
{gallery_items}
        </div>
        <p class="center" style="margin-top:2.5rem" data-reveal><a href="{IG}" class="btn btn--dark" target="_blank" rel="noopener">Suivre sur Instagram</a></p>
      </div>
    </section>

{CTA_BAND}"""

page("realisations.html", "Nos réalisations : mariages et événements à Abidjan",
     "Mariages, réceptions, soirées cocktails et buffets événementiels : découvrez les réalisations des Ateliers de Earland à Abidjan et en Côte d'Ivoire.",
     realisations, LIGHTBOX, schemas=[breadcrumb("realisations.html", "Réalisations")])

# ===================== JOURNAL =====================
ARTICLES = [
    ("buffet-salades.jpg", "Conseils mariage", "Le rétroplanning idéal pour préparer son mariage",
     "Les grandes étapes, mois par mois, pour aborder votre jour J l'esprit serein."),
    ("mojito.jpg", "Cocktails", "Composer une carte de cocktails à l'image de son événement",
     "Couleurs, thème, saison : comment créer des cocktails signature qui racontent votre histoire."),
    ("assiette-salade.jpg", "Chef privé", "Recevoir chez soi comme au restaurant",
     "Tout ce qu'il faut savoir pour organiser un dîner privé avec un chef à domicile."),
]
article_cards = "\n".join(
    f"""          <article class="article">
            <div class="article__media"><img src="images/galerie/{img}" alt="" loading="lazy"><span class="badge">Bientôt</span></div>
            <div class="article__body">
              <span class="article__cat">{cat}</span>
              <h3>{title}</h3>
              <p>{text}</p>
            </div>
          </article>""" for img, cat, title, text in ARTICLES)

journal = page_hero("Journal &amp; podcast", "Le Journal des Ateliers",
                    "Articles, conseils et coulisses : nos idées pour imaginer, organiser et réussir vos événements.",
                    "buffet-salades.jpg") + f"""
    <section class="section">
      <div class="container">
        <div class="section__head" data-reveal>
          <p class="eyebrow">Articles &amp; conseils</p>
          <h2>Les premiers articles arrivent</h2>
          <p>Voici un aperçu des sujets que nous préparons.</p>
        </div>
        <div class="articles" data-stagger>
{article_cards}
        </div>
      </div>
    </section>

    <section class="section section--dark" id="podcast">
      <div class="container podcast">
        <div class="podcast__visual" data-reveal-media>{ICON['mic']}</div>
        <div data-stagger>
          <p class="eyebrow">Podcast</p>
          <h2>Les Conversations des Ateliers</h2>
          <p>Un podcast pour rencontrer celles et ceux qui font l'événementiel et l'art de recevoir. Chaque épisode accueillera un professionnel pour parler de son métier, de son parcours et de sa vision.</p>
          <ul class="chips">
            <li>Événementiel</li><li>Gastronomie</li><li>Décoration</li><li>Photographie</li><li>Communication</li><li>Entrepreneuriat créatif</li>
          </ul>
          <p class="script">Premier épisode bientôt</p>
          <p style="margin-top:1.5rem"><a href="{IG}" class="btn btn--ghost" target="_blank" rel="noopener">Suivre sur Instagram</a></p>
        </div>
      </div>
    </section>

{CTA_BAND}"""

page("journal.html", "Journal et podcast de l'événementiel | Ateliers de Earland",
     "Conseils pour organiser son mariage ou son événement, cocktails, chef privé et podcast Les Conversations des Ateliers : le journal des Ateliers de Earland.",
     journal, schemas=[breadcrumb("journal.html", "Journal")])

# ===================== CONTACT =====================
SERVICES = ["Event planning", "Wedding planning", "Chef exécutif événementiel", "Chef privé", "Cocktails &amp; mignardises"]
checks = "\n".join(
    f'              <label class="check"><input type="checkbox" name="services" value="{s.replace("&amp;", "&")}"> {s}</label>'
    for s in SERVICES)

contact = page_hero("Contact &amp; devis", "Parlons de votre projet",
                    "Racontez-nous votre événement : nous revenons vers vous rapidement avec une proposition sur mesure.",
                    "equipe-service.jpg") + f"""
    <section class="section">
      <div class="container quote">
        <div class="quote__info" data-stagger>
          <p class="eyebrow">Demander un devis</p>
          <h2>Chaque projet commence par une conversation</h2>
          <p>Mariage, événement d'entreprise, dîner privé ou célébration : plus vous nous en dites, plus notre proposition sera juste.</p>
          <ul class="contact-list">
            <li>{ICON['phone']}<a href="tel:{TEL}">{TEL_TXT}</a></li>
            <li>{ICON['chat']}<a href="{WA}" target="_blank" rel="noopener">Échanger sur WhatsApp</a></li>
            <li>{ICON['insta']}<a href="{IG}" target="_blank" rel="noopener">@les_ateliers_de_earland_</a></li>
            <li>{ICON['pin']}<span>Abidjan et partout en Côte d'Ivoire</span></li>
          </ul>
          <p class="quote__note">En cliquant sur « Envoyer ma demande », votre message s'ouvre dans WhatsApp, déjà rempli. Il ne vous reste qu'à l'envoyer.</p>
        </div>

        <form class="quote__form" id="quoteForm" novalidate data-reveal>
          <div class="field">
            <label for="nom">Nom &amp; prénom *</label>
            <input type="text" id="nom" name="nom" required autocomplete="name">
          </div>
          <div class="field field--half">
            <label for="tel">Téléphone / WhatsApp *</label>
            <input type="tel" id="tel" name="tel" required autocomplete="tel" placeholder="+225 07 00 00 00 00">
          </div>
          <div class="field field--half">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" autocomplete="email" placeholder="nom@exemple.com">
          </div>
          <div class="field">
            <label for="evenement">Type d'événement *</label>
            <select id="evenement" name="evenement" required>
              <option value="">Choisir…</option>
              <option>Mariage</option>
              <option>Anniversaire</option>
              <option>Baptême</option>
              <option>Dîner privé</option>
              <option>Événement d'entreprise</option>
              <option>Lancement</option>
              <option>Soirée</option>
              <option>Autre</option>
            </select>
          </div>
          <div class="field field--half">
            <label for="date">Date</label>
            <input type="date" id="date" name="date">
          </div>
          <div class="field field--half">
            <label for="invites">Nombre d'invités</label>
            <input type="number" id="invites" name="invites" min="1" placeholder="150">
          </div>
          <div class="field">
            <label for="lieu">Lieu</label>
            <input type="text" id="lieu" name="lieu" placeholder="Cocody, Abidjan">
          </div>
          <fieldset class="field">
            <legend>Services souhaités</legend>
            <div class="checks">
{checks}
            </div>
          </fieldset>
          <div class="field">
            <label for="message">Description du projet</label>
            <textarea id="message" name="message" rows="5" placeholder="Votre histoire, vos envies, votre thème, votre budget…"></textarea>
          </div>
          <p class="form-error" id="formError" role="alert" hidden>Merci de remplir les champs obligatoires (*).</p>
          <button type="submit" class="btn btn--full">Envoyer ma demande</button>
        </form>
      </div>
    </section>
"""

page("contact.html", "Devis mariage et événement à Abidjan | Ateliers de Earland",
     "Demandez un devis pour votre mariage, événement d'entreprise, dîner privé ou réception à Abidjan. Réponse rapide par WhatsApp au +225 07 59 47 15 17.",
     contact, schemas=[breadcrumb("contact.html", "Contact"), BUSINESS])

# ===================== PAGE 404 =====================
not_found = """    <section class="page-hero" style="min-height:60vh;display:flex;align-items:center">
      <div class="container">
        <p class="eyebrow">Erreur 404</p>
        <h1>Cette page n'existe pas</h1>
        <p>Elle a peut-être été déplacée. Revenez à l'accueil ou parlez-nous directement de votre projet.</p>
        <p style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap"><a href="index.html" class="btn">Retour à l'accueil</a> <a href="contact.html" class="btn btn--ghost">Parlons de votre projet</a></p>
      </div>
    </section>
"""
page("404.html", "Page introuvable | Les Ateliers de Earland", "Cette page n'existe pas ou a été déplacée.", not_found, indexable=False)

# ===================== FICHIERS POUR LES MOTEURS DE RECHERCHE =====================
PRIORITY = {"index.html": "1.0", "expertises.html": "0.9", "contact.html": "0.9", "realisations.html": "0.8", "a-propos.html": "0.7", "journal.html": "0.6"}
urls = "\n".join(
    f"""  <url>
    <loc>{url_for(f)}</loc>
    <lastmod>{TODAY}</lastmod>
    <priority>{PRIORITY.get(f, "0.5")}</priority>
  </url>""" for f in PAGES)
with open(f"{OUT}/sitemap.xml", "w") as f:
    f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")

with open(f"{OUT}/robots.txt", "w") as f:
    f.write(f"""User-agent: *
Allow: /
Disallow: /tools/

Sitemap: {SITE_URL}/sitemap.xml
""")

with open(f"{OUT}/site.webmanifest", "w") as f:
    json.dump({
        "name": SITE_NAME,
        "short_name": "Ateliers Earland",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#faf6ef",
        "theme_color": "#141110",
        "icons": [
            {"src": "images/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "images/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, f, ensure_ascii=False, indent=2)

print("ok")

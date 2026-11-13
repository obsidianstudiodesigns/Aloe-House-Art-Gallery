"""Writes every page in English (site root) and Afrikaans (af/), plus the sitemap and manifest.
Run: python tools/build.py   Works come from tools/collection.json. Business details are the constants below."""
import json
import re
from html import escape as e
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://obsidianstudiodesigns.github.io/Aloe-House-Art-Gallery/"
NAME = "Aloe House Art Gallery"
PHONE_LOCAL = "083 798 2734"
PHONE_INTL = "+27837982734"
WA = "https://wa.me/27837982734"
FB = "https://www.facebook.com/profile.php?id=61595805510704"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote("De Wagendrift Boerdery, Groblersdal, South Africa")
CREDIT = "https://obsidianstudiodesigns.co.za/"
ISO = "2026-11-13"
GREEN = "#14291c"

WORKS = json.loads((ROOT / "tools/collection.json").read_text(encoding="utf8"))
BY = {w["slug"]: w for w in WORKS}
ARTISTS = {"Lizette Nel": "lizette-nel", "Jeanne H Barnes": "jeanne-h-barnes"}

L = "en"   # language being written
R = ""     # path back to the site root from the page being written


def t(en, af):
    return af if L == "af" else en


def wa(text=None):
    return WA + ("?text=" + quote(text) if text else "")


def icon(name):
    return f'<svg class="icon" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def sprite():
    out = []
    for f in sorted((ROOT / "tools/icons").glob("*.svg")):
        inner = re.search(r"<svg[^>]*>(.*)</svg>", f.read_text(encoding="utf8"), re.S).group(1)
        out.append(f'<symbol id="i-{f.stem}" viewBox="0 0 256 256">{inner.strip()}</symbol>')
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(out) + "</svg>"


SPRITE = sprite()


# Works ----------------------------------------------------------------------------------------
def tx(w, key):
    return w[L][key]


def srcset(w):
    return ", ".join(f'{R}assets/img/works/{w["image"]}-{x}.webp {x}w' for x in w["widths"])


def src(w, i=0):
    return f'{R}assets/img/works/{w["image"]}-{w["widths"][i]}.webp'


def dims(w):
    width = w["widths"][-1]
    return f'width="{width}" height="{round(width / w["ratio"])}"'


def label(w, extra=""):
    year = f', {w["year"]}' if w["year"] else ""
    return (f'<span class="label {extra}"><span class="label__by">{e(w["artist"])}</span>'
            f'<span class="label__title">{e(tx(w, "title"))}{year}</span><span class="label__medium">{e(tx(w, "medium"))}</span></span>')


def framed(w, sizes, loading="lazy"):
    view = t("View", "Bekyk")
    return (f'<button class="frame f-{w["frame"]}" type="button" data-work="{w["slug"]}" aria-label="{view} {e(tx(w, "title"))}, {e(w["artist"])}">'
            f'<img src="{src(w)}" srcset="{srcset(w)}" sizes="{sizes}" alt="{e(tx(w, "alt"))}" {dims(w)} loading="{loading}" decoding="async"></button>')


# Page chrome ----------------------------------------------------------------------------------
def head(path, title, desc, og="home", og_alt=None, extra="", ld=None, robots="index,follow,max-image-preview:large", alternates=True):
    url_en, url_af = BASE + path, BASE + "af/" + path
    url = url_af if L == "af" else url_en
    url = url.replace("index.html", "")
    img = f"{BASE}assets/img/og/{og}{'-af' if L == 'af' else ''}.jpg"
    og_alt = og_alt or t(f"{NAME}: where nature meets art", f"{NAME}: waar natuur en kuns ontmoet")
    alt_links = ""
    if alternates:
        en_u, af_u = url_en.replace("index.html", ""), url_af.replace("index.html", "")
        alt_links = (f'<link rel="alternate" hreflang="en-ZA" href="{en_u}">\n<link rel="alternate" hreflang="af-ZA" href="{af_u}">\n'
                     f'<link rel="alternate" hreflang="x-default" href="{en_u}">\n')
    data = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n' if ld else ""
    locale, other = ("af_ZA", "en_ZA") if L == "af" else ("en_ZA", "af_ZA")
    return f"""<!doctype html>
<html lang="{t('en-ZA', 'af-ZA')}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{alt_links}<meta name="robots" content="{robots}">
<meta name="theme-color" content="{GREEN}">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="{locale}">
<meta property="og:locale:alternate" content="{other}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:secure_url" content="{img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="{R}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{R}favicon-32.png">
<link rel="icon" type="image/png" sizes="96x96" href="{R}favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="{R}icon-192.png">
<link rel="apple-touch-icon" href="{R}apple-touch-icon.png">
<link rel="manifest" href="{R}site.webmanifest">
<link rel="preload" href="{R}assets/fonts/Gloock-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{R}assets/fonts/InstrumentSans-normal.woff2" as="font" type="font/woff2" crossorigin>
{extra}<link rel="stylesheet" href="{R}assets/css/style.css">
{data}</head>
"""


def lang_switch(path):
    """EN / AF switch. Each side links to the same page in that language."""
    if path is None:
        return ""
    en_href = (R if L == "af" else "") + path
    af_href = ("" if L == "af" else "af/") + path
    en_cur = ' aria-current="true"' if L == "en" else ""
    af_cur = ' aria-current="true"' if L == "af" else ""
    return (f'<nav class="lang" aria-label="{t("Language", "Taal")}">'
            f'<a href="{en_href}" hreflang="en" lang="en" title="English" data-lang="en"{en_cur}>EN</a>'
            f'<a href="{af_href}" hreflang="af" lang="af" title="Afrikaans" data-lang="af"{af_cur}>AF</a></nav>')


def header(page, path):
    def link(href, text, key):
        cur = ' aria-current="page"' if key == page else ""
        return f'<a href="{href}"{cur}>{text}</a>'

    def tab(href, text, ic, key):
        cur = ' aria-current="page"' if key == page else ""
        return f'<a class="tab" href="{href}"{cur}>{icon(ic)}{text}</a>'

    return f"""<body data-page="{page}">
{SPRITE}
<a class="skip" href="#main">{t("Skip to content", "Gaan na inhoud")}</a>
<div class="top-sentinel" aria-hidden="true"></div>
<header class="site-head">
  <a class="brand" href="index.html">
    <img src="{R}assets/img/brand/crest.webp" alt="" width="396" height="423">
    <span class="brand__text"><span class="brand__a">Aloe House</span><span class="brand__b">Art Gallery</span></span>
  </a>
  <div class="head-end">
    <nav class="site-nav" aria-label="{t("Main", "Hoof")}">
      {link("collection.html", t("Collection", "Versameling"), "collection")}
      {link("index.html#artists", t("Artists", "Kunstenaars"), "artists")}
      {link("visit.html", t("Visit", "Besoek"), "visit")}
      <a class="btn btn--small" href="{wa()}" target="_blank" rel="noopener">{icon("whatsapp-logo")}{t("WhatsApp us", "WhatsApp ons")}</a>
    </nav>
    {lang_switch(path)}
  </div>
</header>
<nav class="tabbar" aria-label="{t("Quick links", "Vinnige skakels")}">
  {tab("index.html", t("Home", "Tuis"), "house", "home")}
  {tab("collection.html", t("Collection", "Versameling"), "frame-corners", "collection")}
  {tab("index.html#artists", t("Artists", "Kunstenaars"), "paint-brush", "artists")}
  {tab("visit.html", t("Visit", "Besoek"), "map-pin", "visit")}
  <a class="tab tab--wa" href="{wa()}" target="_blank" rel="noopener">{icon("whatsapp-logo")}WhatsApp</a>
</nav>
"""


def footer():
    return f"""<footer class="site-foot">
  <div class="foot-main">
    <img class="foot-logo" src="{R}assets/img/brand/logo-round-320.webp" alt="{t(f"{NAME} logo", f"{NAME}-logo")}" width="320" height="320" loading="lazy">
    <div class="foot-col">
      <h2 class="foot-h">{t("Find us", "Vind ons")}</h2>
      <p>De Wagendrift Boerdery<br>{t("Loskop Valley, Groblersdal", "Loskopvallei, Groblersdal")}<br>{t("South Africa", "Suid-Afrika")}</p>
      <p><a href="{MAPS}" target="_blank" rel="noopener">{t("Open in Google Maps", "Maak oop in Google Maps")}</a></p>
    </div>
    <div class="foot-col">
      <h2 class="foot-h">{t("Talk to us", "Praat met ons")}</h2>
      <p><a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a></p>
      <p><a href="{wa()}" target="_blank" rel="noopener">WhatsApp</a></p>
      <p><a href="{FB}" target="_blank" rel="noopener">Facebook</a></p>
    </div>
    <div class="foot-col">
      <h2 class="foot-h">{t("Explore", "Verken")}</h2>
      <p><a href="collection.html">{t("Collection", "Versameling")}</a></p>
      <p><a href="lizette-nel.html">Lizette Nel</a></p>
      <p><a href="jeanne-h-barnes.html">Jeanne H Barnes</a></p>
      <p><a href="visit.html">{t("Visit", "Besoek")}</a></p>
    </div>
  </div>
  <div class="foot-end">
    <span>&copy; 2026 {NAME}. {t("All rights reserved.", "Alle regte voorbehou.")}</span>
    <span class="foot-legal"><a href="privacy.html">{t("Privacy policy", "Privaatheidsbeleid")}</a><a href="terms.html">{t("Terms of use", "Gebruiksvoorwaardes")}</a></span>
    <span class="credit">{t("Designed by", "Ontwerp deur")} <a href="{CREDIT}" target="_blank" rel="noopener">Obsidian Studio Designs</a></span>
  </div>
</footer>
"""


def room():
    return f"""<dialog class="room" id="room" aria-label="{t("Viewing room", "Bekykkamer")}">
  <div class="room__bar">
    <div class="room__walls" role="group" aria-label="{t("Wall colour", "Muurkleur")}">
      <span class="room__walls-label">{t("Wall", "Muur")}</span>
      <button type="button" class="swatch swatch--green" data-wall="green" aria-pressed="true"><span>{t("Aloe green", "Aalwyngroen")}</span></button>
      <button type="button" class="swatch swatch--lime" data-wall="lime" aria-pressed="false"><span>{t("Limewash", "Kalkwit")}</span></button>
      <button type="button" class="swatch swatch--clay" data-wall="clay" aria-pressed="false"><span>{t("Clay", "Klei")}</span></button>
    </div>
    <div class="room__nav">
      <button type="button" class="room__btn" data-prev aria-label="{t("Previous work", "Vorige werk")}">{icon("arrow-left")}</button>
      <button type="button" class="room__btn" data-next aria-label="{t("Next work", "Volgende werk")}">{icon("arrow-right")}</button>
      <button type="button" class="room__btn" data-close aria-label="{t("Close viewing room", "Maak bekykkamer toe")}" autofocus>{icon("x")}</button>
    </div>
  </div>
  <div class="room__body">
    <div class="room__art"><span class="frame" id="room-frame"><img id="room-img" alt=""></span></div>
    <aside class="room__label" id="room-label" aria-live="polite"></aside>
  </div>
</dialog>
"""


def scripts(with_room=True):
    data = ""
    if with_room:
        pub = [{"slug": w["slug"], "artist": w["artist"], "year": w["year"], "frame": w["frame"], "ratio": w["ratio"],
                "title": tx(w, "title"), "medium": tx(w, "medium"), "alt": tx(w, "alt"), "src": src(w, -1), "srcset": srcset(w)} for w in WORKS]
        strings = {
            "wa": WA,
            "note": t("Price on request. Ask us about availability, or arrange to see it in person.",
                      "Prys op aanvraag. Vra ons oor beskikbaarheid, of reël om dit self te kom sien."),
            "enquire": t("Enquire about this work", "Navrae oor hierdie werk"),
            "msg": t('Hello Aloe House, I would like to know more about "{title}" by {artist}.',
                     'Hallo Aloe House, ek wil graag meer weet oor "{title}" deur {artist}.'),
        }
        data = (room() + f'<script type="application/json" id="works">{json.dumps(pub, ensure_ascii=False)}</script>\n'
                f'<script>window.AH={json.dumps(strings, ensure_ascii=False)}</script>\n')
    else:
        data = f'<script>window.AH={json.dumps({"wa": WA}, ensure_ascii=False)}</script>\n'
    return data + f'<script src="{R}assets/js/main.js" defer></script>\n</body>\n</html>\n'


def gallery_ld():
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ArtGallery",
                "@id": BASE + "#gallery",
                "name": NAME,
                "url": BASE,
                "slogan": "Where nature meets art",
                "description": t("Original art and local talent in the heart of the Loskop Valley, at De Wagendrift Boerdery near Groblersdal.",
                                 "Oorspronklike kuns en plaaslike talent in die hartjie van die Loskopvallei, by De Wagendrift Boerdery naby Groblersdal."),
                "logo": BASE + "assets/img/brand/logo-round.png",
                "image": [BASE + "assets/img/photos/gallery-building-1448.webp", BASE + "assets/img/og/home.jpg"],
                "telephone": PHONE_INTL,
                "address": {"@type": "PostalAddress", "streetAddress": "De Wagendrift Boerdery", "addressLocality": "Groblersdal", "addressCountry": "ZA"},
                "areaServed": "Loskop Valley",
                "knowsLanguage": ["en", "af"],
                "sameAs": [FB],
            },
            {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": NAME, "inLanguage": ["en-ZA", "af-ZA"], "publisher": {"@id": BASE + "#gallery"}},
        ],
    }


# Pages ----------------------------------------------------------------------------------------
def page_home(path):
    p = BY["lizette-portrait"]
    preload = (
        f'<link rel="preload" as="image" href="{src(p, 1)}" imagesrcset="{srcset(p)}" imagesizes="(max-width: 1023px) 66vw, 30vw" fetchpriority="high">\n'
        f'<link rel="preload" as="image" href="{R}assets/img/photos/wall-wide.webp" media="(min-width: 1024px)">\n'
        f'<link rel="preload" as="image" href="{R}assets/img/photos/wall-tall.webp" media="(max-width: 1023px)">\n'
    )
    h = head(path,
             t(f"{NAME} | Original Art in the Loskop Valley, Groblersdal", f"{NAME} | Oorspronklike kuns in die Loskopvallei, Groblersdal"),
             t("Original art by Lizette Nel and Jeanne H Barnes at De Wagendrift Boerdery in the Loskop Valley near Groblersdal. Where nature meets art. Opening soon.",
               "Oorspronklike kuns deur Lizette Nel en Jeanne H Barnes by De Wagendrift Boerdery in die Loskopvallei naby Groblersdal. Waar natuur en kuns ontmoet. Binnekort oop."),
             extra=preload, ld=gallery_ld())
    hang = ""
    for w in (w for w in WORKS if w.get("wall")):
        v = w["wall"]
        hang += (f'<figure class="hang" style="--h:{v["h"]};--y:{v["y"]};--ar:{w["ratio"]}">'
                 + framed(w, f'(max-width: 1023px) 78vw, {round(v["h"] * w["ratio"] * 1.1)}vh')
                 + f"<figcaption>{label(w)}</figcaption></figure>\n")
    statement_sub = t('<p class="statement__en">Art that stops you. Art that tells stories. Art that touches your heart.</p>',
                      '<p class="statement__en">Twee kunstenaars. Twee unieke style. Een besondere plek waar kreatiwiteit en die natuur ontmoet.</p>')
    bb, goat = BY["jeanne-bushbabies"], BY["lizette-goat"]
    return h + header("home", path) + f"""<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <picture class="stage">
    <source media="(max-width: 1023px)" srcset="{R}assets/img/photos/wall-tall.webp" width="864" height="1536">
    <img src="{R}assets/img/photos/wall-wide.webp" alt="" width="1536" height="864" fetchpriority="high">
  </picture>
  <div class="hero__dim" aria-hidden="true"></div>
  <figure class="hero-art">
    <button class="frame f-gilt" type="button" data-work="{p["slug"]}" aria-label="{t("View", "Bekyk")} {e(tx(p, "title"))}, {e(p["artist"])}">
      <img src="{src(p, 1)}" srcset="{srcset(p)}" sizes="(max-width: 1023px) 66vw, 30vw" alt="{e(tx(p, "alt"))}" {dims(p)} fetchpriority="high">
      <span class="sunfall" aria-hidden="true"></span>
    </button>
    <figcaption>{label(p)}</figcaption>
  </figure>
  <div class="hero__copy">
    <p class="hero__kicker">{t("Opening soon at De Wagendrift Boerdery", "Binnekort oop by De Wagendrift Boerdery")}</p>
    <h1 id="hero-title">{t("Where nature meets art", "Waar natuur en kuns ontmoet")}</h1>
    <p class="hero__sub">{t("Original art and local talent in the heart of the Loskop Valley.", "Oorspronklike kuns en plaaslike talent in die hartjie van die Loskopvallei.")}</p>
    <div class="cta-row">
      <a class="btn" href="collection.html">{t("See the collection", "Sien die versameling")}</a>
      <a class="btn btn--ghost" href="visit.html">{t("Plan your visit", "Beplan jou besoek")}</a>
    </div>
  </div>
</section>

<section class="statement" aria-label="{t("What to expect", "Wat om te verwag")}">
  <blockquote>
    <p lang="af">Kuns wat jou laat stilstaan.<br>Kuns wat stories vertel.<br>Kuns wat jou hart raak.</p>
  </blockquote>
  {statement_sub}
</section>

<section class="walk" aria-labelledby="walk-title">
  <div class="walk__view" tabindex="-1">
    <div class="walk__track">
      <div class="walk__intro">
        <h2 id="walk-title">{t("Walk the wall", "Stap langs die muur")}</h2>
        <p class="only-pin">{t("Keep scrolling to walk along it. Select any work for a closer look.", "Hou aan rol om langs die muur te stap. Kies enige werk om dit van naby te sien.")}</p>
        <p class="only-swipe">{t("Swipe along the wall and tap any work for a closer look.", "Swiep langs die muur en tik op enige werk om dit van naby te sien.")}</p>
      </div>
{hang}      <div class="walk__end">
        <p>{t("Two artists, and a wall that keeps growing.", "Twee kunstenaars, en &rsquo;n muur wat aanhou groei.")}</p>
        <a class="btn" href="collection.html">{t("See the collection", "Sien die versameling")}</a>
      </div>
      <div class="walk__floor" aria-hidden="true"></div>
    </div>
  </div>
</section>

<section class="artists" id="artists" aria-labelledby="artists-title">
  <h2 id="artists-title">{t("Two artists. Two unique styles.", "Twee kunstenaars. Twee unieke style.")}</h2>
  <div class="artists__grid">
    <article class="artist artist--a">
      <a class="artist__media" href="lizette-nel.html" aria-label="{t("Meet Lizette Nel", "Ontmoet Lizette Nel")}">
        <img class="artist__work" src="{R}assets/img/photos/detail-goat-1000.webp" srcset="{R}assets/img/photos/detail-goat-600.webp 600w, {R}assets/img/photos/detail-goat-1000.webp 1000w, {R}assets/img/photos/detail-goat-1254.webp 1254w" sizes="(max-width: 1023px) 100vw, 56vw" alt="{e(tx(goat, "alt"))}" width="1254" height="1003" loading="lazy">
        <img class="artist__face" src="{R}assets/img/photos/lizette-nel.webp" alt="{t("Lizette Nel, smiling, with a sketchbook and pencil", "Lizette Nel, glimlaggend, met &rsquo;n sketsboek en potlood")}" width="560" height="560" loading="lazy">
      </a>
      <div class="artist__text">
        <p class="artist__role">{t("Mixed media and fine art", "Gemengde media en fynkuns")}</p>
        <h3>Lizette Nel</h3>
        <p class="artist__quote"><span lang="af">&ldquo;Ek is &rsquo;n mens van die aarde.&rdquo;</span>{t('<span class="artist__en">I am a person of the earth.</span>', "")}</p>
        <p>{t("Earthy colour, soft texture and subjects that say more than the eye sees at first glance. Lizette also works with line, lace and embroidery.",
              "Aardse kleure, sagte teksture en onderwerpe wat meer vertel as wat die oog met die eerste oogopslag sien. Lizette eksperimenteer ook met lyn, kant en borduurwerk.")}</p>
        <a class="link" href="lizette-nel.html">{t("Meet Lizette", "Ontmoet Lizette")}</a>
      </div>
    </article>
    <article class="artist artist--b">
      <a class="artist__media" href="jeanne-h-barnes.html" aria-label="{t("Meet Jeanne H Barnes", "Ontmoet Jeanne H Barnes")}">
        <span class="frame f-gilt"><img class="artist__work" src="{src(bb, 1)}" srcset="{srcset(bb)}" sizes="(max-width: 1023px) 90vw, 40vw" alt="{e(tx(bb, "alt"))}" {dims(bb)} loading="lazy"></span>
        <img class="artist__face" src="{R}assets/img/photos/jeanne-h-barnes.webp" alt="{t("Jeanne H Barnes, smiling, in her studio", "Jeanne H Barnes, glimlaggend, in haar ateljee")}" width="560" height="560" loading="lazy">
      </a>
      <div class="artist__text">
        <p class="artist__role">{t("Oil painter", "Olieverfkunstenaar")}</p>
        <h3>Jeanne H Barnes</h3>
        <p class="artist__quote"><span lang="af">&ldquo;Helder lig, warm kleur en die vreugde van kyk.&rdquo;</span>{t('<span class="artist__en">Bright light, warm colour and the joy of looking.</span>', "")}</p>
        <p>{t("Oil paintings that move between impressionism and realism, with strong contrast between light and shadow and bright, warm colour.",
              "Olieverfskilderye wat tussen impressionisme en realisme beweeg, met sterk kontras tussen lig en skadu en helder, warm kleure.")}</p>
        <a class="link" href="jeanne-h-barnes.html">{t("Meet Jeanne", "Ontmoet Jeanne")}</a>
      </div>
    </article>
  </div>
</section>

<section class="exhibit" aria-labelledby="exhibit-title">
  <img class="exhibit__img" src="{R}assets/img/photos/farm-aloes-1448.webp" srcset="{R}assets/img/photos/farm-aloes-900.webp 900w, {R}assets/img/photos/farm-aloes-1448.webp 1448w" sizes="100vw" alt="{t("Tall aloes in flower on a red earth bank in the bushveld, under a blue sky.", "Hoë aalwyne in blom op &rsquo;n rooigrondwal in die bosveld, onder &rsquo;n blou lug.")}" width="1448" height="1086" loading="lazy">
  <div class="exhibit__copy">
    <p class="exhibit__when">November 2026</p>
    <h2 id="exhibit-title">{t("See both artists at the Kranspoort Kunsuitstalling", "Sien albei kunstenaars by die Kranspoort Kunsuitstalling")}</h2>
    <a class="btn" href="{wa(t("Hello Aloe House, please send me the details of the Kranspoort Kunsuitstalling.", "Hallo Aloe House, stuur asseblief vir my die besonderhede van die Kranspoort Kunsuitstalling."))}" target="_blank" rel="noopener">{t("Ask about the exhibition", "Vra oor die uitstalling")}</a>
  </div>
</section>

<section class="visit-band" aria-labelledby="visit-title">
  <img class="visit-band__img" src="{R}assets/img/photos/gallery-building-1448.webp" srcset="{R}assets/img/photos/gallery-building-900.webp 900w, {R}assets/img/photos/gallery-building-1448.webp 1448w" sizes="100vw" alt="{t("The red-brick De Wagendrift Boerdery building with its curved entrance canopy, home of Aloe House Art Gallery.", "Die rooisteengebou van De Wagendrift Boerdery met sy geboë ingangsafdak, die tuiste van Aloe House Art Gallery.")}" width="1448" height="1086" loading="lazy">
  <div class="visit-card">
    <h2 id="visit-title">{t("Find us at De Wagendrift Boerdery", "Vind ons by De Wagendrift Boerdery")}</h2>
    <p>{t("Watch for our sign as you cross the Olifants River bridge, in the heart of the Loskop Valley. Follow us for the official opening announcement.",
          "Hou ons bord dop wanneer jy oor die Olifantsrivierbrug ry, in die hartjie van die Loskopvallei. Volg ons vir die amptelike aankondiging van die opening.")}</p>
    <a class="btn btn--ink" href="visit.html">{t("Plan your visit", "Beplan jou besoek")}</a>
  </div>
</section>
</main>
""" + footer() + scripts()


def page_collection(path):
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": t(f"The collection | {NAME}", f"Die versameling | {NAME}"),
        "url": BASE + t("", "af/") + path,
        "inLanguage": t("en-ZA", "af-ZA"),
        "isPartOf": {"@id": BASE + "#website"},
        "hasPart": [{"@type": "VisualArtwork", "name": tx(w, "title"), "artMedium": tx(w, "medium"),
                     "creator": {"@type": "Person", "name": w["artist"]}, **({"dateCreated": w["year"]} if w["year"] else {}),
                     "image": BASE + f'assets/img/works/{w["image"]}-{w["widths"][-1]}.webp'} for w in WORKS],
    }
    h = head(path,
             t(f"The Collection | {NAME}", f"Die Versameling | {NAME}"),
             t("Original paintings, drawings and mixed media by Lizette Nel and Jeanne H Barnes at Aloe House Art Gallery in the Loskop Valley. See each work up close and enquire on WhatsApp.",
               "Oorspronklike skilderye, tekeninge en gemengde media deur Lizette Nel en Jeanne H Barnes by Aloe House Art Gallery in die Loskopvallei. Sien elke werk van naby en rig navrae op WhatsApp."),
             og="collection", ld=ld)
    items = ""
    for w in WORKS:
        kind = w["artist"].split()[0].lower()
        items += (f'<figure class="piece" data-kind="{kind}" style="--ar:{w["ratio"]}">'
                  + framed(w, "(max-width: 599px) 46vw, (max-width: 1099px) 30vw, 24vw")
                  + f"<figcaption>{label(w, 'label--plain')}</figcaption></figure>\n")
    return h + header("collection", path) + f"""<main id="main" class="page">
<header class="page-head">
  <h1>{t("The collection", "Die versameling")}</h1>
  <p>{t("Original work by Lizette Nel and Jeanne H Barnes. Select any work to see it up close, against the wall colour of your choice.",
        "Oorspronklike werk deur Lizette Nel en Jeanne H Barnes. Kies enige werk om dit van naby te sien, teen die muurkleur van jou keuse.")}</p>
</header>
<div class="filters" role="group" aria-label="{t("Filter the collection", "Filtreer die versameling")}">
  <button class="chip" type="button" data-filter="all" aria-pressed="true">{t("All works", "Alle werke")}</button>
  <button class="chip" type="button" data-filter="lizette" aria-pressed="false">Lizette Nel</button>
  <button class="chip" type="button" data-filter="jeanne" aria-pressed="false">Jeanne H Barnes</button>
</div>
<div class="salon" id="salon">
{items}</div>
<p class="empty" id="salon-empty" hidden>{t("No works match this filter yet.", "Geen werke pas nog by hierdie filter nie.")} <button class="link" type="button" data-filter="all">{t("Show all works", "Wys alle werke")}</button></p>
<section class="page-cta">
  <h2>{t("Seen something you love?", "Iets gesien wat jy liefhet?")}</h2>
  <p>{t("Ask about availability and prices, or arrange to see a work in person.", "Vra oor beskikbaarheid en pryse, of reël om &rsquo;n werk self te kom sien.")}</p>
  <a class="btn" href="{wa(t("Hello Aloe House, I would like to know more about your collection.", "Hallo Aloe House, ek wil graag meer weet oor julle versameling."))}" target="_blank" rel="noopener">{icon("whatsapp-logo")}{t("WhatsApp us", "WhatsApp ons")}</a>
</section>
</main>
""" + footer() + scripts()


ARTIST_COPY = {
    "lizette-nel": {
        "name": "Lizette Nel", "first": "Lizette", "other": "jeanne-h-barnes",
        "role": ("Mixed media and fine art", "Gemengde media en fynkuns"),
        "quote": "&ldquo;Ek is &rsquo;n mens van die aarde.&rdquo;", "quote_en": "I am a person of the earth.",
        "desc": ("Lizette Nel creates portraits and nature scenes in earthy colour and soft texture, with line, lace and embroidery. Discover her work at Aloe House Art Gallery in the Loskop Valley.",
                 "Lizette Nel skep portrette en natuurtonele in aardse kleure en sagte teksture, met lyn, kant en borduurwerk. Ontdek haar werk by Aloe House Art Gallery in die Loskopvallei."),
        "face_alt": ("Lizette Nel, smiling, with a sketchbook and pencil", "Lizette Nel, glimlaggend, met &rsquo;n sketsboek en potlood"),
        "en": [
            "That love runs like a golden thread through Lizette Nel&rsquo;s art. Her interest in portraits and nature comes through in earthy colours, soft textures and subjects that say more than the eye sees at first glance.",
            "With soft browns and greens and warm neutrals, she creates a feeling of calm, connection and homecoming. She also experiments with line, lace and embroidery, which bring new texture and meaning to her drawing and painting.",
            "Faith, family and life experience give her work its depth. Through her honest, human approach, Lizette reminds us that even after loss there is still beauty to notice and hope to discover.",
        ],
        "af": [
            "Dié liefde lê soos &rsquo;n goue draad deur Lizette Nel se kuns. Haar belangstelling in portrette en die natuur kom na vore in aardse kleure, sagte teksture en onderwerpe wat meer vertel as wat die oog met die eerste oogopslag sien.",
            "Met sagte bruin- en groenskakerings en warm neutrale kleure skep sy &rsquo;n gevoel van rus, verbondenheid en tuiskoms. Sy eksperimenteer ook met lyn, kant en borduurwerk, wat nuwe teksture en betekenis aan haar teken- en skildertegnieke gee.",
            "Geloof, familie en lewenservarings gee haar werk diepte. Deur haar eerlike, menslike benadering herinner Lizette ons dat selfs ná verlies daar steeds skoonheid is om raak te sien en hoop om te ontdek.",
        ],
    },
    "jeanne-h-barnes": {
        "name": "Jeanne H Barnes", "first": "Jeanne", "other": "lizette-nel",
        "role": ("Oil painter", "Olieverfkunstenaar"),
        "quote": "&ldquo;Helder lig, warm kleur en die vreugde van kyk.&rdquo;", "quote_en": "Bright light, warm colour and the joy of looking.",
        "desc": ("Jeanne H Barnes paints in oil, between impressionism and realism, with bright light and warm colour. Discover her work at Aloe House Art Gallery in the Loskop Valley.",
                 "Jeanne H Barnes skilder in olieverf, tussen impressionisme en realisme, met helder lig en warm kleure. Ontdek haar werk by Aloe House Art Gallery in die Loskopvallei."),
        "face_alt": ("Jeanne H Barnes, smiling, in her studio", "Jeanne H Barnes, glimlaggend, in haar ateljee"),
        "en": [
            "Jeanne H Barnes&rsquo;s art moves between impressionism and realism, with strong contrast between light and shadow. Her paintings are known for bright, warm colours that bring energy and life to the subject. Oil remains her favourite medium, and she uses it to capture the atmosphere, character and colour of what she paints.",
            "For Jeanne, colour is an important part of the process. She chooses the colours that serve the subject best, and favours combinations that create warmth, light and balance. The interplay of light, shadow and colour gives her work depth, movement and a sense of life.",
            "Through the Kranspoort Kunsuitstalling, Jeanne shares her love of art with the community. She hopes visitors will stop, take in the colour and light, and rediscover the joy of looking.",
        ],
        "af": [
            "Jeanne H Barnes se kuns beweeg tussen impressionisme en realisme, met sterk kontras tussen lig en skadu. Haar skilderye word gekenmerk deur helder, warm kleure wat lewe en energie aan die onderwerp gee. Olieverf bly haar voorkeurmedium en sy gebruik dit om die atmosfeer, karakter en kleur van haar onderwerpe vas te vang.",
            "Kleur is vir Jeanne &rsquo;n belangrike deel van haar kunsproses. Sy kies kleure wat die onderwerp die beste dien en verkies kombinasies wat warmte, lig en balans skep. Die wisselwerking tussen lig, skadu en kleur gee haar werk diepte, beweging en &rsquo;n gevoel van lewe.",
            "Deur haar deelname aan die Kranspoort Kunsuitstalling deel Jeanne haar liefde vir kuns met die gemeenskap. Sy hoop dat besoekers sal stil staan, die kleure en lig sal beleef en die vreugde van kyk weer sal ontdek.",
        ],
    },
}


def page_artist(path):
    slug = path[:-5]
    a = ARTIST_COPY[slug]
    name, first = a["name"], a["first"]
    other = ARTIST_COPY[a["other"]]
    ld = {"@context": "https://schema.org", "@type": "Person", "name": name, "jobTitle": t(a["role"][0], a["role"][1]),
          "image": BASE + f"assets/img/photos/{slug}.webp", "url": BASE + t("", "af/") + path,
          "affiliation": {"@type": "ArtGallery", "name": NAME, "url": BASE}}
    if slug == "jeanne-h-barnes":
        ld["alternateName"] = "Jeanne Barnes Tosen"
    h = head(path, t(f"{name}, Artist | {NAME}", f"{name}, Kunstenaar | {NAME}"), t(*a["desc"]), og=slug,
             og_alt=t(f"{name} at {NAME}", f"{name} by {NAME}"), ld=ld)
    mine = [w for w in WORKS if ARTISTS[w["artist"]] == slug]
    hung = "".join(f'<figure class="piece piece--big" style="--ar:{w["ratio"]}">{framed(w, "(max-width: 1023px) 90vw, 46vw")}<figcaption>{label(w, "label--plain")}</figcaption></figure>' for w in mine)
    body = "".join(f"<p>{p}</p>" for p in a[L])
    quote_en = t(f'<span class="artist__en">{a["quote_en"]}</span>', "")
    ask = t(f"Hello Aloe House, I would like to know more about {name}'s work.", f"Hallo Aloe House, ek wil graag meer weet oor {name} se werk.")
    return h + header("artists", path) + f"""<main id="main" class="page">
<section class="bio">
  <div class="bio__face"><img src="{R}assets/img/photos/{slug}.webp" alt="{t(*a["face_alt"])}" width="560" height="560" fetchpriority="high"></div>
  <div class="bio__text">
    <p class="bio__kicker">{t(*a["role"])}</p>
    <h1>{e(name)}</h1>
    <p class="artist__quote artist__quote--big"><span lang="af">{a["quote"]}</span>{quote_en}</p>
    {body}
    <div class="cta-row">
      <a class="btn" href="{wa(ask)}" target="_blank" rel="noopener">{icon("whatsapp-logo")}{t(f"Ask about {first}&rsquo;s work", f"Vra oor {first} se werk")}</a>
    </div>
  </div>
</section>
<section class="bio-works" aria-labelledby="works-title">
  <h2 id="works-title">{t("On the wall", "Aan die muur")}</h2>
  <div class="bio-works__grid">{hung}</div>
</section>
<section class="exhibit-note">
  <h2>Kranspoort Kunsuitstalling, November 2026</h2>
  <p>{t(f"Come and discover {first}&rsquo;s work in person at the exhibition.", f"Kom ontdek {first} se werk self by die uitstalling.")}</p>
  <a class="link" href="{wa(t("Hello Aloe House, please send me the details of the Kranspoort Kunsuitstalling.", "Hallo Aloe House, stuur asseblief vir my die besonderhede van die Kranspoort Kunsuitstalling."))}" target="_blank" rel="noopener">{t("Ask about the exhibition", "Vra oor die uitstalling")}</a>
</section>
<p class="next-artist">{t("Next artist", "Volgende kunstenaar")}: <a class="link" href="{a["other"]}.html">{e(other["name"])}</a></p>
</main>
""" + footer() + scripts()


def page_visit(path):
    h = head(path,
             t(f"Visit | {NAME}, Loskop Valley", f"Besoek | {NAME}, Loskopvallei"),
             t("Find Aloe House Art Gallery at De Wagendrift Boerdery in the Loskop Valley near Groblersdal. Watch for the sign at the Olifants River bridge. Opening soon.",
               "Vind Aloe House Art Gallery by De Wagendrift Boerdery in die Loskopvallei naby Groblersdal. Hou die bord by die Olifantsrivierbrug dop. Binnekort oop."),
             og="visit", ld=gallery_ld())
    opts = [("Visiting the gallery", "&rsquo;n Besoek aan die galery"), ("A work in the collection", "&rsquo;n Werk in die versameling"),
            ("The Kranspoort Kunsuitstalling", "Die Kranspoort Kunsuitstalling"), ("Showing my work at Aloe House", "Om my werk by Aloe House uit te stal"),
            ("Something else", "Iets anders")]
    options = "".join(f"<option>{t(*o)}</option>" for o in opts)
    return h + header("visit", path) + f"""<main id="main" class="page">
<section class="visit-hero">
  <img src="{R}assets/img/photos/gallery-building-1448.webp" srcset="{R}assets/img/photos/gallery-building-900.webp 900w, {R}assets/img/photos/gallery-building-1448.webp 1448w" sizes="100vw" alt="{t("The red-brick De Wagendrift Boerdery building with its curved entrance canopy, home of Aloe House Art Gallery.", "Die rooisteengebou van De Wagendrift Boerdery met sy geboë ingangsafdak, die tuiste van Aloe House Art Gallery.")}" width="1448" height="1086" fetchpriority="high">
  <div class="visit-hero__copy">
    <h1>{t("Visit Aloe House", "Besoek Aloe House")}</h1>
    <p>{t("A place where art, creativity and nature come together, in the heart of the Loskop Valley.", "&rsquo;n Plek waar kuns, kreatiwiteit en die natuur bymekaarkom, in die hartjie van die Loskopvallei.")}</p>
  </div>
</section>
<section class="visit-grid">
  <div class="visit-info">
    <h2>{t("Finding us", "Hoe om ons te vind")}</h2>
    <p>{t("Watch for the Aloe House sign as you cross the Olifants River bridge. The gallery is at De Wagendrift Boerdery, near Groblersdal.",
          "Hou die Aloe House-bord dop wanneer jy oor die Olifantsrivierbrug ry. Die galery is by De Wagendrift Boerdery, naby Groblersdal.")}</p>
    <dl class="facts">
      <div><dt>{t("Address", "Adres")}</dt><dd>{t("De Wagendrift Boerdery, Loskop Valley, Groblersdal, South Africa", "De Wagendrift Boerdery, Loskopvallei, Groblersdal, Suid-Afrika")}</dd></div>
      <div><dt>{t("Phone and WhatsApp", "Telefoon en WhatsApp")}</dt><dd><a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a></dd></div>
      <div><dt>{t("Opening", "Opening")}</dt><dd>{t(f'Opening soon. The date and hours will be announced on <a href="{FB}" target="_blank" rel="noopener">our Facebook page</a>.', f'Binnekort oop. Die datum en ure word op <a href="{FB}" target="_blank" rel="noopener">ons Facebook-blad</a> aangekondig.')}</dd></div>
    </dl>
    <div class="cta-row">
      <a class="btn" href="{MAPS}" target="_blank" rel="noopener">{icon("navigation-arrow")}{t("Open in Google Maps", "Maak oop in Google Maps")}</a>
    </div>
    <figure class="visit-photo">
      <img src="{R}assets/img/photos/farm-aloes-900.webp" srcset="{R}assets/img/photos/farm-aloes-900.webp 900w, {R}assets/img/photos/farm-aloes-1448.webp 1448w" sizes="(max-width: 1023px) 100vw, 50vw" alt="{t("Tall aloes in flower on a red earth bank in the bushveld, under a blue sky.", "Hoë aalwyne in blom op &rsquo;n rooigrondwal in die bosveld, onder &rsquo;n blou lug.")}" width="1448" height="1086" loading="lazy">
    </figure>
  </div>
  <form class="enquiry" id="enquiry" novalidate data-intro="{t("Hello Aloe House, this is", "Hallo Aloe House, dit is")}" data-about="{t("About", "Oor")}">
    <h2>{t("Send us a message", "Stuur vir ons &rsquo;n boodskap")}</h2>
    <p>{t("Art lover, collector, or simply curious, we&rsquo;d love to hear from you. Your message opens in WhatsApp, ready to send.",
          "Kunsliefhebber, versamelaar of net nuuskierig? Ons hoor graag van jou. Jou boodskap maak in WhatsApp oop, gereed om te stuur.")}</p>
    <div class="field">
      <label for="f-name">{t("Your name", "Jou naam")}</label>
      <input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-err">
      <p class="field__err" id="f-name-err" hidden>{t("Enter your name so we know who to reply to.", "Vul jou naam in sodat ons weet vir wie om te antwoord.")}</p>
    </div>
    <div class="field">
      <label for="f-about">{t("What is it about?", "Waaroor gaan dit?")}</label>
      <select id="f-about" name="about">{options}</select>
    </div>
    <div class="field">
      <label for="f-msg">{t("Your message", "Jou boodskap")}</label>
      <textarea id="f-msg" name="message" rows="4" required aria-describedby="f-msg-err"></textarea>
      <p class="field__err" id="f-msg-err" hidden>{t("Write a short message before sending.", "Skryf &rsquo;n kort boodskap voor jy stuur.")}</p>
    </div>
    <button class="btn" type="submit">{icon("whatsapp-logo")}{t("Send on WhatsApp", "Stuur op WhatsApp")}</button>
  </form>
</section>
</main>
""" + footer() + scripts(with_room=False)


def legal(path, title, desc, body):
    h = head(path, f"{title} | {NAME}", desc)
    return h + header("legal", path) + f"""<main id="main" class="page legal">
<h1>{title}</h1>
<p class="legal__date">{t("Last updated 13 November 2026", "Laas bygewerk op 13 November 2026")}</p>
{body}
</main>
""" + footer() + scripts(with_room=False)


def page_privacy(path):
    tel = f'<a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a>'
    reg = '<a href="https://inforegulator.org.za/" target="_blank" rel="noopener">inforegulator.org.za</a>'
    if L == "af":
        body = f"""
<p>Hierdie beleid verduidelik hoe {NAME} ("ons") persoonlike inligting insamel, gebruik en beskerm wanneer jy hierdie webwerf gebruik of ons kontak, in ooreenstemming met die Wet op die Beskerming van Persoonlike Inligting 4 van 2013 (POPIA).</p>
<h2>Wie ons is</h2>
<dl class="facts">
  <div><dt>Besigheid</dt><dd>{NAME}</dd></div>
  <div><dt>Adres</dt><dd>De Wagendrift Boerdery, Loskopvallei, Groblersdal, Suid-Afrika</dd></div>
  <div><dt>Telefoon en WhatsApp</dt><dd>{tel}</dd></div>
</dl>
<h2>Wat ons insamel</h2>
<p>Hierdie webwerf het geen rekeninge, aanlyn betalings of databasis van besoekers nie. Ons ontvang slegs persoonlike inligting wanneer jy kies om ons te kontak, byvoorbeeld per telefoon, WhatsApp of Facebook. Dit kan jou naam, telefoonnommer, enige besonderhede in jou boodskap en die kunswerke waaroor jy navraag doen, insluit.</p>
<p>Die boodskapvorm op ons Besoek-blad stoor of stuur self niks aan ons nie. Dit berei &rsquo;n boodskap in WhatsApp op jou eie toestel voor, en niks bereik ons tensy jy daar op stuur druk nie.</p>
<h2>Waarvoor ons dit gebruik</h2>
<ul>
  <li>Om jou vrae oor die galery, die kunstenaars en die werke te beantwoord.</li>
  <li>Om besoeke te reël, en om die koop, raam en aflewering van &rsquo;n werk wat jy wil koop, te reël.</li>
  <li>Om die verkoops- en besigheidsrekords te hou wat die wet van ons vereis.</li>
</ul>
<p>Ons stuur nie bemarkingsboodskappe tensy jy daarvoor gevra het nie, en jy kan ons enige tyd vra om op te hou.</p>
<h2>Koekies en naspeuring</h2>
<p>Ons gebruik geen ontledings, advertensie-naspeurders of koekies op hierdie webwerf nie. Ons lettertipes en beelde word van hierdie webwerf self bedien.</p>
<h2>Ander dienste</h2>
<p>Hierdie webwerf word op GitHub Pages gehuisves, wat standaard tegniese logs soos IP-adresse kan hou om die diens veilig te hou. Skakels na WhatsApp, Facebook en Google Maps neem jou na daardie dienste, en hul eie privaatheidsbeleide geld sodra jy daar is.</p>
<h2>Deel van jou inligting</h2>
<p>Ons verkoop nie jou persoonlike inligting nie. Ons deel dit slegs wanneer dit nodig is om jou te help, soos met &rsquo;n koerier of raammaker vir jou bestelling, met &rsquo;n kunstenaar oor wie se werk jy navraag gedoen het, of wanneer die wet dit vereis.</p>
<h2>Hoe lank ons dit hou</h2>
<p>Ons hou navrae so lank as wat dit nuttig is om jou te antwoord, en verkoopsrekords so lank as wat die wet vereis. Daarna vee ons dit uit.</p>
<h2>Jou regte</h2>
<p>Ingevolge POPIA mag jy vra of ons jou persoonlike inligting hou, &rsquo;n afskrif vra, ons vra om dit reg te stel of uit te vee, en beswaar maak teen hoe ons dit gebruik. Kontak ons hiervoor by {tel}.</p>
<p>As jy ontevrede is met hoe ons jou inligting hanteer het, kan jy by die Inligtingsreguleerder van Suid-Afrika kla by {reg}.</p>
<h2>Veranderinge aan hierdie beleid</h2>
<p>Ons kan hierdie beleid van tyd tot tyd bywerk. Die datum bo-aan wys wanneer dit laas verander het.</p>
"""
    else:
        body = f"""
<p>This policy explains how {NAME} ("we", "us") collects, uses and protects personal information when you use this website or contact us, in line with the Protection of Personal Information Act 4 of 2013 (POPIA).</p>
<h2>Who we are</h2>
<dl class="facts">
  <div><dt>Business</dt><dd>{NAME}</dd></div>
  <div><dt>Address</dt><dd>De Wagendrift Boerdery, Loskop Valley, Groblersdal, South Africa</dd></div>
  <div><dt>Phone and WhatsApp</dt><dd>{tel}</dd></div>
</dl>
<h2>What we collect</h2>
<p>This website has no accounts, no online payments and no database of visitors. We only receive personal information when you choose to contact us, for example by phone, WhatsApp or Facebook. That may include your name, phone number, any details you put in your message, and which artworks you asked about.</p>
<p>The message form on our Visit page does not store or send anything to us by itself. It prepares a message in WhatsApp on your own device, and nothing reaches us unless you press send there.</p>
<h2>Why we use it</h2>
<ul>
  <li>To answer your questions about the gallery, the artists and the works.</li>
  <li>To arrange visits, and to arrange the sale, framing and delivery of a work you want to buy.</li>
  <li>To keep the sales and business records we are legally required to keep.</li>
</ul>
<p>We do not send marketing messages unless you have asked us to, and you can ask us to stop at any time.</p>
<h2>Cookies and tracking</h2>
<p>We do not use analytics, advertising trackers or cookies on this website. Our fonts and images are served from this website itself.</p>
<h2>Other services</h2>
<p>This website is hosted on GitHub Pages, which may keep standard technical logs such as IP addresses to keep the service secure. Links to WhatsApp, Facebook and Google Maps take you to those services, and their own privacy policies apply once you are there.</p>
<h2>Sharing your information</h2>
<p>We do not sell your personal information. We share it only when it is needed to help you, such as with a courier or framer for your order, with an artist whose work you have asked about, or when the law requires it.</p>
<h2>How long we keep it</h2>
<p>We keep enquiries for as long as they are useful for answering you, and sales records for as long as the law requires. After that we delete them.</p>
<h2>Your rights</h2>
<p>Under POPIA you may ask whether we hold your personal information, ask for a copy, ask us to correct or delete it, and object to how we use it. To do so, contact us on {tel}.</p>
<p>If you are unhappy with how we handled your information, you may complain to the Information Regulator of South Africa at {reg}.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The date at the top shows when it last changed.</p>
"""
    return legal(path, t("Privacy policy", "Privaatheidsbeleid"),
                 t(f"How {NAME} collects, uses and protects your personal information under POPIA.", f"Hoe {NAME} jou persoonlike inligting ingevolge POPIA insamel, gebruik en beskerm."), body)


def page_terms(path):
    tel = f'<a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a>'
    if L == "af":
        body = f"""
<p>Hierdie voorwaardes geld wanneer jy hierdie webwerf gebruik. Deur dit te gebruik, stem jy daartoe in. As jy &rsquo;n werk by ons koop, geld hierdie voorwaardes saam met enigiets wat ons skriftelik met jou ooreenkom.</p>
<h2>Oor hierdie webwerf</h2>
<p>Hierdie webwerf word bedryf deur {NAME}, De Wagendrift Boerdery, Loskopvallei, Groblersdal, Suid-Afrika. Jy kan ons bereik by {tel}.</p>
<h2>Foto&rsquo;s</h2>
<p>Die foto&rsquo;s van kunswerke word deur die kunstenaars voorsien. Die vertrek agter die skildery op ons tuisblad is &rsquo;n illustrasie van hoe werke gehang word, nie &rsquo;n foto van die galery nie.</p>
<h2>Kunswerke, pryse en beskikbaarheid</h2>
<p>Werke wat hier gewys word, is onderhewig aan beskikbaarheid en kan reeds verkoop wees. Kleure en teksture kan op jou skerm anders lyk as in werklikheid. Niks op hierdie webwerf is &rsquo;n aanbod om te verkoop nie. &rsquo;n Verkoping vind eers plaas wanneer ons die werk, die prys en die afleweringsreëlings direk met jou bevestig het.</p>
<h2>Kopiereg</h2>
<p>Elke kunswerk bly die kopiereg van sy kunstenaar, ook nadat dit verkoop is, tensy skriftelik anders ooreengekom. Jy mag skakels na hierdie webwerf deel, maar jy mag nie beelde van die werke sonder toestemming kopieer, druk, reproduseer of verkoop nie. Die {NAME}-naam en -logo behoort aan die galery.</p>
<h2>Gebruik van hierdie webwerf</h2>
<p>Gebruik asseblief hierdie webwerf wettig en moenie probeer om dit te ontwrig nie. Ons doen moeite om die inligting hier korrek te hou, insluitend openingsbesonderhede, maar dit kan verander, so bevestig asseblief met ons voordat jy reis.</p>
<h2>Skakels na ander dienste</h2>
<p>Ons skakel na WhatsApp, Facebook en Google Maps vir jou gerief. Ons is nie verantwoordelik vir daardie dienste of hul inhoud nie.</p>
<h2>Aanspreeklikheid</h2>
<p>Sover die wet toelaat, is ons nie aanspreeklik vir verlies wat voortspruit uit die gebruik van hierdie webwerf of die vertroue op die inhoud daarvan nie. Niks in hierdie voorwaardes beperk jou regte ingevolge die Wet op Verbruikersbeskerming 68 van 2008 nie.</p>
<h2>Toepaslike reg en veranderinge</h2>
<p>Hierdie voorwaardes word deur die reg van Suid-Afrika beheer. Ons kan dit van tyd tot tyd bywerk, en die datum bo-aan wys wanneer dit laas verander het.</p>
"""
    else:
        body = f"""
<p>These terms apply when you use this website. By using it, you agree to them. If you buy a work from us, these terms apply together with anything we agree with you in writing.</p>
<h2>About this website</h2>
<p>This website is run by {NAME}, De Wagendrift Boerdery, Loskop Valley, Groblersdal, South Africa. You can reach us on {tel}.</p>
<h2>Photographs</h2>
<p>Photographs of the artworks are supplied by the artists. The room behind the painting on our home page is an illustration of how works are hung, not a photograph of the gallery.</p>
<h2>Artworks, prices and availability</h2>
<p>Works shown here are subject to availability and may already be sold. Colours and textures can look different on your screen than they do in person. Nothing on this website is an offer to sell. A sale only takes place once we have confirmed the work, the price and the delivery arrangements with you directly.</p>
<h2>Copyright</h2>
<p>Each artwork remains the copyright of its artist, including after it is sold, unless agreed otherwise in writing. You may share links to this website, but you may not copy, print, reproduce or sell images of the works without permission. The {NAME} name and logo belong to the gallery.</p>
<h2>Using this website</h2>
<p>Please use this website lawfully and do not try to disrupt it. We work to keep the information here correct, including opening details, but it may change, so please confirm with us before you travel.</p>
<h2>Links to other services</h2>
<p>We link to WhatsApp, Facebook and Google Maps for your convenience. We are not responsible for those services or their content.</p>
<h2>Liability</h2>
<p>To the extent the law allows, we are not liable for loss that results from using this website or relying on its content. Nothing in these terms limits rights you have under the Consumer Protection Act 68 of 2008.</p>
<h2>Governing law and changes</h2>
<p>These terms are governed by the laws of South Africa. We may update them from time to time, and the date at the top shows when they last changed.</p>
"""
    return legal(path, t("Terms of use", "Gebruiksvoorwaardes"),
                 t(f"The terms for using the {NAME} website, including copyright and availability.", f"Die voorwaardes vir die gebruik van die {NAME}-webwerf, insluitend kopiereg en beskikbaarheid."), body)


def page_404(path):
    h = head(path, f"Page not found | {NAME}", "This page could not be found.", robots="noindex", alternates=False)
    h = h.replace("<head>\n", '<head>\n<base href="/Aloe-House-Art-Gallery/">\n', 1)
    return h + header("404", None) + f"""<main id="main" class="page not-found">
<span class="frame f-gilt not-found__frame" aria-hidden="true"><span></span></span>
<h1>This wall is empty</h1>
<p>The page you were looking for isn&rsquo;t here. It may have moved, or the link may be wrong. <span lang="af">Hierdie blad bestaan nie.</span></p>
<div class="cta-row"><a class="btn" href="index.html">Back to the gallery</a><a class="btn btn--ghost" href="af/index.html" lang="af">Na die Afrikaanse webwerf</a></div>
</main>
""" + footer() + scripts(with_room=False)


def page_moved(path, to):
    """Old address kept alive so earlier shared links still land on the right page."""
    return f"""<!doctype html>
<html lang="en-ZA"><head><meta charset="utf-8"><title>{NAME}</title>
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE}{to}">
<meta http-equiv="refresh" content="0; url={to}"></head>
<body><p><a href="{to}">Jeanne H Barnes</a></p></body></html>
"""


PAGES = {
    "index.html": page_home,
    "collection.html": page_collection,
    "lizette-nel.html": page_artist,
    "jeanne-h-barnes.html": page_artist,
    "visit.html": page_visit,
    "privacy.html": page_privacy,
    "terms.html": page_terms,
}

(ROOT / "af").mkdir(exist_ok=True)
for lang, prefix in (("en", ""), ("af", "af/")):
    L, R = lang, ("../" if lang == "af" else "")
    for name, fn in PAGES.items():
        html = fn(name)
        if any(c in html for c in ("—", "–")):
            raise SystemExit(f"{prefix}{name} contains a banned dash")
        (ROOT / prefix / name).write_text(html, encoding="utf8", newline="\n")
L, R = "en", ""
(ROOT / "404.html").write_text(page_404("404.html"), encoding="utf8", newline="\n")
(ROOT / "jeanne-barnes-tosen.html").write_text(page_moved("jeanne-barnes-tosen.html", "jeanne-h-barnes.html"), encoding="utf8", newline="\n")

priority = {"index.html": "1.0", "collection.html": "0.9", "lizette-nel.html": "0.8", "jeanne-h-barnes.html": "0.8", "visit.html": "0.8"}
rows = []
for p in PAGES:
    en = BASE + ("" if p == "index.html" else p)
    af = BASE + "af/" + ("" if p == "index.html" else p)
    alts = (f'<xhtml:link rel="alternate" hreflang="en-ZA" href="{en}"/><xhtml:link rel="alternate" hreflang="af-ZA" href="{af}"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{en}"/>')
    for loc in (en, af):
        rows.append(f"<url><loc>{loc}</loc>{alts}<lastmod>{ISO}</lastmod><priority>{priority.get(p, '0.3')}</priority></url>")
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                                  + "\n".join(rows) + "\n</urlset>\n", encoding="utf8", newline="\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf8", newline="\n")
manifest = {
    "name": NAME, "short_name": "Aloe House", "description": "Where nature meets art. Original art in the Loskop Valley.",
    "start_url": "./", "scope": "./", "display": "standalone", "background_color": GREEN, "theme_color": GREEN,
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
(ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf8", newline="\n")
print("built", len(PAGES) * 2 + 2, "pages")

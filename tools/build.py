"""Writes every page, the sitemap and the manifest. Run: python tools/build.py
Works come from tools/collection.json. Business details live in the constants below."""
import json
import re
from html import escape as e
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://obsidianstudiodesigns.github.io/Aloe-House-Art-Gallery/"
NAME = "Aloe House Art Gallery"
TAGLINE = "Where nature meets art"
PHONE_LOCAL = "083 798 2734"
PHONE_INTL = "+27837982734"
WA = "https://wa.me/27837982734"
FB = "https://www.facebook.com/profile.php?id=61595805510704"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote("De Wagendrift Boerdery, Groblersdal, South Africa")
CREDIT = "https://obsidianstudiodesigns.co.za/"
UPDATED = "6 November 2026"
ISO = "2026-11-06"
GREEN = "#14291c"

WORKS = json.loads((ROOT / "tools/collection.json").read_text(encoding="utf8"))
BY = {w["slug"]: w for w in WORKS}


def wa(text=None):
    return WA + ("?text=" + quote(text) if text else "")


def icon(name, cls=""):
    return f'<svg class="icon {cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def sprite():
    out = []
    for f in sorted((ROOT / "tools/icons").glob("*.svg")):
        s = f.read_text(encoding="utf8")
        inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
        out.append(f'<symbol id="i-{f.stem}" viewBox="0 0 256 256">{inner.strip()}</symbol>')
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(out) + "</svg>"


SPRITE = sprite()


def srcset(w):
    return ", ".join(f'assets/img/works/{w["image"]}-{x}.webp {x}w' for x in w["widths"])


def src(w, i=0):
    return f'assets/img/works/{w["image"]}-{w["widths"][i]}.webp'


def dims(w, width=None):
    width = width or w["widths"][-1]
    return f'width="{width}" height="{round(width / w["ratio"])}"'


def byline(w):
    return "Sample artwork" if w["sample"] else w["artist"]


def label(w, extra=""):
    year = f', {w["year"]}' if w["year"] else ""
    sample = '<span class="label__sample">Sample artwork</span>' if w["sample"] else f'<span class="label__by">{e(w["artist"])}</span>'
    return f'<span class="label {extra}">{sample}<span class="label__title">{e(w["title"])}{year}</span><span class="label__medium">{e(w["medium"])}</span></span>'


def framed(w, sizes, loading="lazy", attrs=""):
    return (
        f'<button class="frame f-{w["frame"]}" type="button" data-work="{w["slug"]}" aria-label="View {e(w["title"])}, {e(byline(w))}" {attrs}>'
        f'<img src="{src(w)}" srcset="{srcset(w)}" sizes="{sizes}" alt="{e(w["alt"])}" {dims(w)} loading="{loading}" decoding="async">'
        "</button>"
    )


def head(title, desc, path, og="home", og_alt=None, extra="", ld=None, robots="index,follow,max-image-preview:large"):
    url = BASE + path
    img = f"{BASE}assets/img/og/{og}.jpg"
    og_alt = og_alt or f"{NAME}: {TAGLINE}"
    data = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="{GREEN}">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_ZA">
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
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="96x96" href="favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/Gloock-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/InstrumentSans-normal.woff2" as="font" type="font/woff2" crossorigin>
{extra}<link rel="stylesheet" href="assets/css/style.css">
{data}
</head>
"""


def header(page):
    def link(href, text, key):
        cur = ' aria-current="page"' if key == page else ""
        return f'<a href="{href}"{cur}>{text}</a>'

    def tab(href, text, ic, key):
        cur = ' aria-current="page"' if key == page else ""
        return f'<a class="tab" href="{href}"{cur}>{icon(ic)}{text}</a>'

    return f"""<body data-page="{page}">
{SPRITE}
<a class="skip" href="#main">Skip to content</a>
<div class="top-sentinel" aria-hidden="true"></div>
<header class="site-head">
  <a class="brand" href="index.html">
    <img src="assets/img/brand/crest.webp" alt="" width="396" height="423">
    <span class="brand__text"><span class="brand__a">Aloe House</span><span class="brand__b">Art Gallery</span></span>
  </a>
  <nav class="site-nav" aria-label="Main">
    {link("collection.html", "Collection", "collection")}
    {link("index.html#artists", "Artists", "artists")}
    {link("visit.html", "Visit", "visit")}
    <a class="btn btn--small" href="{wa()}" target="_blank" rel="noopener">{icon("whatsapp-logo")}WhatsApp us</a>
  </nav>
</header>
<nav class="tabbar" aria-label="Quick links">
  {tab("index.html", "Home", "house", "home")}
  {tab("collection.html", "Collection", "frame-corners", "collection")}
  {tab("index.html#artists", "Artists", "paint-brush", "artists")}
  {tab("visit.html", "Visit", "map-pin", "visit")}
  <a class="tab tab--wa" href="{wa()}" target="_blank" rel="noopener">{icon("whatsapp-logo")}WhatsApp</a>
</nav>
"""


def footer():
    return f"""<footer class="site-foot">
  <div class="foot-main">
    <img class="foot-logo" src="assets/img/brand/logo-round-320.webp" alt="{NAME} logo" width="320" height="320" loading="lazy">
    <div class="foot-col">
      <h2 class="foot-h">Find us</h2>
      <p>De Wagendrift Boerdery<br>Loskop Valley, Groblersdal<br>South Africa</p>
      <p><a href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps</a></p>
    </div>
    <div class="foot-col">
      <h2 class="foot-h">Talk to us</h2>
      <p><a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a></p>
      <p><a href="{wa()}" target="_blank" rel="noopener">WhatsApp</a></p>
      <p><a href="{FB}" target="_blank" rel="noopener">Facebook</a></p>
    </div>
    <div class="foot-col">
      <h2 class="foot-h">Explore</h2>
      <p><a href="collection.html">Collection</a></p>
      <p><a href="lizette-nel.html">Lizette Nel</a></p>
      <p><a href="jeanne-barnes-tosen.html">Jeanne Barnes Tosen</a></p>
      <p><a href="visit.html">Visit</a></p>
    </div>
  </div>
  <p class="foot-note">Works marked "Sample artwork" and the room photographs are placeholders until the opening collection is photographed.</p>
  <div class="foot-end">
    <span>&copy; 2026 {NAME}. All rights reserved.</span>
    <span class="foot-legal"><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms of use</a></span>
    <span class="credit">Designed by <a href="{CREDIT}" target="_blank" rel="noopener">Obsidian Studio Designs</a></span>
  </div>
</footer>
"""


ROOM = """<dialog class="room" id="room" aria-label="Viewing room">
  <div class="room__bar">
    <div class="room__walls" role="group" aria-label="Wall colour">
      <span class="room__walls-label">Wall</span>
      <button type="button" class="swatch swatch--green" data-wall="green" aria-pressed="true"><span>Aloe green</span></button>
      <button type="button" class="swatch swatch--lime" data-wall="lime" aria-pressed="false"><span>Limewash</span></button>
      <button type="button" class="swatch swatch--clay" data-wall="clay" aria-pressed="false"><span>Clay</span></button>
    </div>
    <div class="room__nav">
      <button type="button" class="room__btn" data-prev aria-label="Previous work">""" + icon("arrow-left") + """</button>
      <button type="button" class="room__btn" data-next aria-label="Next work">""" + icon("arrow-right") + """</button>
      <button type="button" class="room__btn" data-close aria-label="Close viewing room" autofocus>""" + icon("x") + """</button>
    </div>
  </div>
  <div class="room__body">
    <div class="room__art"><span class="frame" id="room-frame"><img id="room-img" alt=""></span></div>
    <aside class="room__label" id="room-label" aria-live="polite"></aside>
  </div>
</dialog>
"""


def scripts(room=True):
    data = ""
    if room:
        pub = [{k: w[k] for k in ("slug", "title", "artist", "year", "medium", "sample", "alt", "frame", "ratio")} | {"src": src(w, -1), "srcset": srcset(w)} for w in WORKS]
        data = f'{ROOM}<script type="application/json" id="works">{json.dumps(pub, ensure_ascii=False)}</script>\n<script>window.AH={{wa:{json.dumps(WA)}}}</script>\n'
    return data + '<script src="assets/js/main.js" defer></script>\n</body>\n</html>\n'


GALLERY_LD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "ArtGallery",
            "@id": BASE + "#gallery",
            "name": NAME,
            "url": BASE,
            "slogan": TAGLINE,
            "description": "Original art and local talent in the heart of the Loskop Valley, at De Wagendrift Boerdery near Groblersdal.",
            "logo": BASE + "assets/img/brand/logo-round.png",
            "image": BASE + "assets/img/og/home.jpg",
            "telephone": PHONE_INTL,
            "address": {"@type": "PostalAddress", "streetAddress": "De Wagendrift Boerdery", "addressLocality": "Groblersdal", "addressCountry": "ZA"},
            "areaServed": "Loskop Valley",
            "sameAs": [FB],
        },
        {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": NAME, "publisher": {"@id": BASE + "#gallery"}},
    ],
}


def page_home():
    hero_preload = (
        '<link rel="preload" as="image" href="assets/img/works/lizette-portrait-720.webp" imagesrcset="assets/img/works/lizette-portrait-420.webp 420w, assets/img/works/lizette-portrait-720.webp 720w, assets/img/works/lizette-portrait-1200.webp 1200w" imagesizes="(max-width: 1023px) 66vw, 30vw" fetchpriority="high">\n'
        '<link rel="preload" as="image" href="assets/img/photos/wall-wide.webp" media="(min-width: 1024px)">\n'
        '<link rel="preload" as="image" href="assets/img/photos/wall-tall.webp" media="(max-width: 1023px)">\n'
    )
    h = head(
        f"{NAME} | Original Art in the Loskop Valley, Groblersdal",
        "Original art and local talent at De Wagendrift Boerdery in the Loskop Valley near Groblersdal. Where nature meets art. Opening soon.",
        "",
        extra=hero_preload,
        ld=GALLERY_LD,
    )
    p = BY["lizette-portrait"]
    wall_ids = [w for w in WORKS if w.get("wall")]
    hang = ""
    for w in wall_ids:
        v = w["wall"]
        hang += (
            f'<figure class="hang" style="--h:{v["h"]};--y:{v["y"]};--ar:{w["ratio"]}">'
            + framed(w, f'(max-width: 1023px) 78vw, {round(v["h"] * w["ratio"] * 1.1)}vh')
            + f"<figcaption>{label(w)}</figcaption></figure>\n"
        )
    return h + header("home") + f"""<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <picture class="stage">
    <source media="(max-width: 1023px)" srcset="assets/img/photos/wall-tall.webp" width="864" height="1536">
    <img src="assets/img/photos/wall-wide.webp" alt="" width="1536" height="864" fetchpriority="high">
  </picture>
  <div class="hero__dim" aria-hidden="true"></div>
  <figure class="hero-art">
    <button class="frame f-gilt" type="button" data-work="{p["slug"]}" aria-label="View {e(p["title"])}, {e(p["artist"])}">
      <img src="{src(p, 1)}" srcset="{srcset(p)}" sizes="(max-width: 1023px) 66vw, 30vw" alt="{e(p["alt"])}" width="1200" height="1704" fetchpriority="high">
      <span class="sunfall" aria-hidden="true"></span>
    </button>
    <figcaption>{label(p)}</figcaption>
  </figure>
  <div class="hero__copy">
    <p class="hero__kicker">Opening soon at De Wagendrift Boerdery</p>
    <h1 id="hero-title">Where nature meets art</h1>
    <p class="hero__sub">Original art and local talent in the heart of the Loskop Valley.</p>
    <div class="cta-row">
      <a class="btn" href="collection.html">See the collection</a>
      <a class="btn btn--ghost" href="visit.html">Plan your visit</a>
    </div>
  </div>
</section>

<section class="statement" aria-label="What to expect">
  <blockquote>
    <p lang="af">Kuns wat jou laat stilstaan.<br>Kuns wat stories vertel.<br>Kuns wat jou hart raak.</p>
  </blockquote>
  <p class="statement__en">Art that stops you. Art that tells stories. Art that touches your heart.</p>
</section>

<section class="walk" aria-labelledby="walk-title">
  <div class="walk__view" tabindex="-1">
    <div class="walk__track">
      <div class="walk__intro">
        <h2 id="walk-title">Walk the wall</h2>
        <p class="only-pin">Keep scrolling to walk along it. Select any work for a closer look.</p>
        <p class="only-swipe">Swipe along the wall and tap any work for a closer look.</p>
      </div>
{hang}      <div class="walk__end">
        <p>Two artists, and a wall that keeps growing.</p>
        <a class="btn" href="collection.html">See the collection</a>
      </div>
      <div class="walk__floor" aria-hidden="true"></div>
    </div>
  </div>
</section>

<section class="artists" id="artists" aria-labelledby="artists-title">
  <h2 id="artists-title">Two artists. Two unique styles.</h2>
  <div class="artists__grid">
    <article class="artist artist--a">
      <a class="artist__media" href="lizette-nel.html" aria-label="Meet Lizette Nel">
        <img class="artist__work" src="assets/img/photos/detail-aloe-1000.webp" srcset="assets/img/photos/detail-aloe-600.webp 600w, assets/img/photos/detail-aloe-1000.webp 1000w" sizes="(max-width: 1023px) 100vw, 56vw" alt="Detail of Lizette Nel's painting: a farmhouse, a winding road and a flowering aloe beside white lace, on linen." width="1000" height="808" loading="lazy">
        <img class="artist__face" src="assets/img/photos/lizette-nel.webp" alt="Lizette Nel, smiling, with a pencil in her hand" width="556" height="584" loading="lazy">
      </a>
      <div class="artist__text">
        <h3>Lizette Nel</h3>
        <p class="artist__quote"><span lang="af">&ldquo;Ek is &rsquo;n mens van die aarde.&rdquo;</span><span class="artist__en">I am a person of the earth.</span></p>
        <p>Earthy colour, soft texture and close detail. Lizette&rsquo;s work is a celebration of faith, family, belonging and quiet beauty.</p>
        <a class="link" href="lizette-nel.html">Meet Lizette</a>
      </div>
    </article>
    <article class="artist artist--b">
      <a class="artist__media" href="jeanne-barnes-tosen.html" aria-label="Meet Jeanne Barnes Tosen">
        <span class="frame f-gilt"><img class="artist__work" src="assets/img/works/jeanne-bushbabies-720.webp" alt="Jeanne Barnes Tosen's painting of two bushbabies peeping over the rim of a rusted tin." width="720" height="500" loading="lazy"></span>
        <img class="artist__face" src="assets/img/photos/jeanne-barnes-tosen.webp" alt="Jeanne Barnes Tosen, smiling, in a blue scarf" width="588" height="592" loading="lazy">
      </a>
      <div class="artist__text">
        <h3>Jeanne Barnes Tosen</h3>
        <p class="artist__quote"><span lang="af">Waar kleur, natuur en nostalgie ontmoet.</span><span class="artist__en">Where colour, nature and nostalgia meet.</span></p>
        <p>Colourful still lifes, wildlife portraits and the quiet simplicity of the platteland, with a fine feel for light, shadow and composition.</p>
        <a class="link" href="jeanne-barnes-tosen.html">Meet Jeanne</a>
      </div>
    </article>
  </div>
</section>

<section class="exhibit" aria-labelledby="exhibit-title">
  <img class="exhibit__img" src="assets/img/photos/aloe-macro-1280.webp" srcset="assets/img/photos/aloe-macro-720.webp 720w, assets/img/photos/aloe-macro-1280.webp 1280w" sizes="100vw" alt="A flowering aloe, its coral spike lit by low winter sun." width="1280" height="960" loading="lazy">
  <div class="exhibit__copy">
    <p class="exhibit__when">November 2026</p>
    <h2 id="exhibit-title">See both artists at the Kranspoort Kunsuitstalling</h2>
    <a class="btn" href="{wa("Hello Aloe House, please send me the details of the Kranspoort Kunsuitstalling.")}" target="_blank" rel="noopener">Ask about the exhibition</a>
  </div>
</section>

<section class="visit-band" aria-labelledby="visit-title">
  <img class="visit-band__img" src="assets/img/photos/valley-1536.webp" srcset="assets/img/photos/valley-900.webp 900w, assets/img/photos/valley-1536.webp 1536w" sizes="100vw" alt="The Olifants River winding through sandstone hills at golden hour, with flowering aloes in the foreground." width="1536" height="864" loading="lazy">
  <div class="visit-card">
    <h2 id="visit-title">Watch for the sign at the Olifants River bridge</h2>
    <p>We&rsquo;re at De Wagendrift Boerdery, in the heart of the Loskop Valley. Follow us for the official opening announcement.</p>
    <a class="btn btn--ink" href="visit.html">Plan your visit</a>
  </div>
</section>
</main>
""" + footer() + scripts()


def page_collection():
    real = [w for w in WORKS if not w["sample"]]
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"The collection | {NAME}",
        "url": BASE + "collection.html",
        "isPartOf": {"@id": BASE + "#website"},
        "hasPart": [{"@type": "VisualArtwork", "name": w["title"], "creator": {"@type": "Person", "name": w["artist"]}, "dateCreated": w["year"], "image": BASE + src(w, -1)} for w in real],
    }
    h = head(
        f"The Collection | {NAME}",
        "Original paintings and drawings by Lizette Nel and Jeanne Barnes Tosen at Aloe House Art Gallery in the Loskop Valley. See each work on the wall and enquire on WhatsApp.",
        "collection.html",
        og="collection",
        ld=ld,
    )
    items = ""
    for w in WORKS:
        kind = "sample" if w["sample"] else w["artist"].split()[0].lower()
        items += (
            f'<figure class="piece" data-kind="{kind}" style="--ar:{w["ratio"]}">'
            + framed(w, "(max-width: 599px) 46vw, (max-width: 1099px) 30vw, 24vw")
            + f"<figcaption>{label(w, 'label--plain')}</figcaption></figure>\n"
        )
    return h + header("collection") + f"""<main id="main" class="page">
<header class="page-head">
  <h1>The collection</h1>
  <p>Original work by local talent. The opening collection is still being hung, so sample works fill the wall for now. Those are marked clearly on each label.</p>
</header>
<div class="filters" role="group" aria-label="Filter the collection">
  <button class="chip" type="button" data-filter="all" aria-pressed="true">All works</button>
  <button class="chip" type="button" data-filter="lizette" aria-pressed="false">Lizette Nel</button>
  <button class="chip" type="button" data-filter="jeanne" aria-pressed="false">Jeanne Barnes Tosen</button>
  <button class="chip" type="button" data-filter="sample" aria-pressed="false">Sample artwork</button>
</div>
<div class="salon" id="salon">
{items}</div>
<p class="empty" id="salon-empty" hidden>No works match this filter yet. <button class="link" type="button" data-filter="all">Show all works</button></p>
<section class="page-cta">
  <h2>Seen something you love?</h2>
  <p>Ask about availability and prices, or arrange to see a work in person.</p>
  <a class="btn" href="{wa("Hello Aloe House, I would like to know more about your collection.")}" target="_blank" rel="noopener">{icon("whatsapp-logo")}WhatsApp us</a>
</section>
</main>
""" + footer() + scripts()


def page_artist(slug, name, first, title, desc, face, face_dims, quote_html, paras, works, other_slug, other_name):
    ld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": name,
        "jobTitle": "Artist",
        "image": BASE + f"assets/img/photos/{slug}.webp",
        "url": BASE + f"{slug}.html",
        "affiliation": {"@type": "ArtGallery", "name": NAME, "url": BASE},
    }
    h = head(title, desc, f"{slug}.html", og=slug, og_alt=f"{name} at {NAME}", ld=ld)
    hung = "".join(
        f'<figure class="piece piece--big" style="--ar:{BY[s]["ratio"]}">{framed(BY[s], "(max-width: 1023px) 90vw, 46vw")}<figcaption>{label(BY[s], "label--plain")}</figcaption></figure>'
        for s in works
    )
    body = "".join(f"<p>{p}</p>" for p in paras)
    return h + header("artists") + f"""<main id="main" class="page">
<section class="bio">
  <div class="bio__face"><img src="assets/img/photos/{slug}.webp" alt="{e(name)}" {face_dims} fetchpriority="high"></div>
  <div class="bio__text">
    <p class="bio__kicker">Artist at {NAME}</p>
    <h1>{e(name)}</h1>
    {quote_html}
    {body}
    <div class="cta-row">
      <a class="btn" href="{wa(f"Hello Aloe House, I would like to know more about {name}'s work.")}" target="_blank" rel="noopener">{icon("whatsapp-logo")}Ask about {e(first)}&rsquo;s work</a>
    </div>
  </div>
</section>
<section class="bio-works" aria-labelledby="works-title">
  <h2 id="works-title">On the wall</h2>
  <div class="bio-works__grid">{hung}</div>
  <p class="bio-works__more">More of {e(first)}&rsquo;s work will arrive with the opening collection.</p>
</section>
<section class="exhibit-note">
  <h2>Kranspoort Kunsuitstalling, November 2026</h2>
  <p>Come and discover {e(first)}&rsquo;s work in person at the exhibition.</p>
  <a class="link" href="{wa("Hello Aloe House, please send me the details of the Kranspoort Kunsuitstalling.")}" target="_blank" rel="noopener">Ask about the exhibition</a>
</section>
<p class="next-artist">Next artist: <a class="link" href="{other_slug}.html">{e(other_name)}</a></p>
</main>
""" + footer() + scripts()


def page_visit():
    h = head(
        f"Visit | {NAME}, Loskop Valley",
        "Find Aloe House Art Gallery at De Wagendrift Boerdery in the Loskop Valley near Groblersdal. Watch for the sign at the Olifants River bridge. Opening soon.",
        "visit.html",
        og="visit",
        ld=GALLERY_LD,
    )
    return h + header("visit") + f"""<main id="main" class="page">
<section class="visit-hero">
  <img src="assets/img/photos/valley-1536.webp" srcset="assets/img/photos/valley-900.webp 900w, assets/img/photos/valley-1536.webp 1536w" sizes="100vw" alt="The Olifants River winding through sandstone hills at golden hour, with flowering aloes in the foreground." width="1536" height="864" fetchpriority="high">
  <div class="visit-hero__copy">
    <h1>Visit Aloe House</h1>
    <p>A place where art, creativity and nature come together, in the heart of the Loskop Valley.</p>
  </div>
</section>
<section class="visit-grid">
  <div class="visit-info">
    <h2>Finding us</h2>
    <p>Watch for the Aloe House sign as you cross the Olifants River bridge. The gallery is at De Wagendrift Boerdery, near Groblersdal.</p>
    <dl class="facts">
      <div><dt>Address</dt><dd>De Wagendrift Boerdery, Loskop Valley, Groblersdal, South Africa</dd></div>
      <div><dt>Phone and WhatsApp</dt><dd><a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a></dd></div>
      <div><dt>Opening</dt><dd>Opening soon. The date and hours will be announced on <a href="{FB}" target="_blank" rel="noopener">our Facebook page</a>.</dd></div>
    </dl>
    <div class="cta-row">
      <a class="btn" href="{MAPS}" target="_blank" rel="noopener">{icon("navigation-arrow")}Open in Google Maps</a>
    </div>
  </div>
  <form class="enquiry" id="enquiry" novalidate>
    <h2>Send us a message</h2>
    <p>Art lover, collector, or simply curious, we&rsquo;d love to hear from you. Your message opens in WhatsApp, ready to send.</p>
    <div class="field">
      <label for="f-name">Your name</label>
      <input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-err">
      <p class="field__err" id="f-name-err" hidden>Enter your name so we know who to reply to.</p>
    </div>
    <div class="field">
      <label for="f-about">What is it about?</label>
      <select id="f-about" name="about">
        <option>Visiting the gallery</option>
        <option>A work in the collection</option>
        <option>The Kranspoort Kunsuitstalling</option>
        <option>Showing my work at Aloe House</option>
        <option>Something else</option>
      </select>
    </div>
    <div class="field">
      <label for="f-msg">Your message</label>
      <textarea id="f-msg" name="message" rows="4" required aria-describedby="f-msg-err"></textarea>
      <p class="field__err" id="f-msg-err" hidden>Write a short message before sending.</p>
    </div>
    <button class="btn" type="submit">{icon("whatsapp-logo")}Send on WhatsApp</button>
  </form>
</section>
</main>
""" + footer() + scripts(room=False)


def legal(path, title, desc, h1, body):
    h = head(f"{title} | {NAME}", desc, path, ld=None)
    return h + header("legal") + f"""<main id="main" class="page legal">
<h1>{h1}</h1>
<p class="legal__date">Last updated {UPDATED}</p>
{body}
</main>
""" + footer() + scripts(room=False)


def page_privacy():
    body = f"""
<p>This policy explains how {NAME} ("we", "us") collects, uses and protects personal information when you use this website or contact us, in line with the Protection of Personal Information Act 4 of 2013 (POPIA).</p>
<h2>Who we are</h2>
<dl class="facts">
  <div><dt>Business</dt><dd>{NAME}</dd></div>
  <div><dt>Address</dt><dd>De Wagendrift Boerdery, Loskop Valley, Groblersdal, South Africa</dd></div>
  <div><dt>Phone and WhatsApp</dt><dd><a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a></dd></div>
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
<p>Under POPIA you may ask whether we hold your personal information, ask for a copy, ask us to correct or delete it, and object to how we use it. To do so, contact us on <a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a>.</p>
<p>If you are unhappy with how we handled your information, you may complain to the Information Regulator of South Africa at <a href="https://inforegulator.org.za/" target="_blank" rel="noopener">inforegulator.org.za</a>.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The date at the top shows when it last changed.</p>
"""
    return legal("privacy.html", "Privacy Policy", f"How {NAME} collects, uses and protects your personal information under POPIA.", "Privacy policy", body)


def page_terms():
    body = f"""
<p>These terms apply when you use this website. By using it, you agree to them. If you buy a work from us, these terms apply together with anything we agree with you in writing.</p>
<h2>About this website</h2>
<p>This website is run by {NAME}, De Wagendrift Boerdery, Loskop Valley, Groblersdal, South Africa. You can reach us on <a href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a>.</p>
<h2>Sample artwork and photographs</h2>
<p>The gallery is preparing to open. Works marked "Sample artwork" are placeholders that show how the collection will be presented. They are not by the gallery&rsquo;s artists and are not for sale. Room and landscape photographs are illustrative and may not show the actual gallery or farm.</p>
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
    return legal("terms.html", "Terms of Use", f"The terms for using the {NAME} website, including copyright, sample artwork and availability.", "Terms of use", body)


def page_404():
    h = head(f"Page not found | {NAME}", "This page could not be found.", "404.html", robots="noindex").replace("<head>\n", '<head>\n<base href="/Aloe-House-Art-Gallery/">\n', 1)
    return h + header("404") + f"""<main id="main" class="page not-found">
<span class="frame f-gilt not-found__frame" aria-hidden="true"><span></span></span>
<h1>This wall is empty</h1>
<p>The page you were looking for isn&rsquo;t here. It may have moved, or the link may be wrong.</p>
<div class="cta-row"><a class="btn" href="index.html">Back to the gallery</a><a class="btn btn--ghost" href="collection.html">See the collection</a></div>
</main>
""" + footer() + scripts(room=False)


PAGES = {
    "index.html": page_home,
    "collection.html": page_collection,
    "lizette-nel.html": lambda: page_artist(
        "lizette-nel", "Lizette Nel", "Lizette",
        f"Lizette Nel, Artist | {NAME}",
        "Lizette Nel paints striking portraits with earthy colour, soft texture and close detail. Discover her work at Aloe House Art Gallery in the Loskop Valley.",
        None, 'width="556" height="584"',
        '<p class="artist__quote artist__quote--big"><span lang="af">&ldquo;Ek is &rsquo;n mens van die aarde.&rdquo;</span><span class="artist__en">I am a person of the earth.</span></p>',
        [
            "Lizette&rsquo;s love of nature, people and life runs through every work. With earthy colour, soft texture and a fine eye for detail, she tells stories that go much deeper than the eye can see.",
            "Her art is a celebration of faith, family, belonging and the quiet beauty hidden all around us. Art that isn&rsquo;t only seen, but felt.",
        ],
        ["lizette-portrait", "lizette-graphite"], "jeanne-barnes-tosen", "Jeanne Barnes Tosen"),
    "jeanne-barnes-tosen.html": lambda: page_artist(
        "jeanne-barnes-tosen", "Jeanne Barnes Tosen", "Jeanne",
        f"Jeanne Barnes Tosen, Artist | {NAME}",
        "Jeanne Barnes Tosen paints colourful still lifes, wildlife portraits and scenes of the platteland. Discover her work at Aloe House Art Gallery in the Loskop Valley.",
        None, 'width="588" height="592"',
        '<p class="artist__quote artist__quote--big"><span lang="af">Waar kleur, natuur en nostalgie ontmoet.</span><span class="artist__en">Where colour, nature and nostalgia meet.</span></p>',
        [
            "Jeanne captures the beauty of everyday life with every brushstroke. From colourful still lifes and wildlife portraits to the quiet simplicity of the platteland, her paintings tell stories that make you stop and look.",
            "With a fine feel for light, shadow and composition, she brings each subject to life with a touch of emotion and nostalgia.",
        ],
        ["jeanne-bushbabies"], "lizette-nel", "Lizette Nel"),
    "visit.html": page_visit,
    "privacy.html": page_privacy,
    "terms.html": page_terms,
    "404.html": page_404,
}

for name, fn in PAGES.items():
    html = fn()
    bad = [c for c in ("—", "–") if c in html]
    if bad:
        raise SystemExit(f"{name} contains a banned dash")
    (ROOT / name).write_text(html, encoding="utf8", newline="\n")

index = [p for p in PAGES if p != "404.html"]
priority = {"index.html": "1.0", "collection.html": "0.9", "lizette-nel.html": "0.8", "jeanne-barnes-tosen.html": "0.8", "visit.html": "0.8"}
urls = "\n".join(
    f"<url><loc>{BASE}{'' if p == 'index.html' else p}</loc><lastmod>{ISO}</lastmod><priority>{priority.get(p, '0.3')}</priority></url>" for p in index
)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding="utf8", newline="\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf8", newline="\n")
manifest = {
    "name": NAME, "short_name": "Aloe House", "description": f"{TAGLINE}. Original art in the Loskop Valley.",
    "start_url": "./", "scope": "./", "display": "standalone", "background_color": GREEN, "theme_color": GREEN,
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
(ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf8", newline="\n")
print("built", len(PAGES), "pages")

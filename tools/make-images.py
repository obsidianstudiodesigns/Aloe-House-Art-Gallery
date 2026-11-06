"""Turn the gallery's Facebook images and the generated room photos and sample art into web assets.
Run from anywhere: python tools/make-images.py (needs Pillow and numpy)."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
FB = ROOT / "_source/facebook"
GEN = ROOT / "_source/gen"
WORKS = ROOT / "assets/img/works"
PHOTOS = ROOT / "assets/img/photos"
BRAND = ROOT / "assets/img/brand"
for d in (WORKS, PHOTOS, BRAND):
    d.mkdir(parents=True, exist_ok=True)


def rgb(p):
    return Image.open(p).convert("RGB")


def save_sizes(im, out, stem, widths, q=82):
    """Write one .webp per width."""
    for w in widths:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(out / f"{stem}-{w}.webp", quality=q, method=6)


def persp(im, corners, size):
    """Square up a work photographed at an angle. corners: TL, TR, BR, BL in the source image."""
    (w, h) = size
    dst = [(0, 0), (w, 0), (w, h), (0, h)]
    A = []
    for (x, y), (u, v) in zip(dst, corners):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = np.array(corners, dtype=float).reshape(8)
    c = np.linalg.solve(np.array(A, dtype=float), b)
    return im.transform(size, Image.PERSPECTIVE, c, Image.BICUBIC)


# Real work, from the gallery's own Facebook page
painting = rgb(FB / "aloehr-e.jpg")
save_sizes(painting, WORKS, "lizette-portrait", [1200, 720, 420], 84)
W, H = painting.size
detail_aloe = painting.crop((int(.30 * W), int(.40 * H), int(1.0 * W), int(.80 * H)))
save_sizes(detail_aloe, PHOTOS, "detail-aloe", [1000, 600], 84)
detail_face = painting.crop((int(.38 * W), 0, W, int(.34 * H)))
save_sizes(detail_face, PHOTOS, "detail-face", [880, 500], 84)

poster = rgb(FB / "aloehr-a.jpg")
graphite = persp(poster, [(76, 839), (426, 815), (438, 1073), (92, 1094)], (700, 512))
graphite = graphite.filter(ImageFilter.UnsharpMask(1.4, 50, 2))
save_sizes(graphite, WORKS, "lizette-graphite", [700, 420], 84)
bush = persp(poster, [(800, 842), (1124, 864), (1096, 1088), (777, 1064)], (720, 500))
bush = bush.filter(ImageFilter.UnsharpMask(1.4, 50, 2))
save_sizes(bush, WORKS, "jeanne-bushbabies", [720, 420], 84)

for stem, box in {"lizette-nel": (22, 372, 300, 664), "jeanne-barnes-tosen": (905, 374, 1199, 670)}.items():
    p = poster.crop(box)
    p = p.resize((p.width * 2, p.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 45, 2))
    p.save(PHOTOS / f"{stem}.webp", quality=84, method=6)

# Generated room photography and sample art


def grade(im):
    """Pull the olive shadows of the generated room towards the logo's bottle green."""
    a = np.asarray(im, dtype=float)
    lum = a.mean(axis=2, keepdims=True)
    k = np.clip(1 - lum / 110, 0, 1)
    gain = np.array([.72, 1.10, 1.02])
    a = a * (1 + (gain - 1) * k)
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8"))


wall = grade(rgb(GEN / "wall-wide.png"))
wall.save(PHOTOS / "wall-wide.webp", quality=82, method=6)
wall.resize((1100, 619), Image.LANCZOS).save(PHOTOS / "wall-wide-1100.webp", quality=78, method=6)
tall = grade(rgb(GEN / "wall-tall.png"))
tall.save(PHOTOS / "wall-tall.webp", quality=80, method=6)
save_sizes(rgb(GEN / "valley.png"), PHOTOS, "valley", [1536, 900], 80)
save_sizes(rgb(GEN / "aloe-macro.png"), PHOTOS, "aloe-macro", [1280, 720], 80)

for stem in ("aloe-dusk", "river", "kudu", "citrus", "strata", "roller", "thorn", "kloof"):
    save_sizes(rgb(GEN / f"s-{stem}.png"), WORKS, f"sample-{stem}", [1000, 560], 82)

# A tile of the same plaster, so the whole site is painted the colour of the hero wall.
arr = np.asarray(wall, dtype=float)
hh, ww, _ = arr.shape
patch = arr[int(.08 * hh):int(.08 * hh) + 420, int(.46 * ww):int(.46 * ww) + 420]
print("wall median", np.median(patch.reshape(-1, 3), axis=0))
blur = np.asarray(Image.fromarray(patch.astype("uint8")).filter(ImageFilter.GaussianBlur(50)), dtype=float)
flat = (patch - blur) * .42  # keep a quiet version of the trowel marks, drop the light falloff
n = flat.shape[0]
ramp = np.minimum(np.arange(n), np.arange(n)[::-1]) / (n * .22)
ramp = np.clip(ramp, 0, 1)
wx, wy = ramp[None, :, None], ramp[:, None, None]
rolled = np.roll(np.roll(flat, n // 2, 0), n // 2, 1)
w = wx * wy  # cross-fade the edges into a half-offset copy so the tile repeats without a seam or a mirror pattern
mix = flat * w + rolled * (1 - w)
tile = np.clip(mix + np.array([20, 41, 28]), 0, 255)
Image.fromarray(tile.astype("uint8")).save(PHOTOS / "plaster.webp", quality=82, method=6)

# The same polished floor as the hero, mirrored so it runs the whole length of the wall.
floor = np.asarray(wall, dtype=float)[int(.855 * hh):int(.985 * hh), int(.42 * ww):int(.86 * ww)]
floor = np.concatenate([floor, floor[:, ::-1]], axis=1)
Image.fromarray(floor.astype("uint8")).save(PHOTOS / "floor.webp", quality=70, method=6)
print("floor", floor.shape)

# Brand: the gallery's round logo and the aloe crest
logo = rgb(FB / "aloehr-f.jpg")
S = logo.width
mask = Image.new("L", (S * 2, S * 2), 0)
ImageDraw.Draw(mask).ellipse((10, 10, S * 2 - 10, S * 2 - 10), fill=255)
mask = mask.resize((S, S), Image.LANCZOS)
ring = logo.copy()
ring.putalpha(mask)
for s in (640, 320):
    ring.resize((s, s), Image.LANCZOS).save(BRAND / f"logo-round-{s}.webp", quality=88, method=6)
ring.resize((512, 512), Image.LANCZOS).save(BRAND / "logo-round.png", optimize=True)

poster_d = rgb(FB / "aloehr-d.jpg")
crest = poster_d.crop((532, 82, 730, 296))
c = np.asarray(crest, dtype=float)
bg = np.median(np.concatenate([c[:8].reshape(-1, 3), c[:, :8].reshape(-1, 3)]), axis=0)
# Only what is lighter than the wall counts as the crest, so the poster's soft shadow stays behind.
alpha = np.clip((c.mean(axis=2) - bg.mean() - 20) / 42, 0, 1)
rgba = np.dstack([c, alpha * 255]).astype("uint8")
crest_img = Image.fromarray(rgba, "RGBA")
crest_img = crest_img.resize((crest_img.width * 2, crest_img.height * 2), Image.LANCZOS)
crest_img = crest_img.crop(crest_img.getbbox())
crest_img.save(BRAND / "crest.webp", quality=90, method=6)
crest_img.save(BRAND / "crest.png", optimize=True)
print("crest", crest_img.size)

# Favicons: crest on bottle green inside a gold ring.
GREEN, GOLD = (17, 50, 31), (205, 165, 92)


def icon(size, ring_on=True, pad=.17, safe=False):
    k = 4
    s = size * k
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if safe:
        d.rectangle((0, 0, s, s), fill=GREEN + (255,))
    else:
        d.ellipse((0, 0, s - 1, s - 1), fill=GREEN + (255,))
        if ring_on:
            t = max(k, int(s * .035))
            d.ellipse((t, t, s - 1 - t, s - 1 - t), outline=GOLD + (255,), width=t)
    box = int(s * (1 - pad * 2))
    cw, ch = crest_img.size
    r = min(box / cw, box / ch)
    ci = crest_img.resize((int(cw * r), int(ch * r)), Image.LANCZOS)
    if size <= 48:
        ci = ImageEnhance.Contrast(ci).enhance(1.25)
        ci = ImageEnhance.Color(ci).enhance(1.3)
    im.alpha_composite(ci, ((s - ci.width) // 2, (s - ci.height) // 2))
    return im.resize((size, size), Image.LANCZOS)


icon(180, safe=True, pad=.14).convert("RGB").save(ROOT / "apple-touch-icon.png", optimize=True)
icon(192).save(ROOT / "icon-192.png", optimize=True)
icon(512).save(ROOT / "icon-512.png", optimize=True)
icon(512, safe=True, pad=.22).convert("RGB").save(ROOT / "icon-maskable-512.png", optimize=True)
icon(96).save(ROOT / "favicon-96.png", optimize=True)
icon(48, pad=.11).save(ROOT / "favicon-48.png", optimize=True)
icon(32, pad=.09).save(ROOT / "favicon-32.png", optimize=True)
icon(16, ring_on=False, pad=.05).save(ROOT / "favicon-16.png", optimize=True)
icon(48, pad=.11).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


def sheet(paths, out, h=300):
    ims = [Image.open(p).convert("RGB") for p in paths]
    th = [i.resize((int(i.width * h / i.height), h)) for i in ims]
    s = Image.new("RGB", (sum(t.width for t in th) + 8 * len(th), h), "#333")
    x = 0
    for t in th:
        s.paste(t, (x, 0))
        x += t.width + 8
    s.save(out, quality=85)


sheet([WORKS / "lizette-graphite-700.webp", WORKS / "jeanne-bushbabies-720.webp", PHOTOS / "lizette-nel.webp",
       PHOTOS / "jeanne-barnes-tosen.webp", BRAND / "crest.png", PHOTOS / "detail-aloe-600.webp", PHOTOS / "plaster.webp"],
      ROOT / "_source/check.jpg")
ic = Image.new("RGB", (480, 120), "#555")
x = 10
for f, s in [("favicon-16.png", 16), ("favicon-32.png", 32), ("favicon-48.png", 48), ("favicon-96.png", 96), ("apple-touch-icon.png", 110), ("icon-maskable-512.png", 110)]:
    i = Image.open(ROOT / f).convert("RGBA").resize((s, s), Image.LANCZOS)
    ic.paste(i, (x, 5), i)
    x += s + 12
ic.resize((960, 240), Image.NEAREST).save(ROOT / "_source/check-ic.png")

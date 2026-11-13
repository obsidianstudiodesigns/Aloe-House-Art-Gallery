"""Turn the client's photos in "Art Gallery/" into web images.
Run: python tools/make-client-images.py (needs Pillow). Works are listed in tools/collection.json ("source" is the file name)."""
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Art Gallery"
WORKS = ROOT / "assets/img/works"
PHOTOS = ROOT / "assets/img/photos"
WORKS.mkdir(parents=True, exist_ok=True)
PHOTOS.mkdir(parents=True, exist_ok=True)

FOLDER = {"Lizette Nel": "Lizette Nel", "Jeanne H Barnes": "Jeanne H Barnes"}


def load(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def sizes(im, out, stem, widths, q=84):
    made = []
    for w in widths:
        if w > im.width:
            continue
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(out / f"{stem}-{w}.webp", quality=q, method=6)
        made.append(w)
    if im.width not in made and (not made or im.width < widths[-1]):
        im.save(out / f"{stem}-{im.width}.webp", quality=q, method=6)
        made.append(im.width)
    return sorted(made)


works = json.loads((ROOT / "tools/collection.json").read_text(encoding="utf8"))
for w in works:
    im = load(SRC / FOLDER[w["artist"]] / w["source"])
    w["widths"] = sizes(im, WORKS, w["image"], [420, 720, 1200])
    w["ratio"] = round(im.width / im.height, 4)
    print(w["slug"], im.size, w["widths"], w["ratio"])
(ROOT / "tools/collection.json").write_text(json.dumps(works, indent=2, ensure_ascii=False) + "\n", encoding="utf8")

# Details for the artist cards on the home page
goat = load(SRC / "Lizette Nel/WhatsApp Image 2026-11-13 at 13.05.26.jpeg")
W, H = goat.size
sizes(goat.crop((0, int(H * .02), W, int(H * .82))), PHOTOS, "detail-goat", [600, 1000, 1254])

# The gallery and the farm
gal = SRC / "The Gallery"
sizes(load(gal / "WhatsApp Image 2026-11-13 at 13.06.58 (2).jpeg"), PHOTOS, "gallery-building", [900, 1448], 82)
sizes(load(gal / "WhatsApp Image 2026-11-13 at 13.06.57.jpeg"), PHOTOS, "farm-aloes", [900, 1448], 82)

# Artist portraits, from the top of their exhibition posters
for stem, file, box in [
    ("jeanne-h-barnes", "WhatsApp Image 2026-11-13 at 13.06.59 (1).jpeg", (300, 0, 860, 560)),
    ("lizette-nel", "WhatsApp Image 2026-11-13 at 13.06.59.jpeg", (330, 0, 890, 560)),
]:
    p = load(gal / file).crop(box)
    p.save(PHOTOS / f"{stem}.webp", quality=86, method=6)
    print(stem, p.size)

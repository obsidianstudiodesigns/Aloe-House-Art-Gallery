"""Render the WhatsApp and social preview images (1200x630 JPEG) with headless Chrome. Run after make-images.py."""
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/og"
OUT.mkdir(parents=True, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CARDS = {
    "home": ("works/lizette-portrait-720.webp", .704, "gilt", "Aloe House Art Gallery", "Where nature meets art", "Original art and local talent in the Loskop Valley"),
    "collection": ("works/jeanne-bushbabies-720.webp", 1.44, "gilt", "The collection", "Aloe House Art Gallery", "Original work by Lizette Nel and Jeanne Barnes Tosen"),
    "lizette-nel": ("works/lizette-portrait-720.webp", .704, "gilt", "Lizette Nel", "Artist at Aloe House Art Gallery", "Earthy colour, soft texture, close detail"),
    "jeanne-barnes-tosen": ("works/jeanne-bushbabies-720.webp", 1.44, "gilt", "Jeanne Barnes Tosen", "Artist at Aloe House Art Gallery", "Still lifes, wildlife and the platteland"),
    "visit": ("works/lizette-graphite-700.webp", 1.367, "black", "Visit Aloe House", "De Wagendrift Boerdery, Loskop Valley", "Watch for the sign at the Olifants River bridge"),
}

TEMPLATE = """<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:G;src:url("{root}/assets/fonts/Gloock-normal.woff2")}}
@font-face{{font-family:I;src:url("{root}/assets/fonts/InstrumentSans-normal.woff2");font-weight:400 700}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#14291c}}
.w{{position:absolute;left:0;bottom:0;width:1200px;height:675px;object-fit:cover}}
.f{{position:absolute;left:{left}px;top:{top}px;width:{w}px;padding:11px;background:linear-gradient(135deg,#8d6b2d,#e4c67e 22%,#a98238 44%,#f1dc9f 66%,#93702f 84%,#d2b064);box-shadow:14px 22px 38px rgba(3,10,6,.6)}}
.f.black{{padding:7px;background:#201e16}}
.f img{{display:block;width:100%;box-shadow:0 0 0 2px rgba(50,32,8,.75)}}
.t{{position:absolute;left:{tx}px;right:150px;top:0;bottom:60px;display:flex;flex-direction:column;justify-content:center;color:#f6efe0;font-family:I}}
.c{{width:74px;margin-bottom:18px}}
h1{{font:400 {size}px/1.03 G;margin:0 0 10px}}
.s{{font:600 28px/1.25 I;color:#d6b470;margin-bottom:8px}}
.p{{font:400 23px/1.35 I;color:#e4e6d6;max-width:500px}}
.d{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,31,21,0) 34%,rgba(14,31,21,.55) 60%,rgba(14,31,21,.3) 100%)}}
</style>
<img class="w" src="{root}/assets/img/photos/wall-wide.webp"><div class="d"></div>
<div class="f {frame}"><img src="{root}/assets/img/{img}"></div>
<div class="t"><img class="c" src="{root}/assets/img/brand/crest.png"><h1>{title}</h1><div class="s">{sub}</div><div class="p">{para}</div></div>
"""

root = ROOT.as_uri()
with tempfile.TemporaryDirectory() as td:
    for slug, (img, ratio, frame, title, sub, para) in CARDS.items():
        if ratio < 1:
            w, top = 340, 40
            h_est = w / ratio
            top = max(14, int((630 - h_est) / 2) - 16)
            left, tx = 110, 520
        else:
            w = 420
            top = int((630 - w / ratio) / 2) - 16
            left, tx = 60, 540
        size = 66 if len(title) > 18 else 76
        html = TEMPLATE.format(root=root, left=left, top=top, w=w, tx=tx, frame=frame, img=img, title=title, sub=sub, para=para, size=size)
        src = Path(td) / f"{slug}.html"
        src.write_text(html, encoding="utf8")
        png = Path(td) / f"{slug}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--user-data-dir={td}/profile", "--allow-file-access-from-files", "--virtual-time-budget=4000",
                        "--window-size=1200,630", f"--screenshot={png}", src.as_uri()], check=True, capture_output=True, timeout=120)
        im = Image.open(png).convert("RGB")
        if im.size != (1200, 630):
            im = im.crop((0, 0, 1200, 630))
        im.save(OUT / f"{slug}.jpg", quality=84, optimize=True, progressive=True)
        print(slug, im.size, (OUT / f"{slug}.jpg").stat().st_size // 1024, "KB")

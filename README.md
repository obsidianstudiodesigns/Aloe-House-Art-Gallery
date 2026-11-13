# Aloe House Art Gallery

Website for Aloe House Art Gallery: original art by Lizette Nel and Jeanne H Barnes at De Wagendrift Boerdery in the Loskop Valley, near Groblersdal. Where nature meets art.

Live: https://obsidianstudiodesigns.github.io/Aloe-House-Art-Gallery/ (English) and https://obsidianstudiodesigns.github.io/Aloe-House-Art-Gallery/af/ (Afrikaans)

Static site on GitHub Pages from `main`. The Python tools only run on your machine.

## Add or change artworks
1. Put the client's photo in `Art Gallery/<artist folder>/` (kept out of the repository).
2. Add the work to `tools/collection.json`: `source` (file name), `image` (web file name), `artist`, `year`, `frame` (`gilt`, `oak`, `black`, `mat`, `float`), and an `en` and `af` block with `title`, `medium` and `alt`. A `wall` entry hangs it on the home page wall (`h` is its height, `y` nudges it up or down).
3. Run `python tools/make-client-images.py`, then `python tools/build.py`, then commit and push.

The artwork titles are descriptive working titles until the artists confirm their own.

## Words
Every page is written in English and Afrikaans in `tools/build.py` through `t("English", "Afrikaans")`. The Afrikaans pages are built into `af/`. Phone, WhatsApp, Facebook and map links are constants at the top of the file. Remove the Kranspoort sections when the exhibition has passed.

## Other images
`tools/make-images.py` (logo, favicons, the illustrated room behind the hero painting) and `tools/make-og.py` (WhatsApp and social previews in both languages) need the originals in `_source/`.

Site by [Obsidian Studio Designs](https://obsidianstudiodesigns.co.za/).

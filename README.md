# Aloe House Art Gallery

Website for Aloe House Art Gallery: original art and local talent at De Wagendrift Boerdery in the Loskop Valley, near Groblersdal. Where nature meets art.

Live: https://obsidianstudiodesigns.github.io/Aloe-House-Art-Gallery/

Static site, hosted on GitHub Pages from `main`. The Python tools only run on your machine.

## Load the real collection
1. Put a photo of each work in `assets/img/works/` as `.webp`, named `<image>-<width>.webp` (for example `kudu-1000.webp` and `kudu-560.webp`).
2. Edit `tools/collection.json`. Set `"sample": false`, and fill in `artist`, `year`, `medium`, `ratio` (width divided by height), `frame` (`gilt`, `oak`, `black`, `mat`, `float`) and `alt`. A `wall` entry hangs the work on the home page wall (`h` is its height, `y` nudges it up or down).
3. When no samples are left, remove the note in `footer()` in `tools/build.py` and the sample paragraphs on the collection page and in the terms.
4. Run `python tools/build.py`, then commit and push.

## Update details
Phone, WhatsApp, Facebook and map links are constants at the top of `tools/build.py`. Opening date and hours go in `page_visit()`. Remove the Kranspoort section from `page_home()` and `page_artist()` when the exhibition has passed.

## Rebuild images
`python tools/make-images.py` and `python tools/make-og.py` need the originals in `_source/`, which is kept out of the repository.

Site by [Obsidian Studio Designs](https://obsidianstudiodesigns.co.za/).

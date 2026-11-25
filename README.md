# Evie Ceccon · Children's book illustrator

Portfolio site for Evelys "Evie" Ceccon, built from her Behance profile (https://www.behance.net/eviececcon).

- `index.html`: the whole site (painted cover, books gallery with a page-by-page book viewer, about, themes, contact).
- `i18n.js`: all site text in English, Portuguese, Spanish, Italian, German and French. English is the default; the choice is remembered and can be linked with `?lang=pt` (or `es`, `it`, `de`, `fr`).
- `assets.json`: every book and every illustration from her Behance (12 books, 141 images). `data.js` is generated from it.
- `assets/`: web-ready copies of the illustrations, downloaded by the **Fetch illustrations from Behance** workflow (`tools/fetch_images.py`). If a file is missing, the page falls back to Behance's CDN.

## Adding a book

Add an entry to `assets.json` (Behance project id and path, cover id, page file names), regenerate `data.js` with the same content (`window.EVIE = <assets.json>;`), and push. The fetch workflow downloads the new images.

## Deploy

GitHub Pages via `.github/workflows/pages.yml`. In Settings → Pages set Source to "GitHub Actions". Every push to `main` publishes the site.

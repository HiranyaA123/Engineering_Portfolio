# Hiranya Agarwal, engineering portfolio

Static portfolio site for Hiranya Agarwal, a Mechanical Engineering (Honours) student at UNSW working across robotics, autonomous systems, space hardware and software.

No build step, no dependencies. Every page is hand written HTML and CSS with about 30 lines of progressive enhancement JavaScript.

## Local preview

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>. Opening `index.html` directly from the file system also works, but the `404.html` root relative links will not.

## Structure

```
index.html                  landing page
404.html                    error page
projects/                   six case study sheets, 01 to 06
assets/css/base.css         design tokens, typography, shared components
assets/css/home.css         landing page layout
assets/css/case.css         case study layout
assets/js/site.js           current year, active nav section, photo lightbox
assets/img/vex/             robot and team photographs (600 / 1000 / 1600 wide)
assets/img/primo-firle/     real product screenshots (800 / 1280 wide)
assets/docs/                the public resume PDF
_local/                     not deployed, not tracked (see .gitignore)
DESIGN-RULES.md             the ruleset the site is built against
DESIGN-NOTES.md             decisions made under those rules
```

## Design

The site follows `DESIGN-RULES.md`. The direction is a technical drawing sheet: drafting paper ground, graphite ink, one oxide accent, and a title block carried on every page. `DESIGN-NOTES.md` records the palette, the type pairing, the signature element and the deliberate departures.

Change design tokens in `assets/css/base.css` under `:root`. Colour, type scale, spacing, radius and motion all live there, so a change propagates everywhere.

## Deployment

`.github/workflows/deploy-pages.yml` publishes the repository root to GitHub Pages on every push to `main`. In the repository settings, set **Pages > Build and deployment > Source** to **GitHub Actions**.

Files under `_local/` are gitignored, so working documents and archives stay out of the published site.

## Images

Photographs are pre-sized into a responsive set rather than resized in the browser. Each one ships at 600, 1000 and 1600 pixels wide with `srcset` and `sizes`, so a phone downloads roughly 60KB where a desktop downloads 300KB, and the full size file is only fetched if a visitor opens the lightbox.

To add a photograph, generate the three widths, then reference them with the shared `.photo` component:

```bash
python -c "from PIL import Image; im=Image.open('new.jpg').convert('RGB'); [im.resize((w, round(im.height*w/im.width))).save(f'assets/img/vex/slug-{w}.jpg','JPEG',quality=80,optimize=True,progressive=True) for w in (600,1000,1600)]"
```

## Social previews

`og:image` is set to a relative path on every page. Once the site has a final domain, switch those to absolute URLs, since some link scrapers will not resolve a relative one.

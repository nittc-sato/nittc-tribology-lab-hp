# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **static HTML/CSS/vanilla-JS website** (the Sato Group / Tribology
Laboratory site). There is no backend, database, API, bundler, or `package.json`. Nothing
needs to be compiled or built to run it.

### Run the site (development)
Serve the repo root as static files and open it in a browser:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

Any static file server works. `python3` is the only runtime needed to serve the site.

### Lint / test / build
There is **no lint, no automated test suite, and no build step** for this project — it is
plain static files deployed as-is to GitHub Pages. Do not expect `npm`/`pnpm` scripts or a
Makefile; none exist. "Testing" means opening the pages in a browser and checking navigation
and the JP/EN language toggle.

### Key behavior to verify when testing
- The header has a JP/EN language toggle. Text is stored in `data-ja` / `data-en` attributes
  and swapped by `js/script.js`; the choice is persisted in `localStorage`
  (`tribology-lab-lang`) across pages.
- Navigation is via plain multi-page links (`index.html`, `research.html`, `members.html`,
  `facilities.html`, `publications.html`, `for-students.html`, `access.html`, `news.html`).

### Content-generation utilities (optional)
`_reseachmap/*.py` are offline maintenance scripts to regenerate `publications.html` from a
researchmap JSONL export. They are NOT needed to run the site. `build_publications.py` and
`assemble_publications.py` are Python stdlib-only; `fix_research_bg.py` requires **Pillow**
(installed by the startup update script). See `_reseachmap/README.md`.

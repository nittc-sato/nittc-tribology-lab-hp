# Tribology Laboratory Website

Official website for **Sato Group, Tribology Laboratory**  
Department of Mechanical Engineering, National Institute of Technology, Tokyo College.

Static HTML/CSS/JavaScript site, deployable on **GitHub Pages**.

## File structure

```
index.html          # HOME
research.html       # RESEARCH
members.html        # MEMBER
facilities.html     # FACILITIES
publications.html   # PUBLICATIONS
for-students.html   # FOR STUDENTS
access.html         # ACCESS
news.html           # NEWS
css/style.css
js/script.js
images/             # Photos and placeholders
_references/        # Design reference notes (not published)
```

## Publish on GitHub Pages

1. Create a GitHub repository (e.g. `tribology-lab-hp`).
2. Push this project to the repository root (so `index.html` is at the top level).
3. On GitHub: **Settings → Pages**
   - **Source:** Deploy from a branch
   - **Branch:** `main` (or `master`) / **Folder:** `/ (root)`
4. Save. After a few minutes the site is available at  
   `https://<username>.github.io/<repository>/`

### Custom domain (optional)

In **Settings → Pages**, set a custom domain and add the DNS records GitHub shows.

## Local preview

Open `index.html` in a browser, or use a simple local server:

```bash
# Python 3
python -m http.server 8000
# Then open http://localhost:8000
```

## Language switch (JP / EN)

- Text uses `data-ja` and `data-en` attributes; `js/script.js` swaps content.
- Selected language is stored in `localStorage` (`tribology-lab-lang`) and kept across pages.

## Replace photos

1. Put image files in `images/` (e.g. `hero-lab.jpg`, `facility-afm.jpg`, `member-sato.jpg`).
2. Update the matching `<img src="..." alt="...">` in HTML.
3. Prefer JPG/WebP; keep filenames descriptive. Update `alt` for accessibility.

Placeholder files included:

- `images/placeholder.svg` — general equipment / research images
- `images/placeholder-member.svg` — member portraits

HTML comments mark suggested filenames (e.g. `<!-- Replace with images/hero-lab.jpg -->`).

## Add a member

In `members.html`, copy an `<article class="member-card">...</article>` block inside the appropriate `.member-grid`:

```html
<article class="member-card">
  <div class="member-photo">
    <img src="images/placeholder-member.svg" alt="氏名" width="280" height="280">
  </div>
  <p class="member-name-ja">氏名</p>
  <p class="member-name-en">Romanized Name</p>
</article>
```

Replace `src` and `alt` when a photo is ready.

## Add news

1. **Full list:** In `news.html`, copy a `<li class="news-item">...</li>` block at the **top** of `.news-list` (newest first).
2. **HOME teaser:** Add the same item (or a short version) in `index.html` under the News section.

Fields: `datetime` on `<time>`, category in `.news-category`, title in `<h3>` / `<h2>`, body in `.news-excerpt`. Use `data-ja` / `data-en` for bilingual text.

## Update publications from researchmap

1. Export your profile from [researchmap](https://researchmap.jp/kaisei_sato) as JSONL into `_reseachmap/`.
2. Run:

```bash
python _reseachmap/build_publications.py
python _reseachmap/assemble_publications.py
```

See `_reseachmap/README.md` for details.

To add items manually, edit `publications.html` or regenerate after updating the JSONL export.

## Edit contact / map

- **Email:** `access.html` → `#contact` → `mailto:` link
- **Address / room:** `access.html` → address `<dd>`
- **Google Map:** Replace the `.map-placeholder` `<div>` with an embed `<iframe>` from Google Maps

## Design reference

Layout and tone were informed by an external academic lab site; see `_references/reference-notes.md`. Site assets are original.

## License

Content © Sato Group, Tribology Laboratory. Adjust as needed for your institution’s policies.

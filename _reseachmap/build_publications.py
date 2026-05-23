# -*- coding: utf-8 -*-
"""Generate publications HTML from researchmap JSONL export."""
import json
import html
import re
from pathlib import Path

JSONL = Path(__file__).parent / "rm_researchers20260523-1.jsonl"
OUT = Path(__file__).parent / "publications-sections.html"

CONFERENCE_PUB_KEYWORDS = (
    "leeds-lyon", "wtc", "international conference", "proc.", "symposium",
    "icomat", "nanospec", "stle", "asiatrix", "itc fukuoka", "k-trib",
    "tribology international conference", "jvss", "isss",
)


def esc(s):
    return html.escape(s or "", quote=False)


def pick_lang(d, key, prefer="ja"):
    if not isinstance(d, dict):
        return ""
    block = d.get(key) or {}
    if prefer == "ja":
        return (block.get("ja") or block.get("en") or "").strip()
    return (block.get("en") or block.get("ja") or "").strip()


def authors_str(authors):
    if not authors:
        return ""
    parts = []
    for lang in ("ja", "en"):
        for a in (authors.get(lang) or []):
            n = a.get("name", "")
            if n and n not in parts:
                parts.append(n)
    return " ".join(parts) if len(parts) <= 3 else parts[0]


def year_from(date):
    if not date:
        return ""
    return str(date)[:4]


def pub_citation(m):
    title = pick_lang(m, "paper_title") or pick_lang(m, "book_title")
    authors = authors_str(m.get("authors"))
    pub = pick_lang(m, "publication_name")
    vol = m.get("volume", "")
    num = m.get("number", "")
    sp = m.get("starting_page", "")
    ep = m.get("ending_page", "")
    y = year_from(m.get("publication_date"))
    cite = f"<em>{esc(pub)}</em>" if pub else ""
    if vol:
        cite += f" {esc(vol)}"
        if num:
            cite += f"({esc(num)})"
    if sp and ep:
        cite += f", {esc(sp)}–{esc(ep)}"
    elif sp:
        cite += f", {esc(sp)}"
    doi = (m.get("identifiers") or {}).get("doi", [None])[0]
    doi_link = ""
    if doi:
        for link in m.get("see_also") or []:
            if link.get("label") == "doi":
                doi_link = f' <a href="{esc(link["@id"])}" target="_blank" rel="noopener">DOI</a>'
                break
    return title, authors, cite, y, doi_link


def is_journal_paper(m):
    pt = m.get("published_paper_type", "")
    pub = (pick_lang(m, "publication_name") or "").lower()
    if any(k in pub for k in CONFERENCE_PUB_KEYWORDS):
        return False
    if "予稿集" in pub or "講演会" in pub or "annual meeting" in pub:
        return False
    if pt == "scientific_journal":
        return True
    if pt == "international_conference_proceedings":
        return False
    if m.get("volume") and (
        "トライボロジスト" in pub
        or "tribology online" in pub
        or "tribology letters" in pub
        or "tribology international" in pub
        or "tribology transactions" in pub
        or "cellulose" in pub
        or "wear" in pub
        or "langmuir" in pub
        or "軽金属" in pub
    ):
        return True
    if m.get("referee"):
        if "tribology" in pub or "トライボロジ" in pub or "cellulose" in pub or "wear" in pub:
            return True
    return False


def li_pub_item(title, authors, journal, year, doi_link="", data_ja=None, data_en=None):
    t_ja = data_ja or title
    t_en = data_en or title
    a_attr = ""
    if data_ja and data_en and data_ja != data_en:
        a_attr = f' data-ja="{esc(data_ja)}" data-en="{esc(data_en)}"'
    elif authors:
        a_attr = f' data-ja="{esc(authors)}" data-en="{esc(authors)}"'
    t_attr = ""
    if t_ja != t_en:
        t_attr = f' data-ja="{esc(t_ja)}" data-en="{esc(t_en)}"'
    return f"""            <li class="pub-item">
              <span class="pub-title"{t_attr}>{esc(title)}</span>
              <span class="pub-authors"{a_attr}>{esc(authors)}</span>
              <span class="pub-journal">{journal}</span>
              <span class="pub-year">{esc(year)}</span>{doi_link}
            </li>"""


def main():
    records = []
    with open(JSONL, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    by_type = {}
    for r in records:
        t = r["insert"]["type"]
        by_type.setdefault(t, []).append(r["merge"])

    lines = []

    # Journal papers (published_papers + misc entries that are journal articles)
    journals = [m for m in by_type.get("published_papers", []) if is_journal_paper(m)]
    for m in by_type.get("misc", []):
        if is_journal_paper(m) and m.get("volume"):
            journals.append(m)
    # dedupe by title
    seen = set()
    unique = []
    for m in sorted(journals, key=lambda x: x.get("publication_date", ""), reverse=True):
        t = pick_lang(m, "paper_title")
        if t not in seen:
            seen.add(t)
            unique.append(m)
    journals = unique

    lines.append("          <ul class=\"pub-list\">")
    for m in journals:
        title, authors, cite, y, doi = pub_citation(m)
        lines.append(li_pub_item(title, authors, cite, y, doi))
    lines.append("          </ul>")

    journal_html = "\n".join(lines)

    # Books
    books_html = []
    for m in sorted(by_type.get("books_etc", []), key=lambda x: x.get("publication_date", ""), reverse=True):
        title = pick_lang(m, "book_title")
        authors = authors_str(m.get("authors"))
        pub = pick_lang(m, "publisher")
        y = year_from(m.get("publication_date"))
        books_html.append(
            f'            <li data-ja="{esc(y)}年 — {esc(title)}（{esc(pub)}）{esc(authors)}" '
            f'data-en="{esc(y)} — {esc(title)} ({esc(pub)})">{esc(y)} — {esc(title)}（{esc(pub)}）</li>'
        )

    # Awards
    awards_html = []
    for m in sorted(by_type.get("awards", []), key=lambda x: x.get("award_date", ""), reverse=True):
        name = pick_lang(m, "award_name")
        assoc = pick_lang(m, "association")
        winners = ""
        wblock = m.get("winners") or {}
        if isinstance(wblock, dict):
            wj = wblock.get("ja") or wblock.get("en") or []
            if wj and isinstance(wj[0], dict):
                winners = "，".join(x.get("name", "") for x in wj)
            elif wj:
                winners = str(wj[0])
        d = m.get("award_date", "")
        y, mo = d[:4], d[5:7] if len(d) >= 7 else ""
        label_ja = f"{y}年{mo}月 — {name}（{assoc}）{winners}"
        label_en = f"{y}-{mo} — {pick_lang(m, 'award_name', 'en')} ({pick_lang(m, 'association', 'en')}) {winners}"
        awards_html.append(f'            <li data-ja="{esc(label_ja)}" data-en="{esc(label_en)}">{esc(label_ja)}</li>')

    # Presentations (oral, recent 35)
    pres = by_type.get("presentations", [])
    pres.sort(key=lambda m: m.get("publication_date", ""), reverse=True)
    pres_html = []
    for m in pres[:35]:
        title = pick_lang(m, "presentation_title")
        presenters = ""
        pblock = m.get("presenters") or {}
        if isinstance(pblock, dict):
            pj = pblock.get("ja") or pblock.get("en") or []
            if pj:
                presenters = pj[0].get("name", "") if isinstance(pj[0], dict) else str(pj[0])
        event = pick_lang(m, "event")
        d = m.get("publication_date", "")
        pres_html.append(f"""            <li class="pub-item">
              <span class="pub-title">{esc(title)}</span>
              <span class="pub-authors">{esc(presenters)}</span>
              <span class="pub-journal">{esc(event)} ({esc(d)})</span>
            </li>""")

    # Grants
    grants_html = []
    for m in sorted(by_type.get("research_projects", []), key=lambda x: x.get("from_date", ""), reverse=True):
        title = pick_lang(m, "research_project_title")
        org = pick_lang(m, "offer_organization")
        system = pick_lang(m, "system_name")
        cat = pick_lang(m, "category")
        fd = m.get("from_date", "")
        td = m.get("to_date", "")
        inv = ""
        if m.get("investigators"):
            ij = m["investigators"].get("ja") or []
            inv = "（" + "，".join(x.get("name", "") for x in ij) + "）"
        role = m.get("research_project_owner_role", "")
        role_ja = {"principal_investigator": "研究代表者", "coinvestigator": "共同研究者"}.get(role, role)
        grant_no = (m.get("identifiers") or {}).get("grant_number", [""])[0]
        extra = f" [{grant_no}]" if grant_no else ""
        label_ja = f"{fd}–{td} — {title}（{org} / {system} {cat}）{inv}{extra}"
        label_en = f"{fd}–{td} — {pick_lang(m, 'research_project_title', 'en')} ({pick_lang(m, 'offer_organization', 'en')})"
        grants_html.append(f'            <li data-ja="{esc(label_ja)}" data-en="{esc(label_en)}">{esc(label_ja)}</li>')

    # Committee
    comm_html = []
    for m in sorted(by_type.get("committee_memberships", []), key=lambda x: x.get("from_date", ""), reverse=True):
        cn = pick_lang(m, "committee_name")
        assoc = pick_lang(m, "association")
        fd = m.get("from_date", "")
        td = m.get("to_date", "")
        td_disp = "現在" if td == "9999" else td
        label_ja = f"{fd}–{td_disp} — {assoc} {cn}"
        label_en = f"{fd}–{td_disp} — {pick_lang(m, 'association', 'en')} {pick_lang(m, 'committee_name', 'en')}"
        comm_html.append(f'            <li data-ja="{esc(label_ja)}" data-en="{esc(label_en)}">{esc(label_ja)}</li>')

    OUT.write_text(
        f"<!-- AUTO-GENERATED from {JSONL.name} -->\n"
        f"<!-- JOURNAL_COUNT: {len(journals)} -->\n"
        + journal_html,
        encoding="utf-8",
    )
    print(f"Wrote journal list ({len(journals)} papers) to {OUT}")
    print(f"Awards: {len(awards_html)}, Presentations sample: {len(pres_html)}, Grants: {len(grants_html)}")

    # Write fragments for manual merge
    fragments = Path(__file__).parent / "fragments"
    fragments.mkdir(exist_ok=True)
    (fragments / "awards.html").write_text("\n".join(awards_html), encoding="utf-8")
    (fragments / "presentations.html").write_text("\n".join(pres_html), encoding="utf-8")
    (fragments / "grants.html").write_text("\n".join(grants_html), encoding="utf-8")
    (fragments / "committee.html").write_text("\n".join(comm_html), encoding="utf-8")
    (fragments / "books.html").write_text("\n".join(books_html), encoding="utf-8")
    (fragments / "journals.html").write_text(journal_html, encoding="utf-8")


if __name__ == "__main__":
    main()

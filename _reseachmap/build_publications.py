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

# Not Kaisei Sato's papers (researchmap co-affiliation noise)
EXCLUDE_PAPER_IDS = {"47741948", "47741957", "47741956"}
EXCLUDE_TITLE_SUBSTRINGS = (
    "Concentrated Polymer Brush in Reciprocating Seal",
    "レーザ粉末床溶融結合法により造形したMn添加",
    "レーザ粉末床溶融結合法におけるレーザ走査パターン",
)

# Papers not yet in researchmap export (newest first when merged)
MANUAL_JOURNAL_PAPERS = [
    {
        "publication_date": "2026-02",
        "paper_title": {
            "en": (
                "Friction Mechanism on Steel Surface in n-Hexadecane Containing Stearic Acid "
                "Based on Cross-Sectional Observation Using Frequency-Modulation Atomic Force Microscopy"
            ),
        },
        "authors": {
            "ja": [
                {"name": "Kaisei Sato"},
                {"name": "Yuko Sato"},
                {"name": "Seiya Watanabe"},
                {"name": "Shinya Sasaki"},
            ],
            "en": [
                {"name": "Kaisei Sato"},
                {"name": "Yuko Sato"},
                {"name": "Seiya Watanabe"},
                {"name": "Shinya Sasaki"},
            ],
        },
        "publication_name": {"en": "Langmuir", "ja": "Langmuir"},
        "volume": "42",
        "number": "7",
        "starting_page": "5524",
        "ending_page": "5532",
        "published_paper_type": "scientific_journal",
        "identifiers": {"doi": ["10.1021/acs.langmuir.5c05564"]},
        "see_also": [
            {"label": "doi", "@id": "https://doi.org/10.1021/acs.langmuir.5c05564", "is_downloadable": False}
        ],
    },
    {
        "publication_date": "2026-01",
        "paper_title": {
            "ja": "リン系/硫黄系添加剤併用系の濃度が摩耗現象に与える影響の AE 測定を用いた解析",
        },
        "authors": {
            "ja": [
                {"name": "森田美穂"},
                {"name": "土屋拓摩"},
                {"name": "佐藤剛久"},
                {"name": "佐藤魁星"},
                {"name": "佐々木信也"},
            ],
            "en": [
                {"name": "Miho Morita"},
                {"name": "Takuma Tsuchiya"},
                {"name": "Takehisa Sato"},
                {"name": "Kaisei Sato"},
                {"name": "Shinya Sasaki"},
            ],
        },
        "publication_name": {"ja": "トライボロジスト", "en": "トライボロジスト"},
        "volume": "71",
        "number": "1",
        "starting_page": "99",
        "ending_page": "108",
        "published_paper_type": "scientific_journal",
        "identifiers": {"doi": ["10.18914/tribologist.71.1_99"]},
        "see_also": [
            {"label": "doi", "@id": "https://doi.org/10.18914/tribologist.71.1_99", "is_downloadable": False}
        ],
    },
    {
        "publication_date": "2025-11",
        "paper_title": {
            "en": (
                "Influence of Slide-Roll Ratio on Micropitting under Rolling-Sliding Contact "
                "in Base Oil and E-Axle Fluid"
            ),
        },
        "authors": {
            "ja": [
                {"name": "國井卓人"},
                {"name": "福田豊也"},
                {"name": "佐藤魁星"},
                {"name": "佐々木信也"},
            ],
            "en": [
                {"name": "Takuto Kunii"},
                {"name": "Toya Fukuda"},
                {"name": "Kaisei Sato"},
                {"name": "Shinya Sasaki"},
            ],
        },
        "publication_name": {"en": "Tribology Online", "ja": "Tribology Online"},
        "volume": "20",
        "number": "4",
        "starting_page": "220",
        "ending_page": "229",
        "published_paper_type": "scientific_journal",
        "identifiers": {"doi": ["10.2474/trol.20.220"]},
        "see_also": [
            {"label": "doi", "@id": "https://doi.org/10.2474/trol.20.220", "is_downloadable": False}
        ],
    },
]


def esc(s):
    return html.escape(s or "", quote=False)


def pick_lang(d, key, prefer="ja"):
    if not isinstance(d, dict):
        return ""
    block = d.get(key) or {}
    if prefer == "ja":
        return (block.get("ja") or block.get("en") or "").strip()
    return (block.get("en") or block.get("ja") or "").strip()


def authors_strings(authors):
    """Return (ja, en) author lines; join every listed co-author."""
    if not authors:
        return "", ""

    def join_lang(lang):
        names = [
            a.get("name", "").strip()
            for a in (authors.get(lang) or [])
            if a.get("name", "").strip()
        ]
        if not names:
            return ""
        if len(names) == 1:
            return names[0]
        return " ".join(names)

    ja = join_lang("ja")
    en = join_lang("en")
    if not en:
        en = ja
    if not ja:
        ja = en
    return ja, en


def is_excluded_paper(record):
    rid = record["insert"].get("id", "")
    if rid in EXCLUDE_PAPER_IDS:
        return True
    m = record["merge"]
    for prefer in ("ja", "en"):
        title = pick_lang(m, "paper_title", prefer)
        if any(sub in title for sub in EXCLUDE_TITLE_SUBSTRINGS):
            return True
    return False


def year_from(date):
    if not date:
        return ""
    return str(date)[:4]


def pub_citation(m):
    title = pick_lang(m, "paper_title") or pick_lang(m, "book_title")
    authors_ja, authors_en = authors_strings(m.get("authors"))
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
    return title, authors_ja, authors_en, cite, y, doi_link


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
        or "トライボロジスト" in pub
        or "軽金属" in pub
    ):
        return True
    if m.get("referee"):
        if "tribology" in pub or "トライボロジ" in pub or "cellulose" in pub or "wear" in pub:
            return True
    return False


def li_pub_item(title, authors_ja, authors_en, journal, year, doi_link="", data_ja=None, data_en=None):
    t_ja = data_ja or title
    t_en = data_en or title
    a_ja = authors_ja or authors_en
    a_en = authors_en or authors_ja
    a_attr = f' data-ja="{esc(a_ja)}" data-en="{esc(a_en)}"'
    a_display = a_en if a_ja == a_en else a_ja
    t_attr = ""
    if t_ja != t_en:
        t_attr = f' data-ja="{esc(t_ja)}" data-en="{esc(t_en)}"'
    return f"""            <li class="pub-item">
              <span class="pub-title"{t_attr}>{esc(title)}</span>
              <span class="pub-authors"{a_attr}>{esc(a_display)}</span>
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
    journals = []
    for r in records:
        if is_excluded_paper(r):
            continue
        t = r["insert"]["type"]
        m = r["merge"]
        if t == "published_papers" and is_journal_paper(m):
            journals.append(m)
        elif t == "misc" and is_journal_paper(m) and m.get("volume"):
            journals.append(m)
    for manual in MANUAL_JOURNAL_PAPERS:
        journals.append(manual)
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
        title, authors_ja, authors_en, cite, y, doi = pub_citation(m)
        lines.append(li_pub_item(title, authors_ja, authors_en, cite, y, doi))
    lines.append("          </ul>")

    journal_html = "\n".join(lines)

    # Books
    books_html = []
    for m in sorted(by_type.get("books_etc", []), key=lambda x: x.get("publication_date", ""), reverse=True):
        title = pick_lang(m, "book_title")
        authors_ja, authors_en = authors_strings(m.get("authors"))
        authors = authors_ja or authors_en
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
    ADDITIVE_GROUP_URL = "https://www.tribology.jp/unit/s-201/index.html"
    comm_html = []
    for m in sorted(by_type.get("committee_memberships", []), key=lambda x: x.get("from_date", ""), reverse=True):
        cn = pick_lang(m, "committee_name")
        assoc = pick_lang(m, "association")
        fd = m.get("from_date", "")
        td = m.get("to_date", "")
        td_disp = "現在" if td == "9999" else td
        label_ja = f"{fd}–{td_disp} — {assoc} {cn}"
        label_en = f"{fd}–{td_disp} — {pick_lang(m, 'association', 'en')} {pick_lang(m, 'committee_name', 'en')}"
        if "添加剤技術研究会" in label_ja and "幹事" in label_ja:
            prefix_ja = f"{fd}–{td_disp} — {assoc} "
            prefix_en = f"{fd}–{td_disp} — {pick_lang(m, 'association', 'en')} "
            comm_html.append(
                f'            <li class="committee-item"><span data-ja="{esc(prefix_ja)}" data-en="{esc(prefix_en)}">{esc(prefix_ja)}</span>'
                f'<a href="{ADDITIVE_GROUP_URL}" target="_blank" rel="noopener noreferrer" data-ja="添加剤技術研究会" data-en="Research Group on Lubricant Additive Technology">添加剤技術研究会</a>'
                f'<span data-ja=" 幹事" data-en=" (executive member)"> 幹事</span></li>'
            )
        else:
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

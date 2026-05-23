# -*- coding: utf-8 -*-
from pathlib import Path

base = Path(__file__).parent.parent
frag = Path(__file__).parent / "fragments"
pub = base / "publications.html"

raw = pub.read_text(encoding="utf-8")
head, _, rest = raw.partition('<section class="section">')
_, _, tail = rest.rpartition("</main>")

middle = f'''    <section class="section">
      <div class="container">
        <div class="pub-section" id="journal-papers">
          <h2>
            <span class="section-label-en">Journal Papers</span>
            <span data-ja="学術雑誌論文" data-en="Journal papers">学術雑誌論文</span>
          </h2>
          <!-- Source: _reseachmap/rm_researchers20260523-1.jsonl -->
{(frag / "journals.html").read_text(encoding="utf-8")}
        </div>

        <div class="pub-section" id="books">
          <h2>
            <span class="section-label-en">Books &amp; Chapters</span>
            <span data-ja="書籍・論文集" data-en="Books and book chapters">書籍・論文集</span>
          </h2>
          <ul class="pub-list">
{(frag / "books.html").read_text(encoding="utf-8")}
          </ul>
        </div>

        <div class="pub-section" id="awards">
          <h2>
            <span class="section-label-en">Awards</span>
            <span data-ja="受賞" data-en="Awards">受賞</span>
          </h2>
          <ul class="pub-list">
{(frag / "awards.html").read_text(encoding="utf-8")}
          </ul>
        </div>

        <div class="pub-section" id="conferences">
          <h2>
            <span class="section-label-en">Conference Presentations</span>
            <span data-ja="学会発表" data-en="Conference presentations">学会発表</span>
          </h2>
          <p class="text-muted" data-ja="直近の口頭発表（抜粋）です。全文は researchmap をご覧ください。" data-en="Recent oral presentations. See researchmap for the full list.">直近の口頭発表（抜粋）です。全文は researchmap をご覧ください。</p>
          <ul class="pub-list">
{(frag / "presentations.html").read_text(encoding="utf-8")}
          </ul>
        </div>

        <div class="pub-section" id="grants">
          <h2>
            <span class="section-label-en">Research Grants</span>
            <span data-ja="外部研究資金" data-en="Research grants">外部研究資金</span>
          </h2>
          <ul class="pub-list">
{(frag / "grants.html").read_text(encoding="utf-8")}
          </ul>
        </div>

        <div class="pub-section" id="committee">
          <h2>
            <span class="section-label-en">Committee Activities</span>
            <span data-ja="委員歴" data-en="Committee activities">委員歴</span>
          </h2>
          <ul class="pub-list">
{(frag / "committee.html").read_text(encoding="utf-8")}
          </ul>
        </div>

        <div class="pub-section" id="external-links">
          <h2>
            <span class="section-label-en">External Links</span>
            <span data-ja="関連リンク" data-en="External links">関連リンク</span>
          </h2>
          <ul class="pub-list">
            <li><a href="https://www.tokyo-ct.ac.jp/" target="_blank" rel="noopener noreferrer" data-ja="東京工業高等専門学校" data-en="National Institute of Technology, Tokyo College">東京工業高等専門学校</a></li>
            <li><a href="https://mech.tokyo-ct.ac.jp/" target="_blank" rel="noopener noreferrer" data-ja="東京工業高等専門学校 機械工学科" data-en="Dept. of Mechanical Engineering, Tokyo College">東京工業高等専門学校 機械工学科</a></li>
            <li><a href="https://www.jstage.jst.go.jp/" target="_blank" rel="noopener noreferrer">J-STAGE</a></li>
          </ul>
        </div>
      </div>
    </section>
'''

pub.write_text(head + middle + "  </main>" + tail, encoding="utf-8")
print("OK", pub)

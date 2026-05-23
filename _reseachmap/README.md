# researchmap エクスポートデータ

このフォルダには [researchmap](https://researchmap.jp/kaisei_sato) からエクスポートした JSONL と、サイト反映用スクリプトがあります。

## ファイル

| ファイル | 説明 |
|----------|------|
| `rm_researchers20260523-1.jsonl` | researchmap エクスポート（2026-05-23） |
| `build_publications.py` | JSONL から HTML 断片を生成 |
| `assemble_publications.py` | 断片を `publications.html` に組み込み |
| `fragments/` | 生成された HTML 断片 |

## 業績を更新する手順

1. researchmap でデータを更新し、新しい JSONL をエクスポートしてこのフォルダに保存
2. 次を実行:

```bash
python _reseachmap/build_publications.py
python _reseachmap/assemble_publications.py
```

3. ブラウザで `publications.html` を確認

## 反映先

- `publications.html` — 論文，書籍，受賞，学会発表，研究資金，委員歴
- `research.html` — 研究キーワード（手動同期の場合は JSONL を参照）
- `access.html` / `members.html` — 所属・職名（必要に応じて手動更新）

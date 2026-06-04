@echo off
chcp 65001 >nul
echo ============================================================
echo  Google Search Console — サイトマップ送信とインデックス登録
echo ============================================================
echo.
echo [1] Search Console を開きます（ログインしてください）
start "" "https://search.google.com/search-console"
echo.
echo [2] サイトマップ URL（プロパティに追加後、サイトマップ欄へ貼り付け）
echo.
echo   GitHub Pages（DNS 設定前）:
echo   https://nittc-sato.github.io/nittc-tribology-lab-hp/sitemap-github.xml
echo.
echo   カスタムドメイン（DNS 設定後）:
echo   https://tribo.tokyo-ct.ac.jp/sitemap.xml
echo.
echo [3] 主要ページ — URL 検査で「インデックス登録をリクエスト」
echo.
set BASE_GH=https://nittc-sato.github.io/nittc-tribology-lab-hp
set BASE_CD=https://tribo.tokyo-ct.ac.jp
echo   %BASE_GH%/
echo   %BASE_GH%/research.html
echo   %BASE_GH%/publications.html
echo   %BASE_GH%/members.html
echo   %BASE_GH%/news.html
echo   %BASE_GH%/facilities.html
echo   %BASE_GH%/for-students.html
echo   %BASE_GH%/access.html
echo.
echo   （DNS 反映後は %BASE_CD%/ でも同様にリクエスト）
echo.
echo [4] robots.txt の確認
start "" "%BASE_GH%/robots.txt"
echo.
pause

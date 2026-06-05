@echo off
chcp 65001 >nul
echo ============================================================
echo  Google Search Console — サイトマップ送信とインデックス登録
echo ============================================================
echo.
echo 公開 URL: https://nittc-sato.github.io/nittc-tribology-lab-hp/
echo.
echo [1] Search Console を開きます（ログインしてください）
start "" "https://search.google.com/search-console"
echo.
echo [2] プロパティ（URL プレフィックス）:
echo   https://nittc-sato.github.io/nittc-tribology-lab-hp/
echo.
echo [3] サイトマップ URL（サイトマップ欄に貼り付け）:
echo   sitemap.xml
echo   または
echo   https://nittc-sato.github.io/nittc-tribology-lab-hp/sitemap.xml
echo.
echo [4] 主要ページ — URL 検査で「インデックス登録をリクエスト」
echo.
set BASE=https://nittc-sato.github.io/nittc-tribology-lab-hp
echo   %BASE%/
echo   %BASE%/research.html
echo   %BASE%/publications.html
echo   %BASE%/members.html
echo   %BASE%/news.html
echo   %BASE%/facilities.html
echo   %BASE%/for-students.html
echo   %BASE%/access.html
echo.
echo [5] robots.txt / sitemap.xml の確認
start "" "%BASE%/robots.txt"
start "" "%BASE%/sitemap.xml"
echo.
pause

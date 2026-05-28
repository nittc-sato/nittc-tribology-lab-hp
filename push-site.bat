@echo off
setlocal

cd /d "G:\My Drive\9.Cursorcode\3_HP"

set MSG=%*
if "%MSG%"=="" set MSG=Update site

echo.
echo === Git add ===
git add -A
if errorlevel 1 goto :error

echo.
echo === Git commit ===
git -c user.name="Kaisei Sato" -c user.email="sato@tokyo-ct.ac.jp" commit -m "%MSG%"
if errorlevel 1 (
  echo.
  echo [INFO] Commit skipped or failed. If there are no changes, this is expected.
)

echo.
echo === Git push ===
git push
if errorlevel 1 goto :error

echo.
echo Done.
exit /b 0

:error
echo.
echo [ERROR] Command failed. Please review the message above.
exit /b 1

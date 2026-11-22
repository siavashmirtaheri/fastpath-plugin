@echo off
REM Publish fastpath v1.0.0. Requires: gh authenticated with repo scope (gh auth status).
REM Ignore any stale/invalid token in the environment and use gh's keyring token.
set GITHUB_TOKEN=
cd /d D:\Projects\fastpath-plugin
gh auth status
if errorlevel 1 exit /b 1

gh repo create siavashmirtaheri/fastpath-plugin --public --source=. --remote=origin --push
if errorlevel 1 exit /b 1

gh release create v1.0.0 D:\Projects\fastpath-plugin\fastpath-plugin-1.0.0.zip --title "fastpath v1.0.0" --notes-file RELEASE.md

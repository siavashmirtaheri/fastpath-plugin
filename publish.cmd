@echo off
set GITHUB_TOKEN=
gh auth login -h github.com
cd /d D:\Projects\fastpath-plugin
gh repo create siavashmirtaheri/fastpath-plugin --public --source=. --remote=origin --push
gh release create v1.0.0 D:\Projects\fastpath-plugin\fastpath-plugin-1.0.0.zip --title "fastpath v1.0.0" --notes-file RELEASE.md

#!/bin/sh
# Builds dist/ (upstream theme + every patch, in name order) and installs it into each vault in
# $VAULTS (colon-separated), e.g. VAULTS="$HOME/Documents/obsidian/personal" ./build.sh
set -eu
cd "$(dirname "$0")"

version=$(sed -n 's/.*"version": *"\(.*\)".*/\1/p' upstream/manifest.json)
min_app=$(sed -n 's/.*"minAppVersion": *"\(.*\)".*/\1/p' upstream/manifest.json)

mkdir -p dist
{
	cat upstream/theme.css
	for patch in patches/*.css; do
		printf '\n/* ── Willemstad Plus: %s ── */\n' "$patch"
		cat "$patch"
	done
} > dist/theme.css

# Keep theme.css under Obsidian Sync's 5 MB per-file limit (see tools/subset_fonts.py).
[ -x .venv/bin/python ] || { python3 -m venv .venv && .venv/bin/pip install -q fonttools brotli; }
.venv/bin/python tools/subset_fonts.py dist/theme.css

cat > dist/manifest.json <<JSON
{
  "name": "Willemstad Plus",
  "version": "$version",
  "minAppVersion": "$min_app",
  "author": "tingmelvin, patched by Himanshu Gupta",
  "authorUrl": "https://github.com/himanshugupta2077/obsidian-willemstad-plus"
}
JSON

echo "built Willemstad Plus (upstream $version)"
IFS=:
for vault in ${VAULTS:-}; do
	dir="$vault/.obsidian/themes/Willemstad Plus"
	mkdir -p "$dir"
	cp dist/theme.css dist/manifest.json "$dir/"
	echo "installed → $dir"
done

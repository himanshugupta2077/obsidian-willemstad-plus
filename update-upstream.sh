#!/bin/sh
# Pulls the latest Willemstad release from tingmelvin/willemstad-x into upstream/, then rebuilds.
# Patches only override upstream rules, so they normally carry over; check the tabs afterwards.
set -eu
cd "$(dirname "$0")"
base=https://raw.githubusercontent.com/tingmelvin/willemstad-x/main
curl -fsSL "$base/theme.css" -o upstream/theme.css
curl -fsSL "$base/manifest.json" -o upstream/manifest.json
./build.sh

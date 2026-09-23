#!/bin/sh
# Packs the glider course.
#
# The binary is C-Lehrer's, unchanged: that app reads its whole course from
# <app>/data/kurs.json and knows nothing about the subject. So a second
# course is a second package, not a second program -- only the data, the
# pictures, the icon and the name differ.
#
#   tools/build-deb.sh [version]
set -e
cd "$(dirname "$0")/.."

VERSION=${1:-0.1}
BIN=${BIN:-$HOME/ps/c-lehrer/build/c-lehrer}
STAGE=build/stage
rm -rf "$STAGE"

[ -x "$BIN" ] || { echo "Binaer fehlt: $BIN (erst ~/ps/c-lehrer/tools/build.sh)" >&2; exit 1; }

mkdir -p "$STAGE/opt/segelflug/bin" "$STAGE/opt/segelflug/qml" \
         "$STAGE/opt/segelflug/data" "$STAGE/opt/segelflug/bilder" \
         "$STAGE/usr/share/applications" \
         "$STAGE/usr/share/icons/hicolor/80x80/apps" "$STAGE/DEBIAN"

cp "$BIN" "$STAGE/opt/segelflug/bin/segelflug"
cp "$HOME/ps/c-lehrer/qml/"*.qml "$HOME/ps/c-lehrer/qml/"*.js "$STAGE/opt/segelflug/qml/"
cp data/kurs.json "$STAGE/opt/segelflug/data/"
cp bilder/*.png "$STAGE/opt/segelflug/bilder/"
cp segelflug.desktop "$STAGE/usr/share/applications/"
cp icons/icon-80.png "$STAGE/usr/share/icons/hicolor/80x80/apps/segelflug.png"
chmod 755 "$STAGE/opt/segelflug/bin/segelflug"

python3 - "$VERSION" <<'PY'
import base64, io, sys, textwrap
version = sys.argv[1]
icon = base64.b64encode(open("icons/icon-64.png", "rb").read()).decode("ascii")
text = io.open("control.in", encoding="utf-8").read()
text = text.replace("@VERSION@", version)
text = text.replace("@ICON@",
                    "\n".join(" " + line for line in textwrap.wrap(icon, 76)))
io.open("build/stage/DEBIAN/control", "w", encoding="utf-8").write(text)
PY

python3 tools/mkdeb.py "$STAGE" "segelflug_${VERSION}_armel.deb"

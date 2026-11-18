#!/usr/bin/env bash
# Print one version's section of CHANGELOG.md, for the GitHub release body.
#   scripts/release-notes.sh 0.2.0 | gh release create v0.2.0 --notes-file -
set -euo pipefail
v="${1:?usage: release-notes.sh X.Y.Z}"
cd "$(dirname "$0")/.."
out="$(awk -v v="$v" '$0 ~ "^## "v" " {p=1; next} /^## /{p=0} p' CHANGELOG.md)"
[ -n "$out" ] || { echo "no '## $v' section in CHANGELOG.md" >&2; exit 1; }
printf '%s\n\nFull history: [CHANGELOG.md](https://github.com/yamf97/lecture-note-bench/blob/main/CHANGELOG.md)\n' "$out"

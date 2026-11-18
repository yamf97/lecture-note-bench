#!/usr/bin/env bash
# Release check: install a pushed tag from GitHub into a throwaway pipx home and
# confirm it behaves like the repository source.
#
#   scripts/release-check.sh            # tag = v<lnb.__version__>
#   scripts/release-check.sh v0.2.0
#
# It never touches your own pipx install. Run it after pushing the tag.
# Exit 0 = all checks passed, 1 = something failed.
set -uo pipefail

REPO_URL="https://github.com/yamf97/lecture-note-bench"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1

version="$(PYTHONPATH=src python3 -c 'import lnb; print(lnb.__version__)')"
tag="${1:-v$version}"

T="$(mktemp -d "${TMPDIR:-/tmp}/lnb-release-XXXXXX")"
trap 'rm -rf "$T"' EXIT
export PIPX_HOME="$T/home" PIPX_BIN_DIR="$T/bin" PIPX_MAN_DIR="$T/man"
LNB="$T/bin/lnb"

fail=0
ok()  { printf '  ok    %s\n' "$*"; }
bad() { printf '  FAIL  %s\n' "$*"; fail=1; }

echo "release check: $tag"

# 1. The tag exists on GitHub and matches the version in the source
if git ls-remote --exit-code --tags origin "refs/tags/$tag" >/dev/null 2>&1; then
  ok "tag $tag is on GitHub"
else
  bad "tag $tag is not on GitHub (push it first: git push origin $tag)"; exit 1
fi
[ "$tag" = "v$version" ] || echo "  note  source is $version; checking $tag anyway"
if grep -q "최신 버전 $version" README.md && grep -q "Latest: $version" README.md \
   && grep -q "^## $version " CHANGELOG.md; then
  ok "README (KO, EN) and CHANGELOG name $version"
else
  bad "README 「최신 버전」/「Latest」 lines or CHANGELOG section do not name $version"
fi

# 2. Pinned install
if pipx install --force "git+$REPO_URL@$tag" >"$T/install.log" 2>&1; then
  ok "pipx install @$tag"
else
  bad "pipx install @$tag (log below)"; tail -5 "$T/install.log"; exit 1
fi

# 3. Version string
got="$("$LNB" --help | head -n1)"
case "$got" in
  "lnb ${tag#v} "*) ok "lnb --help says ${tag#v}" ;;
  *) bad "lnb --help says: $got" ;;
esac

# 4. Every subcommand answers --help
for cmd in fetch transcribe text frames pages check doctor; do
  if "$LNB" "$cmd" --help >/dev/null 2>&1; then ok "lnb $cmd --help"; else bad "lnb $cmd --help"; fi
done

# 5. The installed checker gives the same result as the source on the experiment notes
"$LNB" check experiments/results/*.md >"$T/installed.txt" 2>&1
python3 tools/check_note.py experiments/results/*.md >"$T/source.txt" 2>&1
if [ "$tag" != "v$version" ]; then
  echo "  skip  installed vs source comparison (source is not $tag)"
elif diff -q "$T/installed.txt" "$T/source.txt" >/dev/null; then
  ok "lnb check output = source output (experiments/results)"
else
  bad "lnb check output differs from source:"; diff "$T/installed.txt" "$T/source.txt" | head -10
fi

# 6. The published experiment table still holds (README: A 3, B 2, C 1, D 3, E 0)
counts="$(awk '/^(FAIL|ok)/{f=$2; c[f]+=0} /^ +[0-9]+행:/{c[f]++}
  END{for(k in c){n=k; sub(/.*\//,"",n); sub(/\.md$/,"",n); printf "%s%d ", n, c[k]}}' "$T/installed.txt" \
  | tr ' ' '\n' | sort | tr '\n' ' ')"
if [ "$counts" = "A3 B2 C1 D3 E0 " ]; then
  ok "experiment failures match README ($counts)"
else
  bad "experiment failures: $counts(README says A3 B2 C1 D3 E0)"
fi

# 7. doctor runs (exit 1 only means something optional is missing on this machine)
"$LNB" doctor >/dev/null 2>&1; rc=$?
if [ "$rc" -le 1 ]; then ok "lnb doctor runs (exit $rc)"; else bad "lnb doctor exit $rc"; fi

# 8. Upgrade path from an unpinned install
pipx uninstall lecture-note-bench >/dev/null 2>&1
if pipx install "git+$REPO_URL" >/dev/null 2>&1 && pipx upgrade lecture-note-bench >/dev/null 2>&1; then
  ok "pipx install (latest) + pipx upgrade"
else
  bad "pipx install (latest) + pipx upgrade"
fi

echo
[ "$fail" = 0 ] && echo "all checks passed" || echo "some checks FAILED"
exit "$fail"

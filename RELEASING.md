# Releasing (maintainers)

1. Bump `src/lnb/__init__.py`.
2. Add a `## X.Y.Z — YYYY-MM-DD` section to CHANGELOG.md, Korean (`### 한국어`) first, then English (`### English`). Write what changed for the person using `lnb`; leave out internal fixes they never see.
3. Update the version notice at the top of README in plain words: KO "X 버전이 나왔습니다" and EN "Version X is out", with one line per recent version on what got better.
4. Commit, tag `vX.Y.Z`, push the commit and the tag.
5. Publish the GitHub release with the same notes: `scripts/release-notes.sh X.Y.Z | gh release create vX.Y.Z --title vX.Y.Z --notes-file -`
6. Run `scripts/release-check.sh`. It installs the pushed tag into a throwaway pipx home and checks it.

Versioning: while the major version is 0, a minor bump means new features or changed check results, a patch bump means bug fixes only, and documentation-only changes do not bump the version.

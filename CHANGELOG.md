# Changelog

Versions follow `MAJOR.MINOR.PATCH`. While the major version is 0, a minor bump (0.1 → 0.2) means new features or changed check results, and a patch bump (0.2.0 → 0.2.1) means bug fixes only. Documentation-only changes do not bump the version.

Releasing: bump `src/lnb/__init__.py`, add a section here, update the "Latest" lines at the top of README (KO and EN), commit, tag `vX.Y.Z`, push the commit and the tag, publish the GitHub release with the same notes (`gh release create vX.Y.Z --notes-file <section>`), then run `scripts/release-check.sh`.

Install a specific version with `pipx install --force git+https://github.com/yamf97/lecture-note-bench@v0.2.0`.

## 0.2.0 — 2026-11-18

### Added
- **`lnb pages`**: turns a textbook or handout into page-marked md (`<!-- p.68 (PDF 78) -->`). It takes MinerU's `*_content_list.json` or a PDF with a text layer, and warns when the printed page numbers disagree with `--offset`.
- **Textbook quote check in `lnb check`**: with `"books"` in `check_note.json`, the check looks up each quote written as ``"…" `Book §x p.N` `` on that page. Math is ignored, quotes may run onto the next page, and a mismatch points to the right page. Quotes that cannot be checked are counted separately and never as passes. Repositories without `"books"` get exactly the same output as before.
- `lnb check --help` shows the `check_note.json` format.

### Changed
- **Installed `lnb check` no longer assumes this repository's `lectures/` folder.** Each repository, including this one, maps its courses in a `check_note.json` at its root. In 0.1.0, an installed `lnb` looked for lectures in the wrong place.
- `lnb transcribe` no longer searches a personal app folder for whisper models. Use `-m`, `WHISPER_MODEL`, `~/.cache/whisper.cpp/` or `~/models/whisper/`.
- `--help` examples use `lnb <command>`, with `python3 tools/<file>.py` as the fallback.

### Fixed
- `lnb fetch` stops with exit code 2 on a block in every download path (single-video metadata, audio, video, and playlist `--video`), not only in some of them. A title containing "bot" (such as *Robotics*) is no longer mistaken for a block.
- `lnb check`: a config without `"books"` now clears books left over from an earlier load in the same process.

### Docs
- README: note-writing steps, the textbook and slide material step (MinerU `-b pipeline`, MarkItDown), MinerU license by version, macOS-only status, a statement that the code was written with Claude Code, and a structured English section.

## 0.1.0 — 2026-11-17

First installable release. The scripts in `tools/` became the `lnb` command (`pipx install`), and `tools/` now holds thin wrappers around `src/lnb/`.

- Subcommands: `fetch`, `transcribe`, `text`, `frames`, `check`, `doctor`.
- `lnb check`: verbatim quotes against the captions, cue start times, and embedded calculations (with a restricted expression allowlist).
- Claude Code skill `skills/lecture-note/`.

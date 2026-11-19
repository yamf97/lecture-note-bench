# Changelog · 바뀐 점

버전마다 한국어를 먼저, 이어서 English를 적습니다. Each version lists Korean first, then English.

**버전 규칙**: `MAJOR.MINOR.PATCH`. 앞자리가 0인 동안 가운데 자리(0.1 → 0.2)는 새 기능이나 검사 결과가 달라지는 변경, 끝자리(0.2.0 → 0.2.1)는 버그 수정만입니다. 문서만 바뀌면 버전을 올리지 않습니다.

**Versioning**: `MAJOR.MINOR.PATCH`. While the major version is 0, a minor bump (0.1 → 0.2) means new features or changed check results, and a patch bump (0.2.0 → 0.2.1) means bug fixes only. Documentation-only changes do not bump the version.

특정 버전 설치 · Install a specific version: `pipx install --force git+https://github.com/yamf97/lecture-note-bench@v0.4.0`

## 0.4.0 — 2026-11-19

### 한국어

**추가**
- `lnb transcribe`가 폴더를 받습니다. 하위 폴더까지 음성·영상을 찾고, `-o`를 주면 그 아래에 같은 폴더 구조로 자막을 만듭니다. 원래 폴더는 건드리지 않습니다.
- 진행 상황(몇 번째인지, 남은 시간 어림)을 보여 주고, 실패한 파일을 끝에 모아 보여 주며 `-o`가 있으면 `failed.txt`에 적습니다.

**바뀜**
- 자막 이름에 모델 이름이 들어갑니다: `<이름> (whisper <모델>).srt`. 같은 모델의 자막이 있으면 건너뛰어 끊긴 곳부터 이어서 하고, 모델을 바꾸면 새 자막을 따로 만들고 예전 것은 남깁니다.
- 자막은 다 만든 뒤에야 제 이름이 됩니다. 도중에 끊겨 반쪽 자막이 남지 않습니다.
- 이미 있는 자막도 끝 시각이 음성보다 10초 넘게 짧으면 경고합니다.
- 같은 폴더에 `1강.mp4`와 `1강.m4a`처럼 이름만 같은 파일이 있으면 자막 이름에 확장자까지 넣어 서로 덮어쓰지 않습니다. 그래도 겹치면 시작 전에 멈추고 이름을 바꿀 파일을 알려 줍니다.
- 0.3.0까지 만든 `<이름> (whisper).srt`는 "이미 있음"으로 보지 않습니다. 그 강의를 `lnb transcribe`로 다시 돌리면 새 이름으로 다시 받아씁니다.

**문서**
- README에 Whisper·whisper.cpp가 무엇인지, 누가 만들었고 어떤 라이선스인지, 왜 쓰는지를 적었습니다. `docs/roadmap.md`에 앞으로 할 일을 적었습니다.

### English

**Added**
- `lnb transcribe` accepts folders. It finds audio and video in subfolders, and with `-o` it writes captions under that folder in the same structure. The source folder is left untouched.
- Progress (item count and estimated time left), a list of failed files at the end, and `failed.txt` under `-o`.

**Changed**
- Caption names include the model: `<name> (whisper <model>).srt`. An existing caption from the same model is skipped, so a rerun resumes; a different model writes a new caption and keeps the old one.
- A caption gets its final name only when complete, so an interrupted run leaves no half-written caption.
- Existing captions are also warned about when they end more than 10 seconds before the audio.
- Files that differ only by extension in one folder (`1.mp4`, `1.m4a`) get the extension in the caption name, so neither overwrites the other. If names still clash, the run stops before starting and names the files to rename.
- Captions named `<name> (whisper).srt` from 0.3.0 and earlier are not treated as done; running `lnb transcribe` on those lectures again transcribes them under the new name.

**Docs**
- README explains what Whisper and whisper.cpp are, who makes them, their licenses, and why lnb uses them. `docs/roadmap.md` lists planned work.

## 0.3.0 — 2026-11-18

### 한국어

**추가**
- **`lnb setup`**: 받아쓰기(transcribe) 준비를 한 번에 합니다.
  - whisper-cli·ffmpeg가 없으면 설치 명령(`brew install …`)을 알려 줍니다. 프로그램을 직접 깔지는 않습니다.
  - whisper 모델 `ggml-large-v3-turbo-q5_0.bin`(약 574MB)을 받을지 묻고 받습니다. 주소는 Hugging Face의 한 커밋에 고정돼 있고, **크기와 SHA256이 맞을 때만** `~/.cache/whisper.cpp/`에 둡니다. 틀리면 받은 파일을 지우고 멈춥니다.
  - 모델이 이미 있으면 해시만 확인하고 덮어쓰지 않습니다. 그 자리가 폴더이거나 읽을 수 없는 파일이면 건드리지 않고 알립니다.
  - `--yes`면 묻지 않고 받습니다.

**바뀜**
- 모델이 없을 때 `lnb doctor`·`lnb transcribe`가 커밋에 고정되지 않은 `curl` 명령 대신 `lnb setup`을 안내합니다.

### English

**Added**
- **`lnb setup`** prepares transcription.
  - It prints the install command for whisper-cli and ffmpeg when they are missing. It never installs programs.
  - It asks before downloading the whisper model `ggml-large-v3-turbo-q5_0.bin` (about 574 MB). The URL is pinned to one Hugging Face commit, and the file is kept in `~/.cache/whisper.cpp/` **only if its size and SHA256 match**; otherwise it is deleted.
  - An existing model is hash-checked and never overwritten. A directory or unreadable file at that path is reported and left alone.
  - `--yes` skips the question.

**Changed**
- When the model is missing, `lnb doctor` and `lnb transcribe` point to `lnb setup` instead of an unpinned `curl` command.

## 0.2.0 — 2026-11-18

### 한국어

**추가**
- **`lnb pages`**: 교재·강의록을 쪽 표시가 든 md(`<!-- p.68 (PDF 78) -->`)로 만듭니다. MinerU의 `*_content_list.json`이나 글자 층이 있는 PDF를 받고, 인쇄된 쪽 번호가 `--offset`과 어긋나면 경고합니다.
- **`lnb check`의 교재 인용 검사**: `check_note.json`에 `"books"`가 있으면 ``"…" `책 §x p.N` `` 꼴 인용을 그 쪽에서 찾습니다. 수식은 무시하고, 다음 쪽으로 넘어가는 인용도 찾으며, 틀리면 맞는 쪽을 알려 줍니다. 검사할 수 없는 인용은 따로 세고 통과로 치지 않습니다. `"books"`가 없는 저장소는 출력이 전과 똑같습니다.
- `lnb check --help`가 `check_note.json` 형식을 보여 줍니다.

**바뀜**
- **설치한 `lnb check`가 더는 이 저장소의 `lectures/` 폴더를 가정하지 않습니다.** 이 저장소를 포함해 저장소마다 뿌리의 `check_note.json`에 강좌 목록을 적습니다. 0.1.0에서는 설치한 `lnb`가 엉뚱한 곳에서 강의를 찾았습니다.
- `lnb transcribe`가 개인 앱 폴더에서 whisper 모델을 찾지 않습니다. `-m`, `WHISPER_MODEL`, `~/.cache/whisper.cpp/`, `~/models/whisper/`를 씁니다.

**고침**
- `lnb fetch`가 모든 받기 경로(영상 하나의 정보, 음성, 영상, 재생목록 `--video`)에서 차단 응답을 받으면 종료 코드 2로 멈춥니다. 전에는 일부 경로에서만 그랬습니다. 제목에 "bot"이 든 강의(예: *Robotics*)를 차단으로 오인하지 않습니다.

**문서**
- README: 노트 쓰는 단계, 교재·슬라이드 재료 단계(MinerU `-b pipeline`, MarkItDown), 버전별 MinerU 라이선스, macOS 전용 상태, Claude Code로 코드를 썼다는 설명, 정리된 영문 절.

### English

**Added**
- **`lnb pages`**: turns a textbook or handout into page-marked md (`<!-- p.68 (PDF 78) -->`). It takes MinerU's `*_content_list.json` or a PDF with a text layer, and warns when the printed page numbers disagree with `--offset`.
- **Textbook quote check in `lnb check`**: with `"books"` in `check_note.json`, the check looks up each quote written as ``"…" `Book §x p.N` `` on that page. Math is ignored, quotes may run onto the next page, and a mismatch points to the right page. Quotes that cannot be checked are counted separately and never as passes. Repositories without `"books"` get exactly the same output as before.
- `lnb check --help` shows the `check_note.json` format.

**Changed**
- **Installed `lnb check` no longer assumes this repository's `lectures/` folder.** Each repository, including this one, maps its courses in a `check_note.json` at its root. In 0.1.0, an installed `lnb` looked for lectures in the wrong place.
- `lnb transcribe` no longer searches a personal app folder for whisper models. Use `-m`, `WHISPER_MODEL`, `~/.cache/whisper.cpp/` or `~/models/whisper/`.

**Fixed**
- `lnb fetch` stops with exit code 2 on a block in every download path (single-video metadata, audio, video, and playlist `--video`), not only in some of them. A title containing "bot" (such as *Robotics*) is no longer mistaken for a block.

**Docs**
- README: note-writing steps, the textbook and slide material step (MinerU `-b pipeline`, MarkItDown), MinerU license by version, macOS-only status, a statement that the code was written with Claude Code, and a structured English section.

## 0.1.0 — 2026-11-17

### 한국어

처음으로 설치할 수 있게 된 판입니다. `tools/`의 스크립트가 `lnb` 명령이 되었고(`pipx install`), `tools/`는 `src/lnb/`를 부르는 얇은 껍데기가 되었습니다.

- 하위 명령: `fetch`, `transcribe`, `text`, `frames`, `check`, `doctor`.
- `lnb check`: 자막과 글자 그대로 맞는지 보는 인용 검사, 큐 시작 시각, 노트에 심은 검산식(허용 목록으로 제한한 식).
- Claude Code 스킬 `skills/lecture-note/`.

### English

First installable release. The scripts in `tools/` became the `lnb` command (`pipx install`), and `tools/` now holds thin wrappers around `src/lnb/`.

- Subcommands: `fetch`, `transcribe`, `text`, `frames`, `check`, `doctor`.
- `lnb check`: verbatim quotes against the captions, cue start times, and embedded calculations (with a restricted expression allowlist).
- Claude Code skill `skills/lecture-note/`.

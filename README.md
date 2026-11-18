# lecture-note-bench

[English](#english)

> **최신 버전 0.2.0** (2026-11-18) — 교재 인용 검사가 들어왔습니다. 새 명령 `lnb pages`로 교재·강의록을 쪽 표시가 든 원문으로 만들면, `lnb check`가 노트의 교재 인용을 그 쪽과 대조합니다. 설치한 `lnb check`는 이제 저장소마다 `check_note.json`이 필요합니다. 바뀐 점 전체는 [CHANGELOG.md](CHANGELOG.md), 업데이트는 `pipx upgrade lecture-note-bench`

강의 영상으로 **근거를 지키는 학습 노트**를 만드는 도구와, 그 방법을 시험한 실험입니다.

- **도구 `lnb`**: 강의 자막·영상을 받아 읽기본과 판서 장면을 만들고, 다 쓴 노트의 인용·시각·계산을 원문과 기계로 대조합니다. `pipx`로 설치하는 명령줄 도구이고 AI 없이도 씁니다 (아래 「설치」)
- **스킬**: 그 도구를 Claude Code가 순서대로 부르게 하는 안내서 (`skills/lecture-note/`). 주로 AI가 `lnb`를 부르는 쪽으로 씁니다
- **실험**: 같은 지시서로 오픈 웨이트 모델 다섯 개에게 노트를 쓰게 하고 모델 이름을 가린 채 비교했습니다

선형대수·계량경제학을 다시 공부하면서 실제로 쓰는 방법을 정리한 것입니다. 노트 작성 규칙은 [METHOD.md](METHOD.md)에 있습니다.

코드는 Claude Code(AI)로 작성했습니다. 무엇을 만들지, 검증 규칙, 실험 설계와 블라인드 판정은 제가 했고, 코드는 다른 회사 모델(Codex)의 검토와 회귀 시험을 거쳐 반영합니다. AI가 쓴 커밋에는 `[AI:<모델>]` 표시가 붙어 있습니다.

## 흐름

```
강의 주소 ─ lnb fetch ─┬─ 자막 있음 ───────────────────┐
                       └─ 없음 → lnb transcribe(전사) ─┼─ lnb text 읽기본 ─ 노트 쓰기 ─ lnb check 검사
         영상 ─ lnb frames(판서·슬라이드 장면) ─────────┤
  교재·슬라이드 PDF ─ md 변환(MinerU 등) ─ lnb pages ────┘
```

노트 쓰기는 사람(또는 AI)이 합니다. 도구는 그 앞의 재료를 만들고, 뒤에서 근거를 확인합니다. 판서를 옮긴 부분은 검사기가 대조할 수 없으므로, 읽기 애매한 곳을 따로 모아 사람이 장면 사진과 맞춰 봅니다.

### 문서 재료 — 교재·슬라이드·강의록

노트는 영상만으로 쓰지 않습니다. 교재 절, 강의 슬라이드, 강의록 PDF도 노트 쓰기 전에 **md로 바꿔 함께 읽습니다.**
이 저장소에 변환 도구는 없고, 공개된 변환 도구를 그대로 씁니다:

```bash
# PDF·사진 → md (수식은 LaTeX). -b pipeline 이 기본(hybrid)보다 6배쯤 빠르다 — M1·8GB에서 2쪽 약 5분(hybrid 30분). 필요한 쪽만, -s/-e 는 0부터 세는 PDF 쪽
mineru -p 교재.pdf -o 자료폴더/md -s 40 -e 52 -b pipeline
# 오피스 문서(pptx·docx·xlsx) → md. 빠르지만 수식은 깨진다 (수식이 있으면 PDF로 바꿔 MinerU)
markitdown 슬라이드.pptx -o 자료폴더/md/슬라이드.md
```

- [MinerU](https://github.com/opendatalab/MinerU), [MarkItDown](https://github.com/microsoft/markitdown)(MIT). 설치는 각 저장소 안내를 따릅니다. MinerU는 버전마다 라이선스가 다릅니다 — 3.4.5는 「MinerU Open Source License」(Apache 2.0 + 상업 이용 문턱 등 추가 조항)이고, 이전 버전은 다를 수 있으니 설치한 버전의 LICENSE를 확인하세요. 모델 가중치에는 따로 조건이 붙을 수 있습니다
- **급할 때 몇 쪽만**은 큰 모델(Claude·GPT·Gemini)에게 쪽 그림을 주고 옮기게 해도 됩니다 — 「한 글자도 고치지 말 것, 읽기 애매하면 `[?]`, 식 번호 `(7)`은 수식 밖에, 쪽마다 `<!-- p.N (PDF M) -->`」를 지시합니다
- **변환본을 그대로 믿지 않습니다.** 한글 깨짐, 표 붕괴, 빈 수식(`$$ $$`)을 열어 보고, 노트에 옮긴 수식은 원본 쪽 그림과 대조합니다
- **변환본에는 쪽 번호가 없습니다.** 노트의 교재 인용에는 원본의 절·쪽을 답니다(`Strang ILA §3.2 p.24`, [METHOD.md](METHOD.md)). PDF 쪽과 책 쪽이 다르면 책마다 한 번 확인합니다
- 교재 변환본은 저작물입니다. 자료 폴더(git 밖)에 두고 공개 저장소에 넣지 않습니다
- **교재 인용 검사**: 변환본을 `lnb pages`로 쪽 표시가 든 원문 md로 만들고 `check_note.json`에 등록하면, `lnb check`가 노트의 `"…" \`Strang ILA §2.4 p.68\``를 그 쪽과 대조합니다 (수식은 빼고 단어로, 수식은 검산식이 따로)

  ```bash
  # MinerU 결과(json) → 쪽 표시 원문. 폴더 이름은 방식마다 다르다(pipeline: auto, hybrid: hybrid_auto). --pdf-start = 변환한 첫 쪽의 PDF 쪽(1부터), 책 쪽 = PDF 쪽 − offset
  lnb pages 자료폴더/md/교재/auto/교재_content_list.json --pdf-start 41 --offset 10 -o 자료폴더/strang-ila.md
  # 글자 층이 살아 있는 PDF는 MinerU 없이 바로
  lnb pages 강의록.pdf --first 1 --last 30 -o 자료폴더/강의록.md
  ```

  `check_note.json`에 `"books": {"Strang ILA": "~/자료폴더/strang-ila.md"}`. 변환하지 않은 쪽, 번역 문구, 단어가 너무 적은 인용은 「교재 대조 불가」로 따로 셉니다(통과로 세지 않음)

### 노트 쓰기 — 재료를 모아 한 편으로

위 재료(자막 읽기본·판서 장면·교재 md)를 옆에 두고 노트를 씁니다. 사람이 써도, AI에게 맡겨도 규칙은 같습니다. 자세한 규칙은 [METHOD.md](METHOD.md).

1. **읽기** — `lnb text`의 30초 읽기본으로 흐름을 잡고, 인용할 곳은 `--cues`로 정확한 시각을 찾습니다. 판서는 장면 사진으로, 교재는 md 변환본으로 읽습니다
2. **옮기기** — 인용은 글자 그대로, 바로 뒤에 좌표: 영상 `[Vision 00 01:47]`(그 말이 시작되는 큐) · 교재 ``"…" `Strang ILA §3.2 p.24` ``(원본 쪽, 책 이름은 `check_note.json`에 등록한 이름) · 판서 장면 `mm:ss`. 판서·교재 수식은 LaTeX로 옮기고, 읽기 애매한 글자는 추측하지 않고 `[원문 미확인]`과 노트 끝 「판독 불확실 모음」 표에 모읍니다
3. **설명 붙이기** — 원문 밖 설명은 `[외부 추론]`, 근거를 못 찾은 곳은 `[정보 없음]`. 쉬운 설명과 별도로 정확한 정의·성립 조건을 좌표와 함께 적습니다(METHOD §3)
4. **계산 심기** — 계산한 곳마다 `<!-- 검산: M([[1,2],[3,4]]).T == M([[1,3],[2,4]]) -->`처럼 식을 심어 둡니다
5. **검사** — `lnb check 노트.md`: 영상 인용이 자막에, 교재 인용이 원문 md(`lnb pages`)의 그 쪽에 글자 그대로 있는지, 시각이 맞는지, 검산식이 성립하는지. 통과할 때까지 고칩니다. 판서 인용은 아직 대조하지 못합니다
6. **사람·다른 모델이 볼 것** — 판서·교재 수식 옮김, 판독 불확실 모음, 번역, 개념의 옳고 그름은 검사기가 못 봅니다. 노트를 쓴 모델이 아닌 다른 모델에게 검토를 맡기고 지적을 원문으로 확인합니다(METHOD §4)

## 설치

```bash
pipx install git+https://github.com/yamf97/lecture-note-bench
lnb --help      # 하위 명령과 흐름
lnb doctor      # 바깥 프로그램·whisper 모델 점검. 빠진 것은 설치 명령을 알려 줍니다
```

- 패키지 이름은 `lecture-note-bench`, 명령은 `lnb`입니다. Python 3.9 이상
- 버전별 바뀐 점은 [CHANGELOG.md](CHANGELOG.md). 특정 버전 설치: `pipx install --force git+https://github.com/yamf97/lecture-note-bench@v0.2.0`, 최신으로: `pipx upgrade lecture-note-bench`
- **macOS에서 만들고 시험했습니다.** 리눅스·윈도우는 아직 시험하지 않았습니다 (파이썬과 바깥 프로그램은 거기에도 있지만, 설치 안내와 한글 출력 등은 확인 전입니다)
- yt-dlp·youtube-transcript-api는 같이 깔립니다. ffmpeg·whisper-cli·pdftotext 같은 바깥 프로그램은 `lnb doctor`가 없는 것과 설치법을 알려 줍니다 (macOS: `brew install ffmpeg whisper-cpp poppler`)
- **whisper 모델은 받아쓰기(`transcribe`)에만** 필요합니다. 자막이 있는 강의만 다루면 없어도 됩니다. 쓸 때는 ggml 모델 파일 하나를 받아 둡니다:

  ```bash
  mkdir -p ~/.cache/whisper.cpp
  curl -L -o ~/.cache/whisper.cpp/ggml-large-v3-turbo-q5_0.bin \
    https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin   # 약 574MB
  ```

  `~/.cache/whisper.cpp/`·`~/models/whisper/`에 두면 저절로 찾습니다. 다른 곳에 두었으면 `export WHISPER_MODEL=<파일 경로>` 또는 `lnb transcribe -m <파일 경로>`
- 설치하지 않고 저장소에서 바로 `python3 tools/<도구>.py …`로 불러도 똑같이 돕니다 (`tools/`는 `src/lnb/`를 부르는 껍데기)

## 하위 명령

| 명령 (`tools/` 파일) | 하는 일 |
|---|---|
| `lnb fetch` (`fetch.py`) | 영상 사이트에서 강의 자막(필요하면 영상·음성)을 받습니다. 강의당 요청 1번, 20–40초 무작위 대기, 차단 응답이면 즉시 멈춤(종료 코드 2), 다시 돌리면 이어받기. 재생목록·id 목록은 강좌 폴더의 `fetch.json`, 한 편은 `--url`. 자막이 없으면 `--transcribe-missing`으로 로컬 전사. **아래 「자료를 받을 때」를 먼저 읽어 주세요** |
| `lnb transcribe` (`transcribe.py`) | 자막이 없는 강의의 음성·영상을 로컬 whisper(whisper.cpp)로 받아써 `<이름> (whisper).srt`를 만듭니다. 밖으로 보내는 것 없이 이 컴퓨터에서만 돕니다. 끝 시각이 음성보다 많이 짧으면 경고합니다 |
| `lnb text` (`vtt_text.py`) | 자막을 30초 단위 `[mm:ss]` 읽기본으로 바꿉니다(`--cues`는 큐마다 정확한 시각). 사람이 단 VTT, 자동 자막(yt-dlp), SRT, youtube_transcript_api 출력을 읽습니다 |
| `lnb frames` (`frames.py`) | 강의 영상에서 판서·슬라이드 장면을 시각과 함께 뽑습니다. 화면이 크게 바뀌기 **직전**(지우기 전 가득 찬 칠판)을 고르고, 빈 구간은 간격으로 채우고, 새 글씨가 없는 장면은 버립니다. `--at`으로 직접 고르고, `--scores`로 강좌에 맞는 기준을 정합니다 |
| `lnb check` (`check_note.py`) | 노트 검사기. 인용이 자막에 글자 그대로 있는지, 적은 시각이 그 말이 시작되는 시각과 맞는지, 심어 둔 검산식이 성립하는지 확인합니다. 저장소마다 `check_note.json`으로 강좌 목록, 라벨 인용(`원문 "…"`, 여러 강의 중 어디든), PDF 자료, 시각 범위, 공백 무시 대조(한국어 자막용), 용어·기호 설명 빠짐 검사를 켭니다 |
| `lnb pages` (`pages.py`) | 교재·강의록을 쪽 표시가 든 원문 md(`<!-- p.68 (PDF 78) -->`)로 정리합니다. MinerU 결과(json)나 글자 층이 있는 PDF를 받고, 변환기는 직접 부르지 않습니다. `lnb check`의 교재 인용 대조에 씁니다 |
| `lnb doctor` | 바깥 프로그램·whisper 모델이 있는지 보고 설치법을 알립니다. 빠진 것이 있으면 종료 코드 1 |
| (`tools/run_gateway.py`만) | 같은 프롬프트를 OpenAI 호환 게이트웨이(OpenRouter 등)의 여러 모델에 보내고 결과를 저장합니다. 아래 실험에 썼습니다. `lnb`에는 넣지 않았습니다 |

### 실행

```bash
# 강의 한 편 받기 (자막 + 판서용 영상, 자막 없으면 로컬 전사)
lnb fetch --url <영상 주소> -o 강좌폴더 --video --transcribe-missing -l ko

# 재생목록: 강좌 폴더에 fetch.json 을 두고 (형식은 lnb fetch --help) 한 번에 10편씩
lnb fetch 강좌폴더 --max 10

# 자막이 없는 녹음을 받아쓰기 → "강의 (whisper).srt"
lnb transcribe 강의.mp3 -l ko

# 읽기본 (정확한 시각은 --cues)
lnb text lectures/Strang_2020_vision_LA/00-intro.vtt --cues

# 판서 장면 → 강의_frames/mm-ss.jpg + index.tsv (처음 쓰는 강좌는 --scores 로 기준부터)
lnb frames 강의.mp4 --scores
lnb frames 강의.mp4
lnb frames 강의.mp4 --at 05:32,12:00

# 노트 검사: 이 저장소의 실험 결과 (저장소 안에서)
lnb check experiments/results/*.md

# 다른 저장소의 노트: 그 저장소 뿌리에 check_note.json 을 두고 (형식은 lnb check --help)
lnb check --all
lnb check 노트.md --lectures 1 2 6
```

### 알아 둘 점

- **자동 자막의 반복**: 자동 자막은 앞 큐의 줄을 다음 큐에서 되풀이합니다. `lnb text`는 단어별 시각이 붙은 자막에서만, 시각 태그가 없는 반복 줄을 버립니다. 새로 나온 말에는 늘 시각이 붙으므로 강사가 같은 말을 연달아 해도 둘 다 남고, 사람이 단 자막은 건드리지 않습니다
- **장면 기준은 강의마다 다릅니다**: 판서를 조금 지우는 순간은 장면 점수가 0.05–0.14로 낮고, 펜으로 서서히 쓰는 강의는 점수가 거의 0입니다. 그래서 기본값은 낮게(0.05) 잡고 빈 구간을 30초 간격으로 채웁니다. 강사의 움직임이 많은 강의는 `--scores`로 확인하세요
- **장면 감지**는 [claude-video](https://github.com/bradautomates/claude-video)(MIT)의 방식(ffmpeg 장면 점수 + 썸네일 비교)을 참고해, 판서 강의에 맞게 「바뀌기 직전」 장면과 「바뀐 화소 수」 판정으로 바꿨습니다
- `tools/run_gateway.py`는 지시서 파일에서 `=====` 두 줄 사이만 보냅니다. API 키는 환경변수·설정 파일에서만 읽고 출력하지 않습니다

## Claude Code 스킬로 쓰기

`skills/lecture-note/`는 위 도구를 Claude Code가 순서대로 부르게 하는 스킬입니다. 「이 강의 노트 만들어 줘」처럼 말하면 받기 → 읽기본 → 판서 장면 → 노트 → 검사로 진행하고, 판서를 옮긴 부분은 사람이 확인하도록 따로 모읍니다.

```bash
pipx install git+https://github.com/yamf97/lecture-note-bench    # 도구 (lnb)
git clone https://github.com/yamf97/lecture-note-bench.git           # 스킬 파일
ln -s "$PWD/lecture-note-bench/skills/lecture-note" ~/.claude/skills/lecture-note
```

스킬은 `lnb`를 부릅니다. 설치하지 않았으면 링크 너머 저장소의 `tools/`를 대신 부릅니다. 링크 대신 복사했다면 스킬 안의 `T=` 줄을 저장소 경로로 바꾸세요.

## 자료를 받을 때

`lnb fetch`는 영상 사이트(YouTube 등)에서 자막·영상·음성을 받는 도구입니다. **받을 권리가 있거나 허락된 자료에만** 쓰세요.

- 예: 이 저장소의 Strang 강의처럼 내려받기와 재사용을 허락하는 라이선스(MIT OpenCourseWare, CC BY-NC-SA)의 강의, 직접 만든 영상, 저작권자가 허락한 영상
- 사이트 이용약관과 각 영상의 라이선스를 지키는 것은 쓰는 사람의 책임입니다. 많은 사이트가 허락 없는 내려받기를 막습니다
- 받은 자막·영상·장면 사진은 개인 공부에만 쓰고 다시 배포하지 마세요. 이 저장소에 실린 강의 자료는 라이선스가 허락하는 것뿐입니다
- 요청을 천천히 보내는 장치(강의당 1번, 20–40초 대기, 차단 응답이면 즉시 멈춤)는 사이트에 부담을 주지 않기 위한 것입니다. 우회하는 데 쓰지 마세요

`text`·`transcribe`·`frames`·`check`는 이미 가진 파일만 다룹니다.

## 실험: 모델 다섯 개의 블라인드 비교

Gilbert Strang의 MIT OCW 강의 *A 2020 Vision of Linear Algebra* 00번 영상(4분)을 대상으로, 같은 지시서를 오픈 웨이트 모델 다섯 개에 보내고 결과를 모델 이름을 가린 채 읽어 비교했습니다.

| 위치 | 내용 |
|---|---|
| `experiments/2026-09-22_vision00_directive-prompt.md` | 모델에 보낸 지시서. 노트의 절 순서, 인용 규칙(번역 먼저, 원문과 영상 시각은 아래), 검산 주석 규칙, 자막 전문 |
| `experiments/results/A.md` ~ `E.md` | 다섯 모델이 쓴 노트 원문. 어느 모델인지는 `labels.json` |
| `experiments/2026-09-23_blind-read.md` | 블라인드로 읽은 소감, 봉인 해제, 원문과 대조해 확인한 문제점, 결론 |
| `lectures/Strang_2020_vision_LA/` | 검사기가 쓰는 00번 영상 자막 |

| 라벨 | 모델 | 읽은 사람 순위 | 검사기 실패 |
|---|---|---|---|
| E | qwen/qwen3.8-27b | 1 | 0 |
| A | qwen/qwen3.5-122b-a10b | 2 | 3 |
| D | qwen/qwen3.6-35b-a3b | A와 비슷 | 3 |
| B | qwen/qwen3.8-flash | 수식 표시 문제 | 2 |
| C | openai/gpt-oss-120b | 가장 부족 | 1 |

- 뼈대를 주면 다섯 모델 모두 노트를 채웠습니다. 남은 흠은 의역, 근거보다 먼저 나온 결론, 출력 형식 위반처럼 **사람이 읽고 잡아야 하는 종류**였습니다.
- 가장 작은 27B dense 모델이 가장 나았습니다. 크기와 품질이 비례하지 않았고, 로컬에서 돌릴 수 있는 크기로도 충분할 수 있다는 신호입니다.
- 과제 하나, 모델당 한 번 돌린 결과라서 결론이 아니라 관찰입니다.

```bash
# 같은 지시서를 다른 모델에 보내기 (OPENROUTER_API_KEY 필요)
python3 tools/run_gateway.py --base-url https://openrouter.ai/api/v1 \
  --model qwen/qwen3.8-27b --reasoning high --stream \
  --prompt experiments/2026-09-22_vision00_directive-prompt.md \
  --out experiments/results/new.md
```

## 출처와 라이선스

- 강의 자막과 슬라이드 내용: Gilbert Strang, *A 2020 Vision of Linear Algebra* (MIT OpenCourseWare RES.18-010, Spring 2020), [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). `lectures/`의 VTT는 OCW 자막에서 큐 시작 시각(초 단위)을 살려 다시 만든 것입니다.
- 지시서, 실험 기록, 모델이 쓴 노트(`experiments/`)도 강의 내용을 담고 있으므로 같은 CC BY-NC-SA 4.0으로 공개합니다.
- 도구 코드(`src/lnb/`·`tools/`)와 스킬(`skills/`)은 MIT License입니다. `lnb frames`의 장면 감지는 claude-video(Bradley Bonanno, MIT)를 참고했습니다.
- 교재(*Introduction to Linear Algebra*)는 절 제목만 참고했고 본문은 싣지 않았습니다.

---

## English

> **Latest: 0.2.0** (2026-11-18). This version adds the textbook quote check: the new `lnb pages` command turns a textbook or handout into page-marked text, and `lnb check` then checks textbook quotes against the cited page. An installed `lnb check` now needs a `check_note.json` in each repository. See [CHANGELOG.md](CHANGELOG.md) for all changes, and update with `pipx upgrade lecture-note-bench`.

### What this is

Tools for turning lecture videos into **study notes that stay faithful to their sources**, plus a small experiment that tested the method.

- **`lnb` command-line tool**: prepares the raw material (captions, reading text, board and slide frames, page-marked textbook text) and mechanically checks finished notes against it. Works without any AI.
- **Claude Code skill** (`skills/lecture-note/`): walks Claude Code through the tools in order.
- **Experiment**: five open-weight models wrote a note from the same instruction sheet, and the results were compared blind.

Note-writing rules are in [METHOD.md](METHOD.md) (Korean). The code was written with Claude Code. I made the design, the verification rules, the experiment and the blind judging. Changes are reviewed by a model from another company (Codex) and covered by regression tests. AI-written commits are marked `[AI:<model>]`.

### Pipeline

```
lecture URL ─ lnb fetch ─┬─ captions ─────────────────────┐
                         └─ none → lnb transcribe ────────┼─ lnb text ─ write note ─ lnb check
        video ─ lnb frames (board / slide frames) ────────┤
   textbook / slide PDF ─ convert to md ─ lnb pages ──────┘
```

A person (or an AI) writes the note. The tools prepare the material before writing and check the evidence after it. Board transcriptions cannot be checked automatically. Unclear readings are collected in a table so that a person can compare them with the frame images.

### Writing a note

1. **Read**: get the flow from the 30-second reading text (`lnb text`), and find exact times with `--cues`.
2. **Quote**: copy quotes verbatim, each followed by its source: video `[Vision 00 01:47]`, textbook ``"…" `Strang ILA §3.2 p.24` `` (the book name as registered in `check_note.json`, so `lnb check` can find it), or board frame `mm:ss`. Mark unclear readings `[원문 미확인]` (unverified) instead of guessing.
3. **Explain**: tag explanations from outside the source `[외부 추론]` (outside inference), and tag points with no source `[정보 없음]` (not in source).
4. **Embed checks**: wherever you calculate, embed a check such as `<!-- 검산: M([[1,2],[3,4]]).T == M([[1,3],[2,4]]) -->`.
5. **Check**: run `lnb check note.md` and fix the note until it passes.
6. **Review**: a different model reviews what the checker cannot see, such as board math, translations and correctness.

### Install

```bash
pipx install git+https://github.com/yamf97/lecture-note-bench
lnb --help
lnb doctor   # checks ffmpeg, whisper-cli, pdftotext and the whisper model, and prints install commands
```

- Requires Python 3.9+. **Built and tested on macOS only**; Linux and Windows are untested.
- Changes by version are in [CHANGELOG.md](CHANGELOG.md). To pin a version, use `pipx install --force git+https://github.com/yamf97/lecture-note-bench@v0.2.0`; to update, use `pipx upgrade lecture-note-bench`.
- You need a whisper model only for `transcribe`. Put a ggml model file in `~/.cache/whisper.cpp/` or set `WHISPER_MODEL`.
- You can run the tools without installing: `python3 tools/<file>.py`. The files are `fetch.py`, `transcribe.py`, `vtt_text.py` (`text`), `frames.py`, `pages.py` and `check_note.py` (`check`); `doctor` needs the installed `lnb`.

### Commands

| Command | What it does |
|---|---|
| `lnb fetch` | Downloads captions, plus video or audio if needed. Makes one request per lecture, waits 20–40 s at random, stops immediately if blocked, and resumes on re-run. |
| `lnb transcribe` | Transcribes audio locally with whisper.cpp when a lecture has no captions. Nothing leaves the machine. |
| `lnb text` | Turns VTT or SRT captions into 30-second `[mm:ss]` reading text; `--cues` keeps exact cue times. |
| `lnb frames` | Picks board and slide frames just **before** each large change, such as a full board before erasing. `--scores` helps tune the threshold for each course. |
| `lnb pages` | Turns textbook or handout text (MinerU JSON or a PDF with a text layer) into page-marked md for quote checking. |
| `lnb check` | Checks finished notes: video quotes against the captions at the stated time, textbook quotes against the cited page, and embedded calculations. Each repository configures it with `check_note.json`. |
| `lnb doctor` | Reports missing external programs and models. |

**Textbooks and slides**: convert them to md with existing tools, [MinerU](https://github.com/opendatalab/MinerU) for PDFs (`-b pipeline` is about 6× faster) or [MarkItDown](https://github.com/microsoft/markitdown) for Office files. For quote checking, run `lnb pages` on MinerU's `*_content_list.json` or on a PDF with a text layer, and register the result under `books` in `check_note.json`. MarkItDown output has no page numbers, so `lnb pages` cannot use it. Do not trust conversions blindly: compare transcribed formulas with the page image. Converted textbooks are copyrighted, so keep them out of public repositories.

### Experiment: five models, read blind

Five open-weight models received the same instruction sheet for a note on Gilbert Strang's *A 2020 Vision of Linear Algebra*, video 00 (MIT OCW). I read the results with the model names hidden.

- All five filled the given structure. The remaining flaws were paraphrase, conclusions placed before their evidence, and format violations, **the kind a human reader has to catch**.
- The smallest model, `qwen/qwen3.8-27b` (dense), did best. Size did not track quality.
- This was one task with one run per model, so it is an observation, not a conclusion.

The details are in `experiments/` (Korean).

### Downloading responsibly

Use `lnb fetch` only for material you have the right or permission to download, such as CC-licensed OCW lectures or your own videos. Follow each site's terms and each video's license, and do not redistribute what you download. The rate limiting exists to spare the site, so do not work around it.

### License

- Lecture content and `experiments/`: CC BY-NC-SA 4.0 (MIT OpenCourseWare RES.18-010).
- Tool code (`src/lnb/`, `tools/`) and skills (`skills/`): MIT. Frame detection in `lnb frames` was adapted from [claude-video](https://github.com/bradautomates/claude-video) (MIT).

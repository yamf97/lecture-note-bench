# lecture-note-bench

강의 영상으로 **근거를 지키는 학습 노트**를 만드는 도구와, 그 방법을 시험한 실험입니다.

- **도구**: 강의 자막·영상을 받아 읽기본과 판서 장면을 만들고, 다 쓴 노트의 인용·시각·계산을 원문과 기계로 대조합니다 (`tools/`, AI 없이도 쓰는 명령줄 도구)
- **스킬**: 그 도구를 Claude Code가 순서대로 부르게 하는 안내서 (`skills/lecture-note/`)
- **실험**: 같은 지시서로 오픈 웨이트 모델 다섯 개에게 노트를 쓰게 하고 모델 이름을 가린 채 비교했습니다

선형대수·계량경제학을 다시 공부하면서 실제로 쓰는 방법을 정리한 것입니다. 노트 작성 규칙은 [METHOD.md](METHOD.md)에 있습니다.

## 흐름

```
강의 주소 ─ fetch ─┬─ 자막 있음 ───────────────┐
                   └─ 없음 → transcribe(전사) ─┼─ vtt_text 읽기본 ─ 노트 쓰기 ─ check_note 검사
        영상 ─ frames(판서·슬라이드 장면) ──────┘
```

노트 쓰기는 사람(또는 AI)이 합니다. 도구는 그 앞의 재료를 만들고, 뒤에서 근거를 확인합니다. 판서를 옮긴 부분은 검사기가 대조할 수 없으므로, 읽기 애매한 곳을 따로 모아 사람이 장면 사진과 맞춰 봅니다.

## 도구 (`tools/`)

| 도구 | 하는 일 |
|---|---|
| `fetch.py` | 영상 사이트에서 강의 자막(필요하면 영상·음성)을 받습니다. 강의당 요청 1번, 20–40초 무작위 대기, 차단 응답이면 즉시 멈춤, 다시 돌리면 이어받기. 재생목록·id 목록은 강좌 폴더의 `fetch.json`, 한 편은 `--url`. 자막이 없으면 `--transcribe-missing`으로 로컬 전사. **아래 「자료를 받을 때」를 먼저 읽어 주세요** |
| `transcribe.py` | 자막이 없는 강의의 음성·영상을 로컬 whisper(whisper.cpp)로 받아써 `<이름> (whisper).srt`를 만듭니다. 밖으로 보내는 것 없이 이 컴퓨터에서만 돕니다. 끝 시각이 음성보다 많이 짧으면 경고합니다 |
| `vtt_text.py` | 자막을 30초 단위 `[mm:ss]` 읽기본으로 바꿉니다(`--cues`는 큐마다 정확한 시각). 사람이 단 VTT, 자동 자막(yt-dlp), SRT, youtube_transcript_api 출력을 읽습니다 |
| `frames.py` | 강의 영상에서 판서·슬라이드 장면을 시각과 함께 뽑습니다. 화면이 크게 바뀌기 **직전**(지우기 전 가득 찬 칠판)을 고르고, 빈 구간은 간격으로 채우고, 새 글씨가 없는 장면은 버립니다. `--at`으로 직접 고르고, `--scores`로 강좌에 맞는 기준을 정합니다 |
| `check_note.py` | 노트 검사기. 인용이 자막에 글자 그대로 있는지, 적은 시각이 그 말이 시작되는 시각과 맞는지, 심어 둔 검산식이 성립하는지 확인합니다. 저장소마다 `check_note.json`으로 강좌 목록, 라벨 인용(`원문 "…"`, 여러 강의 중 어디든), PDF 자료, 시각 범위, 공백 무시 대조(한국어 자막용), 용어·기호 설명 빠짐 검사를 켭니다 |
| `run_gateway.py` | 같은 프롬프트를 OpenAI 호환 게이트웨이(OpenRouter 등)의 여러 모델에 보내고 결과를 저장합니다. 아래 실험에 썼습니다 |

### 필요한 것

- Python 3.9 이상. `vtt_text.py`·`check_note.py`는 표준 라이브러리만 씁니다
- `fetch.py`: [yt-dlp](https://github.com/yt-dlp/yt-dlp), (재생목록 자막) youtube_transcript_api
- `transcribe.py`: ffmpeg, whisper.cpp의 `whisper-cli`, ggml 모델 파일
- `frames.py`: ffmpeg
- `check_note.py`의 PDF 인용 대조: pdftotext

### 실행

```bash
# 강의 한 편 받기 (자막 + 판서용 영상, 자막 없으면 로컬 전사)
python3 tools/fetch.py --url <영상 주소> -o 강좌폴더 --video --transcribe-missing -l ko

# 재생목록: 강좌 폴더에 fetch.json 을 두고 (형식은 fetch.py 머리말) 한 번에 10편씩
python3 tools/fetch.py 강좌폴더 --max 10

# 자막이 없는 녹음을 받아쓰기 → "강의 (whisper).srt"
python3 tools/transcribe.py 강의.mp3 -l ko

# 읽기본 (정확한 시각은 --cues)
python3 tools/vtt_text.py lectures/Strang_2020_vision_LA/00-intro.vtt --cues

# 판서 장면 → 강의_frames/mm-ss.jpg + index.tsv (처음 쓰는 강좌는 --scores 로 기준부터)
python3 tools/frames.py 강의.mp4 --scores
python3 tools/frames.py 강의.mp4
python3 tools/frames.py 강의.mp4 --at 05:32,12:00

# 노트 검사: 이 저장소의 실험 결과
python3 tools/check_note.py experiments/results/*.md

# 다른 저장소의 노트: 그 저장소 뿌리에 check_note.json 을 두고 (형식은 check_note.py 머리말)
python3 tools/check_note.py --all
python3 tools/check_note.py 노트.md --lectures 1 2 6
```

### 알아 둘 점

- **자동 자막의 반복**: 자동 자막은 앞 큐의 줄을 다음 큐에서 되풀이합니다. `vtt_text.py`는 단어별 시각이 붙은 자막에서만, 시각 태그가 없는 반복 줄을 버립니다. 새로 나온 말에는 늘 시각이 붙으므로 강사가 같은 말을 연달아 해도 둘 다 남고, 사람이 단 자막은 건드리지 않습니다
- **장면 기준은 강의마다 다릅니다**: 판서를 조금 지우는 순간은 장면 점수가 0.05–0.14로 낮고, 펜으로 서서히 쓰는 강의는 점수가 거의 0입니다. 그래서 기본값은 낮게(0.05) 잡고 빈 구간을 30초 간격으로 채웁니다. 강사의 움직임이 많은 강의는 `--scores`로 확인하세요
- **장면 감지**는 [claude-video](https://github.com/bradautomates/claude-video)(MIT)의 방식(ffmpeg 장면 점수 + 썸네일 비교)을 참고해, 판서 강의에 맞게 「바뀌기 직전」 장면과 「바뀐 화소 수」 판정으로 바꿨습니다
- `run_gateway.py`는 지시서 파일에서 `=====` 두 줄 사이만 보냅니다. API 키는 환경변수·설정 파일에서만 읽고 출력하지 않습니다

## Claude Code 스킬로 쓰기

`skills/lecture-note/`는 위 도구를 Claude Code가 순서대로 부르게 하는 스킬입니다. 「이 강의 노트 만들어 줘」처럼 말하면 받기 → 읽기본 → 판서 장면 → 노트 → 검사로 진행하고, 판서를 옮긴 부분은 사람이 확인하도록 따로 모읍니다.

```bash
git clone https://github.com/yamf97/lecture-note-bench.git
ln -s "$PWD/lecture-note-bench/skills/lecture-note" ~/.claude/skills/lecture-note
```

스킬은 도구를 링크 너머 저장소의 `tools/`에서 찾습니다. 링크 대신 복사했다면 스킬 안의 `T=` 줄을 저장소 경로로 바꾸세요.

## 자료를 받을 때

`fetch.py`는 영상 사이트(YouTube 등)에서 자막·영상·음성을 받는 도구입니다. **받을 권리가 있거나 허락된 자료에만** 쓰세요.

- 예: 이 저장소의 Strang 강의처럼 내려받기와 재사용을 허락하는 라이선스(MIT OpenCourseWare, CC BY-NC-SA)의 강의, 직접 만든 영상, 저작권자가 허락한 영상
- 사이트 이용약관과 각 영상의 라이선스를 지키는 것은 쓰는 사람의 책임입니다. 많은 사이트가 허락 없는 내려받기를 막습니다
- 받은 자막·영상·장면 사진은 개인 공부에만 쓰고 다시 배포하지 마세요. 이 저장소에 실린 강의 자료는 라이선스가 허락하는 것뿐입니다
- 요청을 천천히 보내는 장치(강의당 1번, 20–40초 대기, 차단 응답이면 즉시 멈춤)는 사이트에 부담을 주지 않기 위한 것입니다. 우회하는 데 쓰지 마세요

`vtt_text.py`·`transcribe.py`·`frames.py`·`check_note.py`는 이미 가진 파일만 다룹니다.

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
- 도구 코드(`tools/`)와 스킬(`skills/`)은 MIT License입니다. `frames.py`의 장면 감지는 claude-video(Bradley Bonanno, MIT)를 참고했습니다.
- 교재(*Introduction to Linear Algebra*)는 절 제목만 참고했고 본문은 싣지 않았습니다.

---

**In English.** Tools for turning lecture videos into study notes that keep to their sources, plus a small experiment. The tools fetch captions (and, if needed, video or audio), transcribe locally with whisper.cpp when there are no captions, turn captions into 30-second reading text, pick board and slide frames just before each large change, and check finished notes (a Claude Code skill in `skills/lecture-note/` chains them): every quote must appear verbatim in the captions at the stated time, and inline calculations must hold. In the experiment, five open-weight models got the same instruction sheet for a note on MIT OCW RES.18-010 video 00 and I read the results blind; the smallest model (a 27B dense model) did best, from a single run, so it is an observation, not a conclusion. Lecture content is CC BY-NC-SA 4.0 (MIT OCW), and the tools are MIT-licensed. `fetch.py` downloads from video sites such as YouTube: use it only for material you have the right or permission to download (e.g. CC-licensed OCW lectures), follow the site's terms and each video's license, and do not redistribute what you download.

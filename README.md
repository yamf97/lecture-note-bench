# lecture-note-bench

강의 자막으로 학습 노트를 만들 때, 여러 언어모델이 **근거를 지키며** 노트를 쓰는지 비교해 본 작은 실험과 도구입니다.

Gilbert Strang의 MIT OCW 강의 *A 2020 Vision of Linear Algebra* 00번 영상(4분)을 대상으로, 같은 지시서를 오픈 웨이트 모델 다섯 개에 보내고 결과를 모델 이름을 가린 채 읽어 비교했습니다. 제가 선형대수를 다시 공부하면서 쓰는 방법을 정리한 것입니다.

## 무엇이 들어 있나

| 위치 | 내용 |
|---|---|
| `METHOD.md` | AI로 학습 노트를 만들 때 쓰는 규칙: 근거 표시, 기계 검사, 노트 짜임, 여러 모델로 검토하는 법과 그 결과 |
| `experiments/2026-09-22_vision00_directive-prompt.md` | 모델에 보낸 지시서. 노트의 절 순서, 인용 규칙(번역 먼저, 원문과 영상 시각은 아래), 검산 주석 규칙, 자막 전문이 들어 있습니다 |
| `experiments/results/A.md` ~ `E.md` | 다섯 모델이 쓴 노트 원문. 어느 모델인지는 `labels.json`에 있습니다 |
| `experiments/2026-09-23_blind-read.md` | 블라인드로 읽은 소감, 봉인 해제, 원문과 대조해 확인한 문제점, 결론 |
| `tools/check_note.py` | 노트 검사기. 인용이 자막에 글자 그대로 있는지, 적은 시각이 그 말이 시작되는 시각과 맞는지, 행렬 검산식이 성립하는지 확인합니다. 저장소마다 `check_note.json`으로 강의 목록, 라벨 인용(`원문 "…"`, 여러 강의 중 어디든), PDF 자료, 시각 범위 검사, 공백 무시 대조(한국어 자막용), 용어·기호 설명 빠짐 검사를 켤 수 있습니다 |
| `tools/vtt_text.py` | 자막을 읽기 좋은 평문으로 바꿉니다. 사람이 단 VTT, YouTube 자동 자막(yt-dlp), SRT(whisper 출력 등), youtube_transcript_api 출력을 읽습니다 |
| `tools/fetch.py` | YouTube에서 강의 자막(필요하면 영상·음성)을 받습니다. 강의당 요청 1번, 20–40초 무작위 대기, 차단 응답이면 즉시 멈춤, 다시 돌리면 이어받기. 재생목록·id 목록은 강좌 폴더의 `fetch.json`, 한 편은 `--url`. 자막이 없으면 `--transcribe-missing`으로 로컬 전사 |
| `tools/transcribe.py` | 자막이 없는 강의의 음성·영상을 로컬 whisper(whisper.cpp)로 받아써 SRT를 만듭니다. 밖으로 보내는 것 없이 이 컴퓨터에서만 돕니다. 결과는 `vtt_text.py`·`check_note.py`가 그대로 읽습니다 |
| `tools/frames.py` | 강의 영상에서 판서·슬라이드 장면을 시각과 함께 뽑습니다. 화면이 크게 바뀌기 **직전**(지우기 전 가득 찬 칠판)을 고르고, 빈 구간은 간격으로 채우고, 같은 장면은 버립니다. `--at`으로 직접 고를 수도 있습니다. 장면 감지는 [claude-video](https://github.com/bradautomates/claude-video)(MIT)의 방식을 참고했습니다 |
| `tools/run_gateway.py` | 같은 프롬프트를 OpenAI 호환 게이트웨이(OpenRouter 등)의 여러 모델에 보내고 결과를 저장합니다 |
| `lectures/Strang_2020_vision_LA/` | 검사기가 쓰는 00번 영상 자막 |

## 결과 요약

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

## 실행

표준 라이브러리만 씁니다(Python 3.9 이상).

```bash
# 다섯 결과를 검사
python3 tools/check_note.py experiments/results/*.md

# 다른 저장소의 노트 검사: 그 저장소 뿌리에 check_note.json 을 두고 (형식은 check_note.py 머리말)
python3 tools/check_note.py --all            # 설정의 "all" 폴더 전체
python3 tools/check_note.py 노트.md --course 과목 --lecture 3

# 자막을 평문으로 (정확한 시각은 --cues)
python3 tools/vtt_text.py lectures/Strang_2020_vision_LA/00-intro.vtt --cues

# 강의 한 편 받기 (자막 + 판서용 영상, 자막 없으면 로컬 전사)
python3 tools/fetch.py --url <영상 주소> -o 강좌폴더 --video --transcribe-missing -l ko

# 자막이 없으면 음성을 받아씁니다 (whisper-cli·ffmpeg·ggml 모델 필요) → "강의 (whisper).srt"
python3 tools/transcribe.py 강의.mp3 -l ko

# 판서 장면 뽑기 → 강의_frames/mm-ss.jpg + index.tsv (처음 쓰는 강좌는 --scores 로 기준부터)
python3 tools/frames.py 강의.mp4
python3 tools/frames.py 강의.mp4 --at 05:32,12:00

# YouTube 자동 자막도 그대로 넣으면 됩니다
yt-dlp --skip-download --write-auto-subs --sub-langs en-orig -o lecture <URL>
python3 tools/vtt_text.py lecture.en-orig.vtt

# 같은 지시서를 다른 모델에 보내기 (OPENROUTER_API_KEY 필요)
python3 tools/run_gateway.py --base-url https://openrouter.ai/api/v1 \
  --model qwen/qwen3.8-27b --reasoning high --stream \
  --prompt experiments/2026-09-22_vision00_directive-prompt.md \
  --out experiments/results/new.md
```

YouTube 자동 자막은 앞 큐의 줄을 다음 큐에서 되풀이합니다. 그대로 이어 붙이면 같은 구절이 두세 번 나오고 시각도 밀립니다. `vtt_text.py`는 바로 앞 줄과 같은 줄을 버려서, 구절마다 처음 나온 시각에 한 번만 남깁니다. 그래서 강사가 같은 말을 연달아 두 번 하면 그것도 한 번으로 합쳐집니다.

`run_gateway.py`는 지시서 파일에서 `=====` 두 줄 사이만 보냅니다. API 키는 환경변수에서만 읽고 출력하지 않습니다.

## 자료를 받을 때

`fetch.py`는 영상 사이트(YouTube 등)에서 자막·영상·음성을 받는 도구입니다. **받을 권리가 있거나 허락된 자료에만** 쓰세요.

- 예: 이 저장소의 Strang 강의처럼 내려받기와 재사용을 허락하는 라이선스(MIT OpenCourseWare, CC BY-NC-SA)의 강의, 직접 만든 영상, 저작권자가 허락한 영상
- 사이트 이용약관과 각 영상의 라이선스를 지키는 것은 쓰는 사람의 책임입니다. 많은 사이트가 허락 없는 내려받기를 막습니다
- 받은 자막·영상·장면 사진은 개인 공부에만 쓰고 다시 배포하지 마세요. 이 저장소에 실린 강의 자료는 라이선스가 허락하는 것뿐입니다
- 요청을 천천히 보내는 장치(강의당 1번, 20–40초 대기, 차단 응답이면 즉시 멈춤)는 사이트에 부담을 주지 않기 위한 것입니다. 우회하는 데 쓰지 마세요

`vtt_text.py`·`transcribe.py`·`frames.py`·`check_note.py`는 이미 가진 파일만 다룹니다.

## 출처와 라이선스

- 강의 자막과 슬라이드 내용: Gilbert Strang, *A 2020 Vision of Linear Algebra* (MIT OpenCourseWare RES.18-010, Spring 2020), [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). `lectures/`의 VTT는 OCW 자막에서 큐 시작 시각(초 단위)을 살려 다시 만든 것입니다.
- 지시서, 실험 기록, 모델이 쓴 노트(`experiments/`)도 강의 내용을 담고 있으므로 같은 CC BY-NC-SA 4.0으로 공개합니다.
- 도구 코드(`tools/`)는 MIT License입니다.
- 교재(*Introduction to Linear Algebra*)는 절 제목만 참고했고 본문은 싣지 않았습니다.

---

**In English.** A small experiment on generating study notes from lecture subtitles. Five open-weight models got the same instruction sheet for a note on MIT OCW RES.18-010 video 00, and I read the results blind. A stdlib-only checker verifies that every quote appears verbatim in the subtitles at the stated timestamp, and that the inline matrix checks hold. The smallest model (a 27B dense model) did best. That's a single run, so treat it as an observation, not a conclusion. Lecture content is CC BY-NC-SA 4.0 (MIT OCW), and the tools are MIT-licensed. `fetch.py` downloads captions and media from video sites such as YouTube: use it only for material you have the right or permission to download (e.g. CC-licensed OCW lectures), follow the site's terms and each video's license, and do not redistribute what you download.

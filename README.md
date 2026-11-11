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
| `tools/check_note.py` | 노트 검사기. 인용이 자막에 글자 그대로 있는지, 적은 시각이 그 말이 시작되는 시각과 맞는지, 행렬 검산식이 성립하는지 확인합니다 |
| `tools/vtt_text.py` | VTT 자막을 읽기 좋은 평문으로 바꿉니다 |
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

# 자막을 평문으로 (정확한 시각은 --cues)
python3 tools/vtt_text.py lectures/Strang_2020_vision_LA/00-intro.vtt --cues

# 같은 지시서를 다른 모델에 보내기 (OPENROUTER_API_KEY 필요)
python3 tools/run_gateway.py --base-url https://openrouter.ai/api/v1 \
  --model qwen/qwen3.8-27b --reasoning high --stream \
  --prompt experiments/2026-09-22_vision00_directive-prompt.md \
  --out experiments/results/new.md
```

`run_gateway.py`는 지시서 파일에서 `=====` 두 줄 사이만 보냅니다. API 키는 환경변수에서만 읽고 출력하지 않습니다.

## 출처와 라이선스

- 강의 자막과 슬라이드 내용: Gilbert Strang, *A 2020 Vision of Linear Algebra* (MIT OpenCourseWare RES.18-010, Spring 2020), [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). `lectures/`의 VTT는 OCW 자막에서 큐 시작 시각(초 단위)을 살려 다시 만든 것입니다.
- 지시서, 실험 기록, 모델이 쓴 노트(`experiments/`)도 강의 내용을 담고 있으므로 같은 CC BY-NC-SA 4.0으로 공개합니다.
- 도구 코드(`tools/`)는 MIT License입니다.
- 교재(*Introduction to Linear Algebra*)는 절 제목만 참고했고 본문은 싣지 않았습니다.

---

**In English.** A small experiment on generating study notes from lecture subtitles. Five open-weight models got the same instruction sheet for a note on MIT OCW RES.18-010 video 00, and I read the results blind. A stdlib-only checker verifies that every quote appears verbatim in the subtitles at the stated timestamp, and that the inline matrix checks hold. The smallest model (a 27B dense model) did best. That's a single run, so treat it as an observation, not a conclusion. Lecture content is CC BY-NC-SA 4.0 (MIT OCW), and the tools are MIT-licensed.

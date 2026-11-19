# lecture-note-bench

[English](#english)

> **0.4.0 버전이 나왔습니다** (2026-11-19)
>
> 좋아진 점
> - **0.4.0**: 강의 폴더를 통째로 받아씁니다. `lnb transcribe ~/강의 -o ~/강의자막`처럼 쓰면 하위 폴더 구조 그대로 자막을 만들고, 도중에 끊겨도 같은 명령으로 이어서 합니다.
> - 0.3.0: 녹음·영상을 글로 받아쓰는(전사) 준비를 명령 하나 `lnb setup`으로 합니다. 음성인식 모델을 받아 파일이 깨지거나 바뀌지 않았는지까지 확인합니다.
>
> 업데이트: `pipx upgrade lecture-note-bench` · 버전별 바뀐 점 전체: [CHANGELOG.md](CHANGELOG.md)

강의 영상으로 학습 노트를 만들 때, **노트에 옮긴 말이 정말 강의·교재에 있는지 확인할 수 있게** 돕는 도구입니다.
노트의 인용마다 영상 시각이나 교재 쪽을 달아 두면, 그 인용이 원문과 글자 그대로 맞는지 프로그램이 대조합니다.

이 저장소에는 세 가지가 있습니다.

- **명령줄 도구 `lnb`**: 강의 자막·영상을 받고, 읽기 좋은 본문과 판서 장면을 만들고, 다 쓴 노트를 원문과 대조합니다. AI 없이도 씁니다
- **Claude Code 스킬** (`skills/lecture-note/`): Claude Code가 위 도구를 순서대로 부르며 노트를 만들게 하는 안내서
- **실험**: 공개 모델 다섯 개에게 같은 지시로 노트를 쓰게 하고, 모델 이름을 가린 채 비교한 기록

선형대수·계량경제학을 다시 공부하면서 실제로 쓰는 방법을 정리했습니다. 노트 작성 규칙은 [METHOD.md](METHOD.md)에 있습니다.

코드는 Claude Code(AI)로 작성했습니다. 무엇을 만들지, 검증 규칙, 실험 설계와 판정은 제가 했습니다. 바뀐 코드는 다른 회사 모델(Codex)이 검토하고, 자동 시험으로 기존 기능이 깨지지 않았는지 확인한 뒤 반영합니다. AI가 쓴 커밋에는 `[AI:<모델>]` 표시가 있습니다.

## 설치

```bash
pipx install git+https://github.com/yamf97/lecture-note-bench
lnb --help      # 명령 목록과 흐름
lnb doctor      # 필요한 바깥 프로그램이 있는지 점검하고, 없으면 설치 명령을 알려 줍니다
```

자막이 없는 강의를 받아쓰려면(전사) 한 번 더 실행합니다.

```bash
lnb setup       # 음성인식 모델(약 574MB)을 받을지 묻고, 받은 파일이 원본과 같은지 확인합니다
```

- 명령은 `lnb`, 패키지 이름은 `lecture-note-bench`입니다. Python 3.9 이상이 필요합니다
- **macOS에서만 만들고 시험했습니다.** 리눅스·윈도우에서는 아직 확인하지 않았습니다
- 바깥 프로그램(ffmpeg·whisper-cli·pdftotext)은 따로 설치합니다. macOS: `brew install ffmpeg whisper-cpp poppler`
- 특정 버전 설치: `pipx install --force git+https://github.com/yamf97/lecture-note-bench@v0.4.0`

### 받아쓰기에 쓰는 프로그램 — Whisper

- **무엇인가:** 말소리를 글자로 바꾸는 음성인식 모델입니다. OpenAI가 만들어 공개했고, 한국어·영어를 포함한 여러 언어를 받아씁니다
- **공개 형식:** 코드와 모델 모두 MIT 라이선스입니다. 누구나 무료로 내려받아 쓰고 고칠 수 있습니다
- **whisper-cli:** 원래 Whisper는 Python으로 실행합니다. lnb는 ggml-org가 이를 C/C++로 다시 만든 [whisper.cpp](https://github.com/ggml-org/whisper.cpp)(MIT)를 씁니다. Python 환경 없이 `brew install whisper-cpp` 한 줄로 설치되고, 맥에서 가볍게 실행됩니다. whisper-cli는 그 안에 든 명령 이름입니다
- **왜 필요한가:** YouTube 강의는 자막을 받으면 되지만, 가지고 있는 녹음·영상 파일에는 자막이 없습니다. 노트에 옮긴 말이 강의에 정말 있는지 확인하려면 시각이 붙은 대본이 필요해서, 그 대본을 만드는 데 씁니다
- **어디서 실행되나:** 이 컴퓨터 안에서만 실행되고 음성은 밖으로 나가지 않습니다. 인터넷은 모델을 처음 받을 때만 씁니다
- **`lnb setup`이 받는 모델:** OpenAI의 large-v3-turbo를 whisper.cpp용으로 바꾸고 크기를 줄인 파일(`ggml-large-v3-turbo-q5_0.bin`, 약 574MB)입니다. 정확도는 조금 낮아지지만 맥에서 쓰기에 알맞습니다. 함께 받는 **VAD 모델**(`ggml-silero-v6.2.0.bin`, 약 0.9MB)은 녹음에서 말소리가 있는 구간만 골라 줍니다
- **쓰는 법:** 파일 하나는 `lnb transcribe 강의.mp4 -l ko`, 폴더 통째는 `lnb transcribe ~/강의 -o ~/강의자막 -l ko`. 자세한 것은 아래 「가지고 있는 녹음·영상 받아쓰기」

## 빠른 시작 — 강의 한 편

```bash
# 1. 받기: 자막과 영상. 자막이 없으면 이 컴퓨터에서 받아씁니다
lnb fetch --url <영상 주소> -o 강의자료 --video --transcribe-missing -l ko

# 2. 읽기: 자막을 30초마다 시각이 붙은 본문으로
lnb text 강의자료/raw/<자막 파일>

# 3. 판서·슬라이드 장면 뽑기 → 강의자료/video/<이름>_frames/
lnb frames 강의자료/video/<이름>.mp4

# 4. 위 재료를 보며 노트를 씁니다 (아래 「노트 쓰기」)

# 5. 검사: 노트의 인용·시각·계산이 원문과 맞는지
lnb check 노트.md
```

5번 검사는 노트가 있는 저장소에 **`check_note.json`** 을 두어, 노트의 강의 이름이 어느 자막 폴더인지 알려 줘야 합니다. 형식은 `lnb check --help`에 있습니다. 이 저장소의 [check_note.json](check_note.json)이 가장 작은 예입니다.

## 흐름과 명령

```
강의 주소 ─ fetch ─┬─ 자막 있음 ─────────────┐
                   └─ 없음 → transcribe ─────┼─ text ─ 노트 쓰기 ─ check
          영상 ─ frames (판서·슬라이드) ─────┤
  교재·슬라이드 PDF ─ md 변환 ─ pages ───────┘
```

노트는 사람(또는 AI)이 씁니다. 도구는 쓰기 전의 재료를 만들고, 쓴 뒤에 근거를 확인합니다.

| 명령 | 하는 일 |
|---|---|
| `lnb fetch` | 영상 사이트에서 강의 자막을 받습니다. 필요하면 영상·음성도. **먼저 아래 「자료를 받을 때」를 읽어 주세요** |
| `lnb transcribe` | 자막이 없는 음성·영상을 이 컴퓨터에서 받아써 자막(`.srt`)을 만듭니다. 파일을 밖으로 보내지 않습니다. 폴더를 통째로 줄 수도 있습니다 |
| `lnb text` | 자막을 30초마다 `[mm:ss]` 시각이 붙은 읽기 좋은 본문으로 바꿉니다. `--cues`는 자막 줄마다 정확한 시각 |
| `lnb frames` | 영상에서 판서·슬라이드 장면을 뽑습니다. 칠판을 지우기 직전처럼 화면이 크게 바뀌기 직전을 고릅니다 |
| `lnb pages` | 교재·강의록을 쪽 번호가 표시된 글로 만듭니다. 교재 인용 검사에 씁니다 |
| `lnb check` | 다 쓴 노트를 검사합니다. 인용이 자막·교재에 글자 그대로 있는지, 적은 시각·쪽이 맞는지, 계산이 맞는지 |
| `lnb setup` | 받아쓰기 준비. 음성인식 모델을 받고 원본과 같은지 확인합니다 |
| `lnb doctor` | 필요한 바깥 프로그램과 모델이 있는지 점검합니다 |

명령마다 자세한 옵션은 `lnb <명령> --help`. 설치하지 않고 저장소에서 `python3 tools/<파일>.py`로 불러도 같게 실행됩니다. 파일 이름: `fetch.py` · `transcribe.py` · `vtt_text.py`(`text`) · `frames.py` · `pages.py` · `check_note.py`(`check`). `setup`·`doctor`는 설치한 `lnb`로만 됩니다.

## 노트 쓰기

자세한 규칙은 [METHOD.md](METHOD.md). 사람이 써도 AI에게 맡겨도 규칙은 같습니다.

1. **읽기** — `lnb text` 본문으로 흐름을 잡고, 인용할 곳은 `lnb text --cues`로 정확한 시각을 찾습니다. 판서는 장면 사진으로, 교재는 md로 바꾼 본문으로 읽습니다
2. **옮기기** — 인용은 글자 그대로 옮기고, 바로 뒤에 출처를 답니다

   | 출처 | 적는 법 | 검사 |
   |---|---|---|
   | 영상 | `"…" [Vision 00 01:47]` — 그 말이 시작되는 시각 | 자막과 대조 |
   | 교재 | ``"…" `Strang ILA §3.2 p.24` `` — 원본 책의 절·쪽 | `lnb pages` 본문과 대조 |
   | 판서 | 장면 시각 `mm:ss` | 사람이 사진과 대조 |

   판서·교재의 수식은 LaTeX로 옮깁니다. 읽기 애매한 글자는 추측하지 말고 `[원문 미확인]`을 달고, 노트 끝 「판독 불확실 모음」 표에 모읍니다
3. **설명 붙이기** — 원문에 없는 내 설명에는 `[외부 추론]`, 근거를 못 찾은 곳에는 `[정보 없음]`
4. **계산 심기** — 계산한 곳마다 검산식을 주석으로 남깁니다. 예: `<!-- 검산: F(1,2) + F(1,3) == F(5,6) -->` (`F`는 분수, `M([[1,2],[3,4]])`은 행렬)
5. **검사** — `lnb check 노트.md`가 통과할 때까지 고칩니다
6. **사람·다른 모델이 볼 것** — 판서·수식 옮김, 판독 불확실 모음, 번역, 개념이 맞는지는 검사기가 못 봅니다. 노트를 쓴 모델이 아닌 다른 모델에게 검토를 맡기고, 지적은 원문으로 확인합니다

## 교재·슬라이드·강의록

노트는 영상만으로 쓰지 않습니다. 교재, 슬라이드, 강의록 PDF도 md(글)로 바꿔 함께 읽습니다. 변환은 공개 도구를 씁니다.

```bash
# PDF → md (수식은 LaTeX). -s/-e는 0부터 세는 PDF 쪽. 필요한 쪽만 바꾸세요
mineru -p 교재.pdf -o 강의자료/md -s 40 -e 52 -b pipeline
# 오피스 문서(pptx·docx·xlsx) → md. 수식은 깨집니다 (수식이 있으면 PDF로 바꿔 MinerU로)
markitdown 슬라이드.pptx -o 강의자료/md/슬라이드.md
```

- [MinerU](https://github.com/opendatalab/MinerU)는 `-b pipeline` 방식이 기본 방식보다 훨씬 빠릅니다. [MarkItDown](https://github.com/microsoft/markitdown). 설치는 각 저장소 안내를 따릅니다
- **변환 결과를 그대로 믿지 마세요.** 한글 깨짐, 표 무너짐, 빈 수식(`$$ $$`)이 없는지 열어 보고, 노트에 옮긴 수식은 원본 쪽 그림과 대조합니다
- 몇 쪽만 급하게 바꿀 때는 큰 AI 모델(Claude·GPT·Gemini)에게 쪽 그림을 주고 옮기게 해도 됩니다. 이렇게 지시하세요:
  - 한 글자도 고치지 말 것
  - 읽기 애매하면 `[?]`
  - 식 번호 `(7)`은 수식 밖에
  - 쪽마다 `<!-- p.N (PDF M) -->`
- 교재 변환본은 저작물입니다. git 밖 자료 폴더에 두고 공개 저장소에 넣지 마세요

**교재 인용 검사.** 변환기는 쪽 번호를 남기지 않습니다. 그래서 `lnb pages`가 쪽 표시를 붙인 본문을 만들고, `lnb check`는 노트의 교재 인용을 그 쪽에서 찾습니다.

```bash
# MinerU 결과에서 (폴더 이름은 방식마다 다릅니다: pipeline이면 auto)
lnb pages 강의자료/md/교재/auto/교재_content_list.json --pdf-start 41 --offset 10 -o 강의자료/strang-ila.md
# 글자를 복사할 수 있는 PDF라면 MinerU 없이 바로
lnb pages 강의록.pdf --first 1 --last 30 -o 강의자료/강의록.md
```

- `--pdf-start`: 변환한 첫 쪽이 PDF로 몇 쪽인지(1부터)
- `--offset`: PDF 쪽과 책 쪽의 차이. 책 24쪽이 PDF 34쪽이면 `--offset 10`
- 만든 파일을 `check_note.json`에 등록합니다: `"books": {"Strang ILA": "~/강의자료/strang-ila.md"}`
- 대조는 글자만 봅니다. 수식이 맞는지는 검산식으로 따로 확인합니다. 변환하지 않은 쪽, 번역한 문장, 너무 짧은 인용은 「교재 대조 불가」로 따로 세고 통과로 치지 않습니다

## 자료를 받을 때

`lnb fetch`는 영상 사이트(YouTube 등)에서 자막·영상·음성을 받습니다. **받을 권리가 있거나 허락된 자료에만** 쓰세요.

- 예: 이 저장소의 Strang 강의처럼 내려받기와 재사용을 허락한 강의(MIT OpenCourseWare, CC BY-NC-SA), 직접 만든 영상, 저작권자가 허락한 영상
- 사이트 이용약관과 각 영상의 라이선스를 지키는 것은 쓰는 사람의 책임입니다
- 받은 자막·영상·장면 사진은 개인 공부에만 쓰고 다시 배포하지 마세요
- `lnb fetch`는 일부러 천천히 받습니다. 강의 하나에 요청 한 번, 요청 사이 20–40초 대기, 사이트가 막으면 즉시 멈춥니다(종료 코드 2). 다시 실행하면 받지 못한 강의부터 이어받습니다. 사이트에 부담을 주지 않기 위한 것이니 우회하지 마세요
- 재생목록을 한꺼번에 받으려면 강좌 폴더에 `fetch.json`을 둡니다. 형식은 `lnb fetch --help`

`text`·`transcribe`·`frames`·`check`는 이미 가진 파일만 다룹니다.

## 가지고 있는 녹음·영상 받아쓰기

```bash
lnb transcribe ~/강의 -o ~/강의자막 -l ko
```

- `~/강의` 안의 음성·영상을 하위 폴더까지 찾아 받아쓰고, `~/강의자막` 아래에 같은 폴더 구조로 자막을 만듭니다. 원래 폴더는 건드리지 않습니다. `-o`를 빼면 강의 파일 바로 옆에 만듭니다
- 자막 이름에 모델 이름이 들어갑니다. 예: `1강 (whisper large-v3-turbo-q5_0 vad-silero-v6.2.0).srt`
- **VAD가 기본으로 켜집니다.** 말소리가 있는 구간만 받아써서, 조용한 구간에 whisper가 "아 아 아 …" 같은 말을 지어내거나 30초 분량을 한 덩어리로 뭉치는 일을 막습니다. 30분 강의로 비교했을 때 VAD를 끈 쪽에만 이런 구간이 두 곳 생겼고, VAD를 켠 쪽이 더 빨리 끝났습니다. 끄려면 `--no-vad`(자막 이름에서 `vad`가 빠집니다)
- 도중에 멈춰도 같은 명령을 다시 치면 끝난 것은 건너뛰고 이어서 합니다. 다른 모델로 다시 하면 새 자막이 따로 생기고 예전 자막은 남습니다
- 실패한 파일은 끝에 모아 보여 주고 `~/강의자막/failed.txt`에도 적습니다

## 알아 둘 점

- **받아쓰기는 틀립니다.** 특히 전문용어(예: "선형대수"를 "선형태수"로)와 숫자. 받아쓴 자막을 인용할 때는 판서·교재와 맞춰 보세요
- **판서 장면 기준은 강의마다 다릅니다.** 펜으로 천천히 쓰는 강의는 화면 변화가 작아 장면이 적게 잡힙니다. 그래서 변화가 없어도 30초마다 한 장씩 채웁니다. 처음 쓰는 강좌는 `lnb frames --scores`로 기준을 맞춰 보세요
- 다른 음성인식 모델을 쓰려면 `~/.cache/whisper.cpp/`에 두거나, `WHISPER_MODEL=<파일 경로>` 또는 `lnb transcribe -m <파일 경로>`

## Claude Code 스킬로 쓰기

`skills/lecture-note/`는 Claude Code가 위 도구를 순서대로 부르게 하는 스킬입니다. 「이 강의 노트 만들어 줘」처럼 말하면 받기 → 읽기 → 판서 장면 → 노트 → 검사로 진행하고, 사람이 확인할 곳(판서 옮김 등)은 따로 모아 보여 줍니다.

```bash
pipx install git+https://github.com/yamf97/lecture-note-bench    # 도구 (lnb)
git clone https://github.com/yamf97/lecture-note-bench.git           # 스킬 파일
ln -s "$PWD/lecture-note-bench/skills/lecture-note" ~/.claude/skills/lecture-note
```

링크 대신 폴더를 복사했다면, `SKILL.md` 안의 `T=` 줄을 저장소를 받은 경로의 `tools`로 바꾸세요(`lnb`를 설치하지 않았을 때 쓰는 경로입니다).

## 실험: 모델 다섯 개 비교

Gilbert Strang의 MIT OCW 강의 *A 2020 Vision of Linear Algebra* 00번 영상(4분)으로, 같은 지시서를 누구나 내려받아 쓸 수 있는 공개 모델 다섯 개에 보내고, 결과를 모델 이름을 가린 채 읽어 비교했습니다.

| 라벨 | 모델 | 읽어 본 평가 | 검사기가 찾은 문제 |
|---|---|---|---|
| E | qwen/qwen3.8-27b | 가장 나음 | 0 |
| A | qwen/qwen3.5-122b-a10b | 두 번째 | 3 |
| D | qwen/qwen3.6-35b-a3b | A와 비슷 | 3 |
| B | qwen/qwen3.8-flash | 수식이 제대로 표시되지 않음 | 2 |
| C | openai/gpt-oss-120b | 가장 부족 | 1 |

「검사기가 찾은 문제」는 `lnb check`가 원문·시각·계산과 맞지 않는다고 찾은 줄의 수입니다.

- 다섯 모델 모두 노트의 틀은 채웠습니다. 남은 흠은 뜻을 바꿔 옮긴 인용, 근거보다 먼저 나온 결론, 형식 위반처럼 **사람이 읽어야 잡히는 것**이었습니다
- 가장 작은 27B 모델이 가장 나았습니다. 모델 크기와 노트 품질이 비례하지 않았습니다
- 과제 하나, 모델마다 한 번씩 돌린 결과라 결론이 아니라 관찰입니다

| 위치 | 내용 |
|---|---|
| `experiments/2026-09-22_vision00_directive-prompt.md` | 모델에 보낸 지시서 |
| `experiments/results/A.md` ~ `E.md` | 다섯 모델이 쓴 노트. 어느 모델인지는 `labels.json` |
| `experiments/2026-09-23_blind-read.md` | 이름을 가리고 읽은 소감, 이름 공개, 원문과 대조한 문제점, 결론 |
| `lectures/Strang_2020_vision_LA/` | 검사에 쓰는 00번 영상 자막 |

같은 지시서를 다른 모델에 보내려면 `tools/run_gateway.py`를 씁니다(`lnb`에는 넣지 않은 실험용 도구, `OPENROUTER_API_KEY` 필요). API 키는 환경변수·설정 파일에서만 읽고 출력하지 않습니다.

```bash
python3 tools/run_gateway.py --base-url https://openrouter.ai/api/v1 \
  --model qwen/qwen3.8-27b --reasoning high --stream \
  --prompt experiments/2026-09-22_vision00_directive-prompt.md \
  --out experiments/results/new.md
```

## 출처와 라이선스

- 강의 자막과 슬라이드 내용: Gilbert Strang, *A 2020 Vision of Linear Algebra* (MIT OpenCourseWare RES.18-010, Spring 2020), [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). `lectures/`의 자막은 OCW 자막에서 문장 시작 시각을 살려 다시 만든 것입니다
- 지시서, 실험 기록, 모델이 쓴 노트(`experiments/`)도 강의 내용을 담고 있어 같은 CC BY-NC-SA 4.0으로 공개합니다
- 도구 코드(`src/lnb/`·`tools/`)와 스킬(`skills/`)은 MIT License입니다
- `lnb frames`의 장면 고르기는 [claude-video](https://github.com/bradautomates/claude-video)(Bradley Bonanno, MIT)의 방식(ffmpeg 장면 점수 + 썸네일 비교)을 참고해, 판서 강의에 맞게 「바뀌기 직전」 장면을 고르도록 바꿨습니다
- 교재(*Introduction to Linear Algebra*)는 절 제목만 참고했고 본문은 싣지 않았습니다
- 받아쓰기: [Whisper](https://github.com/openai/whisper)(OpenAI, MIT)와 [whisper.cpp](https://github.com/ggml-org/whisper.cpp)(ggml-org, MIT). lnb는 이 프로그램을 설치하지 않고 불러 쓰기만 하며, 모델 파일은 `lnb setup`이 Hugging Face의 `ggerganov/whisper.cpp`에서 받습니다
- 말소리 구간 찾기(VAD): [Silero VAD](https://github.com/snakers4/silero-vad)(MIT). whisper.cpp용 파일은 `lnb setup`이 Hugging Face의 `ggml-org/whisper-vad`에서 받습니다
- 함께 쓰는 도구의 라이선스: MarkItDown은 MIT입니다. MinerU는 버전마다 다릅니다(3.4.5는 「MinerU Open Source License」 — Apache 2.0에 상업 이용 조건 등이 더해짐). 설치한 버전의 LICENSE를 확인하세요. 모델 가중치에는 따로 조건이 붙을 수 있습니다

---

## English

> **Version 0.4.0 is out** (2026-11-19)
>
> What got better:
> - **0.4.0**: transcribe a whole folder of lectures. `lnb transcribe ~/lectures -o ~/captions` keeps the subfolder structure, and rerunning the same command resumes after an interruption.
> - 0.3.0: one command, `lnb setup`, prepares transcription (turning a recording into text). It downloads the speech-recognition model and checks that the file is intact and unaltered.
>
> Update with `pipx upgrade lecture-note-bench`. All changes by version: [CHANGELOG.md](CHANGELOG.md)

Tools for making study notes from lecture videos **so that everything quoted in a note can be checked against the lecture or textbook**. Each quote carries its video time or textbook page, and the tool checks that the quote matches the source word for word.

- **`lnb` command-line tool**: downloads captions and video, makes readable text and board frames, and checks finished notes against the sources. Works without any AI.
- **Claude Code skill** (`skills/lecture-note/`): has Claude Code run the tools in order to make a note.
- **Experiment**: five open models wrote a note from the same instructions, and the results were compared with the model names hidden.

Note-writing rules are in [METHOD.md](METHOD.md) (Korean). The code was written with Claude Code; I decided what to build, the verification rules, and the experiment design and judging. Changes are reviewed by a model from another company (Codex) and by automated tests before they go in. AI-written commits are marked `[AI:<model>]`.

### Install

```bash
pipx install git+https://github.com/yamf97/lecture-note-bench
lnb --help
lnb doctor   # checks for the external programs and prints install commands for missing ones
lnb setup    # only for transcription: downloads the speech model (about 574 MB) after asking, and verifies it
```

- Requires Python 3.9+. **Built and tested on macOS only.**
- External programs are installed separately. macOS: `brew install ffmpeg whisper-cpp poppler`
- To pin a version: `pipx install --force git+https://github.com/yamf97/lecture-note-bench@v0.4.0`
- **About Whisper (transcription):** Whisper is OpenAI's speech-recognition model, released with its code under MIT. lnb runs it through [whisper.cpp](https://github.com/ggml-org/whisper.cpp) (ggml-org, MIT), a C/C++ reimplementation installed with `brew install whisper-cpp` that needs no Python environment; `whisper-cli` is its command. It is used to make timestamped transcripts for recordings that have no captions, so quotes in a note can be checked. It runs on this computer only; nothing is uploaded. `lnb setup` downloads `ggml-large-v3-turbo-q5_0.bin` (about 574 MB), a size-reduced build of large-v3-turbo, and the Silero VAD model (about 0.9 MB). VAD is on by default: only speech is transcribed, which stops whisper from inventing text ("ah ah ah …") in quiet stretches. Turn it off with `--no-vad`.

### Quick start: one lecture

```bash
lnb fetch --url <video URL> -o material --video --transcribe-missing -l en   # captions and video
lnb text material/raw/<caption file>                                         # readable text with times
lnb frames material/video/<name>.mp4                                         # board and slide frames
# write the note (see below)
lnb check note.md                                                            # check quotes, times, math
```

`lnb check` needs a `check_note.json` in the note's repository that maps lecture names to caption folders. See `lnb check --help`; this repository's [check_note.json](check_note.json) is the smallest example.

### Commands

| Command | What it does |
|---|---|
| `lnb fetch` | Downloads captions, plus video or audio if needed. **Read "Downloading responsibly" first.** |
| `lnb transcribe` | Transcribes audio or video on this machine when a lecture has no captions. Nothing is uploaded. Accepts a whole folder: `lnb transcribe ~/lectures -o ~/captions` mirrors its subfolders, names each file after the model, and resumes where it stopped. |
| `lnb text` | Turns captions into readable text with a `[mm:ss]` time every 30 seconds; `--cues` gives exact times. |
| `lnb frames` | Picks board and slide frames just before each large change, such as a full board before erasing. |
| `lnb pages` | Turns a textbook or handout into text marked with page numbers, for quote checking. |
| `lnb check` | Checks a finished note: quotes match the captions or textbook word for word, times and pages are right, and calculations hold. |
| `lnb setup` | Prepares transcription: downloads the speech model and verifies it. |
| `lnb doctor` | Checks for the external programs and the model. |

Each command has `lnb <command> --help`. Without installing, run `python3 tools/<file>.py` from the repository: `fetch.py`, `transcribe.py`, `vtt_text.py` (`text`), `frames.py`, `pages.py`, `check_note.py` (`check`). `setup` and `doctor` need the installed `lnb`.

### Writing a note

1. **Read** the text from `lnb text`; find exact times with `--cues`.
2. **Quote** verbatim, followed by the source: video `"…" [Vision 00 01:47]`, textbook ``"…" `Strang ILA §3.2 p.24` ``, or board frame `mm:ss`. Mark unclear readings `[원문 미확인]` (unverified) instead of guessing.
3. **Explain**: tag your own explanations `[외부 추론]` (outside inference) and points with no source `[정보 없음]` (not in source).
4. **Embed checks** for calculations, such as `<!-- 검산: F(1,2) + F(1,3) == F(5,6) -->` (`F` is a fraction, `M(...)` a matrix).
5. **Check** with `lnb check note.md` until it passes.
6. **Review**: board math, translations and correctness are beyond the checker; have a different model review them and verify its points against the source.

**Textbooks and slides**: convert them to md with [MinerU](https://github.com/opendatalab/MinerU) (PDF; `-b pipeline` is much faster) or [MarkItDown](https://github.com/microsoft/markitdown) (Office files). Converters drop page numbers, so run `lnb pages` on MinerU's `*_content_list.json` or on a PDF with selectable text, and register the result under `books` in `check_note.json`. Do not trust conversions blindly, and keep converted textbooks out of public repositories.

### Downloading responsibly

Use `lnb fetch` only for material you have the right or permission to download, such as CC-licensed OCW lectures or your own videos. Follow each site's terms and each video's license, and do not redistribute what you download. `lnb fetch` is deliberately slow (one request per lecture, 20–40 s between requests, stops at once if blocked) to spare the site; do not work around it.

### Experiment

Five open models received the same instructions for a note on Gilbert Strang's *A 2020 Vision of Linear Algebra*, video 00 (MIT OCW), and I read the results with the model names hidden. The smallest, `qwen/qwen3.8-27b`, did best; size did not track quality. All five filled the structure, and the remaining flaws (paraphrased quotes, conclusions before evidence, format errors) were the kind a human reader has to catch. One task, one run per model: an observation, not a conclusion. Details are in `experiments/` (Korean).

### License

- Lecture content and `experiments/`: CC BY-NC-SA 4.0 (MIT OpenCourseWare RES.18-010).
- Tool code (`src/lnb/`, `tools/`) and skills (`skills/`): MIT. Frame selection in `lnb frames` was adapted from [claude-video](https://github.com/bradautomates/claude-video) (MIT).
- Transcription uses [Whisper](https://github.com/openai/whisper) (OpenAI, MIT) via [whisper.cpp](https://github.com/ggml-org/whisper.cpp) (ggml-org, MIT). lnb calls them but does not install them. Voice activity detection: [Silero VAD](https://github.com/snakers4/silero-vad) (MIT).

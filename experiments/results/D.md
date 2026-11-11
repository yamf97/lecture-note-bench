<!-- run_gateway.py
  model: qwen/qwen3.6-35b-a3b
  reasoning: high via reasoning_effort (stream)
  prompt: docs/experiments/2026-09-22_gpt-oss-120b_vision00_prompt2-directive.md
  elapsed_s: 119.0
  usage: {"prompt_tokens": 5069, "completion_tokens": 13869, "total_tokens": 18938, "cost": 0.00996175, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.00996175, "upstream_inference_prompt_cost": 0.00025345, "upstream_inference_completions_cost": 0.0097083}, "completion_tokens_details": {"reasoning_tokens": 8415, "image_tokens": 0, "audio_tokens": 0}}
  finish_reason: stop
  date: 2026-09-23 00:57
-->



```yaml
type: note
scope: "Vision 00 「Intro: A New Way to Start Linear Algebra」 (2020, 4분 09초) — 영상 전체"
layer: 지도 층 (예고편)
sources:
  - 자막 전문 (Vision 00)
  - 슬라이드 2/30 (영상 01:42)
  - Strang ILA 6판 목차 (§1.4, §2.3, §3.2, §4.4, §6.2, §6.3, §7.1)
```

# Vision 00 — 예고편: 선형대수를 새로 시작하는 법

> (번역) 이 영상은 스트랭 교수가 18.06 강의를 다시 찍어, 선형대수를 시작하는 방식을 완전히 바꾼 예고편입니다.
>
> > (원문) "And I'm here today to update them for several reasons." `[Vision 00 00:32]`
>
> > (번역) 줄 세운 행렬 C와 가로로 놓인 행렬 R을 곱해서 원래 행렬 A를 만드는 한 가지 방법으로, 행렬을 둘이나 셋의 조각으로 나눕니다.
>
> > (원문) "the first line... is a product of a C matrix, a column matrix, and a row matrix R." `[Vision 00 01:47]`
>
> > (번역) 슬라이드의 여섯 줄이 모두 같은 곱셈 꼴이라는 점만 먼저 보고, 나머지 다섯 줄은 각 장의 이름을 기억해 두면 됩니다.
>
> > (원문) "the slides tell you the whole course." `[Vision 00 01:10]`

**지금 할 수 있어야 하는 것**: ① 이 영상 묶음이 무엇인지 한두 문장으로 말한다 ② "행렬을 조각의 곱으로 쓴다"가 무슨 뜻인지 작은 행렬 하나로 보여 준다 (→ 3절) ③ 슬라이드 여섯 줄이 첫 줄 / 앞 절반 / 뒤 절반으로 어떻게 나뉘는지 말한다 (→ 2절)

**나중에 돌아올 것**: LU · QR · $Q\Lambda Q^{\mathrm T}$ · $X\Lambda X^{-1}$ · $U\Sigma V^{\mathrm T}$가 각각 무엇인지 — 하나하나가 책의 한 장. 지금 몰라도 된다.

## 「읽는 법」

| 표기 | 뜻 |
|---|---|
| `[Vision 00 mm:ss]` | 스트랭 교수가 자막에서 그 말을 시작한 시각 |
| `슬라이드 2/30` | 영상 01:42에 띄운 전체 강의 요약 슬라이드의 2페이지 |
| `Strang ILA §3.2` | 스트랭 저 서적 《Introduction to Linear Algebra》 6판, 3장 2절 |
| `[외부 추론]` | 출처를 가르는 표시일 뿐, 맞다는 보증은 아니다 |

**인용 형식**: 스트랭 인용은 **번역 먼저, 원문 아래**. 원문은 자막에서 글자 그대로. 원문 바로 뒤 같은 줄에 좌표 `[Vision 00 mm:ss]` — 그 말이 시작되는 큐의 시각. 한 문장이 여러 큐에 걸치면 이어 붙이고 첫 큐 시각을 쓴다.

### 1. 이 영상은 무엇인가

스트랭 교수는 기존 18.06 강의를 다시 찍어왔는데, 고치는 이유는 두 가지입니다. 먼저 "행렬이 점점 더 중요해졌다"며 강조합니다:
> (번역) 다행히 이 전체 주제는 점점 더 필수적이고, 중요하며, 아름답게 되었습니다.
>
> > (원문) "Fortunately, the whole subject has just become more and more essential, more and more important, more and beautiful." `[Vision 00 00:45]`

둘째, "지금 교습할 때 새로운 출발점이 생겼다"고 합니다:
> (번역) 그리고 저는 이제 그것을 가르칠 때 새로운 출발점을 가지고 있습니다.
>
> > (원문) "And also, when I teach it now, I have a new starting point." `[Vision 00 00:59]`

스트랭은 "슬라이드가 강좌 전체를 말해 준다"고 단언하며 두 큐를 이어갑니다:
> (번역) 슬라이드가 여러분에게 전체 강좌를 알려 줍니다.
>
> > (원문) "The slides tell you the whole course. And that's crazy to have a full course within a short video." `[Vision 00 01:10]`

영상의 끝에서 그는 "실제 18.06 영상으로 가라"고 당부합니다:
> (번역) 디테일은 실제 18.06 영상으로 가시길 부탁드립니다.
>
> > (원문) "And please go to the real 18.06 videos for the details." `[Vision 00 04:00]`

이 말은 "영상 단계 = 지도 그리기"의 근거입니다.

### 2. 슬라이드 한 장 — 여섯 줄

스트랭은 영상 01:42에 슬라이드를 띄우며 "이것은 전체 영상의 개요"라고 말합니다. 슬라이드의 여섯 줄이 모두 같은 꼴임(왼쪽 행렬 하나 = 오른쪽 둘 또는 셋의 곱)임을 알 수 있습니다.

| 줄 번호 | 식 | 슬라이드에 적힌 설명 (원문) | 쉬운 말 `[외부 추론]` | 어느 영상 · 책 어디 |
|---|---|---|---|---|
| 1 | $A = CR$ | Independent columns in $C$ | $C$는 서로 독립인 열을 모아 만든 행렬 | 01 열공간 · §3.2 |
| 2 | $A = LU$ | Triangular matrices $L$ and $U$ | $L$과 $U$는 삼각형 모양을 띤 행렬 | 02 큰 그림 · §2.3 |
| 3 | $A = QR$ | Orthogonal columns in $Q$ | $Q$의 열들은 직교(수직) 관계 | 03 직교벡터 · §4.4 |
| 4 | $S = Q\Lambda Q^{\mathrm T}$, $Q^{\mathrm T} = Q^{-1}$ | Orthogonal eigenvectors $Sq = \lambda q$ | 대칭행렬 $S$는 직교 고유벡터로 쪼개짐 | 04 고유값 · §6.3 |
| 5 | $A = X\Lambda X^{-1}$ | Eigenvalues in $\Lambda$ · Eigenvectors in $X$ · $Ax = \lambda x$ | 정사각행렬 $A$는 고유값·고유벡터로 쪼개짐 | 04 고유값 · §6.2 |
| 6 | $A = U\Sigma V^{\mathrm T}$ | Diagonal $\Sigma$ = Singular values $\sigma$ · Orthogonal vectors in $U$... | 어떤 모양의 행렬 $A$도 특이값으로 쪼개짐 | 05 특이값 · §7.1 |

[원문 미확인]

> (번역) 이 표에서 지금 가져갈 것은 하나다 — 여섯 줄이 모두 같은 꼴이라는 것. 1줄은 3절에서 직접 해 본다. 나머지 다섯 줄은 **읽고 지나가면 된다**.

| 줄 번호 | 조건 표 `[외부 추론]` | 설명 |
|---|---|---|
| 1, 6 | $CR$, $U\Sigma V^{\mathrm T}$ | 모든 모양의 행렬에 적용 가능 |
| 3 | $QR$ | 직사각 행렬에도 적용 가능 |
| 2 | $LU$ | 행 이동이 필요한 행렬이 있을 때 필요. 예: $\begin{bmatrix}0&1\\1&0\end{bmatrix}$은 그대로는 LU 분해가 안 됨. 아래에 0이 오면 계산이 멈추거나 분수만 등장해 실용성이 떨어지므로, 위·아래를 바꿔주는 행 이동을 먼저 해야 함. |
| 4 | $Q\Lambda Q^{\mathrm T}$ | 대칭행렬만 적용 가능 |
| 5 | $X\Lambda X^{-1}$ | 정사각행렬 + 독립인 고유벡터가 열 수만큼 있을 때만 적용 가능. 반례: 90° 회전 $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$은 실수 고유벡터가 없다. |

**소절 「첫 줄 / 앞 절반 / 뒤 절반」**
스트랭은 첫 줄이 $C$(열)와 $R$(행)의 곱이라고 말합니다:
> (번역) 그리고 첫 번째 줄... C 행렬, 열 행렬, 그리고 R 행렬, 행 행렬의 곱입니다.
>
> > (원문) "And the first line, which I think about in my mind as matrix A, is a product of a C matrix, a column matrix, and a row matrix R." `[Vision 00 01:47]`

나머지 다섯 줄은 핵심 장들의 이름표라고 합니다:
> (번역) 그런 다음 이들은 다섯 가지 유명한 필수 약자입니다. 선형대수의 핵심 장들의 간결한 설명입니다.
>
> > (원문) "Then these are five famous essential shorthand descriptions of the key chapters of linear algebra, the key chapters." `[Vision 00 02:08]`

$LU$는 소거, 첫 번째 일이라고 합니다:
> (번역) 컴퓨터 명령어는 정확히 연립방정식을 푸는 소거 과정인 LU라고 할 것입니다. 그것은 선형대수의 첫 번째 작업입니다.
>
> > (원문) "And computer commands would be exactly those letters LU for elimination for solving equations, the first job of linear algebra." `[Vision 00 02:25]`

앞 절반과 뒤 절반의 구분은 자막에서 이렇게 나옵니다:
> (번역) 음, 일단 저는 이 첫 번째 절반... QR까지의 구간이 방정식을 푸는 것에 관한 것이라고 해야겠습니다. 두 번째 절반, 이 세 가지...
> (번역) ...고유값과 고유벡터 그리고 특이값에 관한 것입니다. 전체 주제에 접근하는 또 다른 방법입니다.
>
> > (원문) "the first half, ending with there, with QR, is about solving equations. The second half, these three are about eigenvalues and eigenvectors and singular values, a different way to approach the whole subject and a very, very important way." `[Vision 00 03:02]`

특이값이 이론의 꼭대기, 모두 "두세 조각으로 쪼개기"라고 합니다:
> (번역) 제가 원하는 목표 중 하나는... 특이값을 포함시키는 것입니다. 여러분 정말 놓치고 싶지 않으니깐요. 그것이 이론의 최고점입니다. 그리고 그것은 다른 모두처럼 행렬을 두세 조각으로 나누는 방식으로 표현됩니다.
>
> > (원문) "Among my goals is to help courses around the world get singular values included because you really don't want to miss them. That's the high point of the theory. And it's expressed like all the others as breaking a matrix into two or three pieces, two or three parts." `[Vision 00 03:36]`

| 구분 | 무슨 이야기 | 우리의 층 |
|---|---|---|
| 앞 절반(1·2·3줄) | 행렬을 나누어 연립방정식을 푸는 방법 | 1줄만 익히는 층 |
| 뒤 절반(4·5·6줄) | 고유값·고유벡터·특이값으로 나누는 방법 | 나머지 지도 층 |

선형대수의 핵심 장 하나하나가 행렬을 몇 조각의 곱으로 쪼개는 한 가지 방법이고, 조각마다 성질이 다르다. 이것이 이 4분 영상의 핵심이다.

### 3. "행렬을 조각의 곱으로 쓴다"는 게 무슨 말인가 `[외부 추론]`

스트랭은 이 영상에서 숫자 예를 들지 않습니다(01에서 든다). 기준 행렬 $A_2$로 맛만 봅니다.

#### 3.1 열을 하나씩 잘라서 본다.
$$A_2 = \begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}$$
열 1, 열 2, 열 3을 세로 벡터로 나눕니다.

| 열 1 | = | (1, 2) | = | 1 × (1, 2) | 1배 |
|---|---|---|---|---|---|
| 열 2 | = | (2, 4) | = | 2 × (1, 2) | 2배 |
| 열 3 | = | (3, 6) | = | 3 × (1, 2) | 3배 |

세 열이 모두 **같은 재료 $(1,2)$의 몇 배**다.

#### 3.2 재료와 만드는 법.
재료 열 $(1,2)$가 $C$, "1배·2배·3배"를 가로로 적은 $[1\ 2\ 3]$이 $R$.
$$A_2 = C\,R = \underbrace{\begin{bmatrix}1\\2\end{bmatrix}}_{C} \underbrace{\begin{bmatrix}1&2&3\end{bmatrix}}_{R}$$
<!-- 검산: M([[1],[2]]) * M([[1,2,3]]) == M([[1,2,3],[2,4,6]]) -->
"$C\times R$은 '재료를 1배, 2배, 3배 해서 왼쪽부터 나란히 세워라'로 읽는다". **스스로 확인하는 법**: $C\times R$을 직접 계산해 원래 행렬이 나오는지 보면 된다.

#### 3.3 "한 방향"이라는 말.
$(1,2)$를 원점에서의 화살표로 그립니다. $(2,4)$와 $(3,6)$은 같은 화살표를 길게 늘린 것일 뿐입니다. 세 화살표가 같은 직선 위에 있으므로 "열이 한 방향뿐"이라고 합니다. 반면 $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$의 두 열은 서로 다른 직선 위에 있으므로, 재료 열 하나로는 $A_4$를 만들 수 없습니다(3절 끝 (다)에서 확인).

#### 3.4 빠지기 쉬운 곳.
$R$을 찾을 때는 **열 전체**를 재료 열 전체와 비교해야 합니다. 열 하나 **안에서** 위·아래를 비교하면(아래가 위 행렬의 2배) 다른 숫자(2)가 나오는데, 그것은 틀린 관찰이 아닙니다. 다만 그것은 다른 질문(3.5)의 답일 뿐입니다.

#### 3.5 같은 식을 행으로 읽으면.
$A_2$를 행으로 잘라서 보면:

| 행 1 | = | (1, 2, 3) | = | 1 × (1, 2, 3) | $R$의 1배 |
|---|---|---|---|---|---|
| 행 2 | = | (2, 4, 6) | = | 2 × (1, 2, 3) | $R$의 2배 |

이 배수 1, 2를 세로로 적으면 $C$가 다시 나옵니다.

| 읽는 방향 | 뜻 | 몇 배인지는 누가 알려 주나 |
|---|---|---|
| 열로 읽기 | 세로 벡터가 가로 벡터의 몇 배인지 | $R$이 알려 줌 |
| 행으로 읽기 | 가로 벡터가 세로 벡터의 몇 배인지 | $C$가 알려 줌 |

#### 3.6 같은 것은 개수다.
열은 셋이지만 재료 열은 하나, 행은 둘이지만 재료 행은 하나, 개수가 똑같이 1입니다. **"$C$와 $R$이 같다는 말이 아니다"** — 같은 것은 재료의 개수입니다. 이 개수의 이름이 **rank**(여기서 처음 이름을 준다). $A_2$의 rank는 1, $A_4$의 rank는 2입니다.

> (번역) 여기까지 확인된 것과 아닌 것: 열 하나×행 하나 꼴에서는 식의 형태에서 바로 rank 1임을 알 수 있습니다. 재료가 둘이나 셋일 때도 열의 수 = 행의 수인가는 아직 안 보입니다(01·06·09에서 확인 예정). 그리고 위 계산은 예시일 뿐, "모든 행렬이 CR로 쪼개진다"의 증명이 아닙니다.

<details><summary>곁가지 — 지금은 건너뛰어도 된다</summary>
재료 열이 $r$개면 $C$는 열 $r$개, $R$은 행 $r$개입니다. 숫자 개수가 6에서 5로 줄었지만 "정보 5개"는 아닙니다. 앞 조각에 2배를 해도 뒤 조각에 반비례하면 같은 행렬이 만들어지기 때문입니다.
</details>

**「가리고 해 보기」**: (가) 빈칸 계산 — $\begin{bmatrix}1\\3\end{bmatrix}\begin{bmatrix}2&4\end{bmatrix}=?$ 계산 **전에** "둘째 열은 첫째 열의 몇 배일까"를 예측하게 한다. (나) 거꾸로 — $\begin{bmatrix}2&6\\1&3\end{bmatrix}$을 열 하나×행 하나로 만든다. (다) 반례 — $A_4$도 열 하나×행 하나로 되나?

<details><summary>맞춰 보기 (먼저 해 본 뒤에 연다)</summary>
(가) $\begin{bmatrix}2&4\end{bmatrix}$. 둘째 열은 첫째 열의 2배입니다.
<!-- 검산: M([[1],[3]]) * M([[2,4]]) == M([[2,4],[6,12]]) -->
(나) $\begin{bmatrix}1\\1/2\end{bmatrix}\begin{bmatrix}2&6\end{bmatrix}$도 됩니다.
<!-- 검산: M([[1],[0.5]]) * M([[2,6]]) == M([[2,6],[1,3]]) -->
(나)의 답에는 "답이 하나가 아닙니다($\begin{bmatrix}1\\1/2\end{bmatrix}\begin{bmatrix}2&6\end{bmatrix}$도 됨) — 다만 $CR$의 $C$는 원래 행렬의 열에서 고른 것이어야 하므로 그쪽은 $CR$은 아닙니다."를 넣습니다.
(다) $A_4$는 열 하나×행 하나로 되지 않습니다. 두 열이 서로 다른 방향을 가리키므로 rank가 2이기 때문입니다.
</details>

### 4. 시각별 흐름

| 시각 구간 | 내용 |
|---|---|
| 00:13–00:32 | 인사 및 기존 영상(OCS/YT) 언급 |
| 00:32–01:05 | 개정 동기(중요도 상승, 새로운 출발점) |
| 01:05–01:31 | 슬라이드로 전체 강좌 요약, 새 교재 소개 |
| 01:31–02:08 | 첫 줄($CR$)과 나머지 다섯 줄(LU~SVD) 소개 |
| 02:08–03:02 | 앞 절반(LU, QR): 방정식 풀기 및 소거 |
| 03:02–03:54 | 뒤 절반(QΛQ^T, XΛX^{-1}, SVD): 고유값/특이값, 이론의 꼭대기 |
| 03:54–04:08 | 감사 및 실제 18.06 영상 권고 |

여기서 쓰고 있다고 한 책은 6판이 아니라 *Linear Algebra for Everyone* `[01:23]`.

### 5. 말과 기호

| 영어 | 우리말 | 이 영상에서의 자리 |
|---|---|---|
| column | 열 | 슬라이드 1줄 $C$의 구성 요소 |
| row | 행 | 슬라이드 1줄 $R$의 구성 요소 |
| independent columns | 독립인 열 | 슬라이드 1줄 설명 |
| elimination | 소거 | 02:28, LU의 핵심 |
| triangular matrix | 삼각행렬 | 슬라이드 2줄 $L, U$ |
| orthogonal/perpendicular | 직교/수직 | 02:46, QR과 $Q\Lambda Q^T$의 핵심 |
| symmetric matrix | 대칭행렬 | 슬라이드 4줄 $S$ |
| eigenvalue/eigenvector | 고유값/고유벡터 | 슬라이드 4, 5줄 |
| singular value | 특이값 | 슬라이드 6줄 $\Sigma$ |
| factorization | 분해 | 이 영상에서는 이 낱말을 안 쓰고 "breaking a matrix into two or three pieces"라고 한다 |

### 6. 어디에 쓰이나 — 짧게 `[외부 추론]`

**어디에**: 숫자 자료를 표로 적으면 행렬이 됩니다. 행은 사람이나 가구, 열은 변수가 됩니다. 각 데이터가 한 행렬의 하나의 숫자가 되어 정리됩니다.

**방금 본 수학이 설명하는 것**: $A_2$에서 둘째 행이 첫째 행의 2배인 것은, 새로운 방향을 하나도 추가하지 않았음을 수학적으로 보여줍니다. 즉, 자료에서 겉으로 보기에는 숫자가 많아 보이지만, 실제 정보의 방향은 하나뿐이라는 뜻입니다.

**여기까지는 말해 주지 않는다**: 독립인 방향의 수가 현실의 원인 수와 같지 않을 수 있습니다. 또한 몇 배인지 행렬에서는 알 수 있어도 실제 관측 데이터에는 노이즈가 섞여 "정확히 몇 배"인 경우가 거의 없습니다. 그래서 나중에 특이값(SVD)이 필요해집니다.

**"수학적 의미를 가지고 현실에 정답처럼 적용하면 안 된다."**

### 7. 본 뒤에 — 말로 설명해 보기

① 스트랭이 영상을 새로 고쳐 말하는 이유 둘: 선형대수가 더 중요해졌기 때문, 새로운 출발점(행렬을 조각 곱으로 시작)을 제시하기 때문.
② 여섯 줄에 공통된 꼴과 조각들이 다른 점: 모두 왼쪽 행렬 하나를 오른쪽 둘 이상의 곱으로 나눈다는 공통 형태를 띠지만, $C, R, L, U, Q, \Lambda, X, U, \Sigma, V$가 각각 지닌 성질(열 독립, 삼각, 직교, 대칭, 정사각, 특이값 등)이 다릅니다.
③ 앞 절반·뒤 절반은 무엇에 관한 이야기이고 $CR$은 어디 속하며 왜 따로 강조되나: 앞 절반(LU, QR)은 연립방정식을 푸는 계산 과정, 뒤 절반(QΛQ^T, XΛX^{-1}, SVD)은 고유값과 특이값을 다루는 이론입니다. $CR$은 방정식 풀기의 가장 기초가 되는 첫 번째 예이므로 새로운 출발점으로特地 강조됩니다.
④ $\begin{bmatrix}1\\2\end{bmatrix}\begin{bmatrix}1&2&3\end{bmatrix}$을 계산하지 않고도 결과의 행들이 어떤 관계일지 말할 수 있나: 결과 행렬의 모든 행은 가로 벡터 $[1, 2, 3]$의 1배와 2배가 될 것이므로, 둘째 행은 첫째 행의 정확히 2배가 됩니다.

**이해 단계 적어 두기** — 설명을 따라갈 수 있다 / 빈 종이에 다시 쓸 수 있다 / 처음 보는 짧은 문제에 쓸 수 있다
**남은 질문**: (여기에 적는다)
```
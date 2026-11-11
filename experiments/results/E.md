<!-- run_gateway.py
  model: qwen/qwen3.8-27b
  reasoning: high via reasoning_effort (stream)
  prompt: docs/experiments/2026-09-22_gpt-oss-120b_vision00_prompt2-directive.md
  elapsed_s: 242.2
  usage: {"prompt_tokens": 5069, "completion_tokens": 14416, "total_tokens": 19485, "cost": 0.0365469, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.0365469, "upstream_inference_prompt_cost": 0.0005069, "upstream_inference_completions_cost": 0.03604}, "completion_tokens_details": {"reasoning_tokens": 7940, "image_tokens": 0, "audio_tokens": 0}}
  finish_reason: stop
  date: 2026-09-23 00:59
-->



---
type: note
scope: "Vision 00 「Intro: A New Way to Start Linear Algebra」 (2020, 4분 09초) — 영상 전체"
layer: 지도 층 (예고편)
sources:
  - 자막 전문 (OpenCourseWare Vision 00, 2020)
  - 슬라이드 2/30 (영상 01:42에 띄움)
  - Strang, *Introduction to Linear Algebra* 6판 (2023) 목차
---

# Vision 00 — 예고편: 선형대수를 새로 시작하는 법

> **지금 할 수 있어야 하는 것**
>
> 1. 이 영상 묶음이 무엇인지 한두 문장으로 말한다.
> 2. "행렬을 조각의 곱으로 쓴다"가 무슨 뜻인지 작은 행렬 하나로 보여 준다 (→ 3절).
> 3. 슬라이드 여섯 줄이 첫 줄 / 앞 절반 / 뒤 절반으로 어떻게 나뉘는지 말한다 (→ 2절).

> **나중에 돌아올 것**
>
> $LU$ · $QR$ · $Q\Lambda Q^{\mathrm T}$ · $X\Lambda X^{-1}$ · $U\Sigma V^{\mathrm T}$ 가 각각 무엇인지 — 하나하나가 책의 한 장. 지금 몰라도 된다.

---

## 읽는 법

| 표기 | 뜻 |
|---|---|
| `[Vision 00 01:47]` | 이 영상의 자막에서 1분 47초 큐에서 시작하는 말을 가리킨다. |
| `슬라이드 2/30` | 영상에 띄어 준 슬라이드 30장 중 2장 (영상 01:42). |
| `Strang ILA §3.2` | Strang, *Introduction to Linear Algebra* 6판의 3장 2절. |
| `[외부 추론]` | 스트랭이 말하지 않은, 제가 덧붙인 설명. 출처를 가르는 표시일 뿐, 맞다는 보증은 아니다. |

인용 형식: 번역 먼저, 그 아래 원문. 원문 바로 뒤에 좌표.

---

## 1. 이 영상은 무엇인가

스트랭은 MIT 18.06 선형대수 강의 영상을 몇 년 만에 새로 고쳐 말하러 온 것이다. 고치는 이유는 자막에서 직접 두 가지를 든다.

첫째, 그 사이 선형대수가 더 중요해졌다:

> (번역) 다행히 이 분야 전체가 점점 더 필수적이고, 점점 더 중요하고, 점점 더 아름답게 되었습니다.
>
> (원문) "Fortunately, the whole subject has just become more and more essential, more and more important, more and more beautiful." `[Vision 00 00:45]`

둘째, 이제 새로 시작하는 지점이 생겼다:

> (번역) 그리고 지금 가르칠 때는 새로운 출발점이 있습니다.
>
> (원문) "And also, when I teach it now, I have a new starting point." `[Vision 00 00:59]`

그리고 슬라이드 한 장이 강좌 전체를 압축한다고 말한다:

> (번역) 슬라이드가 강좌 전체를 말해 줍니다. 짧은 영상에 강좌 전체가 들어 있다는 건 좀 미친 일이에요.
>
> (원문) "The slides tell you the whole course. And that's crazy to have a full course within a short video." `[Vision 00 01:10]`

영상 마지막에 이렇게 당부를 한다:

> (번역) 자세한 내용은 진짜 18.06 영상으로 가 주세요.
>
> (원문) "And please go to the real 18.06 videos for the details." `[Vision 00 04:00]`

이 한마디가 "이 4분 영상 단계 = 지도 그리기(예고편)"라는 위치의 근거다. `[외부 추론]`

---

## 2. 슬라이드 한 장 — 여섯 줄

스트랭이 `[01:42]`에 슬라이드를 띄우며 "전체 영상의 개요(outline)"라고 소개한다.

> (번역) 이건 전체 영상의 개요입니다.
>
> (원문) "So this is an outline of the whole video." `[Vision 00 01:42]`

**여섯 줄이 모두 같은 꼴이다:** 왼쪽에 행렬 하나, 오른쪽에 행렬 둘 또는 셋을 곱한 것. 즉 "하나의 행렬 = 여러 조각의 곱"이라는 같은 문법으로 여섯 가지를 적어 놓은 것이다. `[외부 추론]`

| 줄 | 식 | 슬라이드에 적힌 설명 (원문) | 쉬운 말 `[외부 추론]` | 어느 영상 · 책 어디 |
|---|---|---|---|---|
| 1 | $A = CR$ | Independent columns in $C$ | $C$의 열은 서로 독립인 재료 열이다 | 영상 01 Column Space, 09 Elimination and $A=CR$ · §3.2 Computing the Nullspace by Elimination: $A = CR$ |
| 2 | $A = LU$ | Triangular matrices $L$ and $U$ | $L$과 $U$는 각각 아래·위 삼각행렬이다 (소거로 나뉨) | 영상 02 Big Picture · §2.3 Matrix Computations and $A = LU$ |
| 3 | $A = QR$ | Orthogonal columns in $Q$ | $Q$의 열은 서로 수직(직교)이다 | 영상 03 Orthogonal Vectors · §4.4 Orthonormal Bases and Gram-Schmidt |
| 4 | $S = Q\Lambda Q^{\mathrm T}$, $Q^{\mathrm T} = Q^{-1}$ | Orthogonal eigenvectors $Sq = \lambda q$ | 대칭행렬 $S$는 수직인 고유벡터로 회전 없이 쪼개진다 | 영상 04 Eigenvalues · §6.2 Diagonalizing a Matrix, §6.3 Symmetric Positive Definite Matrices |
| 5 | $A = X\Lambda X^{-1}$ | Eigenvalues in $\Lambda$ · Eigenvectors in $X$ · $Ax = \lambda x$ | 정사각행렬을 고유값·고유벡터로 분해 (대칭만은 아님) | 영상 04 Eigenvalues · §6.2 Diagonalizing a Matrix |
| 6 | $A = U\Sigma V^{\mathrm T}$ | Diagonal $\Sigma$ = Singular values $\sigma = \sqrt{\lambda(A^{\mathrm T}A)}$ · Orthogonal vectors in $U^{\mathrm T}U = V^{\mathrm T}V = I$ · $Av = \sigma u$ | 어떤 모양(직사각 포함)이든 열·행 벡터가 수직인 세 조각으로 쪼갬 | 영상 05 Singular Values · §7.1 Singular Values and Singular Vectors |

`[원문 미확인]` — 위 책 절 제목은 목차에서 가져온 것이므로, 절 본문 내용이 표의 "쉬운 말" 열과 정확히 일치하는지는 확인하지 않았다.

> **이 표에서 지금 가져갈 것은 하나다 — 여섯 줄이 모두 같은 꼴이라는 것. 1줄은 3절에서 직접 해 본다. 나머지 다섯 줄은 *읽고 지나가면 된다*.**

### 조건 표 `[외부 추론]`

| 분해 | 어느 행렬에 되나 | 비고 |
|---|---|---|
| $A = CR$ | **모든 모양** (직사각 포함) | $C$는 원래 열에서 고른 것 |
| $A = U\Sigma V^{\mathrm T}$ | **모든 모양** (직사각 포함) | 6줄 중 가장 범위가 넓음 |
| $A = QR$ | 직사각도 됨 (단, 열이 독립이어야 완전 $QR$) | |
| $A = LU$ | 행 바꿈이 필요한 행렬이 있음 | 예: $\begin{bmatrix}0&1\\1&0\end{bmatrix}$의 (1,1) 성분이 0 → 피벗이 없어서 소거를 시작할 수 없다. 1행·2행을 바꿔야 하므로 $PA=LU$ ($P$는 행 바꿈 행렬) |
| $S = Q\Lambda Q^{\mathrm T}$ | **대칭행렬만** ($S = S^{\mathrm T}$) | |
| $A = X\Lambda X^{-1}$ | 정사각 + 독립인 실수 고유벡터가 열 수만큼 | 반례: 90° 회전 $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$의 특성방정식 $\lambda^2+1=0$ → 실수 고유값이 없으므로 실수 고유벡터가 없다 |

### 첫 줄 / 앞 절반 / 뒤 절반

자막에서 각 구분을 인용한다.

**첫 줄이 $C$(열)와 $R$(행)의 곱:**

> (번역) 첫 줄, 제 머릿속에서는 행렬 $A$라고 생각하는 것이, $C$ 행렬 — 열 행렬 — 과 $R$ 행렬 — 행 행렬 — 의 곱입니다.
>
> (원문) "And the first line, which I think about in my mind as matrix A, is a product of a C matrix, a column matrix, and a row matrix R." `[Vision 00 01:47]`

**나머지 다섯 줄이 핵심 장들의 이름표:**

> (번역) 그리고 이건 다섯 가지 유명한, 꼭 필요한 약어적 설명인데, 선형대수의 핵심 장, 핵심 장에 대한 겁니다.
>
> (원문) "Then these are five famous essential shorthand descriptions of the key chapters of linear algebra, the key chapters." `[Vision 00 02:08]`

**$LU$ = 소거, 첫 번째 일:**

> (번역) 컴퓨터 명령어는 정확히 그 글자 $LU$인데, 방정식을 푸는 소거법, 선형대수의 첫 번째 일입니다.
>
> (원문) "And computer commands would be exactly those letters LU for elimination for solving equations, the first job of linear algebra." `[Vision 00 02:25]`

**앞 절반은 방정식 풀기, 뒤 절반은 고유값·고유벡터·특이값:**

> (번역) 아, 그래야죠. 앞 절반, $QR$까지 여기에서 끝나는 게 방정식 푸는 겁니다.
>
> (원문) "oh, well, I should say, the first half, ending with there, with QR, is about solving equations." `[Vision 00 03:02]`

> (번역) 뒤 절반, 이 셋은 고유값과 고유벡터, 그리고 특이값에 관한 거예요.
>
> (원문) "The second half, these three are about eigenvalues and eigenvectors and singular values," `[Vision 00 03:11]`

**특이값이 이론의 꼭대기, 모두 "두세 조각으로 쪼개기":**

> (번역) 그게 이론의 꼭대기입니다.
>
> (원문) "That's the high point of the theory." `[Vision 00 03:36]`

> (번역) 그리고 이건 다른 모든 것과 똑같이, 행렬을 두 조각 또는 세 조각, 두 부분 또는 세 부분으로 쪼갬으로 표현됩니다.
>
> (원문) "And it's expressed like all the others as breaking a matrix into two or three pieces, two or three parts." `[Vision 00 03:39]`

| 구분 | 줄 | 무슨 이야기 | 우리의 층 |
|---|---|---|---|
| 앞 절반 | 1·2·3 줄 ($CR$, $LU$, $QR$) | 방정식 $Ax=b$ 푸는 일 | 1줄($CR$)만 지금 익히는 층; 2·3줄은 지도 층 |
| 뒤 절반 | 4·5·6 줄 ($Q\Lambda Q^T$, $X\Lambda X^{-1}$, $U\Sigma V^T$) | 고유값·고유벡터·특이값 — "다른 접근법" | 지도 층 (읽고 지나감) |

**선형대수의 핵심 장 하나하나는 행렬을 몇 조각의 곱으로 쪼개는 한 가지 방법이고, 조각마다 성질이 다르다.** 이 4분의 핵심 문장이다. `[외부 추론]`

---

## 3. "행렬을 조각의 곱으로 쓴다"는 게 무슨 말인가 `[외부 추론]`

스트랭은 이 영상에서 숫자 예를 들지 않는다 (01에서 든다). 기준 행렬 $A_2$로 맛만 본다.

### 3.1 열을 하나씩 잘라서 본다

$$A_2 = \begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}$$

열을 세로로 하나씩 끊으면:

$$\text{열}_1 = \begin{bmatrix}1\\2\end{bmatrix},\qquad \text{열}_2 = \begin{bmatrix}2\\4\end{bmatrix},\qquad \text{열}_3 = \begin{bmatrix}3\\6\end{bmatrix}$$

| 열 | = 재료 × 배수 | 관계 |
|---|---|---|
| 열$_1$ = $(1,\,2)$ | $= 1 \times (1,\,2)$ | 1배 |
| 열$_2$ = $(2,\,4)$ | $= 2 \times (1,\,2)$ | 2배 |
| 열$_3$ = $(3,\,6)$ | $= 3 \times (1,\,2)$ | 3배 |

**결론: 세 열이 모두 같은 재료 $(1,2)$의 몇 배다.**

### 3.2 재료와 만드는 법

- **재료 열** $C = \begin{bmatrix}1\\2\end{bmatrix}$
- **만드는 법(배수를 가로로 적은 것)** $R = \begin{bmatrix}1&2&3\end{bmatrix}$

$$\underbrace{\begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}}_{A_2} \;=\; \underbrace{\begin{bmatrix}1\\2\end{bmatrix}}_{C} \;\underbrace{\begin{bmatrix}1&2&3\end{bmatrix}}_{R}$$

<!-- 검산: M([[1],[2]]) * M([[1,2,3]]) == M([[1,2,3],[2,4,6]]) -->

$C \times R$은 **"재료를 1배, 2배, 3배 해서 왼쪽부터 나란히 세워라"** 로 읽는다. `[외부 추론]`

**스스로 확인하는 법:** $C \times R$을 직접 계산해 원래 행렬이 나오는지 보면 된다. (위 검산 주석이 바로 그 계산이다.)

### 3.3 "한 방향"이라는 말

$(1,2)$를 원점 $(0,0)$에서 $(1,2)$로 가는 화살표로 그린다. $(2,4)$는 그 화살표를 2배로 늘린 것, $(3,6)$은 3배로 늘린 것이다. 세 화살표가 **같은 직선** 위에 있으므로 "열이 한 방향뿐"이다. `[외부 추론]`

반대로 $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$의 두 열 $(1,3)$과 $(3,1)$은 서로 다른 직선 위에 있다. 재료 하나로는 못 만든다 (3절 끝 (다)에서 확인).

### 3.4 빠지기 쉬운 곳

$R$을 찾을 때는 **열 전체**를 **재료 열 전체**와 견준다. 즉 $(2,4)$를 $(1,2)$와 비교해서 "2배"라고 보는 것이다.

열 하나 **안에서** 위·아래를 견주면 (예: 열$_1$에서 $2 \div 1 = 2$) 다른 숫자가 나온다. 그런데 그것은 **틀린 관찰이 아니라 다른 질문** (3.5)의 답이다. "열 안의 위·아래 비"는 행 쪽 이야기를 미리 보여 주는 것뿐이다. `[외부 추론]`

### 3.5 같은 식을 행으로 읽으면

$A_2$를 이번엔 **행**으로 잘라 본다:

| 행 | = 재료 행 × 배수 | 관계 |
|---|---|---|
| 행$_1$ = $(1,2,3)$ | $= 1 \times (1,2,3)$ | $R$의 1배 |
| 행$_2$ = $(2,4,6)$ | $= 2 \times (1,2,3)$ | $R$의 2배 |

배수 1, 2를 **세로**로 적으면 $C = \begin{bmatrix}1\\2\end{bmatrix}$가 다시 나온다.

| 열로 읽기 | 행으로 읽기 | 뜻 | 몇 배인지는 누가 알려 주나 |
|---|---|---|---|
| $A = CR$ | $A = CR$ (같은 식) | 열이 재료 열 $C$의 몇 배 | $R$ (가로)이 알려 줌 |
| $A = CR$ | $A = CR$ (같은 식) | 행이 재료 행 $R$의 몇 배 | $C$ (세로)가 알려 줌 |

같은 곱 $CR$을 열 쪽에서 보면 $R$이 배수를, 행 쪽에서 보면 $C$가 배수를 담당한다. `[외부 추론]`

### 3.6 같은 것은 개수다

- 열은 **3**개지만, 재료 열은 **1**개.
- 행은 **2**개지만, 재료 행은 **1**개.
- 그 "1"이 열 쪽·행 쪽에서 **똑같다.**

**"$C$와 $R$이 같다는 말이 아니다."** 같은 것은 *재료의 개수*다. 이 개수의 이름이 **rank**(계수)다. 여기서 이름을 처음 준다. `[외부 추론]`

- $A_2$의 rank = 1
- $A_4$의 rank = 2

> **여기까지 확인된 것과 아닌 것**
>
> - **확인됨:** 열 하나 × 행 하나 꼴($A_2$처럼)에서는 식의 꼴에서 rank 1이 바로 보인다.
> - **아직 안 보임:** 재료가 둘·셋일 때도 열 쪽 수 = 행 쪽 수인지는 이 영상에서는 안 보였다 (01·06·09에서).
> - **주의:** 위 계산은 예 하나이지, "모든 행렬이 $CR$으로 쪼개진다"의 **증명**은 아니다. `[외부 추론]`

<details>
<summary>곁가지 — 지금은 건너뛰어도 된다</summary>

- 재료 열이 $r$개면 $C$는 열 $r$개, $R$은 행 $r$개. (여기서는 $r=1$.) `[외부 추론]`
- $A_2$의 숫자 개수는 6개인데 $C$(2개) + $R$(3개) = 5개로 줄었다. 하지만 "정보 5개"라고 하면 안 된다: $C$를 2배로, $R$을 $\tfrac{1}{2}$배로 해도 같은 행렬이 나온다. 즉 $C$와 $R$ 각각의 크기는 고정되지 않는다. `[외부 추론]`

</details>

### 가리고 해 보기

**(가)** 빈칸 계산

$$\begin{bmatrix}1\\3\end{bmatrix}\begin{bmatrix}2&4\end{bmatrix} = \;?$$

계산 **전에** 예상해 본다: "둘째 열은 첫째 열의 몇 배일까?" → $4 \div 2 = 2$배. 그래서 둘째 행도 첫째 행의 2배여야 한다.

답: $\begin{bmatrix}2&4\\6&12\end{bmatrix}$

<!-- 검산: M([[1],[3]]) * M([[2,4]]) == M([[2,4],[6,12]]) -->

**(나)** 거꾸로 — $\begin{bmatrix}2&6\\1&3\end{bmatrix}$을 열 하나 × 행 하나로 써라.

답: $\begin{bmatrix}2\\1\end{bmatrix}\begin{bmatrix}1&3\end{bmatrix}$

<!-- 검산: M([[2],[1]]) * M([[1,3]]) == M([[2,6],[1,3]]) -->

참고: 답이 하나가 아니다. $\begin{bmatrix}1\\F(1,2)\end{bmatrix}\begin{bmatrix}2&6\end{bmatrix}$도 같은 행렬을 만든다.

<!-- 검산: M([[1],[F(1,2)]]) * M([[2,6]]) == M([[2,6],[1,3]]) -->

다만 $CR$ 분해의 $C$는 원래 행렬의 **열에서 고른 것**이어야 하므로, $\begin{bmatrix}1\\F(1,2)\end{bmatrix}$은 원래 행렬의 열이 아니므로 그쪽은 $CR$은 아니다. `[외부 추론]`

**(다)** 반례 — $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$도 열 하나 × 행 하나로 되나?

안 된다. 열$_1$(1,3)과 열$_2$(3,1)이 서로 배수가 아니어서(1×$k$=3이면 $k$=3인데, 3×$k$=1이면 $k$=⅓ → 모순), 재료 열 하나로는 두 열을 모두 못 만든다.

<details>
<summary>맞춰 보기 (먼저 해 본 뒤에 연다)</summary>

**(가)** $\begin{bmatrix}2&4\\6&12\end{bmatrix}$

<!-- 검산: M([[1],[3]]) * M([[2,4]]) == M([[2,4],[6,12]]) -->

**(나)** $CR$: $\begin{bmatrix}2\\1\end{bmatrix}\begin{bmatrix}1&3\end{bmatrix}$

<!-- 검산: M([[2],[1]]) * M([[1,3]]) == M([[2,6],[1,3]]) -->

다른 분해 (CR 아님): $\begin{bmatrix}1\\F(1,2)\end{bmatrix}\begin{bmatrix}2&6\end{bmatrix}$

<!-- 검산: M([[1],[F(1,2)]]) * M([[2,6]]) == M([[2,6],[1,3]]) -->

**(다)** 안 됨. 열$_1$=$(1,3)$, 열$_2$=$(3,1)$이 배수 관계가 아니기 때문.

</details>

---

## 4. 시각별 흐름

| 시각 구간 | 내용 |
|---|---|
| [00:13]–[00:45] | 자기소개, 18.06 영상 언급, "고쳐 말하러 왔다" |
| [00:45]–[00:59] | 선형대수가 더 중요해졌다 / 새 출발점 있다는 것 |
| [00:59]–[01:42] | 새 출발점 천천히 보여 주겠다 / 슬라이드가 강좌 전체 / 새 교재 *Linear Algebra for Everyone* |
| [01:42]–[02:08] | 슬라이드 띄움 (개요) / 첫 줄 $A=CR$ 설명 |
| [02:08]–[03:02] | 다섯 분해: $LU$(소거) → $QR$(직교) → $S$(대칭) 소개 |
| [03:02]–[04:00] | 앞 절반 = 방정식 풀기 / 뒤 절반 = 고유값·고유벡터·특이값 / 특이값이 꼭대기 / "두세 조각으로 쪼개기" |
| [04:00]–[04:08] | "진짜 18.06 영상으로 가세요" / Thanks |

여기서 쓰고 있다고 한 책은 6판이 아니라 *Linear Algebra for Everyone* `[Vision 00 01:23]`.

---

## 5. 말과 기호

| 영어 | 우리말 | 이 영상에서의 자리 |
|---|---|---|
| column / row | 열 / 행 | $C$는 "column matrix", $R$은 "row matrix" `[01:55]` |
| independent columns | 독립인 열 | 슬라이드 1줄 설명: "Independent columns in $C$" |
| elimination | 소거 (소거법) | $LU$의 설명: "for elimination for solving equations" `[02:25]` |
| triangular matrix | 삼각행렬 (위·아래) | 슬라이드 2줄: "Triangular matrices $L$ and $U$" |
| orthogonal / perpendicular | 직교 / 수직 | "There is the word orthogonal or perpendicular." `[Vision 00 02:46]` |
| symmetric matrix | 대칭행렬 | "S is for a symmetric matrix" `[02:58]` |
| eigenvalue / eigenvector | 고유값 / 고유벡터 | 뒤 절반의 두 축 `[03:11]` |
| singular value | 특이값 | "That's the high point of the theory." `[Vision 00 03:36]` |
| factorization | 분해 (인수분해) | 이 영상에서는 이 낱말을 안 쓰고 "breaking a matrix into two or three pieces"라고 한다 `[03:39]` |

---

## 6. 어디에 쓰이나 — 짧게 `[외부 추론]`

**어디에.** 숫자 자료를 표로 적으면 행렬이다. 행이 사람·가구·환자, 열이 키·무게·혈압 같은 변수. $A_2$처럼 "2행 3열"이면 사람 2명·변수 3개, 또는 사람 3명·변수 2개.

**방금 본 수학이 설명하는 것.** $A_2$에서 둘째 행이 첫째 행의 2배인 것은, "새 방향을 보태지 않는다"는 뜻이다. 2개 줄처럼 보여도 실제로는 1개 줄의 정보를 2배로 반복한 것. rank 1 = 독립인 방향 1개.

**여기까지는 말해 주지 않는다.** 독립인 방향의 수가 곧 현실의 "원인"의 수는 아니다. "몇 배"인 행도 관측(측정)으로는 필요할 수 있다. 실제 자료에는 잡음이 있어서 "정확히 2배"가 거의 나오지 않는다 → 나중에 특이값(6줄)이 필요해진다.

**"수학적 의미를 가지고 현실에 정답처럼 적용하면 안 된다."**

---

## 7. 본 뒤에 — 말로 설명해 보기

1. 스트랭이 영상을 새로 고쳐 말하는 이유가 둘은?
2. 슬라이드 여섯 줄에 공통된 꼴은? 조각들이 다른 점은?
3. 앞 절반·뒤 절반은 각각 무엇에 관한 이야기이고, $CR$은 어디에 속하며 왜 따로(첫 줄로) 강조되나?
4. $\begin{bmatrix}1\\2\end{bmatrix}\begin{bmatrix}1&2&3\end{bmatrix}$을 계산하지 **않고도** 결과 행렬의 행들이 어떤 관계인지 말할 수 있나?

**이해 단계 적어 두기**

- [ ] 설명을 따라갈 수 있다
- [ ] 빈 종이에 다시 쓸 수 있다
- [ ] 처음 보는 짧은 문제에 쓸 수 있다

**남은 질문:** (여기에 적는다)
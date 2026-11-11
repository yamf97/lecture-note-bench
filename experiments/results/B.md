<!-- run_gateway.py
  model: qwen/qwen3.8-flash
  reasoning: high via reasoning.effort (stream)
  prompt: docs/experiments/2026-09-22_gpt-oss-120b_vision00_prompt2-directive.md
  elapsed_s: 508.9
  usage: {"prompt_tokens": 5120, "completion_tokens": 31962, "total_tokens": 37082, "cost": 0.01510406, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 5120, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.01510406, "upstream_inference_prompt_cost": 8.192e-05, "upstream_inference_completions_cost": 0.01502214}, "completion_tokens_details": {"reasoning_tokens": 25890, "image_tokens": 0, "audio_tokens": 0}}
  finish_reason: stop
  date: 2026-09-23 01:03
-->

---
type: note
scope: "Vision 00 「Intro: A New Way to Start Linear Algebra」 (2020, 4분 09초) — 영상 전체"
layer: 지도 층 (예고편)
sources:
  - "자막 전문 (Vision 00)"
  - "슬라이드 2/30 (영상 01:42)"
  - "Strang, Introduction to Linear Algebra 6판 (2023) 목차"
---

### 0. frontmatter

위 YAML에 `type`, `scope`, `layer`, `sources`를 적었다.

### 제목과 맨 위 상자

# Vision 00 — 예고편: 선형대수를 새로 시작하는 법

> **지금 할 수 있어야 하는 것**
>
> - ① 이 영상 묶음이 무엇인지 한두 문장으로 말한다
> - ② "행렬을 조각의 곱으로 쓴다"가 무슨 뜻인지 작은 행렬 하나로 보여 준다 (→ 3절)
> - ③ 슬라이드 여섯 줄이 첫 줄 / 앞 절반 / 뒤 절반으로 어떻게 나뉘는지 말한다 (→ 2절)

> **나중에 돌아올 것**: LU · QR · $Q\Lambda Q^{\mathrm T}$ · $X\Lambda X^{-1}$ · $U\Sigma V^{\mathrm T}$가 각각 무엇인지 — 하나하나가 책의 한 장. 지금 몰라도 된다.

### 「읽는 법」 표

| 표기 | 뜻 |
|---|---|
| `[Vision 00 01:47]` | Vision 00 영상에서 그 말이 시작되는 큐의 시각. 한 문장이 여러 큐에 걸쳐 있으면 이어 붙이고, 첫 큐 시각을 쓴다. |
| `슬라이드 2/30` | 영상 01:42에 띄운 슬라이드. 30장 중 2번 째 장에 적힌 내용. |
| `Strang ILA §3.2` | Strang, *Introduction to Linear Algebra* 6판 목차의 절. 여기서는 §3.2 Computing the Nullspace by Elimination: $A = CR$ 같은 제목을 뜻한다. |
| `[외부 추론]` · 인용 형식 | `[외부 추론]`은 출처를 가르는 표시일 뿐, 맞다는 보증은 아니다. 인용은 번역 먼저, 원문 아래. 원문 바로 뒤 같은 줄에 `[Vision 00 mm:ss]`를 둔다. |

### 1. 이 영상은 무엇인가

1. 길버트 스트랭은 OpenCourseWare나 YouTube에 있는 18.06 선형대수 영상을 알고 좋아하면 좋겠다며, 그 영상들을 여러 이유로 새로 고쳐 말하러 왔다고 한다. 고치는 첫 번째 이유는 그 사이 선형대수 전체가 더 중요해졌다는 것이고, 두 번째 이유는 지금 가르칠 때 새로운 출발점이 생겼다는 것이다.

   > (번역) 다행히, 이 과목 전체가 점점 더 필수적이고, 점점 더 중요하고, 점점 더 아름다워졌다.
   >
   > (원문) "Fortunately, the whole subject has just become more and more essential, more and more important, more and more beautiful." `[Vision 00 00:45]`

   > (번역) 그리고 또한 내가 지금 가르칠 때, 새로운 출발점이 있다.
   >
   > (원문) "And also, when I teach it now, I have a new starting point." `[Vision 00 00:59]`

2. 슬라이드가 강좌 전체를 말해 준다는 말이 있다. 짧은 영상 안에 전체 강좌가 있다는 것은 무리라고도 한다.

   > (번역) 슬라이드가 전체 강좌를 말해 준다. 짧은 영상 안에 전체 강좌가 있다는 것은 말이 안 된다.
   >
   > (원문) "The slides tell you the whole course. And that's crazy to have a full course within a short video." `[Vision 00 01:10]`

3. 끝의 당부: 진짜 18.06 영상으로 가라는 말.

   > (번역) 그리고 세부 내용은 진짜 18.06 영상으로 가 주십시오.
   >
   > (원문) "And please go to the real 18.06 videos for the details." `[Vision 00 04:00]`

   `[외부 추론]` 이 말은 이 영상이 세부 강의를 채우는 층이 아니라, 앞으로 갈 영상을 지도로 그려 주는 층이라는 근거가 된다.

### 2. 슬라이드 한 장 — 여섯 줄

1. `[Vision 00 01:42]`에서 스트랭은 슬라이드를 전체 영상의 개요라고 한다. 여섯 줄이 모두 같은 꼴이다: 왼쪽 행렬 하나 = 오른쪽 둘 또는 셋의 곱.

   > (번역) 따라서 이것은 전체 영상의 개요다.
   >
   > (원문) "So this is an outline of the whole video." `[Vision 00 01:42]`

2. **표**

   | 줄 | 식 | 슬라이드에 적힌 설명 (원문) | 쉬운 말 `[외부 추론]` | 어느 영상 · 책 어디 |
   |---:|---|---|---|---|
   | 1 | `$A = CR$` | `Independent columns in $C$` | $C$의 열들이 서로 같은 방향에 놓이지 않은, 즉 독립인 열들을 담는다는 뜻. 지금 예 $A_2$는 재료가 하나지만, 일반 $CR$에서는 여러 개일 수 있다. | `01, 06, 09 / §1.4 Matrix Multiplication $AB$ and $CR$ · §3.2 Computing the Nullspace by Elimination: $A = CR$` |
   | 2 | `$A = LU$` | `Triangular matrices $L$ and $U$` | $L$과 $U$는 대각선 한쪽이 비어 있는 삼각 행렬이라 계산이 쉽다. | `02 / §2.3 Matrix Computations and $A = LU$` |
   | 3 | `$A = QR$` | `Orthogonal columns in $Q$` | $Q$의 열들은 서로 수직이다. 계산에 좋은 방향을 잡는다는 뜻이다. | `03 / §4.4 Orthonormal Bases and Gram-Schmidt` |
   | 4 | `$S = Q\Lambda Q^{\mathrm T}$, $Q^{\mathrm T} = Q^{-1}$` | `Orthogonal eigenvectors $Sq = \lambda q$` | 대칭 행렬 $S$는 서로 수직인 고유벡터 $q$들을 갖는다. | `04 / §6.3 Symmetric Positive Definite Matrices` |
   | 5 | `$A = X\Lambda X^{-1}$` | `Eigenvalues in $\Lambda$ · Eigenvectors in $X$ · $Ax = \lambda x$` | 정사각 행렬 $A$를 고유값과 고유벡터로 쪼갠다. | `04 / §6.2 Diagonalizing a Matrix` |
   | 6 | `$A = U\Sigma V^{\mathrm T}$` | `Diagonal $\Sigma$ = Singular values $\sigma = \sqrt{\lambda(A^{\mathrm T}A)}$ · Orthogonal vectors in $U^{\mathrm T}U = V^{\mathrm T}V = I$ · $Av = \sigma u$` | $U$와 $V$의 열들이 각각 서로 수직이고, 대각선 $\Sigma$에 특이값이 들어 있다. 직사각 등 어떤 모양에도 쓸 수 있다. | `05 / §7.1 Singular Values and Singular Vectors` |

   `[원문 미확인]` 책 절은 목차 제목만 확인했고, 절 본문은 이 자료에 없음.

   > 이 표에서 지금 가져갈 것은 하나다 — 여섯 줄이 모두 같은 꼴이라는 것. 1줄은 3절에서 직접 해 본다. 나머지 다섯 줄은 **읽고 지나가면 된다**.

4. **조건 표** `[외부 추론]`

   | 줄 | 어떤 행렬에 되나? | 짧은 이유/예 |
   |---|---|---|
   | `$CR$` | 모든 모양 | 행렬의 열들을 재료 열의 몇 배로 나타내는 방식. |
   | `$U\Sigma V^{\mathrm T}$` | 모든 모양 | 특이값 분해는 직사각에도 가능하다고 한다. |
   | `$QR$` | 직사각도 됨 | 수직인 열을 세우는 계산이므로 정사각에 한정되지 않는다. |
   | `$LU$` | 행 바꿈이 필요한 행렬이 있음 | 예: `$\begin{bmatrix}0&1\\1&0\end{bmatrix}$`은 왼쪽 위가 0이라 그대로는 소거를 시작할 수 없다. 행을 바꾸어야 하므로 그대로의 $LU$가 안 된다. |
   | `$Q\Lambda Q^{\mathrm T}$` | 대칭행렬만 | 슬라이드 설명이 대칭 $S$에 고유벡터가 직교한다고 한다. |
   | `$X\Lambda X^{-1}$` | 정사각 + 독립인 고유벡터가 열 수만큼 | 반례: 90° 회전 `$\begin{bmatrix}0&-1\\1&0\end{bmatrix}$`은 실수 고유벡터가 없다. |

5. **소절 「첫 줄 / 앞 절반 / 뒤 절반」**

   - 첫 줄이 $C$(열)와 $R$(행)의 곱 `[01:47]`:

     > (번역) 그리고 첫 줄은, 내 머릿속에서는 행렬 A로 생각하는 것인데, C 행렬, 즉 열 행렬과 행 행렬 R의 곱이다.
     >
     > (원문) "And the first line, which I think about in my mind as matrix A, is a product of a C matrix, a column matrix, and a row matrix R." `[Vision 00 01:47]`

   - 나머지 다섯 줄은 핵심 장들의 이름표 `[02:08]`:

     > (번역) 그러면 이것들은 선형대수의 주요 장들의 다섯 가지 유명한 핵심 약어 설명이다, 그 주요 장들.
     >
     > (원문) "Then these are five famous essential shorthand descriptions of the key chapters of linear algebra, the key chapters." `[Vision 00 02:08]`

   - $LU$ = 소거, 첫 번째 일 `[02:25]`:

     > (번역) 그리고 컴퓨터 명령은 정확히 그 글자들 LU일 것이다, 방정식을 푸는 소거에 대한, 선형대수의 첫 일.
     >
     > (원문) "And computer commands would be exactly those letters LU for elimination for solving equations, the first job of linear algebra." `[Vision 00 02:25]`

   - 앞 절반은 방정식 풀기, 뒤 절반은 고유값·고유벡터·특이값 `[03:02]`:

     > (번역) 아, 그래야겠다, 첫 절반은, 거기서, QR에서 끝나는데, 방정식을 푸는 것이다. 둘째 절반, 이것 셋은 고유값과 고유벡터와 특이값에 관한 것이다,
     >
     > (원문) "oh, well, I should say, the first half, ending with there, with QR, is about solving equations. The second half, these three are about eigenvalues and eigenvectors and singular values," `[Vision 00 03:02]`

   - 특이값이 이론의 꼭대기, 모두 "두세 조각으로 쪼개기" `[03:36]`:

     > (번역) 그것은 이론의 정점이다. 그리고 그것은 다른 모든 것들과 같이 행렬을 두세 조각으로, 두세 부분으로 쪼개는 것으로 표현된다.
     >
     > (원문) "That's the high point of the theory. And it's expressed like all the others as breaking a matrix into two or three pieces, two or three parts." `[Vision 00 03:36]`

   | 범위 | 줄 | 무슨 이야기 | 우리의 층 `[외부 추론]` |
   |---|---|---|---|
   | 앞 절반 | 1·2·3줄 | 방정식 풀기와 관련된 이야기. $LU$는 소거, $QR$은 수직인 열, 첫 줄 $CR$은 열 재료와 만드는 법. | 1줄만 익히는 층, 나머지 2·3줄은 지도 층 |
   | 뒤 절반 | 4·5·6줄 | 고유값, 고유벡터, 특이값 이야기. 대칭행렬의 고유벡터, 대각화, 특이값 분해. | 모두 지도 층 |

   `[외부 추론]` **선형대수의 핵심 장 하나하나가 행렬을 몇 조각의 곱으로 쪼개는 한 가지 방법이고, 조각마다 성질이 다르다** — 이것이 이 4분의 핵심이다.

### 3. "행렬을 조각의 곱으로 쓴다"는 게 무슨 말인가 `[외부 추론]`

스트랭은 이 영상에서 숫자 예를 들지 않는다(01에서 든다). 기준 행렬 $A_2$로 맛만 본다.

#### 3.1 열을 하나씩 잘라서 본다.

$$A_2 = \begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}$$

열을 따로 쓰면:

$$\begin{bmatrix}1\\2\end{bmatrix},\quad \begin{bmatrix}2\\4\end{bmatrix},\quad \begin{bmatrix}3\\6\end{bmatrix}$$

| 열 | 재료 열로 나타내기 | 배수 |
|---|---|---|
| `열1 = (1,2)` | `= 1 × (1,2)` | 1배 |
| `열2 = (2,4)` | `= 2 × (1,2)` | 2배 |
| `열3 = (3,6)` | `= 3 × (1,2)` | 3배 |

결론: 세 열이 모두 **같은 재료 $(1,2)$의 몇 배**다.

#### 3.2 재료와 만드는 법.

$$
\underbrace{A_2}_{\text{행렬}}
=
\underbrace{\begin{bmatrix}1\\2\end{bmatrix}}_{C\text{ (재료)}}
\underbrace{\begin{bmatrix}1&2&3\end{bmatrix}}_{R\text{ (만드는 법)}}
$$

<!-- 검산: M([[1],[2]]) * M([[1,2,3]]) == M([[1,2,3],[2,4,6]]) -->

`[외부 추론]` $C\times R$은 "재료를 1배, 2배, 3배 해서 왼쪽부터 나란히 세워라"로 읽는다.

`[외부 추론]` 스스로 확인하는 법: $C\times R$을 직접 계산해 원래 행렬이 나오는지 보면 된다.

#### 3.3 "한 방향"이라는 말.

`[외부 추론]` $(1,2)$를 원점에서 출발하는 화살표로 보면, $(2,4)$는 같은 화살표를 2배로 늘인 것, $(3,6)$은 3배로 늘인 것이다. 그러니 세 화살표는 같은 직선 위에 있다. 그래서 "열이 한 방향뿐"이라고 한다.

대비로 $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$의 두 열은 다른 직선 위에 있다. 재료 하나로는 두 열을 모두 만들 수 없다. (3절 끝 (다)에서 확인)

#### 3.4 빠지기 쉬운 곳.

`[외부 추론]` $R$을 찾을 때는 **열 전체**를 재료 열 전체와 견준다. 열 하나 **안에서** 위·아래를 견주면(여기서는 아래가 늘 위의 2배) 다른 숫자가 나오는데, 그것은 틀린 관찰이 아니라 다른 질문(3.5)의 답이다.

#### 3.5 같은 식을 행으로 읽으면.

| 행 | 재료 행으로 나타내기 | 관계 |
|---|---|---|
| `행1 = (1,2,3)` | `= 1 × (1,2,3)` | R의 1배 |
| `행2 = (2,4,6)` | `= 2 × (1,2,3)` | R의 2배 |

배수 1, 2를 세로로 적으면 $C$가 다시 나온다.

| 읽기 | 뜻 | 몇 배인지는 누가 알려 주나 |
|---|---|---|
| 열로 읽기 | 열들이 재료 열의 몇 배인지 | $R$ |
| 행으로 읽기 | 행들이 재료 행의 몇 배인지 | $C$ |

#### 3.6 같은 것은 개수다.

`[외부 추론]` 열은 셋이지만 재료 열은 하나, 행은 둘이지만 재료 행은 하나. 개수가 똑같이 1이다.

`[외부 추론]` **"$C$와 $R$이 같다는 말이 아니다"** — 같은 것은 재료의 개수다. 이 개수의 이름이 **rank**이다(여기서 처음 이름을 준다). $A_2$의 rank 1, $A_4$의 rank 2.

> `[외부 추론]` **여기까지 확인된 것과 아닌 것**
>
> - 열 하나×행 하나 꼴에서는 식의 꼴에서 바로 나온다.
> - 재료가 둘·셋일 때도 열 쪽 수 = 행 쪽 수인지는 아직 안 보였다(01·06·09에서).
> - 위 계산은 예 하나이지 "모든 행렬이 $CR$로 쪼개진다"의 증명이 아니다.

<details>
<summary>곁가지 — 지금은 건너뛰어도 된다</summary>

`[외부 추론]` 재료 열이 $r$개면 $C$는 열 $r$개, $R$은 행 $r$개다. 숫자 개수가 6에서 5로 줄었지만 "정보 5개"는 아니다. 앞 조각을 2배로 하고 뒤 조각을 반으로 해도 같은 행렬이 될 수 있다.

</details>

#### 「가리고 해 보기」

`[외부 추론]` 먼저 아래 세 개를 종이에 답해 보고, 다 푼 다음에 아래 답을 열자.

- (가) 빈칸 계산:  
  `$$\begin{bmatrix}1\\3\end{bmatrix}\begin{bmatrix}2&4\end{bmatrix}$$`  
  계산하기 전에 예측하라: 둘째 열은 첫째 열의 몇 배일까?
- (나) 거꾸로:  
  `$$\begin{bmatrix}2&6\\1&3\end{bmatrix}$$`을 열 하나 × 행 하나로 쓰라.
- (다) 반례:  
  $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$도 열 하나 × 행 하나로 되나? 안 되면 한 문장으로 왜.

<details>
<summary>맞춰 보기 (먼저 해 본 뒤에 연다)</summary>

(가)

$$
\begin{bmatrix}1\\3\end{bmatrix}
\begin{bmatrix}2&4\end{bmatrix}
=
\begin{bmatrix}2&4\\6&12\end{bmatrix}
$$

둘째 열은 첫째 열의 2배다.

<!-- 검산: M([[1],[3]]) * M([[2,4]]) == M([[2,4],[6,12]]) -->

(나)

예를 들어:

$$
\begin{bmatrix}2\\1\end{bmatrix}
\begin{bmatrix}1&3\end{bmatrix}
=
\begin{bmatrix}2&6\\1&3\end{bmatrix}
$$

<!-- 검산: M([[2],[1]]) * M([[1,3]]) == M([[2,6],[1,3]]) -->

답이 하나가 아니다:

$$
\begin{bmatrix}1\\1/2\end{bmatrix}
\begin{bmatrix}2&6\end{bmatrix}
=
\begin{bmatrix}2&6\\1&3\end{bmatrix}
$$

<!-- 검산: M([[1],[F(1,2)]]) * M([[2,6]]) == M([[2,6],[1,3]]) -->

다만 $CR$의 $C$는 원래 행렬의 열에서 고른 것이어야 하므로 $\begin{bmatrix}1\\1/2\end{bmatrix}$ 쪽은 $CR$은 아니다.

(다)

안 된다. $A_4$의 두 열 $(1,3)$과 $(3,1)$은 서로 배수 관계가 아니기 때문이다.

<!-- 검산: M([[1],[3]])과 M([[3],[1]])은 배수 관계가 아니다 (k=3이면 3×M([[1],[3]]) = M([[3],[9]]) ≠ M([[3],[1]])) -->

</details>

### 4. 시각별 흐름

| 시각 구간 | 내용 |
|---|---|
| 00:13–00:32 | 자기소개, OpenCourseWare/YouTube의 18.06 선형대수 영상을 언급하며 좋아하면 좋겠다고 한다. |
| 00:32–00:59 | 영상을 새로 고치러 온 이유. 선형대수가 더 중요해졌고, 지금 가르칠 때 새로운 출발점이 생겼다. |
| 01:10–01:42 | 슬라이드가 전체 강좌를 말해 준다고 한다. 새 교과서 *Linear Algebra for Everyone*를 쓰며 새 출발을 강조한다. |
| 01:42–02:20 | 슬라이드 개요. 첫 줄 $A=CR$이 새 출발이고, 나머지 다섯 줄은 핵심 장들의 이름표다. |
| 02:20–03:02 | $LU$는 소거와 방정식 풀기의 첫 일, $QR$은 직교/수직인 열, $S$는 대칭 행렬. |
| 03:02–03:49 | 앞 절반은 방정식 풀기, 뒤 절반은 고유값·고유벡터·특이값. 모두 행렬을 두세 조각으로 쪼갠다. |
| 03:49–04:08 | 계획과 마무리. 세부 내용은 진짜 18.06 영상으로 가라고 한다. |

여기서 쓰고 있다고 한 책은 6판이 아니라 *Linear Algebra for Everyone* `[Vision 00 01:23]`다.

### 5. 말과 기호

| 영어 | 우리말 | 이 영상에서의 자리 |
|---|---|---|
| column / row | 열 / 행 | 첫 줄 $A=CR$: $C$는 열 재료, $R$은 만드는 법. `[Vision 00 01:47]` |
| independent columns | 독립인 열 | 슬라이드 1번 줄: `Independent columns in $C$` |
| elimination | 소거 | $LU$에 대해 `[Vision 00 02:28]`에서 방정식을 푸는 소거라고 한다. |
| triangular matrix | 삼각 행렬 | 슬라이드 2번 줄: `Triangular matrices $L$ and $U$` |
| orthogonal / perpendicular | 직교 / 수직 | 슬라이드 3번 줄과 `[Vision 00 02:46]`에서 직교 또는 수직이라는 말을 쓴다. |
| symmetric matrix | 대칭 행렬 | 슬라이드 4번 줄 $S$와 `[Vision 00 02:58]`에서 대칭 행렬이라고 한다. |
| eigenvalue / eigenvector | 고유값 / 고유벡터 | 뒤 절반 `[Vision 00 03:11]`과 슬라이드 4·5번 줄. |
| singular value | 특이값 | 뒤 절반 `[Vision 00 03:16]`, 이론의 꼭대기 `[Vision 00 03:36]`. |
| factorization | 분해 / 쪼개기 | 이 영상에서는 이 낱말보다 "두세 조각으로 쪼개기" `[Vision 00 03:39]` 표현을 쓴다. |

### 6. 어디에 쓰이나 — 짧게 `[외부 추론]`

**어디에**: 숫자 자료를 표로 적으면 행렬이 된다. 행은 사람·가구 같은 항목, 열은 나이·소득·변수 같은 특징일 수 있다. `[외부 추론]`

**방금 본 수학이 설명하는 것**: $A_2$에서 둘째 행이 첫째 행의 2배라면, 둘째 행은 첫 행에서 새 방향을 보태지 않는다. 열의 재료도 하나뿐이다. `[외부 추론]`

**여기까지는 말해 주지 않는다**: 독립인 방향의 수와 현실의 원인 수가 같지는 않다. 몇 배인 행도 관측으로는 필요하다. 실제 자료에는 잡음이 있어 "정확히 몇 배"가 거의 나오지 않으므로, 나중에 특이값 같은 도구가 필요해진다. `[외부 추론]`

**"수학적 의미를 가지고 현실에 정답처럼 적용하면 안 된다."**

### 7. 본 뒤에 — 말로 설명해 보기

1. 스트랭이 영상을 새로 고쳐 말하는 이유 둘은?
2. 여섯 줄에 공통된 꼴과 조각들이 다른 점은?
3. 앞 절반·뒤 절반은 무엇에 관한 이야기이고, $CR$은 어디 속하며 왜 따로 강조되나?
4. `$$\begin{bmatrix}1\\2\end{bmatrix}\begin{bmatrix}1&2&3\end{bmatrix}$$`을 계산하지 않고도 결과의 행들이 어떤 관계일지 말할 수 있나?

**이해 단계 적어 두기** — 설명을 따라갈 수 있다 / 빈 종이에 다시 쓸 수 있다 / 처음 보는 짧은 문제에 쓸 수 있다

- [ ] 설명을 따라갈 수 있다
- [ ] 빈 종이에 다시 쓸 수 있다
- [ ] 처음 보는 짧은 문제에 쓸 수 있다

**남은 질문**: (여기에 적는다)
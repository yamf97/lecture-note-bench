<!-- run_gateway.py
  model: qwen/qwen3.5-122b-a10b
  reasoning: high via reasoning_effort (stream)
  prompt: docs/experiments/2026-09-22_gpt-oss-120b_vision00_prompt2-directive.md
  elapsed_s: 59.2
  usage: {"prompt_tokens": 5069, "completion_tokens": 8793, "total_tokens": 13862, "cost": 0.01960738, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.01960738, "upstream_inference_prompt_cost": 0.00131794, "upstream_inference_completions_cost": 0.01828944}, "completion_tokens_details": {"reasoning_tokens": 4211, "image_tokens": 0, "audio_tokens": 0}}
  finish_reason: stop
  date: 2026-09-23 00:56
-->

---
type: note
scope: "Vision 00 「Intro: A New Way to Start Linear Algebra」 (2020, 4 분 09 초) — 영상 전체"
layer: 지도 층 (예고편)
sources: 자막 전문, 슬라이드 2/30, 책 목차 (Strang ILA 6 판)
---

# Vision 00 — 예고편: 선형대수를 새로 시작하는 법

> **지금 할 수 있어야 하는 것**
> 1. 이 영상 묶음이 무엇인지 한두 문장으로 말한다.
> 2. "행렬을 조각의 곱으로 쓴다"가 무슨 뜻인지 작은 행렬 하나로 보여 준다 (→ 3 절).
> 3. 슬라이드 여섯 줄이 첫 줄 / 앞 절반 / 뒤 절반으로 어떻게 나뉘는지 말한다 (→ 2 절).
>
> **나중에 돌아올 것**
> - LU · QR · $Q\Lambda Q^{\mathrm T}$ · $X\Lambda X^{-1}$ · $U\Sigma V^{\mathrm T}$가 각각 무엇인지 — 하나하나가 책의 한 장. 지금 몰라도 된다.

## 「읽는 법」 표

| 구분 | 뜻 |
| :--- | :--- |
| `[Vision 00 01:47]` | 자막에서 해당 대사가 시작되는 시각 (분:초) |
| `슬라이드 2/30` | 영상 01:42 에 띄운 슬라이드 중 2 번째 페이지 |
| `Strang ILA §3.2` | 스트랭의 책 *Introduction to Linear Algebra* 6 판 절 번호 |
| `[외부 추론]` | 출처를 가르는 표시일 뿐, 맞다는 보증은 아니다 |
| 인용 형식 | 번역 먼저, 원문 아래 (원문 끝줄에 시각 좌표) |

## 1. 이 영상은 무엇인가

스트랭이 18.06 강의 영상을 새로 고쳐 말하러 왔다는 것을 한 문단으로. 고치는 이유 두 가지를 자막에서 찾아 각각 인용한다.

> (번역) 그리고 저는 오늘 몇 가지 이유로 그것들을 업데이트하기 위해 여기 있습니다.
>
> (원문) "And I'm here today to update them for several reasons." `[Vision 00 00:32]`
>
> (번역) 다행히도 선형대수학 전체 과목이 점점 더 필수적이고, 점점 더 중요하고, 점점 더 아름다워졌습니다.
>
> (원문) "Fortunately, the whole subject has just become more and more essential, more and more important, more and more beautiful." `[Vision 00 00:45]`
>
> (번역) 그리고 또한, 제가 지금 가르칠 때, 새로운 출발점이 있습니다.
>
> (원문) "And also, when I teach it now, I have a new starting point." `[Vision 00 00:59]`

"슬라이드가 강좌 전체를 말해 준다"는 말을 인용합니다.

> (번역) 슬라이드가 전체 과정을 알려 줍니다.
>
> (원문) "The slides tell you the whole course." `[Vision 00 01:10]`

끝의 당부 "진짜 18.06 영상으로 가라"를 인용합니다. 이 말이 "영상 단계 = 지도 그리기"의 근거입니다.

> (번역) 그리고 자세한 내용은 진짜 18.06 영상으로 가십시오.
>
> (원문) "And please go to the real 18.06 videos for the details." `[Vision 00 04:00]`

## 2. 슬라이드 한 장 — 여섯 줄

스트랭이 `[01:42]` 에 슬라이드를 띄우고 개요라고 한다는 것을 한 줄로. **여섯 줄이 모두 같은 꼴**(왼쪽 행렬 하나 = 오른쪽 둘 또는 셋의 곱)임을 말합니다.

| 줄 | 식 | 슬라이드에 적힌 설명 (원문) | 쉬운 말 `[외부 추론]` | 어느 영상 · 책 어디 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | $A = CR$ | Independent columns in $C$ | $C$ 는 독립인 열들로 구성됨 | 01 Column Space · §3.2 |
| 2 | $A = LU$ | Triangular matrices $L$ and $U$ | 삼각 행렬 $L$ 과 $U$ 로 나눔 | 02 Big Picture · §2.3 |
| 3 | $A = QR$ | Orthogonal columns in $Q$ | $Q$ 의 열들이 서로 수직임 | 03 Orthogonal Vectors · §4.4 |
| 4 | $S = Q\Lambda Q^{\mathrm T}$ | Orthogonal eigenvectors $Sq = \lambda q$ | 대칭행렬, 고유벡터가 수직 | 04 Eigenvalues · §6.3 |
| 5 | $A = X\Lambda X^{-1}$ | Eigenvalues in $\Lambda$ · Eigenvectors in $X$ | 고유값과 고유벡터로 분해 | 04 Eigenvalues · §6.2 |
| 6 | $A = U\Sigma V^{\mathrm T}$ | Diagonal $\Sigma$ = Singular values... | 모든 행렬의 꼭대기 이론 | 05 Singular Values · §7.1 |

[원문 미확인]

> 이 표에서 지금 가져갈 것은 하나다 — 여섯 줄이 모두 같은 꼴이라는 것. 1 줄은 3 절에서 직접 해 본다. 나머지 다섯 줄은 **읽고 지나가면 된다**.

### 조건 표 `[외부 추론]`

| 분해법 | 적용 가능한 행렬 조건 | 예시 및 주의점 |
| :--- | :--- | :--- |
| $CR$ · $U\Sigma V^{\mathrm T}$ | 모든 모양 (사각, 정사각) | 가장 일반적 |
| $QR$ | 직사각도 됨 | $Q$ 는 직교열 필요 |
| $LU$ | 행 바꿈이 필요한 행렬 있음 | $\begin{bmatrix}0&1\\1&0\end{bmatrix}$ 는 그대로 안 됨 (첫 번째 pivot 이 0) |
| $Q\Lambda Q^{\mathrm T}$ | 대칭행렬만 | $S$ 가 대칭이어야 함 |
| $X\Lambda X^{-1}$ | 정사각 + 독립인 고유벡터가 열 수만큼 | 반례: 90° 회전 $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ 은 실수 고유벡터 없음 |

### 소절 「첫 줄 / 앞 절반 / 뒤 절반」

자막에서 다음을 각각 인용합니다.

> (번역) 그리고 첫 줄은... 행렬 A 는 C 행렬... 과 R 행렬의 곱입니다.
>
> (원문) "And the first line... is a product of a C matrix, a column matrix, and a row matrix R." `[Vision 00 01:47]`
>
> (번역) 그리고 이들은 선형대수의 핵심 장들의 이름표입니다.
>
> (원문) "Then these are five famous essential shorthand descriptions of the key chapters of linear algebra." `[Vision 00 02:08]`
>
> (번역) 컴퓨터 명령어는 방정식을 풀기 위한 소거를 위해 정확히 그 문자들 LU 일 것입니다.
>
> (원문) "And computer commands would be exactly those letters LU for elimination for solving equations." `[Vision 00 02:25]`
>
> (번역) 거기에 있는 QR 까지 첫 번째 부분은 방정식을 푸는 것에 관한 것이고, 두 번째 부분은 고유값과 고유벡터와 특이값에 관한 것입니다.
>
> (원문) "the first half, ending with there, with QR, is about solving equations... The second half, these three are about eigenvalues and eigenvectors and singular values." `[Vision 00 03:02]`
>
> (번역) 그것은 이론의 하이라이트입니다.
>
> (원문) "That's the high point of the theory." `[Vision 00 03:36]`

| 구분 | 무슨 이야기 | 우리의 층 |
| :--- | :--- | :--- |
| 앞 절반 (1·2·3 줄) | 방정식 풀기 ($CR, LU, QR$) | 1 줄 ($CR$) 만 익히는 층 |
| 뒤 절반 (4·5·6 줄) | 고유값·고유벡터·특이값 | 나머지 지도 층 |

선형대수의 핵심 장 하나하나가 행렬을 몇 조각의 곱으로 쪼개는 한 가지 방법이고, 조각마다 성질이 다르다.

## 3. "행렬을 조각의 곱으로 쓴다"는 게 무슨 말인가 `[외부 추론]`

첫 줄에 "스트랭은 이 영상에서 숫자 예를 들지 않는다 (01 에서 든다). 기준 행렬 $A_2$로 맛만 본다"를 씁니다. 그리고 소절 여섯 개를 **이 순서로**:

### 3.1 열을 하나씩 잘라서 본다.

$$
A_2 = \begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}
$$

열 1·열 2·열 3 을 각각 세로 벡터로 따로 씁니다.

| 열 | 값 | 관계 | 배수 |
| :--- | :--- | :--- | :--- |
| 열 1 | $\begin{bmatrix}1\\2\end{bmatrix}$ | $= 1 \times \begin{bmatrix}1\\2\end{bmatrix}$ | 1 배 |
| 열 2 | $\begin{bmatrix}2\\4\end{bmatrix}$ | $= 2 \times \begin{bmatrix}1\\2\end{bmatrix}$ | 2 배 |
| 열 3 | $\begin{bmatrix}3\\6\end{bmatrix}$ | $= 3 \times \begin{bmatrix}1\\2\end{bmatrix}$ | 3 배 |

결론 한 줄: 세 열이 모두 **같은 재료 $(1,2)$의 몇 배**다.

### 3.2 재료와 만드는 법.

재료 열 $(1,2)$가 $C$, "1 배·2 배·3 배"를 가로로 적은 $[1\ 2\ 3]$이 $R$. $A_2 = C\,R$을 display 로 `\underbrace` 를 써서 세 덩이에 이름을 붙입니다.

$$
A_2 = \underbrace{\begin{bmatrix}1\\2\end{bmatrix}}_{C} \cdot \underbrace{\begin{bmatrix}1&2&3\end{bmatrix}}_{R}
$$

<!-- 검산: M([[1],[2]]) * M([[1,2,3]]) == M([[1,2,3],[2,4,6]]) -->

"$C\times R$은 '재료를 1 배, 2 배, 3 배 해서 왼쪽부터 나란히 세워라'로 읽는다"를 씁니다. **스스로 확인하는 법**: $C\times R$을 직접 계산해 원래 행렬이 나오는지 보면 됩니다.

### 3.3 "한 방향"이라는 말.

$(1,2)$를 원점에서의 화살표로 설명하고, $(2,4)$·$(3,6)$은 같은 화살표를 늘인 것 → 세 화살표가 같은 직선 위 → "열이 한 방향뿐". 대비로 $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$의 두 열은 다른 직선 위 — 재료 하나로는 못 만든다 (3 절 끝 (다) 에서 확인).

### 3.4 빠지기 쉬운 곳.

$R$을 찾을 때는 **열 전체**를 재료 열 전체와 견줍니다. 열 하나 **안에서** 위·아래를 견주면 (아래가 늘 위의 2 배) 다른 숫자가 나오는데, 그것은 틀린 관찰이 아니라 다른 질문 (3.5) 의 답이다.

### 3.5 같은 식을 행으로 읽으면.

$A_2$를 행으로 잘라 **표** 두 행:

| 행 | 값 | 관계 | 배수 |
| :--- | :--- | :--- | :--- |
| 행 1 | $\begin{bmatrix}1&2&3\end{bmatrix}$ | $= 1 \times \begin{bmatrix}1&2&3\end{bmatrix}$ | R 의 1 배 |
| 행 2 | $\begin{bmatrix}2&4&6\end{bmatrix}$ | $= 2 \times \begin{bmatrix}1&2&3\end{bmatrix}$ | R 의 2 배 |

배수 1, 2 를 세로로 적으면 $C$가 다시 나온다.

| 읽기 | 뜻 | 몇 배인지는 누가 알려 주나 |
| :--- | :--- | :--- |
| 열로 읽기 | 열들이 어떤 재료의 배수인가 | $R$ |
| 행으로 읽기 | 행들이 어떤 재료의 배수인가 | $C$ |

### 3.6 같은 것은 개수다.

열은 셋이지만 재료 열은 하나, 행은 둘이지만 재료 행은 하나, 개수가 똑같이 1. **"$C$와 $R$이 같다는 말이 아니다"** — 같은 것은 재료의 개수. 이 개수의 이름이 **rank**(여기서 처음 이름을 준다). $A_2$의 rank 1, $A_4$의 rank 2.

> 여기까지 확인된 것과 아닌 것
> - 열 하나×행 하나 꼴에서는 식의 꼴에서 바로 나온다
> - 재료가 둘·셋일 때도 열 쪽 수 = 행 쪽 수인지는 아직 안 보였다 (01·06·09 에서)
> - 위 계산은 예 하나이지 "모든 행렬이 $CR$로 쪼개진다"의 증명이 아니다

<details><summary>곁가지 — 지금은 건너뛰어도 된다</summary>
재료 열이 $r$개면 $C$는 열 $r$개, $R$은 행 $r$개 · 숫자 개수가 6 에서 5 로 줄었지만 "정보 5 개"는 아니다 (앞 조각 2 배, 뒤 조각 반으로 해도 같은 행렬).
</details>

### 「가리고 해 보기」

(가) 빈칸 계산 — $\begin{bmatrix}1\\3\end{bmatrix}\begin{bmatrix}2&4\end{bmatrix}=?$ 계산 **전에** "둘째 열은 첫째 열의 몇 배일까"를 예측하게 한다.
(나) 거꾸로 — $\begin{bmatrix}2&6\\1&3\end{bmatrix}$을 열 하나×행 하나로.
(다) 반례 — $A_4$도 열 하나×행 하나로 되나? 안 되면 한 문장으로 왜.

<details><summary>맞춰 보기 (먼저 해 본 뒤에 연다)</summary>

(가) 결과: $\begin{bmatrix}2&4\\6&12\end{bmatrix}$. 둘째 열은 첫째 열의 2 배.
<!-- 검산: M([[1],[3]]) * M([[2,4]]) == M([[2,4],[6,12]]) -->

(나) $\begin{bmatrix}2\\1\end{bmatrix}\begin{bmatrix}1&3\end{bmatrix}$ 또는 $\begin{bmatrix}1\\1/2\end{bmatrix}\begin{bmatrix}2&6\end{bmatrix}$. 답이 하나가 아니다. 다만 $CR$의 $C$는 원래 행렬의 열에서 고른 것이어야 하므로 전자가 더 적합함.
<!-- 검산: M([[2],[1]]) * M([[1,3]]) == M([[2,6],[1,3]]) -->

(다) 안 됨. $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$의 두 열은 서로 비례하지 않으므로 하나의 재료 열로 만들 수 없음.
</details>

## 4. 시각별 흐름

| 시각 구간 | 내용 |
| :--- | :--- |
| 00:13 ~ 00:32 | 인사 및 기존 18.06 강의 언급 |
| 00:32 ~ 00:59 | 업데이트 이유 (중요성 증가, 새로운 출발점) |
| 00:59 ~ 01:42 | 새 출발점 소개 및 교재 언급 |
| 01:42 ~ 02:08 | 슬라이드 개요 제시 (첫 줄 $CR$ 강조) |
| 02:08 ~ 03:02 | 나머지 5 가지 분해법 소개 ($LU, QR$ 등) |
| 03:02 ~ 03:49 | 뒷부분 주제 (고유값, 특이값) 및 이론의 꼭대기 |
| 03:49 ~ 04:08 | 요약 및 실제 18.06 영상 시청 권유 |

여기서 쓰고 있다고 한 책은 6 판이 아니라 *Linear Algebra for Everyone* `[Vision 00 01:23]`.

## 5. 말과 기호

| 영어 | 우리말 | 이 영상에서의 자리 |
| :--- | :--- | :--- |
| column/row | 열/행 | 행렬을 나누는 기본 단위 |
| independent columns | 독립인 열들 | $C$ 행렬의 조건 ($CR$ 분해) |
| elimination | 소거 | $LU$ 분해의 목적 (방정식 풀기) |
| triangular matrix | 삼각 행렬 | $L$ 과 $U$ 의 모양 |
| orthogonal/perpendicular | 직교/수직 | $Q$ 행렬의 특징 `[Vision 00 02:46]` |
| symmetric matrix | 대칭 행렬 | $S$ 행렬, $Q\Lambda Q^{\mathrm T}$ 대상 |
| eigenvalue/eigenvector | 고유값/고유벡터 | 뒤 절반 주제, $X\Lambda X^{-1}$ 요소 |
| singular value | 특이값 | 이론의 꼭대기, $U\Sigma V^{\mathrm T}$ 요소 |
| factorization | 인수분해 | 이 영상에서는 "breaking a matrix into two or three pieces"라고 함 |

## 6. 어디에 쓰이나 — 짧게 `[외부 추론]`

**어디에**: 숫자 자료를 표로 적으면 행렬 — 행이 사람·가구, 열이 변수. 데이터 분석의 기본 형태입니다.

**방금 본 수학이 설명하는 것**: $A_2$에서 둘째 행이 첫째 행의 2 배 = 새 방향을 보태지 않습니다. 즉, 정보의 중복을 나타냅니다.

**여기까지는 말해 주지 않는다**: 독립인 방향의 수 ≠ 현실의 원인 수 · 몇 배인 행도 관측으로는 필요 · 실제 자료는 잡음이 있어 "정확히 몇 배"가 거의 없다 → 나중에 특이값이 필요해집니다.

**"수학적 의미를 가지고 현실에 정답처럼 적용하면 안 된다."**

## 7. 본 뒤에 — 말로 설명해 보기

1.  스트랭이 영상을 새로 고쳐 말하는 이유 둘
2.  여섯 줄에 공통된 꼴과 조각들이 다른 점
3.  앞 절반·뒤 절반은 무엇에 관한 이야기이고 $CR$은 어디 속하며 왜 따로 강조되나
4.  $\begin{bmatrix}1\\2\end{bmatrix}\begin{bmatrix}1&2&3\end{bmatrix}$을 계산하지 않고도 결과의 행들이 어떤 관계일지 말할 수 있나

**이해 단계 적어 두기**
- 설명을 따라갈 수 있다
- 빈 종이에 다시 쓸 수 있다
- 처음 보는 짧은 문제에 쓸 수 있다

**남은 질문**: (여기에 적는다)
<!-- run_gateway.py
  model: openai/gpt-oss-120b
  reasoning: high via reasoning_effort (stream)
  prompt: docs/experiments/2026-09-22_gpt-oss-120b_vision00_prompt2-directive.md
  elapsed_s: 797.4
  usage: {"prompt_tokens": 5139, "completion_tokens": 40094, "total_tokens": 45233, "cost": 0.007006123, "is_byok": false, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "cost_details": {"upstream_inference_cost": 0.007006123, "upstream_inference_prompt_cost": 0.000190143, "upstream_inference_completions_cost": 0.00681598}, "completion_tokens_details": {"reasoning_tokens": 35200, "image_tokens": 0, "audio_tokens": 0}}
  finish_reason: stop
  date: 2026-09-23 01:08
-->

---
type: note
scope: "Vision 00 「Intro: A New Way to Start Linear Algebra」 (2020, 4분 09초) — 영상 전체"
layer: 지도 층 (예고편)
sources:
  - 자막
  - 슬라이드 2/30
  - 책 목차
---

# Vision 00 — 예고편: 선형대수를 새로 시작하는 법

> **지금 할 수 있어야 하는 것**
> 1. 이 영상 묶음이 무엇인지 한두 문장으로 말한다.  
> 2. “행렬을 조각의 곱으로 쓴다”가 무슨 뜻인지 작은 행렬 하나로 보여 준다. (→ 3절)  
> 3. 슬라이드 여섯 줄이 첫 줄 / 앞 절반 / 뒤 절반으로 어떻게 나뉘는지 말한다. (→ 2절)  
> 
> **나중에 돌아올 것**
> - LU  
> - QR  
> - $Q\Lambda Q^{\mathrm T}$  
> - $X\Lambda X^{-1}$  
> - $U\Sigma V^{\mathrm T}$  
> 각각이 책의 한 장. 지금 몰라도 된다.

## 읽는 법

| 표시 | 뜻 | 예시 인용 |
|---|---|---|
| `[Vision 00 01:47]` | 영상에서 첫 줄이 $C$와 $R$의 곱이라는 설명이 시작되는 시점 | (번역) “첫 줄은 C 행렬(열)과 R 행렬(행)의 곱이다.”<br>(원문) “And the first line, which I think … of a C matrix, a column matrix, and a row matrix R.” `[Vision 00 01:47]` |
| `슬라이드 2/30` | 슬라이드에 적힌 내용 | (번역) “C의 독립적인 열”<br>(원문) “Independent columns in C” (슬라이드 2/30) |
| `Strang ILA §3.2` | 책에서 $A = CR$ 형태를 다루는 절 | (번역) “소거를 이용해 영공간을 구한다: $A = CR$”<br>(원문) “Computing the Nullspace by Elimination: $A = CR$” (Strang ILA §3.2) |
| `[외부 추론]` | 출처를 가르는 표시일 뿐, 맞다는 보증은 아니다 | (번역) “[외부 추론]은 출처를 구분하는 표시이며, 내용이 맞다고 보증하지 않는다.”<br>(원문) “[외부 추론]” |

## 1. 이 영상은 무엇인가

1. 스트랭은 18.06 강의 영상을 새로 고쳐 말하러 왔다. 그는 두 가지 이유를 제시한다.  
   (a) 선형대수가 점점 더 중요해졌다.  
   > (번역) “전체 주제가 점점 더 필수적이고, 더 중요해지고, 더 아름다워졌다.”  
   > (원문) “Fortunately, the whole subject has just become more and more essential, more and more important, more and more beautiful.” `[Vision 00 00:45]`  
   (b) 새로운 시작점을 제시하고 싶다.  
   > (번역) “그리고 지금 가르칠 때, 나는 새로운 시작점을 가지고 있다.”  
   > (원문) “And also, when I teach it now, I have a new starting point.” `[Vision 00 00:59]`  

2. “The slides tell you the whole course.” 라는 말을 한다.  
   > (번역) “슬라이드는 전체 강좌를 알려준다.”  
   > (원문) “The slides tell you the whole course.” `[Vision 00 01:10]`  

3. 영상의 마지막에 “And please go to the real 18.06 videos for the details.” 라고 당부한다. 이는 “영상 단계 = 지도 그리기”의 근거가 된다.  
   > (번역) “실제 18.06 영상을 보라.”  
   > (원문) “And please go to the real 18.06 videos for the details.” `[Vision 00 04:00]`  

## 2. 슬라이드 한 장 — 여섯 줄

1. 스트랭은 `[01:42]`에 슬라이드를 띄우고 “This is an outline of the whole video.” 라고 말한다.  
   > (번역) “이것은 전체 영상의 개요이다.”  
   > (원문) “So this is an outline of the whole video.” `[Vision 00 01:42]`  
   그리고 여섯 줄이 모두 같은 꼴(왼쪽 행렬 = 오른쪽 둘 또는 셋의 곱)임을 강조한다.

2. **표**  

| 줄 | 식 | 슬라이드 설명 (원문) | 쉬운 말 `[외부 추론]` | 영상·책 |
|---|---|---|---|---|
| 1 | $A = CR$ | Independent columns in $C$ | C의 열이 서로 독립적이다 (열이 서로 다른 방향을 가짐) `[외부 추론]` | 영상 01:42, 책 §1.4 |
| 2 | $A = LU$ | Triangular matrices $L$ and $U$ | L과 U는 삼각 행렬이다 (하나는 위쪽, 하나는 아래쪽) `[외부 추론]` | 영상 01:42, 책 §2.3 |
| 3 | $A = QR$ | Orthogonal columns in $Q$ | Q의 열이 직교한다 (서로 수직) `[외부 추론]` | 영상 01:42, 책 §4.4 |
| 4 | $S = Q\Lambda Q^{\mathrm T}$, $Q^{\mathrm T}=Q^{-1}$ | Orthogonal eigenvectors $Sq=\lambda q$ | S는 대칭 행렬이며 고유벡터가 직교한다 `[외부 추론]` | 영상 01:42, 책 §6.3 |
| 5 | $A = X\Lambda X^{-1}$ | Eigenvalues in $\Lambda$·Eigenvectors in $X$·$Ax=\lambda x$ | A는 정사각 행렬이며 고유값·고유벡터가 있다 `[외부 추론]` | 영상 01:42, 책 §6.2 |
| 6 | $A = U\Sigma V^{\mathrm T}$ | Diagonal $\Sigma$ = singular values $\sigma=\sqrt{\lambda(A^{\mathrm T}A)}$·Orthogonal vectors in $U^{\mathrm T}U=V^{\mathrm T}V=I$·$Av=\sigma u$ | 어떤 형태의 행렬도 특이값 분해가 가능하다 `[외부 추론]` | 영상 01:42, 책 §7.1 |

[원문 미확인]

> **이 표에서 지금 가져갈 것은 하나다** — 여섯 줄이 모두 같은 꼴이라는 것. 1줄은 3절에서 직접 해 본다. 나머지 다섯 줄은 **읽고 지나가면 된다**.

3. **조건 표** `[외부 추론]`

| 줄 | 가능한 행렬 종류 | 비고 |
|---|---|---|
| $A = CR$ | 모든 형태의 행렬 |  |
| $A = U\Sigma V^{\mathrm T}$ | 모든 형태의 행렬 |  |
| $A = QR$ | 직사각 행렬도 가능 |  |
| $A = LU$ | 행 교환이 필요한 경우가 있음 (예: $\begin{bmatrix}0&1\\1&0\end{bmatrix}$) |  |
| $S = Q\Lambda Q^{\mathrm T}$ | 대칭 행렬만 |  |
| $A = X\Lambda X^{-1}$ | 정사각·독립 고유벡터가 열 수만큼 (반례: $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$은 실수 고유벡터가 없음) |  |

4. **소절 「첫 줄 / 앞 절반 / 뒤 절반」**

- **첫 줄**: $C$와 $R$의 곱이라는 설명.  
  > (번역) “첫 줄은 C 행렬(열)과 R 행렬(행)의 곱이다.”  
  > (원문) “And the first line, which I think … of a C matrix, a column matrix, and a row matrix R.” `[Vision 00 01:47]`

- **다음 다섯 줄**: 핵심 장들의 이름표.  
  > (번역) “다음은 다섯 개의 유명한 핵심 약어이다: LU, QR, S, X, UΣVᵀ.”  
  > (원문) “Then these are five famous essential shorthand descriptions of the key chapters of linear algebra, the key chapters.” `[Vision 00 02:08]`

- **$LU$**: 소거와 첫 번째 일.  
  > (번역) “LU는 소거와 방정식 풀이를 위한 문자이다.”  
  > (원문) “And computer commands would be exactly those letters LU for elimination for solving equations, the first job of linear algebra.” `[Vision 00 02:25]`

- **앞 절반**: 방정식 풀기에 관한 이야기.  
  > (번역) “첫 절반은 QR을 끝으로 방정식 풀이에 관한 것이다.”  
  > (원문) “the first half, ending with there, with QR, is about solving equations.” `[Vision 00 03:02]`

- **뒤 절반**: 고유값·고유벡터·특이값에 관한 이야기.  
  > (번역) “두 번째 절반은 고유값·고유벡터·특이값에 관한 것이다.”  
  > (원문) “The second half, these three are about eigenvalues and eigenvectors and singular values, a different way to approach the whole subject and a very, very important way.” `[Vision 00 03:11]`

- **특이값**: 이론의 꼭대기, 두세 조각으로 쪼개기.  
  > (번역) “특이값은 이론의 꼭대기이며, 모든 행렬을 두세 조각으로 쪼갤 수 있다.”  
  > (원문) “That's the high point of the theory.” `[Vision 00 03:36]`

| 구분 | 무슨 이야기 | 우리의 층 |
|---|---|---|
| 앞 절반 (줄 1·2·3) | $A = CR$, $A = LU$, $A = QR$ — 기본 조각(열, 삼각, 직교) | 1줄만 익히는 층 (기본 조각) |
| 뒤 절반 (줄 4·5·6) | $S = Q\Lambda Q^{\mathrm T}$, $A = X\Lambda X^{-1}$, $A = U\Sigma V^{\mathrm T}$ — 고유값·고유벡터·특이값 | 나머지 지도 층 (고급 조각) |

선형대수의 핵심 장 하나하나가 행렬을 몇 조각의 곱으로 쪼개는 한 가지 방법이고, 조각마다 성질이 다르다.

## 3. "행렬을 조각의 곱으로 쓴다"는 게 무슨 말인가 `[외부 추론]`

첫 줄에 “스트랭은 이 영상에서 숫자 예를 들지 않는다(01에서 든다). 기준 행렬 $A_2$로 맛만 본다”라고 적는다.

### 3.1 열을 하나씩 잘라서 본다
$$
A_2 = \begin{bmatrix}
1 & 2 & 3 \\
2 & 4 & 6
\end{bmatrix}
$$
각 열을 세로 벡터로 적는다.
$$
\mathbf{c}_1 = \begin{bmatrix}1\\2\end{bmatrix},\quad
\mathbf{c}_2 = \begin{bmatrix}2\\4\end{bmatrix},\quad
\mathbf{c}_3 = \begin{bmatrix}3\\6\end{bmatrix}
$$
| 열 | 표현 | 배수 | 비고 |
|---|---|---|---|
| 1 | $(1,2)$ | $=1\times(1,2)$ | 1배 |
| 2 | $(2,4)$ | $=2\times(1,2)$ | 2배 |
| 3 | $(3,6)$ | $=3\times(1,2)$ | 3배 |
> 세 열이 모두 **같은 재료 $(1,2)$의 몇 배**다.

### 3.2 재료와 만드는 법
재료 열 $\mathbf{c}=\begin{bmatrix}1\\2\end{bmatrix}$를 $C$라 하고, 배수 행렬 $R=\begin{bmatrix}1&2&3\end{bmatrix}$라 하면
$$
A_2 = C\,R
\underbrace{= \begin{bmatrix}1\\2\end{bmatrix}\begin{bmatrix}1&2&3\end{bmatrix}}_{\text{재료와 배수}}
$$
<!-- 검산: M([[1],[2]]) * M([[1,2,3]]) == M([[1,2,3],[2,4,6]]) -->
$C\times R$은 “재료를 1배, 2배, 3배 해서 왼쪽부터 나란히 세워라”로 읽는다.  
**스스로 확인하는 법**: $C\times R$을 직접 계산해 원래 행렬이 나오는지 확인한다.

### 3.3 "한 방향"이라는 말
벡터 $\mathbf{c}=(1,2)$를 원점에서 화살표로 그리면, $\mathbf{c}_2=(2,4)$·$\mathbf{c}_3=(3,6)$은 같은 직선 위에 늘어선다. 따라서 **열이 한 방향뿐**이다. 대비로 $A_4=\begin{bmatrix}1&3\\3&1\end{bmatrix}$의 두 열은 서로 다른 직선 위에 있어 같은 재료 하나로는 만들 수 없다 (3절 끝 (다)에서 확인).

### 3.4 빠지기 쉬운 곳
$R$을 찾을 때는 **전체 열**을 재료 열 전체와 비교한다. 열 하나 안에서 위·아래를 비교하면 (아래가 위의 2배) 다른 숫자가 나오지만, 이는 다른 질문(3.5)의 답이다.

### 3.5 같은 식을 행으로 읽으면
행을 세로 벡터로 적는다.
$$
\mathbf{r}_1 = \begin{bmatrix}1&2&3\end{bmatrix},\quad
\mathbf{r}_2 = \begin{bmatrix}2&4&6\end{bmatrix}
$$
| 행 | 표현 | 배수 | 비고 |
|---|---|---|---|
| 1 | $(1,2,3)$ | $=1\times(1,2,3)$ | $R$의 1배 |
| 2 | $(2,4,6)$ | $=2\times(1,2,3)$ | $R$의 2배 |
> **표** — 열로 읽기 / 행으로 읽기 | 뜻 | 몇 배인지는 누가 알려 주나($R$ / $C$) |
> --- | --- | --- |
> 열로 읽기 | $C$가 재료 | $R$가 배수 |
> 행으로 읽기 | $R$가 재료 | $C$가 배수 |

### 3.6 같은 것은 개수다
열은 3개지만 재료 열은 1개, 행은 2개지만 재료 행은 1개이다. **같은 것은 재료의 개수**이며, 이 개수를 **rank**라 부른다. $A_2$의 rank는 1, $A_4$의 rank는 2이다.

> **여기까지 확인된 것과 아닌 것**  
> - 열 하나×행 하나 꼴에서는 식의 꼴에서 바로 나온다.  
> - 재료가 둘·셋일 때도 열 쪽 수 = 행 쪽 수인지는 아직 안 보였다(01·06·09에서).  
> - 위 계산은 예 하나일 뿐 “모든 행렬이 $CR$로 쪼개진다”는 증명이 아니다.

<details><summary>곁가지 — 지금은 건너뛰어도 된다</summary>
재료 열이 $r$개면 $C$는 열 $r$개, $R$은 행 $r$개가 된다. 숫자 개수가 6에서 5로 줄었지만 “정보 5개”는 아니다(앞 조각 2배, 뒤 조각 반으로 해도 같은 행렬).
</details>

#### 가리고 해 보기
- (가) 빈칸 계산  
  $$\begin{bmatrix}1\\3\end{bmatrix}\begin{bmatrix}2&4\end{bmatrix} = ?$$  
  **예측**: 두 번째 열은 첫 번째 열의 몇 배일까?  

- (나) 거꾸로  
  $$\begin{bmatrix}2&6\\1&3\end{bmatrix}$$  
  **질문**: 이것을 열 하나×행 하나로 나타낼 수 있는가?  

- (다) 반례  
  $A_4=\begin{bmatrix}1&3\\3&1\end{bmatrix}$도 열 하나×행 하나로 되나? 안 된다면 이유는?  

<details><summary>맞춰 보기 (먼저 해 본 뒤에 연다)</summary>
- (가) 답: $\begin{bmatrix}1\\3\end{bmatrix}\begin{bmatrix}2&4\end{bmatrix} = \begin{bmatrix}2&4\\6&12\end{bmatrix}$  
  <!-- 검산: M([[1],[3]]) * M([[2,4]]) == M([[2,4],[6,12]]) -->
- (나) 답: 가능. 예: $\begin{bmatrix}2\\1\end{bmatrix}\begin{bmatrix}1&3\end{bmatrix} = \begin{bmatrix}2&6\\1&3\end{bmatrix}$  
  <!-- 검산: M([[2],[1]]) * M([[1,3]]) == M([[2,6],[1,3]]) -->  
  하지만 $C$는 원래 행렬의 열에서 골라야 하므로 이 경우는 $CR$는 아니다.  
- (다) 답: 안 된다. $A_4$는 두 열이 서로 다른 방향을 가지므로 하나의 재료 열로는 만들 수 없다.  
  <!-- 검산: 없음 (논리적 설명) -->
</details>

## 4. 시각별 흐름

| 시각 구간 | 내용 |
|---|---|
| 00:13–00:45 | 스트랭이 자신을 소개하고 18.06 영상을 새로 고쳐 말하려는 이유를 제시한다. |
| 00:45–00:59 | 선형대수가 점점 더 필수·중요·아름다워졌다는 점을 강조한다. |
| 00:59–01:10 | 새로운 시작점을 제시하고 곧 보여줄 것이라고 말한다. |
| 01:10–01:42 | “슬라이드는 전체 강좌를 알려준다”는 말을 하며 슬라이드가 전체 강좌 개요임을 알린다. |
| 01:42–02:08 | 슬라이드에 여섯 줄을 띄우고 첫 줄이 $C$와 $R$의 곱이라는 설명을 한다. |
| 02:08–03:02 | 다섯 개의 유명한 핵심 약어(LU, QR, $S$, $X$, $U\Sigma V^{\mathrm T}$)를 소개하고, QR이 방정식 풀이와 연결됨을 말한다. |
| 03:02–04:08 | 고유값·고유벡터·특이값에 대한 설명, 이론의 꼭대기, 그리고 실제 18.06 영상을 보라는 당부로 마무리한다. |

여기서 쓰고 있다고 한 책은 6판이 아니라 *Linear Algebra for Everyone* `[Vision 00 01:23]`.

## 5. 말과 기호

| 영어 | 우리말 | 영상에서의 자리 |
|---|---|---|
| column | 열 | $A = CR$에서 $C$의 열 |
| row | 행 | $A = CR$에서 $R$의 행 |
| independent columns | 독립적인 열 | $A = CR$에서 $C$의 성질 |
| elimination | 소거 | $LU$에서 행렬 소거를 의미 |
| triangular matrix | 삼각 행렬 | $LU$에서 $L$과 $U$가 삼각 행렬 |
| orthogonal / perpendicular | 직교(수직) | “There is the word orthogonal or perpendicular.” `[Vision 00 02:46]` |
| symmetric matrix | 대칭 행렬 | $S = Q\Lambda Q^{\mathrm T}$에서 사용 |
| eigenvalue / eigenvector | 고유값·고유벡터 | $A = X\Lambda X^{-1}$에서 등장 |
| singular value | 특이값 | $A = U\Sigma V^{\mathrm T}$에서 등장 |
| factorization | (영상에서는 “두세 조각으로 행렬을 쪼개는”이라고 말한다) | 직접적인 용어는 사용되지 않음 |

## 6. 어디에 쓰이나 — 짧게 `[외부 추론]`

- **어디에**: 행렬은 흔히 자료를 정리한 형태로 쓰인다. 행은 사람·가구 같은 관측값을, 열은 변수(키, 몸무게 등)를 나타낸다. `[외부 추론]`

- **무엇을 설명하는가**: $A_2=\begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}$에서 둘째 행은 첫째 행의 2배이다. 따라서 두 행이 같은 방향을 가리키므로 새로운 정보를 제공하지 않는다. `[외부 추론]`

- **여기까지는 말해 주지 않는다**: 독립적인 방향의 수가 원인(원인 변수)의 수와 같다고 할 수 없으며, 실제 자료는 잡음이 있어 정확히 몇 배인지는 거의 알 수 없다. 이런 이유로 나중에 특이값 분해가 필요해진다. `[외부 추론]`

**수학적 의미를 가지고 현실에 정답처럼 적용하면 안 된다.**

## 7. 본 뒤에 — 말로 설명해 보기

1. 스트랭이 영상을 새로 고쳐 말하는 이유 두 가지는 무엇인가?  
2. 여섯 줄에 공통된 꼴과 조각들이 다른 점은 무엇인가?  
3. 앞 절반·뒤 절반은 무엇에 관한 이야기이고 $CR$은 어디 속하며 왜 따로 강조되는가?  
4. $\begin{bmatrix}1\\2\end{bmatrix}\begin{bmatrix}1&2&3\end{bmatrix}$을 계산하지 않고도 결과의 행들이 어떤 관계일지 말할 수 있나?

**이해 단계 적어 두기** — 설명을 따라갈 수 있다 / 빈 종이에 다시 쓸 수 있다 / 처음 보는 짧은 문제에 쓸 수 있다  

**남은 질문**: (여기에 적는다)
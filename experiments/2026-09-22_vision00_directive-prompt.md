---
type: experiment-prompt
date: 2026-09-22
purpose: 2차 — 1차(규칙 묶음 + 자료)에서 gpt-oss-120b(Antigravity, medium 고정)가 노트를 설계하지 못했다. 이번엔 절 뼈대와 할 일을 순서대로 다 적어 주고 "시키면 하는가"를 본다
prior: 2026-09-22_gpt-oss-120b_vision00_prompt.md (1차) · 00-intro.md (1차 결과, 87줄)
result_to: docs/experiments/00-intro-directive.md
---

# 사용법

`=====` 사이를 통째로 복사해 Antigravity 채팅(GPT-OSS 120B)에 붙여넣는다. 결과는 `docs/experiments/00-intro-directive.md`에 원문 그대로 저장한다.

=====

아래 「자료」만 써서 한국어 Markdown 노트 한 파일을 쓴다. **「절 뼈대」의 순서와 항목을 그대로 따른다.** 항목을 빼거나 순서를 바꾸지 않는다. 각 항목의 지시를 하나씩 실행한 결과가 곧 노트다.

## 공통 규칙 (짧게)

- 독자: 한국어 화자, 영어가 편하지 않음, 선형대수는 처음. 행렬 곱셈도 처음 만나는 것처럼 쓴다. 중학생 눈높이, 그러나 수학은 빼지 않는다.
- 스트랭 인용은 **번역 먼저, 원문 아래**. 원문은 자막에서 글자 그대로. 원문 바로 뒤 같은 줄에 좌표 `[Vision 00 mm:ss]` — 그 말이 시작되는 큐의 시각. 한 문장이 여러 큐에 걸치면 이어 붙이고 첫 큐 시각을 쓴다. 형식:
  ```
  > (번역) …
  >
  > (원문) "…" `[Vision 00 01:47]`
  ```
- 스트랭이 말하지 않은, 당신이 덧붙인 설명에는 `[외부 추론]`을 단다.
- 자료에 없는 것은 지어내지 않는다. 시각·쪽수·절 번호는 자료에 있는 것만 쓴다.
- 행렬 계산을 적은 곳마다 바로 아래 줄에 검산 주석: `<!-- 검산: M([[1],[2]]) * M([[1,2,3]]) == M([[1,2,3],[2,4,6]]) -->` (`M(행 리스트)` = 행렬, `F(1,2)` = 1/2, 스칼라배 `-2 * M(...)`).
- 수식은 `$...$` / `$$...$$`. 출력은 파일 내용만 — 머리말·후기 없이.

## 절 뼈대 — 이 순서로, 이 항목을 전부

### 0. frontmatter

`type: note` · `scope: "Vision 00 「Intro: A New Way to Start Linear Algebra」 (2020, 4분 09초) — 영상 전체"` · `layer: 지도 층 (예고편)` · `sources:` 에 자막·슬라이드 2/30·책 목차 셋을 적는다.

### 제목과 맨 위 상자

- 제목: `# Vision 00 — 예고편: 선형대수를 새로 시작하는 법`
- 인용 상자(`>`)로 두 덩이:
  - **지금 할 수 있어야 하는 것** 3개: ① 이 영상 묶음이 무엇인지 한두 문장으로 말한다 ② "행렬을 조각의 곱으로 쓴다"가 무슨 뜻인지 작은 행렬 하나로 보여 준다 (→ 3절) ③ 슬라이드 여섯 줄이 첫 줄 / 앞 절반 / 뒤 절반으로 어떻게 나뉘는지 말한다 (→ 2절)
  - **나중에 돌아올 것**: LU · QR · $Q\Lambda Q^{\mathrm T}$ · $X\Lambda X^{-1}$ · $U\Sigma V^{\mathrm T}$가 각각 무엇인지 — 하나하나가 책의 한 장. 지금 몰라도 된다.

### 「읽는 법」 표

행 4개: `[Vision 00 01:47]`의 뜻 · `슬라이드 2/30`의 뜻 · `Strang ILA §3.2`의 뜻 · `[외부 추론]`의 뜻("출처를 가르는 표시일 뿐, 맞다는 보증은 아니다"까지) · 인용 형식(번역 먼저 원문 아래).

### 1. 이 영상은 무엇인가

1. 스트랭이 18.06 강의 영상을 새로 고쳐 말하러 왔다는 것을 한 문단으로. 고치는 이유 두 가지를 자막에서 찾아 각각 인용한다: (a) 그 사이 선형대수가 더 중요해졌다 — `[00:45]` 큐부터 (b) 새 출발점 — `[00:59]` 큐.
2. "슬라이드가 강좌 전체를 말해 준다"는 말을 인용한다 — `[01:10]`부터 두 큐.
3. 끝의 당부 "진짜 18.06 영상으로 가라"를 인용한다 — `[04:00]`. 이 말이 "영상 단계 = 지도 그리기"의 근거임을 한 줄로.

### 2. 슬라이드 한 장 — 여섯 줄

1. 스트랭이 `[01:42]`에 슬라이드를 띄우고 개요라고 한다는 것을 한 줄로. **여섯 줄이 모두 같은 꼴**(왼쪽 행렬 하나 = 오른쪽 둘 또는 셋의 곱)임을 말한다.
2. **표** — 열 5개: 줄 번호 | 식 | 슬라이드에 적힌 설명 (원문) | 쉬운 말 `[외부 추론]` | 어느 영상 · 책 어디. 여섯 줄 전부. "쉬운 말"은 각 조각의 성질을 한두 문장으로 (독립인 열 / 삼각 / 수직 / 대칭·고유벡터 / 정사각·고유벡터 / 어떤 모양에도). 책 절은 「자료 5.3」 제목으로 맞추고, 절 본문은 못 봤으니 표 아래에 `[원문 미확인]` 한 줄.
3. 표 바로 아래 인용 상자: "이 표에서 지금 가져갈 것은 하나다 — 여섯 줄이 모두 같은 꼴이라는 것. 1줄은 3절에서 직접 해 본다. 나머지 다섯 줄은 **읽고 지나가면 된다**."
4. **조건 표** `[외부 추론]` — 어느 줄이 어떤 행렬에 되나: $CR$·$U\Sigma V^{\mathrm T}$ = 모든 모양 / $QR$ = 직사각도 됨 / $LU$ = 행 바꿈이 필요한 행렬이 있음(예 하나: $\begin{bmatrix}0&1\\1&0\end{bmatrix}$이 그대로는 안 되는 이유 두세 줄) / $Q\Lambda Q^{\mathrm T}$ = 대칭행렬만 / $X\Lambda X^{-1}$ = 정사각 + 독립인 고유벡터가 열 수만큼(반례: 90° 회전 $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$은 실수 고유벡터가 없다).
5. **소절 「첫 줄 / 앞 절반 / 뒤 절반」**: 자막에서 다음을 각각 인용한다 — 첫 줄이 $C$(열)와 $R$(행)의 곱 `[01:47]` · 나머지 다섯 줄은 핵심 장들의 이름표 `[02:08]` · $LU$ = 소거, 첫 번째 일 `[02:25]` · 앞 절반은 방정식 풀기, 뒤 절반은 고유값·고유벡터·특이값 `[03:02]` · 특이값이 이론의 꼭대기, 모두 "두세 조각으로 쪼개기" `[03:36]`. 그런 다음 **표** — 앞 절반(1·2·3줄) / 뒤 절반(4·5·6줄) | 무슨 이야기 | 우리의 층(1줄만 익히는 층, 나머지 지도 층). 마지막에 "선형대수의 핵심 장 하나하나가 행렬을 몇 조각의 곱으로 쪼개는 한 가지 방법이고, 조각마다 성질이 다르다"를 이 4분의 핵심으로 못 박는다.

### 3. "행렬을 조각의 곱으로 쓴다"는 게 무슨 말인가 `[외부 추론]`

첫 줄에 "스트랭은 이 영상에서 숫자 예를 들지 않는다(01에서 든다). 기준 행렬 $A_2$로 맛만 본다"를 쓴다. 그리고 소절 여섯 개를 **이 순서로**:

- **3.1 열을 하나씩 잘라서 본다.** $A_2 = \begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}$를 display로 쓰고, 열1·열2·열3을 각각 세로 벡터로 따로 쓴다. 그 다음 **표** 세 행: `열1 = (1,2) | = 1 × (1,2) | 1배`, `열2 = (2,4) | = 2 × (1,2) | 2배`, `열3 = (3,6) | = 3 × (1,2) | 3배`. 결론 한 줄: 세 열이 모두 **같은 재료 $(1,2)$의 몇 배**다.
- **3.2 재료와 만드는 법.** 재료 열 $(1,2)$가 $C$, "1배·2배·3배"를 가로로 적은 $[1\ 2\ 3]$이 $R$. $A_2 = C\,R$을 display로 `\underbrace`를 써서 세 덩이에 이름을 붙인다. 검산 주석. "$C\times R$은 '재료를 1배, 2배, 3배 해서 왼쪽부터 나란히 세워라'로 읽는다"를 쓴다. **스스로 확인하는 법**: $C\times R$을 직접 계산해 원래 행렬이 나오는지 보면 된다.
- **3.3 "한 방향"이라는 말.** $(1,2)$를 원점에서의 화살표로 설명하고, $(2,4)$·$(3,6)$은 같은 화살표를 늘인 것 → 세 화살표가 같은 직선 위 → "열이 한 방향뿐". 대비로 $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$의 두 열은 다른 직선 위 — 재료 하나로는 못 만든다(3절 끝 (다)에서 확인).
- **3.4 빠지기 쉬운 곳.** $R$을 찾을 때는 **열 전체**를 재료 열 전체와 견준다. 열 하나 **안에서** 위·아래를 견주면(아래가 늘 위의 2배) 다른 숫자가 나오는데, 그것은 틀린 관찰이 아니라 다른 질문(3.5)의 답이다.
- **3.5 같은 식을 행으로 읽으면.** $A_2$를 행으로 잘라 **표** 두 행: `행1 = (1,2,3) | = 1 × (1,2,3) | R의 1배`, `행2 = (2,4,6) | = 2 × (1,2,3) | R의 2배`. 배수 1, 2를 세로로 적으면 $C$가 다시 나온다. **표** — 열로 읽기 / 행으로 읽기 | 뜻 | 몇 배인지는 누가 알려 주나($R$ / $C$).
- **3.6 같은 것은 개수다.** 열은 셋이지만 재료 열은 하나, 행은 둘이지만 재료 행은 하나, 개수가 똑같이 1. **"$C$와 $R$이 같다는 말이 아니다"** — 같은 것은 재료의 개수. 이 개수의 이름이 **rank**(여기서 처음 이름을 준다). $A_2$의 rank 1, $A_4$의 rank 2. 그 다음 인용 상자 「여기까지 확인된 것과 아닌 것」: 열 하나×행 하나 꼴에서는 식의 꼴에서 바로 나온다 / 재료가 둘·셋일 때도 열 쪽 수 = 행 쪽 수인지는 아직 안 보였다(01·06·09에서) / 위 계산은 예 하나이지 "모든 행렬이 $CR$로 쪼개진다"의 증명이 아니다.
- `<details><summary>곁가지 — 지금은 건너뛰어도 된다</summary>`: 재료 열이 $r$개면 $C$는 열 $r$개, $R$은 행 $r$개 · 숫자 개수가 6에서 5로 줄었지만 "정보 5개"는 아니다(앞 조각 2배, 뒤 조각 반으로 해도 같은 행렬).
- **「가리고 해 보기」**: (가) 빈칸 계산 — $\begin{bmatrix}1\\3\end{bmatrix}\begin{bmatrix}2&4\end{bmatrix}=?$ 계산 **전에** "둘째 열은 첫째 열의 몇 배일까"를 예측하게 한다 / (나) 거꾸로 — $\begin{bmatrix}2&6\\1&3\end{bmatrix}$을 열 하나×행 하나로 / (다) 반례 — $A_4$도 열 하나×행 하나로 되나? 안 되면 한 문장으로 왜. 답은 `<details><summary>맞춰 보기 (먼저 해 본 뒤에 연다)</summary>` 안에, 각 답에 검산 주석. (나)의 답에는 "답이 하나가 아니다($\begin{bmatrix}1\\1/2\end{bmatrix}\begin{bmatrix}2&6\end{bmatrix}$도 됨) — 다만 $CR$의 $C$는 원래 행렬의 열에서 고른 것이어야 하므로 그쪽은 $CR$은 아니다"를 넣는다.

### 4. 시각별 흐름

**표** — 시각 구간 | 내용. 자막의 큐 시각만 써서 6–7행. 구간 경계는 자막에 있는 시각이어야 한다. 마지막에 한 줄: 여기서 쓰고 있다고 한 책은 6판이 아니라 *Linear Algebra for Everyone* `[01:23]`.

### 5. 말과 기호

**표** — 영어 | 우리말 | 이 영상에서의 자리. 최소 이 9개: column/row · independent columns · elimination · triangular matrix · orthogonal/perpendicular(스트랭의 말 `[02:46]` 인용) · symmetric matrix · eigenvalue/eigenvector · singular value · factorization(이 영상에서는 이 낱말을 안 쓰고 "breaking a matrix into two or three pieces"라고 한다).

### 6. 어디에 쓰이나 — 짧게 `[외부 추론]`

세 항목을 **각각 한 문단**: **어디에**(숫자 자료를 표로 적으면 행렬 — 행이 사람·가구, 열이 변수) / **방금 본 수학이 설명하는 것**($A_2$에서 둘째 행이 첫째 행의 2배 = 새 방향을 보태지 않는다) / **여기까지는 말해 주지 않는다**(독립인 방향의 수 ≠ 현실의 원인 수 · 몇 배인 행도 관측으로는 필요 · 실제 자료는 잡음이 있어 "정확히 몇 배"가 거의 없다 → 나중에 특이값이 필요해진다). 마지막 한 줄: **"수학적 의미를 가지고 현실에 정답처럼 적용하면 안 된다."**

### 7. 본 뒤에 — 말로 설명해 보기

물음 4개: ① 스트랭이 영상을 새로 고쳐 말하는 이유 둘 ② 여섯 줄에 공통된 꼴과 조각들이 다른 점 ③ 앞 절반·뒤 절반은 무엇에 관한 이야기이고 $CR$은 어디 속하며 왜 따로 강조되나 ④ $\begin{bmatrix}1\\2\end{bmatrix}\begin{bmatrix}1&2&3\end{bmatrix}$을 계산하지 않고도 결과의 행들이 어떤 관계일지 말할 수 있나. 그 아래 "**이해 단계 적어 두기** — 설명을 따라갈 수 있다 / 빈 종이에 다시 쓸 수 있다 / 처음 보는 짧은 문제에 쓸 수 있다" 와 "**남은 질문**: (여기에 적는다)".

## 자료

### 자막 전문 (큐 단위, `[mm:ss]` = 큐 시작 시각)

```
[00:13] GILBERT STRANG: Well, I'm Gil Strang.
[00:15] And I'm very happy if you know the linear algebra
[00:20] videos on OpenCourseWare or on YouTube.
[00:24] That's for the math course 18.06.
[00:28] And I'm even happier if you like them.
[00:32] And I'm here today to update them for several reasons.
[00:38] Well, a lots happened in linear algebra in these years.
[00:45] Fortunately, the whole subject has just
[00:48] become more and more essential, more and more important, more
[00:51] and more beautiful.
[00:53] And so I wanted to say something about those later steps.
[00:59] And also, when I teach it now, I have a new starting point.
[01:05] And I'll show you that.
[01:06] So I'll go a little slowly on that starting point.
[01:10] The slides tell you the whole course.
[01:12] And that's crazy to have a full course within a short video.
[01:18] But especially the first part is new.
[01:23] And I'm even writing a textbook called
[01:27] Linear Algebra for Everyone that will start this way.
[01:31] I hope that the new start brings in real linear algebra ideas
[01:39] right away.
[01:41] And let me show you where those are.
[01:42] So this is an outline of the whole video.
[01:47] And the first line, which I think
[01:51] about in my mind as matrix A, is a product
[01:55] of a C matrix, a column matrix, and a row matrix R.
[02:00] And you'll see what those are.
[02:02] So that's the new idea.
[02:06] That will come first.
[02:08] Then these are five famous essential shorthand
[02:15] descriptions of the key chapters of linear algebra,
[02:19] the key chapters.
[02:20] So they represent, for example, LU is those letters are famous.
[02:25] And computer commands would be exactly
[02:28] those letters LU for elimination for solving equations,
[02:34] the first job of linear algebra.
[02:36] And then QR.
[02:39] So Q is a very interesting important type of matrix.
[02:43] That's standing for an orthogonal matrix.
[02:46] There is the word orthogonal or perpendicular.
[02:50] So those are the best matrices to compute with.
[02:54] And that QR gets us there.
[02:58] And S is for a symmetric matrix.
[03:00] And it will involve--
[03:02] oh, well, I should say, the first half,
[03:04] ending with there, with QR, is about solving equations.
[03:11] The second half, these three are about eigenvalues
[03:16] and eigenvectors and singular values,
[03:18] a different way to approach the whole subject and a very, very
[03:23] important way.
[03:24] Among my goals is to help courses around the world
[03:30] get singular values included because you really
[03:34] don't want to miss them.
[03:36] That's the high point of the theory.
[03:39] And it's expressed like all the others
[03:42] as breaking a matrix into two or three pieces, two
[03:48] or three parts.
[03:49] So that's my plan for this video.
[03:54] And I hope it's helpful.
[03:56] Again, it's a whole course in a short time.
[04:00] And please go to the real 18.06 videos for the details.
[04:08] Thanks
```

### 슬라이드 2/30 (영상 01:42에 띄움) — 적힌 내용 그대로

| 줄 | 식 | 설명 (원문) |
|---|---|---|
| 1 | $A = CR$ | Independent columns in $C$ |
| 2 | $A = LU$ | Triangular matrices $L$ and $U$ |
| 3 | $A = QR$ | Orthogonal columns in $Q$ |
| 4 | $S = Q\Lambda Q^{\mathrm T}$, $Q^{\mathrm T} = Q^{-1}$ | Orthogonal eigenvectors $Sq = \lambda q$ |
| 5 | $A = X\Lambda X^{-1}$ | Eigenvalues in $\Lambda$ · Eigenvectors in $X$ · $Ax = \lambda x$ |
| 6 | $A = U\Sigma V^{\mathrm T}$ | Diagonal $\Sigma$ = Singular values $\sigma = \sqrt{\lambda(A^{\mathrm T}A)}$ · Orthogonal vectors in $U^{\mathrm T}U = V^{\mathrm T}V = I$ · $Av = \sigma u$ |

### 책 목차 — Strang, *Introduction to Linear Algebra* 6판 (2023)

§1.4 Matrix Multiplication $AB$ and $CR$ · §2.3 Matrix Computations and $A = LU$ · §3.2 Computing the Nullspace by Elimination: $A = CR$ · §4.4 Orthonormal Bases and Gram-Schmidt · §6.2 Diagonalizing a Matrix · §6.3 Symmetric Positive Definite Matrices · §7.1 Singular Values and Singular Vectors

### 기준 행렬

$A_2 = \begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}$ (재료 하나) · $A_4 = \begin{bmatrix}1&3\\3&1\end{bmatrix}$ (정사각·대칭·가역, 고유값 4·−2, 고유벡터 $(1,1)$·$(1,-1)$)

### 다른 영상 (자리만 가리킬 때)

01 Column Space · 02 Big Picture(네 부분공간·LU) · 03 Orthogonal Vectors(QR) · 04 Eigenvalues · 05 Singular Values · 06 Nullspace by Elimination · 07 Five Factorizations · 08 Four Subspaces & Least Squares · 09 Elimination and $A=CR$

=====

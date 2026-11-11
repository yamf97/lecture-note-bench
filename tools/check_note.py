#!/usr/bin/env python3
"""노트의 기계 검사 — 커밋 전에 돌린다 .

    python3 tools/check_note.py <노트.md> [<노트.md> …]

검사하는 것
  1. 자막 인용  "…" `[Vision NN mm:ss]`   (좌표가 앞에 오는 꼴 `[…]` "…" 도 읽는다. 같은 줄이어야 한다)
       - 따옴표 안의 글이 그 영상 vtt에 **글자 그대로** 이어져 있는가 (공백만 정규화)
       - 가운데를 … (또는 ...)로 줄인 인용은 조각마다, 순서대로 있는지 본다
       - 적힌 시각이 그 말이 **시작되는 큐**의 시작 시각과 같은가
  2. 좌표만 있는 것  `[Vision NN mm:ss]`
       - 그 시각에 시작하는 큐가 있는가
  3. 검산식  <!-- 검산: 식 == 식 -->
       - 분수(Fraction)로 계산해 성립하는가. 행렬은 M([[1,2],[3,4]]), 분수는 F(1,2)
         쓸 수 있는 것: + - * (행렬곱·스칼라배), .T (전치), ==

  4. frontmatter 문법 — 따옴표 없는 값 안에 "콜론+공백"이나 " #"이 있으면 YAML이 깨진다
       (2026-09-20: `scope: … 「Intro: A New …」` 가 에디터에서 "Nested mappings" 오류). 값을 "…"로 감쌀 것

파일 frontmatter에 `coords: block30` 이 있으면(Study에서 온 대응표처럼 30초로 묶어 읽은 문서)
시각은 "그 말이 시작되는 큐가 들어 있는 30초 구간의 시작"과 비교한다.

``` 로 둘러싼 코드 블록 안은 검사하지 않는다 (보낸 질문문의 기록처럼 고치면 안 되는 원문).

검사하지 **못하는** 것: 책 인용(스캔본이라 텍스트 층이 깨짐 — 쪽 이미지로 사람이/Claude가 대조),
번역이 맞는가, 설명이 개념적으로 옳은가. 그것은 커밋 후 모델 검토와 사용자의 몫이다.

실패가 하나라도 있으면 종료 코드 1.
"""
import csv
import os
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtt_text import parse, mmss  # noqa: E402

# 자막 폴더 위치. 기본은 이 저장소의 lectures/ — 환경변수 LECTURES_DIR 로 바꿀 수 있다.
LECTURES_DIR = os.environ.get(
    "LECTURES_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lectures")
)
LECTURES = {
    "Vision": os.path.join(LECTURES_DIR, "Strang_2020_vision_LA"),
}

COORD = r"\[(?P<key>[A-Za-z0-9.]+) (?P<no>\d{2}) (?P<t>\d{2}:\d{2})\]"
QUOTE = re.compile(r"\"(?P<q>[^\"\n]+)\"[ \t]*`" + COORD + r"`")
PRE = re.compile(r"`" + COORD + r"`[ \t]*\"(?P<q>[^\"\n]+)\"")
FENCE = re.compile(r"^(`{3,})[^\n]*\n.*?^\1[ \t]*$", re.S | re.M)
BARE = re.compile(r"`" + COORD + r"`")
CHECK = re.compile(r"<!--\s*검산:\s*(?P<expr>.+?)\s*-->", re.S)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


class M:
    """분수 행렬. 검산식 전용."""

    def __init__(self, rows):
        self.r = [[Fraction(x) for x in row] for row in rows]
        if len({len(row) for row in self.r}) != 1:
            raise ValueError("행마다 길이가 다르다")

    @property
    def shape(self):
        return len(self.r), len(self.r[0])

    @property
    def T(self):
        return M([list(c) for c in zip(*self.r)])

    def __eq__(self, o):
        return isinstance(o, M) and self.r == o.r

    def __add__(self, o):
        return M([[a + b for a, b in zip(x, y)] for x, y in zip(self.r, o.r)])

    def __sub__(self, o):
        return M([[a - b for a, b in zip(x, y)] for x, y in zip(self.r, o.r)])

    def __mul__(self, o):
        if isinstance(o, M):
            if self.shape[1] != o.shape[0]:
                raise ValueError(f"크기가 안 맞는 곱 {self.shape}×{o.shape}")
            cols = list(zip(*o.r))
            return M([[sum(a * b for a, b in zip(row, col)) for col in cols] for row in self.r])
        return M([[a * Fraction(o) for a in row] for row in self.r])

    def __rmul__(self, k):
        return self * k

    def __neg__(self):
        return self * -1

    def __repr__(self):
        return "[" + "; ".join(" ".join(str(a) for a in row) for row in self.r) + "]"


_cache = {}


def cues_for(key, no):
    if (key, no) in _cache:
        return _cache[(key, no)]
    root = LECTURES.get(key)
    if not root:
        raise KeyError(f"모르는 강좌 키 {key!r} — tools/check_note.py 의 LECTURES 에 등록할 것")
    root, index = root if isinstance(root, tuple) else (root, "index.tsv")
    with open(os.path.join(root, index), encoding="utf-8") as f:
        rows = {r["no"]: r for r in csv.DictReader(f, delimiter="\t")}
    if no not in rows:
        raise KeyError(f"{key} {index} 에 {no}번이 없다")
    cues = parse(os.path.join(root, rows[no]["caption"]))
    _cache[(key, no)] = cues
    return cues


def block_of(sec, block):
    return mmss(int(sec) // block * block)


def check_quote(q, key, no, t, block=0):
    cues = cues_for(key, no)
    joined, starts = "", []
    for s, _, text in cues:
        if joined:
            joined += " "
        starts.append((len(joined), s))
        joined += norm(text)
    parts = [norm(x) for x in re.split(r"\s*(?:…|\.{3})\s*", q) if norm(x)]
    pos, cur = -1, 0
    for i, part in enumerate(parts):
        at = joined.find(part, cur)
        if at < 0:
            return f"자막에 그대로 없다: \"{part[:60]}…\""
        if i == 0:
            pos = at
        cur = at + len(part)
    begin = max(s for off, s in starts if off <= pos)
    found = block_of(begin, block) if block else mmss(begin)
    if found != t:
        what = f"{block}초 구간 {found} (큐 {mmss(begin)})" if block else f"큐 {found}"
        return f"시각 불일치: 노트 {t} ↔ 그 말이 시작되는 {what} — \"{q[:40]}…\""
    return None


def check_bare(key, no, t, block=0):
    cues = cues_for(key, no)
    if block:
        if t not in {block_of(s, block) for s, _, _ in cues}:
            return f"{t}은 큐가 있는 {block}초 구간의 시작이 아니다"
        return None
    if t not in {mmss(s) for s, _, _ in cues}:
        return f"{t}에 시작하는 큐가 없다"
    return None


def check_expr(expr):
    if expr.count("==") != 1:
        return "검산식에는 == 가 정확히 하나 있어야 한다"
    try:
        ok = eval(expr, {"__builtins__": {}}, {"M": M, "F": Fraction})
    except Exception as e:  # 검산식 자체가 틀린 것도 실패다
        return f"계산 불가 ({type(e).__name__}: {e})"
    if ok is not True:
        lhs, rhs = (eval(p, {"__builtins__": {}}, {"M": M, "F": Fraction}) for p in expr.split("=="))
        return f"성립하지 않는다: 왼쪽 {lhs} ≠ 오른쪽 {rhs}"
    return None


FM_LINE = re.compile(r"^(?P<ind>\s*)(?:- )?(?:(?P<k>[^\s:#\"'][^:]*?):(?:\s+|$))?(?P<v>.*)$")


def check_frontmatter(fm_text):
    """PyYAML 없이 하는 최소 검사: 따옴표 없는 값 안의 ': ' 와 ' #'."""
    out = []
    for i, line in enumerate(fm_text.splitlines(), start=2):  # 1행은 ---
        if line.strip().startswith("#"):
            continue
        m = FM_LINE.match(line)
        if not m or not m["v"]:
            continue
        v = m["v"].strip()
        if not v or v[0] in "\"'[{|>&*!":
            continue
        if re.search(r":\s", v) or v.endswith(":"):
            out.append((i, f"frontmatter: 따옴표 없는 값 안에 '콜론+공백' — 값을 \"…\"로 감쌀 것: {v[:50]}"))
        elif " #" in v:
            out.append((i, f"frontmatter: 따옴표 없는 값 안에 ' #'(뒤가 주석으로 잘린다): {v[:50]}"))
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def check_file(path):
    text = open(path, encoding="utf-8").read()
    text = FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
    block = 30 if fm and re.search(r"^coords:\s*block30\s*$", fm.group(1), re.M) else 0
    fails, n = [], {"인용": 0, "좌표": 0, "검산": 0}
    if fm:
        fails.extend(check_frontmatter(fm.group(1)))
    quoted = set()
    for m in QUOTE.finditer(text):
        n["인용"] += 1
        quoted.add(m.start("key") - 1)
        try:
            err = check_quote(m["q"], m["key"], m["no"], m["t"], block)
        except (KeyError, OSError) as e:
            err = str(e)
        if err:
            fails.append((line_of(text, m.start()), err))
    for m in PRE.finditer(text):
        if m.start("key") - 1 in quoted:
            continue
        n["인용"] += 1
        quoted.add(m.start("key") - 1)
        try:
            err = check_quote(m["q"], m["key"], m["no"], m["t"], block)
        except (KeyError, OSError) as e:
            err = str(e)
        if err:
            fails.append((line_of(text, m.start()), err))
    for m in BARE.finditer(text):
        if m.start("key") - 1 in quoted:
            continue
        n["좌표"] += 1
        try:
            err = check_bare(m["key"], m["no"], m["t"], block)
        except (KeyError, OSError) as e:
            err = str(e)
        if err:
            fails.append((line_of(text, m.start()), f"[{m['key']} {m['no']} {m['t']}] {err}"))
    for m in CHECK.finditer(text):
        n["검산"] += 1
        err = check_expr(norm(m["expr"]))
        if err:
            fails.append((line_of(text, m.start()), f"검산 {err}"))
    return n, fails


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    bad = 0
    for path in args:
        n, fails = check_file(path)
        tag = "FAIL" if fails else "ok  "
        print(f"{tag} {os.path.relpath(path)} — 인용 {n['인용']} · 좌표 {n['좌표']} · 검산 {n['검산']}")
        for ln, err in fails:
            print(f"     {ln}행: {err}")
        bad += len(fails)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""노트의 기계 검사 — 커밋 전에 돌린다.

    python3 tools/check_note.py <노트.md> [<노트.md> …]
    python3 tools/check_note.py --all [폴더]          # 폴더(기본: 설정의 "all") 아래 모든 .md
    python3 tools/check_note.py <노트.md> --course 과목 --lecture N   # 라벨 인용의 과목·강을 직접 줄 때
    python3 tools/check_note.py <노트.md> --lectures 1 2 6 --glossary 사전.md

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

설정 파일 check_note.json — 노트가 있는 폴더에서 위로(git 저장소 뿌리까지), 없으면 현재 폴더에서
찾는다. --config 로 직접 줄 수도 있다. 없으면 이 저장소의 lectures/ 만 쓴다. 경로의 ~ 와 상대 경로
(설정 파일 기준)를 읽는다.

    {
      "lectures": {"Vision": "lectures/Strang_2020_vision_LA",
                   "SC1": {"dir": "…/Strang_2011_18.06SC", "index": "index_unit1.tsv"}},
      "all": "books",
      "labels": {                                  # 5. 라벨 인용 — 원문 "…" · 강의록 3쪽 "…"
        "root": "~/자료",
        "path": "(?P<course>[^/]+)/notes/L(?P<lecture>\\d+)",   # 노트 경로에서 과목·강 읽기
        "match": "nospace",                        # 공백을 모두 지우고 대조 (기본 "space": 하나로 맞춤)
        "time": "range",                           # 노트의 mm:ss·hh:mm:ss 가 강의 길이 안인가
        "time_tokens": "backtick",                 # (선택) `03:13`·`00:00–01:26`·`L01 03:13` 만 본다
        "time_slack": 1,                           # (선택) 길이보다 이만큼(초)까지는 봐준다
        "explain": {"marker": "# ② 본문", "terms": ["계수"], "symbols": {"\\hat": "햇"},
                    "glossary": "…/glossary.md"},  # (선택) 6. 설명 빠짐
        "sources": {
          "원문":   {"type": "caption", "files": ["{course}/scripts/*{lecture:02d}강*.srt"]},
          "강의록": {"type": "pdf", "files": ["{course}/강의록/*_{lecture}강_강의록.pdf"],
                     "between": "(?:\\d+쪽\\s*)?"}
        }
      }
    }

  5. 라벨 인용 (labels 가 있을 때)
       - 라벨 "…" 의 글이 그 과목·강의 자료에 있는가. caption 은 자막(vtt_text 가 읽는 모든 꼴), pdf 는 pdftotext
       - files 는 차례로 찾아 처음 맞는 파일을 쓴다. --lectures 1 2 6 이면 셋 중 어디에 있어도 된다
  6. 설명 빠짐 (labels.explain) — 본문에서 쓰는 용어·기호가 본문 표시 앞이나 용어 사전에 있는가.
       "여기 설명이 없다"를 기계적으로 짚을 뿐, 설명이 쉬운지는 판단하지 못한다

실패가 하나라도 있으면 종료 코드 1.
"""
import argparse
import csv
import glob
import json
import os
import re
import subprocess
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
CONFIG = {"dir": os.getcwd(), "all": None, "labels": None}
CONFIG_NAME = "check_note.json"

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
    if CONFIG["labels"]:
        check_labels(path, text, n, fails)
    return n, fails


# ── 설정 ──────────────────────────────────────────────

def find_config(start):
    d = os.path.abspath(start if os.path.isdir(start) else os.path.dirname(start) or ".")
    while True:
        p = os.path.join(d, CONFIG_NAME)
        if os.path.isfile(p):
            return p
        if os.path.isdir(os.path.join(d, ".git")) or os.path.dirname(d) == d:
            return None
        d = os.path.dirname(d)


def load_config(path):
    base = os.path.dirname(os.path.abspath(path))

    def where(p):
        return os.path.join(base, os.path.expanduser(p))

    with open(path, encoding="utf-8") as f:
        c = json.load(f)
    CONFIG["dir"] = base
    if "lectures" in c:
        LECTURES.clear()
        for key, v in c["lectures"].items():
            LECTURES[key] = (where(v["dir"]), v.get("index", "index.tsv")) if isinstance(v, dict) else where(v)
    if c.get("all"):
        CONFIG["all"] = where(c["all"])
    if c.get("labels"):
        lab = dict(c["labels"])
        lab["root"] = where(lab.get("root", "."))
        CONFIG["labels"] = lab


# ── 5. 라벨 인용 ──────────────────────────────────────

ARGS = argparse.Namespace(course=None, lectures=None, glossary=None)
TIME_TOKEN = re.compile(r"(?<![\d:])(\d{1,2}:\d{2}(?::\d{2})?)(?![\d:])")
TICK_TIME = re.compile(r"`(?:L(\d\d)\s+)?(\d\d):(\d\d)(?:\s*[–-]\s*(\d\d):(\d\d))?")
_src_cache = {}


def course_lectures(path):
    """(과목, [강 번호…]) — 첫 강이 그 노트의 강. 모르면 (None, [])."""
    if ARGS.lectures:
        return ARGS.course, ARGS.lectures
    pat = CONFIG["labels"].get("path")
    rel = os.path.relpath(os.path.abspath(path), CONFIG["dir"])
    m = re.search(pat, rel) if pat else None
    if not m:
        return None, []
    return m.groupdict().get("course"), [int(m["lecture"])]


def source_text(name, spec, course, lecture):
    """(대조용 글, 강의 길이 초 또는 None) — 자료가 없으면 (None, None)."""
    k = (name, course, lecture)
    if k in _src_cache:
        return _src_cache[k]
    root = CONFIG["labels"]["root"]
    found = None
    for pat in spec["files"]:
        hits = sorted(glob.glob(os.path.join(root, pat.format(course=course, lecture=lecture))))
        if hits:
            found = hits[0]
            break
    text = length = None
    if found and spec["type"] == "caption":
        cues = parse(found)
        text = " ".join(t for _, _, t in cues)
        length = int(max((e for _, e, _ in cues), default=0))
    elif found and spec["type"] == "pdf":
        try:
            text = subprocess.run(["pdftotext", found, "-"], capture_output=True, text=True).stdout
        except OSError:
            text = None
    _src_cache[k] = (text, length)
    return text, length


def to_sec(parts):
    p = [int(x) for x in parts]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def check_labels(path, text, n, fails):
    lab = CONFIG["labels"]
    squash = (lambda s: re.sub(r"\s+", "", s)) if lab.get("match") == "nospace" else norm
    course, lectures = course_lectures(path)
    lengths = {}
    for name, spec in lab["sources"].items():
        quotes = list(re.finditer(re.escape(name) + r"\s*" + spec.get("between", "") + r'"([^"]+)"', text))
        n[name] = len(quotes)
        if not lectures:
            if quotes:
                fails.append((line_of(text, quotes[0].start()), f"{name} 인용이 있는데 과목·강을 모른다 — --course/--lecture 또는 설정 labels.path"))
            continue
        hays = []
        for lec in lectures:
            src, length = source_text(name, spec, course, lec)
            if length is not None:
                lengths[lec] = max(lengths.get(lec, 0), length)
            if src is not None:
                hays.append(squash(src))
            elif spec["type"] == "caption" and lab.get("time") == "range" and lec == lectures[0]:
                fails.append((1, f"{name} 자료 없음: {course or ''} {lec}강".strip()))
        if not hays:
            for m in quotes:
                fails.append((line_of(text, m.start()), f"{name} 자료 없음: {course or ''} {lectures[0]}강".strip()))
            continue
        for m in quotes:
            q = squash(m.group(1))
            if not any(q in h for h in hays):
                fails.append((line_of(text, m.start()), f"{name} 인용 불일치: {m.group(1)[:80]}"))
    if lab.get("time") == "range" and lectures:
        slack = lab.get("time_slack", 0)
        main = lectures[0]

        def over(lec, sec, shown, pos):
            if lec not in lengths:
                fails.append((line_of(text, pos), f"L{lec:02d} 길이를 모른다 (--lectures 에 없음): {shown}"))
            elif sec > lengths[lec] + slack:
                L = lengths[lec]
                fails.append((line_of(text, pos), f"시각 범위 밖: {shown} (강의 길이 {L // 60}:{L % 60:02d})"))

        count = 0
        if lab.get("time_tokens") == "backtick":       # `03:13` · `00:00–01:26` · `L01 03:13`
            for m in TICK_TIME.finditer(text):
                lec = int(m.group(1)) if m.group(1) else main
                for mm, ss in ((m.group(2), m.group(3)), (m.group(4), m.group(5))):
                    if mm is not None:
                        count += 1
                        over(lec, to_sec((mm, ss)), f"{mm}:{ss}", m.start())
        else:                                           # 글 어디서나 mm:ss · hh:mm:ss
            for m in TIME_TOKEN.finditer(text):
                count += 1
                if lengths:
                    over(main, to_sec(m.group(1).split(":")), m.group(1), m.start())
        n["시각"] = count
    if lab.get("explain") and lectures:
        check_explain(lab["explain"], text, n, fails)


# ── 6. 설명 빠짐 (labels.explain) ──────────────────────

def check_explain(ex, text, n, fails):
    """본문 표시 앞(설명 구역)·용어 사전에 없는 용어·기호를 본문에서 쓰면 짚는다."""
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    marker = ex.get("marker", "# ② 본문")
    cut = body.find(marker)
    if cut < 0:   # 표시를 못 찾으면 검사가 통째로 통과해 버리므로(fail open) 실패로 본다
        fails.append((1, f"본문 표시 '{marker}'를 찾지 못했다 — 설명 구역을 가를 수 없다"))
        intro, rest = "", body
    else:
        intro, rest = body[:cut], body[cut:]
    gl = ARGS.glossary or ex.get("glossary")
    if gl:
        with open(os.path.join(CONFIG["dir"], os.path.expanduser(gl)) if not ARGS.glossary else gl, encoding="utf-8") as f:
            intro += "\n" + f.read()
    miss = [t for t in ex.get("terms", []) if t in rest and t not in intro]
    msym = [name for sym, name in ex.get("symbols", {}).items() if sym in rest and sym not in intro]
    n["설명"] = len(ex.get("terms", [])) + len(ex.get("symbols", {}))
    if miss:
        fails.append((1, f"용어 — 본문에서 쓰는데 앞부분에 설명이 없다: {miss}"))
    if msym:
        fails.append((1, f"기호 — 본문에서 쓰는데 앞부분에 없다: {msym}"))


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("notes", nargs="*")
    ap.add_argument("--all", nargs="?", const="", default=None)
    ap.add_argument("--config")
    ap.add_argument("--course")
    ap.add_argument("--lecture", type=int)
    ap.add_argument("--lectures", type=int, nargs="+", help="인용 출처로 허용할 강 (첫 번째가 그 노트의 강)")
    ap.add_argument("--glossary", help="용어 사전 md — 여기 설명이 있으면 노트에 없어도 통과")
    a = ap.parse_args()
    if not a.notes and a.all is None:
        print(__doc__)
        sys.exit(2)
    ARGS.course, ARGS.glossary = a.course, a.glossary
    ARGS.lectures = a.lectures or ([a.lecture] if a.lecture is not None else None)
    cfg = a.config or find_config(a.notes[0] if a.notes else (a.all or os.getcwd())) or find_config(os.getcwd())
    if cfg:
        load_config(cfg)
    args = list(a.notes)
    if a.all is not None:
        root = os.path.abspath(a.all) if a.all else CONFIG["all"]
        if not root:
            sys.exit("--all: 폴더를 주거나 설정에 \"all\"을 둘 것")
        args += sorted(os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs if f.endswith(".md"))
    bad = 0
    for path in args:
        n, fails = check_file(path)
        tag = "FAIL" if fails else "ok  "
        extra = "".join(f" · {k} {v}" for k, v in n.items() if k not in ("인용", "좌표", "검산"))
        print(f"{tag} {os.path.relpath(path)} — 인용 {n['인용']} · 좌표 {n['좌표']} · 검산 {n['검산']}{extra}")
        for ln, err in fails:
            print(f"     {ln}행: {err}")
        bad += len(fails)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

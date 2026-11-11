#!/usr/bin/env python3
"""vtt 자막을 읽기 좋은 평문으로 바꾼다.

    python3 tools/vtt_text.py <파일.vtt>            # 30초 단위로 묶어 [mm:ss] 문장…
    python3 tools/vtt_text.py <파일.vtt> --cues     # 큐 하나에 한 줄 (정확한 시각)
    python3 tools/vtt_text.py <파일.vtt> --from 03:00 --to 06:30

주의: 30초로 묶은 좌표는 **구간 시작 시각**이다. 인용에 쓸 정확한 시각은 --cues 로 찾는다.
표준 라이브러리만 쓴다.
"""
import argparse
import html
import re
import sys

TIME = re.compile(r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})\s+-->\s+(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})")
TAG = re.compile(r"<[^>]+>")


def parse(path):
    """[(시작초, 끝초, 텍스트), …] — 큐 순서 그대로."""
    cues, start, end, buf = [], None, None, []

    def flush():
        if start is not None and buf:
            text = " ".join(buf)
            text = html.unescape(TAG.sub("", text))
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                cues.append((start, end, text))

    with open(path, encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.rstrip("\n")
            m = TIME.search(line)
            if m:
                flush()
                h1, m1, s1, ms1, h2, m2, s2, ms2 = m.groups()
                start = int(h1 or 0) * 3600 + int(m1) * 60 + int(s1) + int(ms1) / 1000
                end = int(h2 or 0) * 3600 + int(m2) * 60 + int(s2) + int(ms2) / 1000
                buf = []
            elif start is not None:
                if not line.strip():
                    flush()
                    start, buf = None, []
                else:
                    buf.append(line.strip())
    flush()
    return cues


def mmss(sec):
    sec = int(sec)
    return f"{sec // 60:02d}:{sec % 60:02d}"


def to_sec(s):
    parts = [int(p) for p in s.split(":")]
    return parts[-1] + parts[-2] * 60 + (parts[-3] * 3600 if len(parts) == 3 else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vtt")
    ap.add_argument("--cues", action="store_true", help="큐 하나에 한 줄")
    ap.add_argument("--from", dest="lo", default=None, help="mm:ss 부터")
    ap.add_argument("--to", dest="hi", default=None, help="mm:ss 까지")
    ap.add_argument("--block", type=int, default=30, help="묶는 단위(초). 기본 30")
    a = ap.parse_args()

    cues = parse(a.vtt)
    lo = to_sec(a.lo) if a.lo else 0
    hi = to_sec(a.hi) if a.hi else float("inf")
    cues = [c for c in cues if lo <= c[0] < hi]

    if a.cues:
        for s, _, t in cues:
            print(f"[{mmss(s)}] {t}")
        return

    blocks = {}
    for s, _, t in cues:
        blocks.setdefault(int(s) // a.block, []).append(t)
    for k in sorted(blocks):
        print(f"[{mmss(k * a.block)}] {' '.join(blocks[k])}\n")
    if cues:
        print(f"# 큐 {len(cues)}개 · 끝 {mmss(cues[-1][1])} · 단어 약 {sum(len(t.split()) for _, _, t in cues)}", file=sys.stderr)


if __name__ == "__main__":
    main()

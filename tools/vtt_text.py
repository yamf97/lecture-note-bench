#!/usr/bin/env python3
"""vtt 자막을 읽기 좋은 평문으로 바꾼다.

    python3 tools/vtt_text.py <파일.vtt>            # 30초 단위로 묶어 [mm:ss] 문장…
    python3 tools/vtt_text.py <파일.vtt> --cues     # 큐 하나에 한 줄 (정확한 시각)
    python3 tools/vtt_text.py <파일.vtt> --from 03:00 --to 06:30

주의: 30초로 묶은 좌표는 **구간 시작 시각**이다. 인용에 쓸 정확한 시각은 --cues 로 찾는다.
YouTube 자동 자막(yt-dlp, 단어별 시각 포함)과 SRT(whisper 출력 등)도 읽는다.
표준 라이브러리만 쓴다.
"""
import argparse
import html
import re
import sys

TIME = re.compile(r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})\s+-->\s+(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})")
TAG = re.compile(r"<[^>]+>")
WORD_TIME = re.compile(r"<\d{2}:\d{2}:\d{2}[.,]\d{3}>")  # YouTube 자동 자막의 단어별 시각


def clean(line):
    line = html.unescape(TAG.sub("", line))
    return re.sub(r"\s+", " ", line).strip()


def parse(path):
    """[(시작초, 끝초, 텍스트), …] — 큐 순서 그대로.

    YouTube 자동 자막(yt-dlp)은 앞 큐의 줄을 다음 큐에서 되풀이한다. 단어별 시각 태그가 있는
    파일이면 이 자막으로 보고, 시각 태그 없는 줄이 바로 앞에 나온 줄과 같으면 버린다. 새로 나온
    말에는 늘 태그가 붙으므로, 강사가 같은 말을 연달아 두 번 해도 둘 다 남는다.
    사람이 단 자막에는 이 처리를 하지 않는다 — 실제로 되풀이한 말이 지워지기 때문이다.
    """
    raw_cues, start, end, buf, rolling = [], None, None, [], False

    def flush():
        if start is not None and buf:
            raw_cues.append((start, end, buf))

    with open(path, encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            m = TIME.search(line)
            if m:
                flush()
                h1, m1, s1, ms1, h2, m2, s2, ms2 = m.groups()
                start = int(h1 or 0) * 3600 + int(m1) * 60 + int(s1) + int(ms1) / 1000
                end = int(h2 or 0) * 3600 + int(m2) * 60 + int(s2) + int(ms2) / 1000
                buf = []
            elif start is not None:
                if not line.strip():
                    # yt-dlp 단어 시각 큐는 공백 한 칸 줄로 시작한다 — 아직 글이 없으면 큐의 끝이 아니다
                    if buf:
                        flush()
                        start, buf = None, []
                else:
                    buf.append(line)
                    rolling = rolling or bool(WORD_TIME.search(line))
    flush()

    cues, last = [], None
    for s, e, lines in raw_cues:
        lines = [(c, bool(WORD_TIME.search(x))) for x in lines for c in [clean(x)] if c]
        new = [c for c, timed in lines if timed or not rolling or c != last]
        if lines:
            last = lines[-1][0]
        if new:
            cues.append((s, e, " ".join(new)))
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

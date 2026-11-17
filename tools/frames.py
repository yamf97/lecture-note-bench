#!/usr/bin/env python3
"""강의 영상에서 판서·슬라이드 장면을 시각과 함께 뽑는다 — 판서를 노트(LaTeX)로 옮길 때 쓴다.

    python3 tools/frames.py 강의.mp4                     # 자동: 화면이 크게 바뀌기 직전 장면
    python3 tools/frames.py 강의.mp4 --at 05:32,12:00    # 직접: 그 시각의 장면만
    python3 tools/frames.py 강의.mp4 --every 30          # 일정 간격(초)으로
    python3 tools/frames.py 강의.mp4 --from 10:00 --to 20:00 -o 판서

결과: <영상 이름>_frames/ 안에 mm-ss.jpg 와 index.tsv (초 · mm:ss · 왜 뽑았나 · 파일).
시각은 자막 [mm:ss] 좌표와 같은 기준(영상 시작부터)이다.

자동으로 고르는 기준
  1. 화면이 크게 바뀌는 순간을 찾는다 — ffmpeg 장면 점수(앞뒤 화면 차이, 0–1)가 --scene(기본 0.05)를 넘는 때.
     판서 지우기·슬라이드 넘김·카메라 전환이 여기에 걸린다. --min-gap(기본 3초) 안의 잇따른 변화는 하나로 본다.
     기본값 근거: 합성 판서 영상 실측(2026-11-17)에서 글씨 더하기 0.03–0.06, 칠판 일부 지우기 0.05–0.14.
     claude-video 기본 0.2로는 지우기도 안 잡힌다(칠판은 대부분 그대로라 점수가 낮다). 놓치는 것보다
     많이 뽑는 쪽이 노트에 안전해 낮게 잡았다. **실제 강의는 강사의 움직임이 점수를 흔든다 — 처음 쓰는
     강좌는 --scores 로 점수를 보고 --scene 을 맞출 것**
  2. 바뀐 **직후가 아니라 직전**(--before, 기본 0.5초 전) 장면을 뽑는다 — 지운 뒤 빈 칠판이 아니라
     지우기 전 가득 찬 칠판, 넘기기 전 다 채워진 슬라이드가 필요하다. 영상 마지막 장면도 넣는다
  3. 뽑은 장면 사이가 --every(기본 30초)보다 길면 그 사이를 간격 장면으로 채운다
     (지우지 않고 계속 써 내려가는 판서, 카메라 하나가 칠판만 찍는 강의)
  4. 거의 같은 장면은 버린다 — 16×16 썸네일의 화소 평균 차이가 --dedup(기본 2.0, 0–255) 이하이면 같은 장면
  5. --max(기본 120)를 넘으면 고르게 솎는다
장면 감지는 바뀐 순간을 다 잡지 못한다. 빠진 곳은 자막을 읽고 --at 으로 더 뽑는다.

필요한 것: ffmpeg · ffprobe. 표준 라이브러리만 쓴다. 이 컴퓨터에서만 돈다.
장면 점수 + 썸네일 중복 제거는 claude-video(Bradley Bonanno, MIT)의 frames.py 방식을 참고했다
— Inspired by bradautomates/claude-video (license: MIT).
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtt_text import mmss  # noqa: E402


def to_sec(s):
    p = [float(x) for x in str(s).split(":")]
    return p[-1] + (p[-2] * 60 if len(p) > 1 else 0) + (p[-3] * 3600 if len(p) > 2 else 0)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout
    return float(out.strip())


def scene_changes(path, threshold, lo, hi):
    """화면이 크게 바뀐 시각들 (영상 시작 기준 초)."""
    cmd = ["ffmpeg", "-hide_banner", "-ss", str(lo), "-to", str(hi), "-i", path, "-an",
           "-vf", f"scale=320:-2,select='gt(scene\\,{threshold})',showinfo", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL).stderr
    return [lo + float(t) for t in re.findall(r"pts_time:([\d.]+)", err)]


def show_scores(a):
    lo = to_sec(a.lo) if a.lo else 0.0
    hi = to_sec(a.hi) if a.hi else duration(a.video)
    cmd = ["ffmpeg", "-hide_banner", "-ss", str(lo), "-to", str(hi), "-i", a.video, "-an", "-vf",
           "scale=320:-2,select='gt(scene\\,0.01)',metadata=print:key=lavfi.scene_score", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL).stderr
    pts = re.findall(r"pts_time:([\d.]+)", err)
    sc = [float(x) for x in re.findall(r"scene_score=([\d.]+)", err)]
    rows = list(zip((lo + float(t) for t in pts), sc))
    for th in (0.02, 0.03, 0.05, 0.1, 0.2, 0.3):
        print(f"--scene {th:<4} → 바뀐 순간 {sum(1 for _, x in rows if x > th)}개")
    print("점수 높은 순 20개 (시각 · 점수):")
    for t, x in sorted(rows, key=lambda r: -r[1])[:20]:
        print(f"  {mmss(t)}  {x:.3f}")


def grab(path, t, out, width):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                        "-vf", f"scale='min({width},iw)':-2", "-q:v", "3", out], stdin=subprocess.DEVNULL)
    return r.returncode == 0 and os.path.exists(out)


def thumb(img):
    return subprocess.run(["ffmpeg", "-v", "error", "-i", img, "-vf", "scale=16:16", "-f", "rawvideo",
                           "-pix_fmt", "rgb24", "-"], capture_output=True, stdin=subprocess.DEVNULL).stdout


def delta(a, b):
    if not a or len(a) != len(b):
        return 255.0
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def plan(path, a):
    total = duration(path)
    lo = to_sec(a.lo) if a.lo else 0.0
    hi = min(to_sec(a.hi), total) if a.hi else total
    last = max(lo, hi - 0.5)
    if a.at:
        return [(to_sec(t), "직접") for t in a.at.split(",") if t.strip()]
    if a.every_only:
        return [(min(t + a.every_only, last), "간격") for t in frange(lo, hi, a.every_only)]
    changes = []
    for t in scene_changes(path, a.scene, lo, hi):
        if not changes or t - changes[-1] >= a.min_gap:
            changes.append(t)
    picks = [(max(lo, t - a.before), "바뀌기 직전") for t in changes if t - a.before > lo]
    picks += [(t, "간격") for t in fill_gaps([p for p, _ in picks], lo, last, a.every)]
    picks.append((last, "끝"))
    return picks


def fill_gaps(times, lo, hi, step):
    """times 사이(와 앞뒤)가 step 보다 길게 비면 step 간격 시각을 채운다."""
    out, prev = [], lo
    for t in sorted(times) + [hi]:
        k = prev + step
        while k < t - 1:
            out.append(k)
            k += step
        prev = t
    return out


def frange(lo, hi, step):
    t = lo
    while t < hi:
        yield t
        t += step


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-o", "--outdir")
    ap.add_argument("--at", help="직접 고른 시각들 mm:ss,mm:ss,…")
    ap.add_argument("--every", type=float, default=30, help="뽑은 장면 사이가 이보다 길면 채울 간격(초)")
    ap.add_argument("--scores", action="store_true", help="뽑지 않고 장면 점수만 보인다 (--scene 맞추기용)")
    ap.add_argument("--every-only", dest="every_only", type=float, help="장면 감지 없이 이 간격(초)으로만")
    ap.add_argument("--scene", type=float, default=0.05)
    ap.add_argument("--min-gap", dest="min_gap", type=float, default=3)
    ap.add_argument("--before", type=float, default=0.5)
    ap.add_argument("--dedup", type=float, default=2.0)
    ap.add_argument("--no-dedup", action="store_true")
    ap.add_argument("--max", type=int, default=120)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--from", dest="lo")
    ap.add_argument("--to", dest="hi")
    a = ap.parse_args()

    if a.scores:
        show_scores(a)
        return
    stem = os.path.splitext(os.path.basename(a.video))[0]
    outdir = a.outdir or os.path.join(os.path.dirname(os.path.abspath(a.video)), f"{stem}_frames")
    os.makedirs(outdir, exist_ok=True)

    picks = sorted(plan(a.video, a))
    if len(picks) > a.max:
        step = len(picks) / a.max
        picks = [picks[int(i * step)] for i in range(a.max)]
    kept, last_thumb, dropped = [], None, 0
    for t, why in picks:
        name = mmss(t).replace(":", "-") + ".jpg"
        out = os.path.join(outdir, name)
        if not grab(a.video, t, out, a.width):
            print(f"뽑기 실패: {mmss(t)}", file=sys.stderr)
            continue
        th = thumb(out)
        if not a.no_dedup and why != "직접" and last_thumb is not None and delta(th, last_thumb) <= a.dedup:
            os.remove(out)
            dropped += 1
            continue
        last_thumb = th
        kept.append((t, why, name))
    with open(os.path.join(outdir, "index.tsv"), "w", encoding="utf-8") as f:
        f.write("sec\tmmss\twhy\tfile\n")
        for t, why, name in kept:
            f.write(f"{t:.1f}\t{mmss(t)}\t{why}\t{name}\n")
    reasons = {}
    for _, why, _ in kept:
        reasons[why] = reasons.get(why, 0) + 1
    print(f"{outdir} — 장면 {len(kept)}장 ({', '.join(f'{k} {v}' for k, v in reasons.items())})"
          f" · 같은 장면 버림 {dropped}")


if __name__ == "__main__":
    main()

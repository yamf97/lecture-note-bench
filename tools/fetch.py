#!/usr/bin/env python3
"""강의 자막(과 필요하면 영상·음성)을 YouTube에서 받는다 — 막히지 않게 천천히, 이어받기로.

    python3 tools/fetch.py <강좌 폴더> [--max 10]      # 폴더의 fetch.json 대로 (재생목록·id 목록)
    python3 tools/fetch.py <강좌 폴더> --max 0          # 네트워크 없이 plain·failed.tsv·TOC.md 만 갱신
    python3 tools/fetch.py --url <영상 주소> -o <폴더> [--video] [--transcribe-missing]   # 한 편

강좌 폴더의 fetch.json (예):
    {"series": "Ben Lambert - A graduate course in econometrics",
     "playlist": "https://www.youtube.com/playlist?list=…",   # 또는 "ids": "ids.tsv" (id<TAB>묶음)
     "via": "transcript-api",          # 자막 받는 길: transcript-api(youtube_transcript_api) | yt-dlp
     "langs": ["ko", "en"],            # transcript-api 언어 순서 / yt-dlp 는 sub-langs (예: ["en-orig"])
     "naming": "index",                # index: raw/001_제목.txt (+failed.tsv·TOC.md) | id: raw/<id>.<lang>.vtt
     "plain": "lines"}                 # (선택) plain/ 만들기 — lines: 구간마다 한 줄 | blocks: 30초 문단 [mm:ss]

막히지 않게 하는 장치 (강좌별 스크립트 세 개 — Lambert·DSBA·Stapleton — 를 합친 것, 2026-11-17)
  1. 강의당 요청 1번. raw 만 받고 plain 은 raw 에서 로컬로 만든다
  2. 요청 사이 20–40초 무작위 대기, 10번마다 3분 휴식
  3. 차단 응답이면 그 자리에서 멈춘다 (계속 요청해 차단을 늘리지 않는다). 종료코드 2
  4. 한 번에 받을 수를 --max 로 제한. 다시 돌리면 raw 가 없는 강의부터 이어받는다
  판정은 종료코드가 아니라 **내용**으로 한다 — youtube_transcript_api 는 실패해도 0 을 낸다

자막이 없을 때: --transcribe-missing 이면 음성만 받아 transcribe.py(로컬 whisper)로 raw/<이름> (whisper).srt.
--video 면 video/<이름>.mp4 (720p 이하)도 받는다 — frames.py 로 판서 장면을 뽑을 때.
결과 파일은 vtt_text.py · check_note.py 가 그대로 읽는다.

필요한 것: yt-dlp · (via transcript-api 면) youtube_transcript_api · (전사 시) ffmpeg·whisper-cli.
"""
import argparse
import ast
import glob
import json
import os
import random
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vtt_text import parse, mmss  # noqa: E402

NOTX_RE = re.compile(r"Could not retrieve a transcript")
BLOCK_TAPI = re.compile(r"blocking requests from your IP|RequestBlocked|IpBlocked|Too Many Requests")
BLOCK_YTDLP = re.compile(r"429|Too Many Requests|Sign in to confirm|bot", re.I)
SLEEP = (20, 40)
REST_EVERY, REST = 10, 180


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)


def safe_name(title):
    """bash `tr -cd '[:alnum:] ._-' | tr -s ' ' '_' | cut -c1-70` 과 같은 결과 (한글 로캘)."""
    s = "".join(c for c in title if c.isalnum() or c in " ._-")
    return re.sub(r" +", "_", s)[:70]


def read_index(path):
    """(번호, id, 길이 또는 '', 제목). 3열(번호·id·제목)·4열(번호·id·길이·제목) 모두 읽는다."""
    rows = []
    for line in open(path, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 4 and p[2].replace(".", "").isdigit():
            rows.append((p[0], p[1], p[2], "\t".join(p[3:])))
        elif len(p) >= 3:
            rows.append((p[0], p[1], "", "\t".join(p[2:])))
    return rows


def segments(text):
    if text.startswith("# "):
        text = text.split("\n", 4)[4]
    try:
        data = ast.literal_eval(text.strip())
    except (ValueError, SyntaxError):
        return None
    segs = data[0] if data and isinstance(data[0], list) else data
    return segs if segs and all(isinstance(s, dict) and "text" in s for s in segs) else None


def make_plain(raw, dst, style):
    if style == "lines":   # 머리 4줄 + 구간 글을 줄마다 (Lambert·DSBA 꼴)
        parts = open(raw, encoding="utf-8").read().split("\n", 4)
        segs = segments(parts[4])
        if segs is None:
            return False
        with open(dst, "w", encoding="utf-8") as f:
            f.write("\n".join(parts[:4]) + "\n" + "\n".join(s["text"] for s in segs) + "\n")
        return True
    cues = parse(raw)      # blocks: 30초 칸 [mm:ss] 문단 (vtt_text 와 같은 규칙)
    blocks = {}
    for s, _, t in cues:
        blocks.setdefault(int(s) // 30, []).append(t)
    with open(dst, "w", encoding="utf-8") as f:   # vtt_text.py 기본 출력과 같은 꼴
        f.write("".join(f"[{mmss(k * 30)}] {' '.join(v)}\n\n" for k, v in sorted(blocks.items())))
    return bool(cues)


def pause(n):
    if n == 0:
        return
    if n % REST_EVERY == 0:
        print(f">> {REST}초 휴식", flush=True)
        time.sleep(REST)
    else:
        time.sleep(random.randint(*SLEEP))


def get_transcript_api(vid, langs, title, series, out):
    """'ok' | 'none' | 'blocked' | 'bad'."""
    r = run(["youtube_transcript_api", "--languages", *langs, "--", vid])
    body = r.stdout + r.stderr
    if NOTX_RE.search(body):
        return "blocked" if BLOCK_TAPI.search(body) else "none"
    if segments(r.stdout) is None:
        return "bad"
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n# https://www.youtube.com/watch?v={vid}\n# {series}\n\n{r.stdout}")
    return "ok"


def get_ytdlp_subs(vid, langs, out_tmpl, index_line=None, index_file=None):
    cmd = ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", ",".join(langs),
           "--sub-format", "vtt", "-o", out_tmpl]
    if index_line and index_file:
        cmd += ["--print-to-file", index_line, index_file, "--no-simulate"]
    r = run(cmd + ["--", vid])
    log = r.stdout + r.stderr
    if BLOCK_YTDLP.search(log):
        return "blocked", log
    stem = out_tmpl.replace(".%(ext)s", "")
    return ("ok" if glob.glob(glob.escape(stem) + ".*.vtt") else "none"), log


def get_media(vid, out_base, kind):
    if kind == "video":
        cmd = ["yt-dlp", "-f", "bv*[height<=720]+ba/b[height<=720]", "--merge-output-format", "mp4",
               "-o", out_base + ".%(ext)s", "--", vid]
    else:
        cmd = ["yt-dlp", "-f", "ba", "-x", "--audio-format", "m4a", "-o", out_base + ".%(ext)s", "--", vid]
    r = run(cmd)
    if BLOCK_YTDLP.search(r.stdout + r.stderr) and r.returncode:
        return "blocked"
    return "ok" if glob.glob(glob.escape(out_base) + ".*") else "fail"


def transcribe(audio, outdir, lang):
    r = subprocess.run([sys.executable, os.path.join(HERE, "transcribe.py"), audio, "-o", outdir,
                        "-l", lang], stdin=subprocess.DEVNULL)
    return r.returncode == 0


def has_raw(raw_dir, prefix):
    return any(glob.glob(os.path.join(raw_dir, glob.escape(prefix) + ext)) for ext in ("*.txt", "*.vtt", "*.srt"))


def course(folder, a):
    cfg = json.load(open(os.path.join(folder, "fetch.json"), encoding="utf-8"))
    via, langs = cfg.get("via", "transcript-api"), cfg.get("langs", ["en"])
    series, plain = cfg.get("series", ""), cfg.get("plain")
    raw_dir, plain_dir = os.path.join(folder, "raw"), os.path.join(folder, "plain")
    os.makedirs(raw_dir, exist_ok=True)
    if plain:
        os.makedirs(plain_dir, exist_ok=True)
    index = os.path.join(folder, "index.tsv")
    requested = 0
    stopped = False

    if cfg.get("ids"):   # id 목록 꼴 (Stapleton): raw/<id>.<lang>.vtt, index.tsv 에 한 줄씩 덧붙임
        for line in open(os.path.join(folder, cfg["ids"]), encoding="utf-8"):
            vid, _, group = line.rstrip("\n").partition("\t")
            got = glob.glob(os.path.join(raw_dir, glob.escape(vid) + ".*.vtt")) if vid else []
            if got and plain and not os.path.exists(os.path.join(plain_dir, vid + ".txt")):
                ok = make_plain(sorted(got)[0], os.path.join(plain_dir, vid + ".txt"), plain)
                print(f"   [plain] {vid} raw에서 생성 (요청 없음)" if ok else f"   [WARN ] {vid} plain 생성 실패")
            if not vid or got:
                continue
            if requested >= a.max:
                continue
            pause(requested)
            requested += 1
            res, log = get_ytdlp_subs(vid, langs, os.path.join(raw_dir, "%(id)s.%(ext)s"),
                                      f"%(id)s\t%(upload_date)s\t%(duration)s\t%(title)s\t{group}", index)
            if res == "blocked":
                print(f"!! {vid}에서 차단 응답 — 즉시 중단\n" + "\n".join(log.splitlines()[-3:]))
                stopped = True
                break
            got = glob.glob(os.path.join(raw_dir, glob.escape(vid) + ".*.vtt"))
            if res == "ok" and plain and got:
                make_plain(sorted(got)[0], os.path.join(plain_dir, vid + ".txt"), plain)
            print(f"   [{'ok' if res == 'ok' else 'NOSUB'}] {vid}")
        print(f"\n이번 요청 {requested}" + (" · ** 차단으로 중단됨 **" if stopped else ""))
        return 2 if stopped else 0

    if not os.path.exists(index):   # 재생목록 꼴 (Lambert·DSBA)
        print(">> 재생목록 목록 수집 중...")
        r = run(["yt-dlp", "--flat-playlist", "--print",
                 "%(playlist_index)s\t%(id)s\t%(duration)s\t%(title)s", cfg["playlist"]])
        open(index, "w", encoding="utf-8").write(r.stdout)
    rows = read_index(index)
    print(f">> 총 {len(rows)}개 강의, 이번 최대 {a.max}개 요청")
    for idx, vid, _, title in rows:
        num = f"{int(idx):03d}"
        base = f"{num}_{safe_name(title)}"
        rawf = os.path.join(raw_dir, base + ".txt")
        if has_raw(raw_dir, num + "_"):
            if plain and not glob.glob(os.path.join(plain_dir, glob.escape(num) + "_*.txt")):
                src = sorted(glob.glob(os.path.join(raw_dir, glob.escape(num) + "_*")))[0]
                ok = make_plain(src, os.path.join(plain_dir, base + ".txt"), plain)
                print(f"   [plain] {num} raw에서 생성 (요청 없음)" if ok else f"   [WARN ] {num} plain 생성 실패")
            continue
        if requested >= a.max:
            continue
        pause(requested)
        requested += 1
        if via == "transcript-api":
            res = get_transcript_api(vid, langs, title, series, rawf)
        else:
            res, _ = get_ytdlp_subs(vid, langs, os.path.join(raw_dir, base + ".%(ext)s"))
        if res == "none" and a.transcribe_missing:
            audio = os.path.join(folder, "audio", base)
            os.makedirs(os.path.dirname(audio), exist_ok=True)
            res = get_media(vid, audio, "audio")
            if res == "ok":
                res = "ok" if transcribe(glob.glob(glob.escape(audio) + ".*")[0], raw_dir, a.lang) else "none"
        if res == "blocked":
            print(f"!! {num}에서 차단 응답 — 즉시 중단. VPN 서버를 바꾸거나 시간이 지난 뒤 다시 실행")
            stopped = True
            break
        if res != "ok":
            print(f"   [FAIL ] {num} {title} — {'자막 없음' if res == 'none' else '응답을 자막으로 읽지 못함'}")
            continue
        if plain:
            src = sorted(glob.glob(os.path.join(raw_dir, glob.escape(num) + "_*")))[0]
            make_plain(src, os.path.join(plain_dir, base + ".txt"), plain)
        got_video = get_media(vid, os.path.join(folder, "video", base), "video") if a.video else None
        print(f"   [ ok  ] {num} {title}" + (f" · 영상 {got_video}" if got_video else ""))

    with open(os.path.join(folder, "failed.tsv"), "w", encoding="utf-8") as f:
        for idx, vid, _, title in rows:
            if not has_raw(raw_dir, f"{int(idx):03d}_"):
                f.write(f"{idx}\t{vid}\t{title}\n")
    with open(os.path.join(folder, "TOC.md"), "w", encoding="utf-8") as f:
        f.write(f"# {series}\n\n| # | 제목 | 링크 |\n|---|------|------|\n")
        for idx, vid, _, title in rows:
            f.write(f"| {idx} | {title} | https://youtu.be/{vid} |\n")
    n_raw = sum(1 for idx, *_ in rows if has_raw(raw_dir, f"{int(idx):03d}_"))
    print(f"\n이번 요청 {requested} · raw {n_raw}/{len(rows)} · 미확보 {len(rows) - n_raw} (failed.tsv)"
          + (" · ** 차단으로 중단됨 **" if stopped else ""))
    return 2 if stopped else 0


def single(a):
    """영상 한 편: <폴더>/raw/<id>…, 필요하면 video/·audio/."""
    folder = a.outdir or "."
    raw_dir = os.path.join(folder, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    r = run(["yt-dlp", "--print", "%(id)s\t%(title)s", "--skip-download", "--", a.url])
    if r.returncode or "\t" not in r.stdout:
        print("영상 정보를 못 읽었다\n" + r.stderr[-500:], file=sys.stderr)
        return 1
    vid, title = r.stdout.strip().split("\t", 1)
    langs = a.langs.split(",")
    res = get_transcript_api(vid, langs, title, a.series or "", os.path.join(raw_dir, vid + ".txt"))
    if res == "blocked":
        print("!! 차단 응답 — 중단", file=sys.stderr)
        return 2
    if res != "ok" and a.transcribe_missing:
        audio = os.path.join(folder, "audio", vid)
        os.makedirs(os.path.dirname(audio), exist_ok=True)
        if get_media(vid, audio, "audio") == "ok":
            res = "ok" if transcribe(glob.glob(glob.escape(audio) + ".*")[0], raw_dir, a.lang) else res
    print(f"자막: {'ok' if res == 'ok' else '없음'} — {title}")
    if a.video:
        print(f"영상: {get_media(vid, os.path.join(folder, 'video', vid), 'video')}")
    return 0 if res == "ok" else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?")
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--url")
    ap.add_argument("-o", "--outdir")
    ap.add_argument("--langs", default="ko,en", help="--url 일 때 자막 언어 순서")
    ap.add_argument("--series")
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--transcribe-missing", dest="transcribe_missing", action="store_true")
    ap.add_argument("-l", "--lang", default="auto", help="전사 언어 (ko·en·auto)")
    a = ap.parse_args()
    if a.url:
        sys.exit(single(a))
    if not a.folder:
        ap.print_help()
        sys.exit(2)
    sys.exit(course(a.folder, a))


if __name__ == "__main__":
    main()

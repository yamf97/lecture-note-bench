#!/usr/bin/env python3
"""강의 음성·영상을 로컬 whisper로 받아써 SRT 자막을 만든다 — 자막이 없는 강의용.

    lnb transcribe 강의.mp4 -l ko                  # 파일 하나 → 그 옆에 자막
    lnb transcribe ~/강의 -o ~/강의자막 -l ko      # 폴더 통째로 → 같은 하위 구조로
    lnb transcribe 강의.mp3 -m ~/models/ggml-large-v3-turbo-q5_0.bin
    (설치하지 않았으면 저장소에서 `lnb transcribe` 대신 `python3 tools/transcribe.py`)

결과: <이름> (whisper <모델>).srt   예: 1강 (whisper large-v3-turbo-q5_0).srt
  - -o 가 없으면 강의 파일 옆에, 있으면 -o 아래에 만든다. 폴더를 주면 그 안의 하위 폴더
    구조를 -o 아래에 그대로 만든다 (물리/1강.mp4 → <-o>/물리/1강 (whisper …).srt).
  - 같은 폴더에 1강.mp4 와 1강.m4a 처럼 이름만 같은 파일이 있으면 「1강.mp4 (whisper …).srt」처럼
    확장자까지 넣어 서로 덮어쓰지 않게 한다.
  - 같은 모델의 자막이 이미 있으면 건너뛴다 — 끊겼으면 같은 명령을 다시 치면 이어서 한다.
    모델을 바꾸면 이름이 달라지므로 새로 만들고, 예전 자막은 그대로 둔다. 다시 하려면 --force.
  - 자막은 다 만든 뒤에야 제 이름이 된다. 도중에 끊겨 반쪽 자막이 남는 일은 없다.
  - 실패한 파일은 끝에 모아 보이고, -o 가 있으면 <-o>/failed.txt 에도 적는다.

필요한 것 (밖으로 보내는 것 없음, 이 컴퓨터에서만 실행된다):
  - whisper.cpp 의 whisper-cli  (macOS: brew install whisper-cpp)
  - ffmpeg / ffprobe            (어떤 음성·영상이든 16kHz 모노 wav로 바꾼다)
  - ggml 모델 파일 — lnb setup 으로 받거나, -m 또는 환경변수 WHISPER_MODEL

자막 끝 시각이 음성보다 10초 넘게 짧으면 경고한다 (이미 있던 자막도 확인한다).
자동 전사라 숫자·용어 오인식이 있다. 인용은 대본 그대로 하고 정정은 따로 표시한다.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import time

from .vtt_text import parse, mmss

MODEL_DIRS = [
    "~/.cache/whisper.cpp",
    "~/.cache/whisper",
    "~/models/whisper",
]
PREFERRED = ["ggml-large-v3-turbo-q5_0.bin", "ggml-large-v3-turbo.bin", "ggml-large-v3.bin"]
MEDIA = {".mp3", ".m4a", ".aac", ".wav", ".flac", ".ogg", ".opus",
         ".mp4", ".m4v", ".mov", ".mkv", ".webm", ".avi"}
SHORT = 10  # 자막 끝이 음성보다 이만큼(초) 넘게 짧으면 경고


def find_model(given):
    if given:
        return os.path.expanduser(given)
    if os.environ.get("WHISPER_MODEL"):
        return os.path.expanduser(os.environ["WHISPER_MODEL"])
    found = []
    for d in MODEL_DIRS:
        found += glob.glob(os.path.join(os.path.expanduser(d), "ggml-*.bin"))
    for name in PREFERRED:
        for f in found:
            if os.path.basename(f) == name:
                return f
    return found[0] if found else None


def model_tag(model):
    """ggml-large-v3-turbo-q5_0.bin → large-v3-turbo-q5_0 (자막 파일 이름에 들어간다)."""
    name = os.path.basename(model)
    if name.endswith(".bin"):
        name = name[:-4]
    if name.startswith("ggml-"):
        name = name[5:]
    return name


def duration(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout
        return float(out.strip())
    except (OSError, ValueError):
        return None


def collect(paths, outdir):
    """[(원본, 자막을 둘 폴더)] — 폴더는 하위까지 뒤져 MEDIA 확장자만, 숨김 파일은 뺀다."""
    jobs = []
    for p in paths:
        p = os.path.expanduser(p)
        if os.path.isdir(p):
            base = os.path.abspath(p)
            for root, dirs, files in os.walk(base):
                dirs[:] = sorted(d for d in dirs if not d.startswith("."))
                for f in sorted(files):
                    if f.startswith(".") or os.path.splitext(f)[1].lower() not in MEDIA:
                        continue
                    rel = os.path.relpath(root, base)
                    dest = root if not outdir else os.path.normpath(os.path.join(outdir, rel))
                    jobs.append((os.path.join(root, f), dest))
        else:
            jobs.append((p, outdir or os.path.dirname(os.path.abspath(p))))
    return jobs


def srt_path(src, dest, tag, keep_ext=False):
    """keep_ext: 같은 폴더에 이름이 같고 확장자만 다른 파일이 있으면 확장자까지 넣어 겹치지 않게 한다."""
    name = os.path.basename(src)
    stem = name if keep_ext else os.path.splitext(name)[0]
    return os.path.join(dest, f"{stem} (whisper {tag}).srt")


def srt_paths(jobs, tag):
    """[(원본, 자막)] — 1강.mp4 와 1강.m4a 가 같이 있으면 둘 다 「1강.mp4 (whisper …)」 꼴로.
    같은 파일을 두 번 주면 한 번만 한다."""
    uniq, seen = [], set()
    for src, dest in jobs:
        key = (os.path.realpath(src), os.path.normpath(dest))
        if key not in seen:
            seen.add(key)
            uniq.append((src, dest))
    plain = [srt_path(src, dest, tag) for src, dest in uniq]
    return [(src, srt_path(src, dest, tag, keep_ext=plain.count(p) > 1))
            for (src, dest), p in zip(uniq, plain)]


def srt_end(srt):
    """자막 끝 시각(초). 읽을 수 없는 파일이면 0 — 경고로 드러난다."""
    try:
        return max((e for _, e, _ in parse(srt)), default=0)
    except (OSError, ValueError):
        return 0


def transcribe(src, srt, model, lang, threads):
    """src → srt. 성공하면 (True, 메시지), 실패하면 (False, 사유). 반쪽 파일은 남기지 않는다."""
    if not os.path.isfile(src):
        return False, "파일이 없다"
    os.makedirs(os.path.dirname(srt), exist_ok=True)
    part_base = srt[:-4] + ".part"  # whisper-cli 가 .srt 를 붙인다 → "….part.srt"
    part = part_base + ".srt"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "audio.wav")
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ar", "16000", "-ac", "1", wav],
                               capture_output=True, text=True)
            if r.returncode:
                return False, f"ffmpeg — {r.stderr.strip()[-300:]}"
            r = subprocess.run(["whisper-cli", "-m", model, "-f", wav, "-l", lang, "-t", str(threads),
                                "-osrt", "-of", part_base], capture_output=True, text=True)
            if r.returncode or not os.path.exists(part):
                return False, f"whisper-cli — {r.stderr.strip()[-300:]}"
        os.replace(part, srt)
    finally:
        if os.path.exists(part):
            os.remove(part)
    return True, ""


def hms(sec):
    sec = int(sec)
    return f"{sec // 3600}시간 {sec % 3600 // 60}분" if sec >= 3600 else f"{sec // 60}분"


def main(argv=None, prog=None):
    ap = argparse.ArgumentParser(prog=prog, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", metavar="파일|폴더")
    ap.add_argument("-l", "--language", default="auto", help="ko · en · auto(기본)")
    ap.add_argument("-m", "--model")
    ap.add_argument("-o", "--outdir", help="자막을 둘 폴더 (폴더를 주면 하위 구조를 그대로 만든다)")
    ap.add_argument("-t", "--threads", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    ap.add_argument("--force", action="store_true", help="같은 모델의 자막이 있어도 다시 만든다")
    a = ap.parse_args(argv)
    for tool in ("whisper-cli", "ffmpeg"):
        if not shutil.which(tool):
            sys.exit(f"{tool} 이 없다 — lnb setup 으로 확인할 것")
    model = find_model(a.model)
    if not model or not os.path.exists(model):
        sys.exit("whisper 모델 파일을 못 찾았다 — lnb setup 으로 받거나, -m 또는 WHISPER_MODEL 로 ggml-*.bin 경로를 줄 것")
    outdir = os.path.abspath(os.path.expanduser(a.outdir)) if a.outdir else None
    tag = model_tag(model)

    jobs = collect(a.paths, outdir)
    if not jobs:
        sys.exit("받아쓸 파일이 없다 — 지원 확장자: " + " ".join(sorted(MEDIA)))
    todo, done = [], 0
    for src, srt in srt_paths(jobs, tag):
        if os.path.exists(srt) and not a.force:
            done += 1
            total = duration(src)
            if total and total - srt_end(srt) > SHORT:
                print(f"주의  이미 있는 자막이 음성보다 {int(total - srt_end(srt))}초 일찍 끝난다: {srt}"
                      " — 끊긴 것이면 --force 로 다시", file=sys.stderr)
            continue
        todo.append((src, srt, duration(src)))
    known = sum(d for _, _, d in todo if d)
    print(f"모델 {tag} · 받아쓸 것 {len(todo)}개 (음성 {hms(known)}) · 이미 있음 {done}개", flush=True)

    failed, spent, heard, t0 = [], 0.0, 0.0, time.time()
    try:
        for i, (src, srt, total) in enumerate(todo, 1):
            left = known - heard
            eta = f" · 남은 시간 약 {hms(left * spent / heard)}" if heard and spent else ""
            print(f"[{i}/{len(todo)}] {src}{eta}", flush=True)
            start = time.time()
            ok, why = transcribe(src, srt, model, a.language, a.threads)
            spent += time.time() - start
            heard += total or 0
            if not ok:
                failed.append((src, why))
                print(f"  실패: {why}", file=sys.stderr, flush=True)
                continue
            end = srt_end(srt)
            note = f" · 음성 {mmss(total)}" if total else ""
            print(f"  완료: {srt} — 자막 끝 {mmss(end)}{note}", flush=True)
            if total and total - end > SHORT:
                print(f"  경고: 자막이 음성보다 {int(total - end)}초 일찍 끝난다 — 끝부분을 확인할 것",
                      file=sys.stderr)
    except KeyboardInterrupt:
        print("\n멈췄다. 같은 명령을 다시 치면 끝난 것은 건너뛰고 이어서 한다.", file=sys.stderr)
        sys.exit(130)

    print(f"\n끝 — 만듦 {len(todo) - len(failed)}개 · 실패 {len(failed)}개 · 이미 있음 {done}개"
          f" · 걸린 시간 {hms(time.time() - t0)}")
    if failed:
        for src, why in failed:
            print(f"  실패  {src} — {why}", file=sys.stderr)
        if outdir:
            os.makedirs(outdir, exist_ok=True)
            with open(os.path.join(outdir, "failed.txt"), "w", encoding="utf-8") as f:
                f.writelines(f"{src}\t{why}\n" for src, why in failed)
            print(f"  목록: {os.path.join(outdir, 'failed.txt')}", file=sys.stderr)
    elif outdir and os.path.exists(os.path.join(outdir, "failed.txt")):
        os.remove(os.path.join(outdir, "failed.txt"))  # 지난 실행의 목록 — 이번엔 다 됐다
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

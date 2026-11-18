#!/usr/bin/env python3
"""강의 음성·영상을 로컬 whisper로 받아써 SRT 자막을 만든다 — 자막이 없는 강의용.

    python3 tools/transcribe.py <강의.mp3|.m4a|.mp4|…> [<파일> …]
    python3 tools/transcribe.py 강의.mp4 -l ko -o 자막폴더
    python3 tools/transcribe.py 강의.mp3 -m ~/models/ggml-large-v3-turbo-q5_0.bin

결과: <이름> (whisper).srt  — vtt_text.py · check_note.py 가 그대로 읽는다.
이미 있으면 건너뛴다 (--force 로 다시).

필요한 것 (밖으로 보내는 것 없음, 이 컴퓨터에서만 돈다):
  - whisper.cpp 의 whisper-cli  (macOS: brew install whisper-cpp)
  - ffmpeg / ffprobe            (어떤 음성·영상이든 16kHz 모노 wav로 바꾼다)
  - ggml 모델 파일 — -m, 또는 환경변수 WHISPER_MODEL, 또는 아래 MODEL_DIRS 에서 찾는다

다 만든 뒤 자막 끝 시각을 음성 길이와 비교해, 10초 넘게 모자라면 경고한다
(자동 전사는 끝부분을 놓치거나 같은 말을 되풀이하는 일이 있다 — 그 구간은 사람이 확인).
자동 전사라 숫자·용어 오인식이 있다. 인용은 대본 그대로 하고 정정은 따로 표시한다.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

from .vtt_text import parse, mmss

MODEL_DIRS = [
    "~/.cache/whisper.cpp",
    "~/.cache/whisper",
    "~/models/whisper",
]
PREFERRED = ["ggml-large-v3-turbo-q5_0.bin", "ggml-large-v3-turbo.bin", "ggml-large-v3.bin"]


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


def duration(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout
        return float(out.strip())
    except (OSError, ValueError):
        return None


def transcribe(src, model, lang, outdir, force, threads):
    stem = os.path.splitext(os.path.basename(src))[0]
    out_base = os.path.join(outdir or os.path.dirname(os.path.abspath(src)), f"{stem} (whisper)")
    srt = out_base + ".srt"
    if os.path.exists(srt) and not force:
        print(f"건너뜀 (이미 있음): {srt}")
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "audio.wav")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ar", "16000", "-ac", "1", wav])
        if r.returncode:
            print(f"실패 (ffmpeg): {src}", file=sys.stderr)
            return 1
        r = subprocess.run(["whisper-cli", "-m", model, "-f", wav, "-l", lang, "-t", str(threads),
                            "-osrt", "-of", out_base], capture_output=True, text=True)
        if r.returncode or not os.path.exists(srt):
            print(f"실패 (whisper-cli): {src}\n{r.stderr[-800:]}", file=sys.stderr)
            return 1
    cues = parse(srt)
    end = max((e for _, e, _ in cues), default=0)
    total = duration(src)
    note = f" · 음성 {mmss(total)}" if total else ""
    print(f"완료: {srt} — 큐 {len(cues)}개 · 자막 끝 {mmss(end)}{note}")
    if total and total - end > 10:
        print(f"  경고: 자막이 음성보다 {int(total - end)}초 일찍 끝난다 — 끝부분을 확인할 것", file=sys.stderr)
    return 0


def main(argv=None, prog=None):
    ap = argparse.ArgumentParser(prog=prog, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("-l", "--language", default="auto", help="ko · en · auto(기본)")
    ap.add_argument("-m", "--model")
    ap.add_argument("-o", "--outdir")
    ap.add_argument("-t", "--threads", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    for tool in ("whisper-cli", "ffmpeg"):
        if not shutil.which(tool):
            sys.exit(f"{tool} 이 없다 — 머리말의 '필요한 것' 참고")
    model = find_model(a.model)
    if not model or not os.path.exists(model):
        sys.exit("whisper 모델 파일을 못 찾았다 — -m 또는 WHISPER_MODEL 로 ggml-*.bin 경로를 줄 것")
    if a.outdir:
        os.makedirs(a.outdir, exist_ok=True)
    bad = sum(transcribe(f, model, a.language, a.outdir, a.force, a.threads) for f in a.files)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

"""lnb doctor — 바깥 프로그램과 whisper 모델이 있는지 보고, 없으면 설치법을 알린다.

빠진 것이 하나라도 있으면 종료 코드 1. 그 프로그램을 쓰는 하위 명령만 안 되고 나머지는 된다.
"""
import argparse
import importlib.util
import os
import shutil
import sys

from .transcribe import find_model, find_vad


# (이름, 찾는 법, 쓰는 하위 명령, macOS 설치, 그 밖)
PROGRAMS = [
    ("ffmpeg", "bin", "frames · transcribe · fetch --video", "brew install ffmpeg", "https://ffmpeg.org/download.html"),
    ("ffprobe", "bin", "frames · transcribe", "brew install ffmpeg (같이 깔린다)", "ffmpeg 과 같이 깔린다"),
    ("whisper-cli", "bin", "transcribe · fetch --transcribe-missing", "brew install whisper-cpp",
     "https://github.com/ggml-org/whisper.cpp"),
    ("pdftotext", "bin", "check (PDF 자료 인용 대조)", "brew install poppler", "poppler-utils 패키지"),
    ("yt-dlp", "yt_dlp", "fetch", "pipx 로 lnb 를 깔면 같이 깔린다", "pip install yt-dlp"),
    ("youtube_transcript_api", "youtube_transcript_api", "fetch (via transcript-api)",
     "pipx 로 lnb 를 깔면 같이 깔린다", "pip install youtube-transcript-api"),
]


def found(name, how):
    path = shutil.which(name)
    if path:
        return path
    if how != "bin" and importlib.util.find_spec(how):
        return f"파이썬 모듈 {how}"
    return None


def main(argv=None, prog=None):
    ap = argparse.ArgumentParser(prog=prog, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args(argv)
    missing = 0
    for name, how, used, mac, other in PROGRAMS:
        where = found(name, how)
        if where:
            print(f"OK    {name:<23} {where}")
        else:
            missing += 1
            print(f"없음  {name:<23} → {used} 가 안 된다\n      macOS: {mac} · 그 밖: {other}")
    model = find_model(None)
    if model and os.path.exists(model):
        print(f"OK    {'whisper 모델':<21} {model}")
    else:
        missing += 1
        print(f"없음  {'whisper 모델':<21} → transcribe 가 안 된다 (자막 있는 강의만 쓰면 필요 없다)\n"
              f"      받기: lnb setup   (약 574MB, 받은 뒤 SHA256 확인)\n"
              f"      다른 곳에 두었으면: export WHISPER_MODEL=<ggml-*.bin 경로>")
    vad = find_vad(None)
    if vad and os.path.exists(vad):
        print(f"OK    {'VAD 모델':<21} {vad}")
    else:
        missing += 1
        print(f"없음  {'VAD 모델':<21} → transcribe 가 VAD 없이는 --no-vad 로만 된다\n"
              f"      받기: lnb setup   (약 0.9MB, 받은 뒤 SHA256 확인)")
    print("\n모두 있다." if not missing else f"\n빠진 것 {missing}개 — 위 안내대로 깔면 된다.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

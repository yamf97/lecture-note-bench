"""lnb setup — 받아쓰기(transcribe)에 필요한 것을 준비한다.

    lnb setup            # 점검하고, 모델이 없으면 받을지 묻는다
    lnb setup --yes      # 묻지 않고 받는다 (스크립트용)

하는 일:
  - whisper-cli · ffmpeg · ffprobe 가 없으면 설치 명령을 알린다. 직접 설치하지는 않는다.
  - VAD 모델(ggml-silero-v6.2.0.bin, 약 0.9MB — 말소리 구간 찾기)도 같은 방식으로 받는다.
  - whisper 모델(ggml-large-v3-turbo-q5_0.bin, 약 574MB)이 ~/.cache/whisper.cpp/ 에 있으면
    SHA256 을 확인한다. 다르면 경고만 하고 덮어쓰지 않는다.
  - 없으면 묻고 받는다. 주소는 Hugging Face 의 한 커밋에 고정돼 있고, 받은 파일은
    크기와 SHA256 이 맞을 때만 제자리에 놓는다. 틀리면 지우고 종료 코드 1.

다른 모델을 쓰려면 받을 필요 없이 lnb transcribe -m <파일> 또는 WHISPER_MODEL.
"""
import argparse
import hashlib
import os
import shutil
import sys
import urllib.request

from .transcribe import cli_has_vad, find_model, find_vad

MODEL_NAME = "ggml-large-v3-turbo-q5_0.bin"
MODEL_COMMIT = "98aa99a0a9db05ae2342309f5096248665f7cba3"  # huggingface.co/ggerganov/whisper.cpp
MODEL_URL = f"https://huggingface.co/ggerganov/whisper.cpp/resolve/{MODEL_COMMIT}/{MODEL_NAME}"
MODEL_SHA256 = "394221709cd5ad1f40c46e6031ca61bce88931e6e088c188294c6d5a55ffa7e2"
MODEL_SIZE = 574041195
MODEL_DIR = "~/.cache/whisper.cpp"

# VAD(말소리 구간 찾기) — huggingface.co/ggml-org/whisper-vad, MIT
VAD_NAME = "ggml-silero-v6.2.0.bin"
VAD_COMMIT = "9ffd54a1e1ee413ddf265af9913beaf518d1639b"
VAD_URL = f"https://huggingface.co/ggml-org/whisper-vad/resolve/{VAD_COMMIT}/{VAD_NAME}"
VAD_SHA256 = "2aa269b785eeb53a82983a20501ddf7c1d9c48e33ab63a41391ac6c9f7fb6987"
VAD_SIZE = 885098

PROGRAMS = [("whisper-cli", "brew install whisper-cpp"),
            ("ffmpeg", "brew install ffmpeg"),
            ("ffprobe", "brew install ffmpeg (같이 깔린다)")]

CHUNK = 1 << 20


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def download(url, dest, sha256, size, out=sys.stdout):
    """url 을 dest.part 로 받고, 크기·해시가 맞을 때만 dest 로 옮긴다. 맞으면 True."""
    part = dest + ".part"
    h, got, shown = hashlib.sha256(), 0, -1
    try:
        with urllib.request.urlopen(url) as r, open(part, "wb") as f:
            for block in iter(lambda: r.read(CHUNK), b""):
                f.write(block)
                h.update(block)
                got += len(block)
                pct = got * 100 // size if size else 0
                if size >= 10 * CHUNK and pct // 10 != shown // 10:  # 작은 파일은 진행 표시 없이
                    shown = pct
                    print(f"  {got // CHUNK}MB / {size // CHUNK}MB", file=out, flush=True)
    except (OSError, ValueError) as e:
        _remove(part)
        print(f"받기 실패: {e}", file=out)
        return False
    if got != size or h.hexdigest() != sha256:
        _remove(part)
        print(f"받은 파일이 다르다 — 크기 {got} (기대 {size}) · SHA256 {h.hexdigest()} (기대 {sha256})\n"
              "지웠다. 다시 해도 같으면 받는 경로가 바뀐 것이니 lnb 를 업데이트할 것.", file=out)
        return False
    os.replace(part, dest)
    return True


def _remove(path):
    try:
        os.remove(path)
    except OSError:
        pass


def check_programs(out=sys.stdout):
    missing = 0
    for name, how in PROGRAMS:
        where = shutil.which(name)
        if where:
            print(f"OK    {name:<13} {where}", file=out)
        else:
            missing += 1
            print(f"없음  {name:<13} → {how}", file=out)
    if shutil.which("whisper-cli") and not cli_has_vad():
        missing += 1
        print("주의  whisper-cli 가 VAD(--vad)를 모르는 옛 판이다 → brew upgrade whisper-cpp", file=out)
    return missing


def ensure_model(model_dir, yes, ask=input, out=sys.stdout,
                 url=MODEL_URL, sha256=MODEL_SHA256, size=MODEL_SIZE, name=MODEL_NAME,
                 label="모델", finder=find_model):
    """표준 모델이 model_dir 에 맞는 해시로 있게 한다. 성공하면 True."""
    dest = os.path.join(os.path.expanduser(model_dir), name)
    if os.path.lexists(dest):
        if not os.path.exists(dest):
            print(f"없음  {label:<12}  {dest} 는 끊어진 링크다 — 지우고 다시 lnb setup", file=out)
            return False
        if not os.path.isfile(dest):
            print(f"주의  {label:<12}  {dest} 가 보통 파일이 아니다 (폴더 등) — 건드리지 않았다.\n"
                  "      옮기거나 지우고 다시 lnb setup.", file=out)
            return False
        print("확인  모델 SHA256 …", file=out, flush=True)
        try:
            digest = sha256_of(dest)
        except OSError as e:
            print(f"주의  {label:<12}  {dest} 를 읽지 못했다 ({e}) — 건드리지 않았다.", file=out)
            return False
        if digest == sha256:
            print(f"OK    {label:<12}  {dest} (SHA256 일치)", file=out)
            return True
        print(f"주의  {label:<12}  {dest} 의 SHA256 이 lnb 가 아는 값과 다르다.\n"
              "      덮어쓰지 않았다. 직접 받은 다른 판이면 그대로 써도 되고,\n"
              "      표준 모델로 바꾸려면 그 파일을 옮기고 다시 lnb setup.", file=out)
        return False
    other = finder(None)
    if other and os.path.exists(other):
        print(f"참고  지금 transcribe 는 {other} 를 쓴다", file=out)
    print(f"없음  {label:<12}  {dest}", file=out)
    mb = f"{size // CHUNK}MB" if size >= CHUNK else f"{size // 1024}KB"
    if not yes:
        if not sys.stdin.isatty() and ask is input:
            print(f"      받으려면 lnb setup --yes (약 {mb})", file=out)
            return False
        reply = ask(f"{label} {name} ({mb})을 Hugging Face 에서 받을까요? [y/N] ")
        if reply.strip().lower() not in ("y", "yes", "ㅇ", "네"):
            print("받지 않았다.", file=out)
            return False
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print(f"받는 중  {url}", file=out, flush=True)
    if not download(url, dest, sha256, size, out=out):
        return False
    print(f"OK    {label:<12}  {dest} (SHA256 일치)", file=out)
    return True


def main(argv=None, prog=None):
    ap = argparse.ArgumentParser(prog=prog, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-y", "--yes", action="store_true", help="모델을 묻지 않고 받는다")
    a = ap.parse_args(argv)
    missing = check_programs()
    ok = ensure_model(MODEL_DIR, a.yes)
    ok = ensure_model(MODEL_DIR, a.yes, url=VAD_URL, sha256=VAD_SHA256, size=VAD_SIZE, name=VAD_NAME,
                      label="VAD 모델", finder=find_vad) and ok
    if missing:
        print(f"\n빠진 프로그램 {missing}개 — 위 명령으로 깔고 다시 lnb setup.")
    elif ok:
        print("\n준비 끝. lnb transcribe <강의 파일> -l ko")
    return 0 if ok and not missing else 1


if __name__ == "__main__":
    sys.exit(main())

"""`lnb` 명령 — 하위 명령을 각 도구의 main(argv)로 넘긴다."""
import importlib
import sys

from . import __version__

# (하위 명령, 모듈, 언제 쓰나, 입력 → 출력, 예시)
COMMANDS = [
    ("fetch", "fetch", "강의 자막(필요하면 영상·음성)을 영상 사이트에서 받을 때",
     "재생목록·영상 주소 → 강좌 폴더의 자막·index.tsv",
     "lnb fetch --url <영상 주소> -o 강좌폴더 --video"),
    ("transcribe", "transcribe", "자막이 없는 강의를 이 컴퓨터에서 받아쓸 때 (whisper.cpp)",
     "음성·영상 파일 → <이름> (whisper).srt",
     "lnb transcribe 강의.m4a -l ko"),
    ("text", "vtt_text", "자막을 읽기 좋은 본문으로 펼칠 때",
     "자막(.vtt·.srt) → 30초 칸 [mm:ss] 문단 (--cues 면 큐마다 한 줄)",
     "lnb text 강의.vtt --cues"),
    ("frames", "frames", "판서·슬라이드 장면을 뽑을 때",
     "영상 → 장면 .jpg + index.tsv",
     "lnb frames 강의.mp4 --at 05:32,12:00"),
    ("pages", "pages", "교재·강의록 인용을 검사하려고 원문 파일을 만들 때",
     "MinerU 결과(json)·글자 층 PDF → 쪽 표시가 든 원문 md (<!-- p.68 (PDF 78) -->)",
     "lnb pages 교재_content_list.json --pdf-start 78 --offset 10 -o 원문.md"),
    ("check", "check_note", "다 쓴 노트를 검사할 때 — 인용이 자막·교재에 그대로 있나·시각·검산식",
     "노트 .md → 문제 목록 (있으면 종료 코드 1)",
     "lnb check 노트.md"),
    ("setup", "setup_env", "받아쓰기를 처음 쓸 때 — whisper 모델을 받아 해시로 확인",
     "→ whisper-cli·ffmpeg 설치 안내 + 모델(약 574MB) 받기·SHA256 확인",
     "lnb setup"),
    ("doctor", "doctor", "처음 설치했을 때·명령이 안 될 때",
     "→ 바깥 프로그램·whisper 모델 점검과 설치 안내 (빠진 게 있으면 종료 코드 1)",
     "lnb doctor"),
]

FLOW = """흐름:
  영상 주소 ─ fetch ─┬─ 자막 있음 ─────────────┬─ text(읽기본) ─ 노트 쓰기 ─ check
                     └─ 없음 → transcribe ─────┘
  영상 ─ frames(판서·슬라이드 장면) ─────────────┤
  교재 PDF ─ (MinerU 등) ─ pages(쪽 표시 원문) ──┘"""


def usage():
    lines = [f"lnb {__version__} — 강의 영상·음성·자막 → 근거를 지키는 노트 재료", "",
             "사용: lnb <하위 명령> [옵션]   (하위 명령마다 lnb <하위 명령> --help)", "", FLOW, "",
             "하위 명령:"]
    for name, _, when, io, example in COMMANDS:
        lines += [f"  {name:<11} {when}", f"  {'':<11} {io}", f"  {'':<11} 예) {example}"]
    lines += ["", "종료 코드: 0 성공 · 1 실패·문제 발견 · 2 사용법 오류 또는 차단 응답(fetch)"]
    return "\n".join(lines)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(usage())
        return 0 if argv else 2
    if argv[0] in ("-V", "--version"):
        print(__version__)
        return 0
    table = {c[0]: c[1] for c in COMMANDS}
    name = argv[0]
    if name not in table:
        print(f"모르는 하위 명령: {name}\n\n{usage()}", file=sys.stderr)
        return 2
    mod = importlib.import_module(f".{table[name]}", __package__)
    return mod.main(argv[1:], prog=f"lnb {name}") or 0  # 도구는 대개 sys.exit 로 끝난다

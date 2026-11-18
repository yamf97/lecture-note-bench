"""교재·강의록을 쪽 표시가 든 원문 md로 — `lnb check`가 교재 인용을 대조하는 파일.

    lnb pages <MinerU의 *_content_list.json> --pdf-start 78 --offset 10 -o 원문.md
    lnb pages <글자 층이 있는 교재.pdf> --first 78 --last 79 --offset 10 -o 원문.md
    (설치하지 않았으면 저장소에서 `lnb pages` 대신 `python3 tools/pages.py`)

변환기는 부르지 않는다 — 이미 만든 결과를 쪽마다 나눠 정리만 한다.
  - 스캔 교재: 먼저 MinerU 로 변환 (`mineru -p 교재.pdf -o 폴더 -s 77 -e 78`, 쪽은 0부터).
    그 폴더의 `*_content_list.json` 을 준다. `--pdf-start` = 변환한 첫 쪽의 PDF 쪽 번호(1부터)
  - 글자 층이 살아 있는 PDF: 그대로 준다. pdftotext 로 쪽마다 글자를 꺼낸다 (`--first/--last`, 1부터)
  - 상용 모델로 옮길 때는 모델에게 처음부터 아래 쪽 표시를 넣게 한다 — 이 명령은 필요 없다

결과 꼴 (쪽마다):

    <!-- p.68 (PDF 78) -->
    그 쪽의 글 …

  --offset K : 책 쪽 = PDF 쪽 − K. 책마다 실제 쪽을 보고 한 번 확인한다 (스트랭 ILA 본문은 10).
               책 쪽이 1보다 작으면(앞부분) `<!-- PDF 3 -->` 처럼 PDF 쪽만 적는다
  MinerU 가 쪽에 인쇄된 번호를 읽었으면 계산한 책 쪽과 맞춰 보고, 다르면 경고한다.

이 파일은 교재 원문이다 — 자료 폴더(git 밖)에 두고 공개 저장소에 넣지 않는다.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

SKIP = {"header", "footer", "page_header", "page_footer", "page_number", "discarded"}


def item_text(it):
    """content_list 한 덩어리의 글 — 글·수식·목록·표·그림 설명."""
    parts = []
    if it.get("text"):
        parts.append(it["text"])
    for key in ("list_items", "table_caption", "image_caption", "table_footnote", "image_footnote"):
        v = it.get(key)
        if isinstance(v, list):
            parts += [str(x) for x in v if x]
        elif v:
            parts.append(str(v))
    if it.get("table_body"):
        parts.append(re.sub(r"<[^>]+>", " ", it["table_body"]))
    return "\n".join(p.strip() for p in parts if p and p.strip())


def from_content_list(path, pdf_start):
    """{PDF 쪽: [글…]}, {PDF 쪽: 인쇄된 쪽 번호}."""
    items = json.load(open(path, encoding="utf-8"))
    pages, printed = {}, {}
    for it in items:
        pdf = int(it.get("page_idx", 0)) + pdf_start
        pages.setdefault(pdf, [])
        if it.get("type") == "page_number" and str(it.get("text", "")).strip().isdigit():
            printed[pdf] = int(str(it["text"]).strip())
        if it.get("type") in SKIP:
            continue
        t = item_text(it)
        if t:
            pages[pdf].append(t)
    return pages, printed


def from_pdf(path, first, last):
    if not shutil.which("pdftotext"):
        sys.exit("pdftotext 이 없다 — lnb doctor 참고")
    cmd = ["pdftotext", "-f", str(first)] + (["-l", str(last)] if last else []) + [path, "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"pdftotext 실패: {r.stderr.strip()[-300:]}")
    chunks = r.stdout.split("\f")
    if chunks and not chunks[-1].strip():
        chunks = chunks[:-1]
    return {first + i: [c.strip()] if c.strip() else [] for i, c in enumerate(chunks)}, {}


def marker(pdf, offset):
    book = pdf - offset
    return f"<!-- p.{book} (PDF {pdf}) -->" if book >= 1 else f"<!-- PDF {pdf} -->"


def render(pages, offset, source):
    out = [f"<!-- lnb pages: {os.path.basename(source)} · 책 쪽 = PDF 쪽 − {offset} -->", ""]
    for pdf in sorted(pages):
        out += [marker(pdf, offset), ""]
        for t in pages[pdf]:
            out += [t, ""]
    return "\n".join(out).rstrip() + "\n"


def main(argv=None, prog=None):
    ap = argparse.ArgumentParser(prog=prog, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="MinerU *_content_list.json 또는 글자 층이 있는 .pdf")
    ap.add_argument("-o", "--out", required=True, help="만들 원문 md")
    ap.add_argument("--offset", type=int, default=0, help="책 쪽 = PDF 쪽 − OFFSET (기본 0)")
    ap.add_argument("--pdf-start", type=int, default=1, help="(json) 변환한 첫 쪽의 PDF 쪽 번호, 1부터. 기본 1")
    ap.add_argument("--first", type=int, default=1, help="(pdf) 첫 PDF 쪽, 1부터")
    ap.add_argument("--last", type=int, help="(pdf) 끝 PDF 쪽")
    ap.add_argument("--force", action="store_true", help="이미 있는 결과를 덮어쓴다")
    a = ap.parse_args(argv)
    if a.pdf_start < 1 or a.first < 1 or (a.last is not None and a.last < a.first):
        ap.error("쪽 번호는 1부터, --last 는 --first 이상")
    if os.path.exists(a.out) and not a.force:
        sys.exit(f"이미 있다: {a.out} — 덮어쓰려면 --force")
    if a.source.endswith(".json"):
        pages, printed = from_content_list(a.source, a.pdf_start)
    elif a.source.lower().endswith(".pdf"):
        pages, printed = from_pdf(a.source, a.first, a.last)
    else:
        ap.error("MinerU 의 *_content_list.json 또는 .pdf 를 줄 것 (MinerU 의 .md 는 쪽 정보가 없다)")
    if not pages:
        sys.exit("쪽이 하나도 없다")
    for pdf, num in sorted(printed.items()):
        if num != pdf - a.offset:
            print(f"경고: PDF {pdf}쪽에 인쇄된 번호는 {num}인데 계산한 책 쪽은 {pdf - a.offset} — --offset 확인",
                  file=sys.stderr)
    empty = [p for p in sorted(pages) if not pages[p]]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(render(pages, a.offset, a.source))
    first, last = min(pages), max(pages)
    print(f"완료: {a.out} — PDF {first}–{last}쪽 ({len(pages)}쪽)"
          + (f" · 글 없는 쪽 {len(empty)} ({', '.join(map(str, empty[:10]))})" if empty else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

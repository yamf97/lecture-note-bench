"""회귀 시험 — 표준 라이브러리 unittest 만 쓴다.

    python3 -m unittest discover -s tests

2026-11-17 전체 검토(Codex)에서 고친 자리를 지킨다: 검산식 eval 안전화 · 100분 넘는 시각 ·
게이트웨이 키 전송 · fetch 차단 판정·재생목록 실패 · frames 파일명 충돌 · vtt_text --block.
"""
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from lnb import check_note, cli, fetch, setup_env, transcribe, vtt_text  # noqa: E402
import hashlib  # noqa: E402
import pathlib  # noqa: E402


def fake_bin(folder, name, body):
    """PATH 앞에 둘 가짜 명령 (셸 스크립트)."""
    path = os.path.join(folder, name)
    with open(path, "w") as f:
        f.write("#!/bin/sh\n" + body + "\n")
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


def quiet(fn, *args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            r = fn(*args)
        except SystemExit as e:
            r = e.code
    return r, out.getvalue() + err.getvalue()


class CheckExpr(unittest.TestCase):
    def test_normal_expressions_pass(self):
        for e in ["M([[1],[2]]) * M([[1,2,3]]) == M([[1,2,3],[2,4,6]])",
                  "F(1,3) + F(1,6) == F(1,2)", "F('1/3') * 3 == 1", "2**10 == 1024",
                  "M([[1,2],[3,4]]).T == M([[1,3],[2,4]])"]:
            self.assertIsNone(check_note.unsafe_expr(e), e)

    def test_escape_and_dos_rejected(self):
        for e in ["M.__init__.__globals__['os'].getcwd() == 0",
                  "__import__('os').system('true') == 0",
                  "'x' * (2**29) == 0", "[0] * 10**9 == 0",
                  "2**2**2**2**2 == 0", "2**100000 == 0",
                  "F('1e999999999') == 0", "True == 1",
                  "(lambda: 1)() == 1"]:
            self.assertIsNotNone(check_note.unsafe_expr(e), e)
            self.assertTrue(check_note.check_expr(e).startswith("계산 불가"), e)


class Timestamps(unittest.TestCase):
    def test_coordinate_over_100_minutes(self):
        self.assertEqual(vtt_text.mmss(6000), "100:00")
        m = re.search(check_note.COORD, "[Vision 00 100:00]")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("t"), "100:00")
        self.assertIsNotNone(check_note.TIME_TOKEN.search("(100:00)"))

    def test_block_must_be_positive(self):
        with tempfile.NamedTemporaryFile("w", suffix=".vtt", delete=False) as f:
            f.write("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nhello\n")
        try:
            for bad in ("0", "-5"):
                code, msg = quiet(vtt_text.main, [f.name, "--block", bad])
                self.assertEqual(code, 2)
                self.assertIn("--block", msg)
        finally:
            os.unlink(f.name)


class Gateway(unittest.TestCase):
    def test_unknown_host_sends_no_key(self):
        import run_gateway
        old = (run_gateway._BASE, run_gateway._KEY_ENV)
        try:
            run_gateway._BASE, run_gateway._KEY_ENV = "https://attacker.example/v1", None
            with self.assertRaises(SystemExit) as cm:
                run_gateway.key()
            self.assertIn("--key-env", str(cm.exception.code))
        finally:
            run_gateway._BASE, run_gateway._KEY_ENV = old

    def test_crlf_separator(self):
        import run_gateway
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, newline="") as f:
            f.write("meta\r\n=====\r\nBODY\r\n===== \r\ntail\r\n")
        try:
            self.assertEqual(run_gateway.prompt_body(f.name).strip(), "BODY")
        finally:
            os.unlink(f.name)


class Fetch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.bin = os.path.join(self.tmp, "bin")
        os.mkdir(self.bin)
        self.old_path = os.environ["PATH"]
        os.environ["PATH"] = self.bin + os.pathsep + self.old_path

    def tearDown(self):
        os.environ["PATH"] = self.old_path
        shutil.rmtree(self.tmp)

    def course(self):
        folder = os.path.join(self.tmp, "course")
        os.mkdir(folder)
        with open(os.path.join(folder, "fetch.json"), "w") as f:
            json.dump({"playlist": "https://example.invalid/list", "via": "yt-dlp"}, f)
        return folder

    def test_playlist_failure_writes_no_index(self):
        fake_bin(self.bin, "yt-dlp", "echo 'network down' >&2; exit 1")
        folder = self.course()
        code, _ = quiet(fetch.main, [folder])
        self.assertEqual(code, 1)
        self.assertFalse(os.path.exists(os.path.join(folder, "index.tsv")))

    def test_playlist_block_stops_with_2(self):
        fake_bin(self.bin, "yt-dlp", "echo 'HTTP Error 429: Too Many Requests' >&2; exit 1")
        folder = self.course()
        code, _ = quiet(fetch.main, [folder])
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(os.path.join(folder, "index.tsv")))

    def test_transcript_api_block_wins_over_no_transcript(self):
        fake_bin(self.bin, "youtube_transcript_api",
                 "echo 'Could not retrieve a transcript ... RequestBlocked' >&2; exit 0")
        out = os.path.join(self.tmp, "x.txt")
        self.assertEqual(fetch.get_transcript_api("abc", ["en"], "t", "s", out), "blocked")
        fake_bin(self.bin, "youtube_transcript_api", "echo 'RequestBlocked' >&2; exit 0")
        self.assertEqual(fetch.get_transcript_api("abc", ["en"], "t", "s", out), "blocked")

    def fake_ytdlp(self, video_blocked=False, meta_blocked=False):
        """인자를 보고 흉내 내는 가짜 yt-dlp. 부른 인자는 calls.log 에 한 줄씩 남긴다."""
        log = os.path.join(self.tmp, "calls.log")
        path = os.path.join(self.bin, "yt-dlp")
        with open(path, "w") as f:
            f.write(f"""#!{sys.executable}
import sys
a = sys.argv[1:]
open({log!r}, "a").write(" ".join(a) + "\\n")
if "--flat-playlist" in a:
    print("1\\tid1\\t60\\tRobotics 1"); print("2\\tid2\\t60\\tRobotics 2"); sys.exit(0)
if "--write-subs" in a:
    o = a[a.index("-o") + 1]
    open(o.replace("%(ext)s", "en.vtt"), "w").write("WEBVTT\\n\\n00:00:01.000 --> 00:00:02.000\\nhi\\n"); sys.exit(0)
if "--print" in a:
    if {meta_blocked!r}:
        sys.stderr.write("ERROR: Sign in to confirm you're not a bot\\n"); sys.exit(1)
    print("id1\\tRobotics 1"); sys.exit(0)
if "-f" in a:
    if {video_blocked!r}:
        sys.stderr.write("ERROR: HTTP Error 429: Too Many Requests\\n"); sys.exit(1)
    o = a[a.index("-o") + 1]
    open(o.replace("%(ext)s", "mp4"), "w").write("x"); sys.exit(0)
sys.exit(1)
""")
        os.chmod(path, 0o755)
        return log

    def test_title_with_bot_is_not_a_block(self):
        self.fake_ytdlp()
        folder = self.course()
        code, _ = quiet(fetch.main, [folder, "--max", "0"])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists(os.path.join(folder, "index.tsv")))

    def test_course_video_block_stops_before_next_lecture(self):
        log = self.fake_ytdlp(video_blocked=True)
        folder = self.course()
        code, _ = quiet(fetch.main, [folder, "--video", "--max", "2"])
        self.assertEqual(code, 2)
        self.assertNotIn("id2", open(log).read())   # 둘째 강의는 요청하지 않았다

    def test_single_metadata_block_is_2(self):
        self.fake_ytdlp(meta_blocked=True)
        code, _ = quiet(fetch.main, ["--url", "https://example.invalid/v", "-o", self.tmp])
        self.assertEqual(code, 2)

    def test_single_video_block_is_2(self):
        self.fake_ytdlp(video_blocked=True)
        fake_bin(self.bin, "youtube_transcript_api", "echo 'Could not retrieve a transcript' >&2; exit 0")
        code, _ = quiet(fetch.main, ["--url", "https://example.invalid/v", "-o", self.tmp, "--video"])
        self.assertEqual(code, 2)

    def test_tool_prefers_path_binary(self):
        fake_bin(self.bin, "yt-dlp", "exit 0")
        self.assertEqual(fetch.tool("yt-dlp", "yt_dlp"), ["yt-dlp"])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg 없음")
class Frames(unittest.TestCase):
    def test_same_second_names_do_not_collide(self):
        from lnb import frames
        tmp = tempfile.mkdtemp()
        try:
            video = os.path.join(tmp, "v.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=duration=3:size=160x120:rate=10",
                            "-pix_fmt", "yuv420p", video], check=True)
            out = os.path.join(tmp, "f")
            code, _ = quiet(frames.main, [video, "-o", out, "--at", "00:01.1,00:01.9"])
            self.assertIn(code, (0, None))
            jpgs = sorted(n for n in os.listdir(out) if n.endswith(".jpg"))
            self.assertEqual(jpgs, ["00-01.jpg", "00-01_1.jpg"])
        finally:
            shutil.rmtree(tmp)


class Books(unittest.TestCase):
    """교재 인용 — lnb pages 로 만든 쪽 표시 원문 md 와 대조 (지어낸 문장만 쓴다)."""

    SOURCE = """<!-- lnb pages: test · 책 쪽 = PDF 쪽 − 10 -->

<!-- p.5 (PDF 15) -->

The dot product of x and y is the sum of numbers $x_iy_i$ . We write it as a row times a col-
umn without any dot.

<!-- p.6 (PDF 16) -->

A symmetric matrix equals its transpose. Its inverse is also symmetric when it exists.
"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp, "book.md")
        with open(self.src, "w", encoding="utf-8") as f:
            f.write(self.SOURCE)
        check_note._book_cache.clear()
        self.old = dict(check_note.CONFIG)
        check_note.CONFIG["books"] = {"Test Book": self.src}

    def tearDown(self):
        check_note.CONFIG.clear()
        check_note.CONFIG.update(self.old)
        shutil.rmtree(self.tmp)

    def run_note(self, body):
        n, fails = {}, []
        check_note.check_books(body, n, fails)
        return n, fails

    def test_quote_with_math_and_hyphen_passes(self):
        n, fails = self.run_note('"The dot product of $x$ and $y$ is the sum of numbers $x_iy_i$. '
                                 'We write it as a row times a column" `Test Book §1.1 p.5`')
        self.assertEqual((n["교재"], fails), (1, []))

    def test_changed_word_fails(self):
        _, fails = self.run_note('"The dot product of $x$ and $y$ is the product of numbers" `Test Book p.5`')
        self.assertEqual(len(fails), 1)
        self.assertIn("그대로 없다", fails[0][1])

    def test_wrong_page_points_to_right_one(self):
        _, fails = self.run_note('"A symmetric matrix equals its transpose." `Test Book p.5`')
        self.assertIn("p.6에 있다", fails[0][1])

    def test_quote_running_onto_next_page_and_ranges(self):
        n, fails = self.run_note('"without any dot. A symmetric matrix equals" `Test Book p.5`\n'
                                 '"Its inverse is also symmetric" `Test Book pp.5–6`')
        self.assertEqual((n["교재"], fails), (2, []))

    def test_ellipsis_parts_in_order(self):
        _, fails = self.run_note('"The dot product of … row times a column" `Test Book p.5`')
        self.assertEqual(fails, [])
        _, fails = self.run_note('"row times a column … The dot product of" `Test Book p.5`')
        self.assertEqual(len(fails), 1)

    def test_repeated_middle_piece_backtracks(self):
        # 「numbers」가 두 번 나온다: 첫 번째 뒤 8단어 안에는 「without any dot」이 없고, 두 번째 뒤에는 있다
        with open(self.src, "w", encoding="utf-8") as f:
            f.write("<!-- p.5 (PDF 15) -->\nStart here. Then numbers one two three four five six seven eight nine ten "
                    "eleven. Later numbers $n$ without any dot at all.\n")
        check_note._book_cache.clear()
        _, fails = self.run_note('"Start here. … numbers $x$ without any dot" `Test Book p.5`')
        self.assertEqual(fails, [])
        _, fails = self.run_note('"Start here. … numbers $x$ with a dot" `Test Book p.5`')
        self.assertEqual(len(fails), 1)

    def test_korean_source_after_long_english(self):
        with open(self.src, "w", encoding="utf-8") as f:
            f.write("<!-- p.5 (PDF 15) -->\n" + "word " * 300 + "\n대칭 행렬은 전치해도 그대로인 행렬이다.\n")
        check_note._book_cache.clear()
        n, fails = self.run_note('"대칭 행렬은 전치해도 그대로인 행렬이다" `Test Book p.5`')
        self.assertEqual((n["교재"], fails), (1, []))

    def test_config_without_books_clears_books(self):
        cfg = os.path.join(self.tmp, "check_note.json")
        with open(cfg, "w") as f:
            json.dump({"lectures": {}}, f)
        check_note.load_config(cfg)
        self.assertEqual(check_note.CONFIG["books"], {})

    def test_not_checkable_is_not_a_pass(self):
        n, fails = self.run_note('"외적 $xy^\\\\top$ 은 행렬이다" `Test Book p.5`\n'      # 번역
                                 '"$A^\\\\top$ equals" `Test Book p.6`\n'                 # 단어 너무 적음
                                 '"Some sentence on a page we did not convert" `Test Book p.99`\n'
                                 '"A symmetric matrix equals its transpose." `Test Book §2.4`')   # 쪽 없음
        self.assertEqual((n["교재"], n["교재 대조 불가"], fails), (0, 4, []))


class Pages(unittest.TestCase):
    def test_content_list_to_page_marked_md(self):
        from lnb import pages
        tmp = tempfile.mkdtemp()
        try:
            src = os.path.join(tmp, "x_content_list.json")
            with open(src, "w") as f:
                json.dump([{"type": "page_number", "text": "5", "page_idx": "0"},
                           {"type": "header", "text": "Chapter 1", "page_idx": "0"},
                           {"type": "text", "text": "First page words.", "page_idx": "0"},
                           {"type": "equation", "text": "$$\na = b\n$$", "page_idx": "1"},
                           {"type": "text", "text": "Second page words.", "page_idx": "1"}], f)
            out = os.path.join(tmp, "book.md")
            code, msg = quiet(pages.main, [src, "--pdf-start", "15", "--offset", "10", "-o", out])
            self.assertIn(code, (0, None))
            md = open(out, encoding="utf-8").read()
            self.assertIn("<!-- p.5 (PDF 15) -->\n\nFirst page words.", md)
            self.assertIn("<!-- p.6 (PDF 16) -->", md)
            self.assertNotIn("Chapter 1", md)          # 머리글은 뺀다
            self.assertNotIn("경고", msg)               # 인쇄된 5 = 15 − 10
            code, msg = quiet(pages.main, [src, "--pdf-start", "15", "--offset", "9", "-o", out, "--force"])
            self.assertIn("--offset 확인", msg)
            code, _ = quiet(pages.main, [src, "-o", out])  # 덮어쓰기는 --force 로만
            self.assertNotIn(code, (0, None))
        finally:
            shutil.rmtree(tmp)


class Cli(unittest.TestCase):
    def test_help_lists_all_commands(self):
        code, out = quiet(cli.main, ["--help"])
        self.assertEqual(code, 0)
        for name in ("fetch", "transcribe", "text", "frames", "check", "setup", "doctor"):
            self.assertIn(f"  {name} ", out)

    def test_usage_errors(self):
        self.assertEqual(quiet(cli.main, [])[0], 2)
        self.assertEqual(quiet(cli.main, ["bogus"])[0], 2)

    def test_check_help_shows_config_schema(self):
        code, out = quiet(cli.main, ["check", "--help"])
        self.assertEqual(code, 0)
        self.assertIn("check_note.json", out)
        self.assertIn('"lectures"', out)

    def test_installed_lnb_finds_repo_lectures_via_config(self):
        # 설치본처럼 저장소 기준 lectures/ 를 못 쓰게 막고(LECTURES_DIR=없는 곳), 저장소 뿌리에서 lnb check 를 부른다
        env = dict(os.environ, LECTURES_DIR=os.path.join(ROOT, "no-such-dir"),
                   PYTHONPATH=os.path.join(ROOT, "src"))
        r = subprocess.run([sys.executable, "-m", "lnb", "check", "experiments/results/E.md"],
                           cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertRegex(r.stdout, r"ok .*E\.md — 인용 [1-9]")

    def test_subcommand_gets_prog_name(self):
        code, out = quiet(cli.main, ["text", "--help"])
        self.assertEqual(code, 0)
        self.assertIn("usage: lnb text", out)


class Setup(unittest.TestCase):
    """lnb setup — 실제 574MB 대신 작은 가짜 모델을 file:// 로 받는다."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.src = os.path.join(self.tmp, "src.bin")
        with open(self.src, "wb") as f:
            f.write(b"fake model " * 1000)
        self.sha = hashlib.sha256(open(self.src, "rb").read()).hexdigest()
        self.size = os.path.getsize(self.src)
        self.url = pathlib.Path(self.src).as_uri()
        self.dir = os.path.join(self.tmp, "models")
        self.dest = os.path.join(self.dir, "m.bin")
        os.environ.pop("WHISPER_MODEL", None)

    def run_ensure(self, yes=True, reply="y", sha=None, size=None):
        out = io.StringIO()
        ok = setup_env.ensure_model(self.dir, yes, ask=lambda _: reply, out=out, url=self.url,
                                    sha256=sha or self.sha, size=size or self.size, name="m.bin")
        return ok, out.getvalue()

    def test_download_with_matching_hash(self):
        ok, out = self.run_ensure()
        self.assertTrue(ok, out)
        self.assertEqual(open(self.dest, "rb").read(), open(self.src, "rb").read())
        self.assertFalse(os.path.exists(self.dest + ".part"))

    def test_wrong_hash_leaves_nothing(self):
        ok, out = self.run_ensure(sha="0" * 64)
        self.assertFalse(ok)
        self.assertIn("다르다", out)
        self.assertEqual(os.listdir(self.dir), [])

    def test_wrong_size_leaves_nothing(self):
        ok, _ = self.run_ensure(size=self.size + 1)
        self.assertFalse(ok)
        self.assertEqual(os.listdir(self.dir), [])

    def test_declined_downloads_nothing(self):
        ok, out = self.run_ensure(yes=False, reply="n")
        self.assertFalse(ok)
        self.assertFalse(os.path.exists(self.dest))

    def test_existing_good_model_is_kept(self):
        self.assertTrue(self.run_ensure()[0])
        os.remove(self.src)  # 다시 받으려 하면 실패한다
        ok, out = self.run_ensure()
        self.assertTrue(ok)
        self.assertIn("SHA256 일치", out)

    def test_existing_other_model_is_not_overwritten(self):
        os.makedirs(self.dir)
        with open(self.dest, "wb") as f:
            f.write(b"someone else's model")
        ok, out = self.run_ensure()
        self.assertFalse(ok)
        self.assertIn("덮어쓰지 않았다", out)
        self.assertEqual(open(self.dest, "rb").read(), b"someone else's model")

    def test_broken_link_is_reported(self):
        os.makedirs(self.dir)
        os.symlink(os.path.join(self.tmp, "gone.bin"), self.dest)
        ok, out = self.run_ensure()
        self.assertFalse(ok)
        self.assertIn("끊어진 링크", out)

    def test_directory_at_destination_is_reported_not_crashed(self):
        os.makedirs(self.dest)
        ok, out = self.run_ensure()
        self.assertFalse(ok)
        self.assertIn("보통 파일이 아니다", out)
        self.assertTrue(os.path.isdir(self.dest))

    def test_unreadable_model_is_reported_not_crashed(self):
        os.makedirs(self.dir)
        with open(self.dest, "wb") as f:
            f.write(b"x")
        os.chmod(self.dest, 0)
        self.addCleanup(os.chmod, self.dest, 0o644)
        if os.access(self.dest, os.R_OK):
            self.skipTest("root 는 권한을 무시한다")
        ok, out = self.run_ensure()
        self.assertFalse(ok)
        self.assertIn("읽지 못했다", out)

    def test_pinned_url_names_commit_and_file(self):
        self.assertIn("/resolve/" + setup_env.MODEL_COMMIT + "/", setup_env.MODEL_URL)
        self.assertTrue(setup_env.MODEL_URL.endswith(setup_env.MODEL_NAME))
        self.assertRegex(setup_env.MODEL_SHA256, r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()


WHISPER_OK = """of=""
while [ $# -gt 0 ]; do [ "$1" = "-of" ] && of="$2"; shift; done
printf '1\\n00:00:00,000 --> 00:00:05,000\\nhello\\n\\n' > "$of.srt\""""
WHISPER_FAIL = """of=""
while [ $# -gt 0 ]; do [ "$1" = "-of" ] && of="$2"; shift; done
printf 'half' > "$of.srt"; echo 'boom' >&2; exit 1"""


class Transcribe(unittest.TestCase):
    """lnb transcribe — ffmpeg·ffprobe·whisper-cli 는 가짜 셸 스크립트."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.bin = os.path.join(self.tmp, "bin")
        os.mkdir(self.bin)
        old = os.environ["PATH"]
        os.environ["PATH"] = self.bin + os.pathsep + old
        self.addCleanup(os.environ.__setitem__, "PATH", old)
        fake_bin(self.bin, "ffmpeg", 'for a; do last="$a"; done; : > "$last"')
        fake_bin(self.bin, "ffprobe", "echo 5.0")
        fake_bin(self.bin, "whisper-cli", WHISPER_OK)
        self.model = os.path.join(self.tmp, "ggml-tiny.bin")
        open(self.model, "w").close()
        self.lec = os.path.join(self.tmp, "강의")
        for rel in ("물리/1강.mp4", "화학/1강.mp4", "화학/메모.txt", ".숨김/2강.mp4"):
            path = os.path.join(self.lec, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").close()
        self.out = os.path.join(self.tmp, "자막")

    def run_tr(self, *args, model=None):
        return quiet(transcribe.main, [*args, "-m", model or self.model])

    def srts(self):
        found = []
        for root, _, files in os.walk(self.out):
            found += [os.path.relpath(os.path.join(root, f), self.out) for f in files]
        return sorted(found)

    def test_folder_mirrors_tree_with_model_name(self):
        code, out = self.run_tr(self.lec, "-o", self.out)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.srts(), ["물리/1강 (whisper tiny).srt", "화학/1강 (whisper tiny).srt"])
        self.assertEqual(os.listdir(os.path.join(self.lec, "물리")), ["1강.mp4"])  # 원본 폴더는 그대로

    def test_same_stem_different_ext_do_not_collide(self):
        open(os.path.join(self.lec, "물리", "1강.m4a"), "w").close()
        code, out = self.run_tr(os.path.join(self.lec, "물리"), "-o", self.out)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.srts(), ["1강.m4a (whisper tiny).srt", "1강.mp4 (whisper tiny).srt"])
        code, out = self.run_tr(os.path.join(self.lec, "물리"), "-o", self.out)
        self.assertIn("이미 있음 2개", out)

    def test_unresolvable_name_clash_stops(self):
        for n in ("1강.m4a", "1강.mp4.m4a"):
            open(os.path.join(self.lec, "물리", n), "w").close()
        code, out = self.run_tr(os.path.join(self.lec, "물리"), "-o", self.out)
        self.assertIn("자막 이름이 겹쳐", str(code))  # sys.exit(문구) — 문구가 종료 코드로 온다
        self.assertEqual(self.srts(), [])

    def test_same_file_twice_runs_once(self):
        f = os.path.join(self.lec, "물리", "1강.mp4")
        code, out = self.run_tr(f, f, "-o", self.out)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.srts(), ["1강 (whisper tiny).srt"])
        self.assertIn("받아쓸 것 1개", out)

    def test_rerun_skips_existing(self):
        self.run_tr(self.lec, "-o", self.out)
        fake_bin(self.bin, "whisper-cli", "exit 1")  # 다시 받아쓰면 실패한다
        code, out = self.run_tr(self.lec, "-o", self.out)
        self.assertEqual(code, 0, out)
        self.assertIn("받아쓸 것 0개", out)
        self.assertIn("이미 있음 2개", out)

    def test_other_model_adds_file_and_keeps_old(self):
        self.run_tr(self.lec, "-o", self.out)
        other = os.path.join(self.tmp, "ggml-large-v9.bin")
        open(other, "w").close()
        code, out = self.run_tr(self.lec, "-o", self.out, model=other)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.srts(), ["물리/1강 (whisper large-v9).srt", "물리/1강 (whisper tiny).srt",
                                       "화학/1강 (whisper large-v9).srt", "화학/1강 (whisper tiny).srt"])

    def test_failure_leaves_no_partial_and_lists_it(self):
        fake_bin(self.bin, "whisper-cli", WHISPER_FAIL)
        code, out = self.run_tr(self.lec, "-o", self.out)
        self.assertEqual(code, 1)
        self.assertEqual(self.srts(), ["failed.txt"])
        with open(os.path.join(self.out, "failed.txt"), encoding="utf-8") as f:
            lines = f.read().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("boom", lines[0])

    def test_success_removes_stale_failed_list(self):
        os.makedirs(self.out)
        with open(os.path.join(self.out, "failed.txt"), "w") as f:
            f.write("old\n")
        code, out = self.run_tr(self.lec, "-o", self.out)
        self.assertEqual(code, 0, out)
        self.assertNotIn("failed.txt", self.srts())

    def test_single_file_without_outdir_goes_next_to_it(self):
        src = os.path.join(self.lec, "물리", "1강.mp4")
        code, out = self.run_tr(src)
        self.assertEqual(code, 0, out)
        self.assertTrue(os.path.exists(os.path.join(self.lec, "물리", "1강 (whisper tiny).srt")))

    def test_short_existing_srt_warns(self):
        fake_bin(self.bin, "ffprobe", "echo 60.0")  # 음성 60초, 자막은 5초에서 끝난다
        self.run_tr(self.lec, "-o", self.out)
        code, out = self.run_tr(self.lec, "-o", self.out)
        self.assertEqual(code, 0, out)
        self.assertIn("일찍 끝난다", out)

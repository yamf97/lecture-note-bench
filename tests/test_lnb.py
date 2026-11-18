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

from lnb import check_note, cli, fetch, vtt_text  # noqa: E402


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


class Cli(unittest.TestCase):
    def test_help_lists_all_commands(self):
        code, out = quiet(cli.main, ["--help"])
        self.assertEqual(code, 0)
        for name in ("fetch", "transcribe", "text", "frames", "check", "doctor"):
            self.assertIn(f"  {name} ", out)

    def test_usage_errors(self):
        self.assertEqual(quiet(cli.main, [])[0], 2)
        self.assertEqual(quiet(cli.main, ["bogus"])[0], 2)

    def test_subcommand_gets_prog_name(self):
        code, out = quiet(cli.main, ["text", "--help"])
        self.assertEqual(code, 0)
        self.assertIn("usage: lnb text", out)


if __name__ == "__main__":
    unittest.main()

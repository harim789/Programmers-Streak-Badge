import datetime as dt
import subprocess
import tempfile
import unicodedata
import unittest
from pathlib import Path

import collect
from stats import KST

PG = ["프로그래머스"]


class ProblemIdTest(unittest.TestCase):
    def test_level_layout(self):
        self.assertEqual(collect.problem_id("프로그래머스/1/12954. x만큼 간격이 있는 n개의 숫자/README.md", PG),
                         "프로그래머스:12954")

    def test_language_layout(self):
        self.assertEqual(collect.problem_id("Python/프로그래머스/0/181839. 주사위 게임 1/solution.py", PG),
                         "프로그래머스:181839")

    def test_other_platform_ignored(self):
        self.assertIsNone(collect.problem_id("백준/Bronze/1000. A＋B/README.md", PG))
        self.assertIsNone(collect.problem_id("codetree/foo/README.md", PG))

    def test_nfd_path(self):
        p = unicodedata.normalize("NFD", "프로그래머스/1/131705. 삼총사/README.md")
        self.assertEqual(collect.problem_id(p, PG), "프로그래머스:131705")

    def test_multiple_platforms(self):
        dirs = ["프로그래머스", "백준"]
        self.assertEqual(collect.problem_id("백준/Bronze/1000. A＋B/README.md", dirs), "백준:1000")


class ReadmeDateTest(unittest.TestCase):
    def test_zero_padded(self):
        text = "### 채점결과\n\n정확성: 100.0\n\n### 제출 일자\n\n2026년 07월 01일 15:20:33\n\n### 문제 설명\n"
        self.assertEqual(collect.parse_submitted(text), dt.datetime(2026, 7, 1, 15, 20, 33, tzinfo=KST))

    def test_unpadded(self):
        text = "### 제출 일자\n\n2026년 11월 9일 21:14:03\n"
        self.assertEqual(collect.parse_submitted(text), dt.datetime(2026, 11, 9, 21, 14, 3, tzinfo=KST))

    def test_missing(self):
        self.assertIsNone(collect.parse_submitted("### 문제 설명\n\n2026년 07월 01일 15:20:33"))


class GitLogTest(unittest.TestCase):
    LOG = (
        "\x002026-11-05T05:42:56+09:00\n\n프로그래머스/1/131705. 삼총사/README.md\n"
        "프로그래머스/1/131705. 삼총사/삼총사.py\n"
        "\x002026-11-04T19:29:19+09:00\n\ncodetree/x/README.md\n"
        "\x002026-09-11T04:27:59+09:00\n\n프로그래머스/1/136798. 기사단원의 무기/README.md\n"
        "\x002026-09-11T04:25:58+09:00\n\n프로그래머스/1/136798. 기사단원의 무기/README.md\n"
    )

    def test_parse(self):
        got = collect.parse_git_log(self.LOG, PG)
        self.assertEqual(set(got), {"프로그래머스:131705", "프로그래머스:136798"})
        self.assertEqual(len(got["프로그래머스:131705"]), 1)   # 한 커밋의 여러 파일은 1회
        self.assertEqual(len(got["프로그래머스:136798"]), 2)

    def test_merge_prefers_readme_and_counts_resubmits(self):
        r = {"p:1": dt.datetime(2026, 7, 1, 15, 20, 33, tzinfo=KST)}
        c = {"p:1": [dt.datetime(2026, 6, 30, 23, 0, tzinfo=KST), dt.datetime(2026, 7, 1, 15, 20, 36, tzinfo=KST)],
             "p:2": [dt.datetime(2026, 7, 2, 10, 0, tzinfo=KST), dt.datetime(2026, 7, 3, 10, 0, tzinfo=KST)]}
        with_re = collect.merge_events(r, c, count_resubmits=True)
        self.assertEqual(len(with_re), 5)
        without = collect.merge_events(r, c, count_resubmits=False)
        self.assertEqual(without, [("p:1", r["p:1"]), ("p:2", c["p:2"][0])])


class CollectRepoTest(unittest.TestCase):
    """실제 git 저장소를 만들어 끝까지 돌려본다."""

    def git(self, *args, date=None):
        env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@t", "HOME": self.dir, "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"}
        if date:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
        subprocess.run(["git", "-C", self.dir, *args], check=True, capture_output=True, env=env)

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name
        self.git("init", "-q")

    def tearDown(self):
        self._tmp.cleanup()

    def add(self, rel, text, date):
        p = Path(self.dir, rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "c", date=date)

    def test_end_to_end(self):
        self.add("프로그래머스/1/1. 가/README.md", "### 제출 일자\n\n2026년 11월 08일 23:59:00\n",
                 "2026-11-08T23:59:05+09:00")
        self.add("프로그래머스/1/2. 나/sol.py", "print(1)", "2026-11-09T15:00:00+00:00")   # KST 11/10 00:00
        self.add("백준/Bronze/3. 다/README.md", "x", "2026-11-09T12:00:00+09:00")
        ev = collect.collect(Path(self.dir), PG)
        dates = sorted({e[1].astimezone(KST).date() for e in ev})
        self.assertEqual(dates, [dt.date(2026, 11, 8), dt.date(2026, 11, 10)])
        self.assertEqual({e[0] for e in ev}, {"프로그래머스:1", "프로그래머스:2"})


if __name__ == "__main__":
    unittest.main()

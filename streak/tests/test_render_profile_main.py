import datetime as dt
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

import main
import profile as pg_profile
import render
from stats import compute

TODAY = dt.date(2026, 11, 9)


class OrdinalTest(unittest.TestCase):
    def test_suffixes(self):
        cases = {1: "st", 2: "nd", 3: "rd", 4: "th", 11: "th", 12: "th", 13: "th",
                 21: "st", 22: "nd", 101: "st", 111: "th", 112: "th", 187654: "th", 3201: "st"}
        for n, suf in cases.items():
            with self.subTest(n=n):
                self.assertEqual(render.ordinal(n), suf)


class RenderTest(unittest.TestCase):
    def svg(self, counts, **kw):
        start = min(counts) if counts else TODAY
        return render.render(counts, TODAY, start, compute(counts, TODAY), **kw)

    def test_singular_day(self):
        out = self.svg({TODAY: 1})
        self.assertIn(">day in a row<", out)
        self.assertIn(">1 day</tspan>", out)
        self.assertIn(">1 SOLVED TODAY<", out)
        self.assertIn("Day 2 tomorrow.", out)

    def test_today_count_in_pill(self):
        out = self.svg({TODAY - dt.timedelta(days=1): 3, TODAY: 12})
        self.assertIn(">12 SOLVED TODAY<", out)

    def test_zero_pending(self):
        out = self.svg({})
        self.assertIn(">days in a row<", out)
        self.assertIn("NOT YET TODAY", out)
        self.assertIn("Solve one today to start.", out)

    def test_pending_message(self):
        c = {TODAY - dt.timedelta(days=i): 1 for i in range(1, 28)}
        self.assertIn("Solve one today for Day 28.", self.svg(c))

    def test_missing_values_render_dash_without_unit(self):
        out = self.svg({TODAY: 1}, score=None, rank=None, solved=None)
        self.assertEqual(out.count(">—</text>"), 3)
        self.assertNotIn(">pts<", out)
        self.assertNotIn(">problems<", out)

    def test_numbers_formatted(self):
        out = self.svg({TODAY: 1}, score=98765, rank=187654, solved=1284)
        for s in ("98,765", "187,654", ">th<", "1,284"):
            self.assertIn(s, out)

    def test_self_contained(self):
        out = self.svg({TODAY: 1}, score=1, rank=1, solved=1)
        self.assertNotIn("http://", out.replace('xmlns="http://www.w3.org/2000/svg"', ""))
        self.assertNotIn("https://", out)
        self.assertNotIn("<script", out)
        self.assertIn("data:font/woff2;base64,", out)

    def test_numbers_not_animated(self):
        out = self.svg({})
        # 깜빡임(.p)은 모래시계와 오늘 링 두 곳에만
        self.assertEqual(out.count('class="p"'), 2)


class ProfileTest(unittest.TestCase):
    def test_parse(self):
        p = pg_profile.parse_record({"ranking": {"score": 2450, "rank": 3201}, "codingTest": {"solved": 442}})
        self.assertEqual(p.as_dict(), {"score": 2450, "rank": 3201, "solved": 442})

    def test_parse_partial(self):
        p = pg_profile.parse_record({"ranking": {"score": 10}})
        self.assertEqual(p.as_dict(), {"score": 10, "rank": None, "solved": None})

    def test_parse_missing_keys(self):
        with self.assertRaises(pg_profile.FetchError):
            pg_profile.parse_record({"foo": 1})

    def test_http_error_hides_body(self):
        err = urllib.error.HTTPError(pg_profile.SIGN_IN, 401, "no", {}, None)
        with mock.patch("urllib.request.urlopen", side_effect=err):
            with self.assertRaises(pg_profile.FetchError) as cm:
                pg_profile.fetch("me@example.com", "secret-pw")
        self.assertNotIn("secret-pw", str(cm.exception))
        self.assertIn("401", str(cm.exception))

    def test_timeout(self):
        with mock.patch("urllib.request.urlopen", side_effect=TimeoutError()):
            with self.assertRaises(pg_profile.FetchError):
                pg_profile.fetch("a", "b")


class MainCacheTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.patches = [mock.patch.object(main, "DATA", root / "data"),
                        mock.patch.object(main, "OUT", root / "assets" / "badge.svg"),
                        mock.patch.object(main, "ROOT", root)]
        for p in self.patches:
            p.start()
        self.root = root

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self._tmp.cleanup()

    def env(self, **kw):
        base = {"ALGO_REPO": "me/algo", "ALGO_PATH": str(self.root / "nope"),
                "STREAK_NOW": "2026-11-09T03:00:00+00:00"}
        base.update(kw)
        return mock.patch.dict(os.environ, base, clear=True)

    def seed(self, owner_repo="me/algo", pg_id="me@example.com"):
        owner = {"algo_repo": owner_repo, "programmers_id_sha256_12": main.id_hash(pg_id)}
        main.DATA.mkdir(parents=True, exist_ok=True)
        (main.DATA / "profile.json").write_text(json.dumps(
            {"owner": owner, "fetched_at": "x", "score": 2450, "rank": 3201, "solved": 442}))

    def test_missing_algo_repo_fails_clearly(self):
        with self.env(ALGO_REPO=""), mock.patch("sys.stderr") as err:
            self.assertEqual(main.main(), 1)
        self.assertIn("README 5단계", "".join(str(c) for c in err.write.call_args_list))

    def test_login_failure_uses_cache(self):
        self.seed()
        with self.env(PROGRAMMERS_ID="me@example.com", PROGRAMMERS_PW="pw"), \
                mock.patch.object(pg_profile, "fetch", side_effect=pg_profile.FetchError("x")):
            self.assertEqual(main.main(), 0)
        self.assertIn("2,450", main.OUT.read_text())

    def test_other_owner_cache_ignored(self):
        self.seed(owner_repo="me/algo")
        with self.env(ALGO_REPO="someone/else", PROGRAMMERS_ID="them@example.com", PROGRAMMERS_PW="pw"), \
                mock.patch.object(pg_profile, "fetch", side_effect=pg_profile.FetchError("x")):
            self.assertEqual(main.main(), 0)
        out = main.OUT.read_text()
        self.assertNotIn("2,450", out)
        self.assertEqual(out.count(">—</text>"), 3)

    def test_no_credentials_ignores_owner_cache(self):
        self.seed()
        with self.env():
            self.assertEqual(main.main(), 0)
        self.assertNotIn("2,450", main.OUT.read_text())

    def test_solves_cache_owner_checked(self):
        main.DATA.mkdir(parents=True, exist_ok=True)
        (main.DATA / "solves.json").write_text(json.dumps(
            {"owner": {"algo_repo": "me/algo"}, "events": [["p:1", "2026-11-09T10:00:00+09:00"]]}))
        with self.env(ALGO_REPO="someone/else"):
            main.main()
        self.assertIn(">0<tspan", main.OUT.read_text())
        with self.env():
            main.main()
        self.assertIn(">1<tspan", main.OUT.read_text())

    def test_profile_cache_not_rewritten_when_unchanged(self):
        self.seed()
        before = (main.DATA / "profile.json").read_text()
        p = pg_profile.Profile(2450, 3201, 442)
        with self.env(PROGRAMMERS_ID="me@example.com", PROGRAMMERS_PW="pw"), \
                mock.patch.object(pg_profile, "fetch", return_value=p):
            main.main()
        self.assertEqual((main.DATA / "profile.json").read_text(), before)

    def test_svg_written_only_when_changed(self):
        with self.env():
            main.main()
            m1 = main.OUT.stat().st_mtime_ns
            main.main()
        self.assertEqual(main.OUT.stat().st_mtime_ns, m1)


if __name__ == "__main__":
    unittest.main()

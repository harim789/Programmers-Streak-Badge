import datetime as dt
import unittest

import stats
from stats import KST, compute, daily_counts, today_kst

D = dt.date
UTC = dt.timezone.utc


def days(*ds):
    return {d: 1 for d in ds}


def run(end: dt.date, n: int):
    return {end - dt.timedelta(days=i): 1 for i in range(n)}


class StreakTest(unittest.TestCase):
    today = D(2026, 11, 9)

    def test_no_records(self):
        s = compute({}, self.today)
        self.assertEqual((s.current, s.longest, s.status), (0, 0, "pending"))

    def test_only_today(self):
        s = compute(days(self.today), self.today)
        self.assertEqual((s.current, s.longest, s.status), (1, 1, "done"))

    def test_five_until_yesterday_pending_today(self):
        s = compute(run(self.today - dt.timedelta(days=1), 5), self.today)
        self.assertEqual((s.current, s.status), (5, "pending"))

    def test_missed_yesterday_is_zero(self):
        s = compute(run(self.today - dt.timedelta(days=2), 5), self.today)
        self.assertEqual((s.current, s.longest, s.status), (0, 5, "pending"))

    def test_month_boundary(self):
        c = days(D(2026, 10, 30), D(2026, 10, 31), D(2026, 11, 1))
        self.assertEqual(compute(c, D(2026, 11, 1)).current, 3)

    def test_year_boundary(self):
        c = days(D(2026, 12, 30), D(2026, 12, 31), D(2027, 1, 1), D(2027, 1, 2))
        s = compute(c, D(2027, 1, 2))
        self.assertEqual((s.current, s.longest), (4, 4))

    def test_leap_day(self):
        c = days(D(2028, 2, 28), D(2028, 2, 29), D(2028, 3, 1))
        self.assertEqual(compute(c, D(2028, 3, 1)).current, 3)

    def test_longest_equals_current(self):
        c = {**run(self.today, 7), **run(self.today - dt.timedelta(days=20), 3)}
        s = compute(c, self.today)
        self.assertEqual((s.current, s.longest), (7, 7))

    def test_longest_differs_from_current(self):
        c = {**run(self.today, 2), **run(self.today - dt.timedelta(days=30), 10)}
        s = compute(c, self.today)
        self.assertEqual((s.current, s.longest), (2, 10))

    def test_future_days_ignored(self):
        c = run(self.today + dt.timedelta(days=5), 3)
        self.assertEqual(compute(c, self.today).longest, 0)


class TimezoneTest(unittest.TestCase):
    def test_utc_1459_is_same_kst_day(self):
        self.assertEqual(today_kst(dt.datetime(2026, 11, 9, 14, 59, 59, tzinfo=UTC)), D(2026, 11, 9))

    def test_utc_1500_is_next_kst_day(self):
        self.assertEqual(today_kst(dt.datetime(2026, 11, 9, 15, 0, 0, tzinfo=UTC)), D(2026, 11, 10))

    def test_event_dates_convert_to_kst(self):
        ev = [("a", dt.datetime(2026, 11, 9, 14, 59, tzinfo=UTC)),
              ("b", dt.datetime(2026, 11, 9, 15, 0, tzinfo=UTC))]
        self.assertEqual(daily_counts(ev), {D(2026, 11, 9): 1, D(2026, 11, 10): 1})

    def test_streak_survives_until_kst_midnight(self):
        c = run(D(2026, 11, 9), 3)          # 11/7~11/9 풀었고 11/10은 아직
        before = today_kst(dt.datetime(2026, 11, 9, 14, 59, tzinfo=UTC))
        after = today_kst(dt.datetime(2026, 11, 9, 15, 0, tzinfo=UTC))
        self.assertEqual((compute(c, before).current, compute(c, before).status), (3, "done"))
        self.assertEqual((compute(c, after).current, compute(c, after).status), (3, "pending"))

    def test_naive_now_rejected(self):
        with self.assertRaises(ValueError):
            today_kst(dt.datetime(2026, 11, 9))

    def test_naive_event_treated_as_kst(self):
        self.assertEqual(stats.to_kst_date(dt.datetime(2026, 11, 9, 23, 30)), D(2026, 11, 9))


class DailyCountsTest(unittest.TestCase):
    def test_same_problem_same_day_counted_once(self):
        t = dt.datetime(2026, 11, 9, 10, tzinfo=KST)
        ev = [("p:1", t), ("p:1", t + dt.timedelta(hours=3)), ("p:2", t)]
        self.assertEqual(daily_counts(ev), {D(2026, 11, 9): 2})

    def test_same_problem_different_days(self):
        t = dt.datetime(2026, 11, 9, 10, tzinfo=KST)
        ev = [("p:1", t), ("p:1", t + dt.timedelta(days=1))]
        self.assertEqual(daily_counts(ev), {D(2026, 11, 9): 1, D(2026, 11, 10): 1})


if __name__ == "__main__":
    unittest.main()

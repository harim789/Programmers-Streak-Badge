"""스트릭 계산 — 순수 함수만. "오늘"은 항상 인자로 주입받는다 (KST 날짜)."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

KST = dt.timezone(dt.timedelta(hours=9), "KST")
ONE_DAY = dt.timedelta(days=1)


def to_kst_date(moment: dt.datetime) -> dt.date:
    """시각 → KST 날짜. tz 정보가 없는 시각은 KST로 간주한다."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=KST)
    return moment.astimezone(KST).date()


def today_kst(now: dt.datetime) -> dt.date:
    """주입받은 현재 시각(보통 UTC)으로 KST 기준 오늘 날짜를 구한다."""
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    return now.astimezone(KST).date()


@dataclass(frozen=True)
class Stats:
    current: int        # 현재 연속 일수
    longest: int        # 최장 연속 일수
    done_today: bool    # 오늘 풀었는지

    @property
    def status(self) -> str:
        return "done" if self.done_today else "pending"


def current_streak(counts: dict[dt.date, int], today: dt.date) -> int:
    """오늘 풀었으면 오늘부터, 아직이면 어제부터 거꾸로 센다 (자정 전까지는 끊긴 게 아님)."""
    d = today if counts.get(today, 0) > 0 else today - ONE_DAY
    n = 0
    while counts.get(d, 0) > 0:
        n += 1
        d -= ONE_DAY
    return n


def longest_streak(counts: dict[dt.date, int], today: dt.date) -> int:
    """기록이 있는 날들 중(오늘 이후 제외) 가장 긴 연속 구간."""
    days = sorted(d for d, n in counts.items() if n > 0 and d <= today)
    best = run = 0
    prev = None
    for d in days:
        run = run + 1 if prev is not None and d - prev == ONE_DAY else 1
        best = max(best, run)
        prev = d
    return best


def compute(counts: dict[dt.date, int], today: dt.date) -> Stats:
    return Stats(
        current=current_streak(counts, today),
        longest=longest_streak(counts, today),
        done_today=counts.get(today, 0) > 0,
    )


def daily_counts(events: list[tuple[str, dt.datetime]]) -> dict[dt.date, int]:
    """(문제 ID, 풀이 시각) 목록 → KST 날짜별 '서로 다른 문제 수'."""
    per_day: dict[dt.date, set[str]] = {}
    for pid, moment in events:
        per_day.setdefault(to_kst_date(moment), set()).add(pid)
    return {d: len(p) for d, p in per_day.items()}

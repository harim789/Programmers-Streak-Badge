"""수집 → 계산 → 렌더. GitHub Actions에서 `python streak/main.py`로 실행한다.

설정은 전부 환경변수(저장소 변수 / Secrets)로만 받는다.
  ALGO_REPO        (필수) 백준허브 저장소 owner/name — 캐시 소유자 식별에도 쓰임
  ALGO_PATH        체크아웃 경로 (기본 algo)
  PLATFORM_DIRS    쉼표 구분 플랫폼 폴더 (기본 프로그래머스)
  COUNT_RESUBMITS  재제출 커밋도 활동으로 인정 (기본 true)
  PROGRAMMERS_ID / PROGRAMMERS_PW  (선택) 없으면 Stats는 캐시 또는 '—'
  STREAK_NOW       (테스트용) ISO 시각. 없으면 현재 UTC 시각
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import collect  # noqa: E402
import profile as pg_profile  # noqa: E402
import render  # noqa: E402
import stats  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "streak" / "data"
OUT = ROOT / "assets" / "programmers-streak.svg"


def log(msg: str) -> None:
    print(f"[streak] {msg}", flush=True)


def id_hash(pg_id: str | None) -> str | None:
    return hashlib.sha256(pg_id.strip().lower().encode()).hexdigest()[:12] if pg_id else None


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def write_json_if_changed(path: Path, data: dict, ignore: tuple[str, ...] = ()) -> bool:
    """`ignore` 키를 뺀 내용이 같으면 쓰지 않는다 (커밋 노이즈 방지)."""
    old = read_json(path)
    strip = lambda d: {k: v for k, v in (d or {}).items() if k not in ignore}  # noqa: E731
    if old is not None and strip(old) == strip(data):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return True


# ───────────── 프로필 (Score / Rank / Solved) ─────────────
def load_profile(owner: dict, pg_id: str | None, pg_pw: str | None, now: dt.datetime) -> dict:
    """새로 받아오고, 실패하면 소유자가 같은 캐시로, 캐시도 없으면 전부 None."""
    path = DATA / "profile.json"
    if pg_id and pg_pw:
        try:
            p = pg_profile.fetch(pg_id, pg_pw)
            log("programmers record: fetched")
            write_json_if_changed(path, {"owner": owner, "fetched_at": now.isoformat(timespec="seconds"),
                                         **p.as_dict()}, ignore=("fetched_at",))
            return p.as_dict()
        except pg_profile.FetchError as e:
            log(f"programmers record: {e} — using cache")
    else:
        log("programmers record: PROGRAMMERS_ID/PROGRAMMERS_PW not set — skipped")
    cached = read_json(path)
    if cached and cached.get("owner") == owner:
        return {k: cached.get(k) for k in ("score", "rank", "solved")}
    if cached:
        log("programmers record: cache belongs to another owner — ignored")
    return {"score": None, "rank": None, "solved": None}


# ───────────── 풀이 기록 ─────────────
def load_events(owner: dict, algo: Path, platform_dirs: list[str], resubmits: bool):
    path = DATA / "solves.json"
    if (algo / ".git").exists():
        events = collect.collect(algo, platform_dirs, resubmits)
        log(f"solves: {len(events)} events from {len(platform_dirs)} platform dir(s)")
        write_json_if_changed(path, {"owner": owner,
                                     "events": [[pid, t.isoformat()] for pid, t in events]})
        return events
    log("solves: algorithm repo not checked out — using cache")
    cached = read_json(path)
    if cached and cached.get("owner") == owner:
        return [(pid, dt.datetime.fromisoformat(t)) for pid, t in cached.get("events", [])]
    return []


def main() -> int:
    algo_repo = os.environ.get("ALGO_REPO", "").strip()
    if not algo_repo:
        print("::error::ALGO_REPO 변수를 등록하세요 — README 5단계", file=sys.stderr)
        return 1
    algo = Path(os.environ.get("ALGO_PATH", "algo"))
    if not algo.is_absolute():
        algo = ROOT / algo
    platform_dirs = [d.strip() for d in os.environ.get("PLATFORM_DIRS", "").split(",") if d.strip()] or ["프로그래머스"]
    resubmits = os.environ.get("COUNT_RESUBMITS", "true").strip().lower() not in ("0", "false", "no")
    pg_id = os.environ.get("PROGRAMMERS_ID", "").strip() or None
    pg_pw = os.environ.get("PROGRAMMERS_PW", "") or None

    now = (dt.datetime.fromisoformat(os.environ["STREAK_NOW"]) if os.environ.get("STREAK_NOW")
           else dt.datetime.now(dt.timezone.utc))
    today = stats.today_kst(now)

    solves_owner = {"algo_repo": algo_repo.lower()}
    profile_owner = {"algo_repo": algo_repo.lower(), "programmers_id_sha256_12": id_hash(pg_id)}

    events = load_events(solves_owner, algo, platform_dirs, resubmits)
    counts = stats.daily_counts(events)
    start = min(counts) if counts else today
    s = stats.compute(counts, today)
    log(f"today={today} current={s.current} longest={s.longest} status={s.status}")

    rec = load_profile(profile_owner, pg_id, pg_pw, now)
    svg = render.render(counts, today, start, s, **rec)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists() and OUT.read_text(encoding="utf-8") == svg:
        log("badge unchanged")
    else:
        OUT.write_text(svg, encoding="utf-8")
        log(f"badge written: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""백준허브 저장소의 git 기록 → 풀이 이벤트 (문제 ID, 풀이 시각).

우선순위
1. 문제 폴더 README.md의 `제출 일자` (예: `2026년 07월 01일 15:20:33`, KST)
2. README에 없으면 그 문제 경로를 바꾼 커밋의 author date
3. 재제출 커밋도 그날의 활동으로 인정 (count_resubmits=True)
"""
from __future__ import annotations

import datetime as dt
import re
import subprocess
import unicodedata
from pathlib import Path

from stats import KST

PROBLEM_DIR = re.compile(r"^(\d+)\.\s")
SUBMITTED = re.compile(
    r"###\s*제출\s*일자\s*\n+\s*(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일\s*(\d{1,2}):(\d{2})(?::(\d{2}))?"
)


def problem_id(path: str, platform_dirs: list[str]) -> str | None:
    """경로에서 `<플랫폼>/…/<숫자>. <제목>/…`의 문제 ID를 꺼낸다. 플랫폼 폴더 밖이면 None."""
    parts = unicodedata.normalize("NFC", path).split("/")
    dirs = {unicodedata.normalize("NFC", p) for p in platform_dirs}
    for i, part in enumerate(parts):
        if part in dirs:
            for sub in parts[i + 1:]:
                m = PROBLEM_DIR.match(sub)
                if m:
                    return f"{part}:{m.group(1)}"
            return None
    return None


def parse_submitted(readme_text: str) -> dt.datetime | None:
    m = SUBMITTED.search(readme_text)
    if not m:
        return None
    y, mo, d, h, mi, s = m.groups()
    try:
        return dt.datetime(int(y), int(mo), int(d), int(h), int(mi), int(s or 0), tzinfo=KST)
    except ValueError:
        return None


def parse_git_log(output: str, platform_dirs: list[str]) -> dict[str, list[dt.datetime]]:
    """`git log --format=%x00%aI --name-only` 출력 → {문제 ID: [커밋 시각…]}."""
    result: dict[str, list[dt.datetime]] = {}
    for chunk in output.split("\x00"):
        lines = [ln for ln in chunk.splitlines() if ln.strip()]
        if not lines:
            continue
        try:
            when = dt.datetime.fromisoformat(lines[0].strip())
        except ValueError:
            continue
        pids = {pid for f in lines[1:] if (pid := problem_id(f.strip(), platform_dirs))}
        for pid in pids:
            result.setdefault(pid, []).append(when)
    return result


def git_log(repo: Path) -> str:
    return subprocess.run(
        ["git", "-c", "core.quotepath=off", "-C", str(repo), "log",
         "--format=%x00%aI", "--name-only", "--no-renames"],
        check=True, capture_output=True, text=True, encoding="utf-8",
    ).stdout


def readme_dates(repo: Path, platform_dirs: list[str]) -> dict[str, dt.datetime]:
    """작업 트리의 문제 README에서 `제출 일자`를 읽는다 (마지막 제출 시각)."""
    out: dict[str, dt.datetime] = {}
    for pdir in platform_dirs:
        base = repo / pdir
        if not base.is_dir():
            continue
        for readme in base.rglob("README.md"):
            pid = problem_id(readme.relative_to(repo).as_posix(), platform_dirs)
            if not pid:
                continue
            when = parse_submitted(readme.read_text(encoding="utf-8", errors="replace"))
            if when and (pid not in out or when > out[pid]):
                out[pid] = when
    return out


def merge_events(readmes: dict[str, dt.datetime], commits: dict[str, list[dt.datetime]],
                 count_resubmits: bool = True) -> list[tuple[str, dt.datetime]]:
    """README 날짜와 커밋 날짜를 합쳐 이벤트 목록을 만든다 (시간순, 중복 제거)."""
    events: set[tuple[str, dt.datetime]] = set()
    for pid in set(readmes) | set(commits):
        times = sorted(commits.get(pid, []))
        if pid in readmes:
            events.add((pid, readmes[pid]))
        elif times:
            events.add((pid, times[0]))
        if count_resubmits:
            events.update((pid, t) for t in times)
    return sorted(events, key=lambda e: (e[1], e[0]))


def collect(repo: Path, platform_dirs: list[str], count_resubmits: bool = True) -> list[tuple[str, dt.datetime]]:
    commits = parse_git_log(git_log(repo), platform_dirs)
    return merge_events(readme_dates(repo, platform_dirs), commits, count_resubmits)

"""프로그래머스 기록(Score / Rank / Solved) 수집.

공개 API가 없어서 웹사이트가 내부적으로 쓰는 주소를 사용한다 (비공식, 언제든 바뀔 수 있음).
  1) POST /api/v1/account/sign-in  → set-cookie 수집
  2) GET  /api/v1/users/record     → ranking.score, ranking.rank, codingTest.solved

보안: 비밀번호·쿠키·응답 본문·헤더는 절대 출력하지 않는다. 실패 사유도 상태 코드/예외 종류만 남긴다.
실패하면 None을 돌려주고, 호출자(main.py)가 캐시값으로 대체한다.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass

SIGN_IN = "https://programmers.co.kr/api/v1/account/sign-in"
RECORD = "https://programmers.co.kr/api/v1/users/record"
TIMEOUT = 10
UA = "programmers-streak-badge (+https://github.com)"


@dataclass(frozen=True)
class Profile:
    score: int | None
    rank: int | None
    solved: int | None

    def as_dict(self) -> dict:
        return {"score": self.score, "rank": self.rank, "solved": self.solved}


class FetchError(Exception):
    """사유만 담는다 (민감한 값은 담지 않음)."""


def _int_or_none(v) -> int | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, str) and v.replace(",", "").strip().isdigit():
        return int(v.replace(",", "").strip())
    return None


def parse_record(data: dict) -> Profile:
    """users/record 응답 JSON → Profile. 세 값이 모두 없으면 FetchError."""
    if not isinstance(data, dict):
        raise FetchError("unexpected response shape")
    ranking = data.get("ranking") if isinstance(data.get("ranking"), dict) else {}
    coding = data.get("codingTest") if isinstance(data.get("codingTest"), dict) else {}
    p = Profile(_int_or_none(ranking.get("score")), _int_or_none(ranking.get("rank")),
                _int_or_none(coding.get("solved")))
    if p.score is None and p.rank is None and p.solved is None:
        raise FetchError("expected keys missing (ranking.score / ranking.rank / codingTest.solved)")
    return p


def _cookies(headers) -> str:
    return "; ".join(c.split(";", 1)[0].strip() for c in (headers.get_all("Set-Cookie") or []))


def _request_record(email: str, password: str) -> dict:
    body = json.dumps({"user": {"email": email, "password": password}}).encode()
    req = urllib.request.Request(SIGN_IN, data=body, method="POST", headers={
        "Content-Type": "application/json", "Accept": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            cookie = _cookies(resp.headers)
    except urllib.error.HTTPError as e:
        raise FetchError(f"sign-in failed (HTTP {e.code})") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise FetchError(f"sign-in failed ({type(e).__name__})") from None
    if not cookie:
        raise FetchError("sign-in returned no session cookie")

    req = urllib.request.Request(RECORD, headers={
        "Cookie": cookie, "Accept": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise FetchError(f"record request failed (HTTP {e.code})") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise FetchError(f"record request failed ({type(e).__name__})") from None
    try:
        return json.loads(raw)
    except ValueError:
        raise FetchError("record response is not JSON") from None


def fetch(email: str, password: str) -> Profile:
    """로그인 1회 + 조회 1회. 실패하면 FetchError."""
    return parse_record(_request_record(email, password))


def key_tree(obj, prefix: str = "") -> list[str]:
    """값 없이 키 구조만 (처음 1회 응답 구조 확인용)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            out.append(f"{path}: {type(v).__name__}")
            out += key_tree(v, path)
    elif isinstance(obj, list) and obj:
        out += key_tree(obj[0], prefix + "[0]")
    return out


if __name__ == "__main__":
    # 로컬 점검용: PROGRAMMERS_ID / PROGRAMMERS_PW 환경변수로 실행하면 키 구조만 출력한다 (값은 출력 안 함).
    import os
    try:
        data = _request_record(os.environ["PROGRAMMERS_ID"], os.environ["PROGRAMMERS_PW"])
    except KeyError:
        sys.exit("PROGRAMMERS_ID / PROGRAMMERS_PW 환경변수가 필요합니다.")
    except FetchError as e:
        sys.exit(f"실패: {e}")
    print("\n".join(key_tree(data)))
    try:
        p = parse_record(data)
        print("parsed:", {k: ("ok" if v is not None else "missing") for k, v in p.as_dict().items()})
    except FetchError as e:
        print("parse failed:", e)

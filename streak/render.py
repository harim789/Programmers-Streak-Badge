"""SVG 렌더러 — design/render_mockup.py(v4 "Glass / Magenta, 2단")의 render()를 그대로 옮긴 것.

표준 라이브러리만 사용. 폰트(streak/fonts/*.woff2, SIL OFL)는 base64로 내장한다.
외부 리소스·스크립트 없음 (GitHub README의 <img>에서도 그대로 보이도록).
"""
from __future__ import annotations

import base64
import datetime as dt
from functools import lru_cache
from pathlib import Path

from stats import Stats

FONTS = Path(__file__).parent / "fonts"
W, H = 860, 446

# ───────────── 색 ─────────────
BG_TOP, BG_BOTTOM = "#3A1442", "#22092A"
GLOW_PINK, GLOW_VIOLET, ORB = "#E39AD0", "#8E4BC4", "#9B3A9A"
WHITE = "#FFFFFF"
GLASS_FILL, GLASS_STROKE = 0.07, 0.40
MISSED = "#FFC27A"
LEVELS = [("#F2A6DA", .30), ("#F2A6DA", .58), ("#F7C6EA", .85), ("#FFFFFF", 1.0)]  # 1, 2, 3-4, 5+
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

SANS = "'Hanken', 'Helvetica Neue', Arial, sans-serif"
SERIF = "'InstrumentItalic', Georgia, 'Times New Roman', serif"

WEEKS, CELL, GAP = 16, 15, 5
STEP = CELL + GAP


@lru_cache(maxsize=1)
def _font_face() -> str:
    def b64(name):
        return base64.b64encode((FONTS / name).read_bytes()).decode()
    return (
        f"@font-face{{font-family:'Hanken';font-weight:400;src:url(data:font/woff2;base64,{b64('hanken-400.woff2')}) format('woff2')}}"
        f"@font-face{{font-family:'Hanken';font-weight:600;src:url(data:font/woff2;base64,{b64('hanken-600.woff2')}) format('woff2')}}"
        f"@font-face{{font-family:'InstrumentItalic';font-style:italic;src:url(data:font/woff2;base64,{b64('instrument-italic.woff2')}) format('woff2')}}"
    )


def level_of(n: int) -> int:
    return 0 if n <= 0 else 1 if n == 1 else 2 if n == 2 else 3 if n <= 4 else 4


def ordinal(n: int) -> str:
    """영어 서수 접미사: 1st 2nd 3rd 4th … 11th 12th 13th … 21st … 101st 111th 112th."""
    if 11 <= n % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def fmt(n) -> str:
    return f"{n:,}" if isinstance(n, int) else "—"


def plural(n: int, word: str) -> str:
    return word if n == 1 else word + "s"


def message(cur: int, done: bool) -> str:
    if done:
        return f"Day {cur + 1} tomorrow."
    if cur:
        return f"Solve one today for Day {cur + 1}."
    return "Solve one today to start."


# ───────────── 조각 ─────────────
def glass(x, y, w, h, r) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{WHITE}" fill-opacity="{GLASS_FILL}" '
            f'stroke="{WHITE}" stroke-opacity="{GLASS_STROKE}" stroke-width="1"/>')


def panel(x, y, w, h, r) -> str:
    """가독성을 위해 어두운 틴트 + 흰 유리 + 흰 테두리를 겹친다."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#14041C" fill-opacity=".30"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{WHITE}" fill-opacity=".07" '
            f'stroke="{WHITE}" stroke-opacity=".45" stroke-width="1"/>')


def mark(cx, cy) -> str:
    """오리지널 심볼: 위로 피어오르는 3갈래 불꽃 선."""
    return (f'<g transform="translate({cx-9},{cy-10})" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-linecap="round">'
            '<path d="M9 19c-4 0-6-2.6-6-5.6 0-3.4 3-5 3-8.4 2 1.2 3 3 3 5 .6-2.4 2.4-4.4 2.4-8 2.6 2 4.6 5.4 4.6 9.6 0 4.2-2.6 7.4-7 7.4z"/>'
            '<path d="M9 19c-1.6 0-2.6-1.1-2.6-2.6 0-1.6 1.3-2.4 1.6-4 .9.8 1.4 1.8 1.4 2.8.5-.7 1-1.5 1-2.6 1 .9 1.6 2.2 1.6 3.6 0 1.6-1.2 2.8-3 2.8z"/>'
            '</g>')


def icon_done(cx, cy) -> str:
    """오늘 완료: 체크 원."""
    return (f'<g transform="translate({cx-8.4},{cy-8.4}) scale(.7)" fill="none" stroke="{WHITE}" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="9.5"/><path d="M7.8 12.4l2.9 2.9 5.6-6"/></g>')


def icon_pending(cx, cy) -> str:
    """오늘 아직: 모래시계. 천천히 깜빡임."""
    return (f'<g class="p" transform="translate({cx-8.4},{cy-8.4}) scale(.7)" fill="none" stroke="{WHITE}" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M4.5 2.5h15M4.5 21.5h15"/>'
            '<path d="M6 2.5c0 4.6 6 6 6 9.5 0-3.5 6-4.9 6-9.5"/>'
            '<path d="M6 21.5c0-4.6 6-6 6-9.5 0 3.5 6 4.9 6 9.5"/>'
            f'<path d="M8.6 19.8h6.8L12 16.6z" fill="{WHITE}" stroke-width="1.2"/></g>')


# ───────────── 본체 ─────────────
def render(counts: dict[dt.date, int], today: dt.date, start: dt.date, stats: Stats,
           score: int | None = None, rank: int | None = None, solved: int | None = None) -> str:
    """counts: KST 날짜별 푼 문제 수 / start: 기록 시작일 / score·rank·solved: None이면 '—'."""
    cur, done, best = stats.current, stats.done_today, stats.longest

    o: list[str] = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
      f'aria-label="Programmers: score {fmt(score)}, rank {fmt(rank)}, {fmt(solved)} solved, {cur}-day streak">')
    a(f'<title>Programmers — score {fmt(score)} · rank {fmt(rank)} · {fmt(solved)} solved · {cur}-day streak (best {best})</title>')
    a('<defs>'
      f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/></linearGradient>'
      f'<radialGradient id="orb" cx=".45" cy=".35" r=".6"><stop offset="0" stop-color="#C45BB8"/><stop offset=".7" stop-color="{ORB}"/><stop offset="1" stop-color="#5E1D63"/></radialGradient>'
      '<filter id="b60" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'
      '<filter id="b18" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>'
      '<filter id="ts" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#2A0830" flood-opacity=".6"/></filter>'
      '<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#10031A" stop-opacity=".55"/></radialGradient>'
      f'<clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
      '</defs>')
    a('<style>' + _font_face() +
      f'.s{{font-family:{SANS}}}.i{{font-family:{SERIF};font-style:italic}}.up{{letter-spacing:.14em}}'
      '.f{animation:f 7s ease-in-out infinite}@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}'
      '.p{animation:p 2.2s ease-in-out infinite}@keyframes p{0%,100%{opacity:1}50%{opacity:.3}}'
      '@media (prefers-reduced-motion:reduce){.f,.p{animation:none}}'
      '</style>')

    # ── 배경 ──
    a('<g clip-path="url(#card)">')
    a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    a(f'<ellipse cx="190" cy="220" rx="240" ry="200" fill="{GLOW_PINK}" opacity=".55" filter="url(#b60)"/>')
    a(f'<ellipse cx="700" cy="300" rx="230" ry="200" fill="{GLOW_VIOLET}" opacity=".55" filter="url(#b60)"/>')
    a(f'<g class="f"><circle cx="520" cy="120" r="120" fill="url(#orb)" opacity=".75" filter="url(#b18)"/>'
      f'<ellipse cx="492" cy="84" rx="40" ry="26" fill="#F2B8E4" opacity=".25" filter="url(#b18)"/></g>')
    for x, y, r, op in ((150, 60, 2.2, .35), (705, 54, 3, .25), (846, 240, 1.8, .3), (14, 300, 1.6, .25)):
        a(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" opacity="{op}"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    a('</g>')
    a(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{WHITE}" stroke-opacity=".14"/>')

    # ── 상단 바 ──
    a(glass(220, 22, 420, 44, 22))
    a(f'<text x="246" y="49.5" class="s" font-size="17" fill="{WHITE}">programmers</text>')
    a(f'<line x1="358" y1="32" x2="358" y2="56" stroke="{WHITE}" stroke-opacity=".55"/>')
    a(mark(380, 44))
    a(f'<text x="614" y="49" class="s up" font-size="12.5" font-weight="600" fill="{WHITE}" text-anchor="end">DAILY STREAK</text>')

    top, bot = 86, H - 28
    ph = bot - top

    # ═════ 왼쪽: 기록 블록 ═════
    lx, lw = 28, 292
    a(panel(lx, top, lw, ph, 22))
    a(f'<rect x="{lx+20}" y="{top+18}" width="100" height="32" rx="16" fill="{WHITE}" fill-opacity=".14" stroke="{WHITE}" stroke-opacity=".65"/>')
    for dx, dy in ((0, 0), (6, 0), (0, 6), (6, 6)):
        a(f'<circle cx="{lx+37+dx}" cy="{top+31+dy}" r="1.9" fill="{WHITE}"/>')
    a(f'<text x="{lx+56}" y="{top+39.5}" class="s" font-size="15" font-weight="600" fill="{WHITE}">Stats</text>')
    rows = [("Score", score, "pts"),
            ("Rank", rank, ordinal(rank) if rank is not None else ""),
            ("Solved", solved, "problems")]
    a('<g filter="url(#ts)">')
    for i, (k, val, unit) in enumerate(rows):
        u = unit if val is not None else ""
        y = top + 70 + i * 86
        if i:
            a(f'<line x1="{lx+28}" y1="{y-6}" x2="{lx+lw-28}" y2="{y-6}" stroke="{WHITE}" stroke-opacity=".18"/>')
        a(f'<text x="{lx+28}" y="{y+22}" class="s" font-size="15" fill="{WHITE}" fill-opacity=".82">{k}</text>')
        a(f'<text x="{lx+28}" y="{y+66}" class="s" font-size="44" font-weight="600" letter-spacing="-1" fill="{WHITE}">{fmt(val)}'
          + (f'<tspan class="i" font-size="22" font-weight="400" letter-spacing="0" dx="7" fill-opacity=".85">{u}</tspan>' if u else '')
          + '</text>')
    a('</g>')

    # ═════ 오른쪽: 스트릭 문구 + 잔디 ═════
    rx0, rw = 336, W - 28 - 336
    a(panel(rx0, top, rw, ph, 22))
    ix = rx0 + 24
    label = f"{counts.get(today, 0)} SOLVED TODAY" if done else "NOT YET TODAY"
    sw = 50 + len(label) * 9.4
    sx = rx0 + rw - 20 - sw
    a(f'<rect x="{sx}" y="{top+18}" width="{sw:g}" height="32" rx="16" fill="{WHITE}" fill-opacity=".10" stroke="{WHITE}" stroke-opacity=".5"/>')
    a((icon_done if done else icon_pending)(sx + 22, top + 34))
    a(f'<text x="{sx+38:g}" y="{top+38.5}" class="s up" font-size="12.5" font-weight="600" fill="{WHITE}">{label}</text>')
    a('<g filter="url(#ts)">')
    a(f'<text x="{ix}" y="{top+44}" class="s" font-size="15" fill="{WHITE}" fill-opacity=".82">Current streak</text>')
    a(f'<text x="{ix}" y="{top+94}" class="s" font-size="50" font-weight="600" letter-spacing="-1.5" fill="{WHITE}">{cur}'
      f'<tspan class="i" font-size="32" font-weight="400" letter-spacing="0" dx="8">{plural(cur, "day")} in a row</tspan></text>')
    a('</g>')
    a(f'<text x="{ix}" y="{top+124}" class="s" font-size="14" fill="{WHITE}" fill-opacity=".82">Best streak '
      f'<tspan font-weight="600" fill-opacity="1">{best} {plural(best, "day")}</tspan></text>')
    a(f'<text x="{rx0+rw-24}" y="{top+125}" class="i" font-size="18" fill="{WHITE}" text-anchor="end">{message(cur, done)}</text>')

    # 잔디
    gx0 = ix + 34
    gy0 = top + 166
    a(f'<line x1="{ix}" y1="{top+140}" x2="{rx0+rw-24}" y2="{top+140}" stroke="{WHITE}" stroke-opacity=".18"/>')
    last_monday = today - dt.timedelta(days=today.weekday())
    first_monday = last_monday - dt.timedelta(weeks=WEEKS - 1)
    for r, lab in ((0, "Mon"), (2, "Wed"), (4, "Fri"), (6, "Sun")):
        a(f'<text x="{gx0-10}" y="{gy0 + r*STEP + 12}" class="s" font-size="11.5" fill="{WHITE}" fill-opacity=".75" text-anchor="end">{lab}</text>')
    prev = None
    for w in range(WEEKS):
        d0 = first_monday + dt.timedelta(weeks=w)
        if d0.month != prev:
            if prev is not None:
                a(f'<text x="{gx0 + w*STEP}" y="{gy0-8}" class="s" font-size="11.5" fill="{WHITE}" fill-opacity=".75">{MONTHS[d0.month-1]}</text>')
            prev = d0.month
    for w in range(WEEKS):
        for r in range(7):
            d = first_monday + dt.timedelta(weeks=w, days=r)
            if d > today:
                continue
            x, y = gx0 + w * STEP, gy0 + r * STEP
            lv = level_of(counts.get(d, 0))
            if d < start:
                a(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="4.5" fill="{WHITE}" fill-opacity=".05"/>')
            elif lv == 0 and d != today:
                a(f'<rect x="{x+.75}" y="{y+.75}" width="{CELL-1.5}" height="{CELL-1.5}" rx="4" fill="{MISSED}" fill-opacity=".12" stroke="{MISSED}" stroke-opacity=".9" stroke-width="1.5"/>')
            elif lv == 0:
                a(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="4.5" fill="{WHITE}" fill-opacity=".08"/>')
            else:
                c, op = LEVELS[lv - 1]
                a(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="4.5" fill="{c}" fill-opacity="{op}"/>')
            if d == today:
                cls = "" if done else ' class="p"'
                a(f'<rect x="{x-3}" y="{y-3}" width="{CELL+6}" height="{CELL+6}" rx="7" fill="none" stroke="{WHITE}" stroke-width="1.6"{cls}/>')
    # 범례
    lgx = gx0 + WEEKS * STEP + 14
    a(f'<rect x="{lgx+.75}" y="{gy0+.75}" width="12.5" height="12.5" rx="3.5" fill="{MISSED}" fill-opacity=".12" stroke="{MISSED}" stroke-opacity=".9" stroke-width="1.5"/>')
    a(f'<text x="{lgx+21}" y="{gy0+12}" class="s" font-size="12.5" fill="{WHITE}" fill-opacity=".85">Missed</text>')
    a(f'<rect x="{lgx}" y="{gy0+26}" width="14" height="14" rx="4" fill="none" stroke="{WHITE}" stroke-width="1.5"/>')
    a(f'<text x="{lgx+21}" y="{gy0+38}" class="s" font-size="12.5" fill="{WHITE}" fill-opacity=".85">Today</text>')
    a(f'<text x="{lgx}" y="{gy0+76}" class="s" font-size="12.5" fill="{WHITE}" fill-opacity=".85">Less</text>')
    for i, (c, op) in enumerate(LEVELS):
        a(f'<rect x="{lgx + (i%2)*18}" y="{gy0+86 + (i//2)*18}" width="14" height="14" rx="4" fill="{c}" fill-opacity="{op}"/>')
    a(f'<text x="{lgx}" y="{gy0+136}" class="s" font-size="12.5" fill="{WHITE}" fill-opacity=".85">More</text>')

    a('</svg>')
    return "\n".join(o)

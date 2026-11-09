#!/usr/bin/env python3
"""
README 설치 가이드용 '따라 하기 그림' 생성기 (표준 라이브러리만 사용).

GitHub 화면을 단순화해서 그리고, 눌러야 할 곳에 보라색 테두리와 번호를 붙인다.
실제 스크린샷이 아니라 그림이라 개인 정보가 들어가지 않고, GitHub 화면이 조금 바뀌어도
어디를 눌러야 하는지 알아보기 쉽다.

usage: python3 tools/make_guide.py   -> docs/guide/*.svg
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "docs" / "guide"

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', 'Apple SD Gothic Neo', "
        "'Malgun Gothic', Helvetica, Arial, sans-serif")
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# GitHub 라이트 테마 색
BG, CANVAS2, BORDER, TEXT, MUTED = "#ffffff", "#f6f8fa", "#d0d7de", "#1f2328", "#59636e"
LINK, GREEN, GREEN_BORDER = "#0969da", "#1f883d", "#1a7f37"
ACCENT = "#fd8c73"                     # 선택된 탭 밑줄
# 가이드 표시 (README 보라색 버튼과 같은 계열)
MARK, MARK_SOFT = "#8B3FD0", "#F3E8FF"

W = 820


def tw(s: str, size: float = 14) -> float:
    """대략적인 글자 폭."""
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += size * 0.98
        elif ch in "il.,:;|!'":
            w += size * 0.30
        elif ch.isupper() or ch in "mwMW@":
            w += size * 0.66
        else:
            w += size * 0.54
    return w


class Scene:
    def __init__(self, h: int, url: str, title: str):
        self.h = h
        self.p: list[str] = []
        self.marks: list[str] = []
        self.title = title
        self._frame(url)

    # ── 기본 도형 ──
    def add(self, s: str):
        self.p.append(s)

    def rect(self, x, y, w, h, fill=BG, stroke=None, r=6, sw=1, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}{extra}/>')

    def text(self, x, y, s, size=14, color=TEXT, weight=400, anchor="start", mono=False, extra=""):
        fam = MONO if mono else FONT
        ws = ' xml:space="preserve"' if mono else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{color}" text-anchor="{anchor}"{ws}{extra}>{escape(s)}</text>')

    def line(self, x1, y1, x2, y2, color=BORDER, sw=1):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>')

    # ── 브라우저 틀 ──
    def _frame(self, url):
        self.rect(0.5, 0.5, W - 1, self.h - 1, fill=BG, stroke=BORDER, r=12)
        self.add(f'<path d="M0.5 12.5a12 12 0 0 1 12-12h{W-25}a12 12 0 0 1 12 12v27.5h-{W-1}z" fill="#eef1f4"/>')
        self.line(0.5, 40, W - 0.5, 40)
        for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
            self.add(f'<circle cx="{20 + i*18}" cy="20.5" r="5.5" fill="{c}"/>')
        self.rect(90, 9, W - 180, 23, fill=BG, stroke="#e1e4e8", r=11.5)
        self.add(f'<g transform="translate(102,15)" fill="none" stroke="{MUTED}" stroke-width="1.3">'
                 '<rect x="1" y="4.5" width="8" height="6" rx="1.2"/><path d="M3 4.5V3a2 2 0 0 1 4 0v1.5"/></g>')
        self.text(118, 25, url, size=12, color=MUTED)

    # ── GitHub 부품 ──
    def button(self, x, y, label, kind="default", w=None, h=32, size=14, caret=False, icon=None):
        lw = tw(label, size) + (14 if caret else 0) + (20 if icon else 0)
        w = w or round(lw + 28)
        fill, stroke, color = {
            "default": (CANVAS2, BORDER, TEXT),
            "green": (GREEN, GREEN_BORDER, "#ffffff"),
            "danger": (CANVAS2, BORDER, "#d1242f"),
        }[kind]
        self.rect(x, y, w, h, fill=fill, stroke=stroke, r=6)
        tx = x + (w - lw) / 2
        if icon == "play":
            self.add(f'<path d="M{tx+2} {y+h/2-5}l8 5-8 5z" fill="{color}"/>')
            tx += 20
        self.text(tx, y + h / 2 + size * 0.36, label, size=size, color=color, weight=600)
        if caret:
            cx = tx + tw(label, size) + 8
            self.add(f'<path d="M{cx} {y+h/2-2}l4 4 4-4" fill="none" stroke="{color}" stroke-width="1.5"/>')
        return (x, y, w, h)

    def field(self, x, y, w, value="", label=None, placeholder="", mono=False, h=32, req=False):
        if label:
            self.text(x, y - 8, label, size=14, weight=600)
            if req:
                self.text(x + tw(label, 14) + 4, y - 8, "*", size=14, color="#d1242f", weight=600)
        self.rect(x, y, w, h, fill=BG, stroke=BORDER, r=6)
        if value:
            self.text(x + 12, y + h / 2 + 5, value, size=14, mono=mono)
        elif placeholder:
            self.text(x + 12, y + h / 2 + 5, placeholder, size=14, color="#818b98")
        return (x, y, w, h)

    def radio(self, x, y, label, on=False, sub=None):
        self.add(f'<circle cx="{x+8}" cy="{y}" r="7.5" fill="{BG}" stroke="{LINK if on else "#818b98"}" stroke-width="{4.5 if on else 1}"/>')
        self.text(x + 24, y + 5, label, size=14, weight=600)
        if sub:
            self.text(x + 24, y + 24, sub, size=12.5, color=MUTED)

    def repo_header(self, y, owner, name, active, badge="Public", tabs=None):
        tabs = tabs or ["Code", "Issues", "Pull requests", "Actions", "Projects", "Security", "Insights", "Settings"]
        self.rect(0.5, y, W - 1, 92, fill=CANVAS2, r=0)
        # 저장소 아이콘 + 이름
        self.add(f'<g transform="translate(24,{y+16})" fill="none" stroke="{MUTED}" stroke-width="1.4">'
                 '<path d="M2 13V2.5A1.5 1.5 0 0 1 3.5 1H13v10H3.5A1.5 1.5 0 0 0 2 12.5z"/></g>')
        self.text(48, y + 30, owner, size=17, color=LINK)
        ox = 48 + tw(owner, 17) + 6
        self.text(ox, y + 30, "/", size=17, color=MUTED)
        self.text(ox + 14, y + 30, name, size=17, color=LINK, weight=600)
        nx = ox + 14 + tw(name, 17, ) * 1.04 + 10
        bw = tw(badge, 12) + 16
        self.rect(nx, y + 15, bw, 21, fill=BG, stroke=BORDER, r=10.5)
        self.text(nx + bw / 2, y + 30, badge, size=12, color=MUTED, weight=500, anchor="middle")
        # 탭
        x = 24
        pos = {}
        for t in tabs:
            w = tw(t, 14) + 24
            pos[t] = (x - 4, y + 52, w + 8, 34)
            weight = 600 if t == active else 400
            self.text(x + 12, y + 74, t, size=14, weight=weight)
            if t == active:
                self.rect(x, y + 89, w, 3, fill=ACCENT, r=1.5)
            x += w + 6
        self.line(0.5, y + 92, W - 0.5, y + 92)
        return pos

    # ── 가이드 표시 ──
    def mark(self, box, n, note=None, side="right", pad=4, note_dx=0, note_dy=0):
        x, y, w, h = box
        x, y, w, h = x - pad, y - pad, w + pad * 2, h + pad * 2
        self.marks.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="none" stroke="{MARK}" '
                          f'stroke-width="2.5"/>')
        cx, cy = x + w, y          # 번호는 오른쪽 위 모서리 (왼쪽 라벨을 가리지 않게)
        self.marks.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="{MARK}" stroke="#fff" stroke-width="2"/>'
                          f'<text x="{cx}" y="{cy+4.6}" font-family="{FONT}" font-size="13" font-weight="700" '
                          f'fill="#fff" text-anchor="middle">{n}</text>')
        if note:
            nw = tw(note, 13) + 22
            if side == "right":
                bx, by = x + w + 12, y + h / 2 - 14
            elif side == "left":
                bx, by = x - 12 - nw, y + h / 2 - 14
            elif side == "below":
                bx, by = x + w / 2 - nw / 2, y + h + 10
            else:  # above
                bx, by = x + w / 2 - nw / 2, y - 38
            bx, by = bx + note_dx, by + note_dy
            self.marks.append(f'<rect x="{bx}" y="{by}" width="{nw}" height="28" rx="14" fill="{MARK_SOFT}" '
                              f'stroke="{MARK}" stroke-opacity=".5"/>'
                              f'<text x="{bx+11}" y="{by+18.5}" font-family="{FONT}" font-size="13" font-weight="600" '
                              f'fill="#5B1E96">{escape(note)}</text>')

    def svg(self) -> str:
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{self.h}" viewBox="0 0 {W} {self.h}" '
                f'role="img" aria-label="{escape(self.title)}"><title>{escape(self.title)}</title>'
                + "".join(self.p) + "".join(self.marks) + "</svg>")


# ───────────────────────── 장면들 ─────────────────────────
def folder_icon(s: Scene, x, y, color="#54aeff"):
    s.add(f'<path transform="translate({x},{y})" d="M1 3.5A1.5 1.5 0 0 1 2.5 2h4l1.5 2h6.5A1.5 1.5 0 0 1 16 5.5v7'
          f'A1.5 1.5 0 0 1 14.5 14h-12A1.5 1.5 0 0 1 1 12.5z" fill="{color}"/>')


def file_icon(s: Scene, x, y):
    s.add(f'<path transform="translate({x},{y})" d="M3 1.5h6.5L13 5v9.5H3z" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')


def step1_baekjoonhub() -> Scene:
    s = Scene(330, "github.com/내아이디/algorithm", "백준허브 저장소에 프로그래머스 폴더가 생긴 모습")
    s.repo_header(41, "내아이디", "algorithm", "Code")
    y0 = 150
    s.rect(24, y0, W - 48, 160, fill=BG, stroke=BORDER, r=8)
    s.rect(24.5, y0 + .5, W - 49, 44, fill=CANVAS2, r=8)
    s.add(f'<circle cx="46" cy="{y0+22}" r="10" fill="#d8b9ff"/>')
    s.text(64, y0 + 27, "내아이디", size=13.5, weight=600)
    s.text(130, y0 + 27, "[level 1] Title: 삼총사, Time: 0.01 ms, Memory: 4.82 MB -BaekjoonHub",
           size=13.5, color=MUTED)
    s.line(24, y0 + 44, W - 24, y0 + 44)
    rows = [("folder", "백준", "[Bronze II] Title: ..."), ("folder", "프로그래머스", "[level 1] Title: 삼총사 ..."),
            ("file", "README.md", "Create README.md")]
    for i, (kind, name, msg) in enumerate(rows):
        ry = y0 + 44 + i * 38
        if i:
            s.line(24, ry, W - 24, ry, color="#eaeef2")
        (folder_icon if kind == "folder" else file_icon)(s, 42, ry + 12)
        s.text(70, ry + 24, name, size=14, color=TEXT)
        s.text(320, ry + 24, msg, size=13.5, color=MUTED)
        if name == "프로그래머스":
            s.mark((36, ry + 6, 150, 27), 1, "이 폴더가 생겼으면 준비 완료!", side="right", note_dx=330)
    return s


def step2_template() -> Scene:
    s = Scene(300, "github.com/harim789/Programmers-Streak-Badge", "Use this template 버튼 위치")
    s.repo_header(41, "harim789", "Programmers-Streak-Badge", "Code", badge="Public template")
    y = 150
    s.button(24, y, "main", caret=True, size=13.5)
    b1 = s.button(W - 24 - 186, y, "Use this template", kind="green", caret=True)
    # 펼쳐진 메뉴
    mx, my, mw = W - 24 - 250, y + 44, 250
    s.rect(mx, my, mw, 84, fill=BG, stroke=BORDER, r=10,
           extra=' style="filter:drop-shadow(0 6px 14px rgba(31,35,40,.15))"')
    s.text(mx + 16, my + 30, "Create a new repository", size=14, weight=600)
    s.text(mx + 16, my + 62, "Open in a codespace", size=14, color=MUTED)
    s.line(mx, my + 44, mx + mw, my + 44, color="#eaeef2")
    s.mark(b1, 1, "초록 버튼 클릭", side="left")
    s.mark((mx + 6, my + 8, mw - 12, 30), 2, "새 저장소 만들기", side="left")
    return s


def step2_create() -> Scene:
    s = Scene(470, "github.com/new?template_name=Programmers-Streak-Badge", "새 저장소 만들기 화면")
    s.text(40, 82, "Create a new repository", size=22, weight=600)
    s.text(40, 106, "템플릿: harim789/Programmers-Streak-Badge", size=13.5, color=MUTED)
    s.line(40, 122, W - 40, 122)
    s.button(40, 160, "내아이디", caret=True, w=150)
    s.text(40, 152, "Owner", size=14, weight=600)
    s.text(201, 182, "/", size=20, color=MUTED)
    f = s.field(220, 160, 300, "programmers-streak-badge", label="Repository name", req=True)
    s.mark(f, 1, "이름 입력 (다른 이름도 OK)", side="right")
    s.line(40, 222, W - 40, 222)
    s.radio(44, 252, "Public", on=True, sub="Anyone on the internet can see this repository.")
    s.radio(44, 312, "Private", on=False, sub="You choose who can see and commit to this repository.")
    s.mark((36, 236, 380, 46), 2, "꼭 Public!", side="right")
    s.line(40, 346, W - 40, 346)
    b = s.button(W - 40 - 170, 380, "Create repository", kind="green")
    s.mark(b, 3, "클릭", side="left")
    return s


def settings_sidebar(s: Scene, y, active="Actions"):
    items = [("General", 0), ("Collaborators", 0), ("Branches", 0), ("Actions", 0), ("Webhooks", 0),
             ("Secrets and variables", 0), ("Actions", 1), ("Codespaces", 1), ("Dependabot", 1)]
    pos = {}
    for i, (name, indent) in enumerate(items):
        iy = y + i * 32
        x = 32 + indent * 18
        is_active = indent == 1 and name == active
        if is_active:
            s.rect(24, iy, 210, 30, fill="#eef1f4", r=6)
            s.rect(24, iy + 6, 3.5, 18, fill=LINK, r=1.75)
        s.text(x + 10, iy + 20, name, size=14, weight=600 if is_active or name == "Secrets and variables" else 400,
               color=TEXT)
        pos[(name, indent)] = (24, iy, 210, 30)
    return pos


def step4_secrets() -> Scene:
    s = Scene(500, "github.com/내아이디/programmers-streak-badge/settings/secrets/actions", "Secrets 등록 위치")
    tabs = s.repo_header(41, "내아이디", "programmers-streak-badge", "Settings")
    s.mark(tabs["Settings"], 1, None)
    side = settings_sidebar(s, 152)
    a, b_ = side[("Secrets and variables", 0)], side[("Actions", 1)]
    s.mark((a[0], a[1], a[2], b_[1] + b_[3] - a[1]), 2, None)
    x0 = 262
    s.text(x0, 176, "Actions secrets and variables", size=20, weight=600)
    s.text(x0, 200, "비밀번호·토큰은 Secrets, 저장소 이름은 Variables에 넣어요", size=13, color=MUTED)
    # 탭 Secrets / Variables
    s.text(x0 + 10, 240, "Secrets", size=14, weight=600)
    s.rect(x0, 250, 76, 3, fill=ACCENT, r=1.5)
    s.text(x0 + 100, 240, "Variables", size=14)
    s.line(x0, 253, W - 32, 253)
    s.text(x0, 290, "Repository secrets", size=16, weight=600)
    b = s.button(W - 32 - 200, 270, "New repository secret", kind="green")
    s.mark(b, 3, None)
    for i, name in enumerate(["PROGRAMMERS_ID", "PROGRAMMERS_PW"]):
        ry = 320 + i * 44
        s.rect(x0, ry, W - 32 - x0, 44, fill=BG, stroke=BORDER, r=0 if i else 6)
        s.add(f'<g transform="translate({x0+14},{ry+14})" fill="none" stroke="{MUTED}" stroke-width="1.3">'
              '<rect x="1" y="6" width="12" height="9" rx="1.5"/><path d="M4 6V4a3 3 0 0 1 6 0v2"/></g>')
        s.text(x0 + 40, ry + 27, name, size=13.5, mono=True, weight=600)
        s.text(W - 52, ry + 27, "Updated now", size=12.5, color=MUTED, anchor="end")
    s.text(x0, 430, "↑ 등록하면 이렇게 이름만 보이고, 값은 아무도 다시 볼 수 없어요.", size=13, color=MUTED)
    return s


def step4_form() -> Scene:
    s = Scene(380, "github.com/내아이디/programmers-streak-badge/settings/secrets/actions/new", "New secret 입력 화면")
    s.text(40, 82, "Actions secrets / New secret", size=22, weight=600)
    s.line(40, 100, W - 40, 100)
    f1 = s.field(40, 140, 420, "PROGRAMMERS_ID", label="Name", mono=True, req=True)
    s.mark(f1, 1, "이름은 그대로 복사", side="right")
    s.text(40, 210, "Secret", size=14, weight=600)
    s.text(40 + tw("Secret", 14) + 4, 210, "*", size=14, color="#d1242f", weight=600)
    s.rect(40, 218, 420, 90, fill=BG, stroke=BORDER, r=6)
    s.text(52, 244, "you@example.com", size=14, mono=True)
    s.mark((40, 218, 420, 90), 2, "값 입력", side="right")
    b = s.button(40, 330, "Add secret", kind="green")
    s.mark(b, 3, "저장", side="right")
    return s


def step5_variable() -> Scene:
    s = Scene(430, "github.com/내아이디/programmers-streak-badge/settings/variables/actions", "Variables 등록 화면")
    s.repo_header(41, "내아이디", "programmers-streak-badge", "Settings")
    settings_sidebar(s, 152)
    x0 = 262
    s.text(x0, 176, "Actions secrets and variables", size=20, weight=600)
    s.text(x0 + 10, 222, "Secrets", size=14)
    t = (x0 + 92, 202, 90, 30)
    s.text(x0 + 100, 222, "Variables", size=14, weight=600)
    s.rect(x0 + 90, 232, 86, 3, fill=ACCENT, r=1.5)
    s.line(x0, 235, W - 32, 235)
    s.mark(t, 1, None)
    b = s.button(W - 32 - 210, 252, "New repository variable", kind="green")
    s.mark(b, 2, None)
    f1 = s.field(x0, 330, 230, "ALGO_REPO", label="Name", mono=True, req=True)
    f2 = s.field(x0 + 246, 330, W - 32 - x0 - 246, "내아이디/algorithm", label="Value", mono=True, req=True)
    s.mark((f1[0], f1[1], f2[0] + f2[2] - f1[0], 32), 3, "백준허브 저장소의  아이디/저장소이름", side="below")
    return s


def step6_run() -> Scene:
    s = Scene(470, "github.com/내아이디/programmers-streak-badge/actions", "워크플로우 수동 실행")
    tabs = s.repo_header(41, "내아이디", "programmers-streak-badge", "Actions")
    s.mark(tabs["Actions"], 1, None)
    s.text(32, 174, "Actions", size=20, weight=600)
    s.text(40, 214, "All workflows", size=14)
    wf = (24, 230, 220, 32)
    s.rect(*wf, fill="#eef1f4", r=6)
    s.rect(24, 236, 3.5, 20, fill=LINK, r=1.75)
    s.text(40, 251, "Programmers Streak Badge", size=14, weight=600)
    s.mark(wf, 2, None)
    x0 = 266
    s.text(x0, 174, "Programmers Streak Badge", size=20, weight=600)
    s.rect(x0, 196, W - 32 - x0, 52, fill=CANVAS2, stroke=BORDER, r=6)
    s.text(x0 + 14, 227, "This workflow has a workflow_dispatch event trigger.", size=13, color=MUTED)
    b = s.button(W - 32 - 140, 206, "Run workflow", caret=True, size=13.5)
    s.mark(b, 3, None)
    # 펼친 창
    px, py, pw = W - 32 - 250, 256, 250
    s.rect(px, py, pw, 110, fill=BG, stroke=BORDER, r=10,
           extra=' style="filter:drop-shadow(0 6px 14px rgba(31,35,40,.15))"')
    s.text(px + 14, py + 26, "Use workflow from", size=13, color=MUTED)
    s.button(px + 14, py + 34, "Branch: main", caret=True, size=13, h=28)
    b2 = s.button(px + 14, py + 72, "Run workflow", kind="green", size=13.5, h=30)
    s.mark(b2, 4, "한 번 더!", side="left")
    # 결과 목록
    ry = 390
    s.rect(x0, ry, W - 32 - x0, 52, fill=BG, stroke=BORDER, r=6)
    s.add(f'<circle cx="{x0+22}" cy="{ry+26}" r="9" fill="{GREEN}"/>'
          f'<path d="M{x0+17.5} {ry+26}l3 3 6-6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>')
    s.text(x0 + 42, ry + 22, "Programmers Streak Badge", size=14, weight=600)
    s.text(x0 + 42, ry + 41, "Manually run by 내아이디 · 1m 2s", size=12.5, color=MUTED)
    s.text(x0 - 12, ry + 31, "1~2분 뒤 초록 체크면 성공 →", size=13, color=GREEN, weight=600, anchor="end")
    return s


def step7_profile() -> Scene:
    s = Scene(440, "github.com/내아이디/내아이디/edit/main/README.md", "프로필 README에 배지 붙이기")
    s.repo_header(41, "내아이디", "내아이디", "Code", badge="Public")
    s.text(32, 168, "내아이디 / README.md", size=15, weight=600)
    s.text(40 + tw("내아이디 / README.md", 15), 168, "in main", size=13, color=MUTED)
    b = s.button(W - 32 - 150, 148, "Commit changes...", kind="green", size=13.5)
    s.mark(b, 2, "저장", side="left")
    ex, ey, ew, eh = 32, 196, W - 64, 220
    s.rect(ex, ey, ew, eh, fill=BG, stroke=BORDER, r=6)
    s.rect(ex + .5, ey + .5, ew - 1, 36, fill=CANVAS2, r=6)
    s.text(ex + 16, ey + 24, "Edit", size=13.5, weight=600)
    s.text(ex + 64, ey + 24, "Preview", size=13.5, color=MUTED)
    s.line(ex, ey + 36, ex + ew, ey + 36)
    code = [
        ("Hi there 👋", MUTED),
        ("", TEXT),
        ('<p align="center">', TEXT),
        ('  <img src="https://raw.githubusercontent.com/내아이디/', TEXT),
        ('programmers-streak-badge/main/assets/programmers-streak.svg"', TEXT),
        ('       alt="Programmers Streak Badge" width="100%">', TEXT),
        ("</p>", TEXT),
    ]
    for i, (ln, c) in enumerate(code):
        y = ey + 62 + i * 22
        s.text(ex + 14, y, str(i + 1), size=12, color="#8c959f", mono=True, anchor="start")
        s.text(ex + 44, y, ln, size=13, color=c, mono=True)
    s.mark((ex + 36, ey + 62 + 2 * 22 - 16, 560, 22 * 5 + 6), 1, "붙여넣고 '내아이디'만 바꾸기", side="below",
           note_dx=80, note_dy=-4)
    return s


def step_dispatch() -> Scene:
    s = Scene(330, "github.com/내아이디/algorithm/new/main", "백준허브 저장소에 새 파일 만들기")
    s.repo_header(41, "내아이디", "algorithm", "Code")
    s.text(32, 168, "algorithm /", size=15, color=LINK)
    f = s.field(32 + tw("algorithm /", 15) + 10, 148, 380, ".github/workflows/notify-badge.yml", mono=True)
    s.mark(f, 1, "파일 이름 입력", side="below")
    b = s.button(W - 32 - 150, 148, "Commit changes...", kind="green", size=13.5)
    s.mark(b, 3, "저장", side="below")
    s.rect(32, 236, W - 64, 70, fill=BG, stroke=BORDER, r=6)
    s.text(46, 264, "name: notify-badge", size=13, mono=True)
    s.text(46, 286, "on: …  (README의 내용을 그대로 붙여넣기)", size=13, mono=True, color=MUTED)
    s.mark((32, 236, W - 64, 70), 2, None)
    return s


def step3_token() -> Scene:
    s = Scene(540, "github.com/settings/personal-access-tokens/new", "Fine-grained token 만들기")
    s.text(40, 82, "New fine-grained personal access token", size=22, weight=600)
    s.line(40, 100, W - 40, 100)
    f = s.field(40, 140, 360, "programmers-streak-read", label="Token name", req=True)
    s.mark(f, 1, "아무 이름", side="right")
    s.text(40, 214, "Repository access", size=14, weight=600)
    s.radio(44, 244, "Public repositories", on=False)
    s.radio(44, 276, "All repositories", on=False)
    s.radio(44, 308, "Only select repositories", on=True)
    s.button(68, 324, "내아이디/algorithm", caret=True, size=13.5)
    s.mark((36, 294, 290, 66), 2, "백준허브 저장소 하나만", side="right")
    s.text(40, 394, "Permissions  ›  Repository permissions", size=14, weight=600)
    s.rect(40, 406, 520, 44, fill=BG, stroke=BORDER, r=6)
    s.text(56, 433, "Contents", size=14, weight=600)
    c = s.button(400, 412, "Read-only", caret=True, size=13.5, h=32)
    s.mark(c, 3, "읽기 전용", side="right")
    b = s.button(40, 476, "Generate token", kind="green")
    s.mark(b, 4, "만들고 github_pat_… 복사", side="right")
    return s


SCENES = {
    "1-baekjoonhub": step1_baekjoonhub,
    "2-use-template": step2_template,
    "2-create-repo": step2_create,
    "3-token": step3_token,
    "4-secrets": step4_secrets,
    "4-secret-form": step4_form,
    "5-variable": step5_variable,
    "6-run-workflow": step6_run,
    "7-profile-readme": step7_profile,
    "8-dispatch-file": step_dispatch,
}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in SCENES.items():
        (OUT / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
    print(f"{len(SCENES)} guide images -> {OUT}")

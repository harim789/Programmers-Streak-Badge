#!/usr/bin/env python3
"""
README용 '클릭 표시' 버튼 SVG 생성기.
- 테마 보라색 pill + 흰 글자. 글자는 폰트 윤곽선을 path로 변환해 넣으므로
  어떤 환경에서도 똑같이 보이고 파일도 작다.
- 라틴 글자는 Hanken Grotesk 600, 한글 등은 Noto Sans CJK KR Bold로 대체.

usage: pip install fonttools brotli
       python3 tools/make_buttons.py <hanken-600.woff2> <NotoSansCJK-Bold.ttc>
"""
import re
import sys
from pathlib import Path

from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = Path(__file__).resolve().parent.parent / "docs" / "buttons"

BUTTONS = {
    # GitHub
    "use-this-template": "Use this template",
    "create-a-new-repository": "Create a new repository",
    "create-repository": "Create repository",
    "settings": "Settings",
    "secrets-and-variables": "Secrets and variables",
    "actions": "Actions",
    "new-repository-secret": "New repository secret",
    "add-secret": "Add secret",
    "variables": "Variables",
    "new-repository-variable": "New repository variable",
    "add-variable": "Add variable",
    "developer-settings": "Developer settings",
    "personal-access-tokens": "Personal access tokens",
    "fine-grained-tokens": "Fine-grained tokens",
    "generate-new-token": "Generate new token",
    "only-select-repositories": "Only select repositories",
    "generate-token": "Generate token",
    "run-workflow": "Run workflow",
    "general": "General",
    "read-and-write-permissions": "Read and write permissions",
    "save": "Save",
    "add-file": "Add file",
    "create-new-file": "Create new file",
    "commit-changes": "Commit changes...",
    "commit-changes-confirm": "Commit changes",
    "edit": "Edit",
    "workflow": "Programmers Streak Badge",
    # BaekjoonHub / Chrome
    "add-to-chrome": "Chrome에 추가",
    "authorize-with-github": "Authorize with GitHub",
    "get-started": "Get Started",
    # README 범례용
    "click": "클릭",
}

FILL_FROM, FILL_TO, STROKE = "#9B4FD1", "#7A2FB0", "#C9A2EE"
SIZE, H, PADX, R = 13.5, 26, 12, 8


class Fonts:
    def __init__(self, latin_path, cjk_path):
        self.latin = TTFont(latin_path)
        coll = TTCollection(cjk_path)
        self.cjk = next(f for f in coll.fonts if "KR" in f["name"].getDebugName(1))

    def pick(self, ch):
        for f in (self.latin, self.cjk):
            if ord(ch) in f.getBestCmap():
                return f
        return self.cjk

    def run(self, text):
        """return (svg path d, width_px)"""
        x = 0.0
        parts = []
        for ch in text:
            f = self.pick(ch)
            upm = f["head"].unitsPerEm
            scale = SIZE / upm
            gname = f.getBestCmap().get(ord(ch))
            gs = f.getGlyphSet()
            if gname is None:
                x += SIZE * 0.5
                continue
            pen = SVGPathPen(gs)
            # y 뒤집기 + 베이스라인 이동
            tp = TransformPen(pen, (scale, 0, 0, -scale, x, 0))
            gs[gname].draw(tp)
            d = pen.getCommands()
            if d:
                parts.append(d)
            x += f["hmtx"][gname][0] * scale
        return " ".join(parts), x


def round_path(d):
    return re.sub(r"-?\d+\.\d+", lambda m: f"{float(m.group()):.2f}".rstrip("0").rstrip("."), d)


def button(fonts, label):
    d, tw = fonts.run(label)
    w = round(tw + PADX * 2 + 14, 1)          # 14 = 왼쪽 커서 아이콘 공간
    base = H / 2 + SIZE * 0.36
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" '
        f'role="img" aria-label="{label}"><title>{label}</title>'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{FILL_FROM}"/><stop offset="1" stop-color="{FILL_TO}"/></linearGradient></defs>'
        f'<rect x=".5" y=".5" width="{w-1}" height="{H-1}" rx="{R}" fill="url(#g)" stroke="{STROKE}" stroke-opacity=".7"/>'
        # 클릭 커서 아이콘
        f'<path transform="translate({PADX-3},{H/2-6.5}) scale(.62)" fill="#fff" '
        f'd="M2 1l13 7.5-5.6 1.4 3.3 6-2.2 1.2-3.3-6L3 15z"/>'
        f'<path transform="translate({PADX + 14},{base:.2f})" fill="#fff" d="{round_path(d)}"/>'
        f'</svg>'
    )


if __name__ == "__main__":
    fonts = Fonts(sys.argv[1], sys.argv[2])
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, label in BUTTONS.items():
        (OUT / f"{slug}.svg").write_text(button(fonts, label), encoding="utf-8")
    print(f"{len(BUTTONS)} buttons -> {OUT}")

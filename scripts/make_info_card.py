"""Hand-authored neofetch-style info card -> info-card.svg (STATIC=1 for a frozen frame)."""
import os

STATIC = os.environ.get("STATIC") == "1"
W, LINE_H, TOP = 490, 22, 58
KEY, VAL, DIM = "#58a6ff", "#c9d1d9", "#8b949e"

# (key, value) rows; None = blank spacer
ROWS = [
    ("Name", "Anand CB"),
    ("Role", "Flutter Developer"),
    ("Location", "India"),
    None,
    ("Stack", "Flutter · Dart · Firebase"),
    ("State", "Provider"),
    ("Storage", "Hive · SQLite · REST APIs"),
    ("Also", "Android · Java · C · Arduino"),
    ("Design", "Figma · Illustrator · Photoshop"),
    None,
    ("Writing", "meanandcb.github.io/personal"),
    ("Contact", "meanandcb98@gmail.com"),
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

H = TOP + len(ROWS) * LINE_H + 20
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<style>.l{font:13px Menlo,Consolas,monospace}'
     + ('' if STATIC else '.a{opacity:0;animation:in .4s ease-out forwards}'
        '@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}')
     + '</style>',
     f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>',
     '<circle cx="18" cy="18" r="6" fill="#ff5f56"/><circle cx="38" cy="18" r="6" fill="#ffbd2e"/>'
     '<circle cx="58" cy="18" r="6" fill="#27c93f"/>',
     f'<text x="{W/2}" y="22" text-anchor="middle" class="l" fill="{DIM}">anand@github: ~</text>']

def line(i, inner):
    y = TOP + i * LINE_H
    delay = "" if STATIC else f' style="animation-delay:{0.3 + i * 0.12:.2f}s"'
    cls = "l" if STATIC else "l a"
    o.append(f'<text x="24" y="{y}" class="{cls}"{delay} xml:space="preserve">{inner}</text>')

for i, r in enumerate(ROWS):
    if r is None:
        line(i, f'<tspan fill="{DIM}">{"─" * 40}</tspan>')
    else:
        k, v = r
        line(i, f'<tspan fill="{KEY}" font-weight="bold">{esc(k):<9}</tspan><tspan fill="{VAL}">{esc(v)}</tspan>')
o.append("</svg>")
open("info-card.svg", "w").write("\n".join(o))
print("wrote info-card.svg")

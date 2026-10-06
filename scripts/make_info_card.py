"""Hand-authored neofetch-style info card -> info-card.svg (STATIC=1 for a frozen frame)."""
import json
import os
from datetime import datetime, timezone

STATIC = os.environ.get("STATIC") == "1"
W, LINE_H, TOP = 490, 22, 58
KEY, VAL, DIM = "#58a6ff", "#c9d1d9", "#8b949e"

prof = json.load(open("data/profile.json"))
yrs = (datetime.now(timezone.utc) - datetime.fromisoformat(prof["created_at"].replace("Z", "+00:00"))).days / 365.25

# (key, value) rows; None = blank spacer
ROWS = [
    ("Name", "Anand CB"),
    ("Role", "Flutter Developer"),
    ("Location", prof["location"] or "India"),
    ("Uptime", f"{yrs:.1f} years on GitHub"),
    None,
    ("Stack", "Flutter · Dart · Firebase"),
    ("State", "Provider"),
    ("Storage", "Hive · SQLite · REST APIs"),
    ("Also", "Android · Java · C · Arduino"),
    ("Design", "Figma · Illustrator · Photoshop"),
    None,
    ("Repos", f'{prof["repos"]} public · {prof["followers"]} followers · {prof["stars"]} stars'),
    ("Top lang", " · ".join(l for l, _ in prof["languages"][:3])),
    ("Last push", prof["recent"][0]["pushed_at"][:10]),
    None,
    ("Writing", "meanandcb.github.io/personal"),
    ("Contact", "meanandcb98@gmail.com"),
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

H = TOP + (len(ROWS) + 1) * LINE_H + 20
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
        line(i, f'<tspan fill="{KEY}" font-weight="bold">{esc(k):<10}</tspan><tspan fill="{VAL}">{esc(v)}</tspan>')
cy = TOP + len(ROWS) * LINE_H
prompt = '<tspan fill="#27c93f">anand@github</tspan><tspan fill="#8b949e">:~$ </tspan>'
delay = "" if STATIC else f' style="animation-delay:{0.3 + len(ROWS) * 0.12:.2f}s"'
o.append(f'<text x="24" y="{cy}" class="{"l" if STATIC else "l a"}"{delay} xml:space="preserve">{prompt}</text>')
o.append(f'<rect x="{24 + 7.8 * 14}" y="{cy - 11}" width="8" height="14" fill="#c9d1d9">'
         + ('' if STATIC else f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.01;0.02;0.5;1" dur="1.1s" begin="{0.5 + len(ROWS) * 0.12:.2f}s" repeatCount="indefinite"/>') + '</rect>')
o.append("</svg>")
open("info-card.svg", "w").write("\n".join(o))
print("wrote info-card.svg")

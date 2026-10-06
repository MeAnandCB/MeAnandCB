"""Render data/contributions.json as an animated 53x7 heatmap -> contrib-heatmap.svg."""
import json
import os
from datetime import date

STATIC = os.environ.get("STATIC") == "1"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX, GAP, LEFT, TOP = 12, 3, 40, 52
STEP = BOX + GAP

data = json.load(open("data/contributions.json"))
days = data["days"]
first = date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7  # Sunday-first rows
weeks = (offset + len(days) + 6) // 7
W = LEFT + weeks * STEP + 20
H = TOP + 7 * STEP + 60

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<style>text{font:11px Menlo,Consolas,monospace;fill:#8b949e}'
     + ('' if STATIC else '.b{opacity:0;animation:in .5s ease-out forwards}'
        '@keyframes in{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}')
     + '</style>',
     f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>']

last_month = None
for i, d in enumerate(days):
    idx = offset + i
    wk, row = divmod(idx, 7)
    x, y = LEFT + wk * STEP, TOP + row * STEP
    dt = date.fromisoformat(d["date"])
    if row == 0 and dt.month != last_month:
        last_month = dt.month
        o.append(f'<text x="{x}" y="{TOP - 10}">{dt.strftime("%b")}</text>')
    lvl = min(d["level"], len(PALETTE) - 1)
    delay = "" if STATIC else f' style="animation-delay:{(wk + row) * 0.025:.3f}s"'
    cls = "" if STATIC else ' class="b"'
    o.append(f'<rect{cls} x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="3" fill="{PALETTE[lvl]}"{delay}>'
             f'<title>{d["count"]} on {d["date"]}</title></rect>')

for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    o.append(f'<text x="8" y="{TOP + r * STEP + 10}">{name}</text>')

fy = TOP + 7 * STEP + 28
o.append(f'<text x="{LEFT}" y="{fy}" style="fill:#c9d1d9">{data["total"]:,} contributions in the last year'
         f' · longest streak {data["longest_streak"]}d</text>')
lx = W - 20 - (len(PALETTE) * STEP + 70)
o.append(f'<text x="{lx}" y="{fy}">Less</text>')
for i, c in enumerate(PALETTE):
    o.append(f'<rect x="{lx + 34 + i * STEP}" y="{fy - 10}" width="{BOX}" height="{BOX}" rx="3" fill="{c}"/>')
o.append(f'<text x="{lx + 38 + len(PALETTE) * STEP}" y="{fy}">More</text>')
o.append("</svg>")
open("contrib-heatmap.svg", "w").write("\n".join(o))
print(f"wrote contrib-heatmap.svg ({W}x{H})")

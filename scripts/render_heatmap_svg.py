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
H = TOP + 7 * STEP + 190

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<style>text{font:11px Menlo,Consolas,monospace;fill:#8b949e}'
     + ('' if STATIC else '.b{opacity:0;animation:in .5s ease-out forwards}'
        '@keyframes in{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}'
        '.g{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:up .7s cubic-bezier(.2,.8,.2,1) forwards}'
        '@keyframes up{to{transform:scaleY(1)}}')
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

fy = TOP + 7 * STEP + 24
lx = W - 20 - (len(PALETTE) * STEP + 70)
o.append(f'<text x="{lx}" y="{fy}">Less</text>')
for i, c in enumerate(PALETTE):
    o.append(f'<rect x="{lx + 34 + i * STEP}" y="{fy - 10}" width="{BOX}" height="{BOX}" rx="3" fill="{c}"/>')
o.append(f'<text x="{lx + 38 + len(PALETTE) * STEP}" y="{fy}">More</text>')

# pulse ring on the most recent active day
active = [i for i, d in enumerate(days) if d["count"]]
if active and not STATIC:
    wk, row = divmod(offset + active[-1], 7)
    o.append(f'<rect x="{LEFT + wk * STEP - 2}" y="{TOP + row * STEP - 2}" width="{BOX + 4}" height="{BOX + 4}" rx="4" '
             f'fill="none" stroke="#69f0a0"><animate attributeName="opacity" values="1;0.1;1" dur="2s" repeatCount="indefinite"/></rect>')

# stat tiles
active_days = len(active)
busiest = max(data["months"], key=data["months"].get)
best = data["best_day"]
tiles = [(f'{data["total"]:,}', "contributions / year"), (f'{data["current_streak"]}d', "current streak"),
         (f'{data["longest_streak"]}d', "longest streak"),
         (f'{best["count"]}', f'best day · {best["date"][5:]}'),
         (date.fromisoformat(busiest + "-01").strftime("%b %Y"), f'busiest month · {data["months"][busiest]}'),
         (f'{active_days / len(days):.0%}', f'active days · {active_days}')]
ty = fy + 36
for i, (v, k) in enumerate(tiles):
    x = LEFT + i * 130
    a = "" if STATIC else f' class="b" style="animation-delay:{1.2 + i * 0.1:.2f}s"'
    o.append(f'<g{a}><text x="{x}" y="{ty}" style="font-size:20px;font-weight:bold;fill:#c9d1d9">{v}</text>'
             f'<text x="{x}" y="{ty + 16}" style="font-size:10px">{k}</text></g>')

# weekday distribution + monthly bars
by_wd = [0] * 7
for i, d in enumerate(days):
    by_wd[(offset + i) % 7] += d["count"]
by = ty + 44
BH = 50
def bars(x0, vals, labels, bw, gap, delay0):
    mx = max(vals) or 1
    for i, (v, lab) in enumerate(zip(vals, labels)):
        h = max(2, BH * v / mx)
        x = x0 + i * (bw + gap)
        a = "" if STATIC else f' class="g" style="animation-delay:{delay0 + i * 0.06:.2f}s"'
        o.append(f'<rect{a} x="{x}" y="{by + BH - h:.0f}" width="{bw}" height="{h:.0f}" rx="2" fill="#26a641"><title>{lab}: {v}</title></rect>')
        o.append(f'<text x="{x + bw / 2}" y="{by + BH + 13}" text-anchor="middle" style="font-size:9px">{lab}</text>')
o.append(f'<text x="{LEFT}" y="{by - 8}" style="fill:#58a6ff">weekday activity</text>')
bars(LEFT, by_wd, "SMTWTFS", 22, 8, 1.6)
months = list(data["months"].items())
o.append(f'<text x="{LEFT + 300}" y="{by - 8}" style="fill:#58a6ff">contributions per month</text>')
bars(LEFT + 300, [v for _, v in months], [date.fromisoformat(k + "-01").strftime("%b")[0] for k, _ in months], 22, 8, 1.8)
o.append("</svg>")
open("contrib-heatmap.svg", "w").write("\n".join(o))
print(f"wrote contrib-heatmap.svg ({W}x{H})")

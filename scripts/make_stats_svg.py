"""Stats + languages + recent projects card -> stats-card.svg (STATIC=1 for a frozen frame)."""
import json
import os
from datetime import datetime, timezone

STATIC = os.environ.get("STATIC") == "1"
LANG_COLORS = {"Dart": "#00b4ab", "C++": "#f34b7d", "HTML": "#e34c26", "JavaScript": "#f1e05a",
               "CSS": "#563d7c", "Python": "#3572a5", "Java": "#b07219", "Makefile": "#427819"}
W, H = 860, 270
p = json.load(open("data/profile.json"))
created = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
years = (datetime.now(timezone.utc) - created).days / 365.25

def anim(delay):
    return "" if STATIC else f' class="a" style="animation-delay:{delay:.2f}s"'

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<style>text{font:12px Menlo,Consolas,monospace;fill:#8b949e}.v{font-size:22px;font-weight:bold;fill:#c9d1d9}'
     '.h{fill:#58a6ff;font-weight:bold}'
     + ('' if STATIC else '.a{opacity:0;animation:in .5s ease-out forwards}'
        '@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}'
        '.bar{transform-origin:0 0;transform:scaleX(0);animation:grow .9s cubic-bezier(.2,.8,.2,1) forwards}'
        '@keyframes grow{to{transform:scaleX(1)}}')
     + '</style>',
     f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>']

# left: numbers
o.append('<text x="28" y="34" class="h">$ gh stats</text>')
tiles = [("Repos", p["repos"]), ("Followers", p["followers"]), ("Following", p["following"]),
         ("Stars", p["stars"]), ("Forks", p["forks"]), ("Years on GitHub", f"{years:.1f}")]
for i, (k, v) in enumerate(tiles):
    x, y = 28 + (i % 2) * 130, 70 + (i // 2) * 58
    o.append(f'<g{anim(0.2 + i * 0.1)}><text x="{x}" y="{y}" class="v">{v}</text>'
             f'<text x="{x}" y="{y + 18}">{k}</text></g>')

# middle: languages
LX, BW = 320, 190
o.append(f'<text x="{LX}" y="34" class="h">$ top-languages</text>')
top = p["languages"]
mx = max(c for _, c in top)
for i, (lang, c) in enumerate(top):
    y = 62 + i * 30
    col = LANG_COLORS.get(lang, "#8b949e")
    bw = max(4, BW * c / mx)
    delay = "" if STATIC else f' style="animation-delay:{0.4 + i * 0.12:.2f}s"'
    cls = "" if STATIC else ' class="bar"'
    o.append(f'<text x="{LX}" y="{y + 11}" style="fill:#c9d1d9">{lang}</text>')
    o.append(f'<rect x="{LX + 88}" y="{y}" width="{BW}" height="14" rx="4" fill="#161b22"/>')
    o.append(f'<rect{cls} x="{LX + 88}" y="{y}" width="{bw:.0f}" height="14" rx="4" fill="{col}"{delay}/>')
    o.append(f'<text x="{LX + 88 + BW + 8}" y="{y + 11}">{c}</text>')

# right: recent projects
RX = 640
o.append(f'<text x="{RX}" y="34" class="h">$ ls -t recent/</text>')
for i, r in enumerate(p["recent"]):
    y = 66 + i * 34
    col = LANG_COLORS.get(r["language"], "#8b949e")
    name = r["name"] if len(r["name"]) <= 20 else r["name"][:19] + "…"
    o.append(f'<g{anim(0.5 + i * 0.12)}><circle cx="{RX + 5}" cy="{y - 4}" r="5" fill="{col}"/>'
             f'<text x="{RX + 18}" y="{y}" style="fill:#c9d1d9">{name}</text>'
             f'<text x="{RX + 18}" y="{y + 14}" style="font-size:10px">{r["language"] or "—"} · {r["pushed_at"][:10]}</text></g>')
o.append(f'<text x="28" y="{H - 16}" style="font-size:10px">C++ is GitHub\'s label for the native side of Flutter apps</text>')
o.append("</svg>")
open("stats-card.svg", "w").write("\n".join(o))
print("wrote stats-card.svg")

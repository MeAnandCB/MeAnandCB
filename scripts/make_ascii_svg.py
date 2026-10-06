"""Convert source-prepped.png into a monochrome, row-by-row typing ASCII SVG."""
import os
from PIL import Image

STATIC = os.environ.get("STATIC") == "1"  # frozen final frame for local previews

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)
COLS = 100
CHAR_W, CHAR_H = 6.0, 10.0   # px per glyph in the SVG
ROW_DUR, STAGGER = 0.6, 0.07  # seconds
FILL = "#c9d1d9"

img = Image.open("source-prepped.png").convert("L")
rows = round(COLS * img.height / img.width * (CHAR_W / CHAR_H))
img = img.resize((COLS, rows))
px = img.load()

W, H = COLS * CHAR_W, rows * CHAR_H + 10
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">',
       '<rect width="100%" height="100%" fill="#0d1117"/>', "<defs>"]
body = []
for y in range(rows):
    line = "".join(RAMP[int((255 - px[x, y]) / 256 * len(RAMP))] for x in range(COLS))
    line = line.rstrip()
    if not line:
        continue
    begin = f"{y * STAGGER:.2f}s"
    out.append(f'<clipPath id="c{y}"><rect x="0" y="{y*CHAR_H:.1f}" width="{int(W) if STATIC else 0}" height="{CHAR_H}">'
               + ("" if STATIC else f'<animate attributeName="width" from="0" to="{W:.0f}" dur="{ROW_DUR}s" begin="{begin}" fill="freeze"/>')
               + '</rect></clipPath>')
    esc = line.replace("&", "&amp;").replace("<", "&lt;")
    body.append(f'<text x="0" y="{(y+1)*CHAR_H-2:.1f}" clip-path="url(#c{y})" xml:space="preserve">{esc}</text>')
out.append("</defs>")
out.append(f'<g font-family="Menlo,Consolas,monospace" font-size="{CHAR_H}" fill="{FILL}" '
           f'style="white-space:pre">')
out += body
out.append("</g></svg>")
open("ascii.svg", "w").write("\n".join(out))
print(f"wrote ascii.svg ({COLS}x{rows})")

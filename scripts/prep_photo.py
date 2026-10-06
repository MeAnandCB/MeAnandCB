"""Prep a photo for ASCII conversion: crop, remove background, boost contrast, white bg."""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.png"
img = Image.open(src).convert("RGB")
w, h = img.size
# keep head + shoulders (top ~55% of a tall portrait)
img = img.crop((0, int(h * 0.05), w, int(h * 0.55)))

cut = remove(img)  # RGBA, background transparent
alpha = np.array(cut)[:, :, 3]
gray = cv2.cvtColor(np.array(cut.convert("RGB")), cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)

out = np.where(alpha > 128, gray, 255).astype(np.uint8)  # white background
Image.fromarray(out).save("source-prepped.png")
print("wrote source-prepped.png")

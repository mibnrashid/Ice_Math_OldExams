"""Whiten coloured (handwritten ink) pixels in a scan crop; the printed figure is grayscale.
Usage: python -I decolor.py <in.png> <out.png> [threshold]"""
import sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
thr = int(sys.argv[3]) if len(sys.argv) > 3 else 40
im = Image.open(src).convert("RGB")
px = im.load()
n = 0
for y in range(im.height):
    for x in range(im.width):
        r, g, b = px[x, y]
        if max(r, g, b) - min(r, g, b) > thr:
            px[x, y] = (255, 255, 255)
            n += 1
im.save(dst)
print("whitened", n, "of", im.width * im.height)

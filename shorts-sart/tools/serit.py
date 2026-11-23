#!/usr/bin/env python3
"""Kurguya bakış: kareleri ızgarada yan yana (adı = Shorts zamanı). python3 serit.py çıktı.jpg sütun genişlik kare...
"""
import sys, os
from PIL import Image, ImageDraw
out, cols, w, fs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
ims = [Image.open(f).convert('RGB') for f in fs]; h = int(ims[0].height * w / ims[0].width)
rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols * (w + 6), rows * (h + 26)), (255, 255, 255)); d = ImageDraw.Draw(S)
for i, (f, im) in enumerate(zip(fs, ims)):
    x, y = (i % cols) * (w + 6), (i // cols) * (h + 26)
    S.paste(im.resize((w, h)), (x, y + 22)); d.text((x + 4, y + 4), os.path.basename(f)[:-4], fill=(0, 0, 0))
S.save(out, quality=86)

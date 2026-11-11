#!/usr/bin/env python3
"""PNG (1920×1080) → 1280×720 JPG (Lanczos, kalite 92, < 2 MB). Kullanım: python3 kapak/jpg.py girdi.png çıktı.jpg [...]"""
import sys, os
from PIL import Image
a = sys.argv[1:]
for src, dst in zip(a[::2], a[1::2]):
    im = Image.open(src).convert('RGB').resize((1280, 720), Image.LANCZOS)
    q = 92
    while True:
        im.save(dst, quality=q, subsampling=0 if q >= 90 else 2, optimize=True)
        if os.path.getsize(dst) < 2_000_000 or q <= 70: break
        q -= 4
    print(dst, os.path.getsize(dst) // 1024, 'KB, q', q)

"""Kare tabakası: python3 tools/sheet.py çıktı.jpg kare1.png kare2.png ... (sütun=4, her kare 480×270, üstte zaman etiketi)"""
import sys, os
from PIL import Image, ImageDraw
out, files = sys.argv[1], sys.argv[2:]
cols = 4; w, h = 480, 270; rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * (h + 22)), (30, 30, 30)); d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS)
    x, y = (i % cols) * w, (i // cols) * (h + 22)
    sheet.paste(im, (x, y + 22)); d.text((x + 6, y + 4), os.path.basename(f), fill=(255, 220, 120))
sheet.save(out, quality=88); print(out, sheet.size)

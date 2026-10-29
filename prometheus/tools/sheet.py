"""Kontakt sayfası: python3 tools/sheet.py çıktı.png kare1.png kare2.png ... (3 sütun)"""
import sys
from PIL import Image, ImageDraw, ImageFont
out, files = sys.argv[1], sys.argv[2:]
cols = int(__import__('os').environ.get('COLS', 3)); w, h = 640, 360
rows = (len(files) + cols - 1) // cols
im = Image.new('RGB', (cols * w, rows * (h + 26)), (20, 20, 20))
d = ImageDraw.Draw(im)
for i, f in enumerate(files):
    a = Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS)
    x, y = (i % cols) * w, (i // cols) * (h + 26)
    im.paste(a, (x, y + 26)); d.text((x + 6, y + 6), f.split('/')[-1], fill=(255, 220, 120))
im.save(out)

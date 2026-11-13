"""Kapak test seti: python3 tools/kapak_test.py kapak.png çıktı_klasörü
- tam boy 1280×720 JPG, 246×138 ve 168×94 küçültmeler, gri değer, bulanık (odak testi),
- mobil akış taklidi (kanalın önceki kapaklarıyla), sağ alt süre rozeti örtüsü."""
import sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
base = os.path.splitext(os.path.basename(src))[0]
im = Image.open(src).convert('RGB').resize((1280, 720), Image.LANCZOS)
im.save(f'{out}/{base}_1280.jpg', quality=92)
for w, h in [(246, 138), (168, 94)]: im.resize((w, h), Image.LANCZOS).save(f'{out}/{base}_{w}.png')
im.convert('L').save(f'{out}/{base}_gri.png')
im.resize((320, 180), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6)).resize((640, 360)).save(f'{out}/{base}_bulanik.png')
b = im.copy(); d = ImageDraw.Draw(b); d.rounded_rectangle((1280 - 118, 720 - 58, 1280 - 14, 720 - 14), 8, fill=(0, 0, 0)); d.text((1280 - 100, 720 - 50), '6:11', fill=(255, 255, 255)); b.save(f'{out}/{base}_rozet.jpg', quality=90)
# mobil akış: 3 kapak alt alta, her biri 390 px genişlik, altında başlık satırları
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nb = [os.path.join(R, '..', 'sisifos', 'kapak.png'), os.path.join(R, '..', 'orfeus', 'kapak_final_A_arkana_bakma.jpg')]
feed = Image.new('RGB', (420, 3 * 300), (15, 15, 15)); fd = ImageDraw.Draw(feed)
items = [(nb[0], 'Sisifos\'u Neden Mutlu Hayal Etmeliyiz?'), (src, 'Cumhuriyet\'i Kuran Kuşak Nasıl Yetişti? | 29 Ekim'), (nb[1], 'Orfeus ve Evridiki')]
for i, (p, title) in enumerate(items):
    try: th = Image.open(p).convert('RGB').resize((390, 219), Image.LANCZOS)
    except Exception: th = Image.new('RGB', (390, 219), (60, 60, 60))
    feed.paste(th, (15, 10 + i * 300)); fd.text((15, 238 + i * 300), title, fill=(240, 240, 240)); fd.text((15, 256 + i * 300), 'Zaman Kuryesi · 1 B görüntüleme', fill=(150, 150, 150))
feed.save(f'{out}/{base}_akis.png'); print('tamam', out)

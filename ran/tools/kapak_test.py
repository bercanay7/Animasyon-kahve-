"""Ran kapak test seti (CLAUDE.md "Kapak test seti"): python3 tools/kapak_test.py A A2 B C
Girdi kapak/kapak_<ad>.png (1920×1080) → kapak/ran_kapak_<ad>.jpg (1280×720) ve kapak/test/:
 1) boyutlar.jpg: tam boy, 246×138, 168×94, 120×68, bulanık (odak), gri, süre rozeti bölgesi (x 1440–1874, y 829–1034 @1920)
 2) akis_koyu.jpg / akis_acik.jpg: telefon akışı taklidi (360 px genişlik ×2 ölçek), yanında kanalın diğer kapakları ve
    doygun renkli, büyük yazılı yer tutucular (akıştaki tipik rakip kapak); başlık ve kanal adı altta
 3) tv.jpg: 1920×1080 TV ana sayfası, satırda 4 kapak (~430 px)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ROOT = os.path.dirname(R)
T = os.path.join(R, 'kapak', 'test'); os.makedirs(T, exist_ok=True)
DJ = lambda s, b=True: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
BASLIK = "Yaptıkların Sana Döner mi? | Kurosawa'nın Kral Lear'ı"
adlar = sys.argv[1:] or ['A', 'A2', 'B', 'C']
K = {}
for a in adlar:
    im = Image.open(os.path.join(R, 'kapak', f'kapak_{a}.png')).convert('RGB').resize((1280, 720), Image.LANCZOS)
    f = os.path.join(R, 'kapak', f'ran_kapak_{a}.jpg'); im.save(f, quality=92); K[a] = im
    print(f, os.path.getsize(f) // 1024, 'KB')
# 1) boyutlar
S = [(246, 138), (168, 94), (120, 68)]; W = 1300; H = 175 * len(adlar) + 10
im = Image.new('RGB', (W, H), '#111'); d = ImageDraw.Draw(im)
for j, a in enumerate(adlar):
    y = 10 + j * 175; k = K[a]; x = 10
    d.text((x, y), a, fill='white', font=DJ(18)); x += 40
    for w, h in S: im.paste(k.resize((w, h), Image.LANCZOS), (x, y)); x += w + 10
    im.paste(k.resize((246, 138)).filter(ImageFilter.GaussianBlur(4)), (x, y)); x += 256
    im.paste(k.resize((246, 138)).convert('L').convert('RGB'), (x, y)); x += 256
    r = k.resize((246, 138)).copy(); dr = ImageDraw.Draw(r); bx0, by0 = int(246 * 1440 / 1920), int(138 * 829 / 1080)
    dr.rectangle([bx0, by0, 245, 137], outline='yellow', width=2); dr.rectangle([246 - 44, 138 - 22, 241, 133], fill='black'); dr.text((246 - 40, 138 - 20), '8:03', fill='white', font=DJ(13))
    im.paste(r, (x, y))
im.save(os.path.join(T, 'boyutlar.jpg'), quality=88)
# 2) telefon akışı
def yer_tutucu(renk, yazi):
    p = Image.new('RGB', (1280, 720), renk); dd = ImageDraw.Draw(p)
    dd.ellipse([760, 120, 1180, 700], fill=(235, 190, 160)); dd.ellipse([860, 300, 920, 360], fill='black'); dd.ellipse([1010, 300, 1070, 360], fill='black'); dd.ellipse([900, 470, 1040, 600], fill=(120, 20, 20))
    dd.text((60, 230), yazi, fill='white', font=DJ(150), stroke_width=8, stroke_fill='black'); return p
komsu = [('Kafka', os.path.join(ROOT, 'kafka', 'kapak', 'kapak_a.jpg'), "Kafka'nın Dönüşüm'ü: İşe Yaramasan da Seni…"),
         ('X', yer_tutucu((230, 40, 40), 'ŞOK!'), 'Bunu Kimse Bilmiyordu… (yer tutucu)'),
         ('İkaros', os.path.join(ROOT, 'ikaros', 'kapak', 'kapak_a.jpg'), 'İkaros: "Güneşe Yaklaşma." Peki Öteki Uyarı…'),
         ('Y', yer_tutucu((30, 120, 230), '10 SIR'), '10 Gizli Gerçek (yer tutucu)')]
def akis(koyu):
    bg, fg, gr = ((15, 15, 15), (241, 241, 241), (170, 170, 170)) if koyu else ((255, 255, 255), (15, 15, 15), (96, 96, 96))
    cols = len(adlar); w, h = 720, 405; im = Image.new('RGB', (cols * (w + 30) + 30, 3 * (h + 150) + 30), bg); d = ImageDraw.Draw(im)
    for c, a in enumerate(adlar):
        x = 30 + c * (w + 30); sira = [komsu[c % 4], (a, K[a], BASLIK), komsu[(c + 1) % 4]]
        for r_, (ad, src, bas) in enumerate(sira):
            y = 30 + r_ * (h + 150); t = src if isinstance(src, Image.Image) else Image.open(src).convert('RGB')
            im.paste(t.resize((w, h), Image.LANCZOS), (x, y))
            d.ellipse([x, y + h + 18, x + 56, y + h + 74], fill=(90, 90, 90))
            d.text((x + 72, y + h + 16), bas[:44], fill=fg, font=DJ(30)); d.text((x + 72, y + h + 60), 'Zaman Kuryesi · 1,2 B görüntüleme · 1 gün önce' if ad in adlar else 'Başka kanal · 50 B görüntüleme', fill=gr, font=DJ(24, False))
        d.text((x, 4), f'kapak {a}', fill=(255, 210, 31), font=DJ(22))
    return im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
akis(True).save(os.path.join(T, 'akis_koyu.jpg'), quality=86); akis(False).save(os.path.join(T, 'akis_acik.jpg'), quality=86)
# 3) TV ana sayfası (uzaktan): satırda 4 kapak ~430 px; Ran adayları ortada
tv = Image.new('RGB', (1920, 1080), (15, 15, 15)); d = ImageDraw.Draw(tv)
for r_, a in enumerate(adlar[:4]):
    y = 40 + r_ * 255; row = [komsu[0], (a, K[a], ''), komsu[1], komsu[2]]
    for c, (ad, src, _) in enumerate(row):
        t = src if isinstance(src, Image.Image) else Image.open(src).convert('RGB')
        tv.paste(t.resize((420, 236), Image.LANCZOS), (60 + c * 460, y))
    d.text((10, y + 100), a, fill=(255, 210, 31), font=DJ(26))
tv.resize((960, 540), Image.LANCZOS).save(os.path.join(T, 'tv.jpg'), quality=86)
print('test seti:', T)

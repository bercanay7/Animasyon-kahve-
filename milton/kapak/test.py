#!/usr/bin/env python3
"""Kapak test seti (CLAUDE.md "Kapak test seti"). Not: akış taklidi ilk iki kapağı "bizimkiler" olarak kullanır; A ve B'yi önce ver.
Kullanım: python3 kapak/test.py <çıktı-klasörü> kapak1.jpg [kapak2.jpg ...]
Her kapak için: tam boy, küçültmeler (246×138, 168×94, 120×68), bulanıklık (Gauss 8 px), gri değer, süre rozeti (25:46);
bütün kapaklar için: koyu ve açık mobil akış + "önerilen" listesi taklidi, TV boyu (1920 genişlik) ve yan yana karşılaştırma tabloları.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(sz, bold=True): return ImageFont.truetype(FB if bold else FR, sz)

BADGE = (960, 553, 1250, 690)   # 1280×720'de YouTube "önerilen" listesindeki gerçek rozet bölgesi

def rozet(im, w):
    """sağ altta süre rozeti (YouTube biçimi: siyah yarı saydam yuvarlak köşeli, beyaz rakam)"""
    im = im.convert('RGBA'); s = w / 1280
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    f = font(max(9, round(12 * w / 246)) if w <= 400 else round(34 * s))
    tw = d.textlength('25:46', font=f); pad = max(3, round(8 * s)) if w > 400 else 3
    h = f.size + pad
    x1, y1 = im.width - max(4, round(14 * s)), im.height - max(4, round(14 * s))
    d.rounded_rectangle([x1 - tw - 2 * pad, y1 - h, x1, y1], radius=max(2, round(6 * s)), fill=(0, 0, 0, 205))
    d.text((x1 - tw - pad, y1 - h + pad / 2 - 1), '25:46', font=f, fill=(255, 255, 255, 255))
    return Image.alpha_composite(im, ov).convert('RGB')

def sahte(w, h, i):
    """renkli sahte kapak: doygun zemin, büyük yazı, yüz yerine daire"""
    P = [((230, 40, 40), (255, 210, 0), 'ROMA\nÇÖKTÜ!'), ((20, 120, 230), (255, 255, 255), '10 GİZEMLİ\nGERÇEK'),
         ((255, 170, 0), (20, 20, 20), 'BUNU\nBİLMİYORDUN'), ((40, 170, 90), (255, 255, 255), 'MISIR\nPİRAMİTLERİ'),
         ((150, 40, 200), (255, 240, 120), 'NİETZSCHE\n5 DAKİKADA'), ((240, 90, 150), (255, 255, 255), 'OSMANLI\nSARAYI')]
    bg, fg, t = P[i % len(P)]
    im = Image.new('RGB', (w, h), bg); d = ImageDraw.Draw(im)
    d.ellipse([w * .58, h * .12, w * .95, h * .95], fill=tuple(min(255, c + 60) for c in bg), outline=(20, 20, 20), width=max(1, w // 120))
    d.ellipse([w * .68, h * .3, w * .74, h * .4], fill=(20, 20, 20)); d.ellipse([w * .8, h * .3, w * .86, h * .4], fill=(20, 20, 20))
    f = font(max(8, int(h * .2)))
    d.multiline_text((w * .05, h * .12), t, font=f, fill=fg, spacing=2, stroke_width=max(1, w // 160), stroke_fill=(0, 0, 0))
    return im

BASLIK = "Kayıp Cennet: Şeytan Cehennemden Neden Kaçamadı? | Milton"
def akis(kapaklar, koyu, out):
    """mobil ana sayfa (tek sütun, 390 dp ≈ 780 px) + önerilen listesi (168×94) yan yana"""
    bg, fg, gr = ((15, 15, 15), (241, 241, 241), (170, 170, 170)) if koyu else ((255, 255, 255), (15, 15, 15), (96, 96, 96))
    mw = 780; th = round(mw * 9 / 16)
    items = []
    for k, (ad, im) in enumerate(kapaklar): items += [('s', k * 2), ('k', im)]
    items += [('s', 5)]
    # mobil sütun: sahte, bizimki, sahte ... (en çok 4 öğe: ekrana sığan kadar)
    seq = [items[0], items[1], items[2]] if len(items) >= 3 else items
    H = len(seq) * (th + 150) + 40; side_w = 900
    canvas = Image.new('RGB', (mw + 80 + side_w, max(H, 7 * 120 + 80)), bg); d = ImageDraw.Draw(canvas)
    y = 20
    for kind, v in seq:
        im = sahte(mw, th, v) if kind == 's' else v.resize((mw, th), Image.LANCZOS)
        canvas.paste(rozet(im, mw), (20, y))
        d.ellipse([20, y + th + 18, 92, y + th + 90], fill=(120, 120, 120))
        tt = BASLIK if kind == 'k' else 'Bu Video Her Şeyi Değiştirecek | Tarih Belgeseli'
        d.text((110, y + th + 16), tt[:44], font=font(30), fill=fg); d.text((110, y + th + 56), tt[44:] or 'Kanal Adı · 12 B görüntüleme · 2 gün önce', font=font(26, False), fill=gr)
        y += th + 150
    # önerilen listesi (masaüstü yan sütun): 168×94, ×2 piksel yoğunluğu ile 336×188 gösterilir
    x0 = mw + 80; y = 20; d.text((x0, y), 'Önerilen (168×94, 2× büyütülmüş)', font=font(24), fill=gr); y += 44
    lst = [('s', 0), ('k', kapaklar[0][1]), ('s', 1), ('s', 2)] + ([('k', kapaklar[1][1])] if len(kapaklar) > 1 else []) + [('s', 3), ('s', 4)]
    for kind, v in lst[:7]:
        im = sahte(168, 94, v) if kind == 's' else v.resize((168, 94), Image.LANCZOS)
        im = rozet(im, 168).resize((336, 188), Image.NEAREST)
        canvas.paste(im, (x0, y))
        tt = BASLIK if kind == 'k' else 'Tarihin En Büyük Sırrı Ortaya Çıktı'
        d.text((x0 + 352, y + 6), tt[:26], font=font(26), fill=fg); d.text((x0 + 352, y + 42), tt[26:52], font=font(26), fill=fg)
        d.text((x0 + 352, y + 82), 'Zaman Kuryesi · 1 B görüntüleme', font=font(22, False), fill=gr)
        y += 204
    canvas.save(out, quality=90)

def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    kap = [(os.path.splitext(os.path.basename(p))[0], Image.open(p).convert('RGB')) for p in sys.argv[2:]]
    for ad, im in kap:
        im = im.resize((1280, 720), Image.LANCZOS) if im.size != (1280, 720) else im
        # küçültmeler yan yana
        sizes = [(246, 138), (168, 94), (120, 68)]
        c = Image.new('RGB', (246 + 168 + 120 + 80, 160), (40, 40, 40)); x = 20
        for w, h in sizes: c.paste(rozet(im.resize((w, h), Image.LANCZOS), w), (x, 10)); x += w + 20
        c.save(f'{out}/{ad}_kucuk.png')
        c.resize((c.width * 2, c.height * 2), Image.NEAREST).save(f'{out}/{ad}_kucuk2x.png')
        im.filter(ImageFilter.GaussianBlur(8)).save(f'{out}/{ad}_bulanik.jpg', quality=90)
        im.resize((168, 94), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2)).resize((640, 358), Image.LANCZOS).save(f'{out}/{ad}_bulanik168.jpg', quality=90)
        g = ImageOps.grayscale(im); g.save(f'{out}/{ad}_gri.jpg', quality=90)
        # gri değer histogramı özeti
        hist = g.histogram(); n = sum(hist)
        koyu = sum(hist[:60]) / n; acik = sum(hist[200:]) / n
        b = rozet(im, 1280); d = ImageDraw.Draw(b); d.rectangle(BADGE, outline=(255, 0, 0), width=3)
        b.save(f'{out}/{ad}_rozet.jpg', quality=90)
        # TV boyu: 1920 genişlik (55" TV'de ~ 1,2 m kapak), uzaktan bakış için 480'e küçültülmüş hâli de
        im.resize((1920, 1080), Image.LANCZOS).save(f'{out}/{ad}_tv.jpg', quality=88)
        im.resize((480, 270), Image.LANCZOS).save(f'{out}/{ad}_tv_uzak.jpg', quality=90)
        print(f'{ad}: koyu piksel %{koyu*100:.0f}, açık piksel %{acik*100:.0f}')
    akis(kap, True, f'{out}/akis_koyu.jpg'); akis(kap, False, f'{out}/akis_acik.jpg')
    # karşılaştırma tablosu: her kapak tam (640) + 168 (2×) + bulanık
    rows = []
    for ad, im in kap:
        r = Image.new('RGB', (640 + 336 + 320 + 60, 380), (30, 30, 30)); d = ImageDraw.Draw(r)
        r.paste(rozet(im.resize((640, 360), Image.LANCZOS), 640), (10, 10))
        r.paste(rozet(im.resize((168, 94), Image.LANCZOS), 168).resize((336, 188), Image.NEAREST), (660, 10))
        r.paste(im.resize((168, 94), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2)).resize((320, 180)), (1010, 10))
        d.text((660, 210), ad, font=font(22), fill=(230, 230, 230))
        rows.append(r)
    T = Image.new('RGB', (rows[0].width, 380 * len(rows)), (30, 30, 30))
    for i, r in enumerate(rows): T.paste(r, (0, 380 * i))
    T.save(f'{out}/karsilastirma.jpg', quality=90)

if __name__ == '__main__': main()

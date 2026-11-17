#!/usr/bin/env python3
"""Kapak odak ölçümü: göz ilk nereye gider? (spektral artık belirginlik haritası)

Kapak kuralı (CLAUDE.md, Kapak dersleri): tek odak olsun ve karenin en parlak noktası orası olsun;
ikinci bir lekenin odağı bölmesi istenmez. Bu araç kuralı gözle değil sayıyla denetler.

Yöntem: Hou & Zhang, "Saliency Detection: A Spectral Residual Approach" (CVPR 2007). Eğitilmiş model yok,
lisans sorunu yok, yalnız numpy + PIL. Parlaklık ve iki renk karşıtlığı kanalına bakar. Yüz ve yazı anlamını
bilmez: yalnız gözün ilk saniyede neyi "farklı" bulacağını tahmin eder. Tıklanmayı tahmin ETMEZ (en kalabalık
kapak Sisifos'unki kanalın en iyi tıklananı; en temiz tek odak Milton'da ve TO düşük). Soru yalnız şu:
"göz amaçladığımız yere mi gidiyor?" Kesin yargı değil, kurula verilen bir ölçümdür.

Kullanım:
  python3 araclar/kapak/odak.py kapak.jpg [kapak2.jpg ...] [--cikti klasor]
Çıktı: her kapak için <ad>_odak.png (kapak + ısı haritası + odak halkaları) ve ekrana bir satır:
  odak sayısı (en güçlünün ≥ %60'ı olan ayrı tepeler), 1. odağın yeri, 2./1. oranı,
  süre rozeti bölgesine (sağ alt) düşen pay.
"""
import argparse, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

GEN = 128          # analiz genişliği (yöntemin önerdiği küçük ölçek)
ESIK = 0.60        # ayrı odak sayılmak için en güçlü tepeye oranı


def kutu(a, r):
    """r yarıçaplı kutu ortalaması (kenarlar yansıtılarak)."""
    p = np.pad(a, r, mode='reflect')
    c = p.cumsum(0).cumsum(1)
    c = np.pad(c, ((1, 0), (1, 0)))
    k = 2 * r + 1
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def _kanal(g0):
    """Tek kanalın spektral artık haritası (kenar artığına karşı yansıtarak genişletilir)."""
    ph, pw = g0.shape[0] // 4, g0.shape[1] // 4
    g = np.pad(g0, ((ph, ph), (pw, pw)), mode='reflect')
    F = np.fft.fft2(g)
    logA = np.log(np.abs(F) + 1e-9)
    artik = logA - kutu(logA, 1)                       # spektral artık
    s = np.abs(np.fft.ifft2(np.exp(artik + 1j * np.angle(F)))) ** 2
    return s[ph:ph + g0.shape[0], pw:pw + g0.shape[1]]


def belirginlik(img):
    """0..1 arası belirginlik haritası (analiz ölçeğinde). Parlaklık + iki renk karşıtlığı kanalı
    (kırmızı–yeşil, mavi–sarı): siyah üstündeki turuncu alev gibi renkle ayrılan odaklar griye çevrilince kaybolur."""
    w, h = img.size
    k = np.asarray(img.convert('RGB').resize((GEN, max(1, round(GEN * h / w))), Image.BILINEAR), dtype=np.float64) / 255.0
    R, G, B = k[..., 0], k[..., 1], k[..., 2]
    kanallar = [(R + G + B) / 3, R - G, B - (R + G) / 2]
    toplam = 0
    for c in kanallar:
        if c.std() < 1e-3: continue                     # renksiz kapakta boş kanal
        m = _kanal(c)
        toplam = toplam + m / (m.max() + 1e-12) * min(1.0, c.std() / 0.08)   # kanalı, görüntüdeki gerçek renk farkı kadar say
    s = np.asarray(Image.fromarray((toplam / toplam.max() * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), dtype=np.float64)
    s -= s.min()
    return s / (s.max() + 1e-9)


def tepeler(s, esik=ESIK):
    """Eşiği aşan ayrı bölgeler (4-komşuluk); her biri (tepe değeri, y, x, alan)."""
    m = s >= esik * s.max()
    etiket = np.zeros(s.shape, int); n = 0; sonuc = []
    for y0, x0 in zip(*np.nonzero(m)):
        if etiket[y0, x0]: continue
        n += 1; yigin = [(y0, x0)]; etiket[y0, x0] = n; noktalar = []
        while yigin:
            y, x = yigin.pop(); noktalar.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < s.shape[0] and 0 <= xx < s.shape[1] and m[yy, xx] and not etiket[yy, xx]:
                    etiket[yy, xx] = n; yigin.append((yy, xx))
        ys, xs = zip(*noktalar)
        i = int(np.argmax([s[a, b] for a, b in noktalar]))
        sonuc.append((s[ys[i], xs[i]], ys[i], xs[i], len(noktalar)))
    return sorted(sonuc, reverse=True)


def olc(yol, cikti):
    img = Image.open(yol).convert('RGB')
    W, H = img.size
    s = belirginlik(img)
    sh, sw = s.shape
    tp = tepeler(s)
    # süre rozeti: 1920x1080 ölçeğinde x 1440–1874, y 829–1034 (CLAUDE.md) → oranlar
    r = s[int(sh * 829 / 1080):int(sh * 1034 / 1080), int(sw * 1440 / 1920):int(sw * 1874 / 1920)]
    rozet = r.sum() / s.sum()
    oran = tp[1][0] / tp[0][0] if len(tp) > 1 else 0.0
    # görsel: kapak üstüne ısı haritası + halkalar
    isi = Image.fromarray((s * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    a = np.asarray(isi, dtype=np.float64) / 255
    renk = np.stack([np.clip(a * 2, 0, 1), np.clip(a * 2 - 1, 0, 1), np.zeros_like(a)], -1) * 255
    taban = np.asarray(img.convert('L').convert('RGB'), dtype=np.float64) * 0.55
    karisim = (taban * (1 - a[..., None] * 0.8) + renk * a[..., None] * 0.8).clip(0, 255).astype(np.uint8)
    out = Image.fromarray(karisim); d = ImageDraw.Draw(out)
    for i, (v, y, x, alan) in enumerate(tp[:4]):
        cx, cy, rr = x * W / sw, y * H / sh, max(18, (alan ** .5) * W / sw * .7)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(255, 255, 255) if i == 0 else (90, 200, 255), width=4 if i == 0 else 3)
        d.text((cx + rr + 6, cy - 10), str(i + 1), fill=(255, 255, 255))
    d.rectangle([W * 1440 / 1920, H * 829 / 1080, W * 1874 / 1920, H * 1034 / 1080], outline=(255, 80, 80), width=2)
    ust = os.path.basename(os.path.dirname(os.path.abspath(yol)))
    ad = (ust + '_' if ust not in ('kapak', '') else os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(yol)))) + '_') + os.path.splitext(os.path.basename(yol))[0]
    hedef = os.path.join(cikti, ad + '_odak.png')
    yan = Image.new('RGB', (W * 2 + 8, H), (40, 40, 40)); yan.paste(img, (0, 0)); yan.paste(out, (W + 8, 0))
    yan.resize((yan.width // 2, yan.height // 2)).save(hedef)
    y1, x1 = tp[0][1] / sh, tp[0][2] / sw
    return dict(ad=ad, odak=len(tp), yer=f'x%{x1*100:.0f} y%{y1*100:.0f}', oran=oran, rozet=rozet, png=hedef)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('kapaklar', nargs='+')
    ap.add_argument('--cikti', default='.')
    a = ap.parse_args()
    os.makedirs(a.cikti, exist_ok=True)
    print(f"{'kapak':32s} {'odak':>4s}  {'1. odak':14s} {'2./1.':>6s} {'rozet':>6s}")
    for k in a.kapaklar:
        r = olc(k, a.cikti)
        uyari = '  ← 2. tepe neredeyse eşit' if r['oran'] >= .9 else ''
        print(f"{r['ad'][:32]:32s} {r['odak']:4d}  {r['yer']:14s} {r['oran']:6.2f} {r['rozet']*100:5.1f}%{uyari}")


if __name__ == '__main__':
    main()

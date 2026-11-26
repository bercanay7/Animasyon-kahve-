#!/usr/bin/env python3
"""Kapak test seti: CLAUDE.md "Kapak kuralları → Test seti" maddelerini tek sayfada toplar ve ölçer.

Sayfa (<ad>_test.jpg):
  - tam boy (süre rozeti bölgesi kırmızı, yazı kutusu yeşil);
  - gerçek boyda küçültmeler: 246×138, 168×94, 120×68;
  - gri değer; odak ısı haritası (odak.py);
  - koyu ve açık mobil akış taklidi (başlık ve süre rozetiyle); TV boyu (salon ekranında bir satır).
Ölçüm (<ad>_test.txt ve ekran):
  - boyut ve dosya (1280×720, < 2 MB);
  - odak: tepe sayısı, 1. tepenin yeri, 2./1. oranı, rozete düşen pay;
  - en parlak bölge: yazı hariç en parlak %0,5 pikselin ağırlık merkezi (kural 4: en parlak nokta odaktaki nesne);
  - yazı (yalnız --yazisiz verilirse; iki kare farkından): kutu, satır sayısı, en büyük harf yüksekliği (% kare),
    sol yarıda mı, rozete binen yazı pikseli, yazı/zemin parlaklık farkı.
Araç işaret koyar, karar vermez; "kapağı kim beğenir" sorusuna cevap vermez.

Kullanım:
  python3 araclar/kapak/test_seti.py kapak/A.jpg --yazisiz kapak/A_yazisiz.jpg \
      --baslik "Gılgamış: Öleceğini Bile Bile Nasıl Yaşanır?" --sure 12:40 --cikti kapak/test
"""
import argparse, os, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import odak  # noqa: E402

ROZET = (1440 / 1920, 829 / 1080, 1874 / 1920, 1034 / 1080)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def font(px, kalin=False):
    try:
        return ImageFont.truetype(FONT_B if kalin else FONT, px)
    except OSError:
        return ImageFont.load_default()


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def yazi_maskesi(img, yazisiz):
    a = np.asarray(img, dtype=np.int16); b = np.asarray(yazisiz.resize(img.size, Image.BILINEAR), dtype=np.int16)
    m = np.abs(a - b).max(-1) > 40
    # tek tük kodlama gürültüsünü at: 3×3 en az 4 komşu
    k = np.pad(m, 1).astype(np.int8)
    say = sum(k[1 + dy:k.shape[0] - 1 + dy, 1 + dx:k.shape[1] - 1 + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    return m & (say >= 4)


def yazi_olcumu(img, m):
    W, H = img.size
    if m.sum() < 50:
        return None
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    # satırlar: yatay izdüşümde boşlukla ayrılan bantlar (Türkçe nokta ve çengel ana gövdeye 25 px'ten yakın)
    satir = m.sum(1) > max(3, m.sum(1).max() * .04)
    bantlar, i = [], 0
    while i < H:
        if satir[i]:
            j = i
            while j < H and satir[j]:
                j += 1
            bantlar.append([i, j]); i = j
        else:
            i += 1
    birlesik = []
    for b in bantlar:
        # 1–5 px'lik delik: koyu yazı zemindeki koyu çizgiyle kesişince fark maskesi deliniyor (Lale); aynı satırdır
        if birlesik and (b[0] - birlesik[-1][1] < H * .008 or (b[0] - birlesik[-1][1] < H * .025 and (b[1] - b[0] < H * .06 or birlesik[-1][1] - birlesik[-1][0] < H * .06))):
            birlesik[-1][1] = b[1]
        else:
            birlesik.append(b)
    birlesik = [b for b in birlesik if b[1] - b[0] > H * .03]
    # harf yüksekliği: satırın gövdesi (nokta ve çengel hariç) = satırdaki en yoğun bölgenin yüksekliği
    yukseklik = []
    for a, b in birlesik:
        prof = m[a:b].sum(1); ana = np.nonzero(prof > prof.max() * .35)[0]
        yukseklik.append((ana.max() - ana.min() + 1) if len(ana) else b - a)
    rx0, ry0, rx1, ry1 = [v * s for v, s in zip(ROZET, (W, H, W, H))]
    rozet = int(m[int(ry0):int(ry1), int(rx0):int(rx1)].sum())
    L = lum(np.asarray(img, dtype=np.float64))
    halka = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)), dtype=bool) & ~m
    kontrast = L[m].mean() - L[halka].mean() if halka.any() else 0
    return dict(kutu=(int(x0), int(y0), int(x1), int(y1)), satir=len(birlesik),
                harf=max(yukseklik) / H if yukseklik else 0, sol=x1 < W * .6, sag_kenar=x1 / W,
                ust=y0 / H, alt=y1 / H, rozet=rozet, kontrast=kontrast, yazi_L=L[m].mean())


def en_parlak(img, m=None):
    W, H = img.size
    L = lum(np.asarray(img.filter(ImageFilter.GaussianBlur(W / 320)), dtype=np.float64))
    if m is not None:
        L = np.where(np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)), dtype=bool), 0, L)
    esik = np.quantile(L, .995)
    ys, xs = np.nonzero(L >= esik)
    return xs.mean() / W, ys.mean() / H, float(esik)


def mobil(img, baslik, sure, koyu):
    G = 390; th = round(G * 9 / 16)
    zemin, yazi, gri = ((15, 15, 15), (241, 241, 241), (170, 170, 170)) if koyu else ((255, 255, 255), (15, 15, 15), (96, 96, 96))
    out = Image.new('RGB', (G, th + 112), zemin); out.paste(img.resize((G, th), Image.LANCZOS), (0, 0))
    d = ImageDraw.Draw(out); f = font(12, True)
    tw = d.textlength(sure, font=f); d.rounded_rectangle([G - tw - 16, th - 24, G - 6, th - 6], 4, fill=(0, 0, 0, 200)); d.text((G - tw - 11, th - 22), sure, fill=(255, 255, 255), font=f)
    d.ellipse([12, th + 12, 48, th + 48], fill=(70, 62, 48))
    ft = font(15, True); kelimeler, satirlar, s = baslik.split(), [], ''
    for k in kelimeler:
        if d.textlength((s + ' ' + k).strip(), font=ft) > G - 76:
            satirlar.append(s); s = k
        else:
            s = (s + ' ' + k).strip()
    satirlar.append(s)
    if len(satirlar) > 2:
        satirlar = satirlar[:2]; satirlar[1] = satirlar[1][:max(0, len(satirlar[1]) - 2)] + '…'
    for i, s in enumerate(satirlar):
        d.text((60, th + 12 + i * 20), s, fill=yazi, font=ft)
    d.text((60, th + 14 + len(satirlar) * 20), 'Zaman Kuryesi · 1,2 B görüntüleme · 1 gün önce', fill=gri, font=font(12))
    return out


def tv(img, baslik):
    # salon ekranı 1920 genişlikte satırda ~ 4 kapak (her biri ~ 430 px); sayfada yarı ölçek, 3 m'den bakış ≈ masaüstünde 1/3
    out = Image.new('RGB', (960, 300), (18, 18, 18)); d = ImageDraw.Draw(out)
    for i in range(4):
        x = 20 + i * 235
        if i == 1:
            out.paste(img.resize((215, 121), Image.LANCZOS), (x, 40))
            d.rectangle([x - 3, 37, x + 218, 164], outline=(240, 240, 240), width=3)
            d.text((x, 172), baslik[:30] + ('…' if len(baslik) > 30 else ''), fill=(230, 230, 230), font=font(13, True))
        else:
            d.rectangle([x, 40, x + 215, 161], fill=(52 + 9 * i, 48, 44)); d.text((x, 172), 'başka video', fill=(120, 120, 120), font=font(13))
    d.text((20, 10), 'TV satırı (seçili kapak çerçeveli)', fill=(150, 150, 150), font=font(13))
    return out


def sayfa(yol, img, yazisiz, baslik, sure, cikti, ad):
    W, H = 1280, 720
    img = img.resize((W, H), Image.LANCZOS) if img.size != (W, H) else img
    m = yazi_maskesi(img, yazisiz) if yazisiz is not None else None
    yo = yazi_olcumu(img, m) if m is not None else None
    bx, by, bes = en_parlak(img, m)
    with tempfile.TemporaryDirectory() as gecici:   # odak.py çıktısı geçici klasöre: depodaki aynı adlı eski odak dosyası ezilmesin
        od = odak.olc(yol, gecici)
        isi = Image.open(od['png']); isi = isi.crop((isi.width // 2 + 4, 0, isi.width, isi.height)).resize((640, 360))

    P = Image.new('RGB', (1960, 1520), (34, 34, 34)); d = ImageDraw.Draw(P); fl = font(18, True)
    tam = img.copy(); dt = ImageDraw.Draw(tam)
    dt.rectangle([ROZET[0] * W, ROZET[1] * H, ROZET[2] * W, ROZET[3] * H], outline=(255, 70, 70), width=3)
    if yo:
        dt.rectangle(yo['kutu'], outline=(80, 255, 120), width=2)
    dt.ellipse([bx * W - 14, by * H - 14, bx * W + 14, by * H + 14], outline=(255, 255, 0), width=3)
    P.paste(tam, (20, 44)); d.text((20, 14), f'{ad}: tam boy (kırmızı: süre rozeti, yeşil: yazı, sarı halka: yazı hariç en parlak bölge)', fill=(230, 230, 230), font=fl)
    x = 1330; y = 44
    for w, h in ((246, 138), (168, 94), (120, 68)):
        d.text((x, y - 24), f'{w}×{h}', fill=(200, 200, 200), font=fl); P.paste(img.resize((w, h), Image.LANCZOS), (x, y)); y += h + 40
    d.text((x, y - 24), 'gri değer', fill=(200, 200, 200), font=fl); P.paste(img.convert('L').convert('RGB').resize((320, 180), Image.LANCZOS), (x, y))
    y = 800
    d.text((20, y - 26), 'odak ısı haritası', fill=(200, 200, 200), font=fl); P.paste(isi, (20, y))
    d.text((690, y - 26), 'mobil, koyu', fill=(200, 200, 200), font=fl); P.paste(mobil(img, baslik, sure, True), (690, y))
    d.text((1100, y - 26), 'mobil, açık', fill=(200, 200, 200), font=fl); P.paste(mobil(img, baslik, sure, False), (1100, y))
    P.paste(tv(img, baslik), (20, y + 380))
    satirlar = [
        f"dosya: {img.size[0]}×{img.size[1]}, {os.path.getsize(yol) / 1e6:.2f} MB" + ('' if os.path.getsize(yol) < 2e6 else '  ← 2 MB üstü'),
        f"odak: {od['odak']} tepe, 1.: {od['yer']}, 2./1. {od['oran']:.2f}, rozette %{od['rozet'] * 100:.1f}",
        f"yazı hariç en parlak bölge: x%{bx * 100:.0f} y%{by * 100:.0f} (L≥{bes:.0f})",
    ]
    if yo:
        satirlar += [
            f"yazı kutusu: x%{yo['kutu'][0] / W * 100:.0f}–%{yo['sag_kenar'] * 100:.0f}, y%{yo['ust'] * 100:.0f}–%{yo['alt'] * 100:.0f}; {yo['satir']} satır"
            + ('' if yo['sol'] else '  ← sol yarıda değil') + ('' if yo['satir'] <= 2 else '  ← 2 satırdan fazla'),
            f"en büyük harf yüksekliği: kare %{yo['harf'] * 100:.1f}" + ('' if yo['harf'] >= .18 else '  ← %18 altı'),
            f"rozete binen yazı pikseli: {yo['rozet']}" + ('' if yo['rozet'] == 0 else '  ← rozete biniyor'),
            f"yazı/zemin parlaklık farkı: {yo['kontrast']:+.0f} (yazı L {yo['yazi_L']:.0f})",
        ]
    elif yazisiz is None:
        satirlar.append('yazı ölçümü yok (--yazisiz verilmedi)')
    for i, s in enumerate(satirlar):
        d.text((1000, y + 400 + i * 26), s, fill=(235, 235, 235), font=font(16))
    hedef = os.path.join(cikti, ad + '_test.jpg'); P.save(hedef, quality=88)
    with open(os.path.join(cikti, ad + '_test.txt'), 'w') as f:
        f.write('\n'.join(satirlar) + '\n')
    return hedef, satirlar


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('kapak'); ap.add_argument('--yazisiz'); ap.add_argument('--baslik', default='Başlık')
    ap.add_argument('--sure', default='10:00'); ap.add_argument('--cikti', default='.'); ap.add_argument('--ad')
    a = ap.parse_args(); os.makedirs(a.cikti, exist_ok=True)
    img = Image.open(a.kapak).convert('RGB')
    yz = Image.open(a.yazisiz).convert('RGB') if a.yazisiz else None
    ad = a.ad or os.path.splitext(os.path.basename(a.kapak))[0]
    hedef, satirlar = sayfa(a.kapak, img, yz, a.baslik, a.sure, a.cikti, ad)
    print(hedef); print('\n'.join('  ' + s for s in satirlar))


if __name__ == '__main__':
    main()

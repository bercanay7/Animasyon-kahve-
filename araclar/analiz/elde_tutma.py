#!/usr/bin/env python3
"""Studio mobil "Kitleyi Elde Tutma" ekran görüntüsünden eğriyi okur, altyazıyla eşler.

Kullanım:
  python3 elde_tutma.py ekran.png 8:03 [altyazi.srt] [--json cikti.json] [--kirp x0,y0,x1,y1]

- --kirp: yalnız grafik alanını oku (başlıktaki küçük resimde kırmızı/pembe varsa şart; Mary Stuart, 1170×2532 ekran: 200,1680,1105,2235).

- Süre: grafiğin sağ altındaki değer (videonun süresi).
- Eğri pembe çizgi; ızgara çizgileri %100 / %66 / %33 / %0 (Studio mobil, koyu tema).
- Ölçüm Studio'nun "0:30 civarında %X" cümlesiyle karşılaştırılarak doğrulanır (Ran: 66,7 / 66).
- Az izlenmede (≈100 izleyici) bir izleyici ≈ 1 puan: tek videodaki küçük kıpırtı ders değildir.
"""
import sys, json
from PIL import Image

def pembe(c):
    r, g, b = c[:3]
    return r > 150 and g < 130 and b > 90 and r - g > 70

def oku(yol, kirp=None):
    im = Image.open(yol).convert('RGB')
    if kirp: im = im.crop(kirp)   # yalnız grafik alanı: başlıktaki küçük resimde kırmızı varsa eğri sanılır (Mary Stuart)
    px = im.load(); W, H = im.size
    xs, ys = [], []
    for y in range(H):
        for x in range(W):
            if pembe(px[x, y]): xs.append(x); ys.append(y)
    if not xs: sys.exit('pembe eğri bulunamadı')
    x0, x1, ya, yb = min(xs), max(xs), min(ys), max(ys)
    # ızgara: eğrinin bbox'ının sağına yakın bir sütunda tek renkli ince yatay çizgiler
    xc = x0 + (x1 - x0) * 3 // 4
    izg = []
    for y in range(max(0, ya - 120), min(H, yb + 120)):
        c = px[xc, y]
        if abs(c[0] - c[1]) < 4 and abs(c[1] - c[2]) < 4 and 45 < c[0] < 110 and (not izg or y - izg[-1][-1] > 1):
            izg.append([y])
        elif izg and y - izg[-1][-1] == 1 and abs(c[0] - c[2]) < 4 and 45 < c[0] < 110:
            izg[-1].append(y)
    cizgi = [sum(g) / len(g) for g in izg]
    if len(cizgi) < 4: sys.exit(f'ızgara bulunamadı: {cizgi}')
    y100, y0 = cizgi[0], cizgi[-1]
    return px, x0, x1, ya, yb, y100, y0

def sn(s):
    p = [float(v) for v in s.replace(',', '.').split(':')]
    t = 0
    for v in p: t = t * 60 + v
    return t

def main():
    a = [v for v in sys.argv[1:] if not v.startswith('--')]
    js = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
    if js in a: a.remove(js)
    kirp = tuple(int(v) for v in sys.argv[sys.argv.index('--kirp') + 1].split(',')) if '--kirp' in sys.argv else None
    if kirp: a.remove(sys.argv[sys.argv.index('--kirp') + 1])
    yol, D = a[0], sn(a[1])
    px, x0, x1, ya, yb, y100, y0 = oku(yol, kirp)
    pts = []
    for x in range(x0, x1 + 1):
        ys = [y for y in range(int(y100) - 10, int(y0) + 10) if pembe(px[x, y])]
        if ys:
            pts.append(((x - x0) / (x1 - x0) * D, (y0 - (min(ys) + max(ys)) / 2) / (y0 - y100) * 100))
    v = lambda T: min(pts, key=lambda p: abs(p[0] - T))[1]
    print('t     %')
    for T in [3, 10, 20, 30, 45, 60] + list(range(90, int(D), 30)) + [D - 3]:
        print(f'{int(T//60)}:{int(T%60):02d}  {v(T):5.1f}')
    if len(a) > 2:
        print('\naltyazı başında elde tutma')
        for b in open(a[2], encoding='utf-8').read().strip().split('\n\n'):
            L = b.split('\n'); t = sn(L[1].split(' --> ')[0])
            print(f'{int(t//60)}:{t%60:04.1f}  {v(t):4.0f}%  {" ".join(L[2:])}')
    if js: json.dump(pts, open(js, 'w'))

if __name__ == '__main__':
    main()

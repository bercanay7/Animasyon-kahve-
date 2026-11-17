#!/usr/bin/env python3
"""Çeviri altyazı denetimi: çeviri SRT, kaynak (Türkçe) SRT ile aynı videoya oturuyor mu, okunabiliyor mu?

  python3 araclar/altyazi/denetle.py kaynak.tr.srt ceviri.xx.srt [--cps 17] [--satir 42]

Denetler:
  - altyazı sayısı ve numaraları aynı mı; her altyazının zamanı kaynakla birebir aynı mı (HATA)
  - boş altyazı, 2'den fazla satır (HATA)
  - satır uzunluğu > --satir karakter (UYARI; Netflix/YouTube alışkanlığı 42)
  - okuma hızı (saniyede karakter, boşluklar dahil) > --cps (UYARI); > cps+5 (HATA)
Çıkış kodu: hata varsa 1.
"""
import argparse, re, sys

ZAMAN = re.compile(r'(\d\d):(\d\d):(\d\d)[,.](\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d)[,.](\d\d\d)')


def oku(yol):
    metin = open(yol, encoding='utf-8-sig').read().replace('\r\n', '\n').strip()
    bloklar = []
    for b in re.split(r'\n\s*\n', metin):
        satirlar = b.strip().split('\n')
        if len(satirlar) < 2: continue
        m = ZAMAN.search(satirlar[1])
        if not m: raise SystemExit(f'{yol}: zaman satırı okunamadı: {satirlar[:2]}')
        g = list(map(int, m.groups()))
        bas = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        son = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        bloklar.append(dict(no=satirlar[0].strip(), zaman=satirlar[1].strip(), bas=bas, son=son, satirlar=satirlar[2:]))
    return bloklar


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('kaynak'); ap.add_argument('ceviri')
    ap.add_argument('--cps', type=float, default=17); ap.add_argument('--satir', type=int, default=42)
    a = ap.parse_args()
    K, C = oku(a.kaynak), oku(a.ceviri)
    hata, uyari = [], []
    if len(K) != len(C): hata.append(f'altyazı sayısı farklı: kaynak {len(K)}, çeviri {len(C)}')
    for k, c in zip(K, C):
        yer = f'#{c["no"]}'
        if k['no'] != c['no']: hata.append(f'{yer}: numara kaynakta {k["no"]}')
        if k['zaman'].replace('.', ',') != c['zaman'].replace('.', ','): hata.append(f'{yer}: zaman farklı ({c["zaman"]} / kaynak {k["zaman"]})')
        metin = [s for s in c['satirlar'] if s.strip()]
        if not metin: hata.append(f'{yer}: boş'); continue
        if len(metin) > 2: hata.append(f'{yer}: {len(metin)} satır')
        for s in metin:
            if len(s) > a.satir: uyari.append(f'{yer}: satır {len(s)} karakter: "{s}"')
        sure = max(0.001, c['son'] - c['bas'])
        cps = len(' '.join(metin)) / sure
        if cps > a.cps + 5: hata.append(f'{yer}: okuma hızı {cps:.1f} kr/sn ({sure:.2f} sn): "{" / ".join(metin)}"')
        elif cps > a.cps: uyari.append(f'{yer}: okuma hızı {cps:.1f} kr/sn')
    toplam = sum(len(' '.join(c['satirlar'])) for c in C); sure = sum(c['son'] - c['bas'] for c in C)
    print(f'{a.ceviri}: {len(C)} altyazı, ortalama {toplam / max(sure, 1):.1f} kr/sn, {len(hata)} hata, {len(uyari)} uyarı')
    for h in hata: print('HATA  ', h)
    for u in uyari: print('UYARI ', u)
    sys.exit(1 if hata else 0)


if __name__ == '__main__':
    main()

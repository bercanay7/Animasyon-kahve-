"""Seslendirme bölümleri: senaryo.json → vo/bolumler.json (çekim başına metin, ses etiketleriyle) ve kredi hesabı.
Kullanım: python3 tools/vo_bolumler.py"""
import json
d = json.load(open('senaryo.json')); S = {x['id']: x for x in d['segments']}
# bölüm sınırları (anlatı bölümleri; her çekim ≤ ~1000 karakter)
B = [('s00', 'Kanca', 'A01 A02 A03 A04 A05 A06 A07'),
     ('s01', 'Yol', 'B01 B02 B03 B04 B05 B06'),
     ('s02', 'Alev', 'C01 C02 C03 C04 C05 C06'),
     ('s03', 'Rüzgâr', 'D01 D02 D03 D04 D05 D06 D07 D08 D09'),
     ('s04', 'Çöküş', 'E01 E02 E03 E04 E05 E06 E07'),
     ('s05', 'Efsane', 'F01 F02 F03 F04 F05 F06 F07 F08 F09 F10 F11'),
     ('s06', 'İstanbul', 'G01 G02 G03 G04 G05 G06 G07 G08 G09'),
     ('s07', '1730', 'H01 H02 H03 H04 H05 H06'),
     ('s08', 'Ad', 'I02 I03 I04 I05 I06 I07 I08'),
     ('s09', 'Son', 'J02 J03 J04 J05 J06')]
# ses etiketleri (eleven_v4): cümle başına; yoksa bölümün ilk etiketi sürer
ET = json.load(open('tools/etiketler.json')) if __import__('os').path.exists('tools/etiketler.json') else {}
out = []; tot = 0
for onek, ad, ids in B:
    ids = ids.split()
    for i in ids: assert i in S, i
    parca = []
    for i in ids:
        e = ET.get(i); parca.append((f'[{e}] ' if e else '') + S[i]['tts'])
    metin = ' '.join(parca)
    out.append(dict(onek=onek, ad=ad, ids=ids, metin=metin, karakter=len(metin.replace('[', '').replace(']', '')), karakter_etiketli=len(metin)))
    tot += len(metin)
missing = [k for k in S if not any(k in b['ids'] for b in out)]
assert not missing, missing
json.dump(out, open('vo/bolumler.json', 'w'), ensure_ascii=False, indent=1)
for b in out: print(b['onek'], b['ad'], len(b['ids']), 'cümle', b['karakter_etiketli'], 'karakter')
print('toplam karakter (etiketli):', tot, '| iki çekim ≈', 2 * tot, 'kredi')

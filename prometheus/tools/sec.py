"""Her bölüm için iki çekimden metne en sadık olanı seçer (vo/karsilastirma.json → vo/secim.json).
Ölçüt: karakter hata oranı (CER). Eşitlikte (fark < 0,003) daha kısa çekim, yani daha sıkı tempo seçilir.
Kullanım: python3 tools/sec.py   (önce tools/karsilastir.py)"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
k = json.load(open(os.path.join(ROOT, 'vo', 'karsilastirma.json')))
bol = json.load(open(os.path.join(ROOT, 'vo', 'bolumler.json')))
sel, rap = {}, []
for b in bol:
    a, c = k.get(b['onek'] + '_a'), k.get(b['onek'] + '_b')
    if not a or not c: raise SystemExit(f"eksik çekim: {b['onek']}")
    pick = 'a' if (a['cer'] < c['cer'] - .003 or (abs(a['cer'] - c['cer']) <= .003 and a['sure'] <= c['sure'])) else 'b'
    sel[b['ad']] = f"{b['onek']}_{pick}.mp3"
    ch = a if pick == 'a' else c
    rap.append(f"{b['onek']} {b['ad'][:28]:28}  a {a['cer']:.3f} {a['sure']:6.1f} sn | b {c['cer']:.3f} {c['sure']:6.1f} sn  → {pick}  ({len(ch['farklar'])} fark)")
json.dump(sel, open(os.path.join(ROOT, 'vo', 'secim.json'), 'w'), ensure_ascii=False, indent=1)
print('\n'.join(rap))

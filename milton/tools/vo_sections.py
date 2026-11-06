"""Seslendirme bölümleri: senaryodaki ardışık 'bolum' öbekleri → vo/bolumler.json (sıra, ad, dosya öneki, metin, karakter sayısı).
Kullanım: python3 tools/vo_sections.py"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
segs = json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']
secs = []
for s in segs:
    if not secs or secs[-1]['ad'] != s['bolum']: secs.append({'ad': s['bolum'], 'ids': [], 'metin': []})
    secs[-1]['ids'].append(s['id']); secs[-1]['metin'].append(s['tts'])
for k, sc in enumerate(secs):
    sc['onek'] = f's{k:02d}'; sc['metin'] = ' '.join(sc['metin'])
    sc['karakter'] = len(re.sub(r'\[[^\]]*\]\s*', '', sc['metin']))
json.dump(secs, open(os.path.join(ROOT, 'vo', 'bolumler.json'), 'w'), ensure_ascii=False, indent=1)
for sc in secs: print(sc['onek'], f"{sc['karakter']:5d}", len(sc['ids']), sc['ad'])
print('toplam karakter:', sum(sc['karakter'] for sc in secs), ' (etiketlerle:', sum(len(sc['metin']) for sc in secs), ')')

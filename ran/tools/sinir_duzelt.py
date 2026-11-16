"""Hizalama sınırını elle düzeltir (sessizlik ölçümüne dayanarak): python3 tools/sinir_duzelt.py vo/s03_b.words.json D07 47.59 47.17
Önceki cümlenin kelimeleri [başı, onceki_son] aralığına, bu cümlenin kelimeleri [yeni_bas, kendi sonu] aralığına doğrusal yeniden ölçeklenir."""
import json, sys
f, sid, yeni, onceki_son = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
d = json.load(open(f)); W = d if isinstance(d, list) else d['words']
ids = []; [ids.append(x['id']) for x in W if x['id'] not in ids]
prev = ids[ids.index(sid) - 1]
def scale(ws, a, b):
    s0, e0 = ws[0]['s'], ws[-1]['e']; k = (b - a) / max(1e-6, e0 - s0)
    for x in ws: x['s'] = round(a + (x['s'] - s0) * k, 3); x['e'] = round(a + (x['e'] - s0) * k, 3)
pw = [x for x in W if x['id'] == prev]; cw = [x for x in W if x['id'] == sid]
scale(pw, pw[0]['s'], onceki_son); scale(cw, yeni, cw[-1]['e'] if cw[-1]['e'] > yeni + .5 else yeni + len(cw) * .3)
json.dump(d, open(f, 'w'), ensure_ascii=False)
print(prev, pw[0]['s'], pw[-1]['e'], '|', sid, cw[0]['s'], cw[-1]['e'])

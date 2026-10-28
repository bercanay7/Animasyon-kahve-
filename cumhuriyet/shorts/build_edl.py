"""Shorts kurgu listesi: filmin kendi cümlelerinden kesitler (yeni seslendirme yok) → shorts/edl.js, edl.json
Kurgu (kanca kurulu H1): A02 "Yarın…" ile açılır, 1923 kadrosu ve 1893 sınıfı, A05, G01–G02;
sonda A02'nin başı ("Mustafa Kemal Nutuk'ta…") gelir ve döngü ilk kareye dikişsiz bağlanır.
Kesit sınırları kelime ve cümle çapalarıyla verilir: seslendirme değişince kendiliğinden kayar.
python3 shorts/build_edl.py"""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
t = open(os.path.join(R, 'timeline.js'), encoding='utf-8').read()
C = json.loads(re.search(r'window\.CUES = (\{.*?\});', t).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', t, re.S).group(1))


def w(cid, word, edge='s', off=0.0, n=0):
    """cümledeki n. eşleşen kelimenin başı/sonu + ofset"""
    m = [x for x in WORDS if x['id'] == cid and x['w'].startswith(word)]
    assert len(m) > n, (cid, word)
    return m[n][edge] + off


def c(cid, edge='s', off=0.0):
    return C[cid][edge] + off


# f0/f1: film saniyesi; cx: 9:16 pencerenin film x merkezi (cx0 → cx1 kayar); z: yakınlık; fit: 16:9 karenin tamamı
PLAN = [
    dict(id='A02y', f0=w('A02', 'yarın', off=-.245), f1=w('A02', 'edeceğiz', 'e', .5), cx0=1450, z0=1.0, z1=1.05, capY=1400),  # altyazı ağzı örtmesin
    dict(id='A04a', f0=c('A04', 's', -.26), f1=w('A04', 'yaşlarındaydı', 'e'), cx0=560, cx1=1360),  # 1923 kadrosu boyunca kayar
    dict(id='A04k', f0=w('A04', 'yaşlarındaydı', 'e'), f1=w('A04', 'gün', off=-.24), cx0=1400, cx1=760),  # 1893 sınıfı
    dict(id='A04b', f0=w('A04', 'gün', off=-.24), f1=w('A04', 'ikinci', off=-.12), cx0=780, z0=1.0, z1=1.04),
    dict(id='A04c', f0=w('A04', 'ikinci', off=-.12), f1=c('A04', 'e', .41), cx0=960, z0=1.0, z1=1.06),
    dict(id='A05', f0=c('A05', 's', -.24), f1=c('A05', 'e', .53), cx0=960, z0=1.08, z1=1.2),
    dict(id='G01a', f0=c('G01', 's', -.36), f1=w('G01', 'saat', off=-.11), cx0=560, cx1=700),
    dict(id='G01s', f0=w('G01', 'saat', off=-.11), f1=w('G01', 'mecliste', off=-.1), cx0=950, z0=1.0, z1=1.06),
    dict(id='G01m', f0=w('G01', 'mecliste', off=-.1), f1=w('G01', 'yaşasın', off=-.01), cx0=640, cx1=820),
    dict(id='G01b', f0=w('G01', 'yaşasın', off=-.01), f1=c('G02', 's', -.31), cx0=1380),  # doruk boşluğu kesilmez: müzik yatağı filmle aynı akar (ses kurulu son tur)
    dict(id='G02a', f0=c('G02', 's', -.31), f1=w('G02', 'ismet'), cx0=965, z0=1.0, z1=1.05),
    dict(id='G02b', f0=w('G02', 'ismet'), f1=w('G02', 'genelkurmay', off=-.06), cx0=420),
    dict(id='G02c', f0=w('G02', 'genelkurmay', off=-.06), f1=w('G02', 'üçü', off=-.24), cx0=1550),  # "Genelkurmay'da" tek kalmasın (tipografi)
    dict(id='G02d', f0=w('G02', 'üçü', off=-.24), f1=c('G02', 'e', .6), fit=1),
    dict(id='A02k', f0=c('A02', 's', -.1), f1=w('A02', 'yarın', off=-.245), fit=1, cta=1),  # döngü: dikiş filmdeki yakın plan kesmesinde; sofra bütün görünür, çağrı karenin üstünde
]
EDL, groups, s = [], [], 0.0
for p in PLAN:
    f0, f1 = round(p.pop('f0'), 3), round(p.pop('f1'), 3)
    clip = {**p, 'f': f0, 's': round(s, 3), 'e': round(s + f1 - f0, 3)}
    EDL.append(clip)
    # altyazı: kesit aralığındaki görünen sözcükler (d) ve bitişleri (de: tools/fix_disp.py)
    ws = [x for x in WORDS if x['d'] and f0 - .05 <= x['s'] < f1]
    cur = []
    for x in ws:
        cur.append({'w': x['d'], 's': round(x['s'] - f0 + s, 3), 'e': round(x.get('de', x['e']) - f0 + s, 3)})
        if x['d'][-1] in '.,:?!…”' or len(cur) == 3:
            groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur}); cur = []
    if cur: groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur})
    s += f1 - f0
for i in range(len(groups) - 1): groups[i]['e'] = min(groups[i]['e'] + .25, groups[i + 1]['s'] - .02)
DUR = round(s, 3)
CTA = next(x['s'] for x in EDL if x.get('cta'))
out = {'EDL': EDL, 'GROUPS': groups, 'CTA': CTA, 'DUR': DUR}
open(os.path.join(D, 'edl.js'), 'w').write('// shorts/build_edl.py tarafından üretildi\nwindow.SHORT = ' + json.dumps(out, ensure_ascii=False) + ';\n')
json.dump(out, open(os.path.join(D, 'edl.json'), 'w'), ensure_ascii=False, indent=1)
print('süre', DUR, 'kesit', len(EDL), 'grup', len(groups))
for x in EDL: print(f"{x['id']}: shorts {x['s']:.2f}–{x['e']:.2f}  film {x['f']:.2f}")

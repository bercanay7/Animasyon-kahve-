"""Shorts kurgu listesi: anlatım kelime zamanları + film kesitleri → shorts/edl.js (python3 shorts/build_edl.py)"""
import json, os, re, difflib
D = os.path.dirname(os.path.abspath(__file__))
VO_OFF = .25          # anlatım Shorts'ta bu kadar gecikmeyle başlar
TAKE = 'sh_a'
# doğru yazımlı senaryo (altyazı için); whisper sözcükleri bununla hizalanır
SCRIPT = ("Ölümü zincire vuran bir adam düşün. Korint kralı Sisifos, Zeus'un sırrını ele verdi. Zeus ona Ölüm'ü gönderdi. "
          "Ama Sisifos, Ölüm'ü kendi zincirleriyle bağladı. Dünyada kimse ölmez oldu. Yeraltına indiğinde bile tanrıları kandırıp kaçtı. "
          "Sonunda tanrılar en korkunç cezayı verdi: dev bir kayayı tepeye itmek. Ve kaya… her seferinde geri yuvarlanacaktı. Sonsuza dek. "
          "Ama iki bin yıl sonra Albert Camus, bu hikâyede bambaşka bir şey gördü: “Sisifos'u mutlu hayal etmek gerekir.” "
          "Neden mi? Tam hikâye kanalda. Peki… senin kayan ne?").split()
norm = lambda s: re.sub(r"[^a-zçğıöşü0-9]", '', s.lower().replace('i̇', 'i').replace('â', 'a').replace('camus', 'kamü'))
hw = json.load(open(os.path.join(D, TAKE + '.words.json')))
# whisper bölmeleri: "Zeus" + "'un" → birleştir; "2000" → "iki bin"; "Yer altına" → "yeraltına"
hw2 = []
for w in hw:
    t = w['w']
    if t.startswith("'") and hw2: hw2[-1] = {**hw2[-1], 'w': hw2[-1]['w'] + t, 'e': w['e']}; continue
    if norm(t) == '2000': m = (w['s'] + w['e']) / 2; hw2 += [{'w': 'iki', 's': w['s'], 'e': m}, {'w': 'bin', 's': m, 'e': w['e']}]; continue
    if hw2 and norm(hw2[-1]['w']) == 'yer' and norm(t).startswith('altına'): hw2[-1] = {**hw2[-1], 'w': 'yeraltına', 'e': w['e']}; continue
    hw2.append(w)
a, b = [norm(x) for x in SCRIPT], [norm(x['w']) for x in hw2]
sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
words = [None] * len(SCRIPT)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    for k in range(i2 - i1):
        j = j1 + min(k, max(0, j2 - j1 - 1)) if j2 > j1 else max(0, j1 - 1)
        words[i1 + k] = {'w': SCRIPT[i1 + k], 's': round(hw2[j]['s'] + VO_OFF, 3), 'e': round(hw2[j]['e'] + VO_OFF, 3)}
# altyazı grupları: noktalama ya da en fazla 3 sözcük
groups, cur = [], []
P = '.,:?!…”'
for i, w in enumerate(words):
    cur.append(w)
    rest = next((k for k in range(i + 1, len(words)) if words[k]['w'][-1] in P), len(words) - 1) - i  # sonraki noktalamaya kalan sözcük
    if w['w'][-1] in P or (len(cur) >= 3 and rest > 1) or len(cur) == 4:
        groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur}); cur = []
if cur: groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur})
for i in range(len(groups) - 1): groups[i]['e'] = min(groups[i]['e'] + .25, groups[i + 1]['s'] - .02)
# kurgu: (Shorts başlangıç, film başlangıcı, kırpma merkezi x0→x1, yakınlık, hız, parlama)
def wt(k): return words[k]['s']
EDL = [
    dict(s=0.00, f=0.55, cx0=980),                                   # zincirlenen Ölüm
    dict(s=2.85, f=46.0, cx0=380, cx1=430, z0=1.0),                  # Korint kralı
    dict(s=4.75, f=106.0, cx0=1000),                                 # Zeus'un sırrı
    dict(s=6.65, f=148.6, cx0=1300, z0=1.0, z1=1.08),                # Ölüm gönderilir
    dict(s=9.15, f=167.4, cx0=1060, cy0=560, z0=1.1),                # bileklerine geçirir
    dict(s=10.9, f=170.25, cx0=960),                                 # kilit
    dict(s=12.6, f=177.0, cx0=1000, speed=1.8),                      # kimse ölmez
    dict(s=15.05, f=225.6, cx0=1000),                                # Persefoni inanır
    dict(s=16.6, f=228.6, cx0=380, cx1=430),                         # güneşe döner
    dict(s=18.2, f=244.32, cx0=470),                                 # kaya iner (ceza)
    dict(s=21.4, f=260.4, cx0=820, z0=1.0, z1=1.05),                 # tepeye itmek
    dict(s=23.5, f=265.3, cx0=860),                                  # kayar, yana atılır
    dict(s=25.2, f=268.5, cx0=1143, cx1=719),                        # gürleyerek dibe
    dict(s=27.3, f=283.2, cx0=960),                                  # sonsuza dek
    dict(s=28.15, f=296.0, cx0=960),                                 # iki bin yıl
    dict(s=29.9, f=302.6, cx0=700, cx1=1100),                        # Camus ve kitap
    dict(s=33.3, f=377.9, cx0=860, cx1=900),                         # mutlu
    dict(s=36.3, f=384.0, cx0=960),                                  # vazo
    dict(s=38.9, f=402.3, cx0=960),                                  # senin kayan ne?
]
DUR = round(words[-1]['e'] + 1.6, 2)
for i, c in enumerate(EDL): c['e'] = EDL[i + 1]['s'] if i + 1 < len(EDL) else DUR
CTA = round(wt(SCRIPT.index('Peki…')) - .1, 2)
out = {'EDL': EDL, 'GROUPS': groups, 'CTA': CTA, 'DUR': DUR, 'VO_OFF': VO_OFF, 'TAKE': TAKE}
open(os.path.join(D, 'edl.js'), 'w').write('// shorts/build_edl.py tarafından üretildi\nwindow.SHORT = ' + json.dumps(out, ensure_ascii=False) + ';\n')
json.dump(out, open(os.path.join(D, 'edl.json'), 'w'), ensure_ascii=False, indent=1)
print('süre', DUR, 'klip', len(EDL), 'grup', len(groups), 'CTA', CTA)
for g in groups: print(f"{g['s']:6.2f}-{g['e']:6.2f}", ' '.join(w['w'] for w in g['words']))

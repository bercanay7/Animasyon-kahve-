"""Shorts kurgu listesi: filmden bir kesit + 9:16 kırpma anahtarları + kelime vurgulu altyazı → shorts/edl.js, edl.json
Kullanım: python3 shorts/build_edl.py [a|b]   (varsayılan a)
Anlatım ve altyazı filmin kendi zaman çizelgesinden (timeline.js WORDS, 'd' = altyazı yazımı) gelir; yeni seslendirme gerekmez."""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
src = open(os.path.join(R, 'timeline.js'), encoding='utf8').read()
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', src, re.S).group(1))
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', src, re.S).group(1))
def wd(sid, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == sid and x['w'].startswith(w):
            if k == n: return x
            k += 1
    raise KeyError(f'{sid}@{w}#{n}')

# Kısa A: "Asıl tutsak kim?" (IX, doruk): kanca soru ilk karede; cevap ZEUS · KÖLE / PROMETHEUS · ÖZGÜR; son: terazi döner
# Shorts kurulu tur 1 (RED 6,3) sonrası: ilk karede kanca başlığı, filmin silinen ekran yazılarının yerine Shorts'a özel damga ve künyeler,
# kesme kareleri filmin kendi kesmelerine eşlendi (1084,20 / 1091,45 / 1097,10 / 1102,60 sn), anlamlı altyazı grupları, döngü dikişi kısa.
SHORTS = {
  # Kısa A: "Ben cehennemim" (IV. kitap, Nifates iç konuşması; filmin duygusal doruğu ve A kapağının sözü).
  # Kurgu: kendine sorduğu soru → "Ben cehennemim" → dibin altında dip → pişmanlık sorusu → "gururum yasaklıyor".
  # Yayın koşulu (hassasiyet, kurgu kurulu tur 1): ilk kare edebi çerçeveyi taşır (üstte KAYIP CENNET · MILTON);
  # C04, F02–F04, "Kazanmıştır." ve G14 bu kesitte yok.
  'a': dict(
    TITLE='KAYIP CENNET · MILTON',
    F0=wd('G06', 'o')['s'] - .15, F1=wd('G09b', 'yasaklıyor')['e'] + .35,
    # atlama kesmeleri: sorudan sonraki sessizlik filmin kesmesine (P072, 724,10) kadar; "Bağışlanmaya?"dan sonraki 2,6 sn'lik sessizlik 1,8 sn'ye
    CUTS=[(wd('G06', 'suçlayacaksın')['e'] + .45, 724.10), (751.40, 752.20)],
    KEYS=[(720.70, 560, 600, 1.0), (721.40, 560, 600, 1.0), (722.90, 1300, 600, 1.0),          # iki profil: soran ve sorulan aynı kişi
          (724.10, 1210, 560, 1.0), (728.20, 1200, 540, 1.1),                                    # P072 güneşe karşı
          (728.21, 820, 540, 1.0), (730.53, 840, 540, 1.05),                                    # P072y yakın profil
          (730.54, 930, 560, 1.0), (735.34, 930, 700, 1.18),                                    # P072z kanatların arasından göl; "Ben cehennemim"de yakınlaşma
          (735.35, 620, 540, 1.0), (741.0, 740, 540, 1.0), (746.17, 740, 540, 1.0),             # P073 dibin altında dip (filmin geçişi 735,34–736,04)
          (746.18, 900, 540, 1.0), ('CUT_A', 880, 540, 1.04), ('CUT_B', 880, 520, 1.14), (753.09, 880, 520, 1.16),   # P074 yakın profil; atlama kesmesinde yakınlaşma
          (753.10, 890, 540, 1.0), (760.83, 870, 540, 1.04)],                                   # P075 diz çöker, doğrulur
    LIGHT=[],   # altyazı bantsız: krem yazı + kalın mürekkep kontur (krem kâğıtta da siyah siluette de okunur; bant gri leke bırakıyordu)
    CAP=1235,
    CAPS=[(753.10, 1440, 300)],   # P075: figür kadrajın ortasında; altyazı ayakların altına, kanal çağrısı başlığın altına
    HOOK=dict(l1='PİŞMAN', l2='MIYDI?', e=724.10),   # B kapağının sorusu; cevabı son cümlede ("gururum yasaklıyor")
    TAGS=[(724.10, wd('G07', 'kaçayım')['e'] + .3, 'KAYIP CENNET · IV. 73–75'),
          (wd('G08', 'en')['s'] - .1, wd('G08', 'kalıyor')['e'] + .3, 'KAYIP CENNET · IV. 76–78'),
          (wd('G09', 'pişmanlığa')['s'] - .1, wd('G09', 'bağışlanmaya')['e'] + .4, 'KAYIP CENNET · IV. 79–80'),
          (wd('G09b', 'bir')['s'] - .1, wd('G09b', 'eğmek')['e'] + .4, 'KAYIP CENNET · IV. 81–82')],
    GROUPS=['O hâlde', 'kimi suçlayacaksın?”', '“Vay hâlime!', 'Sonsuz gazaptan,', 'sonsuz umutsuzluktan', 'nereye kaçayım?',
            'Hangi yana kaçsam', 'cehennem.', 'Ben cehennemim.”', '“En derin dipte,', 'beni yutmak için', 'ağzını açan', 'daha derin bir dip var.',
            'Onun yanında,', 'çektiğim cehennem', 'cennet gibi kalıyor.”', 'Bir an yumuşar:', '“Pişmanlığa', 'hiç yer kalmadı mı?', 'Bağışlanmaya?”',
            'Cevabı yine', 'kendisi verir:', '“Bir yol kaldı:', 'boyun eğmek.', 'Ama o sözü bana', 'gururum yasaklıyor.”'],
    CTA=dict(s=wd('G09b', 'ama')['s'], l1='GURUR MU, PİŞMANLIK MI?', l2='TAM HİKÂYE · İLGİLİ VİDEODA')),
}
K = sys.argv[1] if len(sys.argv) > 1 else 'a'
cfg = SHORTS[K]
F0, F1 = cfg['F0'], cfg['F1']
CUTS = cfg.get('CUTS', [])
# film saniyesi → Shorts saati (atlama kesmeleriyle çıkarılan aralıklar düşülür)
def sh(t): return round(t - F0 - sum(max(0, min(t, b) - a) for a, b in CUTS), 3)
cfg['KEYS'] = [((CUTS[-1][0] if k[0] == 'CUT_A' else CUTS[-1][1]) if isinstance(k[0], str) else k[0], *k[1:]) for k in cfg['KEYS']]
DUR = sh(F1)
# altyazı sözcükleri: kesite düşen sözcükler, Shorts saatine kaydırılır
words = [{'w': x['d'] or x['w'], 's': sh(x['s']), 'e': sh(x['e'])} for x in WORDS if x['s'] >= F0 - .05 and x['e'] <= F1 + .05 and (x['d'] or '').strip()]
# gruplar: yapılandırmada elle yazılmış anlam birimleri varsa sözcükler sırayla eşlenir; yoksa noktalama ya da en fazla 3 sözcük
P = '.,:?!…”'
groups, cur = [], []
if cfg.get('GROUPS'):
    i = 0
    for ph in cfg['GROUPS']:
        n = len(ph.split()); cur = words[i:i + n]; i += n
        assert [w['w'] for w in cur] == ph.split(), (ph, [w['w'] for w in cur])
        groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur})
    assert i == len(words), (i, len(words))
else:
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = nxt and nxt['s'] - w['e'] > .45
        if w['w'][-1] in P or len(cur) >= 3 or gap: groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur}); cur = []
    if cur: groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur})
for i in range(len(groups) - 1): groups[i]['e'] = min(groups[i]['e'] + .25, groups[i + 1]['s'] - .02)
# kırpma anahtarlarından kesitler (film kesintisiz: f = F0 + s)
keys = [(max(F0, k[0]), *k[1:]) for k in cfg['KEYS'] if k[0] <= F1]
if keys[0][0] > F0: keys.insert(0, (F0, *keys[0][1:]))
if keys[-1][0] < F1: keys.append((F1, *keys[-1][1:]))
EDL = []
for a, b in zip(keys, keys[1:]):
    s, e = sh(a[0]), sh(b[0])
    if e - s < .02: continue
    light = any(l0 <= a[0] < l1 for l0, l1 in cfg.get('LIGHT', []))
    capY, ctaY = cfg['CAP'], cfg.get('CTAY', 1330)
    for f, cy_, ty_ in cfg.get('CAPS', []):
        if a[0] >= f: capY, ctaY = cy_, ty_
    EDL.append(dict(s=s, e=e, f=round(a[0], 3), cx0=a[1], cx1=b[1], cy0=a[2], cy1=b[2], z0=a[3], z1=b[3], capY=capY, ctaY=ctaY, light=light))
cta = cfg.get('CTA')
CTA = sh(cta['s']) if cta else round(DUR - 2.4, 3)
out = dict(TITLE=cfg['TITLE'], F0=round(F0, 3), F1=round(F1, 3), DUR=DUR, CUTS=[[round(a, 3), round(b, 3)] for a, b in CUTS], CTA=CTA, EDL=EDL, GROUPS=groups, WORDS=words,
           CTA_L=[cta['l1'], cta['l2']] if cta else None,
           HOOK=dict(l1=cfg['HOOK']['l1'], l2=cfg['HOOK']['l2'], e=sh(cfg['HOOK']['e'])) if cfg.get('HOOK') else None,
           TAGS=[dict(s=sh(a_), e=sh(b_), t=t_) for a_, b_, t_ in cfg.get('TAGS', [])],
           TITLE_OFF=[dict(s=sh(a_), e=sh(b_)) for a_, b_ in cfg.get('TITLE_OFF', [])],
           STAMP=dict(s=sh(cfg['STAMP']['s']), s2=sh(cfg['STAMP']['s2']), e=sh(cfg['STAMP']['e'])) if cfg.get('STAMP') else None)
json.dump(out, open(os.path.join(D, 'edl.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(D, 'edl.js'), 'w').write('// shorts/build_edl.py tarafından üretildi\nwindow.SHORT = ' + json.dumps(out, ensure_ascii=False) + ';\n')
print(K, 'süre', DUR, 'sn,', len(EDL), 'kesit,', len(groups), 'altyazı grubu, film', round(F0, 2), '→', round(F1, 2))

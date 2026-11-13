"""Shorts kurgu listesi: filmden kesintisiz bir kesit + 9:16 kırpma anahtarları + kelime vurgulu altyazı → shorts/edl.js, edl.json
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
  'a': dict(
    TITLE='PROMETHEUS',
    F0=wd('J01', 'bu', 1)['s'] - .15, F1=wd('J06', 'tutsak')['e'] + .35,
    # kırpma anahtarları: (film saniyesi, kırpma merkezi x, y, yakınlık); arada yumuşak geçiş, 0,02 sn'den kısa aralık = sert kesme
    # atlama kesmesi: sorudan sonraki 1,37 sn'lik sessizlik 0,6 sn'ye iner (ilk saniyeler); kesmede hafif yakınlaşma, kurgu kesmesi gibi okunur
    CUTS=[(wd('J01', 'kim')['e'] + .35, wd('J02', 'görünüşe')['s'] - .25)],
    KEYS=[(1055.2, 1330, 540, 1.0), (1056.6, 1250, 540, 1.0), ('CUT_A', 1170, 535, 1.0), ('CUT_B', 1150, 535, 1.15), (1062.0, 1050, 520, 1.0), (1066.84, 980, 560, 1.0),
          (1066.85, 980, 560, 1.3), (1072.35, 980, 560, 1.3),            # "Prometheus ise zincirde": sert yakınlaşma, "Erhat sorar"da geri
          (1072.36, 960, 560, 1.0), (1073.8, 960, 540, 1.0), (1077.2, 960, 560, 1.0), (1079.3, 960, 540, 1.0), (1081.5, 960, 540, 1.05),
          (1082.0, 1545, 540, 1.0), (1084.19, 1545, 540, 1.0),           # doruk: kırmızı figürlü Prometheus kadrajın ortasında
          (1084.20, 960, 540, 1.0), (1085.4, 960, 540, 1.0), (1086.3, 380, 540, 1.0), (1087.6, 380, 540, 1.0), (1088.8, 960, 630, 1.2), (1091.44, 960, 630, 1.2),   # saray halkı, sonra çocuklaşan Zeus altyazının üstünde
          (1091.45, 960, 540, 1.0), (1097.09, 960, 540, 1.0),
          (1097.10, 1480, 540, 1.0), (1099.3, 1480, 540, 1.0), (1100.6, 450, 540, 1.0), (1102.55, 450, 540, 1.0),   # krem sayfa: tahttan zinciri tutan Prometheus'a
          (1102.56, 560, 520, 1.0), (1106.35, 560, 520, 1.0), (1106.7, 1500, 760, 1.35), (1109.0, 1500, 760, 1.35)],  # terazi: "sanık özgür"de Prometheus, "görünmeyen"de taht
    LIGHT=[(1097.10, 1102.56)],   # filmin kesmesi 1102,567–1102,573 arasında (Shorts kurulu tur 2)  # açık (sayfa) zeminli aralıklar: altyazı mürekkep renginde
    CAP=1235,
    CAPS=[(1097.10, 720, 1330), (1102.56, 1235, 1330), (1106.7, 470, 1330)],  # (film saniyesinden itibaren) altyazı y, kanal çağrısı y: krem sayfada ve son planda altyazı figürün üstündeki boş alanda
    # ilk karede kanca başlığı (ses kapalı izleyen için soru hemen okunur); "Görünüşe"de söner
    HOOK=dict(l1='ASIL TUTSAK', l2='KİM?', e=wd('J02', 'görünüşe')['s']),
    # künyeler: başlığın altında küçük satır (filmdeki Erhat künyesinin ve adların Shorts karşılığı)
    TAGS=[(wd('J02', 'güçün')['s'] - .1, wd('J02', 'değildir')['e'] + .3, 'GÜÇ (KRATOS) · ZEUS\'UN BUYRUKÇUSU'),
          (wd('J02', 'erhat')['s'] - .1, wd('J04', 've')['s'] + .15, 'AZRA ERHAT · 1967 ÖNSÖZÜ · S. XIII'),
          (wd('J04', 've')['s'] - .1, wd('J06', 'aslında')['e'] + .3, 'AZRA ERHAT · ÖNSÖZ · S. XIV')],   # künyeler üst üste biner: kutu kalır, yazı çapraz geçer
    TITLE_OFF=[(1104.2, 1106.75)],   # "Sanık özgür": Prometheus'un başı başlığın altında, başlık söner
    # damga: filmin ZEUS · KÖLE / PROMETHEUS · ÖZGÜR levhası (notext ile silinir), dikey kadraja göre
    STAMP=dict(s=wd('J04', 'gerçekte')['s'], s2=wd('J04', 'prometeus')['s'], e=1084.20),
    # altyazı grupları: anlam birimleri (kelimeler sırayla eşlenir)
    GROUPS=['Bu sahnede', 'asıl tutsak olan kim?', 'Görünüşe bakılırsa', 'cevap açık.', "Güç'ün sözünü hatırla:", "“Zeus'tan başka",
            'hiç kimse özgür değildir.”', 'Prometheus ise zincirde;', 'ölümsüz olduğu için', 'canına kıyma', 'özgürlüğü bile yok.', 'Erhat sorar:',
            '“Ama bakalım', 'gerçekten de öyle mi?”', 'Ve cevap verir:', '“Gerçekte Zeus köle,', 'Prometheus özgürdür.”', 'Ona göre Zeus,',
            'bütün uşaklarına,', 'dalkavuklarına rağmen,', '“bir çocuk gibi', 'zayıf ve çaresizdir”:', 'Onu yıkımdan', 'kurtarabilecek tek kişi,',
            '“akıl gücünün taşıyıcısı”', "Prometheus'tur.", "Erhat'ın deyişiyle:", '“Zeus tutukladığı', 'düşmanının elinde', 'tutukludur aslında.”',
            'Yani roller', 'yer değiştirmiştir:', 'Sanık özgür,', 'görünmeyen yargıç tutsak.'],
    # kanal çağrısı: Shorts'un açık bıraktığı merak (sır) + tek dokunuşluk yol (İlgili video)
    CTA=dict(s=wd('J06', 'sanık')['s'], l1="PROMETHEUS'UN SIRRI NEYDİ?", l2='TAM HİKÂYE · İLGİLİ VİDEODA')),
}
K = sys.argv[1] if len(sys.argv) > 1 else 'a'
cfg = SHORTS[K]
F0, F1 = cfg['F0'], cfg['F1']
CUTS = cfg.get('CUTS', [])
# film saniyesi → Shorts saati (atlama kesmeleriyle çıkarılan aralıklar düşülür)
def sh(t): return round(t - F0 - sum(max(0, min(t, b) - a) for a, b in CUTS), 3)
cfg['KEYS'] = [((CUTS[0][0] if k[0] == 'CUT_A' else CUTS[0][1]) if isinstance(k[0], str) else k[0], *k[1:]) for k in cfg['KEYS']]
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
    capY, ctaY = cfg['CAP'], 1330
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

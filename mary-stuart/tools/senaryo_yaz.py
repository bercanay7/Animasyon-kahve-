"""mary-stuart/senaryo.json ve senaryo_okuma.md üretir.
Satır: (etiket, altyazı metni, kaynak[, tts metni]). tts verilmezse altyazı metninden üretilir:
rakamlar Türkçe sözcüğe, yabancı adlar okunuş biçimine çevrilir (ElevenLabs Emrullah için).
Kimlikler bölüm harfi + sıra; çıkarılan cümlenin numarası boş kalır (Kafka dersi)."""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── okunuş (yalnız tts) ──
OKU = [("En ma fin est mon commencement", "An ma fen e mon komansman"), ("Calais", "Kale"), ("Brantôme", "Brantom"), ("Stefan Zweig", "Ştefan Tsvayg"), ("Zweig", "Tsvayg"),
       ("Mary Stuart", "Meri Stüart"), ("Stuart", "Stüart"), ("Mary", "Meri"), ("Lord Darnley", "Lord Darnli"), ("Darnley", "Darnli"), ("Bothwell", "Botvel"),
       ("Rizzio", "Ritsio"), ("Holyrood", "Holirud"), ("Leith", "Lit"), ("John Knox", "Con Noks"), ("Knox", "Noks"), ("James Melville", "Ceyms Melvil"),
       ("Melville", "Melvil"), ("Robert Dudley", "Robırt Dadli"), ("Dunbar", "Danbar"), ("Carberry", "Karberi"), ("Loch Leven", "Lok Liven"),
       ("Langside", "Lengsayd"), ("Dundrennan", "Dandrenın"), ("Solway", "Solvey"), ("Workington", "Vörkington"), ("Carlisle", "Karlayl"),
       ("Tutbury", "Tatberi"), ("Sheffield", "Şefild"), ("Chartley", "Çartli"), ("Francis Walsingham", "Frensis Volsingım"), ("Walsingham", "Volsingım"),
       ("Burton", "Börtın"), ("Anthony Babington", "Entıni Bebingtın"), ("Babington", "Bebingtın"), ("Fotheringhay", "Fadıringey"),
       ("Amias Paulet", "Eymiyas Polit"), ("Paulet", "Polit"), ("Davison", "Deyvisın"), ("Westminster Abbey", "Vestminster Ebi"), ("Westminster", "Vestminster"),
       ("Edinburgh", "Edinbıra"), ("Greenwich", "Grinic"), ("James", "Ceyms"), ("Henry", "Henri"), ("Peterborough", "Pitırbırı")]
BIR = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
ON = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
def sayi(n):
    n = int(n); s = []
    if n >= 1000: s.append(('' if n // 1000 == 1 else BIR[n // 1000] + ' ') + 'bin'); n %= 1000
    if n >= 100: s.append(('' if n // 100 == 1 else BIR[n // 100] + ' ') + 'yüz'); n %= 100
    if n >= 10: s.append(ON[n // 10]); n %= 10
    if n: s.append(BIR[n])
    return ' '.join(x.strip() for x in s if x.strip()) or 'sıfır'
def tts_of(t):
    for a, b in OKU: t = re.sub(r'(?<![\wçğıöşüÇĞİÖŞÜ])' + re.escape(a) + r'(?![a-zçğıöşü])', b, t)
    t = re.sub(r"(\d+)'(\w+)", lambda m: sayi(m.group(1)) + m.group(2), t)
    t = re.sub(r'\d+', lambda m: sayi(m.group(0)), t)
    t = t.replace('“', '"').replace('”', '"')
    return ({'i': 'İ', 'ı': 'I'}.get(t[:1]) or t[:1].upper()) + t[1:] if t else t

exec(open(os.path.join(R, 'tools', 'senaryo_veri.py'), encoding='utf-8').read())   # veri: tools/senaryo_veri.py (rev1)
# kimlikler: bölüm harfi + sıra
HARF = {}
for s in S:
    if s['bolum'] not in HARF: HARF[s['bolum']] = chr(ord('A') + len(HARF))
cnt = {}
for s in S:
    h = HARF[s['bolum']]; cnt[h] = cnt.get(h, 0) + 1; s['id'] = f'{h}{cnt[h]:02d}'
out = dict(voice='Emrullah (ElevenLabs; voice_id creative_list_voices ile bulunur)', revizyon='rev1 (18 Kasım 2026): Fable danışman denetimi uygulandı (25 bulgu); kurul yok (kullanıcının kararı)',
           segments=S, **{'not': 'tts: okunuş biçimi (yabancı adlar, rakamlar sözcükle); alt: altyazı. Kaynak kimlikleri kaynak/KAYNAKLAR.md'})
json.dump(out, open(os.path.join(R, 'senaryo.json'), 'w'), ensure_ascii=False, indent=1)
# okuma dosyası + sayımlar
W = sum(len(re.findall(r'\w+', s['alt'])) for s in S); C = sum(len(re.sub(r'^\[[a-z ]+\] ', '', s['tts'])) for s in S)
L = [f'# Mary Stuart: senaryo okuma metni (rev1)', '', f'{len(S)} cümle · {W} kelime · tts {C} karakter · tahmini süre {W / 96:.1f}–{W / 90:.1f} dk (Ran 96 kelime/dk)', '']
cur = None
for s in S:
    if s['bolum'] != cur:
        cur = s['bolum']; L += ['', f'## {HARF[cur]}. {cur}' + (f'  ·  *{s["soru"]}*' if s['soru'] else ''), '']
    L.append(f'- **{s["id"]}** {s["alt"]}  <sub>{s["kaynak"]}</sub>')
open(os.path.join(R, 'senaryo_okuma.md'), 'w').write('\n'.join(L) + '\n')
print(len(S), 'cümle', W, 'kelime', C, 'tts karakter', f'~{W / 96:.1f} dk')

"""YouTube bölüm damgaları: bölüm kartının ilk karesi (sahneler.js bolumKarti ile aynı hesap). python3 tools/damga.py"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = open(os.path.join(ROOT, 'timeline.js'), encoding='utf-8').read()
CUES = json.loads(tl.split('window.CUES = ')[1].split(';\n')[0]); ids = list(CUES)
AD = [('A', 'Kırmızı ve deniz'), ('B', 'Altı günlük kraliçe'), ('C', 'Siste dönüş'), ('D', 'Görmediği kuzen'), ('E', "Holyrood'daki gece"), ('F', 'Bothwell'), ('G', 'Gölün ortasındaki ada'),
      ('H', 'Solway: rakibine sığınmak'), ('I', 'On dokuz yıl'), ('J', 'Bira fıçısındaki mektuplar'), ('K', "Elizabeth, Elizabeth'e karşı"), ('L', 'Kırmızı'), ('M', 'Sonumda başlangıcım')]
for h, ad in AD:
    if h == 'A': t = 0
    else: i = ids.index(h + '01'); t = int(max(CUES[ids[i - 1]]['e'] + .15, CUES[h + '01']['s'] - 1.7))
    print(f'{t // 60}:{t % 60:02d} {ad}')

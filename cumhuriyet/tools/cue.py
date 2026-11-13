"""Cümle zamanlarını yazdırır: python3 tools/cue.py B01 B02 ...  (kimlik verilmezse hepsi)
Ayrıca kelime zamanları için: python3 tools/cue.py -w B03"""
import json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(ROOT, 'timeline.js'), encoding='utf-8').read()
C = json.loads(re.search(r'window\.CUES = (\{.*?\});', t).group(1))
Wd = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', t, re.S).group(1))
dur = float(re.search(r'window\.DUR = ([\d.]+)', t).group(1))
args = sys.argv[1:]; words = '-w' in args; args = [a for a in args if a != '-w']
ids = args or list(C)
print(f'DUR {dur:.2f}')
for i in ids:
    c = C[i]; print(f'{i}: {c["s"]:.2f} – {c["e"]:.2f}')
    if words: print('   ' + '  '.join(f'{w["w"]}@{w["s"]:.2f}' for w in Wd if w['id'] == i))

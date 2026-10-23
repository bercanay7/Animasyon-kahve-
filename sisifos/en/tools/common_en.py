"""Shared helpers for the English dub pipeline."""
import re, json, os
EN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(EN)
LET = 'ABCDEFGH'

def strip_tags(t):
    t = re.sub(r'\[[^\]]*\]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

NUM = {'1942': 'nineteen forty two', '2000': 'two thousand', '100': 'hundred', '1000': 'thousand'}
SPELL = {'neighbour': 'neighbor', 'colour': 'color', 'labour': 'labor', 'ok': 'okay'}

def norm1(w):
    w = w.lower().replace('’', "'").replace('‘', "'")
    w = SPELL.get(w.strip('.,!?:;"“”…'), w)
    w = re.sub(r"s'(s)?(?=[^a-z]*$)", 's', w)   # Sisyphus's / Sisyphus' -> sisyphus
    w = re.sub(r"[^a-z0-9']+", '', w).replace("'", '')
    return w

def norm_words(text):
    text = re.sub(r'(\d)\s*,\s*(\d{3})', r'\1\2', text)
    text = text.replace('…', ' ').replace('—', ' ').replace('-', ' ')
    out = []
    for x in text.split():
        n = norm1(x)
        if not n: continue
        if n in NUM: out += NUM[n].split()
        else: out.append(n)
    return out

def display_words(text):
    """script tokens (tags removed) to show in subtitles, aligned 1:1 with norm_words where possible"""
    return strip_tags(text).split()

def load_script():
    d = json.load(open(os.path.join(EN, 'senaryo_en.json')))
    return d['segments']

def load_cues():
    t = open(os.path.join(ROOT, 'timeline.js')).read()
    cues = json.loads(re.search(r'window\.CUES = (\{.*?\});', t, re.S).group(1))
    dur = float(re.search(r'window\.DUR = ([0-9.]+)', t).group(1))
    return cues, dur

def sections():
    segs = load_script()
    return {L: [s for s in segs if s['id'][0] == L] for L in LET}

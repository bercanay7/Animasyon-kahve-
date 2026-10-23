"""Compare whisper transcripts of each take with the script; prints WER-like score and diffs.
Usage: python3 en/tools/verify_en.py WORDSDIR TAG   (TAG: small, mediumen, small_np, mediumen_np)"""
import sys, json, os, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_en import *
wdir, tag = sys.argv[1], sys.argv[2]; suf = f'.{tag}.words.json'
secs = sections()
res = {}
for k, L in enumerate(LET):
    ref = []
    for s in secs[L]: ref += norm_words(strip_tags(s['tts']))
    for t in 'ab':
        f = os.path.join(wdir, f'e{k}_{t}{suf}')
        if not os.path.exists(f): continue
        hw = json.load(open(f))
        hyp = norm_words(' '.join(w['w'] for w in hw))
        sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
        ops = [(op, ' '.join(ref[a:b]), ' '.join(hyp[c:d])) for op, a, b, c, d in sm.get_opcodes() if op != 'equal']
        S = sum(min(b - a, d - c) for op, a, b, c, d in sm.get_opcodes() if op == 'replace')
        D = sum(max(0, (b - a) - (d - c)) for op, a, b, c, d in sm.get_opcodes() if op in ('replace', 'delete'))
        I = sum(max(0, (d - c) - (b - a)) for op, a, b, c, d in sm.get_opcodes() if op in ('replace', 'insert'))
        wer = (S + D + I) / len(ref)
        lowp = [(w['w'], w['p'], w['s']) for w in hw if w.get('p', 1) < 0.35]
        res[f'e{k}_{t}'] = {'wer': round(wer, 4), 'S': S, 'D': D, 'I': I, 'n': len(ref), 'diffs': ops, 'dur': hw[-1]['e'] if hw else 0, 'lowp': lowp}
        print(f'e{k}_{t} WER {wer:.3f} (S{S} D{D} I{I} / {len(ref)})  last word {hw[-1]["e"] if hw else 0:.1f}s')
        for o in ops: print('    ', o)
        if lowp: print('     low-prob words:', lowp)
json.dump(res, open(os.path.join(wdir, f'verify.{tag}.json'), 'w'), indent=1, ensure_ascii=False)

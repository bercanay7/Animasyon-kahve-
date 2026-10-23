"""QA of the finished English track: re-transcribes en/vo_en.wav with whisper and checks every placed
segment against the script (catches clipped / leaked words at the cuts), timing drift of the word
timestamps, window violations, overlaps, loudness and peaks.  Writes en/tools/qa_en.json.
Usage: python3 en/tools/qa_en.py [model]"""
import json, os, sys, difflib
import numpy as np, soundfile as sf, pyloudnorm as pyln, whisper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_en import *

model = sys.argv[1] if len(sys.argv) > 1 else 'small'
cues, DUR = load_cues()
tl = json.load(open(os.path.join(EN, 'timeline_en.json')))
pc, W = tl['cues'], tl['words']
ids = list(cues)
y, sr = sf.read(os.path.join(EN, 'vo_en.wav'))
rep = {'samples': len(y), 'expected': round(DUR * 48000), 'sr': sr,
       'lufs': round(pyln.Meter(sr).integrated_loudness(y), 2), 'peak_dbfs': round(20 * np.log10(np.abs(y).max()), 2)}
ref = sf.read(os.path.join(ROOT, 'vo', 'vo.wav'))[0]
rep['lufs_tr'] = round(pyln.Meter(48000).integrated_loudness(ref), 2)

# window checks
viol = []
for n, i in enumerate(ids):
    lim = cues[ids[n + 1]]['s'] - .12 if n + 1 < len(ids) else 416.0
    if pc[i]['e'] > lim + 1e-3: viol.append(f'{i} ends {pc[i]["e"]} > {lim:.3f}')
    if n and pc[i]['s'] < pc[ids[n - 1]]['e'] + .12 - 1e-3: viol.append(f'{i} starts {pc[i]["s"]} < prev end + 0.12')
    if abs(pc[i]['s'] - cues[i]['s']) > .351: viol.append(f'{i} start offset {pc[i]["s"] - cues[i]["s"]:.3f}')
rep['window_violations'] = viol

# re-transcribe
m = whisper.load_model(model, download_root=os.environ.get('WHISPER_DIR'))
r = m.transcribe(os.path.join(EN, 'vo_en.wav'), language='en', word_timestamps=True, condition_on_previous_text=False,
                 fp16=False, temperature=0, initial_prompt='Sisyphus, Thanatos, Aegina, Asopus, Autolycus, Ephyra, Corinth, '
                 'Merope, Persephone, Hermes, Tartarus, Camus, Zeus, Ares, Homer.')
hw = [{'w': w['word'].strip(), 's': w['start'], 'e': w['end']} for sg in r['segments'] for w in sg['words']]
segs = {s['id']: s for s in load_script()}
per, used = {}, set()
for n, i in enumerate(ids):
    lo = pc[i]['s'] - .25
    hi = pc[i]['e'] + .25
    got = [k for k, w in enumerate(hw) if lo <= (w['s'] + w['e']) / 2 <= hi]
    used.update(got)
    hyp = norm_words(' '.join(hw[k]['w'] for k in got))
    rr = norm_words(strip_tags(segs[i]['tts']))
    sm = difflib.SequenceMatcher(None, rr, hyp, autojunk=False)
    d = [(op, ' '.join(rr[a:b]), ' '.join(hyp[c:e])) for op, a, b, c, e in sm.get_opcodes() if op != 'equal']
    per[i] = d
leak = [hw[k] for k in range(len(hw)) if k not in used]
# timing drift: our word starts vs. whisper word starts (matched by order inside each segment)
drift = []
for i in ids:
    ours = [w for w in W if w['id'] == i]
    theirs = [w for w in hw if pc[i]['s'] - .25 <= (w['s'] + w['e']) / 2 <= pc[i]['e'] + .25]
    a = [norm1(w['w']) for w in ours]; b = [norm1(w['w']) for w in theirs]
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for q in range(blk.size): drift.append(ours[blk.a + q]['s'] - theirs[blk.b + q]['s'])
drift = np.array(drift)
rep['segment_diffs'] = {k: v for k, v in per.items() if v}
rep['unassigned_words'] = leak
rep['word_start_drift'] = {'n': len(drift), 'median': round(float(np.median(drift)), 3), 'p90_abs': round(float(np.percentile(np.abs(drift), 90)), 3),
                           'max_abs': round(float(np.abs(drift).max()), 3)}
# clicks: big sample jumps relative to local level, and activity outside the placed clips
d = np.abs(np.diff(y))
h = 480; rms = np.sqrt(np.convolve(y ** 2, np.ones(h) / h, 'same')) + 1e-6
rep['click_candidates'] = int(np.sum((d > 0.05) & (d > 15 * rms[1:])))
json.dump(rep, open(os.path.join(EN, 'tools', 'qa_en.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in rep.items()}, ensure_ascii=False, indent=1))

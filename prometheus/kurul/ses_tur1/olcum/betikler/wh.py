import numpy as np, soundfile as sf, json, re, whisper, difflib
from scipy import signal
from common import *
d = json.load(open(P + 'senaryo.json')); TTS = {s['id']: re.sub(r'\[[^\]]*\]', '', s['tts']) for s in d['segments']}
norm = lambda s: re.sub(r"[^\wçğıöşüâî]+", ' ', s.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i')).split()
clips = [('A01-A02', 0.0, 11.9, ['A01', 'A02']), ('E10', 399.4, 413.6, ['E10']), ('J04', 1076.9, 1083.3, ['J04']), ('I12', 1197.2, 1215.9, ['I12']), ('L06', 1279.5, 1286.6, ['L06'])]
sos = signal.butter(4, [300, 8000], 'bandpass', fs=SR, output='sos')
m = whisper.load_model('small')
vo = np.load('vo.npy', mmap_mode='r')
res = []
for name, a, b, ids in clips:
    x, _ = sf.read(P + 'audio/mix.wav', start=int(a * SR), stop=int(b * SR), dtype='float32', always_2d=True)
    mono = x.mean(1); ph = signal.sosfilt(sos, mono).astype(np.float32)
    ref = norm(' '.join(TTS[i] for i in ids))
    out = {}
    for tag, sig in (('telefon_miks', ph), ('yalniz_anlatim', np.asarray(vo[int(a * SR):int(b * SR)], np.float32))):
        y = signal.resample_poly(sig, 1, 3).astype(np.float32)
        r = m.transcribe(y, language='tr', condition_on_previous_text=False, fp16=False, initial_prompt='Prometeus, Zeus, Hesiodos, Ayshilos, Erhat, Titan')
        hyp = norm(r['text'])
        sm = difflib.SequenceMatcher(None, ref, hyp)
        errs = [(op, ' '.join(ref[i1:i2]), ' '.join(hyp[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
        wer = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal') / len(ref)
        out[tag] = dict(wer=round(wer, 3), errs=errs, text=r['text'].strip())
        print(name, tag, round(wer, 3), errs, flush=True)
    res.append((name, a, b, out))
json.dump(res, open('whisper.json', 'w'), ensure_ascii=False, indent=1)

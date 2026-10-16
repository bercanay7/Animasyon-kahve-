"""Tek ifade sınaması: python3 chunktest.py "metin" "metin" ... (her biri 4 örnek, kenar dolgulu Whisper)"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator, asr
import tts as T
tts = narrator.load_tts("dfki", dict(narrator.PROFILE, **T.PROF))
prof = dict(narrator.PROFILE); prof.update(T.PROF)
for text in sys.argv[1:]:
    toks = narrator.parse(text)
    ref = " ".join(t["show"] for t in toks).replace("’", "")
    out = []
    for k in range(4):
        y = narrator.synth_chunk(tts, toks, prof["speed"] * 1.04, prof["pitch"], prof, 1.0)
        z = y / (np.max(np.abs(y)) + 1e-9) * 0.5
        z = np.concatenate([np.zeros(int(0.25 * 48000)), z, np.zeros(int(0.45 * 48000))])
        h = asr.transcribe(z, 48000)
        out.append(f"{asr.wer(ref, h.replace(chr(39), '')):.2f}:{h}")
    print(text, "\n    " + "\n    ".join(out), flush=True)

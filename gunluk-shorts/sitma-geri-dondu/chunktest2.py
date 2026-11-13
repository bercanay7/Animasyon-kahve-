"""Stüdyo işlemli sınama: ifade → narrator.studio → seviye → Whisper (son miksle aynı zincire daha yakın)."""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator, asr
import tts as T
prof = dict(narrator.PROFILE); prof.update(T.PROF)
tts = narrator.load_tts("dfki", prof)
N = int(sys.argv[1]) if sys.argv[1].isdigit() else 6
for text in sys.argv[2:]:
    toks = narrator.parse(text)
    ref = " ".join(t["show"] for t in toks).replace("’", "")
    out = []
    for k in range(N):
        y = narrator.synth_chunk(tts, toks, prof["speed"] * 1.04, prof["pitch"], prof, 1.0)
        z = np.concatenate([np.zeros(int(0.3 * 48000)), y, np.zeros(int(0.5 * 48000))])
        z = narrator.studio(z, prof)
        act = np.abs(z) > 0.02 * np.max(np.abs(z))
        z = z * (10 ** (-16.5 / 20) / (np.sqrt(np.mean(z[act] ** 2)) + 1e-9))
        z = np.tanh(z / 0.8) * 0.8
        h = asr.transcribe(z, 48000)
        out.append(f"{asr.wer(ref, h.replace(chr(39), '')):.2f}:{h}")
    print(text, "\n    " + "\n    ".join(out), flush=True)

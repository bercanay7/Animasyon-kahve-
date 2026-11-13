"""En iyi-K sentez: her ifade (virgül/nokta arası parça) K kez sentezlenir, Whisper'ın en doğru yazıya döktüğü seçilir.
Kullanım: python3 tts_best.py [K]   (tts.py ile aynı metin/profil; çıktı out/voice.wav + out/timeline.json)"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator, asr
import tts as T

K = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 4
ORIG = narrator.synth_chunk
LOG = []


def _norm(s):
    return s.replace("’", "").replace("'", "")


def best_chunk(tts, toks, speed, pitch, prof, sent_energy=1.0):
    ref = _norm(" ".join(t["show"] for t in toks))
    if len(toks) < 2:                      # tek kelimelik parçada Whisper güvenilmez
        return ORIG(tts, toks, speed, pitch, prof, sent_energy)
    best, bw, bh = None, 9.0, ""
    for k in range(K):
        y = ORIG(tts, toks, speed, pitch, prof, sent_energy)
        z = y / (np.max(np.abs(y)) + 1e-9) * 0.5
        z = np.concatenate([np.zeros(int(0.25 * narrator.SR)), z, np.zeros(int(0.45 * narrator.SR))])   # kenar etkisi: Whisper son hecede kesiliyor
        hyp = asr.transcribe(z, narrator.SR)
        w = asr.wer(ref, _norm(hyp))
        if w < bw - 1e-9:
            best, bw, bh = y, w, hyp
        if w == 0:
            break
    LOG.append((ref, bw, bh))
    print(f"  [{bw:.2f}] {ref}  ->  {bh}", flush=True)
    return best


if __name__ == "__main__":
    lex = os.path.join(HERE, "..", "ses-lab", "lex.json")
    if os.path.exists(lex):
        narrator.LEX.update(json.load(open(lex)))
    narrator.synth_chunk = best_chunk
    Tt, tot, _ = narrator.render(T.SENTENCES, os.path.join(HERE, "out"), voice=T.VOICE, profile=T.PROF, tail=0.95)
    tl = json.load(open(os.path.join(HERE, "out", "timeline.json")))
    print(f"ses={T.VOICE} süre={Tt:.0f} sn (son kelime {tot:.2f} sn)")
    for s in tl["sentences"]:
        print(f"  {s['id']} {s['t0']:6.2f}–{s['t1']:6.2f}  " + " | ".join(f"{i}:{w['show']}" for i, w in enumerate(s['words'])))

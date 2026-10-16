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


def wer_wild(ref, hyp):
    """ref: [(kelime, joker?)]; joker (yabancı ad / sayı) 0–4 sözcüğü bedelsiz karşılar. Joker olmayan kelimeye göre oranlar."""
    n, m = len(ref), len(hyp)
    INF = 1e9
    d = [[INF] * (m + 1) for _ in range(n + 1)]
    d[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            v = d[i][j]
            if v >= INF:
                continue
            if i < n:
                w, wild = ref[i]
                d[i + 1][j] = min(d[i + 1][j], v + (0 if wild else 1))
                if j < m:
                    d[i + 1][j + 1] = min(d[i + 1][j + 1], v + (0 if (wild or hyp[j] == w) else 1))
                    if wild:
                        for k in range(2, 5):
                            if j + k <= m:
                                d[i + 1][j + k] = min(d[i + 1][j + k], v)
            if j < m:
                d[i][j + 1] = min(d[i][j + 1], v + 1)
    return d[n][m] / max(1, sum(1 for _, wl in ref if not wl))


def best_chunk(tts, toks, speed, pitch, prof, sent_energy=1.0):
    ref = []
    for t in toks:
        wild = (t["show"].replace("_", " ") != t["say"].replace("_", " ")) or any(ch.isdigit() for ch in t["show"])
        ws = asr.norm(_norm(t["show"]))
        if wild or not ws:
            ref.append(("*", True))
        else:
            ref += [(w, False) for w in ws]
    if len(toks) < 2:                      # tek kelimelik parçada Whisper güvenilmez
        return ORIG(tts, toks, speed, pitch, prof, sent_energy)
    best, bw, bh = None, 9.0, ""
    for k in range(K):
        y = ORIG(tts, toks, speed, pitch, prof, sent_energy)
        z = y / (np.max(np.abs(y)) + 1e-9) * 0.5
        z = np.concatenate([np.zeros(int(0.25 * narrator.SR)), z, np.zeros(int(0.45 * narrator.SR))])   # kenar etkisi: Whisper son hecede kesiliyor
        hyp = asr.transcribe(z, narrator.SR)
        w = wer_wild(ref, asr.norm(_norm(hyp)))
        if w < bw - 1e-9:
            best, bw, bh = y, w, hyp
        if w == 0:
            break
    show_txt = " ".join(t["show"] for t in toks)
    LOG.append((show_txt, bw, bh))
    print(f"  [{bw:.2f}] {show_txt}  ->  {bh}", flush=True)
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

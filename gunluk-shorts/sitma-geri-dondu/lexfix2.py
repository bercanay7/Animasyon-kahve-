"""Telaffuz sınaması: sorunlu sözcükler için aday yazımlar → Whisper WER (her aday 3 kez, TTS rastgele)."""
import sys, os, json, tempfile
sys.path.insert(0, "../ses-lab")
import numpy as np
import asr, narrator

CASES = {
 "E": ["Neden? Uzmanlara göre, *etkenler=etkeenler üst üste bindi.*", "Neden? Uzmanlara göre, *faktörler üst üste bindi.*"],
 "H": ["Üstelik, *gözetim zayıftı.*", "Üstelik, *gözetim çok zayıftı.*", "Üstelik, *izleme zayıftı.*"],
 "L": ["Ders şu: *bitti sanılan hastalık,* takip edilmezse döner.", "Ders şu: *biten sanılan hastalık* izlenmezse döner.", "Ders şu: *bitti sanılan hastalık,* gözetilmezse döner.",
       "Ders şu: *bitti sanılan hastalık* bırakılırsa döner."],
}
only = sys.argv[1:]
tmp = tempfile.mkdtemp(prefix="lexfix_")
for key, cands in CASES.items():
    if only and key not in only:
        continue
    for c in cands:
        ws, hyps = [], []
        for k in range(3):
            T, tot, buf = narrator.render([("x", c, 1.04, 1.1, 0.0)], tmp, voice="dfki", profile=dict(speed=1.12, reverb_wet=0.0))
            tl = json.load(open(os.path.join(tmp, "timeline.json")))["sentences"][0]
            hyp = asr.transcribe(buf[int(tl["t0"] * 48000): int(tl["t1"] * 48000) + 14400], 48000)
            ref = " ".join(w["show"] for w in tl["words"])
            ws.append(asr.wer(ref, hyp)); hyps.append(hyp)
        print(f"{key} WER {np.mean(ws):.2f} {['%.2f'%x for x in ws]} | {c}", flush=True)
        for h in hyps:
            print("      ", h, flush=True)

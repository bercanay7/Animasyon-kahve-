"""Telaffuz sınaması: sorunlu sözcükler için aday yazımlar → Whisper WER (her aday 3 kez, TTS rastgele)."""
import sys, os, json, tempfile
sys.path.insert(0, "../ses-lab")
import numpy as np
import asr, narrator

CASES = {
 "L": ["Ders şu: *bitti diye bırakırsan,* hastalık döner.", "Ders şu: *bitti sanıp bırakırsan,* hastalık geri döner.", "Ders şu: *bitti diye izlemezsen,* hastalık döner.",
       "Ders şu: *bitti diye bakmazsan,* hastalık döner."],
 "G": ["Sonra, *işçi göçü* hastalığı *yeni bölgelere taşıdı.*", "Sonra, *işçi göçü* hastalığı *başka bölgelere taşıdı.*"],
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

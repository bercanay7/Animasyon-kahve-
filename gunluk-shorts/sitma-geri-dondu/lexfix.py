"""Telaffuz sınaması: sorunlu sözcükler için aday yazımlar → Whisper WER (her aday 3 kez, TTS rastgele)."""
import sys, os, json, tempfile
sys.path.insert(0, "../ses-lab")
import numpy as np
import asr, narrator

CASES = {
 "C": ["Vaka sayısı *1.263’e=bin_iki_yüz_altmış_üçe düştü.*", "Yıllık vaka sayısı *1.263’e=bin_iki_yüz_altmış_üçe düştü.*", "Kayıtlı vaka sayısı *1.263’e=bin_iki_yüz_altmış_üçe düştü.*"],
 "E": ["Neden? Dünya Sağlık Örgütü’ne=Örgütüne göre, *etkenler üst üste bindi.*", "Neden? Dünya Sağlık Örgütü’ne=Örgütüne göre, *etkenler=et_kenler üst üste bindi.*",
       "Neden? Dünya Sağlık Örgütü’ne=Örgütüne göre, *etkenler=etkeenler üst üste bindi.*", "Neden? Dünya Sağlık Örgütü’ne=Örgütüne göre, *faktörler üst üste bindi.*"],
 "K": ["Bugün, Sağlık Bakanlığı’na=Bakanlığına göre, *yerli vaka yok.* İthal vakalar sürüyor.", "Bugün, Sağlık Bakanlığı’na=Bakanlığına göre, *yerli vaka yok.* İthal=it_hal vakalar sürüyor.",
       "Bugün, Sağlık Bakanlığı’na=Bakanlığına göre, *yerli vaka yok.* İthal=ithaal vakalar sürüyor.", "Bugün, Sağlık Bakanlığı’na=Bakanlığına göre, *yerli vaka yok.* Dışarıdan gelen vakalar sürüyor."],
 "H": ["Üstelik, *gözetim ağı yetersizdi.*", "Üstelik, *gözetim yetersizdi.*", "Üstelik, *gözetim sistemi yetersizdi.*"],
 "L": ["Ders şu: *bitti sanılan hastalık,* izlenmezse döner.", "Ders şu: *bitti sanılan hastalık,* izlenmeyince döner.", "Ders şu: *bitti sanılan hastalık,* takip edilmezse döner."],
 "F": ["Önce, *sulu tarım yayıldı.* Sivrisinek sayısı *keskin arttı.*", "Önce, *sulu=suluu tarım yayıldı.* Sivrisinek sayısı *keskin arttı.*"],
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

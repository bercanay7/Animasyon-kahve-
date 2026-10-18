#!/usr/bin/env python3
"""GEÇİCİ (scratch) anlatım — ElevenLabs kredisi yokken görüntü hattını geliştirmek için. NİHAİ ÜRÜNDE KULLANILMAZ.

  python3 ses_gecici.py                 # ses_ham/cN_v1.mp3 olmayan bölümler için ses_ham/cN_g_48k.wav üretir
  python3 ses_gecici.py c7 c8           # yalnız bu bölümler
  python3 ses_gecici.py --hepsi         # varsa v1'i olanlar dahil hepsi (test)
  python3 ses_gecici.py --hiz 0.82      # tempo (varsayılan 0.85; ElevenLabs c0–c5 ≈1,7 söz/sn duraklar dahil)

Sonra, parça için:   MEDICI_PART=2 python3 ses_birlestir.py c7=g c8=g c9=g c10=g c11=g
                     MEDICI_PART=2 python3 ses_hizala_asr.py (ya da ses_hizala_yerel.py) ; MEDICI_PART=2 python3 ses_hizala.py
Yöntem: Piper (sherpa-onnx, çevrimdışı) "fahrettin" sesi; her cümle ayrı sentezlenir (söylenen metin = script.py okunuşu), cümle arası 0,50 sn, paragraf sonu 0,95 sn.
Kural: ses_ham/GECICI.json geçici bölümleri listeler; parca.assert_gercek_ses() final mux/render öncesi çağrılır ve geçici ses varsa DURUR.
"""
import glob
import json
import os
import subprocess
import sys
import time
import wave

import numpy as np
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import script as S  # noqa: E402

RAW = os.path.join(HERE, "ses_ham")
MODELS = os.path.join(HERE, "..", "ses-modelleri")
SR = 48000
GAP_SENT, GAP_PARA = 0.50, 0.95


def load_tts(voice="fahrettin", threads=3):
    import sherpa_onnx
    d = glob.glob(os.path.join(MODELS, f"ex_{voice}", "*"))[0]
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(d + "/*.onnx")[0], tokens=d + "/tokens.txt", data_dir=d + "/espeak-ng-data",
                                                    noise_scale=0.60, noise_scale_w=0.70), num_threads=threads))
    return sherpa_onnx.OfflineTts(cfg)


def synth(tts, text, speed):
    a = tts.generate(text, sid=0, speed=speed)
    x = np.array(a.samples, dtype=np.float64)
    from fractions import Fraction
    fr = Fraction(SR, a.sample_rate)
    return resample_poly(x, fr.numerator, fr.denominator)


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    w = wave.open(path, "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype("<i2").tobytes())
    w.close()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    hepsi = "--hepsi" in sys.argv
    speed = 0.70
    if "--hiz" in sys.argv:
        speed = float(sys.argv[sys.argv.index("--hiz") + 1])
        args = [a for a in args if a != str(speed) and a != sys.argv[sys.argv.index("--hiz") + 1]]
    want = args or [ch["id"] for ch in S.CHAPTERS]
    todo = []
    for ch in S.CHAPTERS:
        cid = ch["id"]
        if cid not in want:
            continue
        has_real = os.path.exists(os.path.join(RAW, f"{cid}_v1.mp3"))
        if has_real and not hepsi:
            continue
        todo.append(ch)
    if not todo:
        print("yapılacak bölüm yok")
        return
    reg_path = os.path.join(RAW, "GECICI.json")
    reg = json.load(open(reg_path)) if os.path.exists(reg_path) else {}
    tts = load_tts()
    for ch in todo:
        t0 = time.time()
        parts = []
        for pi, para in enumerate(ch["paras"]):
            for ti, tup in enumerate(para):
                x = synth(tts, S._speech_of(tup), speed)
                parts.append(x)
                last = ti == len(para) - 1
                parts.append(np.zeros(int((GAP_PARA if last else GAP_SENT) * SR)))
        y = np.concatenate(parts)
        pk = np.max(np.abs(y)) + 1e-9
        y = y * (0.5 / pk)
        out = os.path.join(RAW, f"{ch['id']}_g_48k.wav")
        write_wav(out, y)
        reg[ch["id"]] = dict(file=os.path.basename(out), sn=round(len(y) / SR, 1), olusturuldu=time.strftime("%Y-%m-%d %H:%M"))
        json.dump(reg, open(reg_path, "w"), indent=1, ensure_ascii=False)
        words = sum(len(S._speech_of(t).split()) for p in ch["paras"] for t in p)
        print(f"{ch['id']:4s} {len(y) / SR:6.1f} sn  {words} söz  ({words / (len(y) / SR):.2f} söz/sn)  [{time.time() - t0:.0f} sn işlem]")


if __name__ == "__main__":
    main()

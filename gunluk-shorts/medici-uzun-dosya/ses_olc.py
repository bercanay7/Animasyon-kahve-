"""Üretilen bölüm sesini ölçer: Whisper (yerel) ile yazıya döker, beklenen metinle karşılaştırır, sessizlik ve tempo raporlar.
Kullanım: python3 ses_olc.py c1 ses_ham/c1_v1.wav"""
import sys, os, re, wave
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ses-lab"))
import asr
import script as S

def load(path):
    w = wave.open(path); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    return x, sr

def gaps(x, sr, thr_db=-38, min_s=0.25):
    hop = int(0.01 * sr)
    e = np.array([np.sqrt(np.mean(x[i:i+hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
    db = 20 * np.log10(e + 1e-9); thr = db.max() + thr_db + 0
    thr = db.max() - 38
    sil = db < thr; out = []; i = 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j < len(sil) and sil[j]: j += 1
            if (j - i) * 0.01 >= min_s: out.append((i * 0.01, (j - i) * 0.01))
            i = j
        else: i += 1
    return out

def main(cid, path):
    x, sr = load(path)
    txt = S.chapter_text(cid)
    dur = len(x) / sr
    words = len(txt.split())
    print(f"{cid}: {dur:.1f} s, {words} sözcük, {words/dur:.2f} söz/sn")
    g = gaps(x, sr)
    long = [f"{t:.1f}s:{d:.2f}" for t, d in g if d >= 0.7]
    print(f"  boşluk≥0,25s: {len(g)} adet; ≥0,7s olanlar: {long}")
    # 28 sn'lik parçalarda Whisper (30 sn sınırı) — boşlukta böl
    cuts = [0.0]; t = 0.0
    for gt, gd in g:
        mid = gt + gd / 2
        if mid - cuts[-1] > 22: cuts.append(mid)
    cuts.append(dur)
    hyp = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        seg = x[int(a * sr):int(b * sr)]
        seg = seg / (np.max(np.abs(seg)) + 1e-9) * 0.5
        hyp.append(asr.transcribe(np.concatenate([np.zeros(int(.25*sr)), seg, np.zeros(int(.4*sr))]), sr))
    h = " ".join(hyp)
    print("  ASR:", h)
    print(f"  WER (sayı/ad karşılaştırması dahil): {asr.wer(txt, h):.3f}")

main(sys.argv[1], sys.argv[2])

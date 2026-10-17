"""Cümle düzeyinde Whisper doğrulaması (Kanal Anayasası, kapı 2 — otomatik kısım; insan kulağı yerine geçmez).
out/voice.wav'ı timeline.json'daki cümle sınırlarından keser, Whisper-medium (çevrimdışı) ile yazıya döker, beklenen okunuşla karşılaştırır.
Çıktı: out/dogrulama_cumle.txt   Kullanım: python3 dogrula.py"""
import json, os, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
sys.argv = [sys.argv[0]]
import narrator, asr
import tts as T
from tts_best import wer_wild, _norm

tl = json.load(open(os.path.join(HERE, "out", "timeline.json")))
w = wave.open(os.path.join(HERE, "out", "voice.wav"))
sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
text_of = {sid: text for sid, text, *_ in T.SENTENCES}

lines, werr = [], []
for s in tl["sentences"]:
    a, b = max(0, int((s["t0"] - 0.2) * sr)), min(len(x), int((s["t1"] + 0.3) * sr))
    seg = x[a:b]
    seg = seg / (np.max(np.abs(seg)) + 1e-9) * 0.5
    hyp = asr.transcribe(np.concatenate([np.zeros(int(0.25 * sr)), seg, np.zeros(int(0.45 * sr))]), sr)
    toks = narrator.parse(text_of[s["id"]])
    ref = []
    for t in toks:
        wild = (t["show"].replace("_", " ") != t["say"].replace("_", " ")) or any(ch.isdigit() for ch in t["show"])
        ws = asr.norm(_norm(t["show"]))
        if wild or not ws:
            ref.append(("*", True))
        else:
            ref += [(q, False) for q in ws]
    e = wer_wild(ref, asr.norm(_norm(hyp)))
    werr.append(e)
    show = " ".join(t["show"] for t in toks)
    lines.append(f"[{e:.2f}] {s['id']:4s} {show}\n        Whisper: {hyp}")
mean = float(np.mean(werr))
head = f"Cümle düzeyinde Whisper-medium doğrulaması (joker: yabancı ad/sayı) — ortalama WER {mean:.3f}, en kötü {max(werr):.2f}, ≥0,3 olan cümle: {sum(1 for e in werr if e >= 0.3)}\n"
open(os.path.join(HERE, "out", "dogrulama_cumle.txt"), "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
print(head)
print("\n".join(lines))

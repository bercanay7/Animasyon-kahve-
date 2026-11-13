"""Whisper (sherpa-onnx, çevrimdışı) ile sentezlenen sesi geri yazdırıp anlaşılırlığı ölçer."""
import glob, os, re, sys
import numpy as np
import sherpa_onnx
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "..", "ses-modelleri", "ex_whisper_medium", glob.glob(os.path.join(HERE, "..", "ses-modelleri", "ex_whisper_medium", "*"))[0].split("/")[-1])
_rec = None

def recognizer():
    global _rec
    if _rec is None:
        _rec = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=glob.glob(MD + "/*-encoder.int8.onnx")[0], decoder=glob.glob(MD + "/*-decoder.int8.onnx")[0],
            tokens=glob.glob(MD + "/*-tokens.txt")[0], language="tr", task="transcribe", num_threads=4)
    return _rec

def transcribe(x, sr):
    y = resample_poly(x, 16000, sr).astype(np.float32) if sr != 16000 else x.astype(np.float32)
    s = recognizer().create_stream()
    s.accept_waveform(16000, y)
    recognizer().decode_stream(s)
    return s.result.text.strip()

_ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def tr_num(n):
    if n == 0:
        return "sıfır"
    parts = []
    if n >= 1000:
        k = n // 1000
        parts.append(("" if k == 1 else tr_num(k)) + " bin")
        n %= 1000
    if n >= 100:
        h = n // 100
        parts.append(("" if h == 1 else _ONES[h]) + " yüz")
        n %= 100
    if n >= 10:
        parts.append(_TENS[n // 10]); n %= 10
    if n:
        parts.append(_ONES[n])
    return " ".join(p.strip() for p in parts if p.strip())


def norm(t):
    t = re.sub(r"(\d+)\.(\d{3})", r"\1\2", t)
    t = re.sub(r"\d+", lambda m: tr_num(int(m.group())), t)
    t = t.lower().replace("i̇", "i")
    t = re.sub(r"[^\wçğıöşü\s]", " ", t)
    return t.split()

def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = np.zeros((len(r) + 1, len(h) + 1), int)
    d[:, 0] = np.arange(len(r) + 1); d[0, :] = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + (r[i-1] != h[j-1]))
    return d[len(r), len(h)] / max(1, len(r))

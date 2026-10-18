#!/usr/bin/env python3
"""KREDİSİZ, ASR-destekli sözcük hizalayıcı (ElevenLabs Scribe yerine; ses_hizala_yerel.py'nin yerini alır).

  MEDICI_PART=1 python3 ses_hizala_asr.py                 # koşular → ASR (önbellekli) → hizalama → out_p1/scribe_words.json
  MEDICI_PART=1 python3 ses_hizala.py                     # (mevcut, değişmedi) → out_p1/timeline.json     [ya da yukarıdakine --timeline ekle]
  MEDICI_PART=1 python3 ses_hizala_asr.py --dogrula       # bağımsız doğrulama (cümle pencerelerini yeniden yazdırır; eski/yeni karşılaştırması)
  MEDICI_PART=1 python3 ses_hizala_asr.py --karsilastir   # eski (timeline_yerel_eski.json) ↔ yeni timeline.json farkları
  MEDICI_PART=1 python3 ses_hizala_asr.py --loo           # koşu içi zamanlama doğruluğu (duraktan bir bırak; ağırlık ↔ akustik HMM)
  Seçenekler: --asr-yok (yalnız önbellek) · --yalniz-asr (sadece önbelleği doldur) · --isci N (ASR süreç sayısı; her biri 1 iş
  parçacığı, toplam ≤2) · --bolum c2 (tek bölüm; ana dosyalara dokunmaz, *_c2.* yazar) · --agirlik (akustik HMM kapalı) ·
  --ham-konusma (rakamlı jetonları birleştirmeden, saf söylenen sözcükler) · --timeline (bitince ses_hizala.py'yi çalıştır)
  Parça 2/3: MEDICI_PART=2 … aynen çalışır (out_p2/voice.wav + voice_chapters.json içindeki bölümler gezilir).

Yöntem (ayrıntı: notlar_hizalama.md):
 1. Her bölümün sesi 250 Hz üstü süzülmüş 10 ms RMS ile "konuşma koşuları"na bölünür (durak ≥ 0,12 sn; gürültü kırıntıları atılır,
    sözcük içi kapanma parçaları komşuya katılır, 14 sn'den uzun koşu en düşük enerjiden bölünür).
 2. Her koşu (±0,12 sn paylı) Whisper medium (sherpa-onnx, çevrimdışı) ile yazıya dökülür; sonuçlar out_pN/asr_cache.json'da önbelleklenir
    (anahtar bölüm+başlangıç/bitiş, ses CRC'siyle doğrulanır).
 3. Bölümün tüm ASR sözcükleri, senaryo jetonlarıyla (S._speech_of; Türkçe harf katlama + bulanık benzerlik + 1↔2 birleştirme)
    monoton Needleman–Wunsch ile eşlenir.
 4. Eşleşmeler her koşunun senaryo-jeton aralığını belirler; koşular arası eşleşmeyen jetonlar (ve kanıtsız koşular) küçük bir DP ile
    (noktalama ↔ durak uyumu + konuşma hızı/süre uyumu) komşu koşulara dağıtılır.
 5. Koşu içi sözcük zamanları: ASR ile doğrulanmış koşu↔metin çiftlerinden kendi kendine eğitilen monofon (harf≈ses) GMM-HMM ile zorlamalı
    Viterbi hizalaması; ilk/son sözcük koşu kenarlarına (VAD) yaslanır, koşular arası boşluk gerçek durak olarak kalır. HMM'in güvenilmediği
    koşularda hece/sözcük ağırlıklı dağıtıma geri düşülür.
 6. Çıktı out_pN/scribe_words.json (ses_hizala_yerel.py ile aynı biçim: [{text,start,end,type:"word"}], bölümler art arda, mutlak sn).
    Her GÖSTERİM jetonu bir sözcük olur (rakamlı jetonlar — "1737'de" — tek sözcük): ses_hizala.py eşleşmesi %100 olur ve cümle
    başı/sonundaki sayılar komşu durakları yutmaz (ses_hizala.py'nin enterpolasyon zayıflığı).
"""
import os

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_k, "1")          # CPU bütçesi: ASR dışında tek iş parçacığı

import argparse
import bisect
import difflib
import glob
import json
import math
import random
import re
import shutil
import sys
import time
import types
import wave
import zlib

import numpy as np

HERE = os.environ.get("MEDICI_DIR") or os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
LAB = os.path.abspath(os.path.join(HERE, "..", "ses-lab"))
if LAB not in sys.path:
    sys.path.insert(0, LAB)

import parca as PA  # noqa: E402

OUT = PA.OUT
HOP = 0.01                      # enerji kare adımı (sn)
MIN_DURAK = 0.12                # koşuları ayıran en kısa sessizlik (sn)
DURAK_ESIK_DB = 34.0            # sessizlik eşiği: yüksek-geçiren sinyalin %95 düzeyinin bu kadar altı
GURULTU_TEPE_DB = -22.0         # koşunun tepe düzeyi (p95'e göre) bunun altındaysa gürültü kırıntısı
PARCA_SURE = 0.30               # bu süreden kısa koşu + kısa komşu durak → komşuya katılır
PARCA_DURAK = 0.16
UZUN_KOSU = 14.0                # bundan uzun koşu en düşük enerjiden bölünür
ASR_PAY = 0.12                  # ASR penceresine her yana payı (sn)
KENAR_GENISLET = 0.01           # koşu kenarlarını eşik karesi kadar dışarı al (yumuşak başlangıç/bitiş)
ASR_ONBELLEK = "asr_cache.json"


def log(*a):
    print(*a, flush=True)


# ════════════════════════════════════════════════════════════ senaryo (diğer ajanların yarım dosyalarına dayanıklı yükleme)
def senaryo_yukle():
    """`import script`: scr_cN.py dosyaları başka ajanlarca yazılırken sözdizimi hatalı olabilir; bozuk bölüm modülü boş bölümle değiştirilir."""
    if "script" in sys.modules:
        return sys.modules["script"]
    import importlib
    for i in range(17):
        name = f"scr_c{i}"
        if name in sys.modules:
            continue
        try:
            importlib.import_module(name)
        except ModuleNotFoundError:
            pass
        except Exception as e:                                       # noqa: BLE001  (SyntaxError dahil)
            log(f"UYARI: {name}.py yüklenemedi ({type(e).__name__}); boş bölümle geçiliyor")
            m = types.ModuleType(name)
            m.CH = dict(id=f"c{i}", title="(yüklenemedi)", paras=[])
            m.PRON = []
            sys.modules[name] = m
    import script as S
    return S


# ════════════════════════════════════════════════════════════ ses
def load_wav(path):
    w = wave.open(path)
    sr = w.getframerate()
    ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x, sr


def _sos(sr, fc=250.0):
    from scipy.signal import butter
    return butter(4, fc, btype="high", fs=sr, output="sos")


def enerji_db(seg, sr):
    """250 Hz üstü süzülmüş 10 ms RMS (dB). Alçak frekanslı uğultu/hum konuşma-dışı bölgeleri 'konuşma' göstermesin diye."""
    from scipy.signal import sosfilt
    hp = sosfilt(_sos(sr), seg)
    h = int(round(HOP * sr))
    n = len(hp) // h
    e = np.sqrt(np.mean(hp[: n * h].reshape(n, h) ** 2, axis=1) + 1e-14)
    return 20 * np.log10(e + 1e-9)


def kosulari_bul(seg, sr):
    """Bölüm sesinden konuşma koşuları. → (koşular, bilgi). Her koşu: dict(a, b, pk) saniye (bölüme göre), pk = tepe − p95 (dB)."""
    db = enerji_db(seg, sr)
    n = len(db)
    p95 = float(np.percentile(db, 95))
    p10 = float(np.percentile(db, 10))
    thr = max(p95 - DURAK_ESIK_DB, p10 + 10.0)                       # yüksek gürültü tabanında (tıslama) eşik tabana göre yükselir
    sil = db < thr
    if sil.all():
        return [], dict(p95=p95, thr=thr, n_ham=0, n_gurultu=0, n_parca=0, n_bolunen=0)
    first = int(np.argmax(~sil))
    last = n - int(np.argmax(~sil[::-1]))
    # sessizlik aralıkları (>= MIN_DURAK) → koşular
    kes = []                                                         # (kare_baş, kare_son) sessizlikler
    i = first
    while i < last:
        if sil[i]:
            j = i
            while j < last and sil[j]:
                j += 1
            if (j - i) * HOP >= MIN_DURAK - 1e-9:
                kes.append((i, j))
            i = j
        else:
            i += 1
    edges = [first] + [v for p in kes for v in p] + [last]
    runs = [dict(a=edges[k] * HOP, b=edges[k + 1] * HOP, ia=edges[k], ib=edges[k + 1]) for k in range(0, len(edges), 2)]
    for r in runs:
        r["pk"] = float(db[r["ia"]: r["ib"]].max() - p95)
    n_ham = len(runs)
    # 1) gürültü kırıntıları: tepe düzeyi çok düşük
    keep = [r for r in runs if r["pk"] >= GURULTU_TEPE_DB]
    n_gurultu = n_ham - len(keep)
    runs = keep
    # 2) kısa parça + komşu kısa durak → komşuya kat (sözcük içi kapanma/patlama parçaları)
    n_parca = 0
    changed = True
    while changed and len(runs) > 1:
        changed = False
        for k, r in enumerate(runs):
            if r["b"] - r["a"] >= PARCA_SURE:
                continue
            dl = r["a"] - runs[k - 1]["b"] if k > 0 else 9.0
            dr = runs[k + 1]["a"] - r["b"] if k + 1 < len(runs) else 9.0
            if min(dl, dr) >= PARCA_DURAK:
                continue
            o = k - 1 if dl <= dr else k + 1
            lo, hi = min(k, o), max(k, o)
            m = dict(a=runs[lo]["a"], b=runs[hi]["b"], ia=runs[lo]["ia"], ib=runs[hi]["ib"], pk=max(runs[lo]["pk"], runs[hi]["pk"]))
            runs[lo: hi + 1] = [m]
            n_parca += 1
            changed = True
            break
    # 3) çok uzun koşu → en düşük enerjiden böl
    n_bol = 0
    out = []
    for r in runs:
        stack = [r]
        while stack:
            q = stack.pop(0)
            if q["b"] - q["a"] <= UZUN_KOSU:
                out.append(q)
                continue
            lo = q["ia"] + int(0.3 * (q["ib"] - q["ia"]))
            hi = q["ia"] + int(0.7 * (q["ib"] - q["ia"]))
            sm = np.convolve(db[lo:hi], np.ones(5) / 5, mode="same")
            c = lo + int(np.argmin(sm))
            n_bol += 1
            stack = [dict(a=q["a"], b=c * HOP, ia=q["ia"], ib=c, pk=q["pk"]), dict(a=c * HOP, b=q["b"], ia=c, ib=q["ib"], pk=q["pk"])] + stack
    runs = out
    T = n * HOP
    for r in runs:                                                   # yumuşak kenarlar için bir kare dışarı
        r["a"] = max(0.0, r["a"] - KENAR_GENISLET)
        r["b"] = min(len(seg) / sr, r["b"] + KENAR_GENISLET)
    for k, r in enumerate(runs):
        r["i"] = k
        r["dur"] = r["b"] - r["a"]
        r["pre"] = (r["a"] - runs[k - 1]["b"]) if k > 0 else None
        r["post"] = (runs[k + 1]["a"] - r["b"]) if k + 1 < len(runs) else None
        r.pop("ia", None)
        r.pop("ib", None)
    return runs, dict(p95=p95, thr=thr, n_ham=n_ham, n_gurultu=n_gurultu, n_parca=n_parca, n_bolunen=n_bol)


# ════════════════════════════════════════════════════════════ ASR (Whisper, çevrimdışı) + önbellek
def _kimlik(ch, a, b):
    return f"{ch}|{a:.2f}|{b:.2f}"


def _crc(x_slice):
    return zlib.crc32(np.round(x_slice * 32767).astype("<i2").tobytes()) & 0xFFFFFFFF


def cache_oku(path):
    for _ in range(5):
        try:
            if os.path.exists(path):
                return json.load(open(path, encoding="utf-8"))
            return {}
        except (json.JSONDecodeError, OSError):
            time.sleep(0.5)
    return {}


def cache_yaz(path, d):
    tmp = path + f".tmp{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    os.replace(tmp, path)


_W = {}


def _isci_baslat(wav_path, num_threads):
    """ASR işçisi: kendi tanıyıcısı (num_threads iş parçacığı) + sesin tamamı (int16)."""
    import sherpa_onnx
    import asr
    md = asr.MD
    asr._rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=glob.glob(md + "/*-encoder.int8.onnx")[0], decoder=glob.glob(md + "/*-decoder.int8.onnx")[0],
        tokens=glob.glob(md + "/*-tokens.txt")[0], language="tr", task="transcribe", num_threads=num_threads)
    w = wave.open(wav_path)
    _W["sr"] = w.getframerate()
    _W["x"] = np.frombuffer(w.readframes(w.getnframes()), "<i2")
    _W["asr"] = asr


def _isci_calis(job):
    key, t0, t1 = job
    sr = _W["sr"]
    seg = _W["x"][int(round(t0 * sr)): int(round(t1 * sr))].astype(np.float64) / 32768
    t = time.time()
    try:
        txt = _W["asr"].transcribe(seg, sr)
    except Exception as e:                                           # noqa: BLE001
        return key, None, time.time() - t, f"{type(e).__name__}: {e}"
    return key, txt, time.time() - t, None


def asr_calistir(isler, cache_path, wav_path, isci=2, baslik="ASR"):
    """isler: [(anahtar, t0_mutlak, t1_mutlak, crc, meta)] — önbellekte (aynı crc ile) olmayanları işler; sonucu cache_path'e yazar."""
    cache = cache_oku(cache_path)
    eksik = [j for j in isler if not (j[0] in cache and cache[j[0]].get("crc") == j[3] and cache[j[0]].get("text") is not None)]
    log(f"[{baslik}] {len(isler)} iş, önbellekte {len(isler) - len(eksik)}, işlenecek {len(eksik)}")
    if not eksik:
        return cache
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    t_basla = time.time()
    done = 0
    with ctx.Pool(processes=isci, initializer=_isci_baslat, initargs=(wav_path, 1)) as pool:
        it = pool.imap_unordered(_isci_calis, [(j[0], j[1], j[2]) for j in eksik], chunksize=1)
        son_yaz = time.time()
        meta = {j[0]: j for j in eksik}
        for key, txt, dt, err in it:
            j = meta[key]
            if txt is None:
                log(f"  HATA {key}: {err}")
                continue
            cache[key] = dict(text=txt, crc=j[3], t0=round(j[1], 3), t1=round(j[2], 3), dt=round(dt, 2), **(j[4] or {}))
            done += 1
            if done % 10 == 0 or time.time() - son_yaz > 30:
                cache_yaz(cache_path, cache)
                son_yaz = time.time()
                gecen = time.time() - t_basla
                log(f"  [{baslik}] {done}/{len(eksik)} (%{100 * done / len(eksik):.0f}) geçen {gecen:.0f} sn, kalan ≈ {gecen / done * (len(eksik) - done):.0f} sn")
    cache_yaz(cache_path, cache)
    log(f"[{baslik}] bitti: {done} iş, {time.time() - t_basla:.0f} sn")
    return cache


# ════════════════════════════════════════════════════════════ bölüm verisi
def bolumleri_hazirla(secim=None):
    """voice_chapters.json'daki bölümler + ses + koşular. → (x, sr, vc, [bolum])"""
    vc = json.load(open(os.path.join(OUT, "voice_chapters.json"), encoding="utf-8"))
    wav_path = os.path.join(OUT, "voice.wav")
    x, sr = load_wav(wav_path)
    bol = []
    for c in vc["chapters"]:
        if secim and c["id"] not in secim:
            continue
        seg = x[int(round(c["t0"] * sr)): int(round(c["t1"] * sr))]
        runs, info = kosulari_bul(seg, sr)
        bol.append(dict(c=c, seg=seg, runs=runs, info=info))
    return x, sr, vc, wav_path, bol


def asr_isleri(x, sr, bol):
    isler = []
    for B in bol:
        c = B["c"]
        for r in B["runs"]:
            dur_ch = len(B["seg"]) / sr
            pl = min(ASR_PAY, (r["pre"] if r["pre"] is not None else 9) / 2)
            pr = min(ASR_PAY, (r["post"] if r["post"] is not None else 9) / 2)
            ta = c["t0"] + max(0.0, r["a"] - max(pl, 0.0))
            tb = c["t0"] + min(dur_ch, r["b"] + max(pr, 0.0))
            ta = round(ta, 3)
            tb = round(tb, 3)
            r["asr_t0"], r["asr_t1"] = ta, tb
            r["key"] = _kimlik(c["id"], c["t0"] + r["a"], c["t0"] + r["b"])
            crc = _crc(x[int(round(ta * sr)): int(round(tb * sr))])
            r["crc"] = crc
            isler.append((r["key"], ta, tb, crc, dict(ch=c["id"], k=r["i"])))
    return isler


def _onsel(isler):
    """Önce c2'nin 355–425 sn bölgesi (hızlı geri bildirim), sonra bölüm sırası."""
    def pri(j):
        return (0 if 355 <= j[1] <= 425 else 1, j[1])
    return sorted(isler, key=pri)


# ════════════════════════════════════════════════════════════ metin normalizasyonu / benzerlik
_KUCUK = str.maketrans({"İ": "i", "I": "ı"})
_KATLA = str.maketrans("çğıöşüâîû", "cgiosuaiu")
VOW = set("aeıioöuüâîûAEIİOÖUÜ")
STRONG, MED, WEAK, PARA = "strong", "med", "weak", "para"
_SAYI = re.compile(r"(\d{1,3}(?:\.\d{3})+|\d+)(['’][A-Za-zçğıöşüÇĞİÖŞÜ]+)?")


def katla(s):
    """Küçük harf (Türkçe İ/I) + ç→c ş→s ğ→g ı→i ö→o ü→u + yalnız [a-z0-9]: bulanık karşılaştırma için."""
    s = s.translate(_KUCUK).lower().replace("i̇", "i").translate(_KATLA)
    return re.sub(r"[^a-z0-9]", "", s)


def hece(w):
    return max(1, sum(1 for ch in w if ch in VOW))


def asr_sozcukleri(text, S):
    """Whisper çıktısı → katlanmış sözcük listesi (rakamlar senaryodaki gibi sözcüğe çevrilir, ek yapışık: 1737'de → …yedide)."""
    t = _SAYI.sub(S._num_sub, text.replace("’", "'"))
    out = []
    for w in re.split(r"[\s/–—\-]+", t):
        k = katla(w)
        if k:
            out.append(k)
    return out


_oran_cache = {}


def _orani(a, b):
    k = (a, b)
    v = _oran_cache.get(k)
    if v is None:
        v = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
        _oran_cache[k] = v
    return v


NEG = -1e9
S_ESLESME = 3.0
GAP = -1.0


def esle_puani(a, b):
    """İki katlanmış sözcüğün eşleşme puanı: tam eşit 3; çok benzer 2,2; benzer 1,2; zayıf 0,2; değilse −1,3 (yerine koyma)."""
    if a == b:
        return S_ESLESME if len(a) > 1 else 1.5
    la, lb = len(a), len(b)
    if not la or not lb or min(la, lb) < 0.38 * max(la, lb):
        return -1.3
    r = _orani(a, b)
    if r >= 0.85:
        return 2.2
    if r >= 0.70:
        return 1.2
    if r >= 0.55:
        return 0.2
    return -1.3


def birlesik_puani(parca, tam):
    """Birleştirme hamlesi (2 sözcük ↔ 1 sözcük): birleşik yazım çok benzerse 2,6 yoksa yasak."""
    if parca == tam:
        return 2.8
    if min(len(parca), len(tam)) < 4:
        return NEG
    return 2.4 if _orani(parca, tam) >= 0.88 else NEG


def nw_hizala(ref, hyp, band=None):
    """Monoton Needleman–Wunsch: ref (senaryo jetonları) ↔ hyp (ASR sözcükleri). Hamleler: 1↔1, ref boş, hyp boş, 2ref↔1hyp, 1ref↔2hyp.
    → ops listesi [(tür, i, j, puan)] (tür: 'M' 1↔1, 'G' ref boş, 'H' hyp boş, 'A' (i,i+1)↔j, 'B' i↔(j,j+1))."""
    n, m = len(ref), len(hyp)
    if band is None:
        band = max(150, int(0.3 * max(n, m)))
    D = [[NEG] * (m + 1) for _ in range(n + 1)]
    P = [[0] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for j in range(1, min(m, band) + 1):
        D[0][j] = j * GAP
        P[0][j] = 2
    ratio = (m / n) if n else 1.0
    for i in range(1, n + 1):
        c = int(round(i * ratio))
        j0, j1 = max(0, c - band), min(m, c + band)
        Di, Dp = D[i], D[i - 1]
        Pi = P[i]
        ri = ref[i - 1]
        if j0 == 0:
            Di[0] = i * GAP
            Pi[0] = 1
        for j in range(max(1, j0), j1 + 1):
            best = Dp[j - 1] + esle_puani(ri, hyp[j - 1])
            op = 0
            v = Dp[j] + GAP
            if v > best:
                best, op = v, 1
            v = Di[j - 1] + GAP
            if v > best:
                best, op = v, 2
            if i >= 2:
                r1 = ref[i - 2]
                h1 = hyp[j - 1]
                if esle_puani(r1, h1) < 2.2 and esle_puani(ri, h1) < 2.2:         # tek parça zaten eşleşiyorsa birleştirme yok (ek sözcük yutma)
                    v = D[i - 2][j - 1] + birlesik_puani(r1 + ri, h1)
                    if v > best:
                        best, op = v, 3
            if j >= 2:
                h0, h1 = hyp[j - 2], hyp[j - 1]
                if esle_puani(ri, h0) < 2.2 and esle_puani(ri, h1) < 2.2:
                    v = Dp[j - 2] + birlesik_puani(h0 + h1, ri)
                    if v > best:
                        best, op = v, 4
            Di[j] = best
            Pi[j] = op
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        op = P[i][j] if (i > 0 and j > 0) else (1 if i > 0 else 2)
        if op == 0:
            ops.append(("M", i - 1, j - 1, esle_puani(ref[i - 1], hyp[j - 1])))
            i -= 1; j -= 1
        elif op == 1:
            ops.append(("G", i - 1, -1, GAP))
            i -= 1
        elif op == 2:
            ops.append(("H", -1, j - 1, GAP))
            j -= 1
        elif op == 3:
            ops.append(("A", i - 2, j - 1, 2.6))
            i -= 2; j -= 1
        else:
            ops.append(("B", i - 1, j - 2, 2.6))
            i -= 1; j -= 2
    ops.reverse()
    return ops, D[n][m]


# ════════════════════════════════════════════════════════════ senaryo jetonları
def bolum_jetonlari(S, ch):
    """[dict(w, typ, si, f, syl)] — paragraf sonu PARA; typ = sözcüğün sonundaki noktalama türü."""
    toks = []
    si = 0
    for para in ch["paras"]:
        for ti, tup in enumerate(para):
            words = S._speech_of(tup).split()
            for wi, w in enumerate(words):
                tail = w.rstrip("”\"’'»)")
                p = tail[-1] if tail else ""
                typ = STRONG if p in ".?!" else MED if p in ";:" else WEAK if p == "," else None
                if wi == len(words) - 1 and ti == len(para) - 1:
                    typ = PARA
                toks.append(dict(w=w, typ=typ, si=si, f=katla(w), syl=hece(w)))
            si += 1
    return toks


# ════════════════════════════════════════════════════════════ koşu ↔ jeton aralığı
def kanitlari_cikar(ops, hyp_run, n_ref, n_run):
    """ops'tan: her koşunun kanıtı. hyp_run[j] = j. ASR sözcüğünün koşusu.
    → ev[r] = dict(lo, hi, n_match, n_hyp, subs=[jeton…]) ya da None; esl[i] = (j, puan) senaryo jetonu → ASR sözcüğü."""
    esl = {}
    per = [dict(match=[], subs=[]) for _ in range(n_run)]
    n_hyp = [0] * n_run
    for j, r in enumerate(hyp_run):
        n_hyp[r] += 1
    for kind, i, j, sc in ops:
        if kind == "M":
            r = hyp_run[j]
            if sc > 0:
                per[r]["match"].append(i)
                esl[i] = (j, sc)
            else:
                per[r]["subs"].append(i)
        elif kind == "A":
            r = hyp_run[j]
            per[r]["match"] += [i, i + 1]
            esl[i] = esl[i + 1] = (j, sc)
        elif kind == "B":
            r = hyp_run[j]
            per[r]["match"].append(i)
            esl[i] = (j, sc)
    ev = []
    for r in range(n_run):
        mt = sorted(per[r]["match"])
        if not mt:
            ev.append(None)
            continue
        # aykırı kanıtı ayıkla: ardışık jetonlar arası en çok 4 boşluk (tek tük yanlış eşleşme koşuyu şişirmesin)
        grup, cur = [], [mt[0]]
        for a, b in zip(mt, mt[1:]):
            if b - a <= 4:
                cur.append(b)
            else:
                grup.append(cur)
                cur = [b]
        grup.append(cur)
        g = max(grup, key=len)
        ev.append(dict(lo=g[0], hi=g[-1], n_match=len(g), n_hyp=n_hyp[r], subs=per[r]["subs"], extra=len(mt) - len(g)))
    return ev, esl


class SureModeli:
    """Koşu süresi ≈ a·hece + b·sözcük + c (koşu verisinden en küçük kareler)."""

    def __init__(self, a=0.16, b=0.06, c=0.10):
        self.a, self.b, self.c = a, b, c
        self.sigma_rel, self.sigma_abs = 0.10, 0.10

    def tahmin(self, hece_say, soz_say):
        return self.a * hece_say + self.b * soz_say + self.c

    def uydur(self, satirlar):
        """satirlar: [(hece, sözcük, süre)]"""
        if len(satirlar) < 12:
            return False
        X = np.array([[h, w, 1.0] for h, w, d in satirlar])
        y = np.array([d for h, w, d in satirlar])
        for _ in range(3):
            coef, *_r = np.linalg.lstsq(X, y, rcond=None)
            res = y - X @ coef
            s = 1.4826 * np.median(np.abs(res - np.median(res))) + 1e-6
            ok = np.abs(res) < 3.0 * max(s, 0.05)
            if ok.sum() < 12:
                break
            X, y = X[ok], y[ok]
        self.a = float(np.clip(coef[0], 0.06, 0.40))
        self.b = float(np.clip(coef[1], 0.0, 0.30))
        self.c = float(np.clip(coef[2], 0.0, 0.40))
        res = y - X @ np.array([self.a, self.b, self.c])
        self.sigma_abs = float(max(0.06, 1.4826 * np.median(np.abs(res - np.median(res)))))
        return True


def sinir_maliyeti(typ, d):
    """Koşular arası durak d (sn) ↔ sınırdan önceki jetonun noktalama türü."""
    if d is None:
        return 0.0
    if typ == PARA:
        return 3.0 * max(0.0, 0.60 - d)
    if typ == STRONG:
        return 3.0 * max(0.0, 0.40 - d)
    if typ == MED:
        return 2.0 * max(0.0, 0.20 - d) + 1.0 * max(0.0, d - 1.0)
    if typ == WEAK:
        return 1.0 * max(0.0, 0.14 - d) + 0.5 * max(0.0, d - 0.9)
    return 4.0 * max(0.0, d - 0.45)                                  # noktalamasız sınır: uzun durak şüpheli


def jetonlari_ata(toks, runs, ev, model, w_bos=1.0):
    """Monoton atama: her koşuya ardışık bir jeton aralığı [B[r], B[r+1]). Sert kısıt: kanıtlı jetonlar kendi koşusunda.
    Maliyet: koşu süresi ↔ beklenen süre (hece/sözcük modeli) + sınır noktalaması ↔ durak + zayıf (yerine koyma) kanıtı + boş koşu."""
    R, N = len(runs), len(toks)
    csyl = np.concatenate([[0], np.cumsum([t["syl"] for t in toks])])
    lowB = [0] * (R + 1)
    highB = [N] * (R + 1)
    cur = 0
    for r in range(R):
        if ev[r] is not None:
            cur = max(cur, ev[r]["hi"] + 1)
        lowB[r + 1] = cur
    nxt = N
    for r in range(R - 1, -1, -1):
        if ev[r] is not None:
            nxt = min(nxt, ev[r]["lo"])
        highB[r] = nxt
    lowB[0] = highB[0] = 0
    lowB[R] = highB[R] = N
    celiski = 0
    for r in range(R + 1):
        if lowB[r] > highB[r]:
            celiski += 1
            lowB[r] = highB[r] = min(max(lowB[r], 0), N)
    INF = 1e18
    dp = [dict() for _ in range(R + 1)]
    bp = [dict() for _ in range(R + 1)]
    dp[0][0] = 0.0
    for r in range(R):
        run = runs[r]
        D = run["dur"]
        sub = ev[r]["subs"] if ev[r] is not None else []
        sig = model.sigma_abs + model.sigma_rel * D
        for b2 in range(lowB[r + 1], highB[r + 1] + 1):
            bc = sinir_maliyeti(toks[b2 - 1]["typ"], run["post"]) if (r < R - 1 and b2 > 0) else 0.0
            best, arg = INF, None
            for b1, c1 in dp[r].items():
                if b1 > b2:
                    continue
                n_tok = b2 - b1
                if n_tok == 0:
                    c = 1.0 + 5.0 * max(0.0, D - 0.30)               # konuşma içermeyen koşu (nefes/tık) — uzunsa pahalı
                else:
                    exp = model.tahmin(csyl[b2] - csyl[b1], n_tok)
                    z = (D - exp) / sig
                    c = min(z * z, 9.0) + 0.3 * min(abs(z), 6.0)
                for k in sub:
                    if k < b1 or k >= b2:
                        c += 0.7
                tot = c1 + c + bc
                if tot < best:
                    best, arg = tot, b1
            if arg is not None:
                dp[r + 1][b2] = best
                bp[r + 1][b2] = arg
    B = [0] * (R + 1)
    B[R] = N
    for r in range(R, 0, -1):
        B[r - 1] = bp[r][B[r]]
    return B, dict(celiski=celiski, maliyet=dp[R].get(N), lowB=list(lowB), highB=list(highB))


def koşu_ici_zamanlar(toks, a, b, t0, t1, model):
    """Bir koşunun [a,b) jetonlarını [t0,t1] aralığına hece/sözcük ağırlığıyla dağıt. → [(start, end)]"""
    n = b - a
    if n <= 0:
        return []
    w = np.array([model.a * toks[k]["syl"] + model.b for k in range(a, b)])
    cum = np.concatenate([[0.0], np.cumsum(w)])
    ts = t0 + (t1 - t0) * cum / cum[-1]
    return [(float(ts[i]), float(ts[i + 1])) for i in range(n)]


# ════════════════════════════════════════════════════════════ bölüm hizalama sürücüsü
def hizala_bolum(S, B, ch, cache):
    """Bir bölümün koşuları + ASR önbelleği + senaryo → jeton zamanları. → dict"""
    c = B["c"]
    runs = B["runs"]
    toks = bolum_jetonlari(S, ch)
    N = len(toks)
    hyp, hyp_run = [], []
    for r in runs:
        e = cache.get(r["key"])
        ok = bool(e) and e.get("crc") == r["crc"] and e.get("text") is not None
        r["asr_text"] = e["text"] if ok else None
        ws = asr_sozcukleri(e["text"], S) if ok else []
        r["asr_words"] = ws
        for w in ws:
            hyp.append(w)
            hyp_run.append(r["i"])
    ref = [t["f"] for t in toks]
    ops, nw_puan = nw_hizala(ref, hyp)
    ev, esl = kanitlari_cikar(ops, hyp_run, N, len(runs))
    model = SureModeli()
    Bnd, info = jetonlari_ata(toks, runs, ev, model)
    for _ in range(3):                                               # süre modelini güvenilir koşulardan uydur, yeniden ata
        satirlar = []
        for r in range(len(runs)):
            a, b = Bnd[r], Bnd[r + 1]
            if b - a >= 2 and ev[r] is not None and ev[r]["n_match"] >= 0.7 * (b - a):
                satirlar.append((sum(t["syl"] for t in toks[a:b]), b - a, runs[r]["dur"]))
        if not model.uydur(satirlar):
            break
        Bn, info = jetonlari_ata(toks, runs, ev, model)
        if Bn == Bnd:
            break
        Bnd = Bn
    # kelime zamanları (bölüme göre, sn)
    tm = [None] * N
    for r, run in enumerate(runs):
        a, b = Bnd[r], Bnd[r + 1]
        run["tok0"], run["tok1"] = a, b
        for k, (s, e) in zip(range(a, b), koşu_ici_zamanlar(toks, a, b, run["a"], run["b"], model)):
            tm[k] = (s, e)
    eslesen = sorted(esl)
    n_hyp = len(hyp)
    hyp_esl = len({v[0] for v in esl.values()})
    # eşleşmeyen jeton aralıkları
    bos = []
    i = 0
    while i < N:
        if i not in esl:
            j = i
            while j < N and j not in esl:
                j += 1
            bos.append((i, j))
            i = j
        else:
            i += 1
    return dict(id=c["id"], toks=toks, tm=tm, runs=runs, B=Bnd, ev=ev, esl=esl, model=model, n_hyp=n_hyp, hyp_esl=hyp_esl,
                n_tok=N, n_esl=len(esl), bos=bos, atama=info, nw=nw_puan)


def koşu_oranlari(sonuc):
    """Koşu başına hece/sn (aykırı hız = olası yanlış atama)."""
    out = []
    for r in sonuc["runs"]:
        a, b = r["tok0"], r["tok1"]
        sy = sum(t["syl"] for t in sonuc["toks"][a:b])
        out.append(sy / r["dur"] if r["dur"] > 0 else 0.0)
    return out


# ════════════════════════════════════════════════════════════ çıktı: scribe_words.json (gösterim-uyumlu sözcükler)
_SAYI_RE = re.compile(r"\d{1,3}(?:\.\d{3})+|\d+")


def _beklenen_k(S, tok):
    nums = _SAYI_RE.findall(tok)
    if not nums:
        return None
    return sum(len(S.tr_num(int(n.replace(".", ""))).split()) for n in nums)


def jeton_gruplari(S, disp, speech_tokens):
    """Gösterim jetonları ↔ söylenen jetonlar ardışık gruplama. → [(disp_tok, [speech_idx…])] ya da None (tutarsız)."""
    dt = disp.split()
    n, m = len(dt), len(speech_tokens)
    if n == m and not any(_beklenen_k(S, t) for t in dt):
        return [(dt[i], [i]) for i in range(n)]
    if n > m:
        return None
    exp = [_beklenen_k(S, t) for t in dt]
    fd = [katla(t) for t in dt]
    fs = [katla(t) for t in speech_tokens]
    INF = 1e9
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    P = [[0] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for i in range(n):
        for j in range(m):
            if D[i][j] >= INF:
                continue
            for k in range(1, min(12, m - j) + 1):
                if exp[i] is not None:
                    c = 0.0 if k == exp[i] else 2.0 + abs(k - exp[i])
                else:
                    c = 0.0 if k == 1 else 3.0 * (k - 1)
                    c += 0.5 * (1 - _orani(fd[i], fs[j])) if fd[i] and fs[j] else 0.0
                v = D[i][j] + c
                if v < D[i + 1][j + k]:
                    D[i + 1][j + k] = v
                    P[i + 1][j + k] = k
    if D[n][m] >= INF:
        return None
    gr = []
    i, j = n, m
    while i > 0:
        k = P[i][j]
        gr.append((dt[i - 1], list(range(j - k, j))))
        i -= 1
        j -= k
    gr.reverse()
    return gr


_SON_NOKTA = re.compile(r"[.,;:?!“”\"’'»«()]+$")


def _temiz(w):
    return _SON_NOKTA.sub("", w).strip("“”\"«").strip()


def kelime_listesi(S, sonuc, sents, ham=False):
    """sonuc (bir bölüm) + o bölümün cümleleri (S.sentences) → [{text,start,end,type}] (bölüme göre sn).
    Varsayılan: her GÖSTERİM jetonu için bir sözcük (rakamlı jetonlar tek sözcük) → ses_hizala.py eşleştirmesi %100 olur;
    ham=True: saf söylenen sözcükler (ses_hizala_yerel.py biçimi)."""
    toks, tm = sonuc["toks"], sonuc["tm"]
    out = []
    k0 = 0
    uyar = []
    for s in sents:
        st = s["speech"].split()
        n = len(st)
        if k0 + n > len(toks):
            uyar.append(f"{s['id']}: jeton sayısı bölümle uyuşmuyor")
            break
        gr = None if ham else jeton_gruplari(S, s["disp"], st)
        if gr is None:
            if not ham:
                uyar.append(f"{s['id']}: gösterim↔söylenen gruplanamadı, saf söylenen sözcükler yazıldı")
            for i in range(n):
                a, b = tm[k0 + i]
                out.append(dict(text=_temiz(st[i]), start=a, end=b, type="word", si=s["id"]))
        else:
            for dtok, idxs in gr:
                a = tm[k0 + idxs[0]][0]
                b = tm[k0 + idxs[-1]][1]
                out.append(dict(text=_temiz(dtok), start=a, end=b, type="word", si=s["id"]))
        k0 += n
    if k0 != len(toks):
        uyar.append(f"cümlelerin jeton toplamı {k0} ≠ bölüm jetonu {len(toks)}")
    return out, uyar


# ════════════════════════════════════════════════════════════ ana akış
def _md5(path):
    import hashlib
    h = hashlib.md5()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def tablo_yaz(path, sonuclar):
    """Koşu koşu: zaman, ASR metni, atanan senaryo jetonları (gözle denetim için)."""
    L = []
    for sn in sonuclar:
        c0 = sn["t0"]
        L.append(f"=== {sn['id']}  (jeton {sn['n_tok']}, koşu {len(sn['runs'])}) ===")
        rates = koşu_oranlari(sn)
        for r, rate in zip(sn["runs"], rates):
            a, b = r["tok0"], r["tok1"]
            tx = " ".join(t["w"] for t in sn["toks"][a:b])
            ev = sn["ev"][r["i"]]
            evs = f"ev {ev['lo']}-{ev['hi']} ({ev['n_match']}/{ev['n_hyp']})" if ev else "ev -"
            L.append(f"{c0 + r['a']:8.2f}-{c0 + r['b']:8.2f} d{r['dur']:5.2f} p{(r['post'] if r['post'] is not None else -1):5.2f} "
                     f"[{a:3d}:{b:3d}) {rate:4.1f}h/s {evs:22s} ASR: {r['asr_text']!s:48.48s} | SEN: {tx}")
        L.append("")
    open(path, "w", encoding="utf-8").write("\n".join(L))


def hesapla_hepsi(args, S):
    """Koşular + ASR (önbellekli) + hizalama (+ akustik HMM iyileştirmesi), tüm (ya da seçilen) bölümler. → ctx"""
    secim = set(args.bolum.split(",")) if args.bolum else None
    x, sr, vc, wav_path, bol = bolumleri_hazirla(secim)
    isler = asr_isleri(x, sr, bol)
    cache_path = os.path.join(OUT, ASR_ONBELLEK)
    if args.asr_yok:
        cache = cache_oku(cache_path)
        eksik = sum(1 for j in isler if not (j[0] in cache and cache[j[0]].get("crc") == j[3]))
        log(f"[ASR] önbellekten okunuyor; ASR'siz koşu: {eksik}/{len(isler)}")
    else:
        cache = asr_calistir(_onsel(isler), cache_path, wav_path, isci=args.isci)
    ctx = dict(x=x, sr=sr, vc=vc, wav_path=wav_path, bol=bol, cache=cache, sonuclar=[], kelimeler=[], hmm=None,
               rapor=dict(bolumler={}, uyarilar=[]))
    if args.yalniz_asr:
        return ctx
    sents_all = S.sentences(PA.PART)
    rapor = ctx["rapor"]
    for B in bol:
        c = B["c"]
        cid = c["id"]
        ch = next((q for q in S.CHAPTERS if q["id"] == cid), None)
        if ch is None or not ch["paras"]:
            rapor["uyarilar"].append(f"{cid}: senaryoda bölüm yok/boş, atlandı")
            log("UYARI:", rapor["uyarilar"][-1])
            continue
        sn = hizala_bolum(S, B, ch, cache)
        sn["t0"] = c["t0"]
        sn["chap"] = B
        ctx["sonuclar"].append(sn)
    if not getattr(args, "agirlik", False) and ctx["sonuclar"]:
        ctx["hmm"] = akustik_iyilestir(S, ctx, n_iter=getattr(args, "hmm_iter", 8))
    cum_rapor = {}
    for sn in ctx["sonuclar"]:
        B, c, cid = sn["chap"], sn["chap"]["c"], sn["id"]
        sents = [s for s in sents_all if s["ch"] == cid]
        words, uyar = kelime_listesi(S, sn, sents, ham=args.ham_konusma)
        for u in uyar:
            rapor["uyarilar"].append(f"{cid} {u}")
            log("UYARI:", cid, u)
        ctx["kelimeler"].append((c, words))
        # cümle sınırları durağa mı yaslı, koşu içinde mi?
        tok_run = {}
        for r in sn["runs"]:
            for k in range(r["tok0"], r["tok1"]):
                tok_run[k] = r["i"]
        k0 = 0
        for s in sents:
            n = len(s["speech"].split())
            if n == 0 or k0 + n > sn["n_tok"]:
                break
            ra, rb = tok_run.get(k0), tok_run.get(k0 + n - 1)
            cum_rapor[s["id"]] = dict(
                t0_durak=bool(ra is not None and sn["runs"][ra]["tok0"] == k0),
                t1_durak=bool(rb is not None and sn["runs"][rb]["tok1"] == k0 + n),
                run_a=ra, run_b=rb)
            k0 += n
        rates = koşu_oranlari(sn)
        aykiri = [(round(c["t0"] + r["a"], 2), round(q, 1), r["asr_text"]) for r, q in zip(sn["runs"], rates)
                  if sum(t["syl"] for t in sn["toks"][r["tok0"]:r["tok1"]]) >= 3 and (q < 3.2 or q > 9.0)]
        bos = [(a, b, " ".join(t["w"] for t in sn["toks"][a:b])) for a, b in sn["bos"] if b - a >= 2]
        n_ev = sum(1 for e in sn["ev"] if e is not None)
        n_bos_run = sum(1 for r in sn["runs"] if r["tok1"] == r["tok0"])
        n_hmm = sum(1 for r in sn["runs"] if r.get("hmm_durum") == "tamam")
        suphe = [(round(c["t0"] + r["a"], 2), round(r["hmm_z"], 1), r["asr_text"], " ".join(t["w"] for t in sn["toks"][r["tok0"]:r["tok1"]]))
                 for r in sn["runs"] if r.get("hmm_z") is not None and r["hmm_z"] < -3.0]
        rapor["bolumler"][cid] = dict(
            jeton=sn["n_tok"], jeton_eslesen=sn["n_esl"], jeton_oran=round(sn["n_esl"] / sn["n_tok"], 4),
            asr_sozcuk=sn["n_hyp"], asr_eslesen=sn["hyp_esl"], asr_oran=round(sn["hyp_esl"] / max(1, sn["n_hyp"]), 4),
            kosu=len(sn["runs"]), kanitli_kosu=n_ev, bos_kosu=n_bos_run, kanitsiz_kosu=len(sn["runs"]) - n_ev, hmm_kosu=n_hmm,
            model=dict(hece=round(sn["model"].a, 4), soz=round(sn["model"].b, 4), sabit=round(sn["model"].c, 4), sigma=round(sn["model"].sigma_abs, 3)),
            celiski=sn["atama"]["celiski"], aykiri_hiz=aykiri, akustik_suphe=suphe, eksik_sozcuk=sn.get("eksik", []), eslesmeyen_bolgeler=bos, kosu_bilgi=B["info"])
        log(f"{cid:3s} jeton {sn['n_tok']:4d} eşleşen {sn['n_esl']:4d} (%{100 * sn['n_esl'] / sn['n_tok']:.1f}) | ASR sözcük {sn['n_hyp']:4d} eşleşen "
            f"{sn['hyp_esl']:4d} (%{100 * sn['hyp_esl'] / max(1, sn['n_hyp']):.1f}) | koşu {len(sn['runs']):3d} (kanıtlı {n_ev}, boş {n_bos_run}, HMM {n_hmm}) | "
            f"hece/sn modeli a={sn['model'].a:.3f} b={sn['model'].b:.3f} c={sn['model'].c:.3f} | aykırı hız {len(aykiri)} | akustik şüphe {len(suphe)} | eşleşmeyen bölge(≥2) {len(bos)}")
    rapor["cumleler"] = cum_rapor
    return ctx


def ana_hizala(args):
    S = senaryo_yukle()
    ctx = hesapla_hepsi(args, S)
    if args.yalniz_asr:
        return
    sonuclar, rapor = ctx["sonuclar"], ctx["rapor"]
    tum = []
    for c, words in ctx["kelimeler"]:
        for w in words:
            a, b = round(c["t0"] + w["start"], 3), round(c["t0"] + w["end"], 3)
            tum.append(dict(text=w["text"], start=a, end=max(b, a + 0.001), type="word"))
    if not tum:
        log("hiç sözcük üretilmedi")
        return
    # kendi kendine denetim: sıralı, çakışmasız, bölüm sınırları içinde
    cak = sum(1 for a, b in zip(tum[:-1], tum[1:]) if b["start"] < a["end"] - 1e-6)
    ters = sum(1 for w in tum if w["end"] <= w["start"])
    log(f"[denetim] {len(tum)} sözcük; çakışan komşu: {cak}; süresi ≤0: {ters}")
    if cak or ters:
        rapor["uyarilar"].append(f"scribe_words: çakışan {cak}, süresi ≤0 {ters}")
    ek = "_" + args.bolum.replace(",", "_") if args.bolum else ""    # bölüm seçimi: ana dosyalara dokunma
    sw_path = os.path.join(OUT, f"scribe_words{ek}.json")
    yedek = os.path.join(OUT, "scribe_words_yerel_eski.json")
    rap_path = os.path.join(OUT, f"hizala_asr_rapor{ek}.json")
    benim = None
    if os.path.exists(rap_path):
        try:
            benim = json.load(open(rap_path, encoding="utf-8")).get("scribe_md5")
        except Exception:                                            # noqa: BLE001
            benim = None
    if not ek and os.path.exists(sw_path) and not os.path.exists(yedek) and _md5(sw_path) != benim:
        shutil.copy2(sw_path, yedek)
        log("yedek:", yedek)
    tmp = sw_path + ".tmp"
    json.dump(tum, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, sw_path)
    log("yazıldı:", sw_path, len(tum), "sözcük")
    tab = os.path.join(OUT, f"hizala_asr_kosular{ek}.txt")
    tablo_yaz(tab, sonuclar)
    toplam = dict(jeton=sum(s["n_tok"] for s in sonuclar), jeton_eslesen=sum(s["n_esl"] for s in sonuclar),
                  asr_sozcuk=sum(s["n_hyp"] for s in sonuclar), asr_eslesen=sum(s["hyp_esl"] for s in sonuclar),
                  kosu=sum(len(s["runs"]) for s in sonuclar))
    toplam["jeton_oran"] = round(toplam["jeton_eslesen"] / toplam["jeton"], 4)
    toplam["asr_oran"] = round(toplam["asr_eslesen"] / max(1, toplam["asr_sozcuk"]), 4)
    cs = rapor.get("cumleler", {})
    toplam["cumle"] = len(cs)
    toplam["cumle_t0_durakta"] = sum(1 for v in cs.values() if v["t0_durak"])
    toplam["cumle_t1_durakta"] = sum(1 for v in cs.values() if v["t1_durak"])
    toplam["seste_olmayan_sozcuk"] = sum(len(s.get("eksik", [])) for s in sonuclar)
    rapor.update(toplam=toplam, scribe_md5=_md5(sw_path), uretim=time.strftime("%Y-%m-%d %H:%M:%S"))
    json.dump(rapor, open(rap_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log(f"TOPLAM jeton {toplam['jeton']} eşleşen {toplam['jeton_eslesen']} (%{100 * toplam['jeton_oran']:.1f}); ASR sözcük {toplam['asr_sozcuk']} "
        f"eşleşen {toplam['asr_eslesen']} (%{100 * toplam['asr_oran']:.1f}); koşu {toplam['kosu']}; cümle {toplam['cumle']}: "
        f"başı durakta {toplam['cumle_t0_durakta']}, sonu durakta {toplam['cumle_t1_durakta']}")
    log("koşu tablosu:", tab, "· rapor:", rap_path)
    if args.timeline:
        import subprocess
        env = dict(os.environ)
        if PA.PART:
            env["MEDICI_PART"] = str(PA.PART)
        r = subprocess.run([sys.executable, os.path.join(HERE, "ses_hizala.py")], cwd=HERE, env=env, capture_output=True, text=True)
        log(r.stdout[-3000:])
        if r.returncode:
            log("ses_hizala.py HATA:", r.stderr[-2000:])


# ════════════════════════════════════════════════════════════ doğrulama / karşılaştırma
def _yuzdelik(a, ps=(50, 90, 95, 99, 100)):
    a = np.asarray(a, dtype=float)
    return {p: float(np.percentile(a, p)) for p in ps} if len(a) else {}


def karsilastir(args):
    """Eski (timeline_yerel_eski.json) ↔ yeni (timeline.json): cümle başlangıç/bitiş farkları."""
    eski_p = os.path.join(OUT, "timeline_yerel_eski.json")
    yeni_p = os.path.join(OUT, "timeline.json")
    E = {s["id"]: s for s in json.load(open(eski_p, encoding="utf-8"))["sentences"]}
    Yn = {s["id"]: s for s in json.load(open(yeni_p, encoding="utf-8"))["sentences"]}
    ids = [i for i in Yn if i in E]
    d0 = np.array([Yn[i]["t0"] - E[i]["t0"] for i in ids])
    d1 = np.array([Yn[i]["t1"] - E[i]["t1"] for i in ids])
    out = []
    P = out.append
    P(f"ESKİ (yerel DP) ↔ YENİ (ASR destekli): {len(ids)} ortak cümle")
    for ad, d in (("başlangıç t0", d0), ("bitiş t1", d1), ("her ikisi (t0 ve t1)", np.concatenate([d0, d1]))):
        a = np.abs(d)
        q = _yuzdelik(a)
        P(f"  |Δ| {ad:22s} medyan {q[50]:.3f}  %90 {q[90]:.3f}  %95 {q[95]:.3f}  azami {q[100]:.3f} sn   ort işaretli Δ {d.mean():+.3f}   "
          f">0,2: {int((a > 0.2).sum())}  >0,5: {int((a > 0.5).sum())}  >1,0: {int((a > 1.0).sum())}  (n={len(a)})")
    mx = np.maximum(np.abs(d0), np.abs(d1))
    order = np.argsort(-mx)[:10]
    P("  en büyük 10 fark (cümle | eski t0–t1 | yeni t0–t1 | Δt0 Δt1):")
    sents = {s["id"]: s for s in senaryo_yukle().sentences(PA.PART)}
    for k in order:
        i = ids[k]
        P(f"   {i:7s} | {E[i]['t0']:8.2f}–{E[i]['t1']:8.2f} | {Yn[i]['t0']:8.2f}–{Yn[i]['t1']:8.2f} | {d0[k]:+6.2f} {d1[k]:+6.2f} | {sents.get(i, {}).get('disp', '')[:60]}")
    P("  bölüm bazında medyan / %95 / azami |Δ| (t0,t1 birlikte):")
    for cid in sorted({Yn[i]["ch"] for i in ids}):
        kk = [n for n, i in enumerate(ids) if Yn[i]["ch"] == cid]
        a = np.concatenate([np.abs(d0[kk]), np.abs(d1[kk])])
        q = _yuzdelik(a)
        P(f"   {cid:3s} n={len(kk):3d}  {q[50]:.3f} / {q[95]:.3f} / {q[100]:.3f}")
    for ad, T in (("eski", E), ("yeni", Yn)):
        sl = list(T.values())
        gaps = [b["t0"] - a["t1"] for a, b in zip(sl[:-1], sl[1:]) if a["ch"] == b["ch"]]
        neg = [g for g in gaps if g < -0.0005]
        P(f"  {ad}: cümle arası boşluk (aynı bölüm içinde) n={len(gaps)} · gap<0: {len(neg)} (en kötü {min(gaps):+.3f}) · gap=0: {sum(1 for g in gaps if abs(g) <= 0.0005)} · medyan {np.median(gaps):.3f}")
    # konuşma etkinliği (miks.py zaman çizelgesi denetimine benzer): cümle içinde konuşma payı ↑, cümleler arası boşlukta ↓ beklenir
    try:
        x, sr = load_wav(os.path.join(OUT, "voice.wav"))
        vc = json.load(open(os.path.join(OUT, "voice_chapters.json"), encoding="utf-8"))
        n_fr = int(len(x) / sr / HOP) + 1
        act = np.zeros(n_fr, dtype=bool)
        for c in vc["chapters"]:
            seg = x[int(round(c["t0"] * sr)): int(round(c["t1"] * sr))]
            db = enerji_db(seg, sr)
            thr = max(np.percentile(db, 95) - DURAK_ESIK_DB, np.percentile(db, 10) + 10.0)
            i0 = int(round(c["t0"] / HOP))
            act[i0: i0 + len(db)] = db >= thr
        for ad, T in (("eski", E), ("yeni", Yn)):
            sl = list(T.values())
            ins, btw = [], []
            for k, sn_ in enumerate(sl):
                lo, hi = int(sn_["t0"] / HOP), min(int(sn_["t1"] / HOP), n_fr)
                if hi > lo + 5:
                    ins.append(float(act[lo:hi].mean()))
                if k + 1 < len(sl) and sl[k + 1]["ch"] == sn_["ch"]:
                    g0, g1 = int(sn_["t1"] / HOP) + 5, int(sl[k + 1]["t0"] / HOP) - 5
                    if g1 > g0 + 10:
                        btw.append(float(act[g0:g1].mean()))
            P(f"  konuşma etkinliği ({ad}): cümle içi ort. {np.mean(ins):.3f} (en düşük {np.min(ins):.2f}; <0,8: {int(np.sum(np.array(ins) < 0.8))}) · "
              f"cümleler arası boşlukta ort. {np.mean(btw) if btw else 0:.3f} (n={len(btw)}; >0,1: {int(np.sum(np.array(btw) > 0.1)) if btw else 0})")
    except Exception as e:                                           # noqa: BLE001
        P(f"  konuşma etkinliği hesaplanamadı: {type(e).__name__}: {e}")
    P("  c2s5–c2s7:")
    for i in ("c2s4", "c2s5", "c2s6", "c2s7", "c2s8"):
        if i in Yn and i in E:
            P(f"   {i}: eski {E[i]['t0']:.2f}–{E[i]['t1']:.2f} → yeni {Yn[i]['t0']:.2f}–{Yn[i]['t1']:.2f}")
    txt = "\n".join(out)
    print(txt)
    open(os.path.join(OUT, "hizala_asr_karsilastirma.txt"), "w", encoding="utf-8").write(txt + "\n")


def pencere_kontrol(S, bekle, hyp_text, onceki, sonraki):
    """Pencere ASR çıktısı ↔ beklenen cümle (söylenen metin). → dict(wer, bas_fazla, son_fazla, bas_sizinti, son_sizinti, bas_eksik, son_eksik)"""
    import asr
    exp = [k for k in (katla(w) for w in bekle.split()) if k]
    hyp = asr_sozcukleri(hyp_text, S)
    res = dict(wer=float(asr.wer(bekle, hyp_text)) if hyp_text.strip() else 1.0, hyp=hyp_text)
    if not hyp:
        res.update(bas_fazla=0, son_fazla=0, bas_sizinti=False, son_sizinti=False, bas_eksik=len(exp), son_eksik=len(exp), bos=True)
        return res
    ops, _ = nw_hizala(exp, hyp, band=60)
    sag = [(i, j) for kind, i, j, sc in ops if kind in ("M", "A", "B") and sc >= 1.0]
    if not sag:
        res.update(bas_fazla=0, son_fazla=0, bas_sizinti=False, son_sizinti=False, bas_eksik=0, son_eksik=0, eslesme_yok=True)
        return res
    i0, j0 = sag[0]
    i1, j1 = sag[-1]
    th, te = len(hyp) - 1 - j1, len(exp) - 1 - i1
    bas_fazla, bas_eksik = max(0, j0 - i0), max(0, i0 - j0)
    son_fazla, son_eksik = max(0, th - te), max(0, te - th)

    def benzer(ws, ref_text, uc):
        ref = [k for k in (katla(w) for w in (ref_text or "").split()) if k]
        ref = ref[:4] if uc == "bas" else ref[-4:]
        return any(esle_puani(w, r) > 0 for w in ws for r in ref)

    ekstra_bas = hyp[:bas_fazla]
    ekstra_son = hyp[len(hyp) - son_fazla:] if son_fazla else []
    res.update(bas_fazla=bas_fazla, son_fazla=son_fazla, bas_eksik=bas_eksik, son_eksik=son_eksik,
               bas_sizinti=bool(ekstra_bas) and benzer(ekstra_bas, " ".join((onceki or "").split()[-4:]), "son"),
               son_sizinti=bool(ekstra_son) and benzer(ekstra_son, " ".join((sonraki or "").split()[:4]), "bas"))
    return res


def dogrula(args):
    """Bağımsız doğrulama: yeni timeline.json'daki cümle pencereleri (±0,1 sn) ASR ile yeniden yazdırılır; beklenen cümleyle WER ve komşu sızıntısı.
    Aynı cümleler eski timeline için de ölçülür (karşılaştırma). Sonuç: out_pN/hizala_asr_dogrulama.json"""
    S = senaryo_yukle()
    yeni = json.load(open(os.path.join(OUT, "timeline.json"), encoding="utf-8"))
    eski_p = os.path.join(OUT, "timeline_yerel_eski.json")
    eski = json.load(open(eski_p, encoding="utf-8")) if os.path.exists(eski_p) else None
    sents = {s["id"]: s for s in S.sentences(PA.PART)}
    sira = [s["id"] for s in yeni["sentences"]]
    ozel = [i for i in ("c2s4", "c2s5", "c2s6", "c2s7", "c2s8") if i in sira]
    rng = random.Random(args.tohum)
    adaylar = [i for i in sira if i not in ozel]
    rast = rng.sample(adaylar, min(args.n, len(adaylar)))
    secim = ozel + rast
    T = {"yeni": {s["id"]: s for s in yeni["sentences"]}}
    if eski:
        T["eski"] = {s["id"]: s for s in eski["sentences"]}
    wav_path = os.path.join(OUT, "voice.wav")
    x, sr = load_wav(wav_path)
    dur = len(x) / sr
    isler, meta = [], {}
    for ver, pay, ad in (("yeni", 0.1, "yeni"), ("yeni", 0.0, "yeni_sikis"), ("eski", 0.1, "eski")):
        if ver not in T:
            continue
        for sid in secim:
            if sid not in T[ver]:
                continue
            s = T[ver][sid]
            a, b = max(0.0, s["t0"] - pay), min(dur, s["t1"] + pay)
            if b - a < 0.3:
                continue
            a, b = round(a, 3), round(b, 3)
            key = f"v|{ad}|{sid}|{a:.3f}|{b:.3f}"
            crc = _crc(x[int(round(a * sr)): int(round(b * sr))])
            isler.append((key, a, b, crc, dict(ad=ad, sid=sid)))
            meta[(ad, sid)] = key
    cache = asr_calistir(isler, os.path.join(OUT, "asr_dogrulama.json"), wav_path, isci=args.isci, baslik="DOĞRULAMA")
    sonuc = {}
    for (ad, sid), key in meta.items():
        k = sira.index(sid)
        onceki = sents[sira[k - 1]]["speech"] if k > 0 and sents[sira[k - 1]]["ch"] == sents[sid]["ch"] else None
        sonraki = sents[sira[k + 1]]["speech"] if k + 1 < len(sira) and sents[sira[k + 1]]["ch"] == sents[sid]["ch"] else None
        e = cache.get(key)
        if not e:
            continue
        r = pencere_kontrol(S, sents[sid]["speech"], e["text"], onceki, sonraki)
        s = T["eski" if ad == "eski" else "yeni"][sid]
        r.update(t0=s["t0"], t1=s["t1"])
        sonuc.setdefault(ad, {})[sid] = r
    L = []
    P = L.append
    for ad, baslik in (("yeni", "YENİ  (pencere = cümle ±0,1 sn)"), ("yeni_sikis", "YENİ  (sıkı pencere = tam t0–t1, pay yok)"), ("eski", "ESKİ  (pencere = cümle ±0,1 sn)")):
        R = sonuc.get(ad)
        if not R:
            continue
        w = np.array([r["wer"] for r in R.values()])
        sz = [sid for sid, r in R.items() if r["bas_sizinti"] or r["son_sizinti"]]
        fz = [sid for sid, r in R.items() if (r["bas_fazla"] >= 1 or r["son_fazla"] >= 1) and sid not in sz]
        ek = [sid for sid, r in R.items() if r["bas_eksik"] >= 2 or r["son_eksik"] >= 2]
        P(f"{baslik}: {len(R)} cümle · WER ort {w.mean():.3f} medyan {np.median(w):.3f} %90 {np.percentile(w, 90):.3f} azami {w.max():.3f} · "
          f"WER>0,3: {int((w > 0.3).sum())} · komşu sızıntısı: {len(sz)} {sz} · başka fazlalık: {len(fz)} · uçta ≥2 sözcük eksik: {len(ek)} {ek}")
    P("")
    P("c2s4–c2s8 ve ayrıntı (YENİ ±0,1 sn penceresi):")
    for sid in ozel:
        r = sonuc.get("yeni", {}).get(sid)
        if r:
            rs = sonuc.get("eski", {}).get(sid)
            P(f"  {sid} {r['t0']:.2f}–{r['t1']:.2f} WER {r['wer']:.2f} sızıntı(baş/son) {r['bas_sizinti']}/{r['son_sizinti']} | ASR: {r['hyp']}")
            if rs:
                P(f"      eski {rs['t0']:.2f}–{rs['t1']:.2f} WER {rs['wer']:.2f} sızıntı {rs['bas_sizinti']}/{rs['son_sizinti']} | ASR: {rs['hyp']}")
            P(f"      beklenen: {sents[sid]['speech']}")
    P("")
    P("WER > 0,25 olan YENİ cümleler:")
    for sid, r in sonuc.get("yeni", {}).items():
        if r["wer"] > 0.25 or r["bas_sizinti"] or r["son_sizinti"]:
            P(f"  {sid} {r['t0']:.2f}–{r['t1']:.2f} WER {r['wer']:.2f} fazla(b/s) {r['bas_fazla']}/{r['son_fazla']} eksik(b/s) {r['bas_eksik']}/{r['son_eksik']} sızıntı {r['bas_sizinti']}/{r['son_sizinti']}")
            P(f"      ASR: {r['hyp']}")
            P(f"      BEK: {sents[sid]['speech']}")
    txt = "\n".join(L)
    print(txt)
    json.dump(sonuc, open(os.path.join(OUT, "hizala_asr_dogrulama.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(OUT, "hizala_asr_dogrulama.txt"), "w", encoding="utf-8").write(txt + "\n")


def loo_testi(args):
    """Koşu içi sözcük/cümle sınırı doğruluğu — 'duraktan bir bırak': ardışık iki koşu, aradaki durak silinip (ses dalgası düzeyinde,
    her iki yandan --kirp sn kırpılarak) tek koşu gibi birleştirilir; yöntemin tahmin ettiği iç sınır gerçek (durak) konumla karşılaştırılır.
    Hece-ağırlığı modeli ile akustik HMM (bölüm bazlı 2 katlı çapraz doğrulama: model, test bölümlerini hiç görmeden eğitilir) karşılaştırılır.
    Not: durak çevresinde konuşma uzaması olduğundan tahminler hafif kötümserdir; gerçek koşu içi sınırlarda hata genelde daha küçüktür."""
    S = senaryo_yukle()
    args.asr_yok = True
    args.agirlik = True
    ctx = hesapla_hepsi(args, S)
    ham, nmu, nsd = hmm_hazirla(ctx)
    ids = [sn["id"] for sn in ctx["sonuclar"]]
    fold = {cid: k % 2 for k, cid in enumerate(ids)}
    log("[LOO] HMM eğitimi (2 katlı, bölüm bazlı)")
    modeller = {}
    for f in (0, 1):
        egit = [h for h in ham if h["guvenli"] and fold[h["sn"]["id"]] != f]
        modeller[f] = akustik_egit([(h["Xn"], h["ph"], h["pl"], h["pr"]) for h in egit], n_iter=getattr(args, "hmm_iter", 8), verbose=False)
    tam = akustik_egit([(h["Xn"], h["ph"], h["pl"], h["pr"]) for h in ham if h["guvenli"]], n_iter=getattr(args, "hmm_iter", 8), verbose=False)
    sr = ctx["sr"]
    K = args.kirp
    E = {"agirlik": [], "hmm_capraz": [], "hmm_ici": []}
    kayit = []
    for sn in ctx["sonuclar"]:
        toks, runs, m, seg = sn["toks"], sn["runs"], sn["model"], sn["chap"]["seg"]
        for r in range(len(runs) - 1):
            a, b = runs[r], runs[r + 1]
            a0, a1, b1 = a["tok0"], a["tok1"], b["tok1"]
            if a1 == a0 or b1 == a1 or a1 != b["tok0"]:
                continue
            w1 = seg[int(round(a["a"] * sr)): int(round((a["b"] - K) * sr))]
            w2 = seg[int(round((b["a"] + K) * sr)): int(round(b["b"] * sr))]
            if len(w1) < 0.15 * sr or len(w2) < 0.15 * sr:
                continue
            D1, D2 = len(w1) / sr, len(w2) / sr
            W1 = sum(m.a * t["syl"] + m.b for t in toks[a0:a1])
            W2 = sum(m.a * t["syl"] + m.b for t in toks[a1:b1])
            E["agirlik"].append((D1 + D2) * W1 / (W1 + W2) - D1)
            X = (ozellik(np.concatenate([w1, w2]), sr) - nmu) / nsd
            ph = [fonlar(toks[k]["w"]) for k in range(a0, b1)]
            n1 = a1 - a0
            for ad, mod in (("hmm_capraz", modeller[fold[sn["id"]]]), ("hmm_ici", tam)):
                w, ll = akustik_hizala(mod, X, ph, ilk_sil=False, son_sil=False, sp_arasi=True)
                est = ((w[n1 - 1][1] + w[n1][0]) / 2) * HOP + 0.0075
                E[ad].append(est - D1)
            kayit.append((sn["id"], a["post"], toks[a1 - 1]["typ"]))
    L = []
    P = L.append
    P(f"DURAKTAN BİR BIRAK (n={len(kayit)} iç sınır; her yandan {K * 1000:.0f} ms kırpıldı; ses dalgası düzeyinde birleştirme):")
    for ad, baslik in (("agirlik", "hece/sözcük ağırlık modeli"), ("hmm_capraz", "akustik HMM (çapraz doğrulama)"), ("hmm_ici", "akustik HMM (tüm veriyle eğitilmiş)")):
        e = np.array(E[ad])
        ae = np.abs(e)
        q = _yuzdelik(ae)
        P(f"  {baslik:38s} |hata| medyan {q[50]:.3f}  %90 {q[90]:.3f}  %95 {q[95]:.3f}  %99 {q[99]:.3f}  azami {q[100]:.3f} sn · ort işaretli {e.mean():+.3f} · "
          f"≤0,1: %{100 * (ae <= 0.1).mean():.1f}  ≤0,2: %{100 * (ae <= 0.2).mean():.1f}  >0,3: {int((ae > 0.3).sum())}  >0,6: {int((ae > 0.6).sum())}")
    for ad, filt in (("cümle sonu (. ? ! paragraf)", lambda k: k[2] in (STRONG, PARA)), ("noktalamasız/virgül/;:", lambda k: k[2] not in (STRONG, PARA))):
        kk = [i for i, k in enumerate(kayit) if filt(k)]
        if kk:
            for a_, baslik in (("agirlik", "ağırlık"), ("hmm_capraz", "HMM çapraz")):
                q = _yuzdelik(np.abs(np.array(E[a_]))[kk])
                P(f"    {ad:30s} {baslik:11s} n={len(kk):3d} medyan {q[50]:.3f} %95 {q[95]:.3f} azami {q[100]:.3f}")
    txt = "\n".join(L)
    print(txt)
    open(os.path.join(OUT, "hizala_asr_loo.txt"), "w", encoding="utf-8").write(txt + "\n")
    return E


def sondaj(args):
    """Koşu İÇİ sözcük sınırı için bağımsız ASR sondajı: akustik HMM sınırı ↔ hece-ağırlığı sınırı. Seçilen sınırda (her yanda 2 sözcük bağlamı) ses
    iki parçaya kesilir; sol parça ("w1 w2") ve sağ parça ("w3 w4") ASR ile yazdırılıp beklenen sözcüklerle WER ölçülür. Kesim doğru sınıra
    yakınsa iki parça da doğru çıkar; yanlışsa sözcük kesilir ya da komşu sözcüğün parçası sızar. Yalnız iki yöntemin ≥50 ms ayrıştığı sınırlar."""
    import asr
    S = senaryo_yukle()
    args.asr_yok = True
    args.agirlik = False
    ctx = hesapla_hepsi(args, S)
    sr = ctx["sr"]
    rng = random.Random(args.tohum)
    adaylar = []
    for sn in ctx["sonuclar"]:
        toks, m = sn["toks"], sn["model"]
        for r in sn["runs"]:
            if r.get("hmm_durum") != "tamam":
                continue
            wt = koşu_ici_zamanlar(toks, r["tok0"], r["tok1"], r["a"], r["b"], m)
            for k in range(r["tok0"] + 2, r["tok1"] - 1):
                hb = 0.5 * (sn["tm"][k - 1][1] + sn["tm"][k][0])
                wb = wt[k - r["tok0"]][0]
                if abs(hb - wb) < 0.05:
                    continue
                adaylar.append((sn, r, k, hb, wb))
    rng.shuffle(adaylar)
    secim = adaylar[:args.n]
    log(f"[sondaj] {len(adaylar)} aday sınır, {len(secim)} seçildi")
    wav_path = ctx["wav_path"]
    x = ctx["x"]
    isler, meta = [], []
    for sn, r, k, hb, wb in secim:
        c0 = sn["t0"]
        toks = sn["toks"]
        sol0 = c0 + sn["tm"][k - 2][0] - 0.04
        sag1 = c0 + sn["tm"][k + 1][1] + 0.04
        exp_l = " ".join(t["w"] for t in toks[k - 2:k])
        exp_r = " ".join(t["w"] for t in toks[k:k + 2])
        for ad, b in (("hmm", hb), ("agirlik", wb)):
            bb = c0 + b
            for yan, (a_, b_), ex in (("sol", (sol0, bb), exp_l), ("sag", (bb, sag1), exp_r)):
                a_, b_ = round(a_, 3), round(b_, 3)
                key = f"s|{ad}|{yan}|{sn['id']}|{k}|{a_:.3f}|{b_:.3f}"
                crc = _crc(x[int(round(a_ * sr)): int(round(b_ * sr))])
                isler.append((key, a_, b_, crc, dict(ad=ad, yan=yan)))
                meta.append((key, ad, yan, sn["id"], k, ex))
    cache = asr_calistir(isler, os.path.join(OUT, "asr_sondaj.json"), wav_path, isci=args.isci, baslik="SONDAJ")
    res = {"hmm": [], "agirlik": []}
    per = {}
    for key, ad, yan, cid, k, ex in meta:
        e = cache.get(key)
        if not e:
            continue
        w = float(asr.wer(ex, e["text"])) if e["text"].strip() else 1.0
        per.setdefault((cid, k), {}).setdefault(ad, {})[yan] = (w, e["text"], ex)
    iyi = kotu = esit = 0
    for (cid, k), d in per.items():
        if "hmm" not in d or "agirlik" not in d or len(d["hmm"]) < 2 or len(d["agirlik"]) < 2:
            continue
        wh = d["hmm"]["sol"][0] + d["hmm"]["sag"][0]
        ww = d["agirlik"]["sol"][0] + d["agirlik"]["sag"][0]
        res["hmm"].append(wh / 2)
        res["agirlik"].append(ww / 2)
        if wh < ww - 1e-9:
            iyi += 1
        elif wh > ww + 1e-9:
            kotu += 1
        else:
            esit += 1
    L = []
    P = L.append
    n = len(res["hmm"])
    P(f"ASR SONDAJI (koşu içi sözcük sınırı; n={n} sınır, her biri 2 parça × 2 sözcük):")
    if n:
        for ad in ("hmm", "agirlik"):
            a = np.array(res[ad])
            P(f"  {ad:8s}: ortalama WER {a.mean():.3f} · tam doğru (iki parça da WER=0) {int((a == 0).sum())}/{n} (%{100 * (a == 0).mean():.0f})")
        P(f"  eşli karşılaştırma: HMM daha iyi {iyi}, daha kötü {kotu}, eşit {esit}")
    txt = "\n".join(L)
    print(txt)
    open(os.path.join(OUT, "hizala_asr_sondaj.txt"), "w", encoding="utf-8").write(txt + "\n")
    return res


# ════════════════════════════════════════════════════════════ akustik zorlamalı hizalama (kendi verisinden eğitilen monofon HMM)
# Türkçe yazım ≈ sesbilgisi: her harf bir birim (3 durumlu, tek Gauss/durum, 39 boyutlu MFCC+Δ+ΔΔ). Model, ASR ile doğrulanmış koşu↔jeton
# eşlemeleriyle (≈15–20 dk, tek konuşmacı) sabit başlangıçtan Viterbi (sert EM) ile eğitilir; sonra her koşu bilinen metniyle zorlamalı hizalanır.
FS = 16000
HOP_N, WIN_N, NFFT, NFILT, NCEP = 160, 400, 512, 26, 12
TR_FON = list("abcçdefgğhıijklmnoöprsştuüvyz")
FON_ID = {p: i for i, p in enumerate(TR_FON)}
NSD = 3                                   # fon başına durum
SIL = len(TR_FON)                         # sil / sp: tek durumlu isteğe bağlı birimler
SP = SIL + 1
N_STATES = len(TR_FON) * NSD + 2
HMM_PAD = 0.03                            # özellik penceresi payı (sn): sil durumunun kareleri olsun


def _mel_fb(nfilt=NFILT, nfft=NFFT, fs=FS, lo=60.0, hi=7600.0):
    def hz2mel(f):
        return 2595 * np.log10(1 + f / 700.0)

    def mel2hz(m):
        return 700 * (10 ** (m / 2595.0) - 1)
    pts = mel2hz(np.linspace(hz2mel(lo), hz2mel(hi), nfilt + 2))
    bins = np.floor((nfft + 1) * pts / fs).astype(int)
    fb = np.zeros((nfilt, nfft // 2 + 1))
    for m in range(1, nfilt + 1):
        l, c, r = bins[m - 1], bins[m], bins[m + 1]
        for k in range(l, c):
            fb[m - 1, k] = (k - l) / max(1, c - l)
        for k in range(c, r):
            fb[m - 1, k] = (r - k) / max(1, r - c)
    return fb


_FB = _mel_fb()
_HAMM = np.hamming(WIN_N)


def _delta(f, N=2):
    T = len(f)
    pad = np.pad(f, ((N, N), (0, 0)), mode="edge")
    den = 2 * sum(i * i for i in range(1, N + 1))
    d = np.zeros_like(f)
    for i in range(1, N + 1):
        d += i * (pad[N + i: N + i + T] - pad[N - i: N - i + T])
    return d / den


def ozellik(x, sr):
    """x (mono, sr) → (T, 39) MFCC(12)+log-enerji+Δ+ΔΔ. Kare t, [10t, 10t+25) ms aralığını kaplar (sınır t ≈ 10t+7,5 ms)."""
    from scipy.signal import resample_poly
    from scipy.fft import dct
    y = resample_poly(x, FS, sr) if sr != FS else np.asarray(x, dtype=np.float64)
    if len(y) < WIN_N + 2 * HOP_N:
        return np.zeros((0, 39))
    y = np.append(y[0], y[1:] - 0.97 * y[:-1])
    n = 1 + (len(y) - WIN_N) // HOP_N
    idx = np.arange(n)[:, None] * HOP_N + np.arange(WIN_N)[None, :]
    P = np.abs(np.fft.rfft(y[idx] * _HAMM[None, :], NFFT, axis=1)) ** 2
    mel = np.log(P @ _FB.T + 1e-8)
    c = dct(mel, type=2, axis=1, norm="ortho")[:, 1:NCEP + 1]
    e = np.log(P.sum(axis=1) + 1e-8)[:, None]
    f = np.hstack([c, e])
    return np.hstack([f, _delta(f), _delta(_delta(f))])


def fonlar(word):
    w = word.translate(_KUCUK).lower().replace("i̇", "i")
    w = w.replace("â", "a").replace("î", "i").replace("û", "u").replace("w", "v").replace("q", "k").replace("x", "ks")
    return [FON_ID[ch] for ch in w if ch in FON_ID]


def _sid(unit, k):
    return len(TR_FON) * NSD + (unit - SIL) if unit >= SIL else unit * NSD + k


class AkustikModel:
    def __init__(self, dim=39):
        self.mu = np.zeros((N_STATES, dim))
        self.var = np.ones((N_STATES, dim))
        self.nmu = np.zeros(dim)
        self.nsd = np.ones(dim)
        self.lp_stay, self.lp_adv = np.log(0.6), np.log(0.4)
        self.ls_stay, self.ls_leave = np.log(0.8), np.log(0.2)

    def loglik(self, X, sids):
        mu, iv = self.mu[sids], 1.0 / self.var[sids]
        const = -0.5 * (np.log(2 * np.pi * self.var[sids]).sum(axis=1) + (mu * mu * iv).sum(axis=1))
        return -0.5 * (X * X) @ iv.T + X @ (mu * iv).T + const[None, :]


ATLA_CEZA = 150.0                         # sözcük atlama cezası (nat): TTS'in söylemediği sözcüğü kabul edilebilir kılar


def zincir(sozcuk_fonlari, ilk_sil=True, son_sil=True, sp_arasi=True):
    """[sil] w1 [sp] w2 … wn [sil]; sil/sp isteğe bağlı. → sids, isteğe_bağlı, sözcük_indisi, birim, yaylar
    yaylar: (kaynak_durum, hedef_durum, sözcük) — sözcüğün tamamını atlayan geçişler (kaynak: sözcükten önceki durum, hedef: sonraki durum)."""
    sids, opt, wof, uof = [], [], [], []
    first, last = {}, {}

    def ekle(unit, k, o, w):
        sids.append(_sid(unit, k)); opt.append(o); wof.append(w); uof.append(unit)
        if w >= 0:
            first.setdefault(w, len(sids) - 1)
            last[w] = len(sids) - 1
    if ilk_sil:
        ekle(SIL, 0, True, -1)
    for wi, ph in enumerate(sozcuk_fonlari):
        for p in ph:
            for k in range(NSD):
                ekle(p, k, False, wi)
        if sp_arasi and wi < len(sozcuk_fonlari) - 1:
            ekle(SP, 0, True, -1)
    if son_sil:
        ekle(SIL, 0, True, -1)
    S = len(sids)
    yaylar = []
    for w in range(len(sozcuk_fonlari)):
        if w in first and first[w] - 1 >= 0 and last[w] + 1 < S:
            yaylar.append((first[w] - 1, last[w] + 1, w))
    return np.array(sids), np.array(opt), np.array(wof), np.array(uof), yaylar


def viterbi(model, X, sids, opt, uof, yaylar=None, ceza=None):
    """Doğrusal zincirde zorlamalı Viterbi (kendine, sonrakine, isteğe bağlı durumu atlayarak iki sonrakine; yaylar verilirse ceza karşılığında
    bütün bir sözcüğü atlayarak). → (yol (T,), log-olasılık)"""
    T, S = len(X), len(sids)
    ceza = ATLA_CEZA if ceza is None else ceza
    L = model.loglik(X, sids)
    NEG = -1e30
    stay = np.where(uof >= SIL, model.ls_stay, model.lp_stay)
    adv = np.where(uof >= SIL, model.ls_leave, model.lp_adv)
    d = np.full(S, NEG)
    bp = np.zeros((T, S), dtype=np.int8)
    d[0] = L[0, 0]
    j = 0
    while j + 1 < S and opt[j]:
        j += 1
        d[j] = L[0, j]
    ar = np.arange(S)
    if yaylar:
        src = np.array([y[0] for y in yaylar])
        dst = np.array([y[1] for y in yaylar])
        bps = np.zeros((T, S), dtype=np.int16)
    for t in range(1, T):
        c0 = d + stay
        c1 = np.concatenate([[NEG], d[:-1] + adv[:-1]])
        c2 = np.full(S, NEG)
        if S > 2:
            c2[2:] = np.where(opt[1:-1], d[:-2] + adv[:-2], NEG)
        st = np.vstack([c0, c1, c2])
        a = st.argmax(axis=0)
        best = st[a, ar]
        if yaylar:
            cand = d[src] + adv[src] - ceza
            iyi = cand > best[dst]
            if iyi.any():
                di = dst[iyi]
                best[di] = cand[iyi]
                a[di] = 3
                bps[t, di] = src[iyi]
        bp[t] = a
        d = best + L[t]
    ends = [S - 1]
    j = S - 1
    while j - 1 >= 0 and opt[j]:
        j -= 1
        ends.append(j)
    e = max(ends, key=lambda s: d[s])
    path = np.zeros(T, dtype=int)
    s = e
    for t in range(T - 1, -1, -1):
        path[t] = s
        if t == 0:
            break
        a = bp[t, s]
        if a == 1:
            s -= 1
        elif a == 2:
            s -= 2
        elif a == 3:
            s = int(bps[t, s])
    return path, float(d[e])


def akustik_egit(utts, n_iter=8, verbose=True, atla_tur=2):
    """utts: [(X (T,D) normalize, sözcük_fonları, pad_sol_kare, pad_sağ_kare)] → AkustikModel.
    Son atla_tur yinelemede sözcük atlama yayları açılır (TTS'in söylemediği sözcükler istatistiği bozmasın)."""
    dim = utts[0][0].shape[1]
    model = AkustikModel(dim)
    chains = [zincir(tp) for _, tp, _, _ in utts]
    allX = np.vstack([u[0] for u in utts])
    gmu, gvar = allX.mean(axis=0), allX.var(axis=0)
    sx = np.zeros((N_STATES, dim)); sxx = np.zeros((N_STATES, dim)); cnt = np.zeros(N_STATES)

    def topla(sids, path, X):
        np.add.at(sx, sids[path], X)
        np.add.at(sxx, sids[path], X * X)
        np.add.at(cnt, sids[path], 1)

    for (X, tp, pl, pr), (sids, opt, wof, uof, yay) in zip(utts, chains):
        T = len(X)
        non = [i for i in range(len(sids)) if not opt[i]]
        k = len(non)
        path = np.zeros(T, dtype=int)
        core = np.arange(pl, T - pr) if T - pr > pl else np.arange(T)
        idx = np.array(non)
        path[core] = idx[np.minimum(((core - core[0]) * k) // max(len(core), 1), k - 1)]
        path[:pl] = 0 if opt[0] else idx[0]
        path[T - pr:] = len(sids) - 1 if opt[-1] else idx[-1]
        topla(sids, path, X)

    def guncelle():
        for s in range(N_STATES):
            if cnt[s] >= 5:
                mu = sx[s] / cnt[s]
                model.mu[s] = mu
                model.var[s] = np.maximum(sxx[s] / cnt[s] - mu * mu, 0.05 * gvar)
            else:
                model.mu[s], model.var[s] = gmu, gvar
        sp_id = _sid(SP, 0)
        if cnt[sp_id] < 5:                                           # sp henüz görülmediyse sil gibi başla
            model.mu[sp_id], model.var[sp_id] = model.mu[_sid(SIL, 0)], model.var[_sid(SIL, 0)]
    guncelle()
    for it in range(n_iter):
        sx[:] = 0; sxx[:] = 0; cnt[:] = 0
        tot, nfr = 0.0, 0
        for (X, tp, pl, pr), (sids, opt, wof, uof, yay) in zip(utts, chains):
            path, ll = viterbi(model, X, sids, opt, uof, yay if it >= n_iter - atla_tur else None)
            tot += ll; nfr += len(X)
            topla(sids, path, X)
        guncelle()
        if verbose:
            log(f"    HMM eğitim {it + 1}/{n_iter}: kare başına log-olasılık {tot / nfr:.3f}")
    return model


def akustik_hizala(model, X, sozcuk_fonlari, ilk_sil=True, son_sil=True, sp_arasi=True, atla=False):
    """→ ([(başlangıç_kare, bitiş_kare_hariç)] sözcük başına (atlanan sözcük: (None, None)), kare başına log-olasılık)"""
    sids, opt, wof, uof, yay = zincir(sozcuk_fonlari, ilk_sil, son_sil, sp_arasi)
    path, ll = viterbi(model, X, sids, opt, uof, yay if atla else None)
    nw = len(sozcuk_fonlari)
    st, en = [None] * nw, [None] * nw
    for t, s in enumerate(path):
        w = wof[s]
        if w >= 0:
            if st[w] is None:
                st[w] = t
            en[w] = t + 1
    return list(zip(st, en)), ll / max(1, len(X))


def _kosu_ozellik(sn, B, sr, r):
    """Koşu penceresi [a−pay, b+pay] özellikleri (bölüme göre). → (X, pencere_başı, pad_sol_kare, pad_sağ_kare)"""
    seg = B["seg"]
    T = len(seg) / sr
    pl = min(HMM_PAD, max(0.0, (r["pre"] if r["pre"] is not None else 9.0) / 2))
    pr = min(HMM_PAD, max(0.0, (r["post"] if r["post"] is not None else 9.0) / 2))
    a = max(0.0, r["a"] - pl)
    b = min(T, r["b"] + pr)
    X = ozellik(seg[int(round(a * sr)): int(round(b * sr))], sr)
    return X, a, int(round((r["a"] - a) / HOP)), int(round((b - r["b"]) / HOP))


def hmm_hazirla(ctx):
    """Tüm koşuların özellikleri (HMM eğitimi/hizalaması için). → (ham liste, nmu, nsd)"""
    sr = ctx["sr"]
    bolmap = {B["c"]["id"]: B for B in ctx["bol"]}
    ham = []
    for sn in ctx["sonuclar"]:
        B = bolmap[sn["id"]]
        for r in sn["runs"]:
            if r["tok1"] <= r["tok0"]:
                continue
            X, a, pl, pr = _kosu_ozellik(sn, B, sr, r)
            if len(X) < 8:
                continue
            ph = [fonlar(sn["toks"][k]["w"]) for k in range(r["tok0"], r["tok1"])]
            if not all(ph):
                continue
            ev = sn["ev"][r["i"]]
            guvenli = ev is not None and ev["n_match"] >= 0.5 * (r["tok1"] - r["tok0"])
            ham.append(dict(sn=sn, r=r, X=X, a=a, pl=pl, pr=pr, ph=ph, guvenli=guvenli))
    if not ham:
        return [], None, None
    allX = np.vstack([h["X"] for h in ham])
    nmu, nsd = allX.mean(axis=0), allX.std(axis=0) + 1e-6
    for h in ham:
        h["Xn"] = (h["X"] - nmu) / nsd
    return ham, nmu, nsd


def akustik_ll(model, Xn, ph, atla=True):
    """Bir koşunun, verilen sözcük dizisiyle zorlamalı hizalamasının TOPLAM log-olasılığı (boş dizi: yalnız sessizlik).
    atla=True: söylenmeyen sözcük (ATLA_CEZA nat karşılığında) atlanabilir."""
    sids, opt, wof, uof, yay = zincir(ph, True, True, True)
    return viterbi(model, Xn, sids, opt, uof, yay if atla else None)[1]


def _kosu_fon(sn, r):
    return [fonlar(sn["toks"][k]["w"]) for k in range(r["tok0"], r["tok1"])]


def sinir_duzelt(ctx, model, ham_idx, esik=20.0, aday_yaricap=4):
    """ASR kanıtının belirlemediği (komşu kanıtlar arasında serbest) koşu sınırlarında jeton ataması, akustik olabilirliğe göre seçilir:
    skor(b) = LL(koşu r−1, jetonlar [B[r−1], b)) + LL(koşu r, jetonlar [b, B[r+1])). DP'nin seçimine göre ≥ eşik nat daha iyiyse değiştirilir.
    Ayrıca TÜM sınırlar için ±1 jeton kaydırma taraması yapılır (kanıtlı sınırlar değiştirilmez, yalnız raporlanır). → (değişen, şüpheli)"""
    degisen, suphe = [], []
    for sn in ctx["sonuclar"]:
        runs, Bn = sn["runs"], sn["B"]
        low, high = sn["atama"]["lowB"], sn["atama"]["highB"]
        for sweep in range(2):
            ch = False
            for r in range(1, len(runs)):
                ha, hb = ham_idx.get((sn["id"], r - 1)), ham_idx.get((sn["id"], r))
                if ha is None or hb is None:
                    continue
                lo = max(low[r], Bn[r - 1])
                hi = min(high[r], Bn[r + 1])
                if hi <= lo:
                    continue
                cur = Bn[r]
                cands = [b for b in range(max(lo, cur - aday_yaricap), min(hi, cur + aday_yaricap) + 1)]
                if len(cands) < 2:
                    continue
                sk = {}
                for b in cands:
                    pa = [fonlar(sn["toks"][k]["w"]) for k in range(Bn[r - 1], b)]
                    pb = [fonlar(sn["toks"][k]["w"]) for k in range(b, Bn[r + 1])]
                    if (pa and not all(pa)) or (pb and not all(pb)):
                        continue
                    sk[b] = akustik_ll(model, ha["Xn"], pa) + akustik_ll(model, hb["Xn"], pb)
                if cur not in sk:
                    continue
                best = max(sk, key=sk.get)
                if best != cur and sk[best] - sk[cur] >= esik:
                    degisen.append((sn["id"], round(sn["t0"] + runs[r]["a"], 2), cur, best, round(sk[best] - sk[cur], 1),
                                    runs[r - 1].get("asr_text"), runs[r].get("asr_text")))
                    Bn[r] = best
                    ch = True
            if not ch:
                break
        for r in range(len(runs)):
            runs[r]["tok0"], runs[r]["tok1"] = Bn[r], Bn[r + 1]
        # ±1 kaydırma taraması (bütün sınırlar; yalnız rapor)
        for r in range(1, len(runs)):
            ha, hb = ham_idx.get((sn["id"], r - 1)), ham_idx.get((sn["id"], r))
            if ha is None or hb is None:
                continue
            cur = Bn[r]
            vals = {}
            for b in (cur - 1, cur, cur + 1):
                if b < Bn[r - 1] or b > Bn[r + 1]:
                    continue
                pa = [fonlar(sn["toks"][k]["w"]) for k in range(Bn[r - 1], b)]
                pb = [fonlar(sn["toks"][k]["w"]) for k in range(b, Bn[r + 1])]
                if (pa and not all(pa)) or (pb and not all(pb)):
                    continue
                vals[b] = akustik_ll(model, ha["Xn"], pa) + akustik_ll(model, hb["Xn"], pb)
            if cur in vals:
                for b in (cur - 1, cur + 1):
                    if b in vals and vals[b] - vals[cur] >= 20.0:
                        suphe.append(dict(ch=sn["id"], t=round(sn["t0"] + runs[r]["a"], 2), sinir=cur, alt=b, kazanc=round(vals[b] - vals[cur], 1),
                                          onceki=runs[r - 1].get("asr_text"), sonraki=runs[r].get("asr_text"),
                                          kanitli=bool(low[r] >= high[r])))
    return degisen, suphe


def eksik_yerlestir(sn):
    """Seste bulunmayan (atlanan) sözcüklerin yer tutucuları: AYNI CÜMLEDEKİ sonraki konuşulan sözcüğün başına (yoksa öncekinin sonuna) 1 ms.
    Böylece cümle başı/sonu yalnızca gerçekten söylenen sözcüklerle belirlenir (atlanan sözcük komşu cümlenin koşusuna düşmüş olsa bile)."""
    toks, tm = sn["toks"], sn["tm"]
    miss = {e["tok"] for e in sn.get("eksik", [])}
    if not miss:
        return
    by = {}
    for k, t in enumerate(toks):
        by.setdefault(t["si"], []).append(k)
    for e in sn["eksik"]:
        k = e["tok"]
        idx = by[toks[k]["si"]]
        nxt = next((q for q in idx if q > k and q not in miss), None)
        prv = next((q for q in reversed(idx) if q < k and q not in miss), None)
        if nxt is not None:
            grup = [q for q in idx if k <= q < nxt]
            geri = len(grup) - 1 - grup.index(k)
            te = tm[nxt][0] - 0.001 * geri
            tm[k] = (te - 0.001, te)
        elif prv is not None:
            grup = [q for q in idx if prv < q <= k]
            ileri = grup.index(k)
            ts = tm[prv][1] + 0.001 * ileri
            tm[k] = (ts, ts + 0.001)
        e["t"] = round(sn["t0"] + tm[k][0], 3)


def akustik_iyilestir(S, ctx, n_iter=8):
    """Tüm bölümlerin koşuları ile HMM'i eğit; ASR kanıtının belirlemediği sınır jetonlarını akustik olabilirlikle düzelt; sonra her koşunun
    sözcük zamanlarını zorlamalı hizalamayla yeniden hesapla. Güvenilmeyen koşular (log-olasılık aykırı / sözcük çok kısa) ağırlık modeline
    geri düşer. sonuç['tm'] yerinde güncellenir."""
    ham, nmu, nsd = hmm_hazirla(ctx)
    if len(ham) < 30:
        log("[HMM] eğitim için yeterli koşu yok; ağırlık modeli kullanılıyor")
        return None
    egit = [h for h in ham if h["guvenli"]]
    ham_idx = {(h["sn"]["id"], h["r"]["i"]): h for h in ham}
    tum_degisen = []
    for tur in range(3):                                               # eğit → sınır jetonlarını düzelt → (değiştiyse) yeniden eğit
        log(f"[HMM] tur {tur + 1}: {len(ham)} koşu özelliği; {len(egit)} güvenilir koşu ile eğitiliyor ({sum(len(h['Xn']) for h in egit) * HOP:.0f} sn)")
        t = time.time()
        model = akustik_egit([(h["Xn"], h["ph"], h["pl"], h["pr"]) for h in egit], n_iter=n_iter, verbose=(tur == 0))
        model.nmu, model.nsd = nmu, nsd
        log(f"[HMM] eğitim {time.time() - t:.0f} sn")
        t = time.time()
        degisen, suphe = sinir_duzelt(ctx, model, ham_idx)
        log(f"[HMM] sınır jetonu düzeltmesi: {len(degisen)} sınır akustik olabilirliğe göre değişti; ±1 kaydırma taramasında şüpheli sınır: {len(suphe)} ({time.time() - t:.0f} sn)")
        for d in degisen:
            log(f"    düzeltme {d[0]} t={d[1]}: sınır {d[2]}→{d[3]} (+{d[4]} nat) | ASR önceki: {d[5]!r} sonraki: {d[6]!r}")
        for q in suphe:
            log(f"    ŞÜPHELİ sınır (kanıtlı) {q['ch']} t={q['t']}: {q['sinir']}→{q['alt']} olsaydı +{q['kazanc']} nat | ASR önceki: {q['onceki']!r} sonraki: {q['sonraki']!r}")
        tum_degisen += degisen
        for h in ham:                                                  # değişen koşuların fonları
            h["ph"] = _kosu_fon(h["sn"], h["r"])
        if not degisen:
            break
    degisen = tum_degisen
    lls = []
    for h in ham:
        w, ll = akustik_hizala(model, h["Xn"], h["ph"], atla=True)
        h["w"], h["ll"] = w, ll
        lls.append(ll)
    lls = np.array(lls)
    med = float(np.median(lls))
    mad = float(1.4826 * np.median(np.abs(lls - med)) + 1e-6)
    n_geri = 0
    for sn in ctx["sonuclar"]:                                         # ağırlık tabanlı zamanları yeni sınırlarla yenile
        sn["eksik"] = []
        for r in sn["runs"]:
            for k, (s_, e_) in zip(range(r["tok0"], r["tok1"]), koşu_ici_zamanlar(sn["toks"], r["tok0"], r["tok1"], r["a"], r["b"], sn["model"])):
                sn["tm"][k] = (s_, e_)
    for h in ham:
        r, sn = h["r"], h["sn"]
        w = h["w"]
        z = (h["ll"] - med) / mad
        n = len(w)
        konus = [k for k in range(n) if w[k][0] is not None]
        kisa = any(w[k][1] - w[k][0] < 3 for k in konus)
        r["hmm_ll"] = h["ll"]
        r["hmm_z"] = float(z)
        if z < -4.0 or kisa or not konus:
            r["hmm_durum"] = "geri"
            n_geri += 1
            continue
        t0w = h["a"]
        tt = [None] * n
        for k in konus:
            tt[k] = [t0w + w[k][0] * HOP + 0.0075, t0w + w[k][1] * HOP + 0.0075]
        # koşu kenarları VAD'a yaslanır (HMM ilk/son fonu belirgin geç/erken başlıyorsa — nefes/uzun yumuşak başlangıç — HMM'e uy)
        if tt[konus[0]][0] - r["a"] <= 0.10:
            tt[konus[0]][0] = r["a"]
        if r["b"] - tt[konus[-1]][1] <= 0.10:
            tt[konus[-1]][1] = r["b"]
        # sözcükler arası kısa boşluklar: <50 ms ise ortadan böl; daha uzunsa gerçek durak olarak bırak
        for a_, b_ in zip(konus[:-1], konus[1:]):
            if b_ == a_ + 1 and tt[b_][0] - tt[a_][1] < 0.05:
                mid = 0.5 * (tt[a_][1] + tt[b_][0])
                tt[a_][1] = tt[b_][0] = mid
        for k in konus:
            tt[k][0] = max(r["a"], min(tt[k][0], r["b"]))
            tt[k][1] = max(tt[k][0] + 0.02, min(tt[k][1], r["b"] + 0.02))
        # söylenmemiş (atlanan) sözcükler: sonraki konuşulan sözcüğün başına 1 ms'lik yer tutucu (yoksa önceki sözcüğün sonuna)
        eks = [k for k in range(n) if tt[k] is None]
        for k in sorted(eks, reverse=True):
            nxt = next((q for q in range(k + 1, n) if tt[q] is not None), None)
            if nxt is not None:
                tt[k] = [tt[nxt][0] - 0.001, tt[nxt][0]]
                tt[nxt] = tt[nxt]
            else:
                prv = max(q for q in range(k) if tt[q] is not None)
                tt[k] = [tt[prv][1], tt[prv][1] + 0.001]
        # yer tutucuların birbiriyle ve komşuyla çakışmaması: ardışık atlananlar sırayla 1 ms
        for k in eks:
            sn["eksik"].append(dict(tok=r["tok0"] + k, kelime=sn["toks"][r["tok0"] + k]["w"], t=round(sn["t0"] + tt[k][0], 2),
                                    onceki=" ".join(t["w"] for t in sn["toks"][max(r["tok0"], r["tok0"] + k - 2): r["tok0"] + k]),
                                    sonraki=" ".join(t["w"] for t in sn["toks"][r["tok0"] + k + 1: r["tok0"] + k + 3]), asr=r.get("asr_text")))
        for k, (s_, e_) in zip(range(r["tok0"], r["tok1"]), tt):
            sn["tm"][k] = (float(s_), float(e_))
        r["hmm_durum"] = "tamam"
    for sn in ctx["sonuclar"]:
        eksik_yerlestir(sn)
    n_eks = sum(len(sn.get("eksik", [])) for sn in ctx["sonuclar"])
    log(f"[HMM] hizalama: {len(ham) - n_geri}/{len(ham)} koşu HMM ile; ağırlık modeline geri düşen: {n_geri}; kare başına log-olasılık medyan {med:.2f} (MAD {mad:.2f}); "
        f"seste bulunmayan (atlanan) sözcük: {n_eks}")
    for sn in ctx["sonuclar"]:
        for e in sn.get("eksik", []):
            log(f"    SESTE YOK? {sn['id']} t≈{e['t']}: «{e['kelime']}» (önceki: {e['onceki']!r} sonraki: {e['sonraki']!r}) ASR: {e['asr']!r}")
    return dict(model=model, n_geri=n_geri, n=len(ham), ll_med=med, ll_mad=mad, degisen=degisen, suphe=suphe)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yalniz-asr", action="store_true", help="yalnız ASR önbelleğini doldur")
    ap.add_argument("--asr-yok", action="store_true", help="ASR çalıştırma; yalnız önbellek")
    ap.add_argument("--isci", type=int, default=2, help="ASR süreç sayısı (her biri 1 iş parçacığı; toplam ≤2)")
    ap.add_argument("--bolum", default=None, help="bölüm seçimi (örn. c2 ya da c0,c1); ana dosyalara dokunmaz, *_c2.* yazar")
    ap.add_argument("--ham-konusma", action="store_true", help="scribe_words.json'a saf söylenen sözcükleri yaz (rakamlı jetonları birleştirme)")
    ap.add_argument("--agirlik", action="store_true", help="akustik HMM'i kapat; yalnız hece-ağırlığı ile koşu içi dağıtım")
    ap.add_argument("--hmm-iter", type=int, default=8, help="HMM eğitim yinelemesi")
    ap.add_argument("--timeline", action="store_true", help="bitince ses_hizala.py'yi çalıştır (out_pN/timeline.json üretir)")
    ap.add_argument("--dogrula", action="store_true", help="bağımsız doğrulama: timeline cümle pencerelerini ASR ile yeniden yazdır")
    ap.add_argument("--karsilastir", action="store_true", help="eski (timeline_yerel_eski.json) ↔ yeni timeline farkları")
    ap.add_argument("--loo", action="store_true", help="koşu içi zamanlama doğruluğu: her duraktan bir bırak testi")
    ap.add_argument("--sondaj", action="store_true", help="koşu içi sözcük sınırı: akustik HMM ↔ hece-ağırlığı, bağımsız ASR sondajı")
    ap.add_argument("--kirp", type=float, default=0.03, help="--loo: birleştirme kenarlarından kırpılan süre (sn)")
    ap.add_argument("--n", type=int, default=40, help="--dogrula: rastgele cümle sayısı")
    ap.add_argument("--tohum", type=int, default=7)
    args = ap.parse_args()
    if args.dogrula:
        return dogrula(args)
    if args.karsilastir:
        return karsilastir(args)
    if args.loo:
        return loo_testi(args)
    if args.sondaj:
        return sondaj(args)
    ana_hizala(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""KREDİSİZ, ASR-destekli sözcük hizalayıcı (ElevenLabs Scribe yerine; ses_hizala_yerel.py'nin yerini alır).

  MEDICI_PART=1 python3 ses_hizala_asr.py                 # koşular → ASR (önbellekli) → hizalama → out_p1/scribe_words.json
  MEDICI_PART=1 python3 ses_hizala.py                     # (mevcut, değişmedi) → out_p1/timeline.json
  MEDICI_PART=1 python3 ses_hizala_asr.py --dogrula       # bağımsız doğrulama (cümle pencerelerini yeniden yazdırır) + rapor
  MEDICI_PART=1 python3 ses_hizala_asr.py --karsilastir   # eski (timeline_yerel_eski.json) ↔ yeni timeline.json farkları
  Seçenekler: --asr-yok (yalnız önbellek) · --yalniz-asr (sadece önbelleği doldur) · --isci N (ASR süreç sayısı; her biri 1 iş
  parçacığı, toplam ≤2) · --bolum c2 (tek bölüm) · --ham-konusma (rakamlı jetonları birleştirmeden, saf söylenen sözcükler)

Yöntem (ayrıntı: notlar_hizalama.md):
 1. Her bölümün sesi 250 Hz üstü süzülmüş 10 ms RMS ile "konuşma koşuları"na bölünür (durak ≥ 0,12 sn; gürültü kırıntıları atılır,
    sözcük içi kapanma parçaları komşuya katılır, 14 sn'den uzun koşu en düşük enerjiden bölünür).
 2. Her koşu (±0,12 sn paylı) Whisper medium (sherpa-onnx, çevrimdışı) ile yazıya dökülür; sonuçlar out_pN/asr_cache.json'da önbelleklenir
    (anahtar bölüm+başlangıç/bitiş, ses CRC'siyle doğrulanır).
 3. Bölümün tüm ASR sözcükleri, senaryo jetonlarıyla (S._speech_of; Türkçe harf katlama + bulanık benzerlik + 1↔2 birleştirme)
    monoton Needleman–Wunsch ile eşlenir.
 4. Eşleşmeler her koşunun senaryo-jeton aralığını belirler; koşular arası eşleşmeyen jetonlar (ve kanıtsız koşular) küçük bir DP ile
    (noktalama ↔ durak uyumu + konuşma hızı/süre uyumu) komşu koşulara dağıtılır.
 5. Koşu içinde sözcük zamanları, koşu verisinden uydurulmuş hece/harf ağırlıklarıyla dağıtılır; ilk sözcük koşu başına, son sözcük koşu
    sonuna yaslanır, koşular arası boşluk gerçek durak olarak kalır.
 6. Çıktı out_pN/scribe_words.json (ses_hizala_yerel.py ile aynı biçim: [{text,start,end,type:"word"}], bölümler art arda, mutlak sn).
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
    thr = p95 - DURAK_ESIK_DB
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
                v = D[i - 2][j - 1] + birlesik_puani(ref[i - 2] + ri, hyp[j - 1])
                if v > best:
                    best, op = v, 3
            if j >= 2:
                v = Dp[j - 2] + birlesik_puani(hyp[j - 2] + hyp[j - 1], ri)
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
    return B, dict(celiski=celiski, maliyet=dp[R].get(N))


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
    """Koşular + ASR (önbellekli) + hizalama, tüm (ya da seçilen) bölümler. → ctx"""
    secim = {args.bolum} if args.bolum else None
    x, sr, vc, wav_path, bol = bolumleri_hazirla(secim)
    isler = asr_isleri(x, sr, bol)
    cache_path = os.path.join(OUT, ASR_ONBELLEK)
    if args.asr_yok:
        cache = cache_oku(cache_path)
        eksik = sum(1 for j in isler if not (j[0] in cache and cache[j[0]].get("crc") == j[3]))
        log(f"[ASR] önbellekten okunuyor; ASR'siz koşu: {eksik}/{len(isler)}")
    else:
        cache = asr_calistir(_onsel(isler), cache_path, wav_path, isci=args.isci)
    ctx = dict(x=x, sr=sr, vc=vc, wav_path=wav_path, bol=bol, cache=cache, sonuclar=[], kelimeler=[], rapor=dict(bolumler={}, uyarilar=[]))
    if args.yalniz_asr:
        return ctx
    sents_all = S.sentences(PA.PART)
    rapor = ctx["rapor"]
    cum_rapor = {}
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
        sents = [s for s in sents_all if s["ch"] == cid]
        words, uyar = kelime_listesi(S, sn, sents, ham=args.ham_konusma)
        for u in uyar:
            rapor["uyarilar"].append(f"{cid} {u}")
            log("UYARI:", cid, u)
        ctx["sonuclar"].append(sn)
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
        rapor["bolumler"][cid] = dict(
            jeton=sn["n_tok"], jeton_eslesen=sn["n_esl"], jeton_oran=round(sn["n_esl"] / sn["n_tok"], 4),
            asr_sozcuk=sn["n_hyp"], asr_eslesen=sn["hyp_esl"], asr_oran=round(sn["hyp_esl"] / max(1, sn["n_hyp"]), 4),
            kosu=len(sn["runs"]), kanitli_kosu=n_ev, bos_kosu=n_bos_run, kanitsiz_kosu=len(sn["runs"]) - n_ev,
            model=dict(hece=round(sn["model"].a, 4), soz=round(sn["model"].b, 4), sabit=round(sn["model"].c, 4), sigma=round(sn["model"].sigma_abs, 3)),
            celiski=sn["atama"]["celiski"], aykiri_hiz=aykiri, eslesmeyen_bolgeler=bos, kosu_bilgi=B["info"])
        log(f"{cid:3s} jeton {sn['n_tok']:4d} eşleşen {sn['n_esl']:4d} (%{100 * sn['n_esl'] / sn['n_tok']:.1f}) | ASR sözcük {sn['n_hyp']:4d} eşleşen "
            f"{sn['hyp_esl']:4d} (%{100 * sn['hyp_esl'] / max(1, sn['n_hyp']):.1f}) | koşu {len(sn['runs']):3d} (kanıtlı {n_ev}, boş {n_bos_run}) | "
            f"hece/sn modeli a={sn['model'].a:.3f} b={sn['model'].b:.3f} c={sn['model'].c:.3f} | aykırı hız {len(aykiri)} | eşleşmeyen bölge(≥2) {len(bos)}")
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
    ek = f"_{args.bolum}" if args.bolum else ""                      # tek bölüm: ana dosyalara dokunma
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
    """Koşu içi zamanlama doğruluğu — 'duraktan bir bırak': ardışık iki koşuyu, aradaki durağı silerek tek koşu gibi birleştir;
    ağırlık modeli ile tahmin edilen iç sınırı gerçek (durak) konumla karşılaştır. Bu hata, koşu İÇİNDE kalan cümle/sözcük sınırlarının
    beklenen hatasıdır (koşu sonu uzaması nedeniyle biraz kötümser)."""
    S = senaryo_yukle()
    args.asr_yok = True
    ctx = hesapla_hepsi(args, S)
    E, kayit = [], []
    for sn in ctx["sonuclar"]:
        toks, runs, m = sn["toks"], sn["runs"], sn["model"]
        for r in range(len(runs) - 1):
            a, b = runs[r], runs[r + 1]
            a0, a1, b1 = a["tok0"], a["tok1"], b["tok1"]
            if a1 == a0 or b1 == a1 or a1 != b["tok0"]:
                continue
            W1 = sum(m.a * t["syl"] + m.b for t in toks[a0:a1])
            W2 = sum(m.a * t["syl"] + m.b for t in toks[a1:b1])
            pred = (a["dur"] + b["dur"]) * W1 / (W1 + W2)
            hata = pred - a["dur"]
            E.append(hata)
            kayit.append((sn["id"], a["dur"] + b["dur"], a["post"], toks[a1 - 1]["typ"]))
    e = np.array(E)
    ae = np.abs(e)
    L = []
    P = L.append
    P(f"DURAKTAN BİR BIRAK (n={len(e)} iç sınır; hece/sözcük ağırlık modeli):")
    q = _yuzdelik(ae)
    P(f"  |hata| medyan {q[50]:.3f}  %90 {q[90]:.3f}  %95 {q[95]:.3f}  %99 {q[99]:.3f}  azami {q[100]:.3f} sn · ort işaretli {e.mean():+.3f} · "
      f"≤0,1: %{100 * (ae <= 0.1).mean():.1f}  ≤0,2: %{100 * (ae <= 0.2).mean():.1f}  >0,3: {int((ae > 0.3).sum())}  >0,6: {int((ae > 0.6).sum())}")
    for ad, filt in (("cümle sonu (. ? ! paragraf)", lambda k: k[3] in (STRONG, PARA)), ("noktalamasız/virgül", lambda k: k[3] not in (STRONG, PARA))):
        kk = [i for i, k in enumerate(kayit) if filt(k)]
        if kk:
            q = _yuzdelik(ae[kk])
            P(f"  {ad:30s} n={len(kk):3d} medyan {q[50]:.3f} %95 {q[95]:.3f} azami {q[100]:.3f}")
    txt = "\n".join(L)
    print(txt)
    open(os.path.join(OUT, "hizala_asr_loo.txt"), "w", encoding="utf-8").write(txt + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yalniz-asr", action="store_true", help="yalnız ASR önbelleğini doldur")
    ap.add_argument("--asr-yok", action="store_true", help="ASR çalıştırma; yalnız önbellek")
    ap.add_argument("--isci", type=int, default=2, help="ASR süreç sayısı (her biri 1 iş parçacığı; toplam ≤2)")
    ap.add_argument("--bolum", default=None, help="tek bölüm (örn. c2)")
    ap.add_argument("--ham-konusma", action="store_true", help="scribe_words.json'a saf söylenen sözcükleri yaz (rakamlı jetonları birleştirme)")
    ap.add_argument("--timeline", action="store_true", help="bitince ses_hizala.py'yi çalıştır (out_pN/timeline.json üretir)")
    ap.add_argument("--dogrula", action="store_true", help="bağımsız doğrulama: timeline cümle pencerelerini ASR ile yeniden yazdır")
    ap.add_argument("--karsilastir", action="store_true", help="eski (timeline_yerel_eski.json) ↔ yeni timeline farkları")
    ap.add_argument("--loo", action="store_true", help="koşu içi zamanlama doğruluğu: her duraktan bir bırak testi")
    ap.add_argument("--n", type=int, default=40, help="--dogrula: rastgele cümle sayısı")
    ap.add_argument("--tohum", type=int, default=7)
    args = ap.parse_args()
    if args.dogrula:
        return dogrula(args)
    if args.karsilastir:
        return karsilastir(args)
    if args.loo:
        return loo_testi(args)
    ana_hizala(args)


if __name__ == "__main__":
    main()

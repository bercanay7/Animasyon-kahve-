#!/usr/bin/env python3
"""Bölüm düzeyinde cümle yaması (kurul tur 1, Parça 1): yeniden seslendirilen cümleleri HAM bölüm sesine yerleştirir.

  MEDICI_PART=1 python3 ses_yama_bolum.py [--dry]
  MEDICI_PART=1 python3 ses_birlestir.py c1=v2 c2=v2          # eşik/kazanç/tepe ölçeği v1'den sabitlenir
  MEDICI_PART=1 python3 ses_hizala_asr.py --timeline          # değişmeyen koşular ASR önbelleğinden CRC ile taşınır

Girdi : ses_ham/yama_p1/<cümle>.mp3 (ElevenLabs, yeni metin; KAYNAK.json),
        ses_ham/yama_p1/timeline_v1.json + voice_chapters_v1.json (YAMADAN ÖNCEKİ hizalama; ilk çalıştırmada out_p1'den dondurulur),
        ses_ham/<bölüm>_v1_48k.wav (ham bölüm sesi).
Çıktı : ses_ham/<bölüm>_v2_48k.wav, ses_ham/yama_p1/rapor.json.

Yöntem: eski cümlenin ses zamanı (timeline) → bölüm sıkıştırma haritasının (ses_birlestir.squeeze_gaps) tersi → ham zaman.
Ham seste cümlenin önündeki ve arkasındaki durak (10 ms enerji, v1 sessizlik eşiği, ≥ 150 ms) bulunur; konuşma
[baş − 50 ms, son + 50 ms] aralığı (10 ms ızgarasında), yeni klibin konuşma kısmıyla (aynı 50 ms paylar, eski cümlenin etkin
RMS'ine eşitlenmiş, uzunluğu 480 örneğin katı) değiştirilir. Böylece yamanın dışındaki her örnek ve 10 ms ızgarası v1 ile aynı
kalır: ses_birlestir çıktısında yama dışı bölgeler bit bit korunur, ASR önbelleği CRC ile yeniden kullanılır.
"""
import json
import os
import shutil
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("MEDICI_PART", "1")
_argv = sys.argv[:]
sys.argv = sys.argv[:1]                      # ses_birlestir argv'den sürüm okur; burada v1 kalmalı
import parca as PA  # noqa: E402
import ses_birlestir as B  # noqa: E402
sys.argv = _argv

SR = B.SR
HOP = int(0.01 * SR)                         # 480: sıkıştırma ızgarası
PAD = 5                                      # 50 ms (kare)
MIN_PAUSE = 15                               # cümle sınırı durağı ≥ 150 ms
SIL_REL_DB = -32                             # sınır araması için sessizlik: tepe (p95) − 32 dB (ElevenLabs gürültü tabanı ≈ −68 dB, v1 eşiği −67 dB'de titriyor)
YAMA = os.path.join(B.RAW, "yama_p1")
PATCHES = {"c1": ["c1s11", "c1s16", "c1s18", "c1s23", "c1s24", "c1s26"], "c2": ["c2s1", "c2s7", "c2s27"]}
# c1s26 ("Roma'da") ve c2s1 ("Çözüm,"): orijinal ElevenLabs kaydında ilk sözcük yutulmuştu (ASR + süre analizi, 4 Kasım);
# yeniden üretimde başa kesilecek bağlam kondu (<sid>_ham.mp3) ve kırpılmış klip <sid>.wav olarak kaydedildi (yerel ASR ile doğrulandı).


def frames_db(x):
    n = len(x) // HOP
    fr = x[: n * HOP].reshape(n, HOP)
    return 20 * np.log10(np.sqrt(np.mean(fr ** 2, axis=1) + 1e-12) + 1e-9)


def write_wav_exact(path, x):
    """B.load /32768 ile okur → tam ters çevir (yama dışı örnekler v1 ile bit bit aynı)."""
    q = np.clip(np.round(x * 32768), -32768, 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(q.tobytes())


def load_clip(mp3):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ar", str(SR), "-ac", "1", "-f", "s16le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, "<i2").astype(np.float64) / 32768


def inv_map(m, p):
    """çıkış örneği → ham örnek (sıkıştırma haritasının tersi; çapraz geçiş bindirmesinde sonraki parça)."""
    best = None
    for a, b, o in m:
        if o <= p < o + (b - a):
            best = a + (p - o)
    if best is None:
        raise ValueError(f"haritada yok: {p}")
    return best


def pause_before(sil, f, lo):
    """f karesinden geriye: ≥ MIN_PAUSE sessiz koşunun SONU (ilk konuşma karesi)."""
    i = f
    while i > lo:
        if sil[i - 1]:
            j = i - 1
            while j > lo and sil[j - 1]:
                j -= 1
            if i - j >= MIN_PAUSE or (j == 0 and lo == 0):      # bölüm başı: baştaki sessizlik kısa olabilir
                return i
            i = j
        else:
            i -= 1
    return None


def pause_after(sil, f, hi):
    """f karesinden ileri: ≥ MIN_PAUSE sessiz koşunun BAŞI (son konuşma karesi + 1)."""
    i = f
    while i < hi:
        if sil[i]:
            j = i
            while j < hi and sil[j]:
                j += 1
            if j - i >= MIN_PAUSE:
                return i
            i = j
        else:
            i += 1
    return None


def clip_speech(z):
    """klibin konuşma kısmı + 50 ms paylar; ızgaraya (480) hizalı uzunluk."""
    db = frames_db(z)
    thr = np.percentile(db, 95) + SIL_REL_DB
    act = db >= thr
    act = np.convolve(act.astype(int), np.ones(3, int), "same") >= 2      # tek karelik çıtırtıları yok say
    on = int(np.argmax(act))
    off = len(act) - int(np.argmax(act[::-1]))
    a = (on - PAD) * HOP
    b = (off + PAD) * HOP
    pre = max(0, -a)
    seg = z[max(0, a): min(len(z), b)]
    post = max(0, b - len(z))
    seg = np.concatenate([np.zeros(pre), seg, np.zeros(post)])
    return seg, on, off, thr


def main(dry=False):
    os.makedirs(YAMA, exist_ok=True)
    tl_path = os.path.join(YAMA, "timeline_v1.json")
    vc_path = os.path.join(YAMA, "voice_chapters_v1.json")
    if not os.path.exists(tl_path):
        shutil.copy(os.path.join(PA.OUT, "timeline.json"), tl_path)
        shutil.copy(os.path.join(PA.OUT, "voice_chapters.json"), vc_path)
        print("yama öncesi hizalama donduruldu:", tl_path)
    tl = json.load(open(tl_path, encoding="utf-8"))
    vc = {c["id"]: c for c in json.load(open(vc_path))["chapters"]}
    sent = {s["id"]: s for s in tl["sentences"]}
    rapor = {}
    for cid, sids in PATCHES.items():
        x = B.load(cid, "v1")
        y, saved, thr, m = B.squeeze_gaps(x, want_map=True)
        db = frames_db(x)
        sil = db < (np.percentile(db, 95) + SIL_REL_DB)
        nfr = len(sil)
        ch_t0 = vc[cid]["t0"]
        assert abs(len(y) / SR - vc[cid]["dur"]) < 0.02, f"{cid}: v1 sıkıştırma süresi hizalamayla uyuşmuyor"
        edits = []
        for sid in sids:
            s = sent[sid]
            ra = inv_map(m, int(round((s["t0"] - ch_t0) * SR)))
            rb = inv_map(m, min(len(y) - 1, int(round((s["t1"] - ch_t0) * SR))))
            fa, fb = ra // HOP, rb // HOP
            on = pause_before(sil, min(nfr, fa + 5), max(0, fa - 60))
            off = pause_after(sil, max(0, fb - 5), min(nfr, fb + 80))
            if on is None or off is None:
                raise SystemExit(f"{sid}: cümle sınırı durağı bulunamadı (fa={fa}, fb={fb})")
            d_on, d_off = (on - fa) * 0.01, (off - fb) * 0.01
            if abs(d_on) > 0.35 or abs(d_off) > 0.45:
                raise SystemExit(f"{sid}: sınır hizalamadan çok uzak (baş {d_on:+.2f} sn, son {d_off:+.2f} sn) — elle bakılmalı")
            cut_a, cut_b = max(0, on - PAD) * HOP, (off + PAD) * HOP
            wav = os.path.join(YAMA, f"{sid}.wav")
            z = load_clip(wav if os.path.exists(wav) else os.path.join(YAMA, f"{sid}.mp3"))
            seg, z_on, z_off, z_thr = clip_speech(z)
            old_sp = x[on * HOP: off * HOP]
            new_sp = seg[PAD * HOP: len(seg) - PAD * HOP]
            g = B.active_rms_db(old_sp) - B.active_rms_db(new_sp)
            seg = seg * (10 ** (g / 20))
            fade = int(0.01 * SR)
            seg[:fade] *= np.linspace(0, 1, fade)
            seg[-fade:] *= np.linspace(1, 0, fade)
            assert len(seg) % HOP == 0 and cut_a % HOP == 0 and cut_b % HOP == 0
            edits.append((cut_a, cut_b, seg))
            rapor[sid] = dict(bolum=cid, eski_ses_t0=s["t0"], eski_ses_t1=s["t1"], ham_bas=round(on * 0.01, 2), ham_son=round(off * 0.01, 2),
                              sinir_farki_bas=round(d_on, 2), sinir_farki_son=round(d_off, 2),
                              eski_konusma_sn=round((off - on) * 0.01, 2), yeni_konusma_sn=round(len(new_sp) / SR, 2),
                              fark_sn=round((len(seg) - (cut_b - cut_a)) / SR, 2), kazanc_db=round(g, 2),
                              yeni_tepe=round(float(np.max(np.abs(seg))), 3), eski_tepe=round(float(np.max(np.abs(old_sp))), 3))
            print(f"{sid}: ham {on * 0.01:7.2f}–{off * 0.01:7.2f} sn (sınır {d_on:+.2f}/{d_off:+.2f}) "
                  f"eski {rapor[sid]['eski_konusma_sn']:.2f} sn → yeni {rapor[sid]['yeni_konusma_sn']:.2f} sn, kazanç {g:+.1f} dB, "
                  f"tepe {rapor[sid]['eski_tepe']:.2f}→{rapor[sid]['yeni_tepe']:.2f}")
        edits.sort()
        parts, pos = [], 0
        for a, b, seg in edits:
            assert a >= pos, "yamalar çakışıyor"
            parts += [x[pos:a], seg]
            pos = b
        parts.append(x[pos:])
        x2 = np.concatenate(parts)
        print(f"{cid}: {len(x) / SR:.2f} → {len(x2) / SR:.2f} sn ({(len(x2) - len(x)) / SR:+.2f})")
        if not dry:
            write_wav_exact(os.path.join(B.RAW, f"{cid}_v2_48k.wav"), x2)
            chk = B.load(cid, "v2")
            a0 = edits[0][0]
            assert np.array_equal(chk[:a0], x[:a0]), "yama öncesi bölge v1 ile aynı değil"
            tail = len(x) - edits[-1][1]
            assert np.array_equal(chk[len(chk) - tail:], x[len(x) - tail:]), "yama sonrası bölge v1 ile aynı değil"
    if not dry:
        json.dump(rapor, open(os.path.join(YAMA, "rapor.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("yazıldı: ses_ham/c1_v2_48k.wav, c2_v2_48k.wav, yama_p1/rapor.json")


if __name__ == "__main__":
    main(dry="--dry" in sys.argv)

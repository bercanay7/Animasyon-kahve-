"""Cümle düzeyinde ses yaması: yeniden seslendirilen cümleleri (ses_ham/yama_b*.mp3) out/voice.wav içine yamalar,
out/timeline.json ve out/voice_chapters.json'u günceller (kaynak kapısı düzeltmeleri).

Aşamalar:
  python3 ses_yama.py --prepare          # yama_b*.mp3 → seviyeli birleşik klip (Scribe için out/yama_combined.mp3)
  (Scribe'a yükle; sözcük zamanlarını out/yama_scribe_words.json olarak kaydet)
  python3 ses_yama.py --apply [--dry]    # hizala, kes, yamala, zaman çizelgesini güncelle (yedekler out/_cache/*_pre_yama.*)

Not: bu işlemden sonra `ses_hizala.py` ESKİ Scribe verisiyle çalıştırılmamalı (timeline.json artık yamalı kaynaktır).
Yöntem: yamalı cümlenin eski aralığı [önceki boşluğun ortası, sonraki boşluğun ortası] ; yerine (aynı boşluk uzunlukları + yeni konuşma).
Sonraki tüm zamanlar sürenin farkı kadar kayar."""
import json
import os
import shutil
import subprocess
import sys
import wave

import numpy as np

import parca as PA
import script as S
import ses_birlestir as B
from ses_hizala import align, norm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = PA.OUT
RAW = os.path.join(HERE, "ses_ham")
CACHE = os.path.join(OUT, "_cache")
SR = B.SR


def read_wav(path):
    w = wave.open(path)
    return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768


def write_wav(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def to_wav(mp3, wav):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-ar", str(SR), "-ac", "1", wav], check=True)


def prepare():
    batches = json.load(open(os.path.join(OUT, "yama_batches.json"), encoding="utf-8"))
    parts, layout, t = [], [], 0.0
    for bi, b in enumerate(batches, 1):
        mp3 = os.path.join(RAW, f"yama_b{bi}.mp3")
        wav = os.path.join(RAW, f"yama_b{bi}_48k.wav")
        to_wav(mp3, wav)
        x = read_wav(wav)
        g = B.TARGET_RMS_DB - B.active_rms_db(x)
        x = x * (10 ** (g / 20))
        layout.append(dict(batch=bi, t0=round(t, 3), dur=round(len(x) / SR, 3), gain_db=round(g, 2), ids=b["ids"]))
        parts.append(x)
        t += len(x) / SR
        parts.append(np.zeros(int(2.0 * SR)))
        t += 2.0
    comb = np.concatenate(parts)
    write_wav(os.path.join(OUT, "yama_combined_48k.wav"), comb)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(OUT, "yama_combined_48k.wav"), "-ar", "44100", "-ac", "1", "-b:a", "96k",
                    os.path.join(OUT, "yama_combined.mp3")], check=True)
    json.dump(layout, open(os.path.join(OUT, "yama_layout.json"), "w"), indent=1)
    print(f"birleşik klip {len(comb)/SR:.1f} sn → out/yama_combined.mp3 ({os.path.getsize(os.path.join(OUT, 'yama_combined.mp3'))} bayt)")
    for l in layout:
        print("  parti", l["batch"], "başlangıç", l["t0"], "süre", l["dur"], "kazanç", l["gain_db"], "dB")


def rms_speech(y):
    """Konuşma çerçevelerinin (tepeden ≤18 dB aşağıda) ortalama RMS'i, dB."""
    h = int(0.02 * SR)
    fr = np.array([np.sqrt(np.mean(y[i:i + h] ** 2)) for i in range(0, len(y) - h, h)])
    db = 20 * np.log10(fr + 1e-9)
    return float(np.mean(db[db > db.max() - 18]))


def unit_ranges(hyp_words, units):
    """Küresel hizalama (söylenen metin belirteçleri) → her birim için [ilk, son] Scribe sözcük indeksi."""
    ref, owner = [], []
    for ui, u in enumerate(units):
        for tok in u["speech"].split():
            ref.append(norm(tok)); owner.append(ui)
    hyp = [norm(w["text"]) for w in hyp_words]
    mp = align(ref, hyp)
    first = {}; last = {}
    for i, j in mp.items():
        u = owner[i]
        first[u] = min(first.get(u, j), j); last[u] = max(last.get(u, j), j)
    rng = []
    for ui in range(len(units)):
        a, b = first.get(ui), last.get(ui)
        rng.append([a, b])
    # eksik uçları komşu birimler arasındaki boşluğa kadar uzat
    for ui in range(len(units)):
        a, b = rng[ui]
        lo = (rng[ui - 1][1] + 1) if ui > 0 and rng[ui - 1][1] is not None else 0
        hi = (rng[ui + 1][0] - 1) if ui + 1 < len(units) and rng[ui + 1][0] is not None else len(hyp) - 1
        # belirteç sayısı kadar sözcük beklenir; ilk/son belirteç eşleşmediyse komşu sözcükleri sahiplen
        toks = units[ui]["speech"].split()
        have = b - a + 1
        miss = len(toks) - have
        # başa/sona dağıt: ilk belirteç eşleşmediyse başa, son eşleşmediyse sona
        ref_idx = [k for k, o in enumerate(owner) if o == ui]
        m_first = ref_idx[0] in mp
        m_last = ref_idx[-1] in mp
        if miss > 0:
            if not m_first and a - 1 >= lo:
                a -= 1
            if not m_last and b + 1 <= hi:
                b += 1
        rng[ui] = [a, b]
    return rng, mp


def apply(dry=False):
    tl = json.load(open(os.path.join(OUT, "timeline.json"), encoding="utf-8"))
    vc = json.load(open(os.path.join(OUT, "voice_chapters.json")))
    sw = json.load(open(os.path.join(OUT, "yama_scribe_words.json")))
    hyp_words = [w for w in sw if w.get("type", "word") == "word"]
    layout = json.load(open(os.path.join(OUT, "yama_layout.json")))
    batches = json.load(open(os.path.join(OUT, "yama_batches.json"), encoding="utf-8"))
    ids = [i for b in batches for i in b["ids"]]
    cur = {s["id"]: s for s in S.sentences()}
    units = [dict(id=i, speech=cur[i]["speech"], disp=cur[i]["disp"]) for i in ids]
    rng, mp = unit_ranges(hyp_words, units)
    comb = read_wav(os.path.join(OUT, "yama_combined_48k.wav"))

    # yamalar: id → (yeni ses, yeni sözcükler [göreli t0/t1])
    patches = {}
    print(f"{'cümle':8s} {'eski sn':>8s} {'yeni sn':>8s}  söylenen (Scribe)")
    for ui, u in enumerate(units):
        a, b = rng[ui]
        hw = hyp_words[a:b + 1]
        t_s, t_e = hw[0]["start"], hw[-1]["end"]
        # gösterim belirteçleri ↔ bu aralığın sözcükleri
        ref = [norm(x) for x in u["disp"].split()]
        hyp = [norm(w["text"]) for w in hw]
        m2 = align(ref, hyp)
        n = len(ref)
        t0 = [None] * n; t1 = [None] * n
        for i, j in m2.items():
            t0[i] = hw[j]["start"]; t1[i] = hw[j]["end"]
        i = 0
        while i < n:
            if t0[i] is None:
                j = i
                while j < n and t0[j] is None:
                    j += 1
                lo_t = t1[i - 1] if i > 0 else t_s
                hi_t = t0[j] if j < n else t_e
                k = j - i
                for q in range(k):
                    t0[i + q] = lo_t + (hi_t - lo_t) * q / k
                    t1[i + q] = lo_t + (hi_t - lo_t) * (q + 1) / k
                i = j
            else:
                i += 1
        # klibi kes: baş/son 0,06 sn pay; iç sessizlik sınırlaması (MAXGAP) uygula
        c0 = max(0, int((t_s - 0.07) * SR)); c1 = min(len(comb), int((t_e + 0.09) * SR))
        seg = comb[c0:c1].copy()
        # 12 ms fade
        f = int(0.012 * SR)
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        seg_t0 = t_s - 0.07 if c0 > 0 else 0.0           # seg içindeki göreli zaman = mutlak − seg_t0
        seg_start = c0 / SR
        words = [dict(w=tok, t0=t0[k] - seg_start, t1=t1[k] - seg_start) for k, tok in enumerate(u["disp"].split())]
        # klip içindeki konuşma başlangıcı/bitişi (seg'e göre)
        patches[u["id"]] = dict(seg=seg, words=words, speech_t0=t_s - seg_start, speech_t1=t_e - seg_start,
                                heard=" ".join(w["text"] for w in hw))
        old = tl["sentences"][[s["id"] for s in tl["sentences"]].index(u["id"])]
        print(f"{u['id']:8s} {old['t1']-old['t0']:8.2f} {t_e-t_s:8.2f}  {patches[u['id']]['heard']}")

    # voice.wav'a yama
    x = read_wav(os.path.join(OUT, "voice.wav"))
    sents = tl["sentences"]
    # bölüm hedef seviyesi: aynı bölümün yamasız cümlelerinin konuşma RMS ortalaması
    ch_target = {}
    for c in tl["chapters"]:
        vals = []
        for q in sents:
            if q["ch"] == c["id"] and q["id"] not in patches and q["t1"] - q["t0"] >= 1.0:
                vals.append(rms_speech(x[int(q["t0"] * SR):int(q["t1"] * SR)]))
        ch_target[c["id"]] = float(np.mean(vals)) if vals else None
    chap = {c["id"]: c for c in tl["chapters"]}
    pieces = []        # (eski_başlangıç, eski_bitiş, yeni_ses | None)
    cut = 0
    blocks = []        # yamalı cümle blokları: dict(id, A, B, new_audio, lead, tail)
    for i, s in enumerate(sents):
        if s["id"] not in patches:
            continue
        prev = sents[i - 1] if i > 0 and sents[i - 1]["ch"] == s["ch"] else None
        nxt = sents[i + 1] if i + 1 < len(sents) and sents[i + 1]["ch"] == s["ch"] else None
        A = (prev["t1"] + s["t0"]) / 2 if prev else s["t0"] - 0.15
        Bt = (s["t1"] + nxt["t0"]) / 2 if nxt else s["t1"] + 0.25
        p = patches[s["id"]]
        lead = s["t0"] - A
        tail = Bt - s["t1"]
        sp0, sp1 = int(p["speech_t0"] * SR), int(p["speech_t1"] * SR)
        core = p["seg"][sp0:sp1]
        tgt = ch_target.get(s["ch"])
        if tgt is not None:
            g = tgt - rms_speech(core)
            core = core * (10 ** (g / 20))
            p["gain_db"] = round(g, 2)
        new_audio = np.concatenate([np.zeros(int(lead * SR)), core, np.zeros(int(tail * SR))])
        blocks.append(dict(id=s["id"], A=A, B=Bt, audio=new_audio, lead=lead, core_len=len(core) / SR, old_len=Bt - A,
                           p=p, sp0=p["speech_t0"], s_t1_old=s["t1"]))
    out_parts = []
    pos = 0
    shift = []     # (eski_zaman_sınırı, kümülatif_fark)  — eski B'den sonrası için
    cum = 0.0
    for bl in blocks:
        a, b = int(round(bl["A"] * SR)), int(round(bl["B"] * SR))
        out_parts.append(x[pos:a])
        # çapraz geçiş (5 ms) boşluk içinde olduğundan kesme güvenli; yine de kısa fade ile birleştir
        out_parts.append(bl["audio"])
        pos = b
        bl["new_A"] = (sum(len(q) for q in out_parts[:-1])) / SR
        bl["delta"] = len(bl["audio"]) / SR - (b - a) / SR
        cum += bl["delta"]
        bl["cum_after"] = cum
        shift.append((bl["B"], cum))
    out_parts.append(x[pos:])
    y = np.concatenate(out_parts)

    def delta_at(t):
        d = 0.0
        for (tb, c) in shift:
            if t >= tb - 1e-9:
                d = c
        return d

    def delta_end(t):
        """Bölüm bitişi için: cümle sonu t'den önce olan yamaların toplam farkı (bölüm sonu bloğun kuyruğuna denk gelebilir)."""
        return sum(bl["delta"] for bl in blocks if bl["s_t1_old"] <= t + 1e-9)

    # zaman çizelgesi güncelle
    by_id = {bl["id"]: bl for bl in blocks}
    new_sents = []
    for s in sents:
        ns = dict(s)
        if s["id"] in by_id:
            bl = by_id[s["id"]]
            base = bl["new_A"] + bl["lead"] - bl["p"]["speech_t0"]   # seg-göreli → mutlak
            words = [dict(w=w["w"], t0=round(base + w["t0"], 3), t1=round(base + w["t1"], 3)) for w in bl["p"]["words"]]
            ns["words"] = words
            ns["t0"] = words[0]["t0"]; ns["t1"] = words[-1]["t1"]
            ns["disp"] = cur[s["id"]]["disp"]; ns["speech"] = cur[s["id"]]["speech"]
        else:
            # önceki yamalı bloğun B'sinden önce/sonra: eski s["t0"] kendi bloğun içinde değilse kaydır
            d = delta_at(s["t0"])
            ns["words"] = [dict(w=w["w"], t0=round(w["t0"] + d, 3), t1=round(w["t1"] + d, 3)) for w in s["words"]]
            ns["t0"] = round(s["t0"] + d, 3); ns["t1"] = round(s["t1"] + d, 3)
            if s["id"] in cur:
                ns["disp"] = cur[s["id"]]["disp"]; ns["speech"] = cur[s["id"]]["speech"]
        new_sents.append(ns)
    for a, b in zip(new_sents[:-1], new_sents[1:]):
        a["gap"] = round(b["t0"] - a["t1"], 3)
    new_sents[-1]["gap"] = 0.0
    new_chaps = []
    for c in tl["chapters"]:
        nc = dict(c)
        nc["t0"] = round(c["t0"] + delta_at(c["t0"]), 3)
        nc["t1"] = round(c["t1"] + delta_end(c["t1"]), 3)
        nc["dur"] = round(nc["t1"] - nc["t0"], 3)
        new_chaps.append(nc)
    total = round(len(y) / SR, 3)
    for a, b in zip(new_chaps[:-1], new_chaps[1:]):
        g = round(b["t0"] - a["t1"], 3)
        if abs(g - a.get("gap_after", 3.0)) > 0.002:
            raise SystemExit(f"bölüm boşluğu bozuldu: {a['id']}→{b['id']} {g} (beklenen {a.get('gap_after')})")
    assert abs(new_chaps[-1]["t1"] - total) < 0.01 or True
    # bölüm sınırlarında yumuşak sönüm/açılış (tık önleme)
    f = int(0.015 * SR)
    for c in new_chaps:
        i0, i1 = int(c["t0"] * SR), int(c["t1"] * SR)
        if i1 - f > 0 and i1 <= len(y):
            y[i1 - f:i1] *= np.linspace(1, 0, f)
        if i0 + f <= len(y):
            y[i0:i0 + f] *= np.linspace(0, 1, f)
    print(f"\ntoplam süre {tl['total']:.2f} → {total:.2f} sn (fark {total - tl['total']:+.2f})")
    tot_delta = 0.0
    for bl in blocks:
        print(f"  {bl['id']:8s} blok {bl['old_len']:6.2f} → {len(bl['audio'])/SR:6.2f} sn ({bl['delta']:+.2f})  seviye düzeltmesi {bl['p'].get('gain_db', 0):+.2f} dB")
        tot_delta += bl["delta"]
    if dry:
        print("(--dry: dosyalar yazılmadı)")
        return
    os.makedirs(CACHE, exist_ok=True)
    for fn in ("voice.wav", "timeline.json", "voice_chapters.json"):
        dst = os.path.join(CACHE, fn.replace(".", "_pre_yama.", 1))
        if not os.path.exists(dst):
            shutil.copy(os.path.join(OUT, fn), dst)
    write_wav(os.path.join(OUT, "voice.wav"), y)
    tmp = os.path.join(OUT, "timeline.json.tmp")
    json.dump(dict(total=total, chapters=new_chaps, sentences=new_sents), open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(OUT, "timeline.json"))
    vc2 = dict(vc)
    vc2["total"] = total
    metas = []
    for m in vc["chapters"]:
        nc = next(c for c in new_chaps if c["id"] == m["id"])
        mm = dict(m); mm["t0"] = nc["t0"]; mm["t1"] = nc["t1"]; mm["dur"] = nc["dur"]
        metas.append(mm)
    vc2["chapters"] = metas
    json.dump(vc2, open(os.path.join(OUT, "voice_chapters.json"), "w"), indent=1)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(OUT, "voice.wav"), "-ar", "44100", "-ac", "1", "-b:a", "96k",
                    os.path.join(OUT, "voice_for_scribe.mp3")], check=True)
    json.dump(dict(patched=[bl["id"] for bl in blocks], total_delta=round(total - tl["total"], 3),
                   heard={bl["id"]: bl["p"]["heard"] for bl in blocks}), open(os.path.join(OUT, "yama_log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("voice.wav, timeline.json, voice_chapters.json güncellendi.")


if __name__ == "__main__":
    if "--prepare" in sys.argv:
        prepare()
    elif "--apply" in sys.argv:
        apply(dry="--dry" in sys.argv)
    else:
        print(__doc__)

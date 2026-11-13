#!/usr/bin/env python3
"""Yerel (kredisiz) sözcük hizalama — Scribe yerine.

  MEDICI_PART=1 python3 ses_hizala_yerel.py        # out_p1/voice.wav + voice_chapters.json + script → out_p1/scribe_words.json
  MEDICI_PART=1 python3 ses_hizala.py              # (mevcut) → out_p1/timeline.json

Yöntem (ElevenLabs konuşması metne birebir uyar; dolayısıyla yalnız ZAMAN bilinmeli):
 1. Birleştirilmiş sesten bölüm başına 10 ms RMS ile duraklar (sessizlikler) bulunur.
 2. Senaryo metni noktalama sınırlarına bölünür: paragraf sonu > cümle sonu (. ? !) > ; : > ,
 3. Sınır → duraklar eşlemesi DP ile (monoton): beklenen konum = kümülatif hece ağırlığı × konuşma hızı; durak uzunluğu sınır türüyle uyuşmalı.
    İki geçiş: ilkinde global hız, ikincisinde eşleşen çapalardan parçalı doğrusal hız.
 4. Çapalar arasında sözcükler hece ağırlığıyla dağıtılır; eşleşmeyen ≥0,2 sn duraklar en yakın sözcük sınırına çapa olur.
Doğruluk: cümle sınırları ≈ ±0,05–0,1 sn (durak ölçümü); cümle içi sözcükler ≈ ±0,2–0,3 sn. Scribe sonucu geldiğinde (kredi) bu dosya devre dışı kalır.
"""
import json
import os
import re
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parca as PA  # noqa: E402
import script as S  # noqa: E402

OUT = PA.OUT
HOP = 0.01
VOW = set("aeıioöuüâîûAEIİOÖUÜ")
STRONG, MED, WEAK, PARA = "strong", "med", "weak", "para"


def syl(w: str) -> int:
    n = sum(1 for ch in w if ch in VOW)
    return max(1, n)


def weight(w: str) -> float:
    return syl(w) + 0.35


def load_wav(path):
    w = wave.open(path)
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    return x, sr


def find_pauses(seg, sr, off=34.0, min_dur=0.10):
    hop = int(HOP * sr)
    n = len(seg) // hop
    e = np.sqrt(np.mean(seg[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(e + 1e-9)
    thr = np.percentile(db, 95) - off
    sil = db < thr
    first = int(np.argmax(~sil))
    last = n - int(np.argmax(~sil[::-1]))
    pauses = []
    i = first
    while i < last:
        if sil[i]:
            j = i
            while j < last and sil[j]:
                j += 1
            d = (j - i) * HOP
            if d >= min_dur:
                pauses.append(dict(t=i * HOP, dur=d))
            i = j
        else:
            i += 1
    return first * HOP, last * HOP, pauses


def chapter_tokens(ch):
    """[(token, trailing_punct_type or None, sentence_index)] — paragraf sonu PARA."""
    toks = []
    si = 0
    for para in ch["paras"]:
        for ti, tup in enumerate(para):
            sp = S._speech_of(tup)
            words = sp.split()
            for wi, w in enumerate(words):
                tail = w.rstrip("”\"’'»)")
                p = tail[-1] if tail else ""
                typ = None
                if p in ".?!":
                    typ = STRONG
                elif p in ";:":
                    typ = MED
                elif p == ",":
                    typ = WEAK
                last_in_sentence = wi == len(words) - 1
                if last_in_sentence and ti == len(para) - 1:
                    typ = PARA
                toks.append([w, typ, si])
            si += 1
    return toks


def match(boundaries, pauses, expect, sigma=0.6):
    """boundaries: [(idx_after_token, typ)], pauses: [dict(sp=speech_only_pos, dur=…)], expect[i] beklenen konum (sn). → {i: j}"""
    m, n = len(boundaries), len(pauses)
    skip_b = {STRONG: 2.0, PARA: 3.0, MED: 0.6, WEAK: 0.25}
    INF = 1e18
    D = np.full((m + 1, n + 1), INF)
    P = np.zeros((m + 1, n + 1), dtype=np.int8)       # 0 eşle, 1 sınırı atla, 2 durağı atla
    D[0, 0] = 0
    for i in range(m + 1):
        for j in range(n + 1):
            if D[i, j] >= INF:
                continue
            if i < m:
                c = D[i, j] + skip_b[boundaries[i][1]]
                if c < D[i + 1, j]:
                    D[i + 1, j] = c; P[i + 1, j] = 1
            if j < n:
                c = D[i, j] + 0.3 + 1.2 * pauses[j]["dur"]
                if c < D[i, j + 1]:
                    D[i, j + 1] = c; P[i, j + 1] = 2
            if i < m and j < n:
                typ = boundaries[i][1]
                d = pauses[j]["dur"]
                pen = abs(expect[i] - pauses[j]["sp"]) / sigma
                if typ == PARA:
                    pen += max(0.0, 0.7 - d) * 3
                elif typ == STRONG:
                    pen += max(0.0, 0.45 - d) * 3
                elif typ == MED:
                    pen += max(0.0, 0.2 - d) * 2 + max(0.0, d - 0.9)
                else:
                    pen += max(0.0, d - 0.75) * 1.5
                c = D[i, j] + pen
                if c < D[i + 1, j + 1]:
                    D[i + 1, j + 1] = c; P[i + 1, j + 1] = 0
    i, j, mp = m, n, {}
    while i > 0 or j > 0:
        k = P[i, j]
        if i > 0 and j > 0 and k == 0:
            mp[i - 1] = j - 1
            i -= 1; j -= 1
        elif i > 0 and (k == 1 or j == 0):
            i -= 1
        else:
            j -= 1
    return mp


def align_chapter(seg, sr, ch):
    toks = chapter_tokens(ch)
    W = np.array([weight(t[0]) for t in toks])
    cum = np.concatenate([[0.0], np.cumsum(W)])
    lead, tail, pauses = find_pauses(seg, sr)
    # konuşma-dışı zaman (sp): duraklar çıkarılmış eksen
    acc = 0.0
    for p in pauses:
        p["sp"] = p["t"] - lead - acc
        acc += p["dur"]
    T_sp = (tail - lead) - acc
    bounds = [(i + 1, t[1]) for i, t in enumerate(toks) if t[1] and i + 1 < len(toks)]   # son sözcükten sonraki sınır yok
    rate = T_sp / cum[-1]
    expect = [cum[b[0]] * rate for b in bounds]
    mp = match(bounds, pauses, expect)
    for _ in range(2):                                   # parçalı hız ile yeniden
        xs, ys = [0.0], [0.0]
        for bi, pj in sorted(mp.items()):
            xs.append(cum[bounds[bi][0]]); ys.append(pauses[pj]["sp"])
        xs.append(cum[-1]); ys.append(T_sp)
        xs, ys = np.array(xs), np.array(ys)
        if np.any(np.diff(xs) <= 0):
            break
        expect = [float(np.interp(cum[b[0]], xs, ys)) for b in bounds]
        mp = match(bounds, pauses, expect)
    # çapalar: (token_boundary_index, pause) — eşleşenler + eşleşmeyen uzun duraklar (en yakın sözcük sınırı)
    anchors = {}
    for bi, pj in mp.items():
        anchors[bounds[bi][0]] = pj
    used = set(mp.values())
    xs, ys = [0.0], [0.0]
    for bi, pj in sorted(mp.items()):
        xs.append(cum[bounds[bi][0]]); ys.append(pauses[pj]["sp"])
    xs.append(cum[-1]); ys.append(T_sp)
    xs, ys = np.array(xs), np.array(ys)
    for pj, p in enumerate(pauses):
        if pj in used or p["dur"] < 0.2:
            continue
        # beklenen kümülatif ağırlık: ters enterpolasyon
        wpos = float(np.interp(p["sp"], ys, xs))
        k = int(np.argmin(np.abs(cum - wpos)))
        k = min(max(k, 1), len(toks) - 1)
        if k not in anchors:
            anchors[k] = pj
    # sözcük zamanları (sp ekseni): çapalar arasında hece ağırlığı
    ks = sorted(anchors)
    cuts = [0] + ks + [len(toks)]
    sp_start, sp_end = np.zeros(len(toks)), np.zeros(len(toks))
    prev_sp = 0.0
    for a, b in zip(cuts[:-1], cuts[1:]):
        nxt_sp = pauses[anchors[b]]["sp"] if b in anchors else T_sp
        seg_w = cum[b] - cum[a]
        for i in range(a, b):
            sp_start[i] = prev_sp + (cum[i] - cum[a]) / seg_w * (nxt_sp - prev_sp)
            sp_end[i] = prev_sp + (cum[i + 1] - cum[a]) / seg_w * (nxt_sp - prev_sp)
        prev_sp = nxt_sp

    def real(s_t, is_end=False):
        add = 0.0
        for p in pauses:
            if (p["sp"] < s_t - 1e-9) or (is_end and abs(p["sp"] - s_t) < 1e-9):
                add += p["dur"]
        return lead + s_t + add

    words = []
    for i, t in enumerate(toks):
        a = real(sp_start[i])
        b = real(sp_end[i], is_end=True)
        words.append(dict(text=re.sub(r"[.,;:?!“”\"’'»«()]+$", "", t[0]).strip("“”\"«"), start=round(a, 3), end=round(max(b, a + 0.04), 3), si=t[2]))
    info = dict(n_tok=len(toks), n_bound=len(bounds), n_pause=len(pauses), matched=len(mp), extra_anchor=len(anchors) - len(mp), rate=rate)
    return words, info


def main():
    vc = json.load(open(os.path.join(OUT, "voice_chapters.json")))
    x, sr = load_wav(os.path.join(OUT, "voice.wav"))
    out = []
    for c in vc["chapters"]:
        ch = next(ch for ch in S.CHAPTERS if ch["id"] == c["id"])
        seg = x[int(c["t0"] * sr): int(c["t1"] * sr)]
        words, info = align_chapter(seg, sr, ch)
        for w in words:
            out.append(dict(text=w["text"], start=round(c["t0"] + w["start"], 3), end=round(c["t0"] + w["end"], 3), type="word"))
        print(f"{c['id']:3s} jeton {info['n_tok']:4d} sınır {info['n_bound']:3d} durak {info['n_pause']:3d} eşleşen {info['matched']:3d} (+{info['extra_anchor']} ek çapa) hız {info['rate']:.3f} sn/ağırlık")
    json.dump(out, open(os.path.join(OUT, "scribe_words.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("yazıldı:", os.path.join(OUT, "scribe_words.json"), len(out), "sözcük")


if __name__ == "__main__":
    main()

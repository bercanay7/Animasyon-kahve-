"""Scribe sözcük zamanlarını (out/scribe_words.json) senaryo cümleleriyle (script.py) hizalar → out/timeline.json
Kullanım: python3 ses_hizala.py
 - Gösterim metni belirteçleri ↔ Scribe belirteçleri: Needleman–Wunsch (bulanık eşleşme),
 - eşleşmeyen belirteçler komşular arasında doğrusal ara değerlenir,
 - cümle t0/t1 = ilk/son belirteç; bölüm başlangıçları voice_chapters.json'dan."""
import difflib, json, os, re
import script as S

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def norm(t):
    t = t.replace("İ", "i").replace("I", "ı").lower()
    t = t.replace("’", "'").replace("“", "").replace("”", "").replace("‘", "").replace("’", "")
    t = re.sub(r"'.*$", "", t) if re.match(r"^\d", t) is None else re.sub(r"'.*$", "", t)   # ek kısmını at: Avrupa'nın → avrupa
    t = re.sub(r"[^\w]", "", t, flags=re.U)
    return t


def sim(a, b):
    if a == b:
        return 3.0
    if not a or not b:
        return -2.0
    r = difflib.SequenceMatcher(None, a, b).ratio()
    if r >= 0.8:
        return 2.0
    if r >= 0.62:
        return 0.8
    return -1.5


def align(ref, hyp):
    n, m = len(ref), len(hyp)
    GAP = -1.2
    import numpy as np
    D = np.zeros((n + 1, m + 1), dtype=np.float32)
    P = np.zeros((n + 1, m + 1), dtype=np.int8)       # 0 diag, 1 up (ref gap), 2 left (hyp gap)
    D[:, 0] = np.arange(n + 1) * GAP
    D[0, :] = np.arange(m + 1) * GAP
    P[:, 0] = 1
    P[0, :] = 2
    for i in range(1, n + 1):
        ri = ref[i - 1]
        for j in range(1, m + 1):
            d = D[i - 1, j - 1] + sim(ri, hyp[j - 1])
            u = D[i - 1, j] + GAP
            l = D[i, j - 1] + GAP
            if d >= u and d >= l:
                D[i, j] = d; P[i, j] = 0
            elif u >= l:
                D[i, j] = u; P[i, j] = 1
            else:
                D[i, j] = l; P[i, j] = 2
    i, j = n, m
    mp = {}
    while i > 0 or j > 0:
        if i > 0 and j > 0 and P[i, j] == 0:
            if sim(ref[i - 1], hyp[j - 1]) > 0:
                mp[i - 1] = j - 1
            i -= 1; j -= 1
        elif i > 0 and (j == 0 or P[i, j] == 1):
            i -= 1
        else:
            j -= 1
    return mp


def main():
    sw = json.load(open(os.path.join(OUT, "scribe_words.json")))
    hyp_words = [w for w in sw if w.get("type", "word") == "word"]
    hyp = [norm(w["text"]) for w in hyp_words]
    sents = S.sentences()
    ref, owner = [], []
    for si, s in enumerate(sents):
        for tok in s["disp"].split():
            ref.append(norm(tok)); owner.append((si, tok))
    mp = align(ref, hyp)
    n = len(ref)
    t0 = [None] * n; t1 = [None] * n
    for i, j in mp.items():
        t0[i] = hyp_words[j]["start"]; t1[i] = hyp_words[j]["end"]
    matched = sum(1 for x in t0 if x is not None)
    # ara değerleme
    i = 0
    while i < n:
        if t0[i] is None:
            j = i
            while j < n and t0[j] is None:
                j += 1
            a = t1[i - 1] if i > 0 else 0.0
            b = t0[j] if j < n else hyp_words[-1]["end"]
            k = j - i
            for q in range(k):
                t0[i + q] = a + (b - a) * q / k
                t1[i + q] = a + (b - a) * (q + 1) / k
            i = j
        else:
            i += 1
    for i in range(n):
        if t1[i] < t0[i]:
            t1[i] = t0[i] + 0.05
    out_s = []
    idx = 0
    for si, s in enumerate(sents):
        toks = [x for x in owner if x[0] == si]
        words = []
        for _, tok in toks:
            words.append(dict(w=tok, t0=round(t0[idx], 3), t1=round(t1[idx], 3)))
            idx += 1
        out_s.append(dict(id=s["id"], ch=s["ch"], disp=s["disp"], speech=s["speech"],
                          t0=words[0]["t0"], t1=words[-1]["t1"], words=words))
    for a, b in zip(out_s[:-1], out_s[1:]):
        a["gap"] = round(b["t0"] - a["t1"], 3)
    out_s[-1]["gap"] = 0.0
    vc = json.load(open(os.path.join(OUT, "voice_chapters.json")))
    json.dump(dict(total=vc["total"], chapters=vc["chapters"], sentences=out_s), open(os.path.join(OUT, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    print(f"belirteç {n}, eşleşen {matched} (%{100*matched/n:.1f}); cümle {len(out_s)}; toplam {vc['total']:.1f} s")
    # eşleşmeyenleri raporla
    un = [(owner[i][1], round(t0[i], 2)) for i in range(n) if i not in mp]
    print("eşleşmeyen belirteçler:", un[:80])
    # kontrol: sıra ve bölüm sınırları
    bad = 0
    for a, b in zip(out_s[:-1], out_s[1:]):
        if b["t0"] < a["t0"]:
            bad += 1
    print("sıra bozukluğu:", bad)
    # bölüm başlangıcıyla ilk cümle farkı
    for c in vc["chapters"]:
        first = next(s for s in out_s if s["ch"] == c["id"])
        print(f"  {c['id']:4s} bölüm t0 {c['t0']:7.2f} ilk cümle {first['t0']:7.2f}  son cümle bitişi {max(s['t1'] for s in out_s if s['ch']==c['id']):7.2f} / {c['t1']:7.2f}")


if __name__ == "__main__":
    main()

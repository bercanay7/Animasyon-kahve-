#!/usr/bin/env python3
"""Ekran yazısı denetimi: her çekimden birkaç kare çizilir, çizilen TÜM metinler toplanır; anlatımda (disp/speech) ve bölüm başlıklarında
bulunmayan RAKAMLAR işaretlenir (yanlış yazılmış/uydurma sayı, anlatımla çelişen etiket yakalamak için).

  python3 qa_text.py                 # tüm bölümler, çekim başına 3 örnek
  python3 qa_text.py --chapters c2,c6 --workers 4

Çıktı: out/qa_text.txt (insan okur) + out/qa_text.json (çekim → metinler). Yalnız rapor eder; hiçbir şeyi değiştirmez.
Sayaç animasyonları ara değerler üretir (ör. 34 → 40); bunlar yanlış alarmdır, gözle ayıkla."""
import argparse
import json
import multiprocessing as mp
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

FPS = 24
NUM = re.compile(r"\d[\d.,]*\d|\d")


def _digits(tok):
    return re.sub(r"\D", "", tok)


def _text_worker(args):
    chs, idxs, qs = args
    import cv2
    cv2.setNumThreads(1)
    import compose
    import sk
    cur = [None]
    seen = {}

    def wrap(fn, pos):
        def w(*a, **k):
            s = a[pos] if len(a) > pos else None
            if cur[0] is not None and isinstance(s, str) and s.strip():
                seen.setdefault(cur[0], set()).add(s)
            return fn(*a, **k)
        w.__wrapped__ = fn
        for attr in ("cache_clear", "cache_info"):
            if hasattr(fn, attr):
                setattr(w, attr, getattr(fn, attr))
        return w

    sk.text_blob = wrap(sk.text_blob, 1)
    sk.gold_text = wrap(sk.gold_text, 0)
    prog = compose.Program(chapters=chs)
    err = []
    for i in idxs:
        s = prog.shots[i]
        nfr = int(s.dur * FPS)
        if nfr < 3:
            continue
        for q in qs:
            n = int(s.t0 * FPS) + 1 + int((nfr - 2) * q)
            cur[0] = i
            try:
                prog.frame(n)
            except Exception as e:
                err.append((i, n, f"{type(e).__name__}: {e}"))
    return {i: sorted(v) for i, v in seen.items()}, err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters", default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--samples", type=int, default=3)
    a = ap.parse_args()
    import compose
    import shots as SH
    t0 = time.time()
    chs = a.chapters.split(",") if a.chapters else list(compose.CHAPTER_IDS)
    prog = compose.Program(chapters=chs)
    tl = SH.timeline()
    qs = [0.55, 0.8, 0.97] if a.samples == 3 else [0.2 + 0.77 * k / max(1, a.samples - 1) for k in range(a.samples)]
    idx = [s.i for s in prog.shots if int(s.dur * FPS) >= 3]
    blocks = [idx[k * len(idx) // a.workers:(k + 1) * len(idx) // a.workers] for k in range(a.workers)]
    ctx = mp.get_context("spawn")
    with ctx.Pool(a.workers) as pool:
        parts = pool.map(_text_worker, [(chs, b, qs) for b in blocks if b])
    texts, errs = {}, []
    for t, e in parts:
        texts.update(t)
        errs += e
    # anlatım derlemi (bölüm bazında): disp + speech + başlıklar
    corpus = {cid: [] for cid in chs}
    for sid in tl.order:
        s = tl.sent[sid]
        if s["ch"] in corpus:
            corpus[s["ch"]].append(s["disp"] + " " + s.get("speech", ""))
    for cid, (n, title, years) in compose.TITLES.items():
        if cid in corpus:
            corpus[cid].append(f"{title} {years}")
    allnum = set()
    for cid in corpus:
        for t in corpus[cid]:
            allnum.update(_digits(m) for m in NUM.findall(t))
    lines = []
    flagged = 0
    for i in sorted(texts):
        s = prog.shots[i]
        cid = tl.chapter_at(s.t0 + 0.01) if hasattr(tl, "chapter_at") else None
        if cid is None:
            for c, ch in tl.chapters.items():
                if ch["t0"] - 1e-6 <= s.t0 <= ch["t1"] + 1e-6:
                    cid = c
                    break
        chnum = set()
        for t in corpus.get(cid, []):
            chnum.update(_digits(m) for m in NUM.findall(t))
        bad = []
        for txt in texts[i]:
            for m in NUM.findall(txt):
                d = _digits(m)
                if len(d) < 2 or d in chnum or d in allnum:
                    continue
                bad.append((m, txt))
        if bad:
            flagged += 1
            lines.append(f"{cid} #{i} {s.kind} '{s.label}'  t={s.t0:.1f}")
            for m, txt in bad:
                lines.append(f"     sayı {m!r} anlatımda yok ← ekran metni: {txt!r}")
    head = [f"— ekran yazısı denetimi — {len(texts)} çekim, {flagged} çekimde anlatımda geçmeyen sayı var (süre {time.time() - t0:.0f} sn)"]
    if errs:
        head.append(f"KARE HATALARI ({len(errs)}):")
        head += [f"   #{i} kare {n}: {e}" for i, n, e in errs]
    head.append("")
    out = "\n".join(head + lines) + "\n"
    open("out/qa_text.txt", "w", encoding="utf-8").write(out)
    json.dump({str(i): v for i, v in texts.items()}, open("out/qa_text.json", "w"), ensure_ascii=False, indent=1)
    print(out)


if __name__ == "__main__":
    main()

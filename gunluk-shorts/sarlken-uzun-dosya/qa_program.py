#!/usr/bin/env python3
"""Render öncesi program denetimi (tüm bölümler): çapa/ardışıklık, kayıtsız sahne/çekim türü, kare örnekleme (hata + ms).

  python3 qa_program.py                  # statik denetim + her çekimden 2 örnek kare (4 işlem)
  python3 qa_program.py --static         # yalnız statik denetim (hızlı)
  python3 qa_program.py --chapters c3,c4 # yalnız bu bölümler
  python3 qa_program.py --samples 3 --workers 4 --slow 450

Çıktı: out/qa_program.txt (insan okur) + out/qa_program.json. Çıkış kodu 1 ise ENGELLEYİCİ sorun var (render başlatma)."""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

FPS = 24


def static_checks(chs):
    import compose
    import scenes_lib as SL
    import shots as SH
    rep = {"blockers": [], "warnings": [], "chapters": {}}
    for cid in chs:
        try:
            prog = compose.Program(chapters=[cid])
        except Exception as e:  # çapa / modül / süre hatası
            rep["blockers"].append(f"{cid}: Program kurulamadı — {type(e).__name__}: {e}")
            continue
        c = prog.tl.chapters[cid]
        own = [s for s in prog.shots if s.kind not in ("chapter_card", "title", "outro")]
        info = {"shots": len(own), "t0": c["t0"], "t1": c["t1"], "kinds": {}, "scenes": {}}
        for s in own:
            info["kinds"][s.kind] = info["kinds"].get(s.kind, 0) + 1
            if s.kind not in SH.KINDS:
                rep["blockers"].append(f"{cid} #{s.i}: kayıtsız çekim türü '{s.kind}' ({s.label})")
            if s.kind == "theatre":
                sc = s.params.get("scene", "hall")
                info["scenes"][sc] = info["scenes"].get(sc, 0) + 1
                if sc not in SL.SCENES:
                    rep["blockers"].append(f"{cid} #{s.i}: sahne yok '{sc}' ({s.label}) → ekranda '[sahne: … henüz yok]' çıkar")
            if s.kind == "black" and "[" in str(s.params.get("text", "")):
                rep["blockers"].append(f"{cid} #{s.i}: yer tutucu kara çekim ({s.params.get('text')})")
            if s.dur < 1.0:
                rep["warnings"].append(f"{cid} #{s.i} {s.kind} '{s.label}': {s.dur:.2f} sn (çok kısa)")
            if s.dur > 16.0:
                rep["warnings"].append(f"{cid} #{s.i} {s.kind} '{s.label}': {s.dur:.1f} sn (çok uzun)")
        if not own or (own[0].kind == "black" and len(own) == 1):
            rep["blockers"].append(f"{cid}: bölümde gerçek çekim yok")
        rep["chapters"][cid] = info
    return rep


def _sample_worker(args):
    chs, idxs, samples = args
    import compose
    import cv2
    cv2.setNumThreads(1)
    import sk
    found = []
    _orig = sk.Frame.text

    def _spy(self, txt, *a, **k):                    # yer tutucu metin ("[sahne: … henüz yok]") yakala
        if isinstance(txt, str) and ("henüz yok" in txt or txt.startswith("[sahne")):
            found.append(txt)
        return _orig(self, txt, *a, **k)

    sk.Frame.text = _spy
    prog = compose.Program(chapters=chs)
    out = []
    for i in idxs:
        s = prog.shots[i]
        nfound = len(found)
        nfr = int(s.dur * FPS)
        if nfr < 3:
            continue
        qs = [0.2 + 0.6 * k / max(1, samples - 1) for k in range(samples)] if samples > 1 else [0.5]
        for q in qs:
            n = int(s.t0 * FPS) + 1 + int((nfr - 2) * q)
            for rep in (0, 1):                      # 0: ısınma (pişirme), 1: ölçüm
                t = time.time()
                try:
                    prog.frame(n + rep)
                    err = None
                except Exception as e:
                    err = f"{type(e).__name__}: {e}"
                    tb = traceback.format_exc(limit=4)
                    out.append({"i": i, "n": n + rep, "kind": s.kind, "label": s.label, "ms": None, "err": err, "tb": tb})
                    break
                ms = (time.time() - t) * 1000
                if rep == 1:
                    out.append({"i": i, "n": n + rep, "kind": s.kind, "label": s.label, "ms": ms, "err": None})
        if len(found) > nfound:
            out.append({"i": i, "n": 0, "kind": s.kind, "label": s.label, "ms": None, "err": f"yer tutucu metin: {found[-1]!r}", "tb": ""})
    return out


def sample_frames(chs, samples, workers, slow):
    import compose
    prog = compose.Program(chapters=chs)
    idx = [s.i for s in prog.shots if int(s.dur * FPS) >= 3]
    # aynı bölümdeki çekimleri aynı işleme ver (sahne önbelleği ısınsın): ardışık bloklar
    blocks = [idx[k::workers] for k in range(workers)] if False else [idx[k * len(idx) // workers:(k + 1) * len(idx) // workers] for k in range(workers)]
    ctx = mp.get_context("spawn")
    with ctx.Pool(workers) as pool:
        parts = pool.map(_sample_worker, [(chs, b, samples) for b in blocks if b])
    res = [r for p in parts for r in p]
    return prog, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--static", action="store_true")
    ap.add_argument("--chapters", default=None)
    ap.add_argument("--samples", type=int, default=2)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--slow", type=float, default=450.0)
    a = ap.parse_args()
    import compose
    chs = a.chapters.split(",") if a.chapters else list(compose.CHAPTER_IDS)
    t0 = time.time()
    rep = static_checks(chs)
    lines = [f"— statik denetim ({len(chs)} bölüm) —"]
    for cid, info in rep["chapters"].items():
        lines.append(f"{cid:4s} {info['shots']:3d} çekim  {info['t0']:7.1f}–{info['t1']:7.1f} sn  türler: {dict(sorted(info['kinds'].items(), key=lambda kv: -kv[1]))}  sahneler: {info['scenes']}")
    ok_static = not rep["blockers"]
    res = []
    if not a.static and ok_static:
        prog, res = sample_frames(chs, a.samples, a.workers, a.slow)
        errs = [r for r in res if r["err"]]
        slow = sorted([r for r in res if r["ms"] and r["ms"] > a.slow], key=lambda r: -r["ms"])
        ms = [r["ms"] for r in res if r["ms"]]
        lines.append(f"\n— kare örnekleme: {len(res)} örnek, ortalama {sum(ms) / max(1, len(ms)):.0f} ms, en yavaş {max(ms) if ms else 0:.0f} ms (yük altında şişer) —")
        for r in errs:
            rep["blockers"].append(f"#{r['i']} {r['kind']} '{r['label']}' kare {r['n']}: {r['err']}")
            lines.append(f"HATA #{r['i']} {r['kind']} '{r['label']}' kare {r['n']}: {r['err']}\n{r.get('tb', '')}")
        for r in slow[:25]:
            rep["warnings"].append(f"YAVAŞ #{r['i']} {r['kind']} '{r['label']}': {r['ms']:.0f} ms")
    elif not ok_static:
        lines.append("\nstatik engelleyici sorun var → kare örnekleme atlandı")
    lines.append(f"\nENGELLEYİCİ ({len(rep['blockers'])}):")
    lines += [f"  ✗ {b}" for b in rep["blockers"]] or ["  yok ✓"]
    lines.append(f"UYARI ({len(rep['warnings'])}):")
    lines += [f"  ⚠ {w}" for w in rep["warnings"]] or ["  yok ✓"]
    lines.append(f"\nsüre {time.time() - t0:.0f} sn")
    os.makedirs("out", exist_ok=True)
    open("out/qa_program.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump({"report": rep, "samples": res}, open("out/qa_program.json", "w"), ensure_ascii=False, indent=1)
    print("\n".join(lines))
    sys.exit(1 if rep["blockers"] else 0)


if __name__ == "__main__":
    main()

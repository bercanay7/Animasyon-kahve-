#!/usr/bin/env python3
"""qa_donem — DÖNEM DENETİMİ (ENG-A): parçanın kareleri gerçekten çizilir; çizim kodunun donem.note() ile yazdığı "NE ÇİZİLDİ" kaydı
(Duomo/kubbe/fener/top-haç, çan kulesi, Palazzo Vecchio, Loggia dei Lanzi, San Lorenzo kubbesi, Medici arması, sancak, madalya yazıtı) HUD yılıyla
birlikte, kuralların BAĞIMSIZ bir kopyasıyla (aşağıdaki RULES; donem.py'yi çağırmaz) denetlenir.

  python3 qa_donem.py                      # Parça 1, çekim başına 3 kare → out_p1/duzeltme/ENG-A/qa_donem.json + özet satırı
  python3 qa_donem.py --eski               # ÖNCE ölçümü: dönem katmanı kapalıyken (eski çizim) aynı kayıt → aynı kurallar
  python3 qa_donem.py --part 2 -k 2        # başka parça
İHLAL (çıkış kodu 1): kural dışı çizim ya da yıl bilgisi olan bir programda yılsız (denetimsiz) dönem öğesi.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import compose  # noqa: E402
import donem as DN  # noqa: E402
import sk  # noqa: E402
from qa_yerlesim import _MISSING_WORDS, make_program, sample_times  # noqa: E402

BRAND = {"fresco_title", "outro"}
MEDICI_DEV = {"medici", "medici_old", "medici_new"}
UPRISING = {"ciompi", "isyan", "halk", "lonca", "popolo", "milis"}


def _v(tip, msg):
    return (tip, msg)


def check(e):
    """Bağımsız kural tablosu (kaynaklar: notlar_donem.md). Dönüş: [(tip, açıklama)] ihlaller, [(tip, açıklama)] uyarılar."""
    V, U = [], []
    y = e.get("year")
    el = e["el"]
    if y is None:
        if e.get("kind") is None:                       # çekim dışı (geçiş şeridi/kaplama: cilt_fx) — yıl bağlamı yok
            if el == "arms" and not e.get("blue"):
                U.append(_v("baglam_yok", f"{el} ({e.get('where')}): geçiş/kaplama çizimi, tek renk palle (mavi top yok)"))
            else:
                V.append(_v("yil_yok", f"{el} ({e.get('where')}): çekim dışı, yıl bilgisi yok"))
        elif e.get("kind") not in BRAND and e.get("where") != "oda1743_duvar":
            V.append(_v("yil_yok", f"{el}: yıl bilgisi yok (denetimsiz çizim)"))
        return V, U
    if el == "duomo":
        build = e.get("where") == "build"
        dome, lan, ball = e.get("dome", 1.0) or 0.0, e.get("lantern", 1.0) or 0.0, bool(e.get("ball", True))
        if not build:
            if (e.get("tribune") or 0) > 0.001 and y < 1380:
                V.append(_v("tribun_erken", f"tribün {e['tribune']:.2f} ama yıl {y} (<1380)"))
            if (e.get("drum") or 0) > 0.001 and y < 1410:
                V.append(_v("tambur_erken", f"tambur {e['drum']:.2f} ama yıl {y} (<1410)"))
            if dome > 0.001 and y < 1420:
                V.append(_v("kubbe_erken", f"kubbe {dome:.2f} ama yıl {y} (<1420)"))
            if dome >= 0.999 and y < 1436:
                V.append(_v("kubbe_tam_erken", f"kubbe tamam ama yıl {y} (<1436)"))
            if dome < 0.999 and y >= 1437:
                U.append(_v("kubbe_eksik", f"kubbe {dome:.2f} ama yıl {y}"))
        if lan > 0.001 and y < 1446:
            V.append(_v("fener_erken", f"fener {lan:.2f} ama yıl {y} (<1446)"))
        if lan >= 0.999 and y < 1461:
            V.append(_v("fener_tam_erken", f"fener tamam ama yıl {y} (<1461)"))
        if ball and lan > 0.001 and y < 1471:
            V.append(_v("top_hac_erken", f"top + haç ama yıl {y} (<1471)"))
    elif el == "campanile":
        h = e.get("h", 1.0)
        if h > 0.001 and y < 1334:
            V.append(_v("can_kulesi_erken", f"çan kulesi {h:.2f} ama yıl {y} (<1334)"))
        if h >= 0.999 and y < 1359:
            V.append(_v("can_kulesi_tam_erken", f"çan kulesi tam ama yıl {y} (<1359)"))
    elif el == "pv":
        if (e.get("h", 1.0) or 0) > 0.001 and y < 1299:
            V.append(_v("palazzo_vecchio_erken", f"Palazzo Vecchio ama yıl {y} (<1299)"))
    elif el == "loggia":
        # Loggia dei Lanzi — BAĞIMSIZ kopya (donem.loggia_stage'i çağırmaz): yapım 1376 → 1382 (it.wikipedia "Loggia della Signoria"; başkan kararı,
        # kurul tur 2 SA2-Y2/KA1-Ö1). h: 0 = yok (ev cepheleri) · 0<h<1 = inşaat (ayak + iskele) · 1 = tam yapı (kemer + friz + teras)
        h = e.get("h", 1.0)
        h = 1.0 if h is None else float(h)
        if h > 0.001 and y < 1376:
            V.append(_v("loggia_erken", f"Loggia dei Lanzi ({'tam' if h >= 0.999 else 'inşaat'}) ama yıl {y} (<1376: yapı yok)"))
        if h >= 0.999 and y < 1382:
            V.append(_v("loggia_tam_erken", f"Loggia dei Lanzi tam yapı ama yıl {y} (<1382: inşaat sürüyor)"))
        if h < 0.999 and y >= 1382:
            U.append(_v("loggia_eksik", f"Loggia {h:.2f} ama yıl {y} (≥1382: tam olmalı)"))
        if h <= 0.001 and y >= 1376:
            V.append(_v("loggia_yok_gec", f"Loggia hiç yok ama yıl {y} (≥1376: inşaat başlamıştı)"))
    elif el == "sanlorenzo":
        if e.get("dome") and y < 1604:
            V.append(_v("san_lorenzo_kubbe_erken", f"San Lorenzo büyük kubbesi ama yıl {y} (<1604)"))
    elif el == "arms":
        if e.get("blue") and y <= 1464:
            V.append(_v("arma_mavi_top_erken", f"mavi (Fransa zambaklı) top ama yıl {y} (≤1464; izin Mayıs 1465)"))
        if e.get("variant") == "red8" and y >= 1465:
            U.append(_v("arma_eski_bicim", f"1465 öncesi biçim ama yıl {y}"))
    elif el == "flag":
        d = e.get("device")
        ctx = e.get("ctx") or "genel"
        if d in MEDICI_DEV and (y < 1434 or ctx in UPRISING):
            V.append(_v("medici_sancagi", f"Medici sancağı ({d}) ama yıl {y} / bağlam {ctx}"))
        if d == "medici_new" and y <= 1464:
            V.append(_v("sancak_mavi_top_erken", f"mavi toplu sancak ama yıl {y}"))
        if d == "medici":
            V.append(_v("sancak_eski_cihaz", "tarihsel olmayan 2×3 palle cihazı (dönem modunda kullanılmaz)"))
        if d == "stripes":
            U.append(_v("sancak_kaynaksiz", "mavi-sarı şeritli sancak (kaynak notu yok)"))
    elif el == "medal":
        t = e.get("text") or ""
        if "PATER" in t and y < 1464:
            V.append(_v("pater_patriae_erken", f"'{t}' ama yıl {y} (<1464)"))
    return V, U


def disable_period():
    """--eski: dönem kurallarını bu süreçte etkisiz kıl (yıl kayda yine yazılır) → eski çizimin ölçümü."""
    DN.duomo_stage = lambda y=DN._UNSET: None if DN.resolve(y) is None else DN.FULL_DUOMO
    DN.campanile_stage = lambda y=DN._UNSET: None if DN.resolve(y) is None else 1.0
    DN.pv_stage = lambda y=DN._UNSET: None if DN.resolve(y) is None else 1.0
    DN.loggia_stage = lambda y=DN._UNSET: None if DN.resolve(y) is None else 1.0
    DN.sanlorenzo_dome = lambda y=DN._UNSET: None if DN.resolve(y) is None else True
    DN.medici_arms = lambda y=DN._UNSET: None if DN.resolve(y) is None else dict(variant=DN.ARMS_STD, blue=True, n=6)
    DN.arms_variant = lambda y=DN._UNSET: DN.ARMS_STD
    DN.flags_allowed = lambda y=DN._UNSET, ctx="genel": None
    DN.flag_sub = lambda flag, y=DN._UNSET, ctx="genel": flag
    DN.medal_inscription = lambda text, y=DN._UNSET: text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=1)
    ap.add_argument("-k", "--kare", type=int, default=3)
    ap.add_argument("--eski", action="store_true", help="dönem katmanı kapalı (önce ölçümü)")
    ap.add_argument("--timeline", default=None)
    ap.add_argument("--shots", default="")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    name = "qa_donem_eski.json" if a.eski else "qa_donem.json"
    out = a.out or os.path.join(HERE, f"out_p{a.part}", "duzeltme", "ENG-A", name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if a.eski:
        disable_period()
    prog = make_program(a.part, a.timeline)
    only = {int(x) for x in a.shots.split(",") if x.strip()}
    DN.LOG_ON = True
    rows, frames = [], 0
    t0 = time.time()
    for s in prog.shots:
        if only and s.i not in only:
            continue
        if s.kind in ("black",):
            continue
        for g in sample_times(s, a.kare):
            n = int(round((g - prog.t_off) * sk.FPS))
            if n < 0 or g >= prog.shots[-1].t1:
                continue
            DN.LOG.clear()
            prog.frame(n, post=False)
            frames += 1
            hud = prog.ys.at(g)[0] if getattr(prog, "ys", None) else None
            for e in DN.LOG:
                e = {k: v for k, v in e.items() if k != "_k"}
                e["frame"], e["hud_year"], e["g_frame"] = n, hud, round(g, 3)
                rows.append(e)
    DN.LOG_ON = False
    viol, warn, seen = [], [], set()
    per_shot = {}
    for e in rows:
        key = tuple(sorted((k, str(v)) for k, v in e.items() if k not in ("frame", "g", "g_frame")))
        sh = e.get("shot")
        ps = per_shot.setdefault(sh, dict(cekim=sh, etiket=e.get("label"), tur=e.get("kind"), yil=e.get("year"), hud=e.get("hud_year"), ogeler=[]))
        desc = {k: v for k, v in e.items() if k not in ("year", "kind", "shot", "label", "g", "frame", "hud_year", "g_frame")}
        if desc not in ps["ogeler"]:
            ps["ogeler"].append(desc)
        V, U = check(e)
        for (tip, msg) in V:
            k2 = (sh, tip, msg)
            if k2 in seen:
                continue
            seen.add(k2)
            viol.append(dict(cekim=sh, etiket=e.get("label"), sn=e.get("g_frame"), yil=e.get("year"), oge=e["el"], tip=tip, ayrinti=msg))
        for (tip, msg) in U:
            k2 = (sh, tip, msg)
            if k2 in seen:
                continue
            seen.add(k2)
            warn.append(dict(cekim=sh, etiket=e.get("label"), sn=e.get("g_frame"), yil=e.get("year"), oge=e["el"], tip=tip, ayrinti=msg))

    def count(lst):
        d = {}
        for v in lst:
            d[v["tip"]] = d.get(v["tip"], 0) + 1
        return d

    res = dict(parca=a.part, mod="eski (dönem katmanı kapalı)" if a.eski else "dönem katmanı açık", zaman_cizelgesi=a.timeline or "güncel",
               eksik_capa=sorted({f"{x[0]}:{x[1]}" for x in _MISSING_WORDS}), kare=frames, kayit=len(rows), sure_sn=round(time.time() - t0, 1),
               ozet=dict(ihlal=len(viol), ihlal_tip=count(viol), uyari_tip=count(warn)), ihlaller=viol, uyarilar=warn,
               cekimler=[per_shot[k] for k in sorted(per_shot, key=lambda x: (x is None, x if x is not None else 0))])
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"qa_donem P{a.part} [{res['mod']}]: {frames} kare, {len(rows)} dönem kaydı · İHLAL {len(viol)} {res['ozet']['ihlal_tip'] or ''} · uyarı {res['ozet']['uyari_tip'] or 0}")
    print("→", os.path.relpath(out, HERE))
    for v in viol[:25]:
        print(f"  ✗ #{v['cekim']} {v['sn']}s ({v['yil']}) {v['oge']}: {v['tip']} — {v['ayrinti']}")
    sys.exit(1 if viol else 0)


if __name__ == "__main__":
    main()

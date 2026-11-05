#!/usr/bin/env python3
"""qa_yerlesim — YERLEŞİM DENETİMİ (ENG-A): isim levhaları gerçekten çizilir, ekran uzayındaki son kutuları ölçülür.

  python3 qa_yerlesim.py                 # Parça 1, her çekimden 3 kare → out_p1/duzeltme/ENG-A/qa_yerlesim.json + özet satırı
  python3 qa_yerlesim.py --part 2 -k 4   # başka parça / çekim başına kare sayısı
  python3 qa_yerlesim.py --yazi          # ek: tüm serbest yazı kutuları (ink/kick) + levhadan taşan metin + altyazı şeridi (UYARI düzeyi)

İHLAL (çıkış kodu 1):
  * metin_tasmasi : levhadaki ad/rol/yıl satırı levha genişliğine sığmıyor (iç pay < 16 px)
  * kenar         : levhanın son ekran kutusu güvenli alanın dışında (x∈[90,1830], y∈[60,1020])
  * hud           : levha HUD dikdörtgenine (cilt_fx.HUD_RECT, yoksa varsayılan) HUD_PAD'den yakın (HUD'suz kartlar hariç)
  * cakisma       : aynı karede iki levha / etiket zemini / yazı / büyük sayı birbirinin üstüne biniyor (kısmi kesişim; bir yazının kendi
                    levhasının İÇİNDE durması çakışma sayılmaz). Kurul tur 2: SA1-Y2 ("1.500" × "EVLİLİK ÇEYİZİ"), SA1-Y3/AN2-Ö2 (GIOVANNI × COSSA).
UYARI: duzeltildi (levha istenen yerinden kıstırıldı → sahne dosyasında nominal konum düzeltilmeli), altyazi_seridi (y 938–1042),
       (--yazi) serbest yazı kenar/HUD/altyazı, metin levhadan taşıyor.
"ONCE" sütunu: aynı levhaların ESKİ kuralla (sabit w, kıskaçsız, eski HUD 1480–1900×10–118) ne olacağı — önce/sonra kıyası için.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import cilt_medici as CM  # noqa: E402
import compose  # noqa: E402
import sk  # noqa: E402

LEGACY_HUD = (1480.0, 10.0, 1900.0, 118.0)
TOL = 0.75


def inside(b, s, tol=TOL):
    return b[0] >= s[0] - tol and b[1] >= s[1] - tol and b[2] <= s[2] + tol and b[3] <= s[3] + tol


def hits(a, b, g=0.0):
    return a[2] > b[0] - g and a[0] < b[2] + g and a[3] > b[1] - g and a[1] < b[3] + g


def legacy_box(e):
    """Eski kural: ww = w (verildiyse) ya da max(wn+110, 460); kıskaç yok; isim fit_size(…,50,780)."""
    req = e["req"]
    cxm = (req[0] + req[2]) / 2
    sc = (req[2] - req[0]) / max(1e-6, e["ww"])            # kamera ölçeği (ekran px / yerel px)
    wn_old = sk.text_width(e["text"], "title_m", CM.fit_size(e["text"], "title_m", 50, 780, 5), 5)
    ww_old = float(e["w_req"]) if e["w_req"] else max(wn_old + 110, 460)
    hh_old = 104 + (40 if e.get("role") else 0) + (34 if e.get("dates") else 0)
    top = req[1]
    return (cxm - ww_old * sc / 2, top, cxm + ww_old * sc / 2, top + hh_old * sc), wn_old, ww_old


_MISSING_WORDS = []


def make_program(part, timeline=None, lenient=True):
    """compose.Program(part=…) kur. timeline: None (parçanın güncel çizelgesi) | dosya yolu (ör. ses_ham/yama_p1/timeline_v1.json — kurulun gördüğü sürüm).
    lenient: sahne dosyasındaki bir SÖZCÜK çapası güncel çizelgede yoksa (ses yaması sonrası sahneler henüz güncellenmemişse) cümle başına düşülür
    ve _MISSING_WORDS'e yazılır (yalnız bu süreçte; dosyalara dokunulmaz)."""
    import shots as SH
    if timeline:
        tl = SH.Timeline(timeline)
        compose._use_part_timeline = lambda p_: setattr(SH, "TL", tl)      # yalnız bu süreç: parça çizelgesi yerine verilen dosya
        SH.TL = tl
    try:
        return compose.Program(part=part)
    except (KeyError, AssertionError) as e:
        if not lenient:
            raise
        print(f"[uyarı] çekim listesi kurulamadı ({e}); eksik sözcük çapaları cümle başına, ters sıralı çekim sınırları en az 0,05 sn'ye "
              f"düşürülerek devam ediliyor (yalnız bu denetim süreci)", file=sys.stderr)
    orig_add = compose.Program._add

    def _add(self, s, t0, t1):
        if t1 <= t0:
            _MISSING_WORDS.append((f"sira:{getattr(s, 'label', '')}", f"{t0:.2f}>{t1:.2f}"))
            t1 = t0 + 0.05
        return orig_add(self, s, t0, t1)
    compose.Program._add = _add
    orig = SH.Timeline.word

    def word(self, sid, key=None, nth=0, end=False):
        try:
            return orig(self, sid, key, nth, end)
        except KeyError:
            _MISSING_WORDS.append((sid, key))
            return self.t1(sid) if end else self.t0(sid)
    SH.Timeline.word = word
    return compose.Program(part=part)


def sample_times(s, k):
    d = s.t1 - s.t0
    if k == 1:
        return [s.t0 + d * 0.6]
    fr = [0.30 + (0.92 - 0.30) * i / (k - 1) for i in range(k)]
    return [s.t0 + d * u for u in fr]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=1)
    ap.add_argument("-k", "--kare", type=int, default=3, help="çekim başına kare")
    ap.add_argument("--yazi", action="store_true", help="serbest yazı kutularını da denetle (uyarı)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--shots", default="", help="yalnız bu çekim indisleri (virgüllü)")
    ap.add_argument("--timeline", default=None, help="zaman çizelgesi dosyası (varsayılan: parçanın güncel çizelgesi)")
    a = ap.parse_args()
    out = a.out or os.path.join(HERE, f"out_p{a.part}", "duzeltme", "ENG-A", "qa_yerlesim.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prog = make_program(a.part, a.timeline)
    only = {int(x) for x in a.shots.split(",") if x.strip()}
    CM.LOG_PLATES = True
    CM.LOG_TEXT = True                      # çakışma denetimi her zaman yazı kutularına bakar; --yazi yalnız ek UYARILARI açar
    S = CM.SAFE_RECT
    HR = CM.hud_rect()
    HG = CM.hud_gap()
    sub = CM.SUB_BAND
    plates, texts, frames = [], [], 0
    t_start = time.time()
    for s in prog.shots:
        if only and s.i not in only:
            continue
        if s.kind in ("outro", "black"):
            continue
        for g in sample_times(s, a.kare):
            n = int(round((g - prog.t_off) * sk.FPS))
            if n < 0 or g >= prog.shots[-1].t1:
                continue
            CM.PLATE_LOG.clear()
            CM.TEXT_LOG.clear()
            prog.frame(n, post=False)
            frames += 1
            hud_on = s.kind not in compose.HUD_SKIP
            for e in CM.PLATE_LOG:
                e = dict(e)
                e["frame"], e["g_frame"], e["hud_on"] = n, round(g, 3), hud_on and e.get("kind") not in compose.HUD_SKIP
                plates.append(e)
            for e in CM.TEXT_LOG:
                e = dict(e)
                e["frame"], e["hud_on"] = n, hud_on and e.get("kind") not in compose.HUD_SKIP
                texts.append(e)
    dt = time.time() - t_start
    CM.LOG_PLATES = CM.LOG_TEXT = False

    viol, warn, before = [], [], []
    seen = set()
    for e in plates:
        if not e.get("main", True):
            continue
        key = (e["shot"], e["text"], e["frame"])
        if key in seen:
            continue
        seen.add(key)
        b = e["box"]
        sc = (b[2] - b[0]) / max(1e-6, e["ww"] * e["k"]) if e["ww"] else 1.0
        base = dict(cekim=e["shot"], etiket=e["label"], tur=e["kind"], sn=e["g_frame"], kare=e["frame"], metin=e["text"], kutu=[round(v) for v in b])
        # levha içi sığma (yerel px; ad: her yan ≥16 px, alt satırlar: ≥12 px)
        pad_n = (e["ww"] - e["wn"]) / 2
        pad_r = (e["ww"] - e["wr"]) / 2 if e.get("role") else 99
        pad_d = (e["ww"] - e["wd"]) / 2 if e.get("dates") else 99
        if pad_n < 16 or pad_r < 12 or pad_d < 12:
            viol.append(dict(base, tip="metin_tasmasi", ayrinti=f"iç pay ad {pad_n:.0f} / rol {pad_r:.0f} / yıl {pad_d:.0f} px"))
        if not inside(b, S):
            viol.append(dict(base, tip="kenar", ayrinti=f"güvenli alan {S}"))
        if e["hud_on"] and hits(b, HR, HG - TOL):
            viol.append(dict(base, tip="hud", ayrinti=f"HUD {tuple(round(v) for v in HR)} + {HG:.0f} px"))
        if b[3] > sub[0] and b[1] < sub[1]:
            warn.append(dict(base, tip="altyazi_seridi"))
        mv = e["moved"]
        if abs(mv[0]) > 0.5 or abs(mv[1]) > 0.5 or e["k"] < 0.999:
            warn.append(dict(base, tip="duzeltildi", ayrinti=f"istenen {[round(v) for v in e['req']]} → kaydırma ({mv[0]:+.0f},{mv[1]:+.0f}) ölçek {e['k']:.2f}"
                                                         + (f" · w={e['w_req']} → {e['ww']:.0f}" if e["w_req"] and e["ww"] > float(e["w_req"]) + 0.5 else "")))
        elif e["w_req"] and e["ww"] > float(e["w_req"]) + 0.5:
            warn.append(dict(base, tip="duzeltildi", ayrinti=f"w={e['w_req']} metne dar → {e['ww']:.0f}"))
        # ÖNCE (eski kural)
        lb, wn_old, ww_old = legacy_box(e)
        bad = []
        if wn_old + 16 > ww_old:
            bad.append("metin_tasmasi")
        if not inside(lb, S):
            bad.append("kenar")
        if e["hud_on"] and hits(lb, LEGACY_HUD, 0.0):
            bad.append("hud")
        if bad:
            before.append(dict(base, kutu=[round(v) for v in lb], tip="+".join(bad)))

    # ── çakışma (İHLAL): aynı karede levha × levha, levha × etiket zemini, zemin × zemin, yazı × yazı/sayı (kısmi kesişim) ──
    def _area(b):
        return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])

    def _inter(p_, q_):
        return max(0.0, min(p_[2], q_[2]) - max(p_[0], q_[0])) * max(0.0, min(p_[3], q_[3]) - max(p_[1], q_[1]))

    def _onscreen(b):
        return b[2] > 0 and b[0] < 1920 and b[3] > 0 and b[1] < 1080
    by_frame = {}
    seen_p = set()
    for e in plates:
        if not e.get("main", True):
            continue
        k_ = (e["shot"], e["text"], e["frame"])
        if k_ in seen_p:
            continue
        seen_p.add(k_)
        by_frame.setdefault(e["frame"], []).append(dict(sinif="levha", metin=e["text"], kutu=tuple(e["box"]), cekim=e["shot"], etiket=e["label"], sn=e["g_frame"]))
    for e in texts:
        if not e.get("main", True) or e["type"] not in ("tablet", "ink", "kick", "sayi"):
            continue
        if e["type"] != "tablet" and not e.get("text"):
            continue
        sinif = "zemin" if e["type"] == "tablet" else "yazi"
        by_frame.setdefault(e["frame"], []).append(dict(sinif=sinif, metin=e.get("text") or "(zemin)", kutu=tuple(e["box"]), cekim=e["shot"], etiket=e["label"], sn=e["g"]))
    cak_seen = set()
    for fr_, els in by_frame.items():
        els = [x for x in els if _onscreen(x["kutu"]) and _area(x["kutu"]) > 1.0]
        for i in range(len(els)):
            for j in range(i + 1, len(els)):
                A, B = els[i], els[j]
                pa, pb = A["kutu"], B["kutu"]
                ov = _inter(pa, pb)
                if ov <= 0:
                    continue
                kutular = {A["sinif"], B["sinif"]}
                if kutular <= {"levha", "zemin"}:
                    if inside(pa, pb, 2.0) or inside(pb, pa, 2.0):
                        continue                                   # iç içe zemin (aynı öğenin katmanları)
                    if ov < 0.04 * min(_area(pa), _area(pb)):
                        continue                                   # gölge/çerçeve teması
                elif "yazi" in kutular and kutular != {"yazi"}:
                    Y_, Z_ = (A, B) if A["sinif"] == "yazi" else (B, A)
                    if inside(Y_["kutu"], Z_["kutu"], 6.0):
                        continue                                   # yazı kendi levhasının/zemininin içinde
                    if _inter(Y_["kutu"], Z_["kutu"]) < 0.12 * _area(Y_["kutu"]):
                        continue
                else:                                              # yazı × yazı
                    if A["metin"] == B["metin"]:
                        continue
                    if ov < 0.12 * min(_area(pa), _area(pb)):
                        continue
                key = (A["cekim"], A["metin"], B["metin"])
                if key in cak_seen:
                    continue
                cak_seen.add(key)
                viol.append(dict(cekim=A["cekim"], etiket=A["etiket"], tur=f"{A['sinif']}×{B['sinif']}", sn=A["sn"], kare=fr_, metin=f"{A['metin']} × {B['metin']}",
                                 kutu=[round(v) for v in pa], tip="cakisma", ayrinti=f"öteki {[round(v) for v in pb]} · kesişim {ov:.0f} px²"))

    twarn = []
    if a.yazi:
        tabs = [e for e in texts if e["type"] == "tablet" and e.get("main", True)]
        seen_t = set()
        for e in texts:
            if e["type"] != "ink" or not e.get("main", True) or not e.get("text"):
                continue
            key = (e["shot"], e["text"])
            if key in seen_t:
                continue
            b = e["box"]
            base = dict(cekim=e["shot"], etiket=e["label"], sn=e["g"], metin=e["text"], kutu=[round(v) for v in b], boy=e["size"])
            n0 = len(twarn)
            if b[2] < 0 or b[0] > 1920 or b[3] < 0 or b[1] > 1080:
                continue                                      # tamamen kadraj dışı (kamera geçişi) — görünmüyor
            if not inside(b, S, 2.0):
                twarn.append(dict(base, tip="yazi_kenar"))
            if e["hud_on"] and hits(b, HR, 0.0) and not inside(b, HR, 2.0):         # HUD'un kendi yazıları (kutunun içinde) hariç
                twarn.append(dict(base, tip="yazi_hud"))
            if b[3] > sub[0] + 2 and b[1] < sub[1]:
                twarn.append(dict(base, tip="yazi_altyazi"))
            for tb in tabs:
                if tb["frame"] != e["frame"]:
                    continue
                B = tb["box"]
                if hits(b, B) and not inside(b, B, 1.5) and (min(b[2], B[2]) - max(b[0], B[0])) > 0.5 * (b[2] - b[0]):
                    twarn.append(dict(base, tip="metin_levhadan_tasiyor", levha=[round(v) for v in B]))
                    break
            if len(twarn) > n0:
                seen_t.add(key)                                   # aynı çekimdeki aynı yazı bir kez raporlanır

    def count(lst):
        d = {}
        for v in lst:
            d[v["tip"]] = d.get(v["tip"], 0) + 1
        return d

    res = dict(parca=a.part, zaman_cizelgesi=a.timeline or "güncel", eksik_capa=sorted({f"{x[0]}:{x[1]}" for x in _MISSING_WORDS}), kare=frames, sure_sn=round(dt, 1), levha_kaydi=len(seen), guvenli_alan=S, hud=HR, hud_pay=HG,
               ozet=dict(ihlal=len(viol), ihlal_tip=count(viol), uyari_tip=count(warn), once_ihlal=len(before), once_tip=count(before),
                         yazi_uyari_tip=count(twarn) if a.yazi else None),
               ihlaller=viol, uyarilar=warn, once=before, yazi_uyarilari=twarn if a.yazi else None)
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    o = res["ozet"]
    line = (f"qa_yerlesim P{a.part}: {frames} kare, {len(seen)} levha kaydı · İHLAL {len(viol)} {o['ihlal_tip'] or ''} · "
            f"düzeltilen {o['uyari_tip'].get('duzeltildi', 0)} · altyazı şeridi {o['uyari_tip'].get('altyazi_seridi', 0)} · "
            f"ÖNCE (eski kural) {len(before)} {o['once_tip'] or ''}")
    if a.yazi:
        line += f" · yazı uyarıları {o['yazi_uyari_tip']}"
    print(line)
    print("→", os.path.relpath(out, HERE))
    for v in viol[:20]:
        print(f"  ✗ #{v['cekim']} {v['sn']:.1f}s {v['tip']}: {v['metin']} {v['kutu']} {v.get('ayrinti', '')}")
    sys.exit(1 if viol else 0)


if __name__ == "__main__":
    main()

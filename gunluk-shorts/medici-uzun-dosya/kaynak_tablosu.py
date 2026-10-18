#!/usr/bin/env python3
"""Kaynak kapısı çıktısı: her cümle için kaynak sınıfı + dayanak; sınıf özeti; "yayın öncesi teyit" listesi.

  python3 kaynak_tablosu.py --part 1      → kaynaklar_P1.md
  python3 kaynak_tablosu.py               → kaynaklar_TUM.md

Sınıflar (Anayasa §5-1): ● birincil metin okundu (bu ortamda mümkün değil: sayfa açılamıyor) · ◐ ≥2 bağımsız ikincil kaynak (arama özeti dahil)
· ○ tek/çelişkili · ANEKDOT (rivayet; kim anlattı yazılı) · YORUM (yazar yorumu) · MİT (düzeltilen yaygın yanlış) · HAFIZA (araçla doğrulanmamış; metne girmez).
Etiket metninden sınıf çıkarılır: ilk simge/sözcük. Etiketsiz cümle "—" (bağ/kapı cümlesi) sayılır.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import script as S  # noqa: E402

ORDER = ["ANEKDOT", "MİT", "○", "◐", "YORUM", "—"]


def klass(tag: str) -> str:
    t = tag.strip()
    if not t or t == "—":
        return "—"
    for k in ("ANEKDOT", "MİT", "YORUM", "HAFIZA"):
        if t.startswith(k):
            return k
    if "ANEKDOT" in t.split("(")[0]:
        return "ANEKDOT"
    if t.startswith("○") or " / ○" in t.split("(")[0] or "◐/○" in t.split("(")[0]:
        return "○"
    if t.startswith("◐"):
        return "◐"
    return "—"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=None)
    a = ap.parse_args()
    sents = S.sentences(a.part)
    name = f"kaynaklar_P{a.part}.md" if a.part else "kaynaklar_TUM.md"
    cnt = {}
    for s in sents:
        cnt[klass(s["tag"])] = cnt.get(klass(s["tag"]), 0) + 1
    L = []
    L.append(f"# MEDICI — Kaynak kapısı {'Parça ' + str(a.part) if a.part else '(tüm bölümler)'}")
    L.append("")
    L.append("> **Sınırlama (kullanıcıya söylenir, Anayasa §5-1):** Bu ortam birincil metin açamıyor (WebFetch DNS hatası; yalnız arama özetleri). Hiçbir olgu ● değildir; video **◐ (nitelikli)** sayılır. "
             "Tarih/sayı/ad için **yayın öncesi teyit listesi** aşağıdadır. Kaynak dayanakları: `arastirma/M1…M5` ve `brif/cK_brif.md` (kimlikler etikette).")
    L.append("")
    L.append("## Özet")
    L.append("")
    L.append("| sınıf | cümle |")
    L.append("|---|---:|")
    for k in ORDER + ["HAFIZA"]:
        if k in cnt:
            L.append(f"| {k} | {cnt[k]} |")
    L.append(f"| **toplam** | **{len(sents)}** |")
    L.append("")
    if cnt.get("HAFIZA"):
        L.append("**UYARI:** HAFIZA sınıfında cümle var; metne girmemeli.")
        L.append("")
    L.append("## Yayın öncesi teyit listesi (○ · ANEKDOT · MİT düzeltmesi · kritik tarih/sayı)")
    L.append("")
    L.append("| id | sınıf | cümle (ekran metni) | dayanak / kip |")
    L.append("|---|---|---|---|")
    for s in sents:
        k = klass(s["tag"])
        if k in ("○", "ANEKDOT", "MİT", "HAFIZA") or "teyit" in s["tag"].lower() or "çelişki" in s["tag"].lower():
            L.append(f"| {s['id']} | {k} | {s['disp']} | {s['tag']} |")
    L.append("")
    L.append("## Tüm cümleler")
    L.append("")
    cur = None
    for s in sents:
        if s["ch"] != cur:
            cur = s["ch"]
            title = next(c["title"] for c in S.CHAPTERS if c["id"] == cur)
            L.append(f"### {cur} — {title}")
            L.append("")
            L.append("| id | sınıf | cümle | dayanak |")
            L.append("|---|---|---|---|")
        L.append(f"| {s['id']} | {klass(s['tag'])} | {s['disp']} | {s['tag']} |")
        # bölüm sonunda boş satır, tabloyu kapatır
        nxt = [x for x in sents if x["ch"] == cur][-1]
        if s is nxt:
            L.append("")
    out = os.path.join(HERE, name)
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(out, dict(sorted(cnt.items())))


if __name__ == "__main__":
    main()

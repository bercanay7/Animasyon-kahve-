#!/usr/bin/env python3
"""Telaffuz kapısı çıktısı: metinde geçen ve PRON ile Türkçe okunuşa çevrilen her ad/terim → okunus_P1.md.

  python3 okunus_tablosu.py --part 1

Her satır: gösterim (ekran) → ElevenLabs'e giden okunuş · geçtiği cümleler. Kulak kontrolü (Anayasa §5-2) bu listedeki sözcükler içindir;
ses üretildikten sonra Scribe dökümü ile karşılaştırılır (`ses_hizala.py`).
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import script as S  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=None)
    a = ap.parse_args()
    sents = S.sentences(a.part)
    raw = {}
    for ch in S.CHAPTERS:
        if a.part and S.PART_OF.get(ch["id"]) != a.part:
            continue
        k = 0
        for para in ch["paras"]:
            for tup in para:
                k += 1
                raw[f"{ch['id']}s{k}"] = tup[0]
    hits = {}
    for pat, rep in S.PRON:
        rx = re.compile(pat)
        for sid, text in raw.items():
            disp = S.to_display(text)
            for m in rx.finditer(disp):
                hits.setdefault((m.group(0), rep if rx.sub(rep, m.group(0)) == rep else rx.sub(rep, m.group(0))), []).append(sid)
    L = [f"# MEDICI — Okunuş listesi {'Parça ' + str(a.part) if a.part else '(tüm)'}", "",
         "Gösterim (ekran) → ElevenLabs'e giden okunuş. **Kulak kontrolü bu sözcükler için** (Scribe dökümü sonrası ayrıca karşılaştırılır).", "",
         "| gösterim | okunuş | adet | ilk geçtiği yerler |", "|---|---|---:|---|"]
    for (g, r), ids in sorted(hits.items(), key=lambda kv: (kv[1][0], kv[0][0])):
        L.append(f"| {g} | {r} | {len(ids)} | {', '.join(ids[:4])} |")
    out = os.path.join(HERE, f"okunus_P{a.part}.md" if a.part else "okunus_TUM.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(out, len(hits), "terim")


if __name__ == "__main__":
    main()

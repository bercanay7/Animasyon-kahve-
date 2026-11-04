#!/usr/bin/env python3
"""Ses yamalarının kulak kontrolü: her yamalı cümleyi önceki/sonraki cümleyle birlikte (bağlam içinde) out_p1/voice.wav'dan keser.

  MEDICI_PART=1 python3 kulak_yama.py      # yayin/kulak_kontrol_P1/yama_<cümle>.mp3 + yayin/KULAK_KONTROL_P1.md'ye bölüm ekler
Ne dinlenir: (1) ek yeri duyuluyor mu (nefes/ton/oda sesi sıçraması), (2) okunuş doğru mu, (3) seviye komşu cümlelerle aynı mı.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("MEDICI_PART", "1")
import parca as PA  # noqa: E402

YAMA = os.path.join(HERE, "ses_ham", "yama_p1")
DIR = os.path.join(HERE, "yayin", "kulak_kontrol_P1")
MD = os.path.join(HERE, "yayin", "KULAK_KONTROL_P1.md")
NOT = {
    "c1s11": "veba süresi ('yaz boyunca')",
    "c1s16": "Salvestro 'kurayla' — ASR 'Mayıs'ında' sözcüğünü 'naysinde' duydu: okunuşa özellikle bakın",
    "c1s18": "'ve Salvestro çekildi' kaldırıldı; cümle 'gonfalonyere oldu.' ile bitiyor",
    "c1s23": "'en kanlı gün' yerine lonca kaldırıldı / dışlandılar",
    "c1s24": "'Medici'nin bu kolu'",
    "c1s26": "orijinalde yutulan 'Roma'da' geri geldi",
    "c2s1": "orijinalde yutulan 'Çözüm,' geri geldi (bölüm başı)",
    "c2s7": "Tim Parks (eski: 'Treysi')",
    "c2s27": "'torununun oğlu Lorentso'",
}


def main():
    tl = json.load(open(os.path.join(PA.OUT, "timeline.json"), encoding="utf-8"))
    ss = tl["sentences"]
    idx = {s["id"]: i for i, s in enumerate(ss)}
    rapor = json.load(open(os.path.join(YAMA, "rapor.json"), encoding="utf-8"))
    os.makedirs(DIR, exist_ok=True)
    rows = []
    for sid in rapor:
        i = idx[sid]
        a = ss[i - 1]["t0"] if i > 0 and ss[i - 1]["ch"] == ss[i]["ch"] else ss[i]["t0"] - 0.6
        b = ss[i + 1]["t1"] if i + 1 < len(ss) and ss[i + 1]["ch"] == ss[i]["ch"] else ss[i]["t1"] + 0.8
        a, b = max(0.0, a - 0.3), b + 0.3
        out = os.path.join(DIR, f"yama_{sid}.mp3")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", os.path.join(PA.OUT, "voice.wav"),
                        "-ac", "1", "-b:a", "128k", out], check=True)
        mm, s_ = divmod(int(ss[i]["t0"]), 60)
        rows.append(f"| `yama_{sid}.mp3` | {mm}:{s_:02d} | {ss[i]['disp']} | {NOT.get(sid, '')} |")
    blok = ("\n\n## Kurul tur 1 ses yamaları (4 Kasım 2026) — bağlam içinde dinleyin\n\n"
            "Her klip: önceki cümle + YAMALI cümle + sonraki cümle (anlatım kanalı, müziksiz). Bakılacaklar: ek yeri (ton/nefes/oda sesi sıçraması), okunuş, seviye.\n\n"
            "| Dosya | Video zamanı | Yamalı cümle | Not |\n|---|---|---|---|\n" + "\n".join(rows) + "\n")
    old = open(MD, encoding="utf-8").read() if os.path.exists(MD) else "# Kulak kontrolü — Parça 1\n"
    k = old.find("\n\n## Kurul tur 1 ses yamaları")
    if k >= 0:
        old = old[:k]
    open(MD, "w", encoding="utf-8").write(old.rstrip("\n") + blok)
    print(f"{len(rows)} klip → {DIR}")


if __name__ == "__main__":
    main()

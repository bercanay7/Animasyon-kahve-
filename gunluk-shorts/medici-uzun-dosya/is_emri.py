#!/usr/bin/env python3
"""Sahne yazarı ajanlar için bölüm İŞ EMRİ üretici: cümleler + zaman çizelgesi + brif §3/§4/§5/§7/§10 + rehber imza sekansı.

  python3 is_emri.py c7            → isemri/c7.md
  python3 is_emri.py --hepsi       → isemri/c0.md … c16.md

Kaynaklar: script.py (metin, kaynak sınıfı), out_pN/timeline.json (cümle zamanları; geçici ya da gerçek ses), brif/cK_brif.md, YONETMENLIK_REHBERI.md.
KISIT ÖNCELİĞİ: brif §5 (tuzaklar), brif §7'deki "YOK/söylenmez/gösterilmez" notları ve scr_cK.py docstring'i, rehber §8 imza sekansından ÖNCE gelir
(örn. c7/c10: çan, saat, şafak, ışık, koku — kaynakta YOK → görüntüde de iddia edilmez).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import script as S  # noqa: E402

PERDE = {1: "ALTIN", 2: "BEDEL", 3: "MİRAS"}
CHIDS = [c["id"] for c in S.CHAPTERS]


def read(path):
    return open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def section(md, num):
    m = re.search(rf"^## {num}\.[^\n]*\n(.*?)(?=^## \d+\.|\Z)", md, re.S | re.M)
    return (m.group(0).rstrip() if m else f"(brif §{num} bulunamadı)")


def rehber_row(cid):
    for ln in read(os.path.join(HERE, "YONETMENLIK_REHBERI.md")).splitlines():
        if ln.startswith(f"| {cid} |"):
            return ln
    return "(rehber §8'de satır yok)"


def timeline(part):
    p = os.path.join(HERE, f"out_p{part}", "timeline.json")
    if not os.path.exists(p):
        return None, None
    tl = json.load(open(p, encoding="utf-8"))
    scratch = os.path.exists(os.path.join(HERE, f"out_p{part}", "GECICI_SES.json"))
    return tl, scratch


def build(cid):
    ch = next(c for c in S.CHAPTERS if c["id"] == cid)
    part = S.PART_OF[cid]
    idx = CHIDS.index(cid)
    prev = S.CHAPTERS[idx - 1] if idx > 0 else None
    nxt = S.CHAPTERS[idx + 1] if idx + 1 < len(S.CHAPTERS) else None
    brief = read(os.path.join(HERE, "brif", f"{cid}_brif.md"))
    tl, scratch = timeline(part)
    sents = [s for s in (tl["sentences"] if tl else []) if s["ch"] == cid]
    first_in_part = S.PARTS[part][0] == cid
    last_in_part = S.PARTS[part][-1] == cid
    L = []
    L.append(f"# İŞ EMRİ — {cid} · {ch['title']} ({ch['years']}) · PARÇA {part} · PERDE {PERDE[part]}")
    L.append("")
    dur = (sents[-1]["t1"] - sents[0]["t0"]) if sents else 0
    L.append(f"- **Ruh hâli (script):** `{ch.get('mood')}` · **Sıra:** bölüm {idx + 1}/{len(CHIDS)}; parça içinde {S.PARTS[part].index(cid) + 1}/{len(S.PARTS[part])}"
             + (" · **PARÇA AÇILIŞI** (kart ayrı değil; ilk çekimde başlık bindirmesi; 'önceki bölümde' bandı YOK)" if first_in_part and part > 1 else "")
             + (" · **PARÇA KAPANIŞI** (bitiş ekranı: " + ("ABONE OL + TÜM FİLM" if part == 3 else "SIRADAKİ PARÇA + ABONE OL") + ")" if last_in_part else ""))
    L.append(f"- **Süre:** {dur:.0f} sn ({len(sents)} cümle) — ses: **{'GEÇİCİ (Piper; gerçek ElevenLabs sesi gelince zamanlar DEĞİŞİR → sahneleri cümle/sözcük ÇAPALARINA bağla, mutlak saniyeye değil)' if scratch else 'gerçek (ElevenLabs)'}**" if sents else "- **Süre:** timeline yok")
    if prev:
        pl = prev["paras"][-1][-1][0]
        L.append(f"- **Önceki bölümün (c{int(cid[1:]) - 1}) son cümlesi (kapı):** «{pl}»")
    last_two = [t[0] for t in ch["paras"][-1]][-2:]
    L.append(f"- **Bu bölümün kapısı (son cümleler):** «{' '.join(last_two)}»" + (f" → sonraki: c{int(cid[1:]) + 1} «{nxt['title']}»" if nxt else " → FİLMİN SONU"))
    L.append("")
    L.append("## 0. Kurallar (özet; ayrıntı: YONETMENLIK_REHBERI.md, STIL_REHBERI.md)")
    L.append("- **Kısıt önceliği:** brif §5 (tuzaklar) + §7 'YOK/söylenmez/gösterilmez' notları + scr_cK.py docstring > rehber §8 imza sekansı. Kaynakta olmayan saat/hava/ışık/çan/koku/yüz/ses **görüntüde de iddia edilmez**.")
    L.append("- Ağır sahnede (mizah KAPALI) şiddet **gösterilmez** (siluet, işaret, pigment yıkama); asılı beden, kan, ceset yok. Gerçek kişi yüzü iddiası yok (madalya silueti/stilize).")
    L.append("- Her cümlenin ≥1 görsel olayı (çapa) olsun (≥%95); statik tutuş ≤1,5 sn; geçişlerin ≥%70'i gerekçeli (`link=`); çıplak `fade` ≤%10; altyazı bölgesi y≈1250–1390 BOŞ.")
    L.append("- Telif: Leonardo/Botticelli/Rubens/Gozzoli görselleri birebir kopyalanmaz — kodla yeniden çizilen temsil.")
    L.append("- c0'daki 'Hiçbir şey buradan çıkmayacak' alıntı kartı **Anna Maria Luisa'ya atfedilmez**; 'Sözleşmenin 3. maddesinin özeti' olarak yazılır (c16 bunu söyler).")
    L.append("")
    L.append("## 1. Cümleler ve zamanlar")
    L.append("")
    L.append("| id | t0 | t1 | sn | sınıf · dayanak | metin |")
    L.append("|---|---:|---:|---:|---|---|")
    tag_of = {}
    k = 0
    for para in ch["paras"]:
        for tup in para:
            k += 1
            tag_of[f"{cid}s{k}"] = tup[2] if len(tup) > 2 else ""
    for s in sents:
        tag = tag_of.get(s["id"], "").replace("|", "/")
        L.append(f"| {s['id']} | {s['t0']:.1f} | {s['t1']:.1f} | {s['t1'] - s['t0']:.1f} | {tag[:90]} | {s['disp']} |")
    if not sents:
        for sid, tag in tag_of.items():
            L.append(f"| {sid} | – | – | – | {tag[:90].replace('|', '/')} | |")
    L.append("")
    L.append("## 2. Brif §7 — Ekran önerileri (+ akış notları varsa)")
    L.append(section(brief, 7).split("\n", 1)[1] if section(brief, 7).count("\n") else section(brief, 7))
    L.append("")
    L.append("## 3. Rehber §8 — bu bölümün imza sekans önerisi (yukarıdaki kısıtlarla çelişirse brif kazanır)")
    L.append(rehber_row(cid))
    L.append("")
    L.append("## 4. Brif §3 — Mizah çıpaları")
    L.append(section(brief, 3).split("\n", 1)[1] if "\n" in section(brief, 3) else section(brief, 3))
    L.append("")
    L.append("## 5. Brif §4 — Sayı bütçesi (ekran kartı listesi dahil)")
    L.append(section(brief, 4).split("\n", 1)[1] if "\n" in section(brief, 4) else section(brief, 4))
    L.append("")
    L.append("## 6. Brif §5 — Tuzaklar (görüntüde de geçerli)")
    L.append(section(brief, 5).split("\n", 1)[1] if "\n" in section(brief, 5) else section(brief, 5))
    L.append("")
    L.append("## 7. Brif §10 — Eksikler (görüntüye de GİRMEZ)")
    L.append(section(brief, 10).split("\n", 1)[1] if "\n" in section(brief, 10) else section(brief, 10))
    L.append("")
    L.append("## 8. Teslim")
    L.append(f"- `scenes_{cid}.py` (STIL_REHBERI sözleşmesi) + `yonetmen_{cid}.md` (rehber §11 kartı: kamera/geçiş/link tablosu, imza sekans, müzik/ses notu, iki 'neden böyle?' gerekçesi).")
    L.append(f"- Doğrulama: `python3 preview_cilt.py {cid}` / `python3 preview_reel.py {cid}` ve `python3 qa_flow.py {cid}` (komutlar STIL_REHBERI'nde); kontak sayfası + kapılar yeşil olmadan teslim etme.")
    L.append("- Geçici ses uyarısı: sahne süreleri değişecek; her çekim çapası cümle/sözcük kimliğiyle bağlı olmalı (qa_flow ≥%90 çapa şartı).")
    return "\n".join(L) + "\n"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ids = CHIDS if "--hepsi" in sys.argv else args
    if not ids:
        raise SystemExit(__doc__)
    os.makedirs(os.path.join(HERE, "isemri"), exist_ok=True)
    for cid in ids:
        out = os.path.join(HERE, "isemri", f"{cid}.md")
        open(out, "w", encoding="utf-8").write(build(cid))
        print(out, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    main()

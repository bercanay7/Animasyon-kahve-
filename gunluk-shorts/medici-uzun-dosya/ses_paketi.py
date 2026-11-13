#!/usr/bin/env python3
"""ElevenLabs paketi: bölüm başına gönderilecek TAM metin (ses_paketi/cN.txt) + manifest (karakter/kredi/özet/sürüm).

  python3 ses_paketi.py                 # tüm bölümler için metin dosyalarını ve manifest'i yazar (ses_paketi/)
  python3 ses_paketi.py --kontrol       # gerçek sesi (ses_ham/cN_v1.mp3) olan bölümlerde metin değişti mi? (özet karşılaştırma)
  python3 ses_paketi.py --onayla c0 c1 c2 c3 c4 c5   # bu bölümlerin ŞU ANKİ metnini "üretilen metin" olarak kaydet (ses_paketi/uretilen.json)

Neden: ses üretildikten sonra senaryoda bir virgül bile değişirse hizalama/altyazı kayar. `--kontrol` bunu erken yakalar; değişen bölüm için ya
metin eski haline döner ya da yalnız o cümle `ses_yama.py` ile yamanır (tüm bölümü yeniden üretmek yerine).
Maliyet: 1 karakter ≈ 1 kredi (≈ $0,0002); ses üretimi `generations_count=1` (kural: tekrar üretme ücretlidir).
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import script as S  # noqa: E402

PK = os.path.join(HERE, "ses_paketi")
RAW = os.path.join(HERE, "ses_ham")
USD_PER_CREDIT = 0.0002


def chapter_text(cid):
    return S.chapter_text(cid)


def digest(t):
    return hashlib.sha1(t.encode("utf-8")).hexdigest()[:12]


def main():
    os.makedirs(PK, exist_ok=True)
    made_path = os.path.join(PK, "uretilen.json")
    made = json.load(open(made_path)) if os.path.exists(made_path) else {}
    if "--onayla" in sys.argv:
        ids = [a for a in sys.argv[1:] if a.startswith("c")]
        for cid in ids:
            made[cid] = dict(sha=digest(chapter_text(cid)), chars=len(chapter_text(cid)))
        json.dump(made, open(made_path, "w"), indent=1)
        print("kaydedildi:", ids)
        return
    man = []
    tot = 0
    for ch in S.CHAPTERS:
        cid = ch["id"]
        t = chapter_text(cid)
        open(os.path.join(PK, f"{cid}.txt"), "w", encoding="utf-8").write(t + "\n")
        has = os.path.exists(os.path.join(RAW, f"{cid}_v1.mp3"))
        man.append(dict(id=cid, part=S.PART_OF[cid], chars=len(t), words=len(t.split()), credits=len(t), usd=round(len(t) * USD_PER_CREDIT, 2),
                        sha=digest(t), gercek_ses=has, uretilen_sha=made.get(cid, {}).get("sha")))
        tot += len(t) if not has else 0
    json.dump(man, open(os.path.join(PK, "manifest.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{'id':4s} {'P':1s} {'kar.':>6s} {'söz':>5s} {'$':>6s}  durum")
    bad = 0
    for m in man:
        st = "gerçek ses VAR" if m["gercek_ses"] else "üretilecek"
        if m["gercek_ses"]:
            if m["uretilen_sha"] is None:
                st += " — üretilen metin kaydı YOK (--onayla)"
            elif m["uretilen_sha"] != m["sha"]:
                st += " — !!! METİN DEĞİŞTİ (üretilenle uyuşmuyor)"
                bad += 1
        print(f"{m['id']:4s} {m['part']:1d} {m['chars']:6d} {m['words']:5d} {m['usd']:6.2f}  {st}")
    todo = sum(m["credits"] for m in man if not m["gercek_ses"])
    print(f"ÜRETİLECEK toplam: {todo} kredi ≈ ${todo * USD_PER_CREDIT:.2f} · tüm film: {sum(m['credits'] for m in man)} kredi ≈ ${sum(m['credits'] for m in man) * USD_PER_CREDIT:.2f}")
    if "--kontrol" in sys.argv and bad:
        raise SystemExit(f"{bad} bölümde metin değişmiş")


if __name__ == "__main__":
    main()

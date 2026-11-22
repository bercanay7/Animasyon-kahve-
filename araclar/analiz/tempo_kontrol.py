#!/usr/bin/env python3
"""Senaryo tempo kontrolü: yayın sonrası analizlerden çıkan dersleri senaryoda arar.

Kullanım:
  python3 tempo_kontrol.py PROJE/senaryo.json [PROJE/timeline.js] [--yazar "Kurosawa,Shakespeare"] [--md cikti.md]

timeline.js verilirse cümleler yayındaki sırayla ve zamanlarıyla dizilir (seslendirmeden önce verilmez).

İşaretler (aday listesidir; karar başkanındır, her işaretli cümleye "olay" ya da "soyut" yazılır):
  K  köprü: kanca bölümünde son sorudan sonra gelen cümleler. Kural: kanca sorusundan sonraki
     ilk cümle hikâyenin ilk cümlesidir; yalnız kimlik bilgisi (ad, yıl) tek cümle olabilir.
  M  soyut aday: karşılaştırma/çıkarım sözcüğü var ("göre", "fark", "tıpkı", "-de de", "eklediği", "asıl"…).
     Kural: somut olay tutar, soyut çözümleme düşürür; art arda iki soyut cümle olmaz.
     Ölçülen (Mary Stuart M2): "göre" sözcüğü değil, olaydan kopuk açıklama kaybettirir; yazarın somut bir karar
     hakkındaki yargısı tutar. Başkan her M'ye "olaya bağlı mı?" diye bakar.
  E  erken soyut: ilk iki dakikadaki M (timeline yoksa ilk ~1.480 karakter). En pahalı kayıp burada
     (Mary Stuart 1:12–1:36 arma ve meşruiyet: 24 sn'de −11). Arka plan gerekiyorsa nesne ya da sahneyle verilir.
  Y  yazar/yaratıcı anılıyor (--yazar), karşılaştırma sözcüğü yok. Kendi başına sorun değil:
     Ran'da "Kurosawa kaleyi inşa ettirdi, sonra yaktı" en iyi tutan yerdi. Başkan "olay mı, yorum mu" diye bakar.
  T  merak sorusu: cevabı bir OLAY olan cümle numarası yazılır, kavram değil.
  A  yeni ad: sürenin (ya da cümlelerin) ilk yarısından sonra ilk kez geçen özel ad.
     İpucu: doruğu taşıyacak kişiler ilk perdede adı ve görüntüsüyle ekilir.

Kaynak dersler: CLAUDE.md "Ran dersleri → Yayın sonrası dersler"; analiz/2026-11-19-ran-48saat.md;
analiz/2026-11-22-mary-stuart-45saat.md; analiz/2026-11-22-genel-karsilastirma.md.
"""
import json, re, sys

KARSILASTIRMA = re.compile(
    r"\b(tıpkı|göre|fark\w*|aksine|oysa|yani|demek|aslında|anlam\w*|simge\w*|sembol\w*|"
    r"temsil\w*|okuma\w*|yorum\w*|kavram\w*|eklediği|ekledi|vermez|vermediği|çok daha|asıl|gözünde|meşru\w*)\b"
    r"|'[dt][ae] de\b|'[dt][ae] da\b", re.I)
MERAK = re.compile(r"\?|bir şey\b|sona sakl|göreceğiz|nedenini|asıl soru|peki\b", re.I)
AD = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])([A-ZÇĞİÖŞÜ][a-zçğıöşüâîûōū]+(?:\s[A-ZÇĞİÖŞÜ][a-zçğıöşüâîûōū]+)?)")
YAYGIN = set("""Bir Bu Ve Ama Peki Sonra Onu Ona Onun Bunu Şimdi Kimse Neden Yine Çünkü İşte Hiçbir
Yıllar Yıl Ya Hem Sen Ben Biz Siz O Orada Burada Asıl Belki Hayır Evet Bugün Dün Ne Kim Hangi Nasıl
Her Hep Daha En Bütün Tek Üç İki Beş Altı Aynı Böyle Öyle Oysa Yani Ayrıca Üstelik Artık Hâlâ Sadece Yalnız
Ilk İlk Son Fransız İngiliz Japon Türk Yunan Romalı Latince Japonca Türkçe Kendi Kendini Gece Sabah Akşam Bunun Bunlar Onlar Şöyle Şu Dostları Kızına Kızı Annesi Babası""".split())

def kok(ad):
    return ad.split("'")[0].split("’")[0]

def yukle(senaryo, timeline=None):
    S = json.load(open(senaryo, encoding="utf-8"))
    not_ = ""
    if isinstance(S, dict):
        not_ = S.get("not", ""); S = S.get("segments", [])
    rows = [dict(id=x["id"], bolum=x.get("bolum", ""), alt=x.get("alt") or x.get("tts", ""), s=None, sec=None) for x in S]
    if timeline:
        t = open(timeline, encoding="utf-8").read()
        i0 = t.index("window.CUES"); i0 = t.index("{", i0)
        cues, _ = json.JSONDecoder().raw_decode(t[i0:])
        by = {r["id"]: r for r in rows}
        rows = []
        for k, v in sorted(cues.items(), key=lambda kv: kv[1]["s"]):
            if k in by:
                r = by[k]; r["s"] = v["s"]; r["sec"] = v.get("sec"); rows.append(r)
    for i, r in enumerate(rows):
        if r["sec"] is None:
            r["sec"] = r["bolum"]
    return rows, not_

def zaman(s):
    return "" if s is None else f"{int(s // 60)}:{int(s % 60):02d}"

def tara(rows, yazarlar):
    n = len(rows)
    toplam = rows[-1]["s"] if rows and rows[-1]["s"] is not None else None
    ilk_sec = rows[0]["sec"]
    kanca = [i for i, r in enumerate(rows) if r["sec"] == ilk_sec]
    son_soru = max([i for i in kanca if "?" in rows[i]["alt"]], default=None)
    gorulen = {}
    ortada = set()
    kar = 0   # timeline yoksa erken bölge karakterle (≈12,3 harf/sn × 120 sn)
    for r in rows:
        for m in AD.finditer(r["alt"]):
            onc = r["alt"][:m.start()].rstrip()[-1:]
            if m.start() > 0 and onc not in ".:!?…\"“":
                ortada.add(kok(m.group(1)))
    for i, r in enumerate(rows):
        b = []
        metin = r["alt"]
        if son_soru is not None and i in kanca and i > son_soru:
            b.append("K")
        yazar_var = any(re.search(r"\b" + re.escape(y), metin) for y in yazarlar)
        erken = (r["s"] < 120) if r["s"] is not None else (kar < 1480)
        kar += len(metin)
        if KARSILASTIRMA.search(metin):
            b.append("M")
            if erken: b.append("E")
        elif yazar_var:
            b.append("Y")
        if MERAK.search(metin) and i > 0:
            b.append("T")
        yari = (r["s"] is not None and toplam and r["s"] > toplam / 2) or (r["s"] is None and i > n / 2)
        yeni = []
        for m in AD.finditer(metin):
            a = kok(m.group(1))
            if a.split()[0] in YAYGIN:
                continue
            bas = m.start() == 0 or metin[:m.start()].rstrip()[-1:] in ".:!?…\"“"
            if bas and a not in ortada:
                continue  # cümle başındaki sıradan sözcük; ad başka yerde cümle ortasında da geçmeli
            if a not in gorulen:
                gorulen[a] = i
                if yari:
                    yeni.append(a)
        if yeni:
            b.append("A")
        r["bayrak"] = b; r["yeni"] = yeni
    return rows

def rapor(rows, md=None):
    out = []
    p = out.append
    p("| zaman | id | bayrak | cümle | karar |")
    p("|---|---|---|---|---|")
    for r in rows:
        if not r["bayrak"]:
            continue
        ek = f" (yeni ad: {', '.join(r['yeni'])})" if r["yeni"] else ""
        p(f"| {zaman(r['s'])} | {r['id']} | {''.join(r['bayrak'])} | {r['alt']}{ek} | |")
    # art arda M dizileri (Y sayılmaz)
    diz, cur = [], []
    for r in rows:
        if "M" in r["bayrak"]:
            cur.append(r)
        else:
            if len(cur) >= 2: diz.append(cur)
            cur = []
    if len(cur) >= 2: diz.append(cur)
    p("")
    p("Art arda soyut aday dizileri (≥2): " + ("; ".join(f"{d[0]['id']}–{d[-1]['id']} ({zaman(d[0]['s'])})" for d in diz) or "yok"))
    e = [f"{r['id']} ({zaman(r['s'])})" if r['s'] is not None else r['id'] for r in rows if "E" in r["bayrak"]]
    p("İlk iki dakikada soyut adaylar (en pahalı kayıp): " + (", ".join(e) or "yok"))
    k = [r["id"] for r in rows if "K" in r["bayrak"]]
    p("Köprü adayları (kanca sorusundan sonra, kanca bölümünde): " + (", ".join(k) or "yok"))
    a = [f"{r['id']} {','.join(r['yeni'])}" for r in rows if r["yeni"]]
    p("İkinci yarıda ilk kez geçen adlar: " + ("; ".join(a) or "yok"))
    s = "\n".join(out)
    print(s)
    if md:
        open(md, "w", encoding="utf-8").write(s + "\n")

def main():
    a = sys.argv[1:]
    yaz = []
    md = None
    if "--yazar" in a:
        i = a.index("--yazar"); yaz = [x.strip() for x in a[i + 1].split(",") if x.strip()]; del a[i:i + 2]
    if "--md" in a:
        i = a.index("--md"); md = a[i + 1]; del a[i:i + 2]
    rows, _ = yukle(a[0], a[1] if len(a) > 1 else None)
    rapor(tara(rows, yaz), md)

if __name__ == "__main__":
    main()

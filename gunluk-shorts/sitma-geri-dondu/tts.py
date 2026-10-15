"""Sıtma Geri Döndü — anlatıcı: ses-lab/narrator.py (Piper dfki + stüdyo işleme). Çıktı: out/voice.wav, out/timeline.json
Metin işareti: gösterilen=söylenen   *vurgulu*   Kullanım: python3 tts.py [--voice=dfki|fahrettin|fettah]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator

VOICE = "dfki"
PROF = dict(speed=1.12, reverb_wet=0.0)   # anayasa: kuru erkek ses (yankı 0)
for a in sys.argv[1:]:
    if a == "--kadin":   # kadın sesi (WORLD dönüşümü) + kuru ses (yankısız)
        PROF.update(f0_scale=1.55, formant=1.14)
    if a.startswith("--voice="):
        VOICE = a.split("=")[1]

# (id, metin, hız, enerji, sonraki boşluk)
SENTENCES = [
    ("A", "Türkiye’de=Türkiyede sıtma *neredeyse bitmişti.* Sonra *geri döndü!*", 1.04, 1.2, 0.18),
    ("B", "Yıllarca *kinin dağıtıldı, bataklıklar kurutuldu.*", 1.02, 1.0, 0.14),
    ("C", "Yıllık vaka sayısı *1.263’e=bin_iki_yüz_altmış_üçe düştü.*", 1.02, 1.05, 0.14),
    ("D", "Birkaç yıl sonra *115.000’i=yüz_on_beş_bini aştı!*", 1.04, 1.2, 0.20),
    ("E", "Neden? Uzmanlara göre, *faktörler üst üste bindi.*", 1.04, 1.1, 0.14),
    ("F", "Önce, *sulu tarım yayıldı.* Sivrisinek sayısı *keskin arttı.*", 1.06, 1.15, 0.12),
    ("G", "Sonra, *işçi göçü* hastalığı *yeni bölgelere taşıdı.*", 1.06, 1.15, 0.12),
    ("H", "Üstelik, *izleme zayıftı.*", 1.06, 1.15, 0.18),
    ("I", "Mücadele *yeniden başlayınca* salgın geriledi.", 1.04, 1.0, 0.18),
    ("J", "Ama sıtma *tekrar patladı:* *84.000’i=seksen_dört_bini aştı!*", 1.02, 1.2, 0.20),
    ("K", "Bugün, Sağlık Bakanlığı’na=Bakanlığına göre, *yerli vaka yok.* İthal=ithhal vakalar sürüyor.", 1.04, 1.0, 0.18),
    ("L", "Ders şu: *bitti diye bırakırsan,* hastalık döner.", 0.96, 0.95, 0.0),
]

if __name__ == "__main__":
    lex = os.path.join(HERE, "..", "ses-lab", "lex.json")
    if os.path.exists(lex):
        narrator.LEX.update(json.load(open(lex)))
    T, tot, _ = narrator.render(SENTENCES, os.path.join(HERE, "out"), voice=VOICE, profile=PROF, tail=0.95)
    tl = json.load(open(os.path.join(HERE, "out", "timeline.json")))
    print(f"ses={VOICE} süre={T:.0f} sn (son kelime {tot:.2f} sn)")
    for s in tl["sentences"]:
        print(f"  {s['id']} {s['t0']:6.2f}–{s['t1']:6.2f}  " + " | ".join(f"{i}:{w['show']}" for i, w in enumerate(s['words'])))

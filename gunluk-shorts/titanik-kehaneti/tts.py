"""Titanik'in Kehaneti — anlatıcı: ses-lab/narrator.py (Piper dfki + stüdyo işleme). Çıktı: out/voice.wav, out/timeline.json
Metin işareti: gösterilen=söylenen   *vurgulu*   Kullanım: python3 tts.py [--voice=dfki|fahrettin|fettah]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator

VOICE = "dfki"
PROF = dict(speed=1.08, reverb_wet=0.0)   # anayasa: kuru erkek ses (yankı 0)
for a in sys.argv[1:]:
    if a == "--kadin":   # kadın sesi (WORLD dönüşümü) + kuru ses (yankısız)
        PROF.update(f0_scale=1.55, formant=1.14)
    if a.startswith("--voice="):
        VOICE = a.split("=")[1]

# (id, metin, hız, enerji, sonraki boşluk)
SENTENCES = [
    ("A", "Titanik batmadan *14=on_dört yıl önce*, bir yazar *benzer felaketi yazdı!*", 1.04, 1.2, 0.22),
    ("B", "*5=beş benzerlik* var, ve sonuncusu *çok ürkütücü!*", 1.04, 1.15, 0.20),
    ("C", "Yıl *1898=bin_sekiz_yüz_doksan_sekiz*. Roman: *Futility=fyutiliti.*", 1.02, 1.0, 0.20),
    ("D", "Bir: İkisi de *pratikte batmaz* diye tanıtıldı!", 1.06, 1.15, 0.16),
    ("E", "İki: Nisan gecesi, *Atlantik’te=Atlantikte buzdağına çarptılar!*", 1.06, 1.15, 0.16),
    ("G", "Üç: İkisinde de *cankurtaran botu yetersizdi!*", 1.06, 1.15, 0.16),
    ("H", "Dört: Boyları da *neredeyse aynı!*", 1.06, 1.15, 0.30),
    ("I", "Ve beşinci: romandaki geminin adı, *Titan!*", 1.00, 1.2, 0.30),
    ("J", "Gerçek geminin adı ise, *Titanik!*", 1.00, 1.2, 0.30),
    ("K", "Kehanet mi? Hayır. Yazar, *denizciliği çok iyi biliyordu*, üstelik roman *Titanik’ten sonra* düzenlendi.", 1.02, 1.0, 0.25),
    ("L", "Yine de, *tüyler ürpertici.*", 0.92, 0.9, 0.0),
]

if __name__ == "__main__":
    lex = os.path.join(HERE, "..", "ses-lab", "lex.json")
    if os.path.exists(lex):
        narrator.LEX.update(json.load(open(lex)))
    T, tot, _ = narrator.render(SENTENCES, os.path.join(HERE, "out"), voice=VOICE, profile=PROF)
    tl = json.load(open(os.path.join(HERE, "out", "timeline.json")))
    print(f"ses={VOICE} süre={T:.0f} sn (son kelime {tot:.2f} sn)")
    for s in tl["sentences"]:
        print(f"  {s['id']} {s['t0']:6.2f}–{s['t1']:6.2f}  " + " | ".join(f"{i}:{w['show']}" for i, w in enumerate(s['words'])))

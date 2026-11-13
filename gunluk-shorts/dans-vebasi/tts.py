"""Dans Salgını — anlatıcı: ses-lab/narrator.py (Piper dfki + stüdyo işleme). Çıktı: out/voice.wav, out/timeline.json
Metin işareti: gösterilen=söylenen   *vurgulu*   Kullanım: python3 tts.py [--voice=dfki|fahrettin|fettah]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator

VOICE = "dfki"
for a in sys.argv[1:]:
    if a.startswith("--voice="):
        VOICE = a.split("=")[1]

# (id, metin, hız, enerji, sonraki boşluk)
SENTENCES = [
    ("A", "Bir kadın sokakta dansa başladı, ve *günlerce duramadı!*", 1.00, 1.1, 0.26),
    ("B", "Ama asıl çılgınlık, *yetkililerin çözümüydü!*", 1.02, 1.1, 0.22),
    ("C", "Yıl *1518=bin_beş_yüz_on_sekiz*, Strazburg.", 1.00, 1.0, 0.20),
    ("D", "Bir haftada *34=otuz_dört* kişi katıldı, bir ayda *400=dört_yüz!*", 1.04, 1.15, 0.22),
    ("E", "Yemek yok, uyku yok! Yorgunluktan yığılanlar bile oldu!", 1.04, 1.15, 0.20),
    ("F", "Doktorlar *sıcak kan* dedi. Çözüm mü? *Daha fazla dans!*", 1.04, 1.15, 0.20),
    ("G", "Sahne kurdular, *müzisyenler tuttular!*", 1.02, 1.1, 0.22),
    ("H", "Dans bitmek yerine, *daha da yayıldı!*", 1.02, 1.15, 0.24),
    ("I", "Sonunda müziği yasakladılar, ve dansçıları bir türbeye götürdüler.", 1.02, 1.0, 0.24),
    ("J", "Bilim insanları hâlâ emin değil: *ergot zehirlenmesi mi, toplu histeri mi?*", 1.04, 1.05, 0.26),
    ("K", "Ve dans, *müzik susunca bitti!*", 1.00, 1.15, 0.55),
    ("L", "Bazen çözüm, *sessizliktir.*", 0.90, 0.9, 0.0),
]

if __name__ == "__main__":
    lex = os.path.join(HERE, "..", "ses-lab", "lex.json")
    if os.path.exists(lex):
        narrator.LEX.update(json.load(open(lex)))
    T, tot, _ = narrator.render(SENTENCES, os.path.join(HERE, "out"), voice=VOICE, profile=dict(speed=1.10))
    tl = json.load(open(os.path.join(HERE, "out", "timeline.json")))
    print(f"ses={VOICE} süre={T:.0f} sn (son kelime {tot:.2f} sn)")
    for s in tl["sentences"]:
        print(f"  {s['id']} {s['t0']:6.2f}–{s['t1']:6.2f}  {s['text'][:60]}")

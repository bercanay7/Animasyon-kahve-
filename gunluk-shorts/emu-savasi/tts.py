"""Emu Savaşı — anlatıcı: ses-lab/narrator.py (Piper dfki + stüdyo işleme). Çıktı: out/voice.wav, out/timeline.json
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
    ("A", "Bir ordu, *20=yirmi bin kuşa* savaş açtı, ve *kaybetti!*", 1.00, 1.0, 0.28),
    ("B", "Ama asıl komik kısım, *sondaki rapor!*", 1.02, 1.02, 0.22),
    ("C", "Bu gerçek! Yıl *1932=bin_dokuz_yüz_otuz_iki*, Avustralya.", 1.02, 0.92, 0.20),
    ("D", "Çiftçiler çaresizdi: *20=yirmi bin emu* tarlaları yiyip bitiriyordu!", 1.04, 1.02, 0.20),
    ("E", "Çözüm mü? Askerler, *makineli tüfekler* ve *10=on bin mermi!*", 1.04, 1.09, 0.22),
    ("F", "Ama emular çok akıllıydı! Küçük gruplara bölünüp, *zikzak çizerek* kaçtılar!", 1.05, 1.09, 0.20),
    ("G", "Üstelik saatte *50=elli kilometre* koşuyorlardı. Kamyon bile yetişemedi!", 1.05, 1.02, 0.24),
    ("H", "Peki ordu *kaç mermi* harcadı?", 1.00, 1.0, 0.30),
    ("I", "Yaklaşık *10.000=on_bin mermi*, sadece *1.000=bin emu!* Yani kuş başına, *tam 10=on mermi!*", 1.05, 1.12, 0.24),
    ("J", "Ordu geri çekildi. Komutan bile itiraf etti: Bu kuşlardan bir tümenimiz olsa, her orduyla savaşırdık!", 1.06, 1.0, 0.26),
    ("K", "Skor: *Ordu 0=sıfır, emu 1=bir!*", 0.95, 1.17, 0.0),
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

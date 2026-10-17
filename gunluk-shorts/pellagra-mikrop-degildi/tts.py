"""Pellagra: Mikrop Değildi (TESLİMAT #7) — anlatıcı: ses-lab/narrator.py (Piper dfki + stüdyo işleme). Çıktı: out/voice.wav, out/timeline.json
Metin işareti: gösterilen=söylenen   *vurgulu*   (Türkçe okunuş: pellagra=pelagra, Mississippi=Misisipi, yuttular=yuttu_lar ...; Goldberger yazıldığı gibi okunur: Whisper 6/6 doğru duydu, 'Goldbörgır' tutarsızdı)
Kullanım: python3 tts.py   (en iyi-K sentez için: python3 tts_best.py 5)

Kanca (R, çelişki): "DIŞKI YUTTULAR. HASTALIK BULAŞMADI." — A1+A2 kartla aynı sözdür (≤9 kelime, ≤3,5 sn).
Kural notları (Anayasa §12): hız ≤1,0 · cümle arası ≥0,4 sn · cümle başına tek olgu · ≤3 sayı (yalnız 1916) · cümle ≤14 kelime."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator

VOICE = "dfki"
PROF = dict(speed=0.96, reverb_wet=0.0, gap_comma=0.22, gap_colon=0.30)

# (id, metin, hız, enerji, sonraki boşluk)
SENTENCES = [
    # ── kanca (kartla aynı söz) ──
    ("A1", "*Dışkı yuttular=yuttu_lar.*", 1.0, 1.15, 0.40),
    ("A2", "*Hastalık bulaşmadı.*", 1.0, 1.15, 0.85),
    # ── bağlam: ne oluyordu? ──
    ("B1", "Yüzyıl başında, Amerika’nın=Amerikanın güneyinde, *pellagra=pelagra* denen bir hastalık milyonlarca kişiyi hasta etti.", 1.0, 1.0, 0.50),
    ("B2", "Cilt döküntüsü, ishal, bunama, bazen ölüm.", 1.0, 1.0, 0.60),
    ("B3", "Çoğu doktor bulaşıcı bir *mikrop* arıyordu.", 1.0, 1.0, 0.90),
    # ── gözlem: Goldberger ──
    ("C1", "1914’te=bin_dokuz_yüz_on_dörtte doktor Goldberger, yetimhanelerde bir şey fark etti: *çocuklar hastalanıyordu, çalışanlar hastalanmıyordu.*", 1.0, 1.05, 0.50),
    ("C2", "Bulaşıcı olsaydı, çalışanlar da hastalanırdı.", 1.0, 1.05, 0.90),
    # ── kanıt 1: kanca ödenir ──
    ("D0", "Ama çoğu doktor ikna olmadı.", 1.0, 1.0, 0.40),
    ("D1", "Goldberger, bulaşıcı olmadığını kanıtlamak istedi.", 1.0, 1.0, 0.45),
    ("D2", "1916’da=bin_dokuz_yüz_on_altıda gönüllü doktorlar, hastaların yara kabuğundan, idrarından ve *dışkısından* yapılmış hapları yuttu.", 0.98, 1.1, 0.55),
    ("D3", "*Kimse pellagra=pelagra olmadı.*", 1.0, 1.15, 0.45),
    ("D4", "Sakın denemeyin.", 1.0, 1.0, 0.90),
    # ── kanıt 2 ve 3: peki neden? ──
    ("E0", "Peki hastalık nereden geliyordu?", 1.0, 1.05, 0.50),
    ("E0b", "Cevap, *tabaktaydı.*", 1.0, 1.1, 0.60),
    ("E1", "Yetimhanedeki çocuklar çoğunlukla mısır unu ve pekmez yiyordu.", 1.0, 1.0, 0.45),
    ("E2", "Goldberger, çocukların tabağına süt, yumurta ve et ekledi.", 1.0, 1.0, 0.40),
    ("E2b", "Çocukların çoğu iyileşti.", 1.0, 1.05, 0.65),
    ("E3", "Mississippi’de=Misisipide, af sözüyle gönüllü olan mahkûmlar=mahkumlar, aylarca çoğunlukla mısır ekmeği ve pekmezle beslendi.", 1.0, 1.0, 0.45),
    ("E4", "Yaklaşık *yarısı* pellagra=pelagra oldu.", 1.0, 1.1, 0.90),
    # ── hüküm + ters köşe ──
    ("F1", "Hastalık, *niasin* adlı bir vitaminin eksikliğiydi.", 1.0, 1.05, 0.50),
    ("F2", "Bunu ancak 1937’de=bin_dokuz_yüz_otuz_yedide, Goldberger *öldükten sonra* gösterdiler.", 1.0, 1.05, 0.90),
    ("F3", "Asıl ters köşe şu: *mısır suçlu değildi.*", 1.0, 1.1, 0.50),
    ("F4", "Orta Amerika’nın=Amerikanın yerli halkı, mısırı *kireç* suyunda işlerdi.", 1.0, 1.0, 0.40),
    ("F4b", "Bu işlem, niasini serbest bırakıyordu.", 1.0, 1.0, 0.50),
    ("F5", "Mısırı alan Avrupalılar ise, bu yöntemi almadı.", 1.0, 1.05, 0.70),
    # ── kapanış (karta döner) ──
    ("G1", "Mikrop, *hiç yoktu.*", 0.96, 1.1, 0.0),
]

if __name__ == "__main__":
    lex = os.path.join(HERE, "..", "ses-lab", "lex.json")
    if os.path.exists(lex):
        narrator.LEX.update(json.load(open(lex)))
    T, tot, _ = narrator.render(SENTENCES, os.path.join(HERE, "out"), voice=VOICE, profile=PROF, tail=0.85)
    tl = json.load(open(os.path.join(HERE, "out", "timeline.json")))
    nwords = sum(len(s["words"]) for s in tl["sentences"])
    print(f"ses={VOICE} süre={T:.0f} sn (son kelime {tot:.2f} sn) · {nwords} sözcük · {nwords / tot:.2f} sözcük/sn (duraklar dahil)")
    for s in tl["sentences"]:
        print(f"  {s['id']} {s['t0']:6.2f}–{s['t1']:6.2f}  " + " | ".join(f"{i}:{w['show']}" for i, w in enumerate(s['words'])))

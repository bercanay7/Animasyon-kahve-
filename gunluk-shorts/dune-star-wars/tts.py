"""Dune × Star Wars — anlatıcı: ses-lab/narrator.py (Piper dfki + stüdyo işleme). Çıktı: out/voice.wav, out/timeline.json
Metin işareti: gösterilen=söylenen   *vurgulu*   (yabancı adlar Türkçe okunuşla: Dune=Dyun, Wars=Vors ...)
Kullanım: python3 tts.py   (en iyi-K sentez için: python3 tts_best.py 5)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator

VOICE = "dfki"
# kullanıcı düzeltmesi (2026-10-15): "çok hızlı anlatıyor" → daha yavaş tempo, daha uzun duraklar
PROF = dict(speed=0.90, reverb_wet=0.0, gap_comma=0.22, gap_colon=0.30)

# (id, metin, hız, enerji, sonraki boşluk)
SENTENCES = [
    # ── kanca ──
    ("A1", "Kupkuru bir *çöl gezegeni.* Kaderi yazılmış bir *çocuk.* Evreni yöneten bir *imparator.*", 1.0, 1.1, 0.55),
    ("A2", "Bu, Star Wars’ın=Vorsın hikâyesi. Ama *on iki yıl önce* yazılmış bir romanın da.", 1.0, 1.15, 0.50),
    ("A3", "Peki Star Wars=Vors, o romandan ne kadar ödünç aldı? Cevabın bir kısmı, *geri çevrilmiş bir teklifte* saklı.", 1.0, 1.1, 0.85),
    # ── roman ──
    ("B1", "O roman, *Dune=Dyun.* Yazarı Frank Herbert=Hörbırt, Oregon’daki=Oregondaki hareketli kum tepelerini araştırırken, *çöl gezegeni* fikrine ulaştı.", 0.98, 1.0, 0.50),
    ("B2", "Kitabı *yirmiden fazla yayıncı* geri çevirdi.", 1.0, 1.0, 0.40),
    ("B3", "Ama çıktığında, Nebula ödülünü kazandı.", 1.0, 1.05, 0.75),
    # ── film ──
    ("C1", "*On iki yıl sonra,* Star Wars=Vors geldi.", 1.0, 1.0, 0.35),
    ("C2", "George=Corc Lucas’ın=Lukasın andığı ilhamlar şunlar: Joseph=Cozef Campbell’ın=Kempbılın kahraman miti, Kurosawa’nın=Kurosavanın Gizli Kale’si=Kalesi, ve Flash=Fleş Gordon=Gordın.", 1.0, 1.0, 0.50),
    ("C3", "Listede *Dune=Dyun yok.* Lucas=Lukas, bu bağı hiçbir zaman açıkça kabul etmedi.", 1.0, 1.1, 0.85),
    # ── benzerlikler ──
    ("D0", "Yorumcuların saydığı *beş benzerlik.*", 1.0, 1.0, 0.60),
    ("D1", "*Birincisi:* neredeyse yaşanmaz bir çöl gezegeni. Arrakis, ve Tatooine=Tatuin.", 1.0, 1.05, 0.55),
    ("D2", "*İkincisi:* çölün halkı. Fremenler, ve Jawa’lar=Cavalar. Bir de, devasa paletli araçlar.", 1.0, 1.05, 0.55),
    ("D3", "*Üçüncüsü:* kumun altındaki dev yaratık.", 1.0, 1.05, 0.55),
    ("D4", "*Dördüncüsü:* baharat. Lucas’ın=Lukasın ilk taslağında, prenses, *aura=a_ura baharatı* taşıyordu.", 1.0, 1.05, 0.55),
    ("D5", "*Beşincisi:* bir imparator, ve uzay yollarını elinde tutan bir birlik.", 1.0, 1.05, 0.85),
    # ── Herbert / Lucas ──
    ("E1", "Frank Herbert=Hörbırt fark etti. Anlatıldığına göre, 1977’de=bin_dokuz_yüz_yetmiş_yedide şöyle dedi: *dava açmamak için elimden geleni yapacağım.*", 0.98, 1.0, 0.50),
    ("E2", "1985’te=bin_dokuz_yüz_seksen_beşte ise, iki eser arasında *on altı özdeşlik noktası* saydı. Ama, *kopyaladılar demiyorum,* diye ekledi.", 0.98, 1.05, 0.50),
    ("E3", "Lucas’ın=Lukasın cevabı: bildirildiğine göre, tek ortak nokta, ikisinde de *çöl* olmasıydı.", 1.0, 1.0, 0.85),
    # ── ortak atalar / uyarı ──
    ("F1", "Peki gerçekten kopya mı? Ortak atalar da var: Arabistanlı Lawrence=Lavrens, ve eski kahraman mitleri.", 1.0, 1.0, 0.50),
    ("F2", "Üstelik Herbert=Hörbırt, Paul’ü=Polü bir *uyarı* olarak yazdı: süper kahramanların hataları, çok insanı felakete sürükler.", 0.98, 1.05, 0.85),
    # ── telefon / teklif ──
    ("G1", "Şimdi o teklif. Lucas=Lukas, Jedi’ın=Cedinin Dönüşü için, David=Deyvid Lynch’e=Linçe kapıyı çaldı.", 1.0, 1.0, 0.50),
    ("G2", "Lynch=Linç teklifi geri çevirdi, ve *Dune=Dyun filmini* çekti.", 1.0, 1.1, 0.40),
    ("G3", "Film, yatırımını bile çıkaramadı.", 1.0, 1.0, 0.50),
    ("G4", "Yıllar sonra Denis=Deni Villeneuve=Vilnöv, yeni Dune=Dyun filmini çekerken şöyle dedi: *Star Wars’ın=Vorsın ana fikirlerinin çoğu, Dune’dan=Dyundan geliyor.*", 0.98, 1.05, 0.90),
    # ── hüküm ──
    ("H1", "Yani kesin bir kopya kanıtı yok. Ama *izler çok.*", 0.98, 1.05, 0.70),
    ("H2", "Sence tesadüf mü, ilham mı, yoksa ortak kaynak mı?", 0.95, 1.0, 0.0),
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

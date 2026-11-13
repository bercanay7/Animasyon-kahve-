"""c5 — Konsil, Kitap, Platon (1439–1492). Brif: brif/c5_brif.md. Hafif-entelektüel, sıcak; 1453 cümlesinde mizah kapalı. Careggi mektubu BURADA (c3'te yok)."""
PRON = [
    (r"\bFerrara\b", "Ferrara"), (r"\bPlethon\b", "Pleton"), (r"\bManuel Chrysoloras\b", "Manuel Hrisoloras"), (r"\bChrysoloras\b", "Hrisoloras"),
    (r"\bNiccolò Niccoli\b", "Nikkolo Nikkoli"), (r"\bNiccoli\b", "Nikkoli"), (r"\bJanus Lascaris\b", "Yanus Laskaris"), (r"\bLascaris\b", "Laskaris"),
    (r"\bAthos\b", "Atos"), (r"\bOrfik\b", "Orfik"),
]

CH = dict(id="c5", n="V", title="Konsil, Kitap, Platon", years="1439 – 1492", mood="warm", front="",
          paras=[[
              ("1439'da Ferrara'daki konsil Floransa'ya taşındı; masraf, veba korkusu ve Cosimo'nun teklifi birlikte etkili oldu.", None, "◐ M3:K25,§5.7 (Medici payı var, tek neden değil)"),
              ("Aktarılana göre Floransa, yaklaşık yedi yüz kişilik Rum heyetinin masraflarını üstlenmeyi bile önermişti; cömert ev sahibi, kalabalık misafir.", None, "◐ teklif M3:K25 / ○ 700 M3:C20 (mizah)"),
              ("Temmuzda Doğu ile Batı kiliselerinin birliği ilan edildi; Bizans bu birliği Osmanlı tehdidi yüzünden istemişti.", None, "◐ M3:K26,TR#6,K23 (tarih 5/6 Temmuz söylenmez)"),
              ("Vaat edilen yardım gelmedi; 1453'te İstanbul düştü.", None, "◐ M3:C21,K28 (mizah KAPALI; \"hiçbir yardım\" DENMEZ)"),
          ], [
              ("Ficino'ya göre Cosimo'nun Platon merakı, konsil sırasında Bizanslı filozof Plethon'un konuşmalarını dinlemesiyle uyandı; Floransalılar Plethon'a “ikinci Platon” dermiş.", None, "ANEKDOT ◐ M3:K27,C19 (Ficino yıllar sonra anlatır)"),
              ("Floransa'da Yunanca öğretimi 1453'te başlamadı; Manuel Chrysoloras 1396 ile 1397 arasında ders vermişti.", None, "◐ M3:K23,§5.8 (1453 → Rönesans mitini kapatır)"),
          ], [
              ("Kitap meraklısı Niccolò Niccoli borç içinde öldü; Cosimo borçları üstlenip yaklaşık sekiz yüz el yazmasının denetimini aldı, kitaplar San Marco'ya gitti.", None, "◐ M3:K10,C7 (800 cilt mi el yazması mı ayrışır)"),
              ("Böylece Floransa'nın halka açık bir kitaplığı doğdu.", None, "◐ YORUM M3:Y5 (\"ilk halk kütüphanesi\" DENMEZ)"),
          ], [
              ("1463 dolaylarında, Ficino'nun derlemesindeki bir mektupta Cosimo, Careggi'ye tarlasını değil, zihnini işlemek için geldiğini yazar.", None, "◐ M3:C16,K31 (tarih editör notu; İngilizce çeviri; birebir söylenmez)"),
              ("Ardından Ficino'dan Platon'un En Yüksek İyi üzerine kitabını ve Orfik lirini getirmesini ister.", None, "◐ M3:C16 (Philebus teşhisi editör notu)"),
              ("Bir bankacı için fena bir alışveriş listesi değil: en yüksek iyi, bir de lir.", None, "YORUM (laf sokma; Cosimo'nun sözü gibi sunulmaz)"),
              ("Cosimo, Ficino'ya Platon'un bütün eserlerinin bir el yazmasını, şehirde bir ev ve Careggi yakınında bir ev daha armağan etmişti.", None, "◐ M3:C17,K30"),
              ("Buna sonradan “Platon Akademisi” dendi; ama tüzüğü yoktu, üye kaydı tutulmadı.", None, "◐ M3:C18,§5.6; M3b:b98,bm10 (\"Akademi\" tırnaklı)"),
              ("Cosimo bu mektuptan yaklaşık bir yıl sonra öldü.", None, "◐ M1:K56 (mektup tarihi kesin değil → \"yaklaşık\")"),
          ], [
              ("Torunu Lorenzo, Janus Lascaris'i 1490 ve 1491'de iki kez Doğu'ya gönderdi: el yazması toplasın, II. Bayezid'le de pazarlık yapsın.", None, "◐ M3:K32,TR#1; M2:K81 (tek sefer DEĞİL)"),
              ("1491'de Athos'a uğradı.", None, "◐ M3:K33"),
              ("Cep defterinde iki şey vardı: Lorenzo'nun elde etmek istediği metinlerin listesi ve Medici kütüphanesinin o günkü içeriği.", None, "◐ M3:C23 (Vat. gr. 1412)"),
              ("Lascaris Yunanistan'dan iki yüz el yazması getirdiğini söyler; defterdeki liste bunun neredeyse iki katı.", None, "◐ M3:C24,S16 (\"söyler\"; mizah: liste tutkusu)"),
              ("Pazarlığın ayrıntısını bilmiyoruz; ama Floransa'nın tahtsız efendisinin kitap hesabını, Osmanlı topraklarında bir Rum bilgin yürütüyordu.", None, "◐ YORUM M3:Aday4,TR#1"),
          ], [
              ("Lascaris'in listesi Lorenzo için yazılmıştı.", None, "◐ M3:C23"),
              ("Şimdi listenin sahibine, Lorenzo'ya bakalım.", None, "YORUM (c6 kapısı)"),
          ]])

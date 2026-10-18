"""c8 — Aslanın İni (1478–1481). Brif: brif/c8_brif.md. Ciddi-diplomatik; kuru mizah YALNIZ kuruma/usule (V1, V3, V5, V7). MİZAH KAPALI: V4 (Bandini, Leonardo), V6 (Otranto).
Yıldız an: V4 paralel kurgu — 29 Aralık 1479'da Bandini Floransa'da asılırken Lorenzo Napoli'de (eşzamanlılık BELGELİ). "Silahsız" DENMEZ. Bandini'yi getiren temsilcinin adı verilmez. Otranto'da Lorenzo özne değil.
Kapı: K1 (c9: şube ışıkları sönüyor)."""
PRON = [
    (r"\bFerrante\b", "Ferrante"), (r"\bAlfonso\b", "Alfonso"), (r"\bSiena\b", "Siyena"), (r"\bChianti\b", "Kyanti"),
    (r"\bColle Val d'Elsa\b", "Kolle Val d'Elsa"), (r"\bPoggio Imperiale\b", "Poççio İmperyale"),
    (r"\bPera\b", "Pera"), (r"\bAntonio de' Medici\b", "Antonyo de Mediçi"), (r"\bBandini\b", "Bandini"),
    (r"\bBargello\b", "Bargello"), (r"\bLeonardo\b", "Leonardo"), (r"\bBertoldo di Giovanni\b", "Bertoldo di Covanni"),
    (r"\bOtranto\b", "Otranto"), (r"\bGedik Ahmed\b", "Gedik Ahmed"), (r"\bVolterra\b", "Volterra"),
    (r"\binterdikt\b", "interdikt"),
]

CH = dict(id="c8", n="VIII", title="Aslanın İni", years="1478 – 1481", mood="serious", front="",
          paras=[[
              ("Aforoz kararı 1 Haziran 1478'de çıktı; çok geçmeden Floransa'nın kendisine de yasak, yani interdikt kondu.", None, "◐ M2c:Y35,Y37 (interdikt günü söylenmez)"),
              ("Aktarıldığına göre papalık belgeleri, alışılmış üslupla, Lorenzo'ya “kötülüğün oğlu ve yıkımın evladı” diyordu.", None, "○ Reumont (Latince iniquitatis filius et perditionis alumnus); çeviri bize ait (mizah a: kurumun üslubu)"),
              ("Napoli Kralı Ferrante Papa'nın yanında savaşa girdi; ordunun başında oğlu Alfonso, generali ise Urbino'dan Federico da Montefeltro vardı.", None, "◐ M2c:Y43 Reumont + Collector + DBI Alfonso II"),
          ], [
              ("Siena ordunun geçişine izin verdi; Alfonso Chianti'ye girip kaleleri aldı.", None, "◐ M2c:Y44 Reumont"),
              ("1479 sonbaharında Floransa ordusu Poggio Imperiale'de yenildi; Colle Val d'Elsa da uzun bir kuşatmanın ardından düştü.", None, "◐ yön M2c:Y45,Y46,D59 (gün/komutan söylenmez)"),
              ("Savaş masrafı hazineyi boşaltıyordu.", None, "◐ M2c:Y47 Collector"),
          ], [
              ("6 Aralık 1479'da Lorenzo Floransa'dan ayrılıp düşman kralın yanına, Napoli'ye gitti.", None, "◐ M2c:Y48 EI + DS (\"silahsız\" DENMEZ — D61)"),
              ("Pisa'ya varınca Signoria'ya yazıp nedenini bildirdiği, Signoria'nın da ona elçilik ve tam yetki verdiği anlatılır.", None, "○ M2c:Y49 (\"anlatılır\")"),
              ("Önce yola çıktı, yetkiyi sonra aldı; diplomasi bazen böyle işler.", None, "YORUM (mizah b — usul; kaynak ○, \"anlatılır\" cümlesinin hemen ardından)"),
              ("Napoli'ye 18 Aralık'ta vardı.", None, "◐ tek DBI M2c:Y50 (\"DBI'ye göre\")"),
              ("Konuk muydu, rehine mi? Ne düşündüğünü bilmiyoruz; ama ne yaptığını biliyoruz: şubat sonuna dek orada kaldı.", None, "kalıp (USLUP §3; bölümün tek iç-dünya kalıbı); ◐ 27 Şubat DBI"),
          ], [
              ("Aynı haftalarda doğudan Floransa'ya gelen bir yolculuk sona eriyordu.", None, "◐ M2c:Y59–Y62 DBI Bandini (heyet 24 Aralık'ta vardı)"),
              ("Giuliano'yu vuranlardan Bernardo Bandini, kiliseden kaçıp İstanbul'a ulaşmıştı; orada akrabaları vardı.", None, "◐ M2c:Y57 DBI Bandini + Louvre + Treccani (\"ilk darbe\" T4 çelişkisi → söylenmez)"),
              ("8 Mayıs 1479'da Pera'daki Floransalı temsilcinin yazdığına göre Fatih Sultan Mehmed, Floransa sevgisinden dolayı katili tutuklatmıştı.", None, "◐ M2c:Y58 DBI Carducci (\"yazdığına göre\" = temsilcinin öz-bildirimi; adı VERİLMEZ)"),
              ("Floransa, Antonio de' Medici'yi elçi seçip 14 Temmuz'da aceleyle yola çıkardı; çünkü Sultan katili Ağustos ortasından fazla hapiste tutmayacaktı.", None, "◐ M2c:Y59,Y60 DBI Bandini + Carducci"),
              ("Sultan'ın bunu neden yaptığını bilmiyoruz; Floransa'nın Osmanlı topraklarında ticaret ayrıcalıkları vardı.", None, "○ M2c:Y65 (opsiyonel; tek makale özeti; \"bilmiyoruz\" + \"vardı\")"),
              ("Heyet 24 Aralık'ta Floransa'ya vardı.", None, "◐ M2c:Y62"),
              ("Bandini beş gün sonra, 29 Aralık'ta, Bargello'nun penceresinden asıldı; üstünde hâlâ Doğu giysileri vardı.", None, "◐ M2c:Y63 (28/29 tek makale; D62 — yayın öncesi teyit; asılı beden GÖSTERİLMEZ)"),
              ("O sırada Lorenzo Napoli'deydi.", None, "◐ hesap: 18 Aralık–27 Şubat M2c:Y50 (eşzamanlılık belgeli)"),
              ("Leonardo asılı adamı çizdi, giysisini satır satır not etti.", None, "◐ M2c:Y64 Louvre (Bayonne) + Richter 664 (not içeriği söylenmez)"),
          ], [
              ("Ferrante Papa'nın safından ayrıldı; Lorenzo mart ortasında Floransa'ya barışla döndü.", None, "◐ M2c:Y51 (13 ↔ 15 Mart → \"mart ortası\") EI + EdP + DBI"),
              ("Barış parlak değildi; şartlar arasında savaşta alınan yerlerin akıbetinin kralın takdirine kalması, Alfonso'ya süreli bir ödeme yapılması ve Volterra'da tutulan Pazzi'lerin salıverilmesi sayılır.", None, "◐/○ M2c:Y53 Reumont + DBI Lorenzo (\"çok avantajlı değil\") + DBI Pazzi (1480'de salıverildi)"),
              ("Nisanda Lorenzo, beş yıllığına bir Yetmişler Konseyi kurdurdu; konsey 1485'te de 1490'da da yenilendi.", None, "◐ M2c:Y54 DBI Lorenzo + Enc. machiavelliana (mizah c: \"beş yıllık\" ↔ iki yenileme)"),
          ], [
              ("Sonra denizden bir haber geldi.", None, "YORUM (Zweig ritmi)"),
              ("28 Temmuz 1480'de Gedik Ahmed Paşa'nın donanması Otranto yakınına çıktı; şehir ağustosta düştü.", None, "◐ M2c:Y67,Y68 (8/11/14 Ağustos çelişir → \"ağustosta\"; ölü sayıları söylenmez)"),
              ("Ferrante, oğlu Alfonso'yu ve ordusunu Toskana'dan geri çağırdı.", None, "◐ M2c:Y69 Historians' + DBI A. Carafa"),
              ("Papa'nın Floransa'ya öfkesi Osmanlı çıkarması karşısında geri plana düştü; Aralık 1480'de Floransa'nın elçileri affedildi.", None, "◐ M2c:Y70 EdP (3 Aralık) ↔ Reumont (23 Aralık) → \"Aralık\"; tören ANLATILMAZ"),
          ], [
              ("Bu yıllarda Floransa'da, Lorenzo'nun heykeltıraşı Bertoldo di Giovanni, Fatih Sultan Mehmed'in profilini bronza döküyordu.", None, "◐ M2c:Y66 V&A + Met + Frick (1480 ↔ 1481 → \"bu yıllarda\")"),
              ("Müzelerin yazdığına göre madalya, Sultan'ın katili yakalatmasına bir teşekkür olarak ısmarlanmış olabilir; kesin belge yok.", None, "◐ hedge'li M2c:Y66,D66 (\"düşünülür\")"),
              ("Arka yüzünde Mehmed bir zafer arabasındadır; arabada Napoli krallarının alevli sandalye amblemi görülür.", None, "◐ M3:§5.18 V&A + Met (nesne tarifi)"),
              ("Müzeler bunu Napoli'ye olası bir saldırıya imâ sayar; Napoli'yle barışı yeni imzalamış bir şehir için tuhaf bir hediye.", None, "◐ olgu / YORUM (mizah c: kuru; opsiyonel)"),
              ("Mehmed 3 Mayıs 1481'de öldü; Otranto aynı yılın eylülünde Napoli'ye döndü.", None, "HAFIZA-Y (3 Mayıs) + ◐ (10 Eylül 1481) M2c:Y72,Y73 — yayın öncesi teyit"),
          ], [
              ("Lorenzo bir savaşı barışa çevirmişti.", None, "YORUM (K1, c9 kapısı)"),
              ("Ama bankasının şubelerinde, Londra'dan Milano'ya, ışıklar birer birer sönüyordu.", None, "◐ M1b:b51–b54 (Londra 1477–78, Milano 1478–79, Avignon 1479–80, Brugge 1480–81; \"ışık\" mecaz)"),
          ]])

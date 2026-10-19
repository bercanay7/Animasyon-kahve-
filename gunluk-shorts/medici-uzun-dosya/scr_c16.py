"""c16 — Hesap (1737–bugün). Brif: brif/c16_brif.md. Kapanış: c0'daki odaya dönüş; izleyici artık her şeyi biliyor (dramatik ironi bitti, hesap başlıyor).
Ağır giriş (ölüm odası, mizah KAPALI) → hafif-kuşkucu orta (tez sorgusu, sağlamlık haritası) → sessiz kapanış (mezar, alay). Söylenen sayı ≤6: 18 Şubat 1743 · yetmiş beş · 1737 (s3) · 1494 · 1769 (+ ekranda: 1340/1407 · 1563 · 1588 · 1734 · 2004 · 2009 · 2012-13).
'Bağışladı / miras bıraktı' DENMEZ (şartlı devir; tek akademik özet ○). 'Hiçbir şey buradan çıkmayacak' = maddenin BİZİM özetimiz (söylenir). Maddenin UYGULANDIĞI araştırmada YOK → 'çıkmadı' mutlak cümlesi kurulmaz. 'Tüm Medici'ler bitti' DENMEZ.
V7 (Medici Etkisi / oyun / dizi) sığmadı — YEDEK. Ekran: sağlamlık haritası (altın SAĞLAM / lacivert NİTELİKLİ / kızıl MİT) + mit kapanış tablosu (§3c; 'frengi' satırı DÜŞER — seste anlatılmadı).
Kapanış: K2 uyarlaması."""
PRON = [
    (r"\bGombrich\b", "Gombrih"), (r"\bCapitoline\b", "Kapitolin"), (r"\bRothschild\b", "Rotşild"),
    (r"\bTornabuoni\b", "Tornabuvoni"), (r"\bPrimavera\b", "Primavera"), (r"\bHarvard\b", "Harvard"),
]

CH = dict(id="c16", n="XVI", title="Hesap", years="1737 – bugün", mood="solemn", front="",
          paras=[[
              ("18 Şubat 1743. Yetmiş beş yaşındaki kadın, Anna Maria Luisa, ölüyor.", None, "◐ M4:#107; M4b:b78 (ölüm yeri Pitti ◐ zayıf; saat, tanık, son söz YOK; c0'a dönüş)"),
              ("Bir anlatıya göre, bedeninin açılmamasını ve yüzüyle ellerinin yalnız nedimelerince yıkanmasını istemiş.", None, "○ M4b:b79,bD26 (blog zinciri; birincil görülmedi — \"bir anlatıya göre\"; opsiyonel; \"istediği yerine gelmemiş\" ÇIKARILDI — kaynağı yok, bizim çıkarımımızdı)"),
          ], [
              ("1737'de imzalanan sözleşmeye çoğu zaman bağış denir; bir akademik yoruma göre ise bu bir devir koşuluydu: Lorraine, eserlerin Floransa'dan çıkarılamayacağını kabul ediyordu.", None, "◐ \"devredilemezlik\" / ○ akademik yorum tek özet M4b:b75,bM13,D11 (\"bir yoruma göre\"; \"bağışladı\" DENMEZ; tarih c0'daki 31 Ekim 1737 ile tutarlı — yıl söylenir, gün ekranda; hangi sözleşme: c15s19 kapısı)"),
              ("Uffizi'ye göre madde, yeni hanedanın Floransa'nın hazinelerini yağmalamasını hukuken önlemek içindi.", None, "◐ M4b:b74 (\"Uffizi'ye göre\")"),
              ("“Hiçbir şey buradan çıkmayacak” demek, maddenin bizim özetimizdir; Anna Maria Luisa'nın söylediği bilinen bir söz değil.", None, "◐ M4b:bD23 (3. madde çevirisinin özeti; \"dedi\" DEĞİL — c0 başlık/alıntı kartı da \"sözleşmeye yazıldı\" biçiminde)"),
              ("Maddenin sonradan nasıl uygulandığını ise bilmiyoruz.", None, "uygulama araştırmada YOK (Patto'nun UYGULANMASI: Lorraine dönemi taşınmalar/mücevherlerin akıbeti aranmadı)"),
          ], [
              ("Peki Medici'ler Rönesans'ı yarattı mı?", None, "—"),
              ("Kaynaklar onu tek yaratıcı değil, en görünür patronlardan biri olarak anlatıyor.", None, "YORUM/◐ M3:§5.1,Y3 (değerlendirme; tırnak kaldırıldı — USLUP §3: tırnak içi kaynaklı söz sayılır)"),
              ("Kubbeyi yün loncası yaptırdı; Strozzi, Rucellai, Tornabuoni da sipariş verdi; Primavera bile büyük olasılıkla ailenin başka bir kolunun siparişiydi.", None, "◐ M3:D1,K18,K20,K44,§5.13; M3b:b83,b87 (Primavera: 1499 envanteri → \"büyük olasılıkla\"; sipariş belgesi yok)"),
              ("Tarihçiler de tartışır: Gombrich, benzersiz konumdaki Medici'nin “tipik” patron sayılmasına itiraz etti; Goldthwaite sanat talebini şehirde biriken zenginliğe bağladı.", None, "◐ özet düzeyi M3:C65,C67 (1993 tartışması; Burckhardt/Baron/Kent/Welch adları ANILMAZ — HAFIZA)"),
              ("Görünürlüğün bir kısmı kaynaklardan geliyor: Vespasiano Cosimo'yu övdü; Vasari de Medici'nin hizmetindeydi.", None, "◐ Vespasiano M3:C1; Vasari Medici hizmeti c12/c14'te belgeli (\"Vasari Cosimo I sarayında yazdı\" H söylenmez)"),
              ("Medici'yi ayıran, ölçek ve siyasi görünürlüktü.", None, "YORUM M3:Y3 (\"şöyle okumak mümkün\")"),
          ], [
              ("Şimdi anlattıklarımızı sağlamlığına göre ayıralım.", None, "— (ekran: altın SAĞLAM / lacivert NİTELİKLİ / kızıl MİT)"),
              ("Çifte kaydı Medici icat etmedi; Cenova'da ve Venedik'te bu yöntem onlardan çok önce kullanılıyordu.", None, "◐ mit M1:mit1,K71,K73 (Cenova 1340 / Venedik 1407 ekranda)"),
              ("Opera ve piyano Medici'nin sarayında ortaya çıktı, ama icat onların değil.", None, "◐ M3b:bm3,bm5"),
              ("Uffizi çoğu yerde ilk modern müze diye anılır; oysa Roma'daki Capitoline ondan önce halka açılmıştı.", None, "◐ M3b:b78,b79,bm12 (Capitoline 1734 ekranda; \"ilk modern müze\" DENMEZ)"),
              ("Medici'den Fugger'e, Fugger'den Rothschild'e uzanan zincir de bir benzetmeden ibaret; kurumsal süreklilik yok.", None, "◐ M1b:bM11"),
          ], [
              ("Banka resmen 1494'te bitti; ama çözülme çok önceden, şube şube sürüyordu ve suçlu tek kişi değildi.", None, "◐ M1:K69,DÜZ#10; M1b:b58,U33,bM8,U31 (\"1494'te battı\" DENMEZ; resmen bitti)"),
              ("Medici defterlerinin bir kısmı bugün Floransa Devlet Arşivi'nde, bir kısmı Harvard'da.", None, "◐ M1:D50 (Baker Library, Selfridge Koleksiyonu = ailenin bir kolunun hesap defterleri; \"banka defteri\" DENMEZ)"),
              ("Banka öldü; kurumlar kaldı: Opificio delle Pietre Dure bugün de çalışıyor, Uffizi 1769'dan beri halka açık.", None, "◐ M3:Y13,K74,K72"),
          ], [
              ("Yol boyunca düzelttiğimiz hikâyeleri ekranda bir arada bırakıyoruz.", None, "— (ekran: mit kapanış tablosu §3c; sessiz 6–8 sn; \"çürüttüğümüz\" zafer dili idi → \"düzelttiğimiz\")"),
          ], [
              ("Mezarı yakın zamanda açıldığında iç organları ayrı bir kapta bulundu; ölüm nedeni belirsiz kaldı.", None, "◐ M4b:b81,bM15 (açım Aralık 2012–Şubat 2013 ekranda; frengi izi yoktu — ekran notu)"),
              ("Her 18 Şubat'ta Floransa, Anna Maria Luisa'yı tarihî bir alayla anar: Palazzo Vecchio'dan Medici Şapelleri'ndeki mezarına yürünür, o gün belediye müzeleri ücretsizdir.", None, "◐ M4b:b82 (\"Elettrice Palatina günü\"; 18 Şubat belediye müzeleri ücretsiz; Uffizi 31 Ekim ○ söylenmez)"),
              ("Para gitti, banka gitti.", None, "YORUM (kapanış K2 uyarlaması)"),
              ("Kalan şey, bir kadının da imzaladığı bir cümle ve o kadını her yıl yürüyerek anan bir şehir.", None, "◐ b82 + YORUM"),
          ]])

"""c9 — Defter Kapanıyor (1470–1494). Brif: brif/c9_brif.md. Kuru-hüzünlü; mizah yalnız kuruma/kaynak çelişkisine. 1494 el koyma: mizah KAPALI.
c6–c8'le çakışan olaylar (Pazzi, Volterra, Otranto) burada TEKRAR EDİLMEZ; yalnız bankacılık yönü."""
PRON = [
    (r"\bTommaso Portinari\b", "Tommazo Portinari"), (r"\bPortinari\b", "Portinari"),
    (r"\bSassetti\b", "Sassetti"), (r"\bGhirlandaio\b", "Girlandayo"), (r"\bSanta Trinita\b", "Santa Trinita"),
    (r"\bTolfa\b", "Tolfa"), (r"\bDonatello\b", "Donatello"), (r"\bJudith\b", "Yudit"),
    (r"\bAvignon\b", "Avinyon"), (r"\bRaymond\b", "Reymond"), (r"\bGoldthwaite\b", "Goldtveyt"), (r"\bPalazzo Medici\b", "Palattso Mediçi"),
]

CH = dict(id="c9", n="IX", title="Defter Kapanıyor", years="1470 – 1494", mood="dry", front="",
          paras=[[
              ("Lorenzo'nun Floransa'sı parlarken, bankanın defteri sessizce incelmeye başlamıştı.", None, "◐ M1:düz10 (fiilî çözülme 1470'lerden beri) + YORUM"),
              ("Bankanın yolu şapa da düştü: boyayı kumaşa tutturan, Floransa'nın boyahanelerinin ihtiyaç duyduğu bir mineral.", None, "◐ M1b:§6B#1,KB26 (Floransa yünüyle bağ = çıkarım)"),
              ("Batı'nın şapı Foça'dan geliyordu; Foça 1455'te Osmanlı'ya geçince papalık kendi topraklarında, Tolfa'da yatak buldu.", None, "◐ M1b:b5,b7 (Foça 1455; Tolfa)"),
              ("Pazarlama hakkını 1466'da, Piero de' Medici'nin de içinde olduğu bir gruba verdi.", None, "◐ M1b:b11 (Piero, Lorenzo DEĞİL; \"II. Pius Medici'ye verdi\" DENMEZ)"),
              ("Papa, Türk şapı alanları aforozla tehdit etti; alıcılar yine de daha ucuz Türk şapına yöneldi.", None, "○ tehdit ayrıntısı Parks / ◐ Türk şapı sürdü M1b:bM5,bD15 (mizah a: kurumun silahı ↔ fiyat)"),
              ("Medici'nin şaptan ne kazandığını bilmiyoruz; yalnız, 1475'te banka şapta zarar yazıyordu diye aktarılır.", None, "○ M1b:b22,X1 (yokluk cümlesi; Parks; rakam yok)"),
          ], [
              ("Brugge'de yıllarca yardımcı olarak çalışan Tommaso Portinari'ye Cosimo'nun pek güvenmediği anlatılır; ama Cosimo ölünce Portinari şubenin müdürü ve ortağı oldu.", None, "◐ \"anlatılır\" M1:#57,D40 (yıl ≈1465–68 belirsiz; \"genel müdür\" = yalnız Brugge şubesi — banka genel müdürü Sassetti, s17 ile karışmasın)"),
              ("Portinari, Burgonya Dükü Cesur Şarl'a büyük, teminatsız krediler verdi; borç geri ödenmedi.", None, "○ \"yazılır\" M1:#63,D41 (kapsamı tartışmalı; Memling portreleri ekranda, M1:D43)"),
              ("Hem Medici'nin müdürüydü hem dükün danışmanı: iki efendiye hizmet.", None, "○ M1:D42 (mizah b)"),
              ("Medici sonunda Brugge'yi tasfiyeye karar verip Portinari'yi şubeyi üstlenmeye zorladı; şube 1480 ya da 1481'de kapandı.", None, "◐ M1b:b52,bD7 (kapanış aralık)"),
          ], [
              ("Londra şubesi, 1466 ile 1471 arasında Kral IV. Edward'a toplam yirmi altı bin sterlinden fazla kredi verdi.", None, "○ M1:#60,D44 (Holmes/Cambridge: TOPLAM kredi, kalan borç DEĞİL; popüler £10.500 SÖYLENMEZ)"),
              ("Bir kısmı geri ödendi; kalanı için Güller Savaşı suçlanır, ama rakamlar kaynaktan kaynağa değişir.", None, "○ çelişkili M1:#60; M1b:U23,b50 (mizah a: kaynaklar da uzlaşmıyor)"),
              ("Şube 1477 ile 1478 arasında tasfiye edildi.", None, "◐ aralık M1b:b51,bM9 (51.533 florin zarar ekran kartı, ○)"),
          ], [
              ("Milano, Avignon, Brugge, Venedik: şubeler 1470'lerin sonundan 1481'e dek tek tek kapandı.", None, "◐/○ aralıklar M1b:b53,b54,b52,b55 (kesin yıl söylenmez)"),
          ], [
              ("Suçlu kimdi?", None, "—"),
              ("Medici'nin siparişiyle tarih yazan Machiavelli, suçu ajanlara atar: Lorenzo ticarette talihsizdi, ajanlarının uygunsuz davranışları yüzünden.", None, "◐ M1b:bD4,M1:D39 (EN çeviri özeti; çeviri bize ait)"),
              ("Sassetti 1463'ten 1490'daki ölümüne dek, yaklaşık otuz yıl, genel müdürdü; İtalyan Ansiklopedisi Treccani sorunu “verimsiz bir mali örgütlenme” diye özetler.", None, "◐ M1b:bD11,b47,U18 (parçada ilk Treccani → kısa tanım; 1463 ↔ 1458/59 ve \"otuz yıl\" yayın öncesi teyit)"),
              ("Tarihçi Raymond de Roover'a göre Lorenzo parlak bir devlet adamıydı, iş adamı değil; Goldthwaite ise 1500 öncesi Floransa'da genel bir banka krizi görmez.", None, "○ yaklaşık M1b:bD17,b82 (birebir tırnak yok; \"genel\" eklendi; Goldthwaite özeti ○; \"Tarihçi de\" bağlaç okunmasın diye ad tam)"),
              ("Yani bankayı kimin batırdığı, kime sorduğunuza bağlı.", None, "YORUM"),
              ("Genel müdür Sassetti ise 1480'lerde Santa Trinita'da Ghirlandaio'ya kendi şapelini yaptırıyordu.", None, "◐ M3:k21 (yıllar HAFIZA 1483–85 → \"1480'lerde\"; ironi YORUM)"),
          ], [
              ("Kasım 1494'te Lorenzo'nun oğlu Piero kaçtı; Signoria Medici'yi sürgün etti.", None, "◐ M1b:b64; M2:K91 (8↔9 Kasım söylenmez; öyküsü c10)"),
              ("Cumhuriyet Palazzo Medici'ye ve öteki Medici konutlarına resmen el koydu; Donatello'nun David'i ve Judith'i Palazzo Vecchio'ya taşındı.", None, "◐ M1b:b65"),
              ("Kalabalık bahçelere daldı; saray kısmen yağmalandı, resmen el kondu.", None, "◐/○ M1b:b66,bD12,bM16 (üst kat ayrıntısı tek müze sitesi → söylenmez)"),
              ("Bankanın bütün mülkü, Floransa'daki masası dahil, kayyumlara verildi.", None, "◐ M1b:b67 (15.445 florin alacak ekran kartı, ○)"),
              ("Resmî son 1494'tü; fiilî çözülme 1470'lerden beri şube şube sürüyordu.", None, "◐ M1:düz10,mit17; M1b:U33"),
          ], [
              ("Banka sona ermişti; ama Donatello'nun bronzları Palazzo Vecchio'ya taşındı.", None, "◐ M1b:b65 + YORUM"),
              ("Banka öldü, güzellik kaldı.", None, "YORUM (tez cümlesi)"),
              ("Peki Medici'yi sürgüne gönderen o güne nasıl gelindi? Bir kralın Alpler'i aşmasıyla, bir rahibin vaazlarıyla.", None, "YORUM (c10 kapısı; \"o gün\" = Kasım 1494; kral c10s12'de VIII. Charles diye adlandırılır)"),
          ]])

"""c14 — Yıldızlar, Notalar, Taşlar (1584–1737). Brif: brif/c14_brif.md. Parlak ve meraklı; 1633'te AĞIRLAŞIR (V6 MİZAH KAPALI, süssüz). Bölümün ipi (YORUM): Medici bu çağda icatçı değil, ev sahibidir: sahne, maaş, envanter.
Mizah: Bandini soyadı göz kırpması (V1), Caccini'nin altı hafta önce bastırdığı nota (V4), 'yıldızlar aileye zimmetlendi, kayıtlar tutmadı' (V5), envanterde 'yeni icat' (V7). 'İlk opera / Medici icat etti' ve 'Osmanlı matbaayı yasakladı' DENMEZ.
Söylenen yıl ≤: 1600 · 1610 · 1633 · 1700 (+ dört, altı hafta). 1584/1588/1593/1688/1711 HUD'da. Livornina + Fahreddin + Mustafa Ağa c15 V2'de (burada YOK). Zweig kalıbı kullanılmadı.
Kapı: K1 (YORUM) → c15."""
PRON = [
    (r"\bGregorius\b", "Gregoryus"), (r"\bGranjon\b", "Granjon"), (r"\bOrazio Bandini\b", "Orattsyo Bandini"),
    (r"\bOpificio delle Pietre Dure\b", "Opifiçyo delle Piyetre Dure"), (r"\bDialogo\b", "Dialogo"),
    (r"\bMarius\b", "Maryus"), (r"\bSidereus Nuncius\b", "Sidereus Nuntsius"), (r"\bJacopo Peri\b", "Yakopo Peri"),
    (r"\bPeri\b", "Peri"), (r"\bCaccini\b", "Kaççini"), (r"\bVittoria Archilei\b", "Vittorya Arkilei"),
    (r"\bEuridice\b", "Euridiçe"), (r"\bOrfeo\b", "Orfeo"), (r"\bVincenzo Galilei\b", "Vinçentso Galilei"),
    (r"\bCristofori\b", "Kristofori"), (r"\barpicembalo\b", "arpiçembalo"), (r"\bBartolomeo\b", "Bartolomeo"),
    (r"\bLeipzig\b", "Layptsig"), (r"\bNiccolini\b", "Nikkolini"), (r"\bGalileo Galilei\b", "Galileo Galilei"),
    (r"\bScipione\b", "Şipyone"),
]

CH = dict(id="c14", n="XIV", title="Yıldızlar, Notalar, Taşlar", years="1584 – 1737", mood="bright", front="",
          paras=[[
              ("16. yüzyılın sonunda Roma'da, Papa XIII. Gregorius'un desteğiyle ve Büyük Dük Cosimo'nun oğlu Kardinal Ferdinando'nun himayesinde, bir Medici Doğu Dilleri Matbaası kuruldu.", None, "◐ M3:K66,D5 (Roma'da, Floransa'da DEĞİL; yıl 1584 HUD'da); P7 açılışı: hangi Cosimo (Cosimo I, Büyük Dük) — il Vecchio ile karışmasın"),
              ("Arapça harfleri Robert Granjon kesti; Arapça İncil, İbn Sina'nın Kanun'u ve Öklid bu harflerle basıldı.", None, "◐ M3:K66,K69,C58 (1590–91, 1593, 1594 HUD)"),
              ("Bunlar basılmadan önce İstanbul'dan bir ferman çıkmıştı: III. Murad, Arapça ve Farsça kitap getiren iki Avrupalı tüccarı koruma altına alıyordu; yasak değil, koruma.", None, "◐ M3:K68,C59,D9 (ferman Ekim 1588 HUD; Arapça İncil 1590–91, Kanun 1593, Öklid 1594 → \"Sonra\" yanıltıyordu; \"Osmanlı matbaayı yasakladı\" ile karıştırılmaz; ferman yılı 1587/1588 ayrışır ○ — yayın öncesi teyit)"),
              ("Tüccarlardan biri Orazio Bandini'ydi; evet, 1478'de Giuliano'yu vuranlardan biriyle aynı soyadı, ama bağ gösteren bir kayıt yok.", None, "◐ ad / bağ yok M3:TR#4; M2:§5.11 (göz kırpması; c8s10 geri çağrısı — P4'ten uzak izleyen için yıl+\"vuranlardan biri\" eklendi)"),
              ("İstanbul'da bu baskıların satışının beklenenin altında kaldığı anlatılır.", None, "○ M3:C60 (\"anlatılır\"; el yazması nüshaya talep ayrı)"),
          ], [
              ("Aynı yıllarda büyük dük olan Ferdinando, Uffizi'nin doğu kanadında sert taşla resim yapılan bir atölye kurdu: Opificio delle Pietre Dure; kurum bugün de çalışıyor.", None, "◐ M3:K67,K74,C57 (\"Avrupa'nın ilk saray manufakturası\" V&A betimi — söylenmez)"),
          ], [
              ("5 Ekim 1600'de Marie de' Medici'nin vekâleten evlendiği Floransa'da, ertesi gün Pitti Sarayı'nda bu düğün için Euridice ilk kez sahnelendi.", None, "◐ M3b:b4,b5; M4b:b40 (\"ertesi gün\" hesap bize ait; vekil kimliği söylenmez; salon/ışık/alkış kaynakta YOK)"),
              ("Jacopo Peri, Orfeo'yu kendisi söyledi; Euridice'yi Vittoria Archilei canlandırdı.", None, "◐ M3b:b5,b6,bd6"),
              ("Günümüze müziği ve librettosuyla tam ulaşan en eski opera budur; Dafne daha önceydi, ama müziği kayıp.", None, "◐ M3b:b3,b5,bm3 (\"ilk opera / Medici icat etti\" DENMEZ)"),
              ("Caccini, kendi Euridice'sinin notalarını Peri'ninkinden altı hafta önce bastırmıştı.", None, "◐ M3b:b7,bd7 (mizah: rekabet/kibir)"),
              ("Bu işin kuramcılarından Vincenzo Galilei, astronom Galileo'nun babasıydı.", None, "◐ M3b:b1 (Britannica; Plutarkhos bağı)"),
          ], [
              ("7 Ocak 1610'da Galileo, Jüpiter'in yanında üç küçük “yıldız” fark etti; ocak bitmeden sayı dörde çıktı.", None, "◐ M3b:b10 (gecenin havası/sesi/ışığı kaynakta YOK; Galileo'nun iç dünyası YOK)"),
              ("Şubat'ta saraya iki seçenek sundu: yeni gökcisimlerine yalnız genç Büyük Dük II. Cosimo'nun adı mı verilsin, yoksa dört kardeşin adı mı?", None, "◐ M3b:b11,bd1,bs4 (kardeşler Cosimo, Francesco, Carlo, Lorenzo; mektup tarihleri söylenmez)"),
              ("Saray ikincisini seçti; 13 Mart'ta Venedik'te çıkan Sidereus Nuncius'un, yani Yıldız Habercisi'nin kapağında “Medici yıldızları” yazıyordu.", None, "◐ M3b:bm1,b9,bd3 (seçimi kimin yaptığı ÇELİŞİR → kişi atfı YOK; \"teleskop gözlemine dayanan ilk eser\" DENMEZ)"),
              ("Kitap Cosimo'ya ithaf edilmişti; Galileo bir nüshayı, teleskopla birlikte Büyük Dük'e gönderdiği yazılır.", None, "◐ ithaf / ○ teleskop (19 Mart) M3b:b9,b13 (\"gönderdi\" = teslimat çerçevesi; ekranda \"TESLİMAT #N\" YOK)"),
              ("O yaz Padua'dan ayrılıp “Büyük Dük'ün Birinci Matematikçisi ve Filozofu” oldu; ders verme yükü yoktu.", None, "◐ M3b:b14 (atama günü 10 Haz ↔ Tem ↔ 1611: \"o yaz\"; maaş söylenmez)"),
              ("Ama adlar tutmadı: bugün kullandığımız uydu adları Marius'un.", None, "◐ olgu; adların kendisi HAFIZA-Y M3b:bm1 (mizah: yıldızlar aileye zimmetlendi, kayıtlar tutmadı)"),
          ], [
              ("1633'te Galileo yargılandı. Yargılanan kitabı Dialogo, Büyük Dük II. Ferdinando'ya ithaf edilmişti; Ferdinando aklanmasını istedi, mahkûmiyetten sonra da temkinli girişimlerde bulundu.", None, "◐ M3b:b18 (MİZAH KAPALI; masraf iki anlatımı söylenmez — b19,bd5,bm2)"),
              ("Medici Galileo'yu kollayabildiği yere kadar kolladı.", None, "YORUM/◐ M3b:bm2 (ağır sahne: süssüz)"),
          ], [
              ("17. yüzyılın sonlarında Büyük Dük III. Cosimo'nun oğlu Prens Ferdinando, Padovalı klavsen ustası Bartolomeo Cristofori'yi sarayın enstrümanlarına bakması için çağırdı.", None, "◐ M3b:b24,b25 (1688/≈1690 HUD; iç dünya YOK)"),
              ("1700 tarihli Medici envanterinde bir satır var: Cristofori'nin “yeni icat ettiği”, çekiçli ve sönümleyicili bir arpicembalo.", None, "◐ M3b:b26,bd8 (çeviri bize ait; İtalyanca metin görülmedi; mizah: bürokratik ad)"),
              ("Bugünkü adının ilk biçimi, 18. yüzyılın başında Scipione Maffei'nin bir gazete makalesinde geçer: piano ve forte'li klavsen.", None, "◐ M3b:b28,bd10 (1711 HUD)"),
              ("Cristofori'nin yaptığı üç piyano bugüne kaldı; New York'ta, Roma'da, Leipzig'de.", None, "◐ M3b:b31 (1720, 1722, 1726 ekran kartı)"),
              ("Piyanoyu Medici icat etmedi; Cristofori'ye maaş verdi, aleti envantere yazdı.", None, "YORUM M3b:bm5,b30 (bölümün ipi: sahne, maaş, envanter)"),
              ("Büyük icatlar bazen envanterde tek bir satır olarak doğar.", None, "YORUM M3b:Aday3"),
          ], [
              ("Envanterdeki satırlar sürdü; ama o envanteri tutan ailenin kendi satırları azalıyordu.", None, "YORUM (K1 → c15)"),
          ]])

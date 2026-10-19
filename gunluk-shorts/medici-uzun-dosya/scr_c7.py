"""c7 — 26 Nisan 1478 (Pazzi suikastı). Brif: brif/c7_brif.md. AĞIR bölüm: MİZAH TÜM BÖLÜM KAPALI. Parça 3'ün ikinci bölümü (c6'nın hemen ardından; Medici/Pazzi bağlam özeti V2'ye gömülü, "önceki bölümde" yok). c7s19 = köprü cümlesi (Giuliano'nun yaşı yalnız c6s27'de).
Yıldız an: V4–V7 (Pazar sabahı; ayin içinde; SAAT/HAVA/KOKU/ÇAN YOK). "Paskalya" geçmez. Papa'nın sözü yazılmaz. Pazzi tarafının sesi yok — söylenir (V13).
Kapı: K1 (tanrısal kesinlik hakkı, bölümde tek): sonda YORUM → c8 V1 aforozu (gün söylenmeden; ay düzeyinde) anlatır."""
PRON = [
    (r"\bSanta Maria del Fiore\b", "Santa Maria del Fyore"), (r"\bRaffaele Riario\b", "Rafaele Riaryo"),
    (r"\bGirolamo Riario\b", "Cirolamo Riaryo"), (r"\bRiario\b", "Riaryo"),
    (r"\bFrancesco\b", "Françesko"), (r"\bJacopo\b", "Yakopo"), (r"\bAntonio\b", "Antonyo"),
    (r"\bStefano da Bagnone\b", "Stefano da Banyone"), (r"\bMontesecco\b", "Montesekko"),
    (r"\bSalviati\b", "Salvyati"), (r"\bPetrucci\b", "Petrutçi"), (r"\bCesare\b", "Çezare"),
    (r"\bLuca della Robbia\b", "Luka della Robbya"), (r"\bImola\b", "İmola"), (r"\bSixtus\b", "Sikstus"),
    (r"\bFederico da Montefeltro\b", "Federiko da Montefeltro"), (r"\bGuicciardini\b", "Gviçardini"),
    (r"\bGiulio\b", "Culyo"), (r"\bde' ", "de "), (r"\bMaffei\b", "Maffey"),
]

CH = dict(id="c7", n="VII", title="26 Nisan 1478", years="1478", mood="heavy", front="",
          paras=[[
              ("26 Nisan 1478, bir pazar sabahı.", None, "◐ M2c:Y08 (gün = hesap bize ait; \"Paskalya\" DENMEZ; saat YOK)"),
              ("Floransa'nın katedralinde, Santa Maria del Fiore'de, yüksek ayin yapılıyordu.", None, "◐ M2c:Y08; EI Pazzi"),
              ("Ayin, şehre yeni gelmiş genç bir konuğun onuruna yapılıyordu: 16 ya da 17 yaşındaki Kardinal Raffaele Riario, Papa'nın akrabası.", None, "◐ doğum 3 Mayıs 1461 (EN Wikipedia; italyonthisday) → 16 y 11 ay; DBI \"17\" ayrışır; \"onuruna\" Enc. machiavelliana; akrabalık M2:K41 ○ (\"kardinal yönetti\" söylenmez)"),
          ], [
              ("Floransa'yı Cosimo'dan beri, hiçbir unvan taşımadan, bir bankacı ailesi yönetiyordu: Medici.", None, "◐ M2:K11, C3.7 (Parça 2 özeti)"),
              ("1474'te Papa IV. Sixtus, papalığın bankerliğini Medici'den alıp Pazzi'ye verdi; iki yıl sonra şap tekelinin de aynı yoldan gittiği yazılır.", None, "◐ 1474 M1b:b21,U14 / ○ Haz 1476 M1b:b23 (\"yazılır\")"),
              ("Lorenzo, Papa'nın yeğeni Girolamo Riario'nun Imola'yı alması için para vermemiş, Salviati'nin Pisa başpiskoposluğuna girmesini de iki yıl engellemişti.", None, "◐ M1b:b21 (tutar söylenmez); M2c:Y01 DBI Salviati (kin = iç dünya DEĞİL)"),
          ], [
              ("1477'de Girolamo Riario, Başpiskopos Salviati ve Pazzi'lerden Francesco, Lorenzo'yla Giuliano'yu ortadan kaldırmak için anlaştı.", None, "◐ M2c:Y05 EdP/DBI Salviati"),
              ("İlk planın bir ziyafette uygulanacağı, Giuliano gelmeyince saldırının kiliseye kaydırıldığı anlatılır.", None, "◐ çekirdek, ayrıntı ÇELİŞİR M2c:Y09,D55 (gün/yer söylenmez)"),
              ("Lorenzo'yu öldürmekle görevli paralı asker Montesecco, kilisede kan dökmeyi reddetti.", None, "◐ M2c:Y10 DBI Montesecco"),
              ("Yerine aceleyle iki papaz seçildi: Antonio Maffei ve Stefano da Bagnone; İtalyan Ansiklopedisi Treccani bu değişikliği planın kısmen çökmesinin nedenlerinden sayar.", None, "◐ DBI Montesecco özet tırnağı (\"Treccani'ye göre\"; parçada ilk Treccani → kısa tanım eklendi)"),
              ("Stefano, Jacopo de' Pazzi'nin kızına Latince öğreten papazdı.", None, "◐ Machiavelli VIII özeti (opsiyonel; kurbana alay YOK)"),
          ], [
              ("Kilise doluydu, ayin başlamıştı; Giuliano ise henüz gelmemişti.", None, "◐ M2c:Y11 Machiavelli VIII özeti"),
              ("Francesco de' Pazzi ile Bernardo Bandini onun evine gidip dil dökerek onu kiliseye getirdi.", None, "◐ Machiavelli özeti \"preghi e arti\"; M2:K45"),
              ("Yol boyunca şakalaştıkları, Francesco'nun sarılır gibi yapıp Giuliano'nun giysisinin altında zırh olup olmadığını yokladığı anlatılır.", None, "◐ M2:K45/C7.2 (\"anlatılır\")"),
          ], [
              ("İşaret konusunda anlatılar ayrışır: kimi ayini yöneten papazın komünyon alışını söyler, kimi ekmeğin kaldırıldığı anı.", None, "◐ ↔ ◐ M2c:T1,D56 (Poliziano'ya atıf YOK)"),
              ("Ekmek kaldırılırken herkesin diz çökmesi gelenekti.", None, "◐ liturji bilgisi (opsiyonel)"),
          ], [
              ("Bandini kısa bir silahı Giuliano'nun göğsüne sapladı; Giuliano birkaç adım gidip düştü.", None, "◐ M2c:Y14 Machiavelli VIII özeti (kan gösterilmez)"),
              ("Francesco üstüne kapanıp defalarca vurdu; yara sayısı 19 diye sayılır.", None, "◐ 19: Wikipedia, Gardner/Staley, Magenta; 18 bir kaynakta M2c:Y15"),
              ("Ama hedef yalnız Giuliano değildi.", None, "◐ M2c:Y05 (plan iki kardeşe yönelikti, c7s7; köprü cümlesi — Giuliano'nun yaşı yalnız c6s27'de, 24/25 tartışması tek yerde)"),
          ], [
              ("Aynı anda Lorenzo'ya iki papaz saldırdı.", None, "◐ M2c:Y16 EI + DBI Lorenzo + Gardner"),
              ("Lorenzo boynundan hafifçe yaralandı, kendini savundu ve sakristiye kaçtı.", None, "◐ M2c:Y16 (\"kılıç çekti\", \"pelerin kolunda\" söylenmez)"),
              ("Dostlarının, sakristinin ağır tunç kapısını arkasından kapattığı anlatılır; aralarında şair Poliziano da vardı.", None, "◐ Gardner + Britannica; adlar ÇELİŞİR M2c:T3 (\"anlatılır\"; kapıyı yapanlar — Luca della Robbia/Michelozzo — ekranda, seste değil: dostların adı sanılıyordu)"),
              ("Onu korumaya çalışan arkadaşı Francesco Nori, Bandini'nin hançerinden öldü.", None, "◐ Gardner + Staley + M2:C7.6"),
          ], [
              ("Giuliano'nun bedeni, katedralin papazları gelip toplayana dek yerde yattı.", None, "◐ M2c:Y19 DBI Lorenzo özeti"),
              ("Genç kardinal tutuklandı; halkın elinden kurtuldu ve haftalarca rehin kaldı.", None, "◐ M2c:Y20 DBI Riario + Enc. machiavelliana (12 Haziran söylenmez)"),
          ], [
              ("Aynı sırada Palazzo Vecchio'da Başpiskopos Salviati, bir grup adamla cumhuriyetin başı olan gonfaloniereyi öldürüp sarayı almaya çalışıyordu.", None, "◐ M2c:Y21 DBI Salviati (\"≈30 adam\" söylenmez; Petrucci'nin \"şişi\" YOK)"),
              ("Gonfaloniere Cesare Petrucci hileyi sezip alarm verdi; Salviati'nin adamları sarayda bir odada kapana kısıldı.", None, "◐ DBI Salviati + Reumont"),
          ], [
              ("Jacopo de' Pazzi, yüz kadar silahlı adamla meydana gelip halkı ve özgürlüğü yardıma çağırdı.", None, "◐ M2c:Y22 Machiavelli VIII özeti + Reumont"),
              ("Machiavelli'ye göre karşılık veren çıkmadı: halkı Medici'nin talihi ve cömertliği sağır etmişti, özgürlüğü ise Floransa pek tanımıyordu.", None, "◐ özet tırnağı; çeviri bize ait (\"Machiavelli'ye göre\")"),
              ("Sokaklarda ise Medici armasındaki toplara gönderme yapan “palle, palle” sesleri yükseliyordu; bunu Guicciardini yazar.", None, "◐ Guicciardini IV özet tırnağı M2c:Y23,D52 (Machiavelli'den DEĞİL)"),
          ], [
              ("Lorenzo'nun silahlı gençlerin koruması altında Medici Sarayı'na götürüldüğü, yaralı boynuyla pencerede göründüğü ve alkışlandığı anlatılır.", None, "◐ Gardner + Reumont (19. yy.) M2c:Y24 (\"anlatılır\")"),
          ], [
              ("Salviati, başpiskoposluk giysileriyle Palazzo Vecchio'nun penceresinden asıldı; yanına Francesco de' Pazzi getirildi.", None, "◐ M2c:Y25 DBI Salviati + DBI Francesco (asılı beden gösterilmez)"),
              ("Poliziano'ya göre Salviati, can çekişirken dişlerini Francesco'nun göğsüne geçirdi.", None, "ANEKDOT ◐ DBI Salviati özeti (\"cannibalism\") + Weinstein; D51 (alaysız, tek cümle)"),
              ("O gün yaklaşık otuz kişi daha idam edildi; aralarında Salviati'nin kardeşi de vardı.", None, "◐ M2c:Y26 DBI Lorenzo özeti (\"daha\" okuması teyit) + EI"),
              ("Kalabalık başkalarını kendi eliyle öldürdü.", None, "◐ M2c:Y26 EI"),
              ("Jacopo kaçtı, birkaç gün içinde yakalanıp asıldı; cesedinin sonraki pazar mezardan çıkarılıp sürüklendiği ve Arno'ya atıldığı yazılır.", None, "◐ olgu / ○ gün 27–29 / ○ ceset tek DBI M2c:Y27,Y28,D52,D53 (\"yazılır\")"),
              ("Toplamda seksenden fazla kişinin öldüğü de yazılır.", None, "◐ M2:§3 (tek sayı verilmez)"),
          ], [
              ("Bu işte Papa'nın payı bugün de tartışılır; iki taraf iki ayrı hikâye anlattı.", None, "YORUM + ◐ M2c:T2"),
              ("Floransa, Montesecco'nun hapisteyken, idamından kısa süre önce yazdığı itirafı yayımlayıp Papa'yı suçladı.", None, "◐ M2c:Y32 DBI Montesecco + Excusatio (öz-bildirim niteliği söylenir)"),
              ("Roma, Papa'nın bu işle ilgisini reddetti ve Lorenzo'yu aforoz etti; gerekçe, bir başpiskoposun kilise mahkemesine çıkarılmadan asılmasıydı.", None, "◐ M2c:Y35 EdP + DBI Salviati (düz ton; tarih c8'de)"),
              ("Treccani'ye göre Papa komployu büyük olasılıkla biliyordu; iki kardeşin öldürülmesini isteyip istemediği ise belli değil.", None, "◐ EI Pazzi + DBI Sisto IV M2c:T2 (\"Treccani'ye göre\"; Papa'nın \"sözü\" YOK)"),
              ("2023'te ortaya çıktığı anlatılan Maffei itirafı, Papa'yı, Napoli Kralı'nı ve Urbino Dükü'nü teşvikçi diye anar; ama o da zorla yazılmış olabilir.", None, "◐ M2:C7.11 (opsiyonel; \"anlatılır\"; kardinalin habersizliği söylenmez)"),
              ("Üstelik bu anlatıların çoğu Medici'nin süzgecinden geçti; Pazzi'lerin kendi sesi bu kaynaklarda yok.", None, "YORUM + ◐ M2c genel kaynak uyarısı (Poliziano, Excusatio, Machiavelli, itiraflar)"),
          ], [
              ("Giuliano 30 Nisan'da San Lorenzo'ya gömüldü.", None, "◐ M2c:Y30 DBI Giuliano"),
              ("Saldırıdan tam bir ay sonra, 26 Mayıs'ta, Giuliano'nun gayrimeşru oğlu Giulio doğdu.", None, "◐ M2c:Y34; M5:K24,P12 (Clemens adı c11'de)"),
              ("Aynı yıl bu olay bronza da döküldü: Bertoldo'ya atfedilen bir madalyanın bir yüzünde Lorenzo, ötekinde Giuliano var; yazılar “Halkın Esenliği” ve “Halkın Yası”.", None, "◐ NGA + V&A M2c:Y40 (atıf ○; çeviri bize ait; \"o sabah\" YANLIŞ okunuyordu — madalya sonradan, 1478 içinde)"),
              ("Lorenzo yaşıyordu; ama Floransa'nın Papa'yla barışı o sabah ölmüştü.", None, "YORUM (K1 — bölümde tek 'tanrısal kesinlik' hakkı)"),
          ]])

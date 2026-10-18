"""c15 — Son Medici'ler (1587–1737). Brif: brif/c15_brif.md. AĞIR/YORGUN. Mizah yalnız kaynağın kendi kara/kuru mizahı ve hafif: V1 (studiolo tarifi, iki haber başlığı), V3 (ruspanti), V4 (yönetmeyen varis).
MİZAH KAPALI: Francesco/Bianca'nın ölümü, Gian Gastone'nin yatağı/hastalığı/ölümü (ANEKDOT söylenmez), soyun bitişi. Yıldız an: Ekim 1587 (V1; dört yüzyıllık ölçek: 1587 → 2006 → 2010 → 2026).
'Zehir çürütüldü / çözüldü' DENMEZ → 'büyük olasılıkla sıtma'. 2026'daki 'Giovanni' söylenmez. Livornina + Mustafa Ağa + Fahreddin burada (c14'te YOK). 'Son Medici' yalnız Toskana'yı yöneten hat (Ottajano kolu ○).
Kapı: K1 (sade) → c16."""
PRON = [
    (r"\bBianca Cappello\b", "Bianka Kappello"), (r"\bLivornina\b", "Livornina"), (r"\bruspanti\b", "ruspanti"),
    (r"\bruspi\b", "ruspi"), (r"\bMustafa Ağa\b", "Mustafa Ağa"), (r"\bFahreddin\b", "Fahreddin"),
]

CH = dict(id="c15", n="XV", title="Son Medici'ler", years="1587 – 1737", mood="weary", front="",
          paras=[[
              ("I. Francesco, Palazzo Vecchio'da kendine bir oda yaptırmıştı: yarı ofis, yarı laboratuvar, yarı saklanma yeri, yarı merak kabini; kendisi dışında çok az kişi o odayı görmüştü.", None, "◐ M3:#62,cd55 (\"bugün şöyle tarif ediliyor\"; mizah a: kaynağın tarifi; porselen ○ söylenmez)"),
              ("Ekim 1587'de Francesco, eşi Bianca Cappello'yla birkaç gün arayla öldü.", None, "◐ Francesco 19 Ekim (Ferdinando'nun tahta çıkışı) M4b:b50 / H Bianca, \"bir gün arayla\" — hedge: \"birkaç gün arayla\""),
              ("Zehir söylentisinin o günlerde dolaştığı söylenir; zehirli turta hikâyesi ise sonradan anlatılmıştır, ilk anlatıcısı bilinmez.", None, "H / ANEKDOT M4:3E#3,§5.15 (\"söylenir\"; çağdaş kayıt H)"),
              ("2006'da bir çalışma kalıntılarda arsenik, 2010'da bir başkası sıtma antijeni bulduğunu bildirdi.", None, "H künyeler (Mari ve ark. BMJ 2006; Fornaciari ve ark. 2010) M4:#90,#91 — yayın öncesi teyit"),
              ("2026'da ise Francesco'nun üç kaburgasından alınan örneklerde iki sıtma parazitinin DNA'sı bulundu.", None, "◐ basın (Yale, CNN, Science; makale açılmadı) M4:#92,3E#1 — \"basına göre\"; yöntem/örnek ayrıntısı verilmez"),
              ("Bir haber başlığı “kitabı kapattı” dedi, bir başkası “çözülmüş olabilir”; aynı çalışma, iki ayrı kesinlik.", None, "◐ M4:3E#1 (mizah a: kaynağın kendi tutarsızlığı; kişiye değil)"),
              ("DNA bir enfeksiyonu gösterir, ölümün nedenini tek başına kanıtlamaz; ama dört yüzyıllık zehir hikâyesinin ağırlığı bugün sıtmanın tarafında.", None, "YORUM M4:3E#2,§5.15,D7 (\"büyük olasılıkla sıtma\" kalıbı)"),
          ], [
              ("Kardeşi Ferdinando, 13 yaşında kardinal yapılmıştı ve hiçbir zaman rahip olmadı; ağabeyinin ölümüyle 19 Ekim 1587'de büyük dük oldu.", None, "◐ M4b:b50 (EN Wikipedia + britishinstitute.it)"),
              ("Livorno'nun ticareti onun döneminde büyüdü; 1593'te ilan edilen Livornina, oraya gelen tüccara dinî özgürlük, af ve Toskana vatandaşlığı vaat ediyordu.", None, "◐ M4b:b52,b53,b31 (10 Haziran 1593 / taslak 1591; \"ilk serbest liman\" DENMEZ; hitap listesi ○ söylenmez)"),
              ("1598'de Sultan III. Mehmed'in mektuplarını getiren Osmanlı elçisi Mustafa Ağa Floransa'da ağırlandı, ama müzakere başarısızlıkla bitti.", None, "◐ M4b:b54,bD28 (Mercan 2023 özet; başarısızlığın nedeni araştırmada YOK)"),
              ("Ferdinando'nun 1608'de Dürzi Emiri Fahreddin'le yaptığı antlaşmanın, İstanbul sıkıştırırsa Toskana'da sığınma güvencesi içerdiği yazılır.", None, "◐ M4b:b58,bD30 (Aramco World 2014; journals.ku.edu)"),
              ("Fahreddin gerçekten 1613'te, II. Cosimo döneminde geldi.", None, "◐ M4b:b59,bD30 (sürgün Cosimo II dönemi)"),
          ], [
              ("III. Cosimo elli üç yıl hüküm sürdü; dönemi çoğu anlatıda gerileme diye geçer, ama bu anlatı tek bir kaynak hattına dayanıyor.", None, "○ M4b:b63,bM12 (\"53 yıl\" ○ → \"yazılır\"; sektörel nüans)"),
              ("Oğlu Gian Gastone 1723'te büyük dük oldu; çevresindeki 379 adama “ruspanti” derlerdi, çünkü adlarını altın sikkelerden, yani “ruspi”den alırlardı.", None, "◐ M4b:b66,bD19 (Treccani DBI Paoli 2000; mizah a: adını paradan alan çevre; yatak/hastalık ANEKDOT söylenmez)"),
              ("Treccani'nin 1932 tarihli maddesi onu devlet işlerine kayıtsız bulur ama saltanatını bir onarım sayar.", None, "◐ M4b:bD20 (çeviri bize ait)"),
              ("2010 tarihli maddesi ise tek reformunun üniversiteyi Aristotelesçilikten kurtarmak olduğunu yazar.", None, "◐ M4b:bD21 (iki hüküm ayrışır; çeviri bize ait)"),
          ], [
              ("Gian Gastone 9 Temmuz 1737'de öldü; Treccani'ye göre artık kendi devletinin hükümdarı değildi, çünkü devleti Lorraine Dükü Francis Stephen'ın birlikleri işgal etmişti.", None, "◐ M4b:b68,bD22 (IT + TR çeviri bize ait; Dami \"29 Temmuz\" çelişkisi söylenmez)"),
              ("Toskana'nın geleceği Viyana'da kararlaştırılmıştı; yeni büyük dük Francis Stephen Floransa'ya yalnızca bir kez, 1739 başında geldi.", None, "◐ M4b:b69,b70 (mizah a kuru: yönetmeyen varis)"),
              ("Erkek hat kapanmıştı; geriye bir kadın ve imzalanacak bir sözleşme kalmıştı.", None, "◐ M4b:b68,b73 (K1 → c16)"),
          ]])

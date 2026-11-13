# Tur 3 → v3.1 düzeltme listesi (başkan; tur 3 raporları geldikçe büyür)

Neredeyse bütün segmentler etkilendiği için v3.1 tam zincirle üretilir (`VER=v31 bash p1_uret.sh`, ≈45 dk). Sonra ilgili üyelerle tek üyeli gerileme kontrolü yapılır.

**Kim yapıyor:**
- **B:** başkan.
- **SCN-3:** `c2_kinds.py`, `scenes_c2.py`. Brif: `duzeltme_tur3/BRIF_SCN-3.md`.
- **ENG-E:** motor, c0, c1. Brif: `duzeltme_tur3/BRIF_ENG-E.md`.

| # | Kaynak (önem) | Madde | Kim | Durum |
|---|---|---|---|---|
| 1 | SA2-Y10 (önemli, hassasiyet) | Mitra ikonunda Othala rününe benzeyen işaret → titulus + circulus, inciler, Latin haçı | B | **yapıldı** (f0bdaad) |
| 2 | KA2-N1 + KA1-N1 (önemli) | Konstanz: işaret eden kol öndeki din adamının ensesinde | B | **yapıldı**: rahip x 2060→1880; 444,4 karesinde ayrık (bf1645b) |
| 3 | KA2-N2 + KA1-N2 (önemli) | Türkçe bloklar özet: "TÜRKÇESİ ÖZET · ÇEVİRİ BİZE AİT" (Cavalcanti) ve "TÜRKÇE SATIRLAR ÖZET · ÇEVİRİ BİZE AİT" (iki sayfa) | B | **yapıldı**: 563,5 ve 567,5 karelerinde (bf1645b) |
| 3b | KA1-N2 (isteğe bağlı) | Machiavelli İtalyancasına "…non vi recherà mai né invidia né pericolo, perché…" (teyit_P1.md:92) | SCN-3 | **yapıldı** (SCN-3; 567,6 karesinde teyit metniyle birebir) |
| 4 | KA2-N3 + KA1-Y3 (küçük) | "DEFTERLER GÖSTERİR" "defterler" sözcüğünde basar | B | **yapıldı**: 515,5 (bf1645b) |
| 5 | KA2-N4 + KA1-Y2 (küçük) | "O KALEM" çekiminde HUD gizli | B | **yapıldı**: 577,5 (bf1645b) |
| 6 | AN2-Ö1 + PK2-N1 (önemli; 9,5'in ana maddesi) | Üstten açık defter 4 kez → en çok 2; #83 ≥2× yakın plan, #88 eğik ya da sandık; sayfalar başlığı yazılı açılır | SCN-3 | **yapıldı** (SCN-3): #72 ve #85 üstten, başlıklar yazılı açılıyor; #83 kızıl kadife kasada el+anahtar ≥2× yakın plan, bilgi kapağa iğneli şeritte; #88 üç çeyrek eğik ciltli defterler + sandık |
| 7 | SA1-Y6-k + AN2 (önemli) | Defter içi arayüz grafikleri (dolum çubukları, 9.780 hane bloğu, tik eksen) → mürekkep ve tüy kalem | SCN-3 | **yapıldı** (SCN-3): elle çekilmiş eksen ve el yazısı yıllar; 9.780 hane beşli çetele (ilk 137 yaldızlı); KAYITLI SERVET mürekkep taraması |
| 8 | SA2-Y11 (küçük) | 1511 öncesinde papa sakalsız | B | **yapıldı** (e7d6e73) |
| 9 | SA2-Y12 (gerileme) | 416–431,6 çifte kayıt çizelgesinde HUD gizli | B | **yapıldı**: 420,0 (bf1645b) |
| 10 | SA2-Y13 (küçük) | PORTATA levhası Komün kalkanını örtüyor | B | **yapıldı**: "HANE BEYANNAMESİ · PORTATA" x 560; kalkanla arada ≥69 px (490,6–493,55) (bf1645b) |
| 11 | SA1-N1 (koşul) | Eğilen Giovanni'nin mitrası havada | B | **yapıldı**: mitra el nesnesi (e7d6e73) |
| 12 | SA1-N2 (koşul) | Mitra ara planında kol ağzı deseni taşıyor | B | **yapıldı**: kol ağzı yoluna kırpıldı (e7d6e73) |
| 13 | SA1-N3 (önemli) | 1737 belgesinde zikzak satırlar → asemik el yazısı (özgün Fransızca metin kaynaklarda yok) | ENG-E | **yapıldı** (ENG-E): yordamsal asemik el yazısı (harf alfabesi yok), 2× çözünürlük; K1 kapağı da yeniden çizildi |
| 14 | SA1-N4 + AN1-Y-N2 (küçük) | Kese ara planı: kol soluklaşıyor ve el oturmadan duruyor → geri çekilme, `settle`, bilek dönüşü; mitra ellerinde oturma ve itme | SCN-3 | **yapıldı** (SCN-3): çan eğrisi + %8 aşma, bilek dönüşü; kol keseyle kadrajdan çıkıyor |
| 15 | AN1-Y-N1 (küçük-önemli) | 367,9–369,3 ölü bağlantı (#63 harita donuyor → #64 boş parşömen) | SCN-3 | **yapıldı** (SCN-3): #63 itme kesmeye dek (ölçülen hareket medyanı 0,90 → 3,41); #64 BORÇ ilk karede |
| 16 | AN1-Y-N3 (küçük) | Kesme girişinde 1 karelik duruş: 43,9 (`c0_belge`) ve 575,5 (`c2_yakin`) | ENG-E + SCN-3 | **yapıldı** (ENG-E #8 0,19→0,47, #14 de; SCN-3 #98 0,10→2,06, #62 0,21→1,53) |
| 17 | AN1-Y7 (küçük-önemli) | Küçük hızlı nesnede deklanşör: florin yağmuru (389,5), damga düşüşleri | SCN-3 + ENG-E | **yapıldı** (ENG-E damga/yay/sikke/mühür; SCN-3 florin yağmuru 0→23, sadaka 0→18 alt-kare bulanık kare) |
| 18 | AN2 (küçük) | 559,7 kesmesinde CAVALCANTİ levhası ≈340 px sıçrıyor | SCN-3 | **yapıldı** (SCN-3; 559,6/559,8 karelerinde aynı yerde) |
| 19 | AN2 (küçük) | 471,7'de mitra ≈0,3 sn kayboluyor (#11 ile büyük olasılıkla kapandı) | SCN-3 | **kapandı** (SCN-3 kare kare doğruladı) |
| 20 | AN2 #91 + PK2-Y3 (küçük) | c2s28 sayfaları boş açılıyor | B | **yapıldı**: yazı ilk saniyede başlıyor (bf1645b) |
| 21 | KA1-Y1 (küçük) | Vieri levhası HUD 1378 altında → c1s26 başında 1385 | B | **yapıldı**: 293,5 (bf1645b) |
| 22 | PK1-G1, G2 (küçük) | Kapak QA görseli; YAYIN_TASLAK §6.8 | B | **yapıldı** (e7d6e73) |
| 23 | PK2-N2 (küçük, metin) | Bitiş ekranı 9:53'ten; P2 günü sol öğe; sabit yorumda P2 tarihi | B | **yapıldı** (5e4bd3a) |
| 24 | PK2-Y7 (küçük) | Çifte kayıt: "BORÇLULAR / ALACAKLILAR"; MİT damgası CREDITORI'yi örtmesin | SCN-3 | **yapıldı** (SCN-3) |
| 25 | PK2-Y8 (küçük) | Yankı eski K1 zemini (kenar grisi 17 → 38); kilitte beyaz parıltı | ENG-E | **yapıldı** (ENG-E): kenar grisi 16–23 → 38–45; sıcak yansıma |
| 26 | PK2-Y9 (küçük) | 271,1 sn kırmızı taşıma geçişi → nötr | ENG-E | **yapıldı** (ENG-E): mürekkep şeridi |
| 27 | PK2-Y5 (küçük, isteğe bağlı) | "FAİZ" bölüm etiketi | B | **değişiklik yok** (KURUL.md tur 3 kararı) |
| 28 | SA1-E-1 (P2'ye) | Yakın plan el silueti ("eldiven") | B | P2 öncesi motor işi; `sonraki_parcalar_notlari.md` |
| 29 | KA1 (P2–P7) | Loggia terası 1583'te eklendi → 1382–1582 terassız aşama | B | `sonraki_parcalar_notlari.md` |
| 30 | TE1-Y9 (önemli, yeni gerileme) | Kâğıt dokusu `BORDER_REFLECT` ile aynalanıyor (karelerin %44'ünde dikiş; 110,0 sn x≈1537) → döşenebilir doku + `BORDER_WRAP` | ENG-E | **yapıldı** (ENG-E): periyodik 3840×2160 karo + BORDER_WRAP; dikiş sütunu korelasyonu medyan 0,900 → 0,055 |
| 31 | TE1-Y11 + §8 (süreç) | `.done` özetine kod özeti; birleştirmede kod özeti, akış imzası, kare sayısı ve renk etiketi öz sınaması | B | **yapıldı** (render.py) |
| 32 | TE1-Y6 (küçük) | H.264 seviye 5.0 → 4.1 (`-refs 4 -level:v 4.1`) | B | **yapıldı** (render.py; deneme kodlaması seviye 41) |
| 33 | TE1-Y10, Y12 (küçük) | Uzun karanlık bitiş ekranında hafif bantlaşma; karmaşık karelerde SSIM 0,940 | B | **iş yok** (üye: "iş gerekmez"; bedel beklenen) |
| 34 | TE2-G1 (önemli) | Defter çekimlerinde kamera sayfadan ayrılınca yarım sözcük/sayı kadrajda (#85 "80 HANE", "7 HANE"; #72 "MEDİLER"; #83) → ayrılan sayfanın etiketleri söner ya da ≥90 px pay | SCN-3 | **yapıldı** (SCN-3): ayrılan sayfanın etiketleri söner; qa_yerlesim yarım yazı uyarısı c2'de 0 |
| 35 | TE2-G2 + G7 (önemli) | ETMEDİLER (416,5–421,4) ve KENDİ DEFTERİ (429,8–431,6) altyazı bandında → ≥80 px yukarı | SCN-3 | **yapıldı** (SCN-3): ETMEDİLER altı ≤769, KENDİ DEFTERİ altı ≤838 |
| 36 | TE2-Y5 kalanı | BELGE · DE ROOVER damgası fişsiz (466,9–469; ≈3,5:1) → `anim.paper_stamp` | SCN-3 | **yapıldı** (SCN-3) |
| 37 | TE2-G4 (gerileme) | FRANSIZCA damgası sağ kenarda (x≈1915) → sağ uç ≤1830 | ENG-E | **yapıldı** (ENG-E): harfler ≤1749, çerçeve ≤1830 |
| 38 | TE2-G5 | CİOMPİ LONCASI etiketi x≈1887 → ≥60 px sola | ENG-E | **yapıldı** (ENG-E): kamera anahtarlarıyla, sağ uç ≤1812 |
| 39 | TE2-G6 | Bitiş ekranı "2/7 · COSIMO": 28 → ≥34 px, tr_upper (COSİMO), ≥40 px yukarı | ENG-E | **yapıldı** (ENG-E): 34 px, COSİMO, satır 916–952 (yuvalar 54 px yukarı; bütün parçalar) |
| 40 | TE2-G8 | DEFTERLER GÖSTERİR ≈0,5 sn | B | **yapıldı** (#4: "defterler" sözcüğünde, ≈4 sn); SCN-3 #88'de korur |
| 41 | TE2 (süreç) | `qa_yerlesim` OWN_CAMERA yazılarını (world→ekran) ve sprite damgaları görmüyor; yarım görünen yazı kuralı yok | B | **kısmen** (B): yarım yazı UYARI kuralı eklendi (e1419b6); OWN_CAMERA yazılarının ekran uzayına çevrilmesi P2 öncesi motor işi |


**Başkan (SCN-3/ENG-E sonrası):**
- #95 'CAVALCANTİ'YE GÖRE' ve 'TÜRKÇESİ ÖZET · ÇEVİRİ BİZE AİT' levhaları y 880 → 850; özgün alıntı altındaki Türkçe satır aralığı 74 → 64. Levhalar iki satırlık altyazının (559,95–565,28) üstünde, 4. satırla çakışmıyor (565,3 karesi).
- 110,0 sn x≈1754'teki 'içerik aynalaması' (ENG-E notu) karede görülmedi: o sütunda simetrik çizilmiş asılı kumaşlar var. Pano kenar dolgusu bu çekimde yalnız başta ve sol kenarda, ≤35 katman px.
- Bütün oda önbelleği (230 dosya) silindi: belge çizimi değiştiği için odalardaki küçük belgeler yeniden çizilir.

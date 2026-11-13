# notlar_c4 — Kubbe ve Kefaret (1418–1460'lar) · sahne yazarı teslim notu (Parça 2 / c4)

## (a) Dosyalar ve çekim listesi özeti
- `scenes_c4.py` (43 çekim; `YIL_AT`: 1418 · 1420 · 1436 · (zaman atlamalı kubbede 1420→1436) · 1471), `c4_kinds.py` (c4'e özel ~26 çekim türü), ortak `p2_lib.py` + `c3_kinds.py` yardımcıları (etiket/damga/etiket-yapıştırma, torba, kâğıt, siluet kısayolları), `yonetmen_c4.md` (kart; satır sayısı ve tür sırası `scenes_c4.py` ile birebir), bu dosya.
- Akış: kubbeli silüet → yün loncası → yarışma ilanı/ödül → seçim → yumurta (gravür, 2 çekim) → Kolomb/Benzoni → 25 Mart 1436 → kutsama + koro → nota (Terribilis) → kubbe zaman atlaması → Eski Sakristi → Vespasiano → vicdan → Papa/San Marco → 10.000→40.000+ → «kefaret» etiketi → iki hücre/VIP → Rucellai (palazzolar, bal kavanozu) → Strozzi tablosu (şahinci) → Strozzi sarayı (1489) → Pazzi şapeli (1478) → Lippi (gravür) → defter/663.755 → Lorenzo'nun tepkisi → kefaret⇄yatırım terazisi + üç iz → kitap kulesi (c5 kapısı).
- Rehberin imza sekansı **«Kubbe kendini kurar»** (çekim 16) stok `build dome` ile yapıldı (kabuk sıra sıra, vinç, işçiler, `orbit`; `p` bilerek fener tamamlanmadan biter — iş emri tuzak 3: 'kubbe 1436'da tamam' denmez). Sonda **terazi** (çekim 41–42) ve **kitap kulesi** (43).
- Rivayetler gravür sepyası: Vasari'nin yumurtası, Lippi'nin odası. Vespasiano (yazar sesi) renkli ama ANEKDOT damgalı. 'Kefaret' kelimesi sahnede **sonradan yapışan beyaz etiket**tir (bölüm c3'te kurulan 'sonradan eklendi' dilinin devamı).

## (b) Bilinen kusurlar
- Palazzo (Medici/Rucellai/Strozzi), Pazzi Şapeli, Eski Sakristi kesiti, tablo (Üç Kral) ve San Marco/Osmanlı yapıları **genel temsil**dir (yeniden çizim, belge görseli değil; telif için bilerek). Tabloda 'Gentile da Fabriano · 1423 · yeniden çizim' alt yazısı bu yüzden var.
- Cinzel/Cormorant/IM Fell'de **Yunanca glif ve → ok yok**; Yunanca alfabe çizgilerle temsil edildi (c5), yıl aralıkları '–' ile yazıldı.
- Hücre planı soyuttur (kuşbakışı, iç donatı blok halinde); VIP etiketi bilinçli anakronik şakadır (YORUM damgalı).
- HUD yılı zaman atlamalı kubbede 1420→1436 yuvarlanır; Strozzi 1489 / Pazzi 1478 / Rucellai sahneleri HUD'u 1436'da bırakır (ekrandaki büyük yıl yazıları asıl göstergedir).
- Sahnelerde kamera zaman zaman parça içi 'zoomthru' ile aynı sahneyi iki çekime böler (medyan çekim süresini bantta tutmak için): ikinci çekim aynı türden başlar; geçişin ortasında iki çerçeve kısa süre iç içe görünür.

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
| ekran | sınıf · dayanak |
|---|---|
| KUBBE etiketi; Medici işareti çarpılı ('yaptırmadı') | ◐ M3:D1,§5.2 |
| YÜN LONCASI, KATEDRALİN YAPIMI; denetim anahtarı; kumaşa ✓, kubbeye ? ve ✗; yarışma tomarı | ◐ M3:K1,K3,D1 (ilk yarı YORUM, mizah) |
| AĞUSTOS 1418 ilanı; 200 ALTIN FLORİN; EYLÜL SONU takvimi; MODEL | ◐ M3:K2,S1,S2 |
| 1420 · BAHAR; BRUNELLESCHI, GHIBERTI; iki maket, seçilen mühürlenir | ◐ M3:K4 |
| VASARI, ANEKDOT; yumurta, rakipler, «BUNU BİZ DE YAPARDIK», plan tomarı | ANEKDOT ○ M3:C8,§5.3 |
| 1565, BENZONI, ○ TEK KAYNAK; yumurtanın Kolomb'a (gemi) uçuşu | ○ M3b:b105,bm9 |
| 25 MART 1436, FLORANSA TAKVİMİ, YILBAŞI | ◐ M3:K7 |
| PAPA IV. EUGENIUS; DUFAY · MOTET (YAZILDIĞI KABUL EDİLİR) | ◐ M3:K7,C9 |
| TENOR, KUTSAMA AYİNİ EZGİSİ, «Terribilis est locus iste», «NE HEYBETLİ BU YER.» (çeviri bize ait) | ◐ M3:C9 |
| AHŞAP KALIP YOK · KAYNAKLAR BÖYLE AKTARIR; 1420→1436 | ◐ rehber/blog düzeyi M3:K6,S4,D2 ('iskelesiz' denmiyor) |
| ESKİ SAKRİSTİ, SAN LORENZO, KATEDRAL, belgeli mühürlü kâğıt | ◐ M3:D1,K5,§5.2 |
| VESPASIANO · KİTAPÇI, COSİMO'NUN ÖLÜMÜNDEN SONRA, ANEKDOT; VİCDAN; ÇOĞU ADAM | ANEKDOT ◐ M1:D26, M3:C1,C3 |
| PAPA; SAN MARCO · DOMİNİKEN MANASTIRI; 10.000 → 40.000+ FLORİN | ANEKDOT ◐ M3:C2,S9; M1:K43 |
| «KEFARET» etiketi, SONRADAN, MODERN BİR YAZAR, KAYITLI DEĞİL | ◐ M1:D31,K43,mit7 |
| San Marco iki hücre: COSİMO İÇİN / KONUKLAR İÇİN; VIP, YORUM | ◐ M3:C5,K11 (VIP/YORUM = bizim şakamız) |
| MEDICI / RUCELLAI / STROZZI palazzo silüetleri; GIOVANNI RUCELLAI; ZİBALDONE; KAZANMAK / HARCAMAK; 50 YIL | ◐ M3:C10,D12 (Rucellai'ye ait, Cosimo'ya atfedilmez) |
| PALLA STROZZI; ÜÇ KRAL'IN TAPINIŞI (GENTILE DA FABRIANO · 1423 · YENİDEN ÇİZİM); şahinci; STROZZI + ERE = ŞAHİNCİ | ◐ M3b:b83,bd21 ('sanki imzalamış': niyet iddia edilmez) |
| STROZZI; 1489; MEDICI SARAYI; astrolog + gök diski | ◐ M3b:b87,b88 |
| PAZZI ŞAPELİ; ATFEDİLEN: BRUNELLESCHI; 1478 | ◐ M3b:b85,b86 (yan yana koyuş YORUM) |
| VASARI; FRA FILIPPO LIPPI; ANEKDOT; anahtar, makas, ip, açılan kapı | ANEKDOT ◐ M3b:bd22,b106 |
| LORENZO (GENÇ); 1434 – 1471; SADAKA · YAPI · VERGİ; TOPLAM 663.755 FLORİN | ◐ M1b:bD3,b59,U1 (hane toplamı; 'sanat' DEĞİL) |
| RICORDI · LORENZO; TOPLAMIN DIŞINDA | ◐ M1b:bD3 (çeviri bize ait) |
| KEFARET ⇄ YATIRIM terazisi; VİCDAN, ONUR, ÖLÜMDEN SONRA İÇİN BİR YER; YORUM | YORUM M3:§5.5,C1,C10,C15 |
| KİTAP (kule) | YORUM (c5 kapısı) |

Ekrana **koymadığım**: 600.000 florin 'sanata', kubbe maliyeti/4 milyon tuğla/114,5 m, 60.000 dukat Palazzo Medici, 'magnificence', 'Tanrı'yı borçlu yazamam', Lippi'nin kaçırma olayı, Pazzi komplosunun ayrıntısı (yalnız '1478' gölgesi), fener 1446–61 / top 1468–71.

## (d) Ana ajandan istekler / motor notları
1. `build dome`: son aşamada (fener+haç) tamamlanmadan durdurmak için `p`'yi çekim sonunu aşan bir çapaya gererek kullandım; belge/tuzak gereği 'fener/haç yok' seçeneği (`lantern=False` ya da `p_max`) olursa temizlenir.
2. Yazı tipi glifleri: Cinzel ve IM Fell'de Yunanca/ok yok, Cormorant'ta ○ ve → var; stok `CM.stamp` ○'yu boş bırakıyor (bkz. notlar_c3 §d.2). Ortak kit'e yedek yazı tipi/glif haritası eklenirse çözüm tek yerde olur.
3. `p2_ledger` (stok `ledger`): `at` sayı olmalı; `total=dict(amt=...)` yalnızca ilk sütuna yazılıyor; `focus` yerel defter koordinatıdır (belgelendirilmemiş).
4. `qa_flow` kartı: tablo satırı = çekim (zoomthru ile bölünen sahneler iki satır). Kart `/tmp` dışı bir üreteçten üretildi (`yonetmen_c4.md` elle düzenlenirse tür sırası bozulmamalı).
5. sfx dilekleri `yonetmen_c4.md` 'Ses köprüleri' satırında (sfx_cues_p2.json'a dokunmadım).

## (e) Kapılar (qa_flow --part 2 --chapters c4)
- Statik (--flow): kamera 43/43 · hareket yeterliliği 0 zayıf · gerekçeli geçiş %100 (çıplak fade %0) · tür tekrarı 0 · çapa: sözcük 28/cümle 31/mutlak 2 · yön 0 uyarı (yön bozma yok) · altyazı bölgesi 0 · kart uyumlu · çekim uzunluğu medyanı bantta.
- Örneklemeli (durgunluk, olay yoğunluğu) ve ms/kare: aşağıdaki 'Son sayılar' başlığında.

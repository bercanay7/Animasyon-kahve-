# PK1 — TUR 2 · Paket: kapak/başlık, tıklama vaadi · Medici Parça 1 (v2)

**Sınır:** videoyu oynatamadım, sesi dinleyemedim. Kare çıkardım (ffmpeg, v2 `out_p1/medici_P1.mp4`, 598,54 sn): 0,0–10 sn arası 12 kare; 63, 66,5–69, 101,5, 104, 339,5–345,5, 366,5–372,5, 375, 381, 390, 394, 413, 420, 477–502, 553, 560, 590,5–597 sn. Okuduklarım:
- kurul kanıt sayfaları `out_p1/kurul/genel_01–04`;
- `timeline.json` (cümle başlangıç zamanları);
- kapaklar: `studio_paketi_P1/kapak_P1_K1.jpg`, `_K2.jpg`, `out_p1/kapak/kapak_qa_P1.png` + `.json`;
- `kapak_medici.py`, `paket_P1.py`, `studio_paketi_P1/01–05`, `yayin/bolumler_P1.txt`, `yayin/YAYIN_TASLAK.md`, `SURUM_KUNYESI_P1.md`;
- `kurul/KURUL.md`, tur 2 raporları `KA1.md` ve `KA2.md`, tur 1 raporları `PK2.md` ve `SA1.md` (yalnız kapak ve paket bölümleri).

Ölçümleri kendim tekrarladım; QA aracına körü körüne güvenmedim. Scratch: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/pk1t2/`:
- `open_v2.png`: açılış ve kapak yankısı;
- `lock_map.png`: 1:07'deki kilit;
- `mid_v2a/b.png`: K2 vaadinin ödendiği kareler;
- `glints.png`: parıltı yıldızları;
- `cards_check.png`, `blank500.png`: kart sahneleri.

---

## 1. Karar

**ONAY — 9,0 / 10 (koşullu).** Koşul: aşağıdaki **Y1** ve **Y2** yayından önce düzeltilsin. İkisi de yalnız metin ve belge düzeltmesi; render ya da ses gerekmiyor. Düzeltilmeden yayınlanırsa puanım **8,0 (RED)** sayılsın.

| Parça | Tur 1 | Tur 2 | Gerekçe |
|---|---:|---:|---|
| Kapak K1 "SON MEDİCİ / MİRASI KİLİTLEDİ" | (B: 6) | **9,5** | Tek odak (kilit), "MEDİCİ" büyük harfi %18,3 (ölçtüğüm 136–139 px), 120 px'te okunuyor. Açılışın ilk 3,3 sn'si bu kapağın aynısı, kilit 1:07'de haritada tekrar kapanıyor: vaat 0. sn'de ve 67. sn'de ödeniyor |
| Kapak K2 "FAİZ YASAKTI" | (C: 6,5) | **9,0** | "FAİZ" %22,2 (ölçtüğüm 162–166 px). Florin yağan kese ironiyi tek bakışta söylüyor. Vaat 5:33–6:31'de ödeniyor ("FAİZ GÜNAHTIR" levhası, KİLİSE: FAİZ = TEFECİLİK, BORÇ ✗ FAİZ ✗ KUR FARKI ✓, kesede "FAİZ ✗", MÜŞTERİ: KİLİSE). 4 parlak leke (odak payı %78) |
| Başlık (T1) | 5,5 | **9,0** | 56 karakter, aranan ad başta, "NEDEN" yok; K1 ile tamamlayıcı, K2 ile pekiştirici |
| Açıklama ilk 2 satır | 6,5 | **8,0** | Metin doğru, ama 2. satırdaki "5:39" bölüm listesinin önüne geçiyor (Y1) |
| Bölüm damgaları | 6 | **9,0** | 9 bölüm; her biri cümle çapasında ve ≥ 10 sn (aşağıda doğruladım) |
| Sabit yorum | 7,5 | **9,5** | Soru önde, "(5:39)" tıklanabilir, dayanak satırı dürüst |
| Etiketler | 6,5 | **9,0** | Lorenzo/Cosimo/Uffizi çıktı; 311 karakter |
| Yayın talimatı + test planı | — | **7,0** | `YAYIN_TASLAK.md` ve `yayin/bolumler_P1.txt` eski paketi gösteriyor (Y2). Hangi kapağın varsayılan olduğu ve özellik yoksa ne yapılacağı yazılı değil (Y3) |

Benim alanımın çekirdeği (kapak, başlık, vaat–açılış uyumu) eşiğin üstünde. Kalan risk paketi Studio'ya taşıyan yazılarda.

---

## 2. Tur 1 maddelerinin durumu (kendi listem, `kurul/tur1/PK1.md`)

### 3a — Kapak

| # | Madde | Durum | Kanıt |
|---|---|---|---|
| 1 | [E] A/B/C başlık kartı; yerine K1/K2 | **KAPANDI** | K1/K2 üretildi; A/B/C `studio_paketi_P1/ESKI_kapaklar/`'a taşındı |
| 2 | [E] Hero büyük harf < %18 | **KAPANDI** | K1 "MEDİCİ" 132 px (%18,3); kendi eşik ölçümüm y 55–191. K2 "FAİZ" 160 px (%22,2); ölçümüm y 89–251. Benim önerdiğim 120 px'lik sapmaya gerek kalmadı: `kapak_medici.py` 76–81. satır "SON" 92 + "MEDİCİ" 132'yi aynı tabana koyuyor, böylece fare simgesi bölgesi de temiz. Önerimden iyi çözüm |
| 3 | [E] İkincil küçük yazılar | **KAPANDI** | K1 "MİRASI KİLİTLEDİ" 74 px (%10,3); K2 "YASAKTI" 104 px (%14,4); "ZAMAN KURYESİ", "PARÇA 1/7 · …" yok |
| 4 | [E] B "bir şehri bağladı" vaat hatası | **KAPANDI** | Yeni metin "MİRASI KİLİTLEDİ". KA2 tur 2: "SON MEDİCİ … kapak için kabul". "Kilitledi" mecazını video kendisi kuruyor: 1:07,6'da "çıkarılamayacaktı" sözcüğünde aynı altın kilit + zincir Büyük Dukalık'a kapanıyor, altında "3. MADDE · ÖZET: Koleksiyonlar … çıkarılamaz" kartı (`lock_map.png`) |
| 5 | [Ö] C "çifte defter" Medici-icadı mitini çağırıyor | **KAPANDI** | C emekli. Bölüm adı "6:52 Çifte kayıt: Medici'nin icadı mı?" (c2s12 6:52,9). KA2 K5 KAPANDI |
| 6 | [Ö] Doygunluk/kontrast | **KISMEN** | Hero kontrastı 11,8:1 / 12,1:1, gri farkı 186/190, tek ışık: hepsi tamam. Ama zemin, tur 1'de **benim önerdiğim** yakın-siyah. 168 px'te piksellerin %57'si < 25/255; kenar ortalaması ≈ 17, YouTube koyu temasının (≈15) aynısı. Ayrıntı Y4 |
| 7 | [Ö] Cinzel Black 900 | **KAPANDI** | Kapaklarda 900 ağırlığı; İ/Ş/Ğ doğru |
| 8 | [Ö] "1/7" rozeti 150×74 | **KAPANDI** | İki kapakta sol altta x 26–176, y 620–694 |
| 9 | [Ö] Süre rozeti ve fare simgesi bölgeleri | **KAPANDI** | QA "ihlal 0". Kendi bakışım: K1'de sağ alt düz kırmızı örtü, K2'de masa |
| 10 | [K] A kapağının çerçevesi | **KAPANDI (geçersiz)** | A kullanılmıyor; fresk yalnız 1:41'deki başlık kartı |
| 11 | [K] `kapak_medici.py` kuralı + QA | **KAPANDI** | `kapak_qa.py`: %18/%10, kontrast ≥ 7/4,5, gri farkı ≥ 70, odak payı ≥ 0,6, 246/168/120 px, gri ve bulanık, koyu/açık akış maketi, bölge kesişimi → çıkış kodu 1. Tur 1'de istediğimden fazlası |

### 3b — A/B çifti ve test

| Madde | Durum | Kanıt |
|---|---|---|
| K1 tarifi (belge + zincir + asma kilit, tek parlak odak, mühür, makara/silüet yok) | **KAPANDI** | QA: parlak leke 1, odak payı 1,0. Makara ve kesik silüet kalktı |
| K2 tarifi (hediye kutusu → **kese**, palle, etiket yazısı yok, 3. satır yok) | **KAPANDI (değiştirilerek)** | Kutu yerine kese: videonun 6:29'daki çekimiyle aynı nesne (`m_390.png`: kese + "FAİZ ✗"). Kapak–video tutarlılığı arttı; kabul ediyorum |
| Test düzeni (14 gün, başlık sabit) | **KISMEN** | `SURUM_KUNYESI_P1.md`: "Öneri: Test ve Karşılaştır, 14 gün, başlık sabit". Yazılı olmayanlar: varsayılan kapak (K1 olmalı, çünkü açılış yankısı K1), ilk yüklenecek kapak, özellik yoksa yedek plan. Y3 |
| Açılış ile kapak uyumu (Sisifos dersi) | **KAPANDI** | 0,0–3,3 sn kapak yankısı: kilit, belge, "SON MEDİCİ / MİRASI KİLİTLEDİ", "18 ŞUBAT 1743 · FLORANSA" künyesi. 3,3–3,7 sn ışık geçişiyle yatak odası. Anlatım 0,14 sn'de başlıyor, ölü hava yok |

### 3c–3h — Metin paketi

| Madde | Durum | Kanıt |
|---|---|---|
| 3c Başlık T1 | **KAPANDI** | `01_baslik.txt` 56 karakter |
| 3c "NEDEN" yok | **KAPANDI** | Kapakta da başlıkta da yok. Akış maketinde "Nasıl" iki kez yan yana (Cumhuriyet + Medici): kabul edilebilir, not olarak kalsın |
| 3c T2/T3 sonraki başlık testi için kayıt | **AÇIK (küçük)** | Hiçbir yerde yazılı değil; `YAYIN_TASLAK` §2'de P1 satırı hâlâ eski başlık (Y2) |
| 3c Seri ritmi, P2–P7'de soru/ifade dönüşümü | **AÇIK (sonraki parçalar)** | P4 alternatifi hâlâ "Defter Neden Kapandı?" (Y8) |
| 3d İlk 2 satır | **KAPANDI, bir gerilemeyle** | Benim tur 1 metnimdeki hata düzeltilmiş: "1743'te son Medici'nin imzaladığı sözleşme" yanlıştı (sözleşme 1737), yerine "…ölümünden" yazılmış, doğru. Ama aynı satırdaki "5:39'da" bölümleri bozabilir: Y1 |
| 3e Bölüm damgaları | **KAPANDI** | Benim "0:00 … 1743 sözleşmesi" hatam "1737" olarak düzeltilmiş. Çapalar (timeline): 3:01 → c1s11 3:01,4 · 3:34 → c1s15 3:34,5 · 4:37 → c1s24 4:37,8 · 5:39 → c2 bölüm kartı (c1 sesi 5:39,8'de biter; "FAİZ GÜNAHTIR" levhası ekranda) · 6:52 → c2s12 6:52,9 · 7:11 → c2s15 7:11,7 · 8:06 → c2s22 8:06,6. En kısa bölüm 19 sn. Kök dizindeki `bolumler_P1.txt` hâlâ eski 3 bölümlük liste: Y2 |
| 3f Sabit yorum | **KAPANDI** | Soru önde, "(5:39)" bağlantısı, "erişemediğimiz" cümlesi kalktı, "Sıradaki: 2/7" var |
| 3g Etiketler | **KAPANDI** | Önerdiğim ekler var ("Medici Ailesi Tarihi", "Mediciler", "Medici bankası", "faiz yasağı", "kambiyo", "Orta Çağ bankacılığı", "Floransa tarihi"); hashtag sırası doğru |
| 3h Aile ilkesi (P2–P7) | **KAPANDI (P1 için)** | Sıcak koyu zemin, altın Cinzel Black hero, krem ikincil, sol altta "n/7", sağda nesne, palle. P2–P7 bunu sürdürecek |

### §5 Motor iyileştirmeleri ve §6 kabul ölçütü

| Madde | Durum | Not |
|---|---|---|
| (a) Kapak QA otomasyonu | **KAPANDI** | — |
| (b) Tipografi + kapak modu | **KAPANDI, zemin dışında** | Zemin için Y4 |
| (c) İki kapak sahnesi | **KAPANDI** | Kilitli belge ve florin yağan kese |

Tur 1 kabul ölçütümün (§6) hepsi sağlanıyor. İki istisna: kapakta "parlak tek odak" K2'de 4 lekeyle sınırda; paket metinlerinde Y1.

---

## 3. Yeni sorunlar

**Y1 — [ÖNEMLİ, yayın öncesi; maliyet 1 satır] Açıklamadaki ilk zaman damgası "0:00" değil, "5:39".**
- `02_aciklama.txt`, 2. satır: "…5:39'da faiz yasağı ve 'vicdan komitesi'." (182. karakter). Bölüm listesi 1121. karakterde başlıyor.
- YouTube'un kuralı: listelenen ilk zaman damgası 0:00 olmalı. Topluluk deneyimine göre açıklamada listeden önce gelen bir damga özel bölümlerin oluşmamasına yol açabiliyor; resmî belgeyle doğrulayamadım.
- Bu satır **tur 1'deki benim önerimdi**; hatayı ben getirdim.
- Ne yapılmalı: 2. satırı damgasız yaz, örneğin: `1743'te son Medici'nin ölümünden 1252'de basılan ilk florine geri sarıyoruz; faiz yasağı ve "vicdan komitesi" de bu parçada.`. Tıklanabilir 5:39 bağlantısı sabit yorumda zaten var.
- `paket_P1.py` içine denetim ekle: açıklamadaki ilk `\d{1,2}:\d{2}` eşleşmesi "0:00" değilse hata ver.
- Yayından sonra bölümlerin ilerleme çubuğunda göründüğünü gözle doğrula.

**Y2 — [ÖNEMLİ, yayın öncesi; ≈15 dk] Yayın belgeleri eski paketi gösteriyor; kullanıcı Studio'da bunlara bakarsa geri dönüş olur.**
`yayin/YAYIN_TASLAK.md` dosyasında:
- §2, 22. satır: P1 başlığı hâlâ `Medici (1/7): Bankacı Aile Nasıl Doğdu? Florin ve Defter`.
- §3, 43–56. satırlar: P1 açıklaması eski. "buradan çıkarılamaz" tırnak içinde, "çifte kayıt defteri" geçiyor; yani tur 1'de kapattığımız iki vaat hatası.
- §3, 33. satır: "[BÖLÜMLER] yerine `bolumler_P*.txt`" diyor. `yayin/bolumler_P1.txt` hâlâ eski 3 bölümlük liste ("5:40 Defterin Sihri").
- 65. satır, P2 açıklaması: "Önceki: 1/7 — Bankacı Aile Nasıl Doğdu?".
- §6 madde 1: "Kapak: `kapak_P#_A.jpg` (B/C yedek)". A artık `ESKI_kapaklar/` içinde; bu talimatla eski kapak yüklenebilir.
- §6 madde 4: "parça başına 2–3 bölüm".
- §7: "● hiçbir satırda yok" (artık 51 ●).

Ne yapılmalı:
- P1 satırlarını "geçerli kaynak: `studio_paketi_P1/` (`paket_P1.py`)" diye işaretle ya da güncelle.
- `bolumler_P1.txt` dosyasını `05_bolumler.txt` ile eşitle ya da sil.
- P2'deki "Önceki" satırını yeni başlıkla yaz.
- §6.1'i şöyle yaz: "`kapak_P#_K1.jpg` varsayılan + `_K2` test".
- §6.4'ü şöyle yaz: "bölümler paket üreticisinden".

**Y3 — [ÖNEMLİ; ≈10 dk, Y2 ile aynı yerde] P1 için tek sayfalık yayın adımları yok.**
CLAUDE.md "adım adım bir yayin.md yazılır" diyor. Öneri: `studio_paketi_P1/00_yayin_adimlari.txt` dosyası, şu adımlarla:
1. Önce **K1**'i yükle; varsayılan K1 olsun. Açılışın ilk 3,3 sn'si K1'in birebir yankısı. Test sonuçsuz biterse ilk yüklenen kapak kalır; o da K1 olmalı.
2. Test ve Karşılaştır: K1 + K2, başlık T1 sabit, 14 gün. Test sürerken başlığa dokunma.
3. Özellik hesapta açık değilse (Anayasa §13-16 "doğrulanmalı"): K1 ile 72 saat. Gösterim başına izlenme süresiyle (TO × ortalama izleme; Prometheus dersi) değerlendir. 2–3 gün yeni dalga gelmezse K2'ye geç (kanal kuralı) ve aynı trafik kaynağında önce/sonra karşılaştır.
4. K2 kazanırsa açılışı kırpmaya kalkma: ilk cümle ("18 Şubat 1743, Floransa.") yankının altında, kırpılırsa kaybolur. Testin ölçtüğü izlenme süresi zaten bu açılışla ölçüldü, sonuç bu video için geçerli.
5. Bitiş ekranı: sol kutunun etiketi "SIRADAKİ PARÇA" ama P1 yayınlandığında P2 yok. Sol kutuya **Oynatma listesi: Medici (7 parça)** koy, P2 yayınlanınca P2 videosuna çevir. Sağ kutu "Abone ol".
6. T2 (`Medici (1/7): Son Medici Mirasını Kilitledi. Peki Nasıl?`) ve T3'ü (`Medici Ailesi (1/7): Faiz Yasaktı, Kilise Müşteri Oldu`; ○, kaynak üyesi onayıyla) sonraki başlık testi için not et.

**Y4 — [ÖNEMLİ ama engelleyici değil; ≈30 dk, render yok] Koyu temada kapağın kenarı sayfaya karışıyor.**
- 168 px ölçümü (kenar ortalaması / piksellerin < 25/255 payı):
  - K1: 17,6 / %57;
  - K2: 17,2 / %57;
  - Sisifos: 59 / %23;
  - Orfeus: 68 / %5;
  - Sultanın Öğrencisi: 123 / %0;
  - Şarlken madalyalar: 14 / %31.
- YouTube koyu teması ≈ 15. K1 ve K2 kanalın en koyu kapakları; kanalın en iyi tıklanan kapakları ise açık zeminli.
- Bu yakın-siyah zemini tur 1'de ben önermiştim (#140C08); düzeltiyorum.
- Ne yapılmalı: `kapak_medici.py` içinde `ton=(18, 10, 15)` → kenarlarda ≈ (44, 26, 22) (gri ≈ 30–35). Dış vinyeti kenarda koyulaştırma, merkezde topla. Hedef: 168 px'te kenar ortalaması ≥ 35, < 25 payı ≤ %35.
- Hero kontrastı yine geçer (hesap: altın 237,193,101 / zemin 44,26,22 ≈ 9,8:1; krem ≈ 14:1).
- `kapak_qa.py`'ye "koyu tema ayrışması" uyarısı ekle.
- Videodaki yankı yeniden render edilmez: yazı ve kilit aynı kaldığı için yankı kapağı hâlâ tanıtır.

**Y5 — [KÜÇÜK] Parıltı yıldızları stok/YZ kapak klişesi.**
- Konumlar: K1'de kilidin sol üst köşesinde (≈ x 545, y 472) dört kollu yıldız; K2'de kese ağzında (≈ x 914, y 173) sekiz kollu yıldız (`glints.png`).
- Ne yapılmalı: ışınları kaldır, yumuşak parlama (bloom) kalsın. Kapağın en parlak noktası yine aynı yerde olur. Kullanıcının sorusuyla doğrudan ilgili (bölüm 4).

**Y6 — [KÜÇÜK, SA2'ye] K2 kesesindeki arma 6 kırmızı top; videonun 1397–1429 bölüm kartı (5:41,5) 8 top.**
- 168 px'te fark görünmez. KA2 armayı dönemle uyumlu buldu (zambaksız).
- Tutarlılık için kapak da `donem.py`'nin 1397–1429 armasını kullansın ya da sanat üyesi 6'yı onaylasın.

**Y7 — [KÜÇÜK] QA akış maketi Medici süresini "10:02" (v1) gösteriyor; v2 9:58.** Yalnız maketteki sabit; etkisi yok.

**Y8 — [KÜÇÜK, sonraki parçalar] Seri başlık öneki tutarsız.**
- P1 `Medici Ailesi (1/7):`, YAYIN_TASLAK'taki P2–P7 `Medici (n/7):`.
- P5'te "Ailesi" eklenince 62 karakter olur; kısaltma gerekir.
- P4 alternatifi "Defter Neden Kapandı?" art arda "NEDEN" kuralına takılır.

**İsteğe bağlı, puanlanmadı — K3 (insan varlığı, yüz çizmeden):**
- Ne zaman: 48. saatte TO %2'nin altında kalırsa ya da gösterim bir yerde durursa.
- Nasıl: K1 düzeninde, kilitli belgenin arkasında büyük ve koyu bir peçeli kadın profil silüeti. Cumhuriyet'in "SULTANIN ÖĞRENCİSİ" kapağındaki dev silüet kalıbı; motorun zayıf olduğu yüz/el çizimini gerektirmez.
- Kanalda en iyi çalışan kapakların hepsinde bir insan var; K1 ve K2 yalnız nesne.

---

## 4. Kullanıcının sorusu: "Bu çizim tarzı çok mu basit, ucuz görünüyor; yapay zekâ ile üretilmiş gibi mi duruyor?"

Paket merceğinden kısa cevap: **kapaklar ve açılış ne ucuz ne de yapay zekâ işi gibi duruyor; videonun ortasında ise yer yer "slayt şablonu" gibi okunan kareler var.**

YZ izlenimi vermiyor. Her şey aynı mürekkep kontürü, aynı kâğıt dokusu, aynı palet ve doğru Türkçe tipografiyle çiziliyor. YZ görsellerinin bilinen izleri yok: erimiş el ve parmak, bozuk ya da uydurma harf, plastik parlaklık, tekinsiz yüz. Kapaktaki kilit videoda 0:00'da ve 1:07'de aynen var; bu da izleyiciye "kapak ile video aynı elden çıkmış" güveni veriyor.

Ucuz ya da şablon okunabilen üç yer var:
- **Tam ekran belgelerde gerçek yazı yerine kıvrımlı çizgiler.** 0:33–0:58 (13 madde / FRANSIZCA) ve 9:15–9:25 (Cavalcanti: neredeyse boş sayfada tek kıvrım) "yer tutucu" gibi duruyor.
- **Boş parşömen üstünde tek ikon + etiket kartları.** 7:56'da ≈3,5 sn yalnız anahtarlar; 8:14'te "%29,8" çubuğu; 6:09'da BORÇ / FAİZ / KUR FARKI kartları.
- **Kırmızı damga.** Neredeyse her sahnede tekrar ediyor; PK2'nin tur 1 bulgusuyla aynı.

Kapaklarda stok/YZ klişesine en yakın tek öğe, kilit ve kesedeki parıltı yıldızı (Y5).

Önerilerim:
- Belgelere dönem el yazısı havasında gerçek metin koy: depoda IM Fell ve Cormorant italik var, düşük kontrastla kullanılabilir; içerik, kaynak üyesinin verdiği sözleşme III. madde metni ya da açıkça temsilî bir metin olsun.
- Tek ikonlu kartlara bir dünya öğesi ekle (ör. anahtarı teslim eden bir el ya da figür).
- Damgayı yalnız gerçekten tartışmalı yerlerde kullan.
- Kapaklardaki yıldızları kaldır.

---

## 5. En emin olmadığım nokta

1. **Y1'in gerçek etkisi.** YouTube'un listeden önceki bir damga yüzünden özel bölümleri kurmadığını topluluk deneyimine dayanarak söylüyorum, resmî metinle doğrulayamadım. Düzeltme bedava, risk almaya değmez.
2. **K1 yankısının K2 koluna etkisi.** K2'ye tıklayan izleyici ilk 3,3 sn'de K1'in yazısını görüyor. Test bu açılışla ölçtüğü için sonuç bu video için doğru; ama "K2 kendi yankısıyla ne yapardı?" sorusunu yanıtlamıyor. P2–P7 için çıkarım sınırlı.
3. **Y4'ün TO'ya etkisi.** Kanalın açık zeminli kapakları daha iyi gitti, ama konu ve kitle de farklıydı; nedensel değil. Bu yüzden engelleyici yapmadım.
4. **Sesi duyamadım.** Başlığın ve kapağın vaadinin anlatımda ne kadar hissedildiğini (vurgu, ritim) bilemem.

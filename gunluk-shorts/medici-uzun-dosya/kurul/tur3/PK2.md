# PK2 — TUR 3 · Kanca/tutma ve paket · Mercek: "İLK KEZ GÖREN İZLEYİCİ" · Medici Parça 1 (v3)

Kanalı tanımayan, akışta kaydıran, sabırsız ve şüpheci izleyici gözüyle baktım. Önceki raporlarım: `kurul/tur1/PK2.md`, `kurul/tur2/PK2.md`.

**Sınır:** videoyu OYNATAMADIM, sesi DUYAMADIM. Değerlendirmem şunlara dayanıyor:
- **Kendi çıkardığım kareler** (`out_p1/medici_P1.mp4`, v3, 601,54 sn, ffmpeg): 0–13 sn, 0:15–1:56 arasında 24 kare, papa sahnesi 7:40–7:58, defter çekimleri 6:52–8:38, 8:54–9:01, MİT damgası 6:53–6:56, 4:31 geçişi, mekân setleri, bitiş 9:40–10:01,4 ve bitiş çerçevelerinin beliriş anı 9:51,3–9:52,9.
- **Belgeler:** `out_p1/kurul/hareket.json` (v2 ve v3), `out_p1/qa_flow_v3.txt` (102 çekim; 19 GEÇTİ / 2 UYARI), `timeline.json` (ses değişmedi), `yayin/studio_paketi_P1/00–05` (11:44 sürümü), kapaklar K1 ve K2 (07:07), `kurul/KURUL.md` ("Tur 2 — tam kurul sonucu" ve "v3 düzeltme planı"), `kurul/duzeltme_tur2/SCN-2.md` ve `ENG-D.md`, AN2'nin tur 3 raporu, `scenes_c2.py:216` ve `cilt_anim.act_admonish`.
- **Kanıt kareleri:** `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/pk2v3/`. Raporda adı geçenler: `pope3.png`, `pope474.png`, `blank3.png`, `ledgers3.png`, `droov3.png`, `mit3.png`, `end3.png`, `es3.png`, `outro596.png`, `open3.png`, `glint.png`, `carry3.png`, `sets3.png`, `early3.png`, `covers3.png`, `kart3.png`.

---

## 1. Karar

**ONAY — 9,1 / 10** (tur 1: 6,0 → tur 2: 8,5, koşullu 9,0 → tur 3: 9,1; eşik ≥ 9).

- Tur 2'deki iki ONAY koşulum kapandı:
  - **Y1 hançer:** v3'te silah yok.
  - **Y2 bitiş ekranının sol öğesi:** yayın adımlarına yazıldı.
- Bunlara ek olarak iki önemli maddem daha kapandı: **Y6** (bitiş ekranı) ve **Y3**'ün büyük kısmı (boş sayfalar).
- Puanı 9,5'ten uzak tutan yeni sorun: **N1**. Kart benzeri ekran süresi değişmedi (v2'de 279 sn, v3'te 278 sn; %46). Değişen yalnız biçimi: yüzen infografik kartların yerini üstten çekilmiş açık defter aldı. Bu kalıp 102 saniyede dört kez dönüyor. Engelleyici değil.

**Puan tablosu:**

| Parça | Tur 2 | Tur 3 | Tek cümle |
|---|---:|---:|---|
| Kapak (K1/K2) | 9,0 | **9,0** | Değişmedi. K2'deki arma artık 8 toplu, videoyla aynı (`covers3.png`) |
| Başlık | 9,0 | **9,0** | Değişmedi |
| İlk 5 sn (K1 kolu) | 9,0 | **9,0** | Yankı ve künye yerinde. İtme ve ışık süpürmesi eklendi. Yankı hâlâ eski K1 render'ı (Y8) |
| 15–90 sn | 8,5 | **8,5** | Gerileme yok. Kilit 1:07,8'de, çipler 1:47,5'te |
| Gövde ritmi | 8,0 | **8,5** | Hançer yok, her mekânın kendi seti var, el ve nesne yakın planları var. 4 sn'yi aşan durgun koşu 6'dan 2'ye indi (bitiş ekranı hariç). Kart payı değişmedi; defter ×4 (N1) |
| Bölüm geçişleri ve son | 8,0 | **9,0** | Cosimo kartı ≈2 sn okunuyor. Bitiş ekranı 10 sn, çerçeveler 1,4. sn'de beliriyor, "2/7" satırı var |
| Paket metni | 9,0 | **9,0** | Y2 uygulandı. Küçük: Studio'da bitiş ekranı başlangıcı 9:52 değil 9:53 olmalı (N2) |

---

## 2. Tur 2 maddelerimin durumu

### 2a. Koşullar ve yeni bulgular (Y1–Y9)

| # | Madde | Durum | Kanıt (v3) |
|---|---|---|---|
| **Y1** (koşul) | Papa hançer çekiyor; "AFOROZ TEHDİDİ" levhası papanın başını kapatıyor | **KAPANDI** | `scenes_c2.py:216` artık `action="admonish"`. `cilt_anim.act_admonish` belgesinde "threat (hançer) KULLANILMAZ" yazıyor. 7:51,8–7:55,8 arası karelerde (`pope3.png`) papa kurşun mühürlü belgeyi (bulla) tutuyor; 7:52,8'den sonra omuz–baş hizasına kaldırıyor. Hiçbir karede silah yok. Giovanni 7:53,8–7:54,8 arasında eğiliyor. Levha ≈ x 644–1276, y 100–180, kolun üstünde. Taç ve yüz açık (≈ x 1240–1360, y 180–340; `pope474.png`). Araya mitra ara planı girdi (7:50–7:51,7): ellerde mitra, sağdan papanın işaret eden eli. Olay artık "belgeyle yaptırım" diye okunuyor |
| **Y2** (koşul) | Bitiş ekranının sol öğesi ilk hafta aynı videoya dönüyor | **KAPANDI** (paket metni) | `00_yayin_adimlari.txt` 36–37. satırlar: P2 yayınlanana dek "İzleyiciye en uygun video"; "yalnız bu videoyu içeren oynatma listesini KOYMA… (kurul PK2-Y2)"; P2 çıkınca P2'ye çevir. Geriye kalan küçük etiket uyuşmazlığı için N2'ye bakın |
| **Y3** | Boş sayfa anları (7:04 ve 8:54,5) | **7:04 KAPANDI · 8:54,5 KISMEN** | **7:04:** çekimler tek kamera hareketinde birleşti (#72, 6:56,0–7:11,6). 7:04,0'da sol sayfada zaman çizgisi ve ETMEDİLER damgası var, kamera sağ sayfaya kayıyor, "MEDİCİ'NİN FARKI" yazılıyor (`blank3.png`). **8:54,5:** levhalar ("MACHİAVELLİ · BİR ASRA YAKIN SONRA", "CAVALCANTİ · 1430'LAR · HAPİSTE") ve iki sayfa çerçevesi ilk karede hazır, yani "iki kaynak" fikri hemen okunuyor. Ama sayfalar 8:54,6–8:56,4 arasında ≈1,8 sn boş. Yazı "kalemden" sözcüğünde (536,4) soluk İtalyanca satırlarla başlıyor. `hareket.json`'a göre 534,5–539,0 sn, bitiş ekranı dışında filmin en uzun durgun koşusu (4,5 sn; ortalama 2,7). AN2-K1 ile aynı bulgu. Küçük |
| **Y4** | K2'ye tıklayan, açılışta K1'in yazısını görüyor | **REDDEDİLDİ** (başkan) | Gerekçe (KURUL.md): Test ve Karşılaştır izlenme süresi payıyla seçer; uyumsuzluk izlenme kaybettiriyorsa test bunu ölçer. **Görüşüm:** kararı kabul ediyorum. Test bu açılışla ölçüldüğü için sonuç bu video için geçerli. Bedeli: test süresince K2 kolu kaybını telafi edemeyecek, ancak ölçecek. Ucuz önlem hâlâ Y5. P2–P7 için not: yankıyı yalnız varsayılan kapağa göre tasarlamak doğru; test kapağının vaadi ise ilk 15 sn'de bir kez görsel olarak anılsın (ör. P1'de "faiz" sözcüğü 1:32'deki "kılıç değil sikke" çekimine eklenebilirdi). Kullanıcıya not olarak kalsın |
| **Y5** | Bölüm kartı "DEFTERİN SİHRİ", K2 kolu için "FAİZ" sözcüğü yok | **AÇIK** (karar kaydı yok) · önemi **KÜÇÜK**'e indirdim | Kart 5:41–5:42,8'de "BÖLÜM II · DEFTERİN SİHRİ · 1397–1429". Köşe çipi 5:43,6'da "…N SİHRİ" (`kart3.png`). v3'te c2'nin görsel omurgası defter olduğu için başlık artık görüntüyle uyumlu; önemini bu yüzden düşürdüm. Kalan tek gerekçe K2 kolu: "FAİZ" sözcüğü videoda bölüm etiketi olarak hiç geçmiyor, yalnız açıklamadaki bölüm listesinde var (5:39). İsteğe bağlı |
| **Y6** | Bitiş ekranı kısa; 2/7'ye dair bir şey yok | **KAPANDI** | Bitiş 591,5 sn'de başlıyor, 10,0 sn. Çerçeveler 9:52,3'te soluk, 9:52,9'da tam (`es3.png`), son kareye kadar kalıyor (`end3.png`). Sol çerçevenin altında "SIRADAKİ PARÇA" ve "2/7 · COSIMO: SÜRGÜN VE DÖNÜŞ"; sağda "ABONE OL · ZAMAN KURYESİ" (`outro596.png`). Başlık kontrastı iyi |
| **Y7** | Çifte kayıt defteri İtalyanca; MİT damgası "CREDITORI"yi örtüyor | **KISMEN** · küçük | 412,9–415,1 sn'de tüy kalem aynı kaydı iki sayfaya yazıyor; her sayfaya bir sikke konuyor (`mit3.png`). "Bir kayıt, iki sütun" fikri artık görüntüyle anlatılıyor. Ü6'nın görsel karşılığı büyük ölçüde sağlandı. Kalan: Türkçe "BORÇLULAR / ALACAKLILAR" yok. Kâğıt fişli MİT damgası "derler" sözcüğünde (415,13) iniyor ve CREDITORI başlığını (≈ x 1460–1760, y 265–305) kesmeye kadar ≈0,8 sn tamamen örtüyor. Kabul edilebilir |
| **Y8** | Yankı eski K1 render'ı; 1–3 sn arası durağan | **KISMEN** · küçük | Durağanlık giderildi: yankıda +%7,9 itme ve ışık süpürmesi var; 1,0–3,0 sn kare farkı v2'de 0,5–1,0, v3'te 1,3–3,2. Kalanlar: (a) yankı hâlâ eski K1. 0,6 sn karesinin kenar grisi 17, yeni kapağınki 38; zemin daha koyu. (b) Kilidin sol üst köşesinde 0,3–3,0 sn arası küçük beyaz parıltı (≈ x 760–830, y 690–760; `glint.png`). Kollar kısalmış ama ışık lekesi duruyor. ENG-D de not etmiş (`k_kapak_kilit` varsayılanı `isinlar=True`; tek satır, sahne dosyasında). Tanınmayı bozmuyor |
| **Y9** | 4:31'de "isyanı ezdi" cümlesinin ardından kırmızı geçiş | **AÇIK** · küçük | 4:31,1–4:31,4 sn'de taşıma geçişi: kırmızı bant, üstünde mühür benzeri daireler, ≈0,3 sn (`carry3.png`). Rengi v2'dekiyle aynı. "Ezdi" sözcüğünün hemen ardından kırmızı silme hâlâ "kan" çağrışımına açık. Rengi nötrleştirmek tek parametre. KA2/SA kararına bırakıyorum |

### 2b. Tur 2'de kapanan K maddeleri: gerileme kontrolü

| # | Durum | Kanıt |
|---|---|---|
| K1 kapak, K16 rozet | Kapalı, gerileme yok | K1/K2 07:07 sürümü; 168 px'te ikisi de okunuyor (`covers3.png`) |
| K2 açılış yankısı | Kapalı (K1 kolu) | 0,0–3,3 sn K1 yankısı. Anlatım 0,14 sn'de başlıyor (`open3.png`) |
| K3 tarih künyesi | Kapalı | "18 ŞUBAT 1743" 0,5 sn'de, "FLORANSA" ≈2,5 sn'de, kilidin sağında koyu levhada |
| K4 yatak odası, "Medici" ilk ekranda | Kısmen (asıl amaç kapalı); değişmedi | 9,1 sn'de arma ve "ANNA MARIA LUISA"; 12,2 sn'de "MEDİCİ HANEDANININ SON ÜYESİ". Oda hâlâ yatan bir siluet |
| K5 liste + kilit | Kapalı | 1:00'da ikonlar; 1:07,8'de zincir ve kilit Büyük Dukalık'a kapanıyor; 1:09,5'te "3. MADDE · ÖZET" (`early3.png`) |
| K6 başlık kartı | Kapalı | 1:41–1:45 MEDİCİ freski, sessizlik ≈4,5 sn |
| K7 yol haritası çipleri | Kapalı | 1:47,5'te sol üstte "ALTIN" çipi |
| K8 durgun çekimler | Kapalı, daha iyi | 4 sn'yi aşan durgun koşu (kare farkı < 3): v2'de 6 (29 sn), v3'te 2 (8,5 sn): 534,5–539,0 ve 548–552. Bunlara ek olarak 593–601 bitiş ekranı (beklenen). Not: v3'te kâğıt dokusu dünyaya kilitli; ölçüm kısmen bu yüzden değişti (AN2) |
| K9 soyut mekanizmalar | **KAPANDI** (tur 2'de kısmendi) | Kambiyo: 5:55,8–6:01,1 arası ≥2× kese yakın planı (elden ele kese, poliçe karşılığında). Haritada kazanç sikkeleri. Çifte kayıt: Y7'deki çift yazım |
| K10 ad levhaları | Kapalı | 7:14'te GİOVANNİ ve BALDASSARRE COSSA levhaları ayrı (`sets3.png`); AN2 çakışma ölçümü 0 |
| K11 şablon hissi | **KISMEN** | Kapananlar: her mekânın kendi seti var (Roma bankası, Brugge'de Flaman pencereler ve dışbükey ayna, Konstanz'da kartallı sancak, Catasto'da zambaklı kalkan, Stinche hücresinde parmaklık ve zincir; `sets3.png`); üç yoksul artık kopya değil; damgalar kâğıt fişli. Açık kalan: kart benzeri süre değişmedi (N1) |
| K12 video sonu | **KAPANDI** (tur 2'de kısmendi) | 9:42,5'te "COSİMO · GİOVANNİ'NİN OĞLU" ve "39 YAŞINDAYDI" (sayaçsız, ≈2 sn); kule; Y6 |
| K13 bölümler, K14 başlık ve sabit yorum | Kapalı | Ses ve zaman çizelgesi değişmedi; 9 bölüm damgası geçerli. Sabit yorumun ilk satırı soru |
| K15 parşömen yamaları | Kapalı | Yeni kare yamasına rastlamadım |

### 2c. Ücretli öneriler (Ü1–Ü8)

**REDDEDİLDİ** (kullanıcı kuralı; tur 2'de kabul ettim). Değişiklik yok. Ü6'nın görsel karşılığı v3'te büyük ölçüde sağlandı (Y7).

---

## 3. Gerilemeler ve yeni sorunlar

### N1 — [ÖNEMLİ, engelleyici değil] Kart payı azalmadı, biçim değişti; aynı defter 102 saniyede dört kez

**Ölçüm** (qa_flow v3 aileleri; `c2_masa` ve `p1_ledger` "defter" olarak ayrıldı):

| | v2 | v3 |
|---|---|---|
| Kart benzeri süre (kart + kart* + defter) | 279 sn (%46,6) | 218 + 18 + 42 = 278 sn (%46) |
| 7:00–8:00 dakikasında kart benzeri pay | %58 | %58 (kart %32 + defter %26) |
| 8:00–9:00 dakikasında kart benzeri pay | %59 | %59 (kart %22 + defter %37) |

**Defter çekimleri** (`ledgers3.png`, `blank3.png`): #72 6:56,0–7:11,6 (15,6 sn; filmin en uzun çekimi) · #83 7:55,8–8:06,4 · #85 8:13,6–8:22,8 · #88 8:31,7–8:38,3. Dördünde de kadraj aynı: üstten açık defter, ekranı dolduran krem sayfa, ortada cilt çizgisi, tüy kalem.

**İzleyici olarak:**
- Defter, v2'nin "parşömen üstünde ikon" kartlarından iyi. Odadaki bankanın kendi defteri gibi okunuyor: mum, kalem canlı yazıyor, anahtarları bırakan bir el (7:56,8), tek kesintisiz kamera.
- Boş açılışlar kısa ve canlı. 7:56,3'te iki boş sayfa var ama kalem "PAPALIĞ…" yazıyor ve el 0,5 sn sonra giriyor. 8:14,2'de "CATASTO" başlığı ve hane sayacı (`droov3.png`). Ölü sayılmazlar.
- Sorun tekrar. Üçüncü defterde (8:13,6) "yine defter" derim. Üstelik bu, videonun en riskli bölgesi (6:52–8:54; sayı yığılması).

AN2'nin tur 3 Ö1 bulgusuyla aynı sonuç, farklı ölçümle.

**Ne yapılmalı** (ücretsiz; c2 segmentleri yeniden render):
1. Dört defterden en çok ikisi üstten tam açılım kalsın. Mantıklı olanlar #72 (çifte kayıt; "Defterin Sihri"nin kendisi) ve #85 (catasto sayımı).
2. #83'ü (kasa) masa yakın planına çevir: el ve anahtarlar çekimin baş öğesi olsun; "22 YIL + 18 YIL" şeridi sandığın üstünde ya da masaya serili bir şeritte dursun.
3. #88'deki "150.000+ florin kâr" vuruşunu defter dışına taşı: sandık ya da masada Giovanni.
4. Sayfalar başlığı yazılı açılsın; kalem yalnız yeni veriyi yazsın.

Bu iki değişiklik diziyi "defter – yakın plan – defter – sandık" ritmine çevirir. Puanımı 9,5'e taşıyacak tek ana madde bu.

### N2 — [KÜÇÜK; yalnız paket metni] Bitiş ekranının başlangıcı ve ilk hafta etiketi

**(a) Başlangıç saati.** `00_yayin_adimlari.txt` 35. satır "9:52'den" ve "çerçeveler 9:52'de belirir" diyor. Kareler (`es3.png`):
- 9:52,0'da kule hâlâ silinmenin altında;
- 9:52,3'te çerçeveler soluk;
- 9:52,9'da tam.

9:52,0'da konan Studio öğeleri kule görüntüsünün üstünde ve boş çerçeveler belirmeden açılır. **"9:53'ten videonun sonuna"** yazılsın: 8,5 sn, YouTube'un ≥5 sn sınırının üstünde.

**(b) İlk hafta etiketi.** Sol çerçevenin altındaki "SIRADAKİ PARÇA · 2/7 · COSIMO: SÜRGÜN VE DÖNÜŞ" yazısı (≈ x 280–900, y 905–1010) kalıcı ve P2 çıktıktan sonra doğru. Ancak ilk hafta çerçevenin içinde YouTube'un seçtiği başka bir video görünecek. `out_p2/` altında henüz render edilmiş video yok, yani bu süre en az bir hafta. Tıklayan "Cosimo" beklerken başka bir video bulur: küçük bir güven kaybı. Video ömrü boyunca doğru olan etiket bu, değiştirilmesin. Yayın adımlarına iki satır eklensin:
- "P2 yayınlandığı gün sol öğeyi P2'ye çevir."
- "P2'nin tarihi kesinleşince sabit yorumun son satırına yaz (ör. 'Sıradaki: 2/7, Pazar 20:00')."

YAYIN_TASLAK "Pazar + Çarşamba" ritmine izin veriyor. P2 hazır olursa erken yayınlamak bu pencereyi kısaltır.

"2/7 · COSIMO…" satırının büyük harf yüksekliği 1080p'de ≈18–20 px; telefonda okunmaz, TV ve masaüstünde okunur. Çerçevenin üstüne YouTube öğesi geleceği için işlem gerekmiyor.

### Gerileme taraması: başka bulgu yok

Şunlarda gerileme bulmadım:
- 0–2:00 arası 30 kare: yankı, künye, kilit, Uffizi'de "BUGÜN" çekiminde HUD gizli, başlık kartı, çipler;
- papa sahnesi;
- c2 setleri;
- 7:44,8–7:46,9 de Roover kartı: levha 7:45,0'da, damga 7:45,5'te, mitra 7:46,0'da; ≈0,5 sn boş, kabul;
- üç yoksulun kompozisyonu (9:33,5): ön planda büyük figür, arkada iki küçük figür; kopya hissi gitti.

Ses değişmedi; anlatım, SRT ve bölüm zamanlarıyla tutarlı (`timeline.json` 4 Kasım 22:13, `voice_chapters.json` aynı).

**Öncelik:** N1 → N2 → Y3 (8:54,5) → Y8, Y9, Y5, Y7. Hepsi ücretsiz; hiçbiri ses yaması gerektirmiyor.

---

## 4. Kullanıcının sorusu: "Bu çizim tarzı ucuz mu, yapay zekâ gibi mi?"

**Değişti, iyi yönde.**
- Yapay zekâ izi yine yok; ucuz da durmuyor.
- Tur 2'de saydığım "kâğıt bebek / şablon" işaretlerinin çoğu gitti:
  - papa artık hançer değil mühürlü belge tutuyor, yüzü açık;
  - yoksullar kopya değil;
  - her mekânın kendi seti var;
  - el ve nesne yakın planları var.
- Kalan iki iz:
  - figür oranlarının sadeliği: büyük, dikdörtgen cüppeler ve küçük başlar;
  - aynı üstten defter kadrajının 102 saniyede dört kez dönmesi. Kart benzeri süre aynı kaldı (%46), ama artık "parşömen üstünde ikon" değil "odadaki defter" olarak okunuyor; slayt hissi azaldı.

---

## 5. En emin olmadığım nokta

1. **Defter tekrarı tam hızda motif mi okunur, şablon mu?**
   - Bölümün adı "Defterin Sihri". Dört çekimde masa, ışık ve nesneler farklı; kalem ve el hareket ediyor. Oynatamadığım için tekrarın gerçekten göze batıp batmadığını göremiyorum.
   - Kart benzeri süre ölçümüm kaba bir vekil. qa_flow defteri "dünya" sayıyor; ben "kart" saydım.
2. **N2-b'nin etkisi.** İlk hafta "SIRADAKİ PARÇA · 2/7" etiketinin altında başka bir video görünmesinin tıklamayı mı düşüreceğini yoksa yalnız kafa mı karıştıracağını ölçemem. Studio'nun bitiş ekranı raporu gösterecek.
3. **K2 kolu (Y4).** Kararı kabul ettim; gerçek kaybı Test ve Karşılaştır'ın sonucu gösterecek.

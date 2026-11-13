# notlar_c7 — 26 Nisan 1478 (PERDE II) · Parça 3 sahne yazarı notları

Teslim dosyaları: `scenes_c7.py` (57 çekim) · `c7_kinds.py` (c7'ye özel türler + `c7_nave` dünyası + istasyonlar) · `p3_lib.py` (Parça 3 ortak yardımcılar, stilize madalya anahtarları) · `yonetmen_c7.md` · bu not.
Motor/ortak dosyalara dokunulmadı (compose.py, shots.py, cilt_*.py, qa_flow.py, sfx_cues_p3.json, parca.py); `cilt_cam.OWN_CAMERA` yalnız kendi modülümden `add` edildi (c7_nef, c7_oda, c7_sehir). Önbellek: `out/_cache/world/c7_nave_*` (nef kodu değişirse sil).

## 1. Kısıtlar (brif + yönetmen emri) ve nasıl uygulandı
- **Mizah KAPALI**: hiçbir çekimde şaka/alay/komik ayrıntı yok. Kurbana, yaraya, kardinalin yaşına, Salviati'nin son anına alay yok (yaş yalnız «16 ya da 17»).
- **Şiddet gösterilmez**: yalnız siluet (yüzsüz), işaret çizgisi (ince parlak çizgi), gölge, pigment yıkama (kızıl bulut), çetele (19 / ≈30 / 80+), lacivert leke. Beden düşmez; Giuliano yıkamaya karışarak solar; Nori solar; asılma yalnız pencere + levha; ip/ceset/kan yok. Poliziano'nun dişleme anekdotu çizilmedi (yalnız ANEKDOT damgası + kaynak).
- **Çan / saat / şafak / ışık koşulu / Paskalya / koku görüntüde de yok**: nef dünyası `c7_nave` çan sarkacı, şamdan-mum, asılı kandil, ışık huzmesi, buhurdan içermez (yalnız süzülen toz, sütunlar, vitray); «Pazar sabahı» yalnız tarih levhası + metin; kapı aralığı ışığı yalnız sakristi odasının mimari efekti. Meydan palle çekimi (37) motorun kendi gün→sıcak renk uyarlamasını taşır (saat yazılmaz).
- **Renk anahtarı** (brif): kireç beyazı → defter sarısı → tunç/pigment kızılı (yalnız saldırıda) → lacivert (yas; ekran örtüsü). **Gravür** yalnız ANEKDOT/«anlatılır» (çekim 12, 19, 38–39, 41).
- **Riario kartı**: «16 ya da 17» (24 kartı yok). **Bertoldo madalyası**: «Bertoldo'ya atfedilen», yazılar HALKIN ESENLİĞİ / HALKIN YASI + «çeviri bize ait».
- **Yıldız an (V5–V7, çekim 22–26)**: tek sert yön kırılması çekim 22 (`slide dir=l punch`); müzik 0,6 sn önce çekilir, sessizlik, tek ses köprüsü sakristi kapısı (26) → ayrıntı `yonetmen_c7.md`.

## 2. Ekrana konan olgular ve kaynak sınıfı (brif sınıfları)
| çekim | ekrandaki olgu | sınıf |
|---|---|---|
| 1–2 | 26 Nisan 1478 · Pazar; Santa Maria del Fiore'de yüksek ayin | ◐ |
| 3–4 | Kardinal Raffaele Riario «16 YA DA 17», «Papa'nın akrabası» | ◐ (yaş) / ○ (akrabalık) |
| 5 | Cosimo'dan beri unvan yok (kesikli taç) | ◐ |
| 6–7 | 1474 bankerlik Medici→Pazzi; 1476 şap tekeli «yazılır» | ◐ / ○ TEK KAYNAK |
| 8–9 | Imola için para verilmemesi; Salviati'nin Pisa'ya girişi 2 yıl engellendi | ◐ |
| 10–11 | 1477: Girolamo Riario, Salviati, Francesco de' Pazzi anlaştı | ◐ |
| 12 | ilk plan ziyafette, kiliseye kaydı | ANLATILIR (gravür) |
| 13–16 | Montesecco reddetti; Maffei ve Stefano; Treccani'ye göre planın kısmen çökmesi; Stefano Latince öğretmeni | ◐ / «Treccani'ye göre» |
| 17–18 | Giuliano gelmedi; Francesco+Bandini getirdi | ◐ |
| 19 | sarılır gibi yapıp zırh yoklama | ANLATILIR (gravür) |
| 20 | sinyal: komünyon ↔ ekmeğin kaldırılması (iki varyant) | ◐ ↔ ◐ |
| 21–23 | diz çökme geleneği; Bandini'nin saplayışı; yara sayısı 19 «diye sayılır» | ◐ |
| 24–30 | Lorenzo'ya iki papaz; sakristi, tunç kapı (kapatanlar «anlatılır», Poliziano ◐); Nori; Giuliano'nun bedeni toplanana dek; kardinal tutuklandı, rehin | ◐ |
| 31–35 | Salviati/Palazzo Vecchio; Petrucci alarmı; kapana kısılma; Jacopo meydanda; karşılık yok | ◐ |
| 36–37 | Machiavelli'ye göre (çeviri bize ait); «palle, palle» (Guicciardini yazar) | ◐ |
| 38–39 | Lorenzo saraya, pencerede, alkış | ANLATILIR (gravür) |
| 40–43 | Salviati+Francesco pencere; Poliziano'ya göre; ≈30 idam; kalabalık | ◐ / ANEKDOT |
| 44–46 | Jacopo kaçtı/yakalandı; cesedin Arno'ya atılması; 80+ | ◐ / ○ TEK KAYNAK / «yazılır» |
| 47–53 | taraflar: Montesecco itirafı (4 Mayıs), Roma/aforoz, Treccani, Maffei 2023, Medici süzgeci | ◐ / YORUM |
| 54–57 | Giuliano 30 Nisan San Lorenzo; Giulio 26 Mayıs; Bertoldo madalyası; barışın ölümü | ◐ |

## 3. Stilizasyon ve «temsil» notları
- Madalya portreleri (`c7_riario`, `c7_girolamo`, `c7_salviati`, `c7_fpazzi`, `c7_montesecco`, `c7_maffei`, `c7_stefano`, `c7_giulio`, Giuliano, Poliziano, Lorenzo/Giuliano bronz yüzleri) **prosedürel stilize profil**tir; yüz benzerliği iddiası yok; yazıtlar yer tutucu (·) ya da kaynaklı (SALVS PVBLICA / LVCTVS PVBLICVS).
- Nef (`c7_nave`) Lab-B `nave` dünyasının sadeleştirilmiş sürümüdür: genel gotik sütun/tonoz/vitray; gerçek S. Maria del Fiore iç mekânı iddiası yok. Sakristi ve Signoria odaları motorun genel odalarıdır (kendi lamba/avize/pencere ışıkları kalır).
- Figürler siluet (yüz yok); `threat` siluetinde motor kısa hançer sprite'ı ekler (yalnız jest).

## 4. Kapılar (qa_flow, Parça 3 / c7)
Tam (`--fast` değil) çalıştırma sonucu: bkz. aşağıdaki «QA ÇIKTISI» bölümü (teslim anında güncellendi).

## 5. Bilinen kusurlar
- Machiavelli alıntısı (36) tek yerinde duran alıntı kartıdır (yalnız itme + el yazısı); hareketi azdır.
- Çekim 22 (saplama) pigment yıkaması tüm ekranı kaplar; Program post'u üzerinde çok doygun görünebilir (sprite yoğunluğu `a=0.9`; istenirse `c7_kinds.pigment_bloom` alfa düşürülür).
- Giuliano'nun «henüz yok» kesikli silueti ve işaretler 0,5 ölçekli kontak sayfasında zor seçilir; tam çözünürlükte okunur.
- Sakristi/salon odaları motorun genel lamba/avize ışığını taşır (çan/saat iddiası değil ama «ışık»); `oda` için `lights=False` seçeneği yok.
- Ağır çekimler (22: 356 ms/kare) hariç tümü ≤260 ms/kare; bölüm ortalaması ≈150 ms/kare, tahmini render ≈20 dk (tek çekirdek).
- Gerçek ElevenLabs sesi geldiğinde süreler değişir: tüm çekimler cümle/sözcük kimliğine çapalı (mutlak saniye ≤%10); uzun cümlelerde (c7s10, c7s46) çekim bölünmeleri yeniden gözden geçirilebilir.

## 6. Motordan (ana ajan) istekler
Bloklayıcı istek yok. İsteğe bağlı: (1) `oda` sakristi/salon için `lights=False`/`sun=False` (ışıksız iç mekân); (2) `sehir meydan palle` için `tint=False` (gün→akşam uyarlamasız); (3) `cilt_cam.OWN_CAMERA` içine `c7_nef/c7_oda/c7_sehir` yerine dosya içi kayıt (şimdi modülden ekleniyor); (4) `pano` zoom>1,5'te band altına taşan figürler için `cams` y=None (otomatik dikey kayma) — c7_nef'te `_auto_y` ile çözüldü, ortak kit'e alınabilir.

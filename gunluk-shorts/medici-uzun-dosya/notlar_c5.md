# notlar_c5 — Konsil, Kitap, Platon (1439–1492) · sahne yazarı teslim notu (Parça 2 / c5, parça kapanışı)

## (a) Dosyalar ve çekim listesi özeti
- `scenes_c5.py` (33 çekim; `YIL_AT`: 1453 · 1463 · 1491; `OUTRO_TR = ("iris", 1.0, dict(obj="palle", at=(960, 491), r=100))`), `c5_kinds.py` (c5'e özel ~20 çekim türü), ortak `p2_lib.py` / `c3_kinds.py` / `c4_kinds.py` yardımcıları, `yonetmen_c5.md` (kart; satır = çekim), bu dosya.
- Akış: Ferrara→Floransa haritası → üç etken → yedi yüz kişilik Rum heyeti (2 çekim) → birlik (köprü, bulla; hilal) → İstanbul 1453 → Plethon (gravür, 2 çekim) → Yunanca/Chrysoloras → Niccoli / San Marco / halka açık kitaplık → Careggi mektubu → Orfik lir → alışveriş listesi → armağan → «Akademi» → bir yıl sonra → Lorenzo/Lascaris (harita, pazarlık, Athos) → cep defteri (2 çekim) → 200 ↔ iki kat liste → bilinmeyen pazarlık / tahtsız efendinin hesabı → liste → palla → **iris ile bitiş ekranı**.
- **Kapanış:** son çekimde liste yukarı kayar, tek kırmızı palla (r=100, (960,491)) büyür; `OUTRO_TR` iris'i aynı konum/yarıçaptan açılır (bitiş ekranında 'SIRADAKİ PARÇA' + abone ol Program'dan).
- Rehberin imza sekansı 'Konsil alayı (Gozzoli friz, pan r)' **kullanılmadı**: brif §10 konsilin tören/kalabalık/mekân betimini 'görüntüye de girmez' sayar. Yerine yedi yüz küçük figürlü levha, harita okları ve belge/defter nesneleri (brif §7 önerileri) kuruldu. 'Kitap yolculuğu şeridi 1494→1571' ve 'Poggio–Niccoli kopyalama' anlatıda yok → yapılmadı.

## (b) Bilinen kusurlar
- Doğu/Batı kiliseleri, Osmanlı yapısı, villa ve palazzo **genel temsil**dir (belge görseli değil). Cinzel/IM Fell'de Yunanca glif yok: Yunanca tahta çizgilerle temsil edildi.
- HUD yılı: 1453'ten sonra flashback çekimlerinde (Plethon 1439, Chrysoloras 1396–97, Niccoli) 1453'te kalır — ekrandaki büyük yıl yazıları (1396 – 1397 vb.) asıl göstergedir; HUD 1463 ve 1491'de güncellenir.
- Niccoli'nin ölümü şiddetsiz (siluet solar, boş koltuk); Cosimo ölümü c5s14'te **gösterilmez** (mektup + kum saati).
- Careggi: yalnız dış temsil (villa), Latince mektup metni okunmaz; 'tarla ✗ / zihin ✓' görseli mektup içeriğinin çevirisinden bizim kurguladığımız yorumdur (YORUM değil ama 'çeviri bize ait' notuyla).
- `c5_defter` ve `c5_bilinmiyor` en ağır çekimler (~200–270 ms/kare); el yazısı önbelleklendi, bulanık katman kırpıldı.

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
| ekran | sınıf · dayanak |
|---|---|
| 1439, KONSİL, FERRARA → FLORANSA | ◐ M3:K25,§5.7 |
| MASRAF · VEBA KORKUSU · COSİMO'NUN TEKLİFİ, BİRLİKTE, TEK NEDEN DEĞİL | ◐ M3:K25,§5.7 (Medici payı gerçek, tek neden değil) |
| AKTARILANA GÖRE; RUM HEYETİ; 700 (YAKLAŞIK); ○ TEK KAYNAK; EV SAHİBİ | ◐ teklif M3:K25 / ○ 700 M3:C20 |
| TEMMUZ 1439; DOĞU / BATI; LAETENTUR CAELI (bulla satırı); OSMANLI TEHDİDİ; yardım oku | ◐ M3:K26,TR#6,K23 (gün söylenmedi) |
| İSTANBUL, 1453, kırmızı halka; yarıda sönen yardım oku | ◐ M3:C21,K28 |
| FICINO'YA GÖRE, ANEKDOT; PLETHON · BİZANSLI FİLOZOF; KONSİL SIRASINDA; «İKİNCİ PLATON» | ANEKDOT ◐ M3:K27,C19 |
| YUNANCA ÖĞRETİMİ; 1453 çarpılı + MİT; MANUEL CHRYSOLORAS; 1396 – 1397 | ◐ M3:K23,§5.8 |
| NICCOLÒ NICCOLI; BORÇ; ≈800 EL YAZMASI (sayaç); SAN MARCO; HALKA AÇIK KİTAPLIK + YORUM | ◐ M3:K10,C7,Y5 ('ilk halk kütüphanesi' denmedi) |
| 1463 DOLAYLARI; FICINO'NUN DERLEMESİ; MEKTUP; CAREGGİ; TARLA ✗ / ZİHİN | ◐ M3:C16,K31 (tarih editör notu; çeviri bize ait) |
| PLATON; EN YÜKSEK İYİ; ORFİK LİR; FICINO | ◐ M3:C16 (Philebus teşhisi editör notu — ekrana yazılmadı) |
| LİSTE: EN YÜKSEK İYİ ✓ / BİR LİR ✓; BANKACI; YORUM | YORUM (laf sokma; Cosimo'nun sözü gibi sunulmadı) |
| PLATON'UN BÜTÜN ESERLERİ; ŞEHİRDE BİR EV; CAREGGİ YAKININDA BİR EV DAHA | ◐ M3:C17,K30 (yıl yazılmadı) |
| SONRADAN; «PLATON AKADEMİSİ» etiketi; TÜZÜK ✗; ÜYE KAYDI ✗ | ◐ M3:C18,§5.6; M3b:b98,bm10 |
| YAKLAŞIK BİR YIL | ◐ M1:K56 |
| LORENZO (TORUNU); JANUS LASCARIS; DOĞU; 1490 · 1491; II. BAYEZİD; EL YAZMASI; PAZARLIK; ATHOS | ◐ M3:K32,K33,TR#1; M2:K81 (tek sefer değil) |
| CEP DEFTERİ · JANUS LASCARIS; VAT. GR. 1412; İSTENEN METİNLER; KÜTÜPHANENİN İÇERİĞİ | ◐ M3:C23 (satırlar okunmaz çubuklar) |
| 200 EL YAZMASI + «200» balonu; YUNANİSTAN'DAN; LİSTE; NEREDEYSE İKİ KAT | ◐ M3:C24,S16 ('söyler') |
| KAYITTA YOK; FLORANSA'NIN TAHTSIZ EFENDİSİ; OSMANLI TOPRAKLARI; RUM BİLGİN | YORUM M3:Aday4,TR#1 |
| LORENZO İÇİN; LORENZO; palla | YORUM (c6 kapısı) |

Ekrana **koymadığım**: Poggio–Lucretius 14 yıl/50 kopya, 1417, ≈6.000 florin kartı (anlatıda yok), Plethon≈Platon söz oyunu, Argyropoulos/Chalcondyles yılları, Pico–Poliziano, 1494/1508/1524/1571 şeridi, Lorenzo'nun ölüm günü.

## (d) Ana ajandan istekler / motor notları
1. `OUTRO_TR` iris (palle, (960,491), r=100) ile kurguladım; palla yarıçapı/konum ortak kit'te sabitlenirse (OBJ_R['palle']) c5 son çekimi otomatik uyar.
2. Stok `map`: `labels` parametresinin bazı durumlarda çizilmediğini gördüm (c5s15 'DOĞU' etiketi görünmeyebilir); yedek olarak `over` etiketi kullandım.
3. `iconrow`/`mountain` gibi ek simgeler `icons_extra` içinde; `icons.draw_icon` adlarının listesi belgelenirse yeni simge aramak kolaylaşır.
4. Yazı tipi: bkz. notlar_c3 §d.2 (○, →, Yunanca).
5. sfx dilekleri `yonetmen_c5.md` 'Ses köprüleri' satırında (sfx_cues_p2.json'a dokunmadım).

## (e) Kapılar (qa_flow --part 2 --chapters c5)
- Statik (--flow): kamera 33/33 · hareket yeterliliği 0 zayıf · gerekçeli geçiş %100 (çıplak fade %0) · tür tekrarı 0 · çapa: sözcük 25/cümle 23/mutlak 0 · yön 0 uyarı (1 bilinçli: Osmanlı tehdidi) · altyazı bölgesi 0 · kart uyumlu · çekim uzunluğu medyanı bantta.
- Örneklemeli (durgunluk, olay yoğunluğu) ve ms/kare: 'Son sayılar' başlığında.

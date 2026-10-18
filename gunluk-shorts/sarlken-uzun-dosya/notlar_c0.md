# Bölüm 0 — Brüksel, 25 Ekim 1555 · yazar notları (BÖLÜM YAZARI D)

**Dosyalar:** `scenes_c0.py` (SHOTS) · `shots_c0.py` (c0_ önekli türler: `c0_forty`, `c0_fronts`, `c0_borc`, `c0_title`) · `scenes_d.py` (c0/c12 ortak: `d_pair` bastonsuz çift figür, `d_hall_gold` sahnesi, kamera/ekran dönüşüm yardımcıları) · `d_common.py` (D ortak: `A()` çapa yardımcısı, `wd_*` türleri, `tag`, `kick_rule`, `draw_hourglass` …).
**Süre** 46.1 sn · **14 çekim** · ort. 3.3 sn/çekim · `--check`: **uyarı yok** (bölüm ort. ≈ 140 ms/kare, en ağır çekim < 200 ms; 2× süper-örnekli stage.py ile ölçüldü).
**Ton:** sıcak altın/kara, merak. **Kimlik gizli:** isim levhası ilk kez s8'de (V. KARL); öncesinde yalnız yer (BRÜKSEL), yaş (55 YAŞINDA), sayı (40 YIL) ve harita var.
**Ayna bölüm:** c12 aynı salonun ikinci görünüşü (aynı `hall`; orada ağır altın ışık, çift kapıdan girer, tahtta kimse yok). c0'da kamera kalabalığa süzülür, c12'de ters yönden gelir.

## 1. Çekim listesi
| # | tür | bölüm içi | süre | etiket | ne gösteriyor |
|---|---|---|---|---|---|
| 0 | title | 0:00.0 | 2.9 | tarih | "25 EKİM 1555" altın başlık (sesle aynı anda, 0.35 sn'de) |
| 1 | theatre / hall | 0:02.9 | 3.9 | salon_genis | Salon geniş: kalabalık siluet, pencereden gün ışığı, ortada yaşlı + genç çift; "BRÜKSEL / büyük salon" levhası; kamera yavaşça kalabalığa iner |
| 2 | theatre / hall | 0:06.8 | 4.1 | cift_orta | Çift ortada; "55 YAŞINDA" levhası ince çizgiyle başa bağlanır ("elli" sözünde) |
| 3 | theatre / hall | 0:10.9 | 3.5 | omuz_yakin | Yakın plan: omuza dayanan el (BASTON YOK — kaynak kapısı) |
| 4 | c0_forty | 0:14.4 | 1.7 | kirk_yil | Kum saati akar + "40" sayacı ("kırk" sözünde sayar) + "YIL" ("yıldır" sözünde) |
| 5 | map | 0:16.1 | 2.3 | avrupa | Habsburg toprakları sırayla yanar (İspanya, Hollanda, Franche-Comté, Milano, Napoli, Sicilya, Sardunya); taralı "KUTSAL ROMA İMPARATORLUĞU"; "1555" |
| 6 | map (wipe) | 0:18.3 | 3.3 | yeni_dunya | Atlantik geniş kadraj; gemi İspanya'dan Karayipler'e; Yeni İspanya + Peru bölgeleri yanar; "YENİ DÜNYA", "ATLANTİK OKYANUSU" |
| 7 | theatre / hall | 0:21.6 | 3.3 | salon_birakma | Kamera geri çekilir, pencere ışığı taşar, çift yürür ("hepsini bırakmaya başlıyor") |
| 8 | medal | 0:24.9 | 2.1 | medal | İlk isim levhası: V. KARL · İmparator · 1500 – 1558 |
| 9 | emblem | 0:27.0 | 1.4 | neden | Soru işareti ("Peki neden?") |
| 10 | c0_fronts | 0:28.4 | 8.5 | cephe5 | "BEŞ CEPHE": beş kesikli yuva (I–V); bankacı, keşiş, kral, sultan, miras kendi sözcüğünde yuvaya oturur; bağlayan çizgi; sonda hepsi birlikte parlar |
| 11 | emblem | 0:36.9 | 3.8 | ilk_kanit | Taç + "İLK KANIT" |
| 12 | c0_borc | 0:40.7 | 3.2 | tac_borc | Taca sikke yağar ("büyük" sözünde), "BÜYÜK ÖLÇÜDE" + **BORÇLA** damgası |
| 13 | c0_title | 0:43.9 | 2.3 | baslik | "ŞARLKEN" + "ZAMAN KURYESİ · TESLİMAT" + "DÜNYAYI TESLİM EDEN İMPARATOR" (compose'un c1 başlık kartıyla kesintisiz, bkz. §2.9) |

Tür çeşitliliği: başlık ×2, diorama ×4 (3'lü seri + 1), sayaç/kum saati, harita ×2, madalya, simge ×2, özel ızgara (beş cephe), taç/sikke. En uzun diorama serisi 3 çekim (uyarı eşiği 4).

## 2. Bilinen kusurlar / dürüst notlar
1. **Çift figür sade bir siluet:** yaşlı imparator + genç prens (bere), el omuzda; yüz ayrıntısı yok (kimlik gizli, bilinçli). Geniş planda küçük; kalabalık siluetlerle kontrast için çiftin arkasına ılık bir hale (`halo`) konuldu.
2. **Baston yok:** `d_pair` figürü `figs_lab` parçalarından (`emperor_fig(cane=False)`, `prince_fig(sword=False)`) kuruldu; lab'ın hazır "çift"i bastonlu/kılıçlıydı ve kılıç kını baston gibi okunuyordu.
3. **"55 YAŞINDA" çizgisi** kamera fonksiyonundan hesaplanıyor (`scenes_d.scene_to_screen`); hall sahnesinin katman derinlikleri değişirse çizgi başın yanından kayar.
4. **Salon tahtı boş:** `emperor=False` (imparator figürü çift olarak ayrıca çiziliyor). c12 aynı salonu tahtı boş görür (ayna).
5. **Avrupa haritası:** bölgeler modern sınırlara yakın çokgenler (Milano dikdörtgensi); altta harita altyazısı "SINIRLAR YAKLAŞIKTIR". **Avusturya bilerek boyanmadı** (1555'te Ferdinand yönetiyordu; "Avrupa'nın büyük bölümünü yönetiyor" retoriği kaynaklarda DÜŞÜK risk). Almanya yalnız taralı (imparatorluk unvanı).
6. **Kum saati** akışı çekim süresince doğrusal doluyor (söze bağlı değil); sayaç "kırk" sözünde 0.45 sn'de 40'a oturur.
7. **Pencere ışığı taşması** (s7) ilave (additive) bir daire: en sonda salonun üstü bilinçli olarak beyaza yaklaşır.
8. **İlk kare maliyeti:** hall sahnesi ilk karede 3–7 sn pişer (önbellek sonrası ≈ 150–250 ms/kare); sıralı render'da sorun değil.
9. **Kapanış başlığı ↔ compose c1 kartı:** compose c0'dan sonra 3 sn'lik c1 başlık kartı (aynı "ŞARLKEN", at=−4 → kicker/alt başlık baştan tam, ölçek 1.06→1.00) ekliyor. `c0_title` çekimi ölçeği 1.00→1.06 büyütüp kicker + alt başlığı sesle birlikte getirir; kesme anında kare farkı ≈ 0 (ölçüldü: ort. mutlak fark 2/255). Compose'un başlık kartı değişirse bu çekim de güncellenmeli.

## 3. Ekrandaki olgular ve kaynak sınıfı (sınıf = `kaynaklar.md` cümle tablosu)
| Ekran metni / öğe | Çekim | Anlatıda | Sınıf / dayanak |
|---|---|---|---|
| 25 EKİM 1555 | 0 | evet (c0s1) | CONFIRMED (A5 #16) |
| BRÜKSEL · büyük salon | 1 | evet (c0s2) | YORUM/CONFIRMED (yer: A5 #16 Brüksel sarayı büyük salonu) |
| 55 YAŞINDA | 2 | evet (c0s3 "elli beş") | NİTELİKLİ (A1 #1: 24.02.1500 → 55 yıl 8 ay) |
| Kolunu genç prensin omzuna dayamış (el yakın planı, bastonsuz) | 3 | evet (c0s4) | NİTELİKLİ (A5 #17 yalnız "omzuna yaslanarak girdi"; baston kaldırıldı, bkz. METIN_DEGISIKLIKLERI) |
| 40 YIL (kum saati) | 4 | evet (c0s5) | YORUM (A5 #16 "tam 40 yıl önce"; A1 #6 NİTELİKLİ) |
| Habsburg toprakları (İspanya, Hollanda, Franche-Comté, Milano, Napoli, Sicilya, Sardunya) + KUTSAL ROMA İMPARATORLUĞU (taralı) · 1555 | 5 | "Avrupa'nın büyük bölümü" | YORUM (retorik; bölge çokgenleri yaklaşık). Milano/Napoli/Sicilya/Sardunya adları araştırmada kısmen (A5 #6 Milano/Napoli); haritadaki renklendirme genel bilgi |
| YENİ DÜNYA · ATLANTİK OKYANUSU · gemi + Yeni İspanya/Peru boyası | 6 | evet (c0s6) | CONFIRMED (A4 #2, #5; bölge çokgenleri yaklaşık) |
| V. KARL · İmparator · 1500 – 1558 | 8 | evet (c0s8 "tahttan") | CONFIRMED (A1 #1) |
| ? (soru) | 9 | evet | YORUM |
| BEŞ CEPHE: BANKACI · KEŞİŞ · KRAL · SULTAN · MİRAS (I–V) | 10 | evet (c0s10) | YORUM (anlatı çerçevesi; "tarihçilere göre" denmiyor) |
| İLK KANIT · taç | 11 | evet | YORUM |
| BÜYÜK ÖLÇÜDE · BORÇLA (damga) | 12 | evet (c0s11, 'büyük ölçüde borçla alındı') | NİTELİKLİ (A1 #12–#14; A4 #12–#13) — damga hedge'li cümleyle aynı anda |
| ŞARLKEN · ZAMAN KURYESİ · TESLİMAT · DÜNYAYI TESLİM EDEN İMPARATOR | 13 | evet (c0s12) | YORUM (başlık; metinler compose c1 kartıyla aynı) |

## 4. Montaj/ses için vurgu anları (global sn)
BRÜKSEL levhası 3.2 · "55 YAŞINDA" 7.8 · 40 sayacı 15.0 · V. KARL levhası 25.6 · beş cephe oturuşları 31.3 / 32.5 / 33.6 / 34.6 / 35.8 · sikke yağmuru 41.4 · BORÇLA damgası 42.4.

## 5. Ana ajana istekler / bulgular
1. **compose.py / shots.py — Türkçe büyük harf:** HUD başlığı (`compose.py:203`) ve bölüm kartı (`shots.py:264`) `title.upper()` kullanıyor; "i"→"I" olduğundan c9'da **"YENI DÜNYA: ALTIN, GÜMÜŞ VE VICDAN"** (doğrusu YENİ … VİCDAN) çıkıyor (ölçekli kırpıntıda doğrulandı). Öneri: `def tr_upper(s): return s.replace("i","İ").replace("ı","I").upper()`. c0 bu hatadan etkilenmiyor (başlıklar baştan büyük harf yazıldı).
2. **Başlık kartı sürekliliği:** compose'un c1 kartı kicker/alt başlığı `at=-4.0` ile baştan tam gösteriyor; c0 son çekimim bunu önceden hazırlıyor (§2.9). Kart metni veya düzeni değişirse haber verin ya da `c0_title` parametrelerini güncelleyin.
3. **Paylaşılan `medals/emblem/doc/quote/counter` (+ `bars/stacked/timeline/iconrow` varsayılanları) türleri** `at + 0.3` gibi işlem yaptığı için demet çapayla (`("c0s5","kırk",-0.1)`) TypeError verir; c0'da `emblem` yalnız yerel-sn `at` (0.0/0.3) ile kullanıldı, `medal` çapalı `plate_at` ile sorunsuz; çapalı sayaç/belge/madalya sürümleri `d_common.wd_*` içinde. Ortak türler `cx.at()/cx.amt()` kullanacak şekilde güncellenirse `wd_*` kopyalarına gerek kalmaz.
4. **`sk.text_width("")`** boş dizgede HarfBuzz'i çökertiyor (tek karakter koruması `d_common.tw()`'de).
5. **`theatre` sahne önbelleği** ~5 sahne tutuyor; hall→başka sahne→hall dönüşlerinde yeniden pişer (c0'da 3'lü seri bilerek ardışık).
6. **Bölüm kartı girişi sert kesme** (card'a `tr` verilmiyor): önceki bölümün son karesinden karta ani geçiş; kısa siyaha dalış önerilir.

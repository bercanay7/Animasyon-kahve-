# Bölüm 9 — Yeni Dünya: Altın, Gümüş ve Vicdan · yazar notları (BÖLÜM YAZARI D)

**Dosyalar:** `scenes_c9.py` (SHOTS) · `shots_c9.py` (c9_ önekli türler: `c9_durer`, `c9_fifth`, `c9_arma`; yardımcılar `circum_extra` (dünya turu, c13 ile ortak), `open_extra`, `cortes_extra`, `tenoch_overlay`, `ransom_overlay`, `debate_overlay`, `fleet_extra`, `sun_disc`) · `d_common.py` (D ortak: `A()`, `wd_counter`, `wd_vs`, `wd_medal_swap`, `wd_medals`, `wd_doc`, `tag`, `cameo`, `nplate` …).
**Süre** 109.1 sn · **20 çekim** (bölüm kartı hariç) · ort. 5.4 sn/çekim · `--check`: **uyarı yok** (bölüm ort. ≈ 110 ms/kare, en ağır çekim < 210 ms; 2× süper-örnekli stage.py ile ölçüldü).
**Ton:** tropik yeşil/altın/kan yerine sıcak kahve-altın; son kısım vicdan (sade). **Saygılı dil:** yerli halk karikatürü yok; ağır konularda (esaret, idam, fetih) madalya + harita + belge ağırlıklı; idam gösterilmez (madalya sessizce kararır). Damgalar: **TAHMİN** (s4), **RESMÎ KAZANAN YOK** (s11).

## 1. Çekim listesi
| # | tür | bölüm içi | süre | etiket | ne gösteriyor |
|---|---|---|---|---|---|
| 1 | map | 0:00.0 | 6.0 | atlantik_hic | Atlantik; kesikli rota yarı yolda söner ("hiç görmedi"), "HİÇ GÖRMEDİ" levhası, ŞARLKEN madalya + levha; "fethedildi" sözünde İspanya/Yeni İspanya/Peru bölgeleri yanar |
| 2 | map | 0:06.0 | 6.8 | cortes_rota | 1519: Küba → Veracruz → Tenochtitlan rotası; "KÜBA VALİSİNİN İZNİ OLMADAN" notu + Küba üstünde kırmızı yasak halkası; HERNÁN CORTÉS madalya + levha |
| 3 | theatre / siege | 0:12.8 | 4.8 | tenochtitlan | Sahne-lab `siege/tenochtitlan` (göl kenti, gün batımı, duman); altta "AZTEK BAŞKENTİ / TENOCHTİTLAN / 13 AĞUSTOS 1521" (koyu degrade üstünde) |
| 4 | wd_doc | 0:17.6 | 7.8 | cortes_mektup | "CORTÉS'İN MEKTUPLARI" parşömeni: önce karalama satırları, sonra "Fethi anlatır, / ama kendini savunur." (ikinci satır altın vurgu); "CARTAS DE RELACIÓN" |
| 5 | c9_durer | 0:25.4 | 4.4 | durer_sergi | Solda ALBRECHT DÜRER madalyası; sağda "BRÜKSEL" ve spot ışıklı tezgâhta altın güneş diski, tüy, sandık (Aztek eserleri) |
| 6 | wd_counter | 0:29.8 | 3.6 | yuz_bin_florin | "≈ 100.000 FLORİN" sayacı + **TAHMİN** damgası (arkada solgun güneş diski) |
| 7 | map | 0:33.4 | 3.0 | cajamarca_harita | 1532: İnka bölgesi, "İNKA İMPARATORLUĞU", CAJAMARCA |
| 8 | wd_medals | 0:36.4 | 4.6 | pizarro_atahualpa | FRANCISCO PIZARRO · ATAHUALPA (kesikli yuva önce görünür, söylenince dolar) |
| 9 | theatre / ransom_room | 0:41.0 | 7.5 | fidye_odasi | Oda-lab `ransom_room`: oda altınla dolar; altta "ALTIN 1.326.539 PESO" sayacı (koyu degrade üstünde) |
| 10 | wd_medal_swap | 0:48.5 | 2.8 | idam_sessiz | ATAHUALPA madalyası bronzdan oniks'e döner, sonra kararır (idam görüntüsü yok); "dip" geçişi |
| 11 | c9_fifth | 0:51.4 | 3.9 | beste_bir | Taç "Kraliyetin" sözünde ortada belirir; "ganimetin"de sola kayar, 5 külçe dizilir; "beşte"de ilk külçe yükselir, "1/5" |
| 12 | wd_doc | 0:55.2 | 5.8 | yeni_yasalar | "YENİ YASALAR · 1542": "Yerlileri köle yapmak yasaktır." ("köle yapmak yasaktır" vurgulanır) + mum mührü ("yasaktı" sonrası) |
| 13 | map | 1:01.0 | 6.2 | peru_valisi | Atlantik'ten Peru'ya kesikli rota + vali bayrağı; Peru'da meşaleler (öfke), "YERLEŞİMCİLER", "PERU VALİSİ", kafatası (öldürüldü) |
| 14 | map | 1:07.2 | 5.5 | valladolid_1550 | 1550: İspanya, VALLADOLID; "FETİHLER GEÇİCİ OLARAK DURDURULDU" notu; yakınlaşma |
| 15 | wd_vs | 1:12.7 | 5.1 | sepulveda_lascasas | SEPÚLVEDA (gümüş) ⟷ LAS CASAS (fildişi), ortada terazi |
| 16 | theatre / debate_hall | 1:17.8 | 8.3 | tartisma | Oda-lab `debate_hall`: iki kürsü; "SEPÚLVEDA · Savı: köleliğe layık", "LAS CASAS · Savı: fetih bir suç"; **RESMÎ KAZANAN YOK** damgası (arkasında yumuşak koyu bant) |
| 17 | map | 1:26.1 | 6.0 | dunya_turu | Dünya haritası 1519 – 1522: Sanlúcar → Güney Amerika → Pasifik → Moluk → Ümit Burnu → Sanlúcar; gemi + İspanya bayrağı; ATLANTİK / PASİFİK / HİNT OKYANUSU |
| 18 | wd_medal_swap | 1:32.1 | 1.9 | magellan_oldu | MAGELLAN madalyası ("öldü" sözünde bronzdan oniks'e, kararır) |
| 19 | wd_counter | 1:34.0 | 5.7 | elcano_on_sekiz | Beş gemiden dördü solar, biri ışır ("TEK GEMİ"); ELCANO madalyası; "18 AVRUPALI SAĞ KALDI" |
| 20 | c9_arma | 1:39.7 | 9.3 | arma_primus | ŞARLKEN → ELCANO ("ona … verdi", kesikli ok); mavi arma kalkanı + altın küre; "PRIMUS CIRCUMDEDISTI ME" kuşağı (kelime kelime); “Beni ilk dolaşan sensin.” |

Tür çeşitliliği: harita ×6, diorama ×3, belge ×2, madalya/karşılaştırma ×5, sayaç ×2, özel (Dürer, beşte bir, arma) ×3. En uzun aynı tür serisi 2 (hiçbir tür üst üste 3'ü geçmiyor).

## 2. Bilinen kusurlar / dürüst notlar
1. **Tenochtitlan** sahne-lab'ın `siege` sahnesi (figürler çok küçük; piramit tepesinde bayrak ve meşaleli figürler lab tasarımı). Yerli figürler küçük siluetler; alay/karikatür yok. Lab sahnesi değişirse yazı kaplaması (altta) yeniden gözden geçirilmeli.
2. **Fidye odası** (`ransom_room`) ve **Valladolid salonu** (`debate_hall`) oda-lab sahneleri aynen kullanıldı; `p` anahtarları (`fill_t`, `lecterns`, `city/time/fire`) lab API'sine bağlı.
3. **Dürer çekimindeki "Aztek eserleri" genel simgeler** (altın güneş diski, tüy, sandık): belirli bir eserin kopyası değil. Güneş diski ben çizdim (`sun_disc`, yüzsüz); hazır `sun_disc` simgesi gülen yüz gibi okunuyordu.
4. **Kafatası konumu genel:** Peru haritasında kafatası Lima enleminde duruyor; vali gerçekte Quito yakınında öldü (HAFIZA, etiket yok) — etiketsiz olduğu için yer iddiası taşımıyor.
5. **Dünya turu rotası şematik:** tek kopya Mercator; Pasifik geçişi antimeridyende ikiye bölünüyor (sol kenardan çıkıp sağ kenardan giriyor). Okyanus etiketleri rota ve karaya değmeyecek biçimde hesaplanmış konumlarda (ATLANTİK −51°/25°, PASİFİK −147°/−31°, HİNT OKYANUSU 71°/−3°).
6. **Arma kalkanı** sade (mavi alan + altın küre + altın çerçeve): gerçek Elcano armasının (baharat/kaşif unsurları) birebir kopyası değil. 'Primus' iddiası tartışmalı (kaynak notu A4 #19).
7. **Harita bölgeleri** (Aztek, İnka, Yeni İspanya, Peru) yaklaşık çokgenler; haritada "SINIRLAR YAKLAŞIKTIR" altyazısı var. İnka bölgesi turuncu-kehribar, İspanya kırmızı (ayrışır).
8. **wd_medals yuvaları:** ilk madalya söylenince diğer yuva kesikli halka olarak bekler; iki isim arası bekleme ≈ 1 sn.
9. **c9s1'deki ŞARLKEN madalya + levhası** yalnız hatırlatma amaçlı küçük bir kamera (cameo); "isim levhası s8'den önce yok" kuralı yalnız c0'ı bağlar.
10. **`theatre` 3 ayrı sahne** (siege, ransom_room, debate_hall) farklı anlarda; sahne önbelleği ~5 olduğundan bölüm içinde yeniden pişirme yok.

## 3. Ekrandaki olgular ve kaynak sınıfı (sınıf = `kaynaklar.md` cümle tablosu)
| Ekran metni / öğe | Çekim | Anlatıda | Sınıf / dayanak |
|---|---|---|---|
| HİÇ GÖRMEDİ · ŞARLKEN (İmparator) | 1 | evet (c9s1) | CONFIRMED +H31 (hiç gitmedi: çok yüksek güven, araştırmada yok) |
| 1519 · KÜBA · AZTEK · VERACRUZ · TENOCHTİTLAN · Küba→Tenochtitlan rotası | 2 | evet (c9s2) | CONFIRMED (A4 #1); rota şematik |
| KÜBA VALİSİNİN İZNİ OLMADAN | 2 | evet | CONFIRMED (A4 #1) |
| HERNÁN CORTÉS · Konkistador | 2 | evet | CONFIRMED (A4 #1) |
| AZTEK BAŞKENTİ · TENOCHTİTLAN · 13 AĞUSTOS 1521 | 3 | evet | CONFIRMED (A4 #1) |
| CORTÉS'İN MEKTUPLARI · "Fethi anlatır, ama kendini savunur." · CARTAS DE RELACIÓN | 4 | evet (c9s3) | CONFIRMED (A4 #2). Belge metni anlatının özeti, alıntı değil |
| ALBRECHT DÜRER · Ressam · BRÜKSEL · Aztek eserleri (genel simgeler) | 5 | evet (c9s4) | NİTELİKLİ (A4 #3 tek kaynak) |
| ≈ 100.000 FLORİN · TAHMİN | 6 | evet ('yaklaşık yüz bin florin tahmin etti') | NİTELİKLİ (A4 #3); damga cümledeki hedge'in aynısı |
| 1532 · CAJAMARCA · İNKA İMPARATORLUĞU | 7 | evet (c9s5) | CONFIRMED (A4 #6) |
| FRANCISCO PIZARRO · ATAHUALPA (İnka Hükümdarı) | 8 | evet | CONFIRMED (A4 #6) |
| ALTIN · 1.326.539 PESO | 9 | evet (c9s6) | CONFIRMED (A4 #7); gümüş kısmı anlatılmıyor/gösterilmiyor |
| ATAHUALPA madalyası kararır | 10 | evet (c9s7 'idam edildi') | CONFIRMED (A4 #9); tarih yok |
| GANİMET · KRALİYETİN PAYI · 1/5 | 11 | evet (c9s8) | NİTELİKLİ (A4 #8 tek kaynak) |
| YENİ YASALAR · 1542 · "Yerlileri köle yapmak yasaktır." | 12 | evet (c9s9) | CONFIRMED (A4 #20). Belge metni özet; encomienda kalktı iddiası YOK |
| YERLEŞİMCİLER · PERU VALİSİ · PERU · meşale/kafatası | 13 | evet | CONFIRMED (A4 #20); meşale = görsel metafor (YORUM) |
| 1550 · VALLADOLID · FETİHLER GEÇİCİ OLARAK DURDURULDU | 14 | evet (c9s10 'geçici olarak') | CONFIRMED (A4 #21; kaynak 'askıya aldı', metin 'geçici olarak durdurdu') |
| SEPÚLVEDA ⟷ LAS CASAS | 15, 16 | evet | CONFIRMED (A4 #21) |
| SEPÚLVEDA · Savı: köleliğe layık / LAS CASAS · Savı: fetih bir suç | 16 | evet (c9s11) | CONFIRMED +H32 (web doğruladı: Aristoteles 'doğal kölelik' / Las Casas) |
| RESMÎ KAZANAN YOK | 16 | evet | CONFIRMED (A4 #21) |
| 1519 – 1522 · dünya turu rotası · İspanya bayrağı | 17 | evet (c9s12) | CONFIRMED (A4 #17); rota şematik |
| MAGELLAN · Denizci | 18 | evet (c9s13) | NİTELİKLİ (A4 #18: ölüm Filipinler 1521; ekranda yer/tarih yok) |
| TEK GEMİ · ELCANO · Kaptan · 18 AVRUPALI SAĞ KALDI | 19 | evet | NİTELİKLİ (A4 #18–#19: 18/22 çelişkisi; 'Avrupalı' diyerek güvenli) |
| PRIMUS CIRCUMDEDISTI ME · “Beni ilk dolaşan sensin.” · ŞARLKEN → ELCANO | 20 | evet (c9s14) | CONFIRMED (A4 #19); 'Primus' iddiası tartışmalı (araştırma notu) |

## 4. Montaj/ses için vurgu anları (global sn)
13 AĞUSTOS 863.9 · TENOCHTİTLAN 866.4 · mektup karalamaları 870.2 · TAHMİN damgası 882.6 · 1.326.539 sayacı 894.7 · Atahualpa kararır 901.2 · 1/5 904.4 · Yeni Yasalar mührü 911.2 · RESMÎ KAZANAN YOK damgası 934.9 · dünya turu rotası 938.2 · "18" 948.1 · arma 952.0 · PRIMUS 955.0.

## 5. Ana ajana istekler / bulgular
1. **compose.py / shots.py — Türkçe büyük harf:** sol üst HUD başlığı ("IX · YENI DÜNYA: ALTIN, GÜMÜŞ VE VICDAN") ve bölüm kartı `title.upper()` ile üretildiği için **İ noktaları kayıp** (doğrusu YENİ … VİCDAN). Ölçekli kırpıntıda doğrulandı. Öneri: `tr_upper = lambda s: s.replace("i","İ").replace("ı","I").upper()` (compose.py:203, shots.py:264–265; `counter` türünde `unit.upper()` aynı hata, shots.py:541).
2. **Paylaşılan `medals/emblem/doc/quote/counter` (+ `bars/stacked/timeline/iconrow`) türleri** `at + 0.3` işlemi yapıyor → demet çapa TypeError verir; bu bölümde çapalı kopyalar `d_common.wd_*` olarak yazıldı (`wd_counter`, `wd_vs`, `wd_medal_swap`, `wd_medals`, `wd_doc`). Ortak türlerde `cx.at()/cx.amt()` kullanımı bu kopyaları gereksiz kılar.
3. **`sk.text_width("")`** boş dizgede HarfBuzz'i çökertiyor (doc vurgusunda boş `start`); `d_common.tw()` korumalı.
4. **`shot(label=…)` ile tür parametresi `label` çakışıyor** (paylaşılan `counter`'ın `label` parametresi): `wd_counter`'da `lab`/`lab_at` adını kullandım. Ortak türde yeniden adlandırma önerilir.
5. **`theatre` sahne önbelleği** yalnız ~5 sahne tutuyor (`stage._SCENES`); aynı sahneye farklı `p` ile dönüşte 3–8 sn yeniden pişirme.
6. **`check()` yanlış pozitifi:** ölçülen kare bir `dip`/`fade` geçiş penceresine düşerse sonraki çekimin ilk pişirmesi öncekine yazılıyor (c12'de 2 sn görünmüştü); bu bölümde `dip` süreleri 0.8–0.9 ile çözüldü, gerçek render'ı etkilemez.
7. **Bölüm kartı girişi sert kesme:** `chapter_card`a `tr` verilmiyor; önceki bölümün son karesinden karta ani geçiş (siyaha dalış önerilir).
8. **Lab bağımlılıkları:** `tower/cloister/chapel/bedroom/ransom_room/debate_hall` ve `siege/tenochtitlan` parametre adları değişirse (`fill_t`, `lecterns`, `city/time/fire`) c9/c12 etkilenir; son `--check` temiz.

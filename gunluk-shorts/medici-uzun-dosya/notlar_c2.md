# notlar_c2 — Defterin Sihri (1397–1429 · 244 sn · gerçek ses · PARÇA 1 KAPANIŞI)

Dosyalar: `scenes_c2.py` (37 çekim; 5 longtake), `c2_kinds.py` (özel türler), `p1_ortak.py`, `yonetmen_c2.md`.
Özel türler: `c2_nolist` (BORÇ ✗ FAİZ ✗ KUR FARKI ✓), `c2_hediye`, `c2_kasa`, `c2_borc` (Giovanni–Cossa–taç–Konstanz), `c2_ayrim` (kefalet/fidye yol ayrımı), `c2_mezar` (ESKİ PAPA yazıtı), `c2_rivayet` (mitra/aforoz — ANEKDOT), `c2_katasto` (hane kutuları), `c2_yil` (20 Şubat 1429, mum + yıl ruloyu), `c2_kalemler` (Machiavelli/Cavalcanti panelleri), `c2_sadaka`. `c1_machiavelli` c2'de yeniden kullanıldı (`stamp_text`, `rebel_who="old"`, `order_big`). Özel simgeler: `c2_mitra`, `c2_bulla`.

## Kısıtlar (uygulananlar)
- **Kapı:** "Birkaç yıl sonra aynı Cosimo, şehrin en yüksek kulesinde bir hücreye kapatılacaktı." → Palazzo Vecchio kulesinde yavaş crane up (4160 px yüksekliğe), doygunluk + vinyet ile söner; hücre GÖSTERİLMEZ (yalnız kule ucunda soluk bir parıltı); çan/saat/ses olayı yok; bölüm sessiz ve ağır biter. Bitiş ekranı Program'dan.
- **KAPALI (mizah/ayrıntı yok):** Giovanni'nin ölümü (yalnız sönen mum + yıl ruloyu; ölüm yeri/saati/tanık/yatak YOK) ve Cossa'nın esareti (yalnız yol ayrımı: kefalet/fidye; kimse "yakalanmıyor", hücre/kafes yok).
- **Mum (c2_yil):** yalnız sembol; "gece" iddiası, oda/yatak yok. Arka plan `mode="night"` yalnız koyu renk derecelendirmesi; Cosimo madalyası çekimi de aynı koyu paletle (kapıya geçiş için).
- **Kaynak sınıfı damgaları:** ANEKDOT ×4 (rivayet, Machiavelli, Cavalcanti, sadaka), MİT (çifte kayıt), "KLASİK BİR ÖRNEK" (kambiyo modeli; Medici'ye özgü belge yok, tutar yok), "BİR HESABA GÖRE" (%29,8), AKTARDIĞINA GÖRE (Parks), DE ROOVER'A GÖRE, LORENZO'NUN KAYDINA GÖRE, DEFTERLER GÖSTERİR.
- **Mizah (rehber §5-B):** faiz ↔ kambiyo ↔ vicdan komitesi; "faiz değil, hediye"; ESKİ PAPA yazıtı + itiraz; çifte kayıt miti. Mizah yalnız kurum/kibir/mit üzerinden; kişiye (Giovanni, Cossa, Cosimo) şaka yok.
- Kitap/kişi yüzleri: madalya (Giovanni, Lorenzo, Cosimo — bronz profil, uydurma yüz değil) + silüet (Cossa, Martinus, bankacılar); Rubens/Botticelli vb. kopyası yok.
- Sayılar: son değerler çıkış geçişinden ≥0,6 sn önce oturur (Strozzi 0,96 · 152.820: 0,79 · 180.000: 0,66 · 39: 0,81).
- Mutlak saniye yok: çapa ≥%90 (tüm P1 mutlak %3).
- Dokunulmayanlar: motor/dünya/cilt dosyaları, `sfx_cues_p1.json`, `out_p1/*`.

## Ekrandaki olgular ve kaynak sınıfı
| ekran | cümle | sınıf |
|---|---|---|
| KAMBİYO; KİLİSE: FAİZ = TEFECİLİK; YASAK | c2s1–2 | YORUM / ◐ M1:§5B,D35 |
| BİR YOL; PARAYI PEŞİN VERİRSİN; BRUGGE → BARSELONA; POLİÇE; KLASİK BİR ÖRNEK | c2s3 | ◐ model M1:§5A (tutar yok) |
| VADESİ GELİNCE TAHSİL; 2. POLİÇE; KUR FARKI | c2s4 | ◐ model M1:§5A |
| BORÇ ✗ · FAİZ ✗ · KUR FARKI ✓ | c2s5 | ◐ gerekçe M1:§5B |
| VİCDAN KOMİTESİ; EN YARATICI DEPARTMAN (terazi) | c2s6 | YORUM (mizah a) |
| MEVDUAT SÖZLEŞMESİ; Faiz: —; TRACY PARKS · AKTARDIĞINA GÖRE | c2s7 | ○ M1:§5B |
| hediye kutusu; FAİZ çizilir; HEDİYE | c2s8 | ○ M1:§5B (mizah a) |
| MÜŞTERİ: KİLİSE (kardinal siluet) | c2s9 | ○ M1:D19 |
| ROMA ŞUBESİ; AYRI SERMAYE ✗; KİLİSE → kasa; DE ROOVER'A GÖRE | c2s10 | ○ M1:#27,D19 |
| 25 MART 1402; FLORANSA → VENEDİK; YILBAŞI | c2s11 | ◐ M1:#28,D18 |
| DEBITORI/CREDITORI defteri; Medici arması; MİT | c2s12 | MİT M1:mit1 |
| ÇİFTE KAYDIN İZİ: CENOVA 1340 · VENEDİK 1407 · PACIOLI 1494; Medici arması ✗; ETMEDİLER | c2s13 | ◐ M1:#71,#76 (1407 ve 1494 brif zaman çizelgesi kalemleri; anlatıda "Cenova 1340" geçer) |
| MEDİCİ'NİN FARKI: YAPI; FLORANSA/ROMA/VENEDİK; KENDİ ORTAKLIĞI · KENDİ DEFTERİ | c2s14 | ◐ M1:§5C |
| GIOVANNI · BORÇ VEREN; BALDASSARRE COSSA · KİLİSE ADAMI; XXIII. JOHANNES · PAPA; KONSTANZ KONSİLİ · 1415 | c2s15–16 | ◐ M1b:b28,bD13,U4,b29 (yalnız "borç") |
| KEFALET / FİDYE; KAYNAKLAR AYRIŞIYOR | c2s17 | ○ M1:D16,M1b:b30 (tutar yok) |
| VAFTİZHANE · COSSA'NIN MEZARI; ESKİ PAPA; V. MARTINUS · İTİRAZ | c2s18–19 | ◐ M1:#33,#36,D15 |
| TRECCANI · GIOVANNI MADDESİNDE; ANEKDOT; mitra · BORÇ; AFOROZ TEHDİDİ | c2s20 | ANEKDOT ○ M1b:b34,bD1 |
| PAPALIĞIN RESMÎ KASA MEMURLUĞU · 1420'LERİN BAŞINDAN İTİBAREN; 22 YIL; KESİNTİLERLE | c2s21 | ◐ M1b:b32,U2 |
| KATASTO · 1427; 9.780 HANE (sayaç, ekran kartı) | c2s22 | ◐ M1:#39 (brif ekran kartı; sözle yok) |
| KAYITLI SERVET: 137 HANE %29,8; BİR HESABA GÖRE | c2s23 | ○ %29,8 M1:#39,§4B |
| PALLA STROZZI · EN ZENGİNİ; 162.925 FLORİN · BRÜT | c2s23 | ◐ Strozzi M1:#39 |
| GIOVANNI · CATASTO'YU DESTEKLEDİ; DESTEKLEDİ | c2s24 | ◐ M1:#38 (yıl 1426/27 çelişkili: yıl yazılmaz) |
| 1420 · BANKANIN YÖNETİMİ (Giovanni → oğulları) | c2s25 | ◐ M1b:U5,b33 |
| 1397–1420 · 152.820 FLORİN KÂR; DEFTERLER GÖSTERİR | c2s25 | ◐ toplam M1:#35 ("gösterir") |
| 20 ŞUBAT 1429 (mum söner); yıl 1429 → 1428; FLORANSA TAKVİMİ · YILBAŞI 25 MART | c2s26 | ◐ M1:#40; M5:P1 |
| LORENZO · İLERİDE MUHTEŞEM DİYE ANILACAK; 180.000 FLORİN; LORENZO'NUN KAYDINA GÖRE | c2s27 | ○ DBI/M5:D32 |
| MACHIAVELLİ · BİR ASIR SONRA; CAVALCANTI · 1440'LARDA; ANEKDOT ×2; soru işareti | c2s28–31 | ANEKDOT ◐/○ M1:D11–D14 (birebir söz yok) |
| MACHIAVELLİ'NİN ÇİZDİĞİ · KİMSE İSTEMEDEN DE; ANEKDOT | c2s32 | ANEKDOT ◐ M1:D14 |
| MEDİCİ SİPARİŞİ (mühür) | c2s33 | ◐ M1:D07,D11 |
| COSIMO · GIOVANNI'NİN OĞLU; 39 YAŞINDAYDI; 1389 DOĞUMLU · HESAPLA | c2s34 | ◐ M5:P2 (39 = hesap; ekranda "HESAPLA" ile işaretli; anlatı "kırk yaşına yaklaşıyordu") |
| kule (kapı) | c2s35 | ◐ M2:K06 (Eylül 1433 söylenmez) |

## Bilinen kusurlar
1. **Poliçe/harita çizgisi** (Brugge → Barselona) düz rota; kaynakta Medici'ye özgü belge/rota yok, "klasik örnek" damgası bunu söylüyor. Harita dünyası Brugge'den Barselona'ya "yaklaşık" bir kuş uçuşu çizgisi çiziyor.
2. **Poliçe belgesi** (`p1_doc`): geniş parşömen boşluğu, belgenin içeriği üç kısa satır; çekim 3,6 sn olduğu için kabul edildi.
3. **c1_machiavelli** türü c2'de iki kez yeniden kullanıldı (aynı sahne dili; plaket/damga/konuşma ruloşu farklı).
4. **Strozzi sayacı:** çekim 3,0 sn; son 0,9 sn geçiş (iris) penceresi olduğundan sayaç erken başlatıldı (“en zengini” sözcüğü); Strozzi levhası adı söylenmeden ≈0,3 sn önce çıkıyor (spoiler değil, sayaç ismin öncülü).
5. **Cosimo kartı:** 39 sayısı doğrudan kaynak değil, hesap; levha "1389 DOĞUMLU · HESAPLA" ile işaretli. Anlatıdaki "kırk yaşına yaklaşıyordu" ile uyumlu.
6. Kapı çekimi (`skyline_dikey`, `tod="day"`) gündüz gökyüzü; doygunluk/vinyet ile ağır, "alacakaranlık/gece" iddiası yok. Kule tepesindeki çan odası açıklıkları çansız (çan çizilmedi).

## Ana ajandan istekler
- `cilt_cam.OWN_CAMERA`'ya `oda`/`sehir` (ve `p1_*` sarmalayıcıları) resmî eklensin; şimdi `p1_ortak.py` çalışma anında ekliyor.
- `counter` türü çapa tuple'ı kabul etmiyor (c2'de `at=0.3` float ile kullandım); anchor desteği istenir.
- `qa_flow --chapters c2` tek bölüm koşusunda olay yoğunluğu yapay sapar; gerçek kapı `--part 1`.
- `preview_chapter.py --check` ms/kare: kısa (≤3 sn) çekimlerin örnek noktaları geçiş pencerelerine düşüyor (iki sahne render); eşik uyarısı çekimin tek başına maliyetini yansıtmıyor.

## Kapı sonuçları (qa_flow --part 1 = 92 çekim)
Durgunluk GEÇTİ (en uzun durgun koşu 0,5 sn) · kamera %100 (92/92) · hareket yeterliliği 0 zayıf · gerekçeli geçiş %100 (89/89), çıplak fade %0, çıplak kesme 0 · çekim uzunluğu GEÇTİ (c2: 37 çekim; medyan 5,93 sn; longtake hariç 5,69; max 13,3 sn longtake) · tür tekrarı 0 ihlal · çapa GEÇTİ (sözcük 239 · cümle 107 · mutlak %3) · yön 0 uyarı (c2: `slide l` sadaka, önceki cam yönüne uyduğu için bilinçli kırılma sayılmaz) · altyazı bölgesi boş · yönetmen kartı 37 satır = 37 çekim, tür sırası aynı · olay yoğunluğu %96 (82/85, tüm Parça 1). `preview_chapter.py c2 --check`: uyarı yok; ort. ≈102–112 ms/kare (≈10–11 dk tek çekirdek); hiçbir çekim >250 ms.

Görsel denetim: tüm çekimlerin kontak sayfaları görüldü (bölünen çekimler: banka 1a/1b, poliçe, anahtarlar, 22 yıl, stacked/Strozzi dahil); `--clip` ile harita → poliçe sayfa geçişi (359,9–361,7 sn), ledger → mum (c2_yil, 518,9–520,7 sn), Cosimo madalyası → kule (iris + light, 585,1–586,7 sn) kare kare akıyor.

# notlar_c8 — Bölüm VIII · Akdeniz'de Barbaros (c8)  ·  yazar: bölüm yazarı C

Dosyalar: `scenes_c8.py`, `stage_c8.py` (c8_konsey, c8_zafer [yedek kutlama kartı]), `stage_c678.py` (ortak).
Yeni (yamalı) anlatıya göre: c8s5 "Habsburg çevresinde kutlandı", c8s8 "Sonraki yıllarda" ('30 YIL' sayacı YOK), c8s9 "beş yüz kadar" (≈500), c8s11 "çağrılmadığı anlatılır" (damga ANLATILIR).

## (a) Çekim listesi özeti (15 çekim + bölüm kartı, ≈ 72 sn)
| # | tür | etiket | ne gösteriyor |
|---|---|---|---|
| 1 | c678_sahne (sea) | akdeniz_kadirgalar | şafakta 8 yeşil bayraklı Osmanlı kadırgası; AKDENİZ |
| 2 | medal | barbaros | BARBAROS HAYREDDİN PAŞA (forest madalya); "1534" |
| 3 | map | istanbul_tunus | İstanbul → Tunus rotası (gemi simgesi ilerler), KAPTAN-I DERYA, 1534 |
| 4 | c678_medals | karl_doria | V. Karl + Andrea Doria; BİZZAT; TUNUS SEFERİ · 1535 |
| 5 | c678_sahne (siege) | halkulvadi | Halkulvadi kuşatması; TEMMUZ 1535; TUNUS ALINDI |
| 6 | c678_cift | 20bin_esir | 20.000 ESİR · SERBEST KALDI (zincir simgesi) + YAKLAŞIK damgası |
| 7 | c678_sahne (sea harbor) | zafer_kutlama | liman alacakaranlığı: sallanan çanlar, Habsburg sancakları, defne, ZAFER; HABSBURG ÇEVRESİNDE |
| 8 | c678_sahne (sea night) | gece_deniz_filo | gece denizi, ufukta Osmanlı filosu; Barbaros madalyası |
| 9 | map | preveze_harita | Preveze, "28 EYLÜL 1538" |
| 10 | c678_sahne (sea) | preveze_savas | Preveze deniz savaşı; PAPALIK/VENEDİK/İMPARATOR (birleşik filo) vs BARBAROS; GERİ ÇEKİLDİ |
| 11 | map | dogu_akdeniz_ustunluk | doğu Akdeniz'de yeşil dalga, Osmanlı donanması; AKDENİZ'İN DOĞUSU (30 YIL YOK) |
| 12 | map | cezayir_harita | Cezayir, 1541, kuzeyden kıyıya okla çıkış |
| 13 | c678_cift | 500_24bin | ≈ 500 YELKENLİ · ≈ 24.000 ASKER |
| 14 | c678_sahne (sea storm) | cezayir_firtina | fırtına, şimşek (flashes anlatıya bağlı), gemiler batar; BARUT ISLANDI; ≈ 150 GEMİ BATTI (YAKLAŞIK) |
| 15 | c8_konsey | cortes_konsey | savaş konseyi masası, BOŞ sandalye, kapıda Cortés madalyası; KONSEYE ÇAĞRILMADI + ANLATILIR damgası |

## (b) Bilinen kusurlar
- Halkulvadi çekimi (#5) `siege` (sahne-lab) teslimine bağlı; o zamana dek yer tutucu.
- #13 etiketleri: "≈" Cinzel'de var (denetlendi); oklar (→) Cinzel'de yok (kullanılmadı).
- c8_zafer (alternatif kutlama kartı) kullanılmıyor; yedek olarak kodda duruyor.
- Preveze çekiminde tarafların renkleri/yarım ay–haç otomatik (sea sahnesi): Venedik bayrağı turkuaz, Papalık altın.

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
- Barbaros Hayreddin Paşa, sultanın amirali; 1534 kaptan-ı derya, Tunus — CONFIRMED (A3 #12; gün tutarsız, yalnız yıl).
- 1535: Şarlken Doria'nın filosuyla bizzat Tunus'ta — CONFIRMED (A3 #13; H28 DOĞRULANDI). Temmuz 1535 Halkulvadi düştü; ≈20 bin esir — CONFIRMED (A3 #13) → YAKLAŞIK damgası.
- Kutlama: Habsburg çevresinde — NİTELİKLİ/HAFIZA H29 (KISMEN: Sicilya girişleri, Vermeyen halıları): ekranda "HABSBURG ÇEVRESİNDE".
- Preveze 28 Eylül 1538; Papalık+Venedik+İmparator birleşik filosu geri çekildi — CONFIRMED (A3 #14; sonuç yorumları ayrışır, "geri çekildi" nötr).
- Sonraki yıllarda doğu Akdeniz'de Osmanlı üstünlüğü — H30 (sayı kaldırıldı): ekranda sayı yok.
- Cezayir 1541; ≈500 yelkenli; ≈24.000 asker — NİTELİKLİ (A3 #15) → ≈ işaretiyle. Fırtına, barut ıslandı, ≈150 gemi battı — NİTELİKLİ (A3 #15) → YAKLAŞIK damgası.
- Cortés orada, savaş konseyine çağrılmadığı anlatılır — CONFIRMED/NİTELİKLİ (A3 #16, Gómara hattı): damga ANLATILIR. (A3 #17 zümrüt anekdotu KONMADI.)

## (d) Ana ajandan istekler / uyarılar
1. Sea sahnesi harika çalışıyor; `flashes=[...]` ve `sink_t=(...)` yerel saniyelerle yazıldı (anlatı değişirse yeniden hesap gerekir: c8s10 çekimi c8s10−0.2 sn'de başlar).
2. `siege` (halkulvadi) geldiğinde #5'in kamera/p ayarı yapılacak.

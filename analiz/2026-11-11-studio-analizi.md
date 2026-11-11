# YouTube Studio analizi — 11 Kasım 2026

Kaynak: Studio "İçerik" dışa aktarımı, 13 Ekim – 10 Kasım 2026 (Table/Chart/Totals CSV). İlk üç gün (10–12 Ekim) ve 10 Kasım dışarıda; günlük tablo yalnız en çok izlenen videoları içerir (toplamla küçük farklar olabilir). Trafik kaynağı, tutma eğrisi, yaş/ülke bu dışa aktarımda yok. Ayrıca Supermetrics "YouTube Public Data" (herkese açık görüntüleme/beğeni/yorum). Bu dosya `CLAUDE.md`'deki "Ölçütler"e **dokunmaz**; onların güncel devamıdır. Kanıt düzeyi: B (kanalın kendi verisi).

## Genel
38.990 görüntüleme · 905,7 saat · 442 abone · 318.138 gösterim · TO %2,35 · ort. izleme 3:01.

## Shorts ve uzun video
| | Video | Görüntüleme | Abone | 1000 görüntülemede abone | Görüntüleme başına izlenme (dk) |
|---|---|---|---|---|---|
| Shorts (≤60 sn) | 13 | 7.700 | 10 | 1,3 | 0,23 |
| Uzun | 11 | 31.277 | 276 | 8,8 | 1,68 |

Aboneler uzun videolardan geliyor. Shorts'un görevi uzun videoya yönlendirmek ("İlgili video").

## Uzun videolar
| Video | Süre | Gör. | Ort. izleme | Abone/1000 | Gösterim (pay) | TO | Gösterim başına izlenme (dk) |
|---|---|---|---|---|---|---|---|
| Sisifos | 7:05 | 21.890 | %38,8 | 9,1 | 199.463 (%62,7) | %2,61 | 0,125 |
| Prometheus | 23:56 | 3.867 | %39,9 | 10,3 | 51.429 (%16,2) | %2,00 | **0,379** |
| Abdülhamid / Cumhuriyet | 6:20 | 1.416 | %40,8 | 6,4 | 26.432 (%8,3) | %1,56 | 0,056 |
| Orfeus | 4:48 | 689 | %45,8 | **24,7** | 22.891 (%7,2) | %1,45 | 0,047 |
| Şarlken | 21:27 | 535 | %43,7 | 3,7 | 1.865 (%0,6) | %8,36 | 2,207 |
| Medici (1/7) | 10:02 | 246 | **%29,1** | 0 | 5.449 (%1,7) | %1,52 | 0,076 |

## Bulgular ve öneriler
1. **Prometheus gösterim başına Sisifos'un ~3 katı izlenme süresi getiriyor** ama gösterimi dörtte biri. İçerik güçlü, gösterim eksik → `CLAUDE.md` kuralı: 2–3 gün yeni dalga yoksa kapak ve başlığı kurulla yenile; yeni kapakla "Test ve karşılaştır".
2. **Orfeus abone dönüşümünde birinci** (1000 görüntülemede 24,7; Sisifos 9,1) ve tutma %45,8, ama gösterilmiyor. Sisifos'un sabit yorumu ve bitiş ekranı Orfeus'a bağlanabilir.
3. **Şarlken:** TO %8,36 ama yalnız 1.865 gösterim; YouTube geniş kitleye açmamış. Başlık hâlâ kapak yazısı ("KANUNİ'NİN RAKİBİ / TAHTI BIRAKTI"); planlanan başlık uygulanmadıysa Studio'da kontrol et.
4. **Sisifos taşıyıcı:** gösterimin %62,7'si, son haftalarda günlük izlenmenin ~%85–90'ı. 4 Kasım'da yeni dalga (3.776). 6–9 Kasım'da günlük 1.400–1.700, 9 Kasım 692 (son gün eksik olabilir). Sıradaki videoyu Sisifos hâlâ trafik çekerken çıkar.
5. **Sisifos ort. izleme %44,8 (5. gün) → %38,8:** geniş kitleye açılırken beklenen düşüş.
6. **Medici (1/7) zayıf:** %29 izleme (uzun videoların en düşüğü), 0 abone, 6 günde 246. 7 bölümlük seri; yeni bölümler üretmeden önce 7. günde kurulla paketleme ve ilk dakika incelemesi. 6 günlük veriyle kesin hüküm değil.
7. **Shorts izleme %52–62:** iyi. Shorts TO'su ana akış gösterimidir, uzun videolarla kıyaslanmaz.
8. **Başlık:** "14 Ekim 2026", "18 Ekim 2026" konuyu söylemiyor (~100 gör.). Orfeus listede iki kez (ikincisi yayın tarihsiz, 2 gör.; muhtemelen İngilizce ya da liste dışı yükleme).

## Eksik veri (sonraki dışa aktarım)
Kitle (yaş/ülke/yeni-geri dönen), trafik kaynakları, izleyici tutma (Prometheus ve Medici'nin hangi saniyede düştüğü).

## Yöntem
`python3 -I` ile CSV'ler salt veri olarak okundu; hesaplar yukarıdaki tablolardan yeniden üretilebilir (izlenme dk = saat×60 ÷ gösterim; ort. izleme % = ort. süre ÷ video süresi).

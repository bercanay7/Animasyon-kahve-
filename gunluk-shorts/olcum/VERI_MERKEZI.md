# YouTube Veri Merkezi (Google Sheets)

**Dosya:** Google Drive → *Zaman Kuryesi — Veri Merkezi* (yalnızca sahibi görür; paylaşım kapalı).
Bağlantı: https://docs.google.com/spreadsheets/d/1grLYcliMUoFMnSLFVUAJDrLAMUS_Vm1PYsr1WsqAtxs/edit

| Sekme | İçerik |
|---|---|
| BAŞLA | kullanım, kurulum adımları, okuma kuralları |
| Videolar | video kimlik kartları (kulvar, süre, cilt, kanca, durum, ses) — 11 satır (Şarlken dahil) |
| Okumalar | `olcum/olcum.csv` ile aynı şema + hesaplı sütunlar (izleme süresi/görüntülenme, tekrar oranı, n<300 uyarısı) |
| Takvim | 13 haftalık yayın kuyruğu (`konsey/YOL_HARITASI.md` §5) + Uzun Dosya #1 |
| Kanal_28gun | haftalık kanal fotoğrafı (Pazartesi) |
| Windsor_YouTube | Windsor.ai YouTube bağlayıcısından ham veri iniş sayfası |

## Otomatik veri (tek seferlik kurulum)

1. Windsor.ai hesabında (deneme planı) **Connectors → YouTube → yetkilendir**; Windsor ekranında kişisel Google hesabını değil **kanalın marka hesabını** seç.
2. Claude'a "YouTube bağlandı" yaz → Claude Windsor `get_data` ile video/kanal metriklerini çeker, `Okumalar` ve `Kanal_28gun` sekmelerini doldurur ve Windsor→Google Sheets zamanlı aktarımını (`Windsor_YouTube`) kurar.

Giriş/yetkilendirme bağlantıları sohbetle iletilir; **depoya yazılmaz** (Anayasa: kimlik bilgisi/oturum bağlantısı depoya girmez).
Durum (18 Ekim 2026): YouTube Windsor'a bağlandı (kanal hesabı, yalnız okuma; deneme planı: saatlik yenileme yok, önbellek eski kalabilir). `Okumalar` ve `Kanal_28gun` doldurma ile `Windsor_YouTube` aktarımı henüz yapılmadı.
Yeni veriler artık Windsor'dan okunur; Studio ekran görüntüsü yalnız Windsor'un vermediği alanlar için (yayın saati, "değiştirilmiş içerik", oynatma listesi, tutma eğrisi) gerekir.

# Hatırlatıcı görevleri

Her dosya bir ölçüm görevidir. Zamanlanmış görev (hatırlatıcı) ana Zaman Kuryesi oturumuna gelir; o oturum dosyayı okur ve görevi **depoya bağlı yeni bir oturumda** başlatır:
`create_session(source_url="https://github.com/bercanay7/Animasyon-kahve-", title=<dosyanın başlığı>, prompt=<dosyanın içeriği>)`, ardından kullanıcıya telefon bildirimi.

Neden böyle (27 Kasım 2026): hatırlatıcının kendi açtığı oturuma (create_new_session_on_fire) depo bağlanmıyor; okuyabiliyor ama main'e gönderemiyor (git proxy 403; Mary Stuart 7. gün yaması elle taşındı). create_session ile açılan ve depo kaynağı verilen oturum okuyup yazabiliyor (27 Kasım sınaması). Depo büyük: yeni oturumun açılması ~4 dk.

Yeni video için: buraya `NN-video-48.md` ve `NN-video-7.md` ekle, ana oturumdan aynı düzende hatırlatıcı kur.

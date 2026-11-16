# Kafka, Dönüşüm: kurul kaydı

## Kurulsuz geçen kapılar (açık kayıt)
Kullanıcının haftalık kullanımı %89'daydı. Kullanıcı "İkaros'taki gibi yapıp bitirelim, kurulu beklemeyelim" dedi (15 Kasım 2026). Bu yüzden **hiçbir kapıda bağımsız kurul (alt ajan) toplanmadı.** Bütün kapılar yalnız başkanın (ana oturum) doğrulamasıyla geçti. ≥9 eşiği hiçbir kapıda bağımsız olarak ölçülmedi.

| Kapı | Durum | Başkanın yaptığı denetim |
|---|---|---|
| Senaryo + paketleme taslağı | **Kurulsuz** | Talep kontrolü (otomatik tamamlama, Türkçe videolar); iskelet önceden seçildi (Kişōtenketsu); her kaynak cümlesi Almanca metinde satır numarasıyla doğrulandı; üç dış atıf ayrıca doğrulandı (Wolff mektubu 25.10.1915, Babaya Mektup'taki cümle, Camus eki); bir zaman hatası yakalandı (Grete'nin ihmali III. bölüme taşındı); zayıf bir yorum cümlesi çıkarıldı |
| Seslendirme | **Kurulsuz** | Whisper yok: sessizliğe dayalı hizalama (`tools/hizala.py`); iki sınır sessizlik ölçümüyle elle düzeltildi (`tools/sinir_duzelt.py`: D07, E04). Telaffuz denetlenmedi: **kulakla onay kullanıcıda** |
| Üslup kapısı | **Kurulsuz** | Açılış karesi + figür sayfası + bütün filmin kurgu özeti; figürler iki turda düzeltildi (kutu gövde → bel ve omuz; kollar ayrı konturla) |
| Hassasiyet (üslup aşamasında) | **Kurulsuz; başkan bakışı** | Böcek hiç çizilmedi (ne gölgesi ne bacağı). Kilise kulesinde haç yok. Kafka ve babası gerçekçi portre değil, dönem silueti. Yahudi kimliği ve 1940'lar videoya girmedi. Hastalık/engellilik böcekle eşleştirilmedi. Kapak B'de elma ilk denemede babanın bacakları arasına düşüyordu (yanlış okuma riski): taşındı. **Açık nokta:** üç kiracı metne uygun olarak gür sakallı; bir hassasiyet okurunun "dinî ya da etnik çağrışım var mı?" diye bakması iyi olurdu |
| İlk tam kurgu | **Kurulsuz** | `tools/kurgu_ozet.py` ile 56 planın her birinden kare; beş zayıf plan yeniden çizildi (P13, P21 dev yakın planlar; P22 kol; P48 kollar; P49 yazı taşması); P55'teki soru anlatımla eşlendi (numara kayması hatası) |
| Ses ve miks | **Kurulsuz** | −14,1 LUFS, −1,4 dBFS tepe (ölçüm). Kulakla onay kullanıcıda |
| Son render + yayın paketi | **Kurulsuz** | Bitiş ekranı anlatımla eşlendi (kuyruk 20 → 12,7 sn) |
| Kapak | **Kurulsuz** | Test seti: 246/168/120 küçültme, gri, rozet, koyu/açık akış, TV (`tools/kapak_seti.py`) |
| Shorts | **Kurulsuz** | 32,6 sn; en güçlü kare (elma) ve kişisel soru ilk saniyede |

## Sonraki oturum için öneri
Yayından önce kullanım payı açılırsa en değerli tek kurul turu: **hassasiyet + kaynak** (tek birleşik üye; kapak ve kurgu özeti sayfalarıyla). İkincisi: **kanca ve tutma** (ilk 30 sn'yi ilk kez gören izleyici gözüyle).

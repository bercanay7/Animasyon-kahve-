# Lale Çılgınlığı: geriye bakış (22 Kasım 2026; kurulsuz üretim, başkan)

Çalışma düzeni kullanıcının kararıydı: kurul, puanlama ve çok ajanlı akış yok; Fable yalnız emin olunmayan yerde. Web sayfalarını okumak için okuma ajanları kullanıldı (TDV, Goldgar söyleşileri, Osmanlı narh belgeleri); bunlar kurul değil, sayfa okumaydı. Fable iki kez danışıldı: seslendirmeden önce senaryo (aşağıda ve `uretim_plani.md`), yayından önce bütün iş (aşağıda "Fable son yorumu").

## Ne işe yaradı
- **Türkçe boşluk ölçütü:** konu kullanıcının yeni ölçütüyle seçildi (dünyada yankı, Türkçede boşluk, Türkiye bağı). Talep kontrolüyle çelişmedi: konu adı aranmıyor ama tanıdık kapı ("lale", okuldan "Lale Devri") başlıkta öne alındı.
- **İki efsane, iki kanıt:** omurga (kullanıcının önerisi) kaynakla tuttu ve güçlendi. Hollanda'da Mackay'in denizcisi ↔ Goldgar'ın arşivi; İstanbul'da Ahmed Refik'in "500–1000 altın"ı ↔ Aktepe'nin narh defteri (en pahalısı 50 kuruş). İki somut "belge karşı belge" anı, soyut bir "tarih yazımı" yorumunun yerini aldı (somut olay kuralı).
- **Kaynak taraması seslendirmeden önce:** TDV'deki "Ekim 1722 fermanı" sicilde bulunamadı; Aktepe'nin dergipark'taki makaleleri 28 Haziran 1726 ve Ağustos 1727 belgelerini verdi. Patrona tarihi iki kaynakta farklıydı (25/28 Eylül), iki bağımsız kaynakla 28 Eylül seçildi.
- **Fable'ın senaryo okuması** (puansız, tek tur) dört engelleyici bulgu getirdi (Ahmed Refik'in rolü, "Lale Devri hiç yaşanmamıştır" bağlamı, Goldgar'ın tam bulgusu, kapak A'nın vaadi) ve okunuş hatalarını yakaladı. 15.652 kredilik seslendirmeden önce yapıldığı için yeniden kayıt gerekmedi.
- **Renk = değer kuralı** tek parametreyle (`LALE.boya(..., renk)`) bütün filme yayıldı; üslup kapısından render'a kadar kare başına ~0,3–0,6 sn.

## Ne zorladı, ne öğrendik
- **Kodla çizilen kıyafetin kendiliğinden simge üretmesi:** kaftanın önündeki açık şerit + kuşak, koyu silüette **haç**; beyaz sivri börk koyu kalabalıkta **kukuleta**; kemerin ortasındaki kandil **mihrap** gibi okundu. Üçü de kurgu özetinde değil, tam boy karede ve kalabalık planında görüldü. **Ders:** her yeni figür kiti (giysi) tek başına, önden ve arkadan, koyu ve açık zeminde bir kez tam boy çizilip hassasiyet gözüyle bakılır; sonra sahneye konur.
- **Gerçek görselde alegori:** 1637 hiciv gravüründe Flora ve "Ydel hope" açık göğüslü; sol üstte kilise kulesi. Dönemin sanatında olağan, ama kanalın kitlesi için kadraja alınmadı; yalnız iki güvenli ayrıntı (meyhane köşe resmi, yerdeki adlı laleler) kullanıldı. Kural (Mary Stuart): gerçek görsel tam boyda, her köşesine bakılarak incelenir.
- **Commons istek sınırı (429):** API ve standart dışı genişlikteki küçük resimler sık sık reddedildi; 1920 px standart boy ve istekler arasında 20–60 sn bekleme ile ancak iki görsel indi. **Ders:** görsel listesi erken çıkarılır, indirme arka planda uzun beklemelerle yapılır.
- **Scribe'ın izin denetleyicisine takılması:** tahmini 0 kredi olsa da çağrı durduruldu; sessizlik hizalaması yetti. Kelime düzeyinde doğrulama yok; kulak denetimi kullanıcıda (`yayin.md`).
- **Ekran yazısı alt bandı:** künyeler ilk taslakta y ≈ 980'deydi; render'dan önce bütün `over` çağrıları tarandı.
- **Kanca süresi:** ilk taslak (rev1) 680 karakterle ~53 sn'ydi; rev2'de 596 karakter, ses kaydında hikâye 0:44,6'da başladı. Kanca bölümüne kişi ekmek (İbrahim Paşa, Patrona Halil, "Lale Devri" adı) süreyi sınıra itiyor; ekilecek kişi tek cümleye sığmalı.

## Fable son yorumu (izleyici gözü dahil; ayrıntı `uretim_plani.md` → Fable danışmaları 2, raporlar `fable_son_okuma/`)
- **İzleyici kişilikleri işe yaradı:** üç farklı izleyici (telefonda sabırsız öğrenci, TV'de abone öğretmen, ekonomi merakıyla gelen pazarlamacı) zamanlı bir izleme günlüğü yazdı. Üçünün **ortak** düştüğü yerler kanalın kendi derslerinin tam yerleriydi (kancadan sonra ön hikâye 0:44; hikâye bitince "video bitti" hissi 5:53; art arda belge 8:10; tek planda soyut tez 8:48). Tek kişinin düşüşü zevk, ortak düşüş bulgu sayıldı. Seslendirme sabitken bu yerler görüntüyle (yeni plan, sözcüğe bağlı eylem, olay) karşılandı.
- **Doğrulayıcı katmanı gerekliydi:** Fable'ın 59 mercek bulgusundan birkaçı yanlış ya da abartılıydı (meşale/mızrak, kopuk el, "kaynaksız" satırlar aslında Aktepe'de). Her bulgu ayrı bir ajanla karede ve kaynakta sınandı; doğrulayıcılar ayrıca kök nedenleri koda kadar izledi (künye paneli tek satır; lale boyası örtüsüz).
- **Kod çizimi yine simge üretti:** servi + kayık (haç), kapı + pencere (bomba), kabuk ve yastıkta halka tarama (hedef tahtası), başın yanında açık bohça (hale), belde çizgili oval (kalkan), alna giden el (selam). Son üçü düzeltme sırasında başkanın kare kontrolünde çıktı: **her düzeltme kendisi yeni bir simge üretebilir; düzeltilen her plan tam boy karede yeniden bakılır.**
- **Kullanıcının renk önerisi:** filmde değil kapakta uygulandı (kanıt: izleyicilerin üçü de filmde renk kuralını övdü, kapağı soluk buldu).

## Gerileme okuması (23 Kasım; iki Fable hassasiyet okuyucusu + düzeltme doğrulayıcısı, yeni render üstünde)
- 29 düzeltmeden 25'i tam; engelleyici yok. Kalan dört: kaftanın önünde ince açık çizgi (kenar ışığı dar redingotun hattını izliyordu, geniş kaftanın içine düşüyordu), Patrona'nın çıkını (üçüncü biçimde de kalkan okundu → kaldırıldı), liste satırından geçen kâğıt tarama çizgisi (satırların arkasına temiz kâğıt), sandıktaki soğanlar.
- **Halka tarama ("rad") yuvarlak nesnede hedef tahtası okunuyor; tek tek değil kök nedeninden düzeltildi:** sarık, soğan, kese, para, halat, hokka, mühür. Soğan artık boyuna kabuk çizgisiyle (soğana daha çok benziyor). Çark, güneş, kandil gibi doğası gereği halkalı küçük şeyler kaldı.
- Ayrıca: grafiğin ilk saniyesinde eğri aşağı iniyordu (fiyat artarken düşüş), İkdam manşetinden sütun çizgisi geçiyordu, iki gerçek görsel künyesi sağ kenara 30 px kalıyordu, düz uzanan üç kol, gemi gövdesi yürüyen figürün arkasından geçiyordu (servi + kayığın figürle tekrarı).
- **Teslim:** gravürün ince taraması kodlayıcıyı şişiriyor: x265 CRF 26 "100 MB kopyası" 266 MB çıktı. 100 MB altı kopya iki geçişli sabit bit hızıyla (1,15 Mbps) üretildi; YouTube kopyası H.264 CRF 22 (~345 MB, gönderim sınırı 400 MiB).

## Açık kalanlar
- Kulakla son onay kullanıcıda (`yayin.md` → "Kulakla bakılacaklar").
- Shorts yapılmadı (isteğe bağlı; aday kesitler `youtube.md`).
- Leyster'in lale kitabı indirilemedi; ileride C bölümüne ikinci gerçek görsel olarak eklenebilir.
- Sonuçlar 48. saat (4 Aralık) ve 7. gün (9 Aralık) verisiyle `CLAUDE.md`'ye ve `analiz/tahminler.md`'ye (L1–L3) yazılır: Türkçe boşluk ölçütünün ilk sınaması.

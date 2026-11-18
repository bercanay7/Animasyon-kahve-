# Mary Stuart ve I. Elizabeth: geriye bakış (18 Kasım 2026)

Kanalın ilk "Kitapların Sorduğu Sorular" videosu: Stefan Zweig'ın *Maria Stuart*'ı (1935), 20:49, sessiz film üslubu, kurulsuz üretim (kullanıcının kararı; Fable iki noktada danışman).

## Ne işe yaradı
- **Talep kontrolü konuyu doğru kapıdan açtı.** En güçlü Türkçe kapı "I. Elizabeth" (yüz binlerce izlenmeli videolar), "kraliçe elizabeth" II. Elizabeth'e gidiyor, en çok merak edilen an "idam". Başlık ve kapaklar buna göre kuruldu; Fable "I. Elizabeth"i başlıkta öne aldırdı (akışta başlık ~45–50 karakterde kesilir).
- **Zweig omurga, birinci el kaynak denetçi.** Zweig'ın tezleri "Zweig'a göre" kipinde; Casket mektuplarının kaybı ve Melville'in tanıklığı aynı bölümde dürüstçe yan yana. Fable'ın senaryo denetimi Zweig'ın hükmünün ters aktarıldığını yakaladı (M10).
- **Hazır motor + kendi çekim sistemimiz:** LemoLab silent-film (MIT) yeniden çizim ve film baskısı, bizim `S()/Wd()/plan()` sistemimiz ve gerçek CC0 gravürler. Gerçek gravürler motordan geçince filmin en güçlü kareleri oldu; çizilmiş figürler uzak ve orta planda kaldı.
- **Ara yazı kartları kişilerin kendi sözlerini taşıdı** (Mary, Elizabeth, Knox, Melville, Paulet): sessiz film dili ile "iç dünya kaynaktan" kuralı aynı şeye hizmet etti.
- **Tek renk anlatıyı bağladı:** kırmızı yalnız Mary'nin (Solway'deki etek, mühürler, arma iddiası, idam sabahı); kapak B ve Shorts filmin ilk karesinden.
- **Ölçerek hızlandırma:** yazılımsal WebGL'de kare 0,95 sn idi; Redraw'ın iki bulanıklık geçişi tek geçişe, ağırlıklar JS'e, tarama yalnız karanlığa alınınca 0,55 sn. Bulutlar ve gölge oyunu için süzgeç yerine düşük çözünürlüklü tuval + büyütme (22 sn → 0,5 sn).
- **15 kare/sn görüntü:** sessiz film hızı; 30 kare/sn çıktıda kareler ikişer aynı, render yarı süre.

## Ne zorladı
- **Sessizliğe dayalı hizalama** iki cümleli satırlarda ve iki nokta duraklamalarında yanıldı (D10, I12–I13, I17, E12). Çözüm: satır alt cümlelere bölünerek hizalandı, kalan beş sınır sessizlik ölçümüyle elle zorlandı (`vo/sinir.json`). Whisper olsaydı gerekmezdi.
- **Çizilmiş figürler yakın planda kaba.** Kural doğrulandı: yüz ve el gerçek gravürden; çizim uzak siluet.
- **Hassasiyet görüntüde:** Finden gravürünün köşesindeki ek resim idam anını (balta) gösteriyordu; Fable'ın da işaret ettiği kırmızı lekeler kan gibi okunuyordu; dans sahnesindeki kalkık kollar selama, simetrik anka amblem kartalına benziyordu. Hepsi düzeltildi; ama ilk ikisi render başladıktan sonra fark edildi ve dört parça yeniden üretildi.
- **Dosya boyu:** film greni her karede değiştiği için usta kopya ~3 GB; teslim kopyaları ayrıca sıkıştırıldı.

## Sonraki videoya
1. Gerçek görselleri kullanmadan önce **tam boyutta, her köşesine bakarak** incele (ek resimler, yazılar, şiddet). Bir gravürün küçük ek sahnesi bütün planlara taşınır.
2. Kırmızı gibi tek renk bir gravüre boyanacaksa: koyuluk maskesi + yumuşak kenar + el ve nesneleri çıkarma. Düz çokgen "yapıştırılmış kâğıt", çizgiyle çarpılan koyu leke "kan" okunur.
3. Render'dan önce `tools/kontrol.js` (kurallar) + kurgu özeti + **tam boy kare** kontrolü; özet 480 px'te kusurları gizliyor.
4. Uzun render'ı başlatmadan önce hassasiyet taramasını bitir (29 Ekim dersi yine geçerli).
5. Whisper ortamın kurulum betiğine eklenirse hizalama elle sınır gerektirmez.

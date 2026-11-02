# Şarlken videosu: yeni paket (Kanuni açısı)

## Neden
- **Durum, 14. gün:** toplam yalnız 1,0 B gösterim, göz at payı %13.
  - YouTube videoyu hiç geniş bir göz atma testine sokmadı.
  - Yayın sırasında kanalın kitlesi yoktu; sonra gelen kitle (Sisifos) mit ve felsefe izleyicisi.
- **İçerik güçlü:**
  - 0:30'da kalan izleyici %79, kanalın en iyi açılışı.
  - Ortalama izlenme %41,8.
- **Kanuni açısı:**
  - Türk izleyici "Şarlken"i tanımıyor ama Kanuni'yi tanıyor. Videoda Kanuni bölümü var (11:03).
  - Video 25 Ekim 1555'teki tahttan çekilmeyle açılıyor; kapak vaadi açılışta karşılanıyor.

## Dosyalar
| Dosya | Ne | Kurul |
|---|---|---|
| `kapak_yeni_1_madalyalar.jpg` | "KANUNİ'NİN RAKİBİ / TAHTI BIRAKTI". Kanuni ile Şarlken madalyaları yüz yüze; aralarında yere bırakılmış imparatorluk tacı | TO 9/10, sanat 9/10: ONAY |
| `kapak_yeni_2_salon.jpg` | Aynı yazı. Videonun ilk saniyelerindeki Brüksel salonu: boş taht, Şarlken ve prens | TO 8 → (son düzeltme), sanat: aşağıya bak |
| `kapak_kanuni.py` | Çizim kodu. Videonun motorunu kullanır; `gunluk-shorts/sarlken-uzun-dosya/` içine kopyalanıp `python3 kapak_kanuni.py K1v2` ya da `K3` ile çalışır | |

## Kurul (yeni düzen: iki üye, çapraz eleştiri, başkan kararı; 4 tur)
- **Üyeler:** TO/paketleme stratejisti; sanat yönetmeni ve dönem doğruluğu.
- **1. tur:** iki üye de 6/10 verdi.
  - Yazılar küçüktü.
  - Çatlak taç küçük boyda "iki çan" gibi okunuyordu. Üstelik videoyla çelişiyordu: c0s8'de "Kimse onu tahttan indirmedi" deniyor, oysa çatlak taç "tahttan indirildi" anlamı veriyor.
  - Madalyalar ikiz gibi duruyordu.
  - YouTube'un gerçek süre rozeti "önerilen" listesinde alt yazıyı "TAHTI BIRAK" diye kesiyordu. Bu listeden gelen trafik %45.
- **Çapraz eleştiride ayrışılan noktalar ve başkan kararı:**
  - **Yazı tipi:** TO üyesi Anton önerdi. Sanat üyesi, Anton'un videonun yazı kimliğini bozacağını söyledi. Karar: videonun yazı tipi Cinzel kaldı.
  - **Madalyaların yeri:** sanat üyesi madalyaların yer değiştirmesini önerdi, TO üyesi karşı çıktı. Karar: iki satır yazı üste taşındı. Böylece rozet sorunu da yanlış okuma riski de ortadan kalktı; Kanuni solda, "KANUNİ" sözcüğünün altında kaldı.
- **Doğruluk denetimi:**
  - "Dünyanın yarısına hükmetti" iddiası yanlış; video "Avrupa'nın büyük bölümü" diyor.
  - "En büyük rakibi" iddiası zayıf.
  - 1529'da Viyana'yı Şarlken değil kardeşi Ferdinand savundu; bu yüzden başlıkta böyle bir iddia yok.

## YouTube Studio'da sırayla
1. **Başlık:** `Osmanlı'nın 'İspanya Kralı' Dediği İmparator: Şarlken Neden Vazgeçti?`
   - Testi başlatmadan önce değiştir; test sürerken başlığa dokunma.
   - Başlık kapağı tekrar etmiyor, Osmanlı açısını ve "neden" sorusunu ekliyor.
   - Videoda karşılığı var: c7s10 ve c7s13 (Osmanlı sefer günlüğü ve belgeleri Şarlken için "İspanya kralı" der).
2. **Açıklamadaki bölümler:** `11:03 Sultan: Hiç Karşılaşmadılar (1526–1547)` satırını şöyle değiştir: `11:03 Kanuni: Viyana ve "İspanya Kralı" (1526–1547)`. Böylece Kanuni adı ilerleme çubuğunda görünür ve izleyici o bölüme atlayabilir.
3. **Sabit yorum:** "Kanuni bölümü 11:03'te: Viyana kuşatması ve Osmanlı'nın onu neden 'İspanya kralı' diye andığı."
4. **Test et ve karşılaştır,** bu sırayla:
   1. `kapak_yeni_1_madalyalar.jpg`
   2. `kapak_yeni_2_salon.jpg`
   3. mevcut madalya kapağı ("5 CEPHE TEK ADAM"), kontrol
5. **Bekleme:** günde ~70 gösterimde test uzun sürebilir. Sonuç "fark yok" çıkarsa madalyalı yeni kapak kalır.
6. **İzlenecekler:**
   - Göz atma payı ve gösterim artıyor mu?
   - 0:30 ve 3:00 arasındaki izleyici tutma korunuyor mu?

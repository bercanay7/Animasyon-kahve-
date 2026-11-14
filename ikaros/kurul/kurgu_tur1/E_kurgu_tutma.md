# Kurgu kurulu, tur 1: Üye E (animasyon + kurgu/ritim + tutma)

**Puan: 7,6/10, RED.**

Ölçüm: film 5 fps'te 480×270 gri karelere çevrildi. Bir adımda piksellerin %0,05'inden azı değişiyorsa o adım "durgun" sayıldı. Ayrıca plan başı ve sonu kareleri karşılaştırıldı. Sonuçlar:
- Adımların %25,7'si tamamen durgun.
- Kanal kuralı "animasyon hiç durmasın" diyor; durgun bölgeler aşağıda.

**Güçlü yanlar:**
- 0. kare kapaktaki figürün aynısı. Anlatım 0,74 sn'de başlıyor ve kapağın vaadi ("iki uyarı") 3 sn'de karşılanıyor.
- Kesmeler kelimeye kilitli (`@güneşe`, `@yalan`, `@bacak`…).
- Art arda aynı ölçekte iki plan yok.
- Paletin saat yayı hikâyeyi taşıyor.
- Düşüş (P27–P32) grafik olmadan anlatılıyor.
- P17'deki gölge ve keklik tohumu F bölümünde karşılığını buluyor.
- P48'de ışığın geri dönüşü güçlü.

## Düzeltmeler (önem sırasıyla)

1. **P38–P39 (3:28,7–3:41,6; 12,9 sn) tamamen donuk.**
   - Ölçüm: ilk ve son kare arasındaki en büyük fark 2/255. Sahnenin en ağır cümlesi ("kıskandı… aşağı attı… yalan") bu planlarda geçiyor.
   - Neden: `a5.js:58–70` içinde `st.lt` kullanılmıyor.
   - Çözüm, üç adımda:
     - **(a) "Usta onu kıskandı":** kısa bir orta plan. Daidalos'un uzun gölgesi çırağın ve pergelin üstüne düşer; bu P17'ye kafiye olur.
     - **(b) Akropolis:** figürlere doğru itme, `{cx: 960→1260, cy: 540→500, z: 1→1,35}`.
     - **(c) P39:** "yalan" kelimesinde baş ya da göz ışığı izleyiciden kaçsın.
   - İtiş yine gösterilmez.

2. **P50 Bruegel (5:07,8–5:19,5; 11,8 sn) donuk.**
   - Çözüm: çiftçiden bacaklara yavaş kaydırma, `cx: 800→1450`, `cy: 540→700`, `z: 1→1,6`. Hareket `Wd('G08','bacak')`'ta bacaklarda bitsin.
   - **P51:** bacaklar yakın planda yaklaşık 270 px. Bu, kırmızı çizgi 6'ya ("bacaklar küçük olur") ve cümlenin anlamına ("kimse bakmıyor") aykırı.
     - Keklik dalda kalsın (Bruegel'in tablosunda da var).
     - Bacaklar 60 px'in altına insin ya da P51 kaldırılsın.

3. **Kırılma: P42 (3:55,1–4:02,8) ve P43'ün başı.**
   - Ölçümler:
     - P42'nin %92'si durgun.
     - P43 ilk 1,6 sn boş siyah: `a6.js:13` önce `fillAll`, ilk pano `güneşe`yi bekliyor.
     - Sonuç: filmin en sert cümlesinden sonra ~4,2 sn hiçbir şey değişmiyor.
   - Çözüm:
     - `Wd('F08','atmıştı')`'ta GECE paleti afişin üstünden çapraz rakleyle geçsin.
     - "ORTADAN UÇ" bandı çatlasın (P44'te planlanan ama görünmeyen çatlak buraya alınsın).
     - Daidalos'un gözüne doğru yavaş itme (yaklaşık 900, 500).
     - P43'ün ilk panosu plan başında basılsın.

4. **"Üç uçuş" (4:02,8–4:47) vaaz gibi duruyor.**
   - Ölçümler:
     - 44 sn karanlık ve hareketsiz semboller. Durgun oranları: P44 %85, P45 %82, P46 %92.
     - P44'teki kürsü ve usta P46'nın sol yarısında 13 sn sonra aynen tekrarlanıyor.
   - Çözüm, her görüntüye bir eylem:
     - **P44:** "dayanamadı"da kürsü basamak basamak yükselir, bant çatlar.
     - **P46:** solda kürsü durmadan yükselir. Sağda keklik kalkmaya çalışır ve geri düşer ("cesaret edemeyen").
     - **P47:** "Unutulan uyarı buydu"da P16'daki "ÇOK ALÇAKTAN DA UÇMA" bandı ya da P03'ün suya değen kanat ucu gece paletinde yeniden basılsın. Kancanın cevabı açılışa görsel kafiyeyle bağlanır.

5. **P15 (1:13,75–1:16,5): 2,8 sn boş kâğıt.**
   - Anlatıcı "Ortadan uç, İkaros" derken ekranda iki çizgiden başka bir şey yok. Bu, boş kâğıt kuralını (≤ 2 sn) aşıyor.
   - Çözüm (`a2.js:68–75`):
     - Orta banttaki küçük İkaros plan başında girsin.
     - "ORTADAN UÇ" ilk "ortadan" kelimesinde basılsın.
     - Dalga ve güneş şimdiki gibi kalsın.

6. **Açılış (0–16 sn).**
   - Ölçümler:
     - P01 6,9 sn aynı kadraj. Yalnız halkalar hareket ediyor; adım başına piksellerin ~%1,5'i değişiyor.
     - P03 7 sn aynı görüntü; içinde 14,2–16,2 arası 2 sn sessizlik var. Bu tam 10–15 sn kayıp penceresi.
   - Çözüm:
     - **P01:** itme `z 1→1,08` ve tüylerde rüzgâr.
     - **P03:** "sırrı" kelimesinde bir tüy kopsun, koyulaşıp batsın.
     - **P04:** 1 sn önce girsin (A03 sonu + 0,9 sn).
   - **0:30 bölgesi:**
     - P04 (%87) ve P07 (%100) düşük hareketli. İkisine P06 gibi kayma ekle (`cx: 960 + st.lt*10`).
     - P07'de ufuktaki uzak karaya doğru bir kuş dizisi geçsin. Bu özlemi anlatır ve "gök açık" cümlesini hazırlar.
   - **Tahminim:** 0:30'da kalan oran düzeltme olmadan ~%68 (Milton ve Prometheus düzeyi), düzeltmeyle %72'nin üstü.

7. **P40 (3:41,6–3:45,0): dönüşüm okunmuyor.**
   - Düşen çocuk (`h:10`, 'near') koyu kayanın üstünde 'near' rengiyle çizildiği için görünmüyor.
   - Dönüşüm kayada kıvılcım gibi okunuyor ve ortaya keklik çıkmıyor. Kadraj da P38'in tekrarı.
   - Çözüm:
     - Daha sıkı bir kadraj kullanılsın.
     - Yakalama noktası kayanın sağında, gökte olsun (≈1450, 520) ve huzme oraya insin.
     - Siluet açık mürekkeple çizilsin.
     - Tüy patlamasından bir keklik çıkıp sağa uçsun; bu P41'e köprü olur.

8. **P35 (3:14,6–3:22,6): ölçek uyuşmuyor.**
   - Keklik ~300 px; yerine gelen çocuk (`h:30`) ~110 px. Bu "kuş çocuğa dönüştü" diye değil, "kuş gitti, uzakta biri var" diye okunuyor.
   - Çözüm: çocuk kuşun kütlesinde olsun, `h≈70`, aynı noktada (1000, 780) çömelmiş.

9. **Rakle hiç yok.**
   - Bütün palet değişimleri plan başında. `film.js:98` yalnız çekim içindeki değişimde rakle çiziyor, bu yüzden 52 geçişin hepsi kesme.
   - Kesme doğru varsayılan, ama üslup kapısının rakle imzası filmde hiç görünmüyor.
   - Öneri: rakle 2–3 anlamlı anda kullanılsın:
     - E01'de "yumuşadı" (mum erirken gök ısınır);
     - F08'de "atmıştı";
     - isteğe bağlı D04'te "sevincine".
   - Bu, `PALT`'a kelimeye bağlı çapa eklemeyi gerektiriyor. Ortak dosya olduğu için başkan yapar.

10. **P19 (1:37,6–1:47; 9,4 sn): %89 durgun.**
    - Öpüş anı tutulabilir, ama iki başa doğru yavaş itme gerekir: `z 1→1,1`, merkez ≈ (900, 450).

11. **P53 (bitiş, 24,6 sn).**
    - YouTube öğeleri yalnız son 20 sn'de gösterilebilir. Bu yüzden boş video kutusu 330,65–335,2 arasında eksik bir öğe gibi görünüyor.
    - Çözüm: yer tutucu 335,2'den sonra basılsın ya da plan 20 sn'ye insin.

12. **P22 (2:00,8–2:08): hassasiyet kuruluna not.**
    - Balıkçı tek dizi üstünde (≈1420, 790) göğe bakıyor; hemen ardından "tanrı sandılar" geliyor. Bu, kırmızı çizgi 5'e yakın.
    - Öneri: balıkçı kayada otursun ya da ayakta dursun.

**Daha küçük notlar:**
- P32 (%82) ve P33 (%100) durgun. İkisine de hafif kayma yetiyor.
- Plan süreleri kurala uyuyor: hepsi 1,9–11,8 sn arasında (P53 hariç).
- Yazı levhaları sınırın içinde: en uzunu P16, 8,1 sn. P52'nin yazısı yaklaşık 5 sn ekranda kalıyor.

## En emin olmadığım nokta
Bölüm aralarındaki 2 sn'lik nefesler (14,2, 46,1, 105,0, 179,4 ve 240,3 sn) ritim açısından doğru. Ama hepsi donuk bir karenin üstüne düşüyor.

Kulakla dinlemeden, müziğin bu boşlukları canlı tuttuğunu varsayamıyorum. 14,2 sn civarı ölçüldü: anlatım yok, müzik -19 ile -24 LUFS arasında (anlık ölçüm), yani müzik çalıyor.

Bu yüzden 14,2 ve 240,3 sn'deki iki duraklamayı tutma açısından riskli sayıyorum. Ötekileri kullanıcının kulağına bırakıyorum.

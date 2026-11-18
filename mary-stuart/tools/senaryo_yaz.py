"""mary-stuart/senaryo.json ve senaryo_okuma.md üretir.
Satır: (etiket, altyazı metni, kaynak[, tts metni]). tts verilmezse altyazı metninden üretilir:
rakamlar Türkçe sözcüğe, yabancı adlar okunuş biçimine çevrilir (ElevenLabs Emrullah için).
Kimlikler bölüm harfi + sıra; çıkarılan cümlenin numarası boş kalır (Kafka dersi)."""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── okunuş (yalnız tts) ──
OKU = [("En ma fin est mon commencement", "On ma fen e mon komansman"), ("Stefan Zweig", "Ştefan Tsvayg"), ("Zweig", "Tsvayg"),
       ("Mary Stuart", "Meri Stuart"), ("Mary", "Meri"), ("Lord Darnley", "Lord Darnli"), ("Darnley", "Darnli"), ("Bothwell", "Botvel"),
       ("Rizzio", "Ritsio"), ("Holyrood", "Holirud"), ("Leith", "Lit"), ("John Knox", "Con Noks"), ("Knox", "Noks"), ("James Melville", "Ceyms Melvil"),
       ("Melville", "Melvil"), ("Robert Dudley", "Robırt Dadli"), ("Dunbar", "Danbar"), ("Carberry", "Karberi"), ("Loch Leven", "Lok Liven"),
       ("Langside", "Lengsayd"), ("Dundrennan", "Dandrenın"), ("Solway", "Solvey"), ("Workington", "Vörkington"), ("Carlisle", "Karlayl"),
       ("Tutbury", "Tatberi"), ("Sheffield", "Şefild"), ("Chartley", "Çartli"), ("Francis Walsingham", "Frensis Volsingım"), ("Walsingham", "Volsingım"),
       ("Burton", "Börtın"), ("Anthony Babington", "Entıni Bebingtın"), ("Babington", "Bebingtın"), ("Fotheringhay", "Fozeringey"),
       ("Amias Paulet", "Eymiyas Pole"), ("Paulet", "Pole"), ("Davison", "Deyvisın"), ("Westminster Abbey", "Vestminster Ebi"), ("Westminster", "Vestminster"),
       ("Edinburgh", "Edinbıra"), ("Greenwich", "Grinic"), ("James", "Ceyms"), ("Henry", "Henri"), ("Peterborough", "Pitırbırı")]
BIR = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
ON = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
def sayi(n):
    n = int(n); s = []
    if n >= 1000: s.append(('' if n // 1000 == 1 else BIR[n // 1000] + ' ') + 'bin'); n %= 1000
    if n >= 100: s.append(('' if n // 100 == 1 else BIR[n // 100] + ' ') + 'yüz'); n %= 100
    if n >= 10: s.append(ON[n // 10]); n %= 10
    if n: s.append(BIR[n])
    return ' '.join(x.strip() for x in s if x.strip()) or 'sıfır'
def tts_of(t):
    for a, b in OKU: t = re.sub(r'(?<![\wçğıöşüÇĞİÖŞÜ])' + re.escape(a) + r'(?![a-zçğıöşü])', b, t)
    t = re.sub(r"(\d+)'(\w+)", lambda m: sayi(m.group(1)) + m.group(2), t)
    t = re.sub(r'\d+', lambda m: sayi(m.group(0)), t)
    t = t.replace('“', '"').replace('”', '"')
    return t[:1].upper() + t[1:] if t else t

S = []
def b(bolum, soru, rows):
    for i, r in enumerate(rows):
        tag, alt, kay = r[0], r[1], r[2]
        tts = r[3] if len(r) > 3 else tts_of(alt)
        S.append(dict(id=None, bolum=bolum, soru=soru if i == 0 else None, tts=(f'[{tag}] ' if tag else '') + tts, alt=alt, kaynak=kay))

b('Kırmızı ve deniz', None, [
 ('softly', '8 Şubat 1587, sabah. Bir kadın siyah elbisesini çıkarıyor. Altından kırmızı çıkıyor.', 'K34; kapak B vaadi 0:00; L1 açılır (cevap L12–L14)'),
 ('', 'Bu kadın İskoçya Kraliçesi Mary Stuart. Birazdan idam edilecek.', 'K34'),
 ('', 'Onu buraya, neredeyse on dokuz yıl önce verdiği tek bir karar getirdi.', 'K26'),
 ('', '1568 baharında, yenilmiş ve kaçan bu kraliçe küçük bir balıkçı teknesine bindi.', 'K21; kapak A vaadi'),
 ('', 'Önünde iki kıyı vardı: ailesinin yaşadığı Fransa ya da rakibi Elizabeth\'in İngilteresi.', 'K20'),
 ('', 'Dostları "Fransa" dedi. Mary, rakibine sığındı.', 'K20; L2 açılır (cevap H)'),
 ('', 'İki kraliçe on dokuz yıla yakın aynı adada yaşadı ve bir kez bile yüz yüze gelmedi.', 'K09, K26'),
 ('curious', 'Stefan Zweig bu hikâyeyi iki ilkenin savaşı diye anlatır: biri kalbiyle yaşar, öteki aklıyla. Sen hangisisin? Ve hangisi kazanır?', 'Z02; başlığın sorusu; L4 açılır (cevap M)'),
 ('', 'Hikâye bir beşikte başlıyor.', 'geçiş; hikâye ~0:40'),
])
b('Altı günlük kraliçe', 'Bir arma, iki kuzeni nasıl düşman yaptı?', [
 ('', 'Aralık 1542. İskoçya, İngiltere\'ye karşı bir savaşı kaybetmiş. Kral James yatağa düşmüş.', 'Solway Moss, 24 Kasım 1542 (Zweig 3. bölüm); K01'),
 ('', 'Ölüm döşeğindeyken bir kızı doğar. Altı gün sonra kendisi ölür.', 'K01'),
 ('', 'Mary, altı günlükken İskoçya kraliçesi olur.', 'K01'),
 ('', 'Babasını yıkan o yenilginin adı Solway\'di. Kızının kaderini değiştirecek deniz de aynı adı taşıyacaktı.', 'Solway Moss / Solway Firth (aynı bölge)'),
 ('', 'İngiltere kralı Sekizinci Henry bu bebeği oğluna gelin istedi. İskoçlar reddedince savaş açtı.', '"Rough Wooing" (standart)'),
 ('', 'Mary beş yaşındayken denizden Fransa\'ya gönderildi.', 'K02'),
 ('', 'Fransız sarayında, şiir ve dans arasında büyüdü. On beşinde veliahtla evlendi, on altısında Fransa kraliçesi oldu.', 'K03'),
 ('', 'O yıl hayatının en pahalı hatasını yaptı.', 'K04'),
 ('', 'Kocasıyla birlikte armalarına İngiltere\'nin kraliyet armasını da kattılar. Anlamı açıktı: İngiltere\'nin gerçek kraliçesi benim.', 'K04'),
 ('', 'Çünkü Katoliklerin gözünde İngiltere tahtındaki Protestan Elizabeth meşru değildi.', 'K04 (Katolik görüş: VIII. Henry\'nin Anne Boleyn evliliği geçersiz)'),
 ('', 'Elizabeth yıllarca tek bir şey istedi: Mary bu armadan vazgeçtiğini imzalasın. Mary hiç imzalamadı.', 'K04 (Edinburgh Antlaşması 1560, onaylanmadı); L3 açılır'),
 ('', 'On sekizine üç gün kala genç kocası öldü. Fransa\'da artık yeri yoktu.', 'K05'),
 ('', 'Ağustos 1561\'de Calais limanından bir kadırgaya bindi. Yanındaki şair Brantôme o günü anılarında anlatır.', 'K41 (Brantôme, görgü tanığı)'),
 ('', 'Liman ağzında, gözlerinin önünde bir gemi battı. Mary, "Tanrım, bu yolculuk için ne kötü bir işaret!" dedi.', 'K41'),
 ('sad', 'Sonra kıça yaslandı ve beş saat boyunca kıyıya bakıp ağladı: "Elveda Fransa, elveda Fransa. Seni bir daha göremeyeceğim."', 'K41'),
 ('', 'Fransa\'yı bir daha hiç görmedi.', 'K41; K33 (Fransa\'ya gömülme isteği de reddedildi)'),
 ('', 'Dul kraliçe, hiç tanımadığı ülkesine dönüyordu.', 'K06'),
])
b('Siste dönüş', 'Ona inanmayan bir ülkede kraliçe olmak nasıl bir şeydi?', [
 ('', '19 Ağustos 1561. Mary, Leith limanına iniyor.', 'K06'),
 ('', 'O gün ülkenin en sert vaizi John Knox, gökyüzünü bile ona karşı tanık gösterdi.', 'K06'),
 ('', 'Knox\'a göre göğün yüzü bu ülkeye ne getirildiğini açıkça söylüyordu: keder, acı ve karanlık.', 'K06 (Knox, IV)'),
 ('', 'Sis öyle kalındı ki, iki çizme boyu ötesi görülmüyordu.', 'K06'),
 ('', 'Mary Katolikti. İskoçya bir yıl önce Protestan olmuştu.', '1560 Reform Parlamentosu (standart)'),
 ('', 'Ama bu genç kadın ilk yıllarında şaşırtıcı bir akılla yönetti: kimsenin inancına dokunmadı, kendi ayinini yalnız kendi şapelinde yaptı.', 'standart; Zweig 7. bölüm'),
 ('thoughtful', 'Ve o yıllarda bir tek şeyi çok istedi: güneydeki kuzenini görmeyi.', 'K07'),
])
b('Görmediği kuzen', 'Hiç karşılaşmadan birbirlerini nasıl tanıdılar?', [
 ('', '1562 yazında Mary, Elizabeth\'e bir yüzük gönderdi: kalp biçiminde kesilmiş bir elmas.', 'K07'),
 ('', 'İngiliz elçisine şöyle dedi: "İyi niyetimi bundan daha iyi anlatan bir şey bilmiyorum."', 'K07 (Randolph, 17 Haziran 1562)'),
 ('', 'Elizabeth de karşılığında bir elmas yolladı. O yaz yüz yüze görüşmeyi bile planladılar.', 'K08, K09'),
 ('', 'Görüşme ertelendi. Bir daha da hiç gerçekleşmedi.', 'K09'),
 ('', 'Bu yüzden ikisi birbirini yalnız elçilerin gözünden tanıdı.', 'anlatım'),
 ('', '1564\'te Mary\'nin elçisi James Melville, Londra\'da Elizabeth\'in karşısındaydı. Anılarında o günleri anlatır.', 'K10'),
 ('', 'Elizabeth ona sorular sordu: Kimin saçı daha güzeldi, Mary\'nin mi, kendisinin mi? Hangisi daha güzeldi?', 'K10'),
 ('', 'Sonra boylarını sordu. Melville, Mary\'nin daha uzun olduğunu söyleyince Elizabeth şöyle dedi: "O hâlde fazla uzun; çünkü ben ne fazla uzunum ne fazla kısa."', 'K10 (Melville 1827, 1564)'),
 ('', 'İki kraliçe arasındaki rekabetin en insani hâli buydu: hiç görmediğin birine kendini ölçtürmek.', 'anlatım'),
 ('', 'Ama Elizabeth\'in aklı başka bir şeyle meşguldü: Mary kiminle evlenecekti?', 'K11'),
 ('', 'Çünkü Mary\'nin kocası, bir gün İngiltere\'nin de kralı olabilirdi.', 'Mary, Elizabeth\'in olası varisi (standart)'),
 ('', 'Elizabeth ona tuhaf bir aday önerdi: kendi gözdesi Robert Dudley\'i.', 'K11'),
 ('', 'Mary kalbini dinledi ve başka birini seçti: uzun boylu, yakışıklı, on dokuz yaşındaki kuzeni Lord Darnley.', 'K12; Darnley Aralık 1545 doğumlu'),
 ('', 'Zweig\'e göre bu seçim, onun başka zaman berrak olan aklının tamamen dışında yapılmıştı. Gerçek tutku, der Zweig, hesaplanamaz.', 'Zweig 9. bölüm ("unanalysierbar und irrational"; "jenseits ihres sonst hellen Verstandes")'),
 ('', 'Temmuz 1565\'te evlendiler.', 'K12'),
])
b('Holyrood\'daki gece', 'Kalbiyle seçtiği adam ona ne yaptı?', [
 ('', 'Birkaç ay içinde Mary, Zweig\'in deyişiyle olgunlaşmamış ve kendini beğenmiş bir adamla evlendiğini gördü.', 'Zweig 9. bölüm ("unreif, eitel")'),
 ('', 'Ona kral unvanını verdi ama yetkisini vermedi.', 'standart (crown matrimonial verilmedi)'),
 ('', 'Darnley\'nin kıskançlığı, kraliçenin İtalyan sekreteri David Rizzio\'ya yöneldi.', 'standart'),
 ('', '9 Mart 1566 akşamı Mary, Holyrood sarayında küçük bir odada yemekteydi. Altı aylık hamileydi.', 'K13'),
 ('', 'Darnley\'nin de aralarında olduğu silahlı lordlar odaya girdi ve Rizzio\'yu onun gözü önünde sürükleyip öldürdü.', 'K13; görsel: gölgeler, şiddet gösterilmez'),
 ('', 'Mary bunu iki yıl sonra kendi kalemiyle yazacaktı: hizmetkârımı gözümün önünde, karnım burnumdayken öldürdüler.', 'K13 (Workington mektubu, Camden)'),
 ('', 'Ama o gece ağlayıp beklemedi. Kocasını korkutup kendi yanına çekti; ikisi gece yarısı saraydan kaçtılar.', 'standart (Mart 1566, Dunbar\'a kaçış)'),
 ('', 'Üç ay sonra bir oğlan doğurdu: James.', 'K14'),
 ('', 'Haber Londra\'ya ulaştığında Elizabeth, Greenwich\'te yemekten sonra dans ediyordu.', 'K14 (Melville: "in gret merines and dancing efter supper")'),
 ('', 'Melville\'e göre Elizabeth elini yanağına koyup oturdu ve hanımlarına şöyle dedi: "İskoçya kraliçesi güzel bir oğlan doğurdu, bense kısır bir kütüğüm."', 'K14 (Melville 1827, s. 158–159)'),
 ('', 'Ertesi sabah elçiyi sevinçli bir yüzle karşıladı.', 'K14'),
 ('', 'Uzaktaki Elizabeth buydu: yüzü sevinçli, içi kederli. Aklı hep kalbinin önünde.', 'anlatım'),
])
b('Bothwell', 'Mary\'yi tutku mu yıktı, zorbalık mı?', [
 ('', 'Mary ile Darnley artık birbirine yabancıydı.', 'standart'),
 ('', '10 Şubat 1567 gecesi Edinburgh\'da, Darnley\'nin kaldığı ev havaya uçtu.', 'K15'),
 ('', 'Darnley\'nin cesedi bahçede bulundu. Patlamadan değil, boğularak ölmüştü.', 'standart (Kirk o\'Field)'),
 ('', 'Herkesin parmağı tek bir adamı gösterdi: sert, cesur, gözü kara bir sınır lordu, Bothwell Kontu.', 'standart'),
 ('', 'Elizabeth o günlerde Mary\'ye bir mektup yazdı. Belki de ona en yakın olduğu an.', 'K16'),
 ('', '"Kulaklarım öyle sağır oldu, yüreğim öyle korktu ki, yazacak gücüm zor yetiyor. Sizin için, ondan daha çok üzülüyorum."', 'K16 (24 Şubat 1567)'),
 ('', 'Ve onu uyardı: onurunu korusun, bu cinayeti cezasız bırakmasın.', 'K16'),
 ('', 'Mary bu uyarıyı dinlemedi. Bothwell bir mahkemede aklandı.', 'standart (12 Nisan 1567)'),
 ('', 'Birkaç gün sonra Bothwell, Mary\'nin yolunu kesti ve onu Dunbar kalesine götürdü.', 'K17'),
 ('', 'Yanında esir alınanlardan biri, o elçi Melville\'di. Anılarında iki şey yazar.', 'K17'),
 ('', 'Bothwell\'in yüzbaşısı bunun kraliçenin rızasıyla olduğunu söylemişti. Melville ise şöyle yazar: kraliçe onunla evlenmekten başka yol bulamadı, çünkü Bothwell onu zorla almıştı.', 'K17 (Melville 1827, s. 177)'),
 ('', 'Üç hafta sonra Mary, Bothwell\'le evlendi. Darnley\'nin ölümünden yalnız üç ay sonra.', 'K18'),
 ('', 'Zweig hikâyenin tam ortasına burada bir tutku koyar.', 'Z04; Zweig 13. bölüm "Bir tutkunun trajedisi"'),
 ('', 'Ona göre Mary, Bothwell\'e delice âşıktı. Kanıtı da Mary\'nin ona yazdığı söylenen mektuplar ve şiirlerdi.', 'Z04, K24'),
 ('', 'Bu mektupların asılları kayıp. Yalnız düşmanlarının sunduğu kopyalar kaldı; bugün birçok tarihçi değiştirildiklerini düşünüyor.', 'K24'),
 ('', 'Zweig ise onlara inandı. Bu hikâyeyi onun gözüyle anlatıyoruz, ama karar senin: tutku mu, zorbalık mı?', 'dürüstlük cümlesi (yorum)'),
])
b('Gölün ortasındaki ada', 'Bir kraliçe tahtını nasıl kaybeder?', [
 ('', 'Lordlar ayaklandı. Haziran 1567\'de, Carberry tepesinde iki ordu karşılaştı; savaş olmadı.', 'K18'),
 ('', 'Bothwell kaçtı, Mary teslim oldu. Onu bir daha hiç görmedi.', 'standart'),
 ('', 'Lordlar onu Edinburgh sokaklarından geçirdi; halk ona hakaretler yağdırdı.', 'standart'),
 ('', 'Sonra Loch Leven gölünün ortasındaki küçük bir ada kalesine kapatıldı.', 'K18'),
 ('', 'Orada ikiz bebeklerini düşürdü.', 'standart (Temmuz 1567)'),
 ('', 'Birkaç gün sonra, hasta yatağındayken, tahttan feragat belgesini zorla imzalattılar. Bir yaşındaki oğlu James kral ilan edildi.', 'K18'),
 ('', 'Yirmi dört yaşındaydı. Tahtını, kocasını ve oğlunu kaybetmişti.', 'yaş: Aralık 1542 → Temmuz 1567'),
 ('', 'Ama on bir ay sonra gölde bir kayık bekliyordu.', 'K19'),
 ('', '2 Mayıs 1568 gecesi, kalenin anahtarlarını çalan genç bir uşak onu kaçırdı. Uşak anahtarları göle attı.', 'K19 (standart)'),
 ('', 'Birkaç gün içinde etrafında altı bin kişilik bir ordu toplandı.', 'standart'),
 ('', '13 Mayıs\'ta, Langside\'da, bu ordu kırk beş dakikada dağıldı.', 'K19 (standart)'),
])
b('Solway', 'Neden rakibine sığındı?', [
 ('', 'Mary güneye kaçtı.', 'K23'),
 ('', 'Bir ay sonra o kaçışı kendi eliyle şöyle anlatacaktı:', 'K23'),
 ('sad', '"Doksan iki mil, durmadan, attan inmeden. Sonra çıplak yerde uyumak, ekşi süt içmek, ekmeksiz yulaf yemek. Üç gece, baykuşlar gibi."', 'K23 (Carlisle, 21 Haziran 1568; Labanoff II)'),
 ('', 'Sonunda kıyıda, Dundrennan manastırına sığındı.', 'standart'),
 ('', 'Karşısında Solway körfezi vardı. Körfezin öbür yanında İngiltere.', 'coğrafya'),
 ('', 'Yanındaki lordlar ona yalvardı: Fransa\'ya git. Orada ailen var, gelirin var, orada bir kraliçe olarak karşılanırsın.', 'K20 (dostlarının ısrarı); Fransa\'daki dul geliri ve Guise ailesi (standart)'),
 ('', 'Ama Mary, Elizabeth\'e çoktan bir haberci yollamıştı.', 'K20'),
 ('', 'Habercinin elinde bir elmas vardı: yıllar önce Elizabeth\'ten aldığı dostluk nişanı.', 'K20 (Camden 1688)'),
 ('', 'Elizabeth sevgi ve yardım vaat etmişti.', 'K20'),
 ('', 'Zweig bu anı hayatının dönüm noktası sayar. Mary\'nin kalbi, İngiltere dedi.', 'Z03; anlatım'),
 ('', '16 Mayıs 1568. Mary küçük bir balıkçı teknesine bindi ve Solway\'i geçti.', 'K21'),
 ('', 'Akşam İngiliz kıyısına, Workington\'a çıktı. Ertesi gün Elizabeth\'e kendi eliyle yazdı.', 'K21, K22'),
 ('softly', '"Sizden yalvarırım, beni bir an önce yanınıza çağırın. Acınacak hâldeyim; dünyada, kaçtığım hâlimle kendimden başka hiçbir şeyim yok."', 'K22 (Labanoff II, s. 76–77: "je suis en piteux estat... je n\'ay chose du monde que ma personne")'),
 ('', 'Ve mektubu şöyle imzaladı: "Sadık ve sevgi dolu iyi kız kardeşiniz, kuzeniniz ve kaçmış tutsak, Mary."', 'K22 ("eschappée prisonière, Marie R.")'),
 ('', 'Kaçmış tutsak. Bu imza, ömrünün geri kalanının başlığı olacaktı.', 'anlatım'),
 ('', 'Yirmi beş yaşındaydı. Zweig\'e göre gerçek hayatı o gün bitmişti.', 'Z03 (Zweig "henüz yirmi beşinde değil" der; Mary Aralık 1567\'de 25\'ine girmişti, bu yüzden yaş düzeltildi)'),
 ('', 'Gerisi on dokuz yıl sürecek bir bekleyişti.', 'K26'),
])
b('On dokuz yıl', 'Elizabeth onu neden ne bıraktı ne öldürdü?', [
 ('', 'Mary bir misafir olarak geldiğini sanıyordu. Bir ay sonra Carlisle\'dan yazdığı mektupta bir cümle var: "Bir tutsaktan pek farkım yok."', 'K23'),
 ('', 'İlk günden Elizabeth\'le yüz yüze görüşmek istedi. Elizabeth reddetti: önce Darnley cinayetinden aklanmalıydı.', 'standart (1568); K09'),
 ('', 'İki kraliçenin hiç gerçekleşmeyen buluşması, bu sefer bir kalenin kapısında kaldı.', 'anlatım'),
 ('', 'Elizabeth\'in önünde üç kapı vardı. Üçü de kapalıydı.', 'anlatım'),
 ('', 'Onu serbest bırakırsa, Mary bir ordu toplayıp geri dönebilirdi.', 'standart'),
 ('', 'Fransa\'ya gönderirse, Katolik krallar onu İngiltere tahtına oturtmak için kullanabilirdi.', 'standart'),
 ('', 'Öldürürse, kutsanmış bir kraliçenin kanını dökmüş olurdu; bu da kendi tacını tartışmaya açardı.', 'standart'),
 ('', 'Bu yüzden Elizabeth en iyi bildiği şeyi yaptı: bekledi.', 'Z02 (Zweig: sabır ve gerçekçilik)'),
 ('', 'Mary\'nin Darnley cinayetine karışıp karışmadığını tartışmak için York\'ta ve Westminster\'da bir soruşturma toplandı. Masaya o mektuplar kondu. Karar çıkmadı.', 'K24'),
 ('', 'Mary kaleden kaleye taşındı: Tutbury, Sheffield, Chartley.', 'standart'),
 ('', 'Uzun yılları iğne ve iplikle geçirdi.', 'standart (işlemeler)'),
 ('', '1569\'da onu ziyaret eden bir İngiliz, kraliçenin taht örtüsüne işlenmiş bir söz gördü ve anlamadı:', 'K25 (Nicholas White, Tutbury)'),
 ('thoughtful', '"En ma fin est mon commencement." Sonumda başlangıcım.', 'K25; L6 açılır (cevap M)'),
 ('', 'Bu söz annesinindi: ateşin içinde yeniden doğan bir anka kuşunun altında yazılıydı.', 'K25 (Palliser 1870: Mary of Guise\'in amblemi)'),
 ('', 'Yıllar boyunca Mary, adına kurulan planların merkezinde kaldı. Bir kısmından haberi vardı, bir kısmından yoktu.', 'standart (Ridolfi, Throckmorton)'),
 ('', 'Bir yaşında bıraktığı oğlu büyüdü, Protestan bir kral oldu. 1586\'da Elizabeth\'le ittifak imzaladı ve ondan yıllık para almayı kabul etti.', 'standart (Berwick Antlaşması, Temmuz 1586)'),
 ('', 'Mary artık kırk yaşını geçmişti. Romatizma yüzünden zor yürüyordu.', 'standart'),
 ('', 'Ve İngiltere\'de bir adam, onun bir hata yapmasını sabırla bekliyordu: Elizabeth\'in casus şefi Francis Walsingham.', 'standart'),
])
b('Bira fıçısındaki mektuplar', 'Mektuplarını kim okuyordu?', [
 ('', '1586\'da Mary, Chartley\'de tamamen yalnızdı. Bütün mektuplaşması yasaklanmıştı.', 'standart (1585)'),
 ('', 'Sonra bir gün gizli bir yol açıldı.', 'K27'),
 ('', 'Mektuplar, Burton\'dan bira getiren bir biracının fıçılarında saklanarak geliyor ve gidiyordu.', 'K27 (Pollen 1922)'),
 ('', 'Mary yıllar sonra ilk kez dışarıya yazabiliyordu.', 'K27'),
 ('', 'Ama bu yolu Walsingham açmıştı. Her mektup önce onun masasına gidiyor, şifresi çözülüyor, kopyalanıyor, sonra yoluna devam ediyordu.', 'K27'),
 ('', 'Temmuz 1586\'da genç bir Katolik soylu, Anthony Babington, ona bir plan yazdı: Elizabeth öldürülecek, Mary kurtarılacaktı.', 'standart; K28'),
 ('', 'Mary cevap verdi.', 'K28'),
 ('', 'Mektubunun çözülmüş kopyasında şu cümle var: "O zaman altı beyefendiyi işe koşmanın vakti gelecek."', 'K28 (Pollen 1922)'),
 ('', 'Altı beyefendi, Elizabeth\'i öldürecek altı adamdı.', 'standart'),
 ('', 'Walsingham\'ın şifre çözücüsü bu mektubun üstüne küçük bir darağacı çizdi.', 'standart (Phelippes)'),
 ('', 'Mary yargılanmak üzere Fotheringhay şatosuna götürüldü.', 'standart'),
 ('', 'Orada İngiliz lordlarına şöyle dedi: "Vicdanınıza bakın ve unutmayın: bütün dünya sahnesi İngiltere krallığından daha geniştir."', 'K29 (Camden 1688)'),
 ('', 'Mahkeme onu ölüme mahkûm etti. Geriye tek bir imza kalıyordu.', 'standart'),
])
b('Elizabeth, Elizabeth\'e karşı', 'O imzayı kim attı?', [
 ('', 'Zweig bu bölüme "Elizabeth, Elizabeth\'e karşı" der.', 'Z01 (24. bölüm)'),
 ('', 'Çünkü artık savaş iki kraliçe arasında değil, Elizabeth\'in kendi içindeydi.', 'Zweig 24. bölüm (yorum)'),
 ('', 'Parlamento idam istedi. Elizabeth şöyle cevap verdi:', 'K30'),
 ('thoughtful', '"Dileğinizi kabul etmeyeceğim desem, belki düşündüğümden fazlasını söylemiş olurum. Kabul edeceğim desem, bilmeniz gerekenden fazlasını. Size cevapsız bir cevap vermek zorundayım."', 'K30 (D\'Ewes; Tanner 1922, s. 564)'),
 ('', 'Haftalar geçti. 1 Şubat 1587\'de sonunda fermanı imzaladı.', 'K32'),
 ('', 'Aynı gün iki sekreteri, Mary\'nin gardiyanı Amias Paulet\'e gizli bir mektup yazdı.', 'K31'),
 ('', 'Mektupta kraliçenin ona kırgın olduğu yazıyordu: Paulet, kendiliğinden, "o kraliçenin hayatını kısaltmanın bir yolunu" bulmamıştı.', 'K31 (Poulet Letter-Books, s. 359)'),
 ('', 'Yani fermanla değil, sessizce.', 'K31 (yorum)'),
 ('', 'Paulet ertesi gün cevap verdi: "Tanrı korusun; vicdanımı böyle batıramam, torunlarıma böyle bir leke bırakamam. Kanun ve ferman olmadan kan dökmem."', 'K31 (s. 362)'),
 ('', 'Ferman Fotheringhay\'e gönderildi. Elizabeth\'in haberi olmadan mı? Kendisi sonradan öyle söyleyecekti.', 'K32, K36'),
 ('', 'Mary 7 Şubat akşamı, yemekten sonra, ertesi sabah sekizde öleceğini öğrendi.', 'K33'),
])
b('Kırmızı', 'Neden kırmızı giydi?', [
 ('', 'O gece uyumadı. Vasiyetini yazdı, hizmetkârlarına veda etti.', 'K33 (standart)'),
 ('', 'Gece saat ikide son mektubunu yazdı: Fransa kralına, ilk kocasının kardeşine.', 'K33'),
 ('', 'Mektubun ilk cümlesi bütün hikâyeyi anlatıyor:', 'K33'),
 ('softly', '"Tanrı\'nın izniyle, sanırım günahlarım yüzünden, bu kraliçenin, kuzenimin kollarına atıldım. Orada çok sıkıntı çektim ve yirmi yıla yakın geçirdim."', 'K33 (Labanoff VI, s. 491)'),
 ('', 'Ölmeden önceki gece, kendi hayatını Solway\'den başlatıyordu.', 'anlatım; L2 kapanır'),
 ('', 'Sabah büyük salona siyahlar içinde girdi. Elinde bir haç, belinde bir tespih vardı.', 'K34'),
 ('', 'Hizmetçileri siyah elbisesini çıkardı. Altından kızıl kadife bir iç etek çıktı.', 'K34 (L1 kapanır)'),
 ('', 'Hizmetçi kadınlar ağlamaya başladı. Mary onlara Fransızca, "Ağlamayın, sizin için dua ettim" dedi.', 'K34'),
 ('', 'Diz çöktü ve Latince dua etti: "Ruhumu senin ellerine bırakıyorum."', 'K34 (In manus tuas)'),
 ('', 'Ve salon sustu.', 'görsel: idam gösterilmez'),
 ('', 'Neden kırmızı? Zweig\'e göre Mary bunu, kan elbisesinin üstünde çok sert görünmesin diye seçmişti.', 'Z05 (25. bölüm)'),
 ('', 'Bugün birçok tarihçiye göre ise başka bir anlamı vardı: kırmızı, Katolik kilisesinde şehitlerin rengidir.', 'K40'),
 ('', 'Mary bir gece önce aynı mektupta şöyle yazmıştı: onu inancı ve tacı yüzünden öldürüyorlardı. Kırmızı, bir suçlunun değil, bir şehidin rengiydi.', 'K33 (Labanoff VI, s. 492–493: "La religion catholique et le maintien du droit... sont les deux points de ma condemnation"), K40'),
 ('', 'Başındaki tül düştüğünde saçlarının yetmiş yaşında birininki gibi ağarmış ve kısacık olduğu görüldü. Kırk dört yaşındaydı.', 'K34'),
 ('', 'Ve eteğinin altından, oraya saklanmış küçük köpeği çıktı. Yanından ayrılmak istemedi.', 'K34'),
 ('', 'Dekan haykırdı: "Kraliçe\'nin bütün düşmanları böyle yok olsun."', 'K34'),
 ('', 'Haber Londra\'ya ulaştığında Elizabeth\'in yüzü değişti, sesi kesildi. Yas giydi, ağladı, meclisini azarladı.', 'K35'),
 ('', 'Fermanı gönderen sekreteri Davison\'ı yargılattı. Mary\'nin oğluna da şöyle yazdı: "Niyetimin tam tersine başa gelen o sefil kaza."', 'K32, K36'),
 ('', 'Kaza.', 'anlatım'),
])
b('Sonumda başlangıcım', 'Peki kim kazandı?', [
 ('', 'Elizabeth on altı yıl daha yaşadı. Hiç evlenmedi, hiç çocuğu olmadı.', 'K37, K39'),
 ('', 'Kırk dört yıl hüküm sürdü ve İngiltere\'yi en güçlü dönemlerinden birine taşıdı. Akıl, tahtı korudu.', 'K39'),
 ('', '24 Mart 1603\'te öldü.', 'K37'),
 ('', 'Peki İngiltere tahtına kim oturdu? Mary Stuart\'ın oğlu James.', 'K37; L3 kapanır'),
 ('', 'On altı yaşında İngiltere\'nin armasını taşıyan kız o tahta hiç oturamadı. Ama oğlu oturdu.', 'K04, K37'),
 ('', 'Bugün İngiltere\'nin kraliyet ailesi Mary Stuart\'ın soyundan gelir. Elizabeth\'in soyu kendisiyle bitti.', 'standart (I. James → Bohemya Kraliçesi Elizabeth → Hannover Sophia)'),
 ('thoughtful', 'Sonumda başlangıcım. Taht örtüsüne işlenmiş o bilmece, böyle çözüldü.', 'K25, Z06; L6 kapanır'),
 ('', 'Oğlu James, annesini Westminster Abbey\'e taşıttı.', 'K38'),
 ('', 'Bugün iki kraliçe aynı şapelin iki yanında, birkaç metre arayla yatıyor. Hayattayken bir kez bile yüz yüze gelmediler.', 'K38, K09'),
 ('', 'Zweig\'e göre siyasette akıl kazandı. Ama tarihte, kalp.', 'Z02, Z06'),
 ('', 'Zaman Kuryesi, geçmişten bugüne böyle sorular taşıyor. Bu yolculuğu sevdiysen abone ol; bir sonraki soruyu birlikte taşıyalım.', 'abone çağrısı (doruk anında)'),
 ('curious', 'Şimdi soru senin: sen kalbinle mi yaşıyorsun, aklınla mı? Ve sence hangisi kazandı? Cevabını yorumlarda bekliyorum.', 'L4 kapanır (izleyiciye)'),
 ('', 'Aynı yüzyılda, tahtını kendi isteğiyle bırakan bir imparator daha vardı. Onun hikâyesi ekranda.', 'bitiş ekranı: Şarlken (son 20 sn içinde)'),
])

# kimlikler: bölüm harfi + sıra
HARF = {}
for s in S:
    if s['bolum'] not in HARF: HARF[s['bolum']] = chr(ord('A') + len(HARF))
cnt = {}
for s in S:
    h = HARF[s['bolum']]; cnt[h] = cnt.get(h, 0) + 1; s['id'] = f'{h}{cnt[h]:02d}'
out = dict(voice='Emrullah (ElevenLabs; voice_id creative_list_voices ile bulunur)', revizyon='rev0 (18 Kasım 2026): başkan taslağı; kurul yok (kullanıcının kararı); Fable danışman denetimi bekleniyor',
           segments=S, **{'not': 'tts: okunuş biçimi (yabancı adlar, rakamlar sözcükle); alt: altyazı. Kaynak kimlikleri kaynak/KAYNAKLAR.md'})
json.dump(out, open(os.path.join(R, 'senaryo.json'), 'w'), ensure_ascii=False, indent=1)
# okuma dosyası + sayımlar
W = sum(len(re.findall(r'\w+', s['alt'])) for s in S); C = sum(len(re.sub(r'^\[[a-z ]+\] ', '', s['tts'])) for s in S)
L = [f'# Mary Stuart: senaryo okuma metni (rev0)', '', f'{len(S)} cümle · {W} kelime · tts {C} karakter · tahmini süre {W / 96:.1f}–{W / 90:.1f} dk (Ran 96 kelime/dk)', '']
cur = None
for s in S:
    if s['bolum'] != cur:
        cur = s['bolum']; L += ['', f'## {HARF[cur]}. {cur}' + (f'  ·  *{s["soru"]}*' if s['soru'] else ''), '']
    L.append(f'- **{s["id"]}** {s["alt"]}  <sub>{s["kaynak"]}</sub>')
open(os.path.join(R, 'senaryo_okuma.md'), 'w').write('\n'.join(L) + '\n')
print(len(S), 'cümle', W, 'kelime', C, 'tts karakter', f'~{W / 96:.1f} dk')

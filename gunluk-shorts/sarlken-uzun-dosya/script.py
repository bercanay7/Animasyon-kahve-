"""Şarlken (V. Karl) — Uzun Dosya #1: anlatım metni (tek kaynak).

Her cümle:  (gösterim_metni, [söylenen_metin])   — söylenen yoksa gösterimden türetilir.
  * Gösterim: altyazı/SRT ve ekran için (rakam, doğru yazım).
  * Söylenen: ElevenLabs'e giden metin — rakamlar sözcüğe çevrilir, yabancı adlar Türkçe okunuşla yazılır (PRON).
  * {gösterim|söylenen} biçimi satır içi değişkendir.
Bölüm = paragraf listesi; paragraf = cümle listesi. Kimlikler: c<bölüm>s<sıra>.
Olgu dayanakları: arastirma/*.md ve kaynaklar.md (CONFIRMED / NİTELİKLİ / ANEKDOT=rivayet olarak anlatılır).
"""
import re

# ---------------------------------------------------------------- sayı → Türkçe sözcük
_ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def tr_num(n: int) -> str:
    if n == 0:
        return "sıfır"
    parts = []
    if n >= 1_000_000:
        parts.append(tr_num(n // 1_000_000) + " milyon")
        n %= 1_000_000
    if n >= 1000:
        k = n // 1000
        parts.append(("" if k == 1 else tr_num(k) + " ") + "bin")
        n %= 1000
    if n >= 100:
        h = n // 100
        parts.append(("" if h == 1 else _ONES[h] + " ") + "yüz")
        n %= 100
    if n >= 10:
        parts.append(_TENS[n // 10])
        n %= 10
    if n:
        parts.append(_ONES[n])
    return " ".join(p.strip() for p in parts if p.strip())


# ---------------------------------------------------------------- okunuş sözlüğü (yalnız söylenen metne uygulanır)
PRON = [
    (r"\bTordesillas\b", "Tordesiyas"), (r"\bJuana\b", "Huana"), (r"\bMechelen\b", "Mehelen"),
    (r"\bWorms\b", "Vorms"), (r"\bWartburg\b", "Vartburg"), (r"\bSpeyer\b", "Şpayer"),
    (r"\bAugsburg\b", "Aogsburg"), (r"\bAachen\b", "Aahen"), (r"\bMühlberg\b", "Mülberg"),
    (r"\bInnsbruck\b", "İnsbruk"), (r"\bFrançois\b", "Fransuva"), (r"\bPavia\b", "Pavya"),
    (r"\bCambrai\b", "Kambre"), (r"\bCastel Sant'Angelo\b", "Kastel Sant Anjelo"), (r"\becü\b", "ekü"),
    (r"\bLajos\b", "Lajoş"), (r"\bCortés\b", "Kortes"), (r"\bHernán\b", "Hernan"),
    (r"\bTenochtitlan\b", "Tenoçtitlan"), (r"\bCajamarca\b", "Kahamarka"), (r"\bAtahualpa\b", "Atawalpa"),
    (r"\bPizarro\b", "Pisarro"), (r"\bValladolid\b", "Valyadolid"), (r"\bSepúlveda\b", "Sepulveda"),
    (r"\bLas Casas\b", "Las Kasas"), (r"\bPotosí\b", "Potosi"), (r"\bMagellan\b", "Macellan"),
    (r"\bElcano\b", "Elkano"), (r"\bWelser\b", "Velzer"), (r"\bCatherine\b", "Katerina"),
    (r"\bHenry\b", "Henri"), (r"\bJörg\b", "Yörg"), (r"\bLuther\b", "Luter"), (r"\bLutherciliği\b", "Luterciliği"),
    (r"\bLutherciliğe\b", "Luterciliğe"), (r"\bOrange\b", "Oranj"), (r"\bWillem\b", "Vilhelm"),
    (r"\bJakob\b", "Yakob"), (r"\bVillalar\b", "Vilyalar"), (r"\bPadilla\b", "Padilya"),
    (r"\bPacheco\b", "Pacheko"), (r"\bMaría\b", "Maria"), (r"\bGermanía\b", "Hermanya"),
    (r"\bMelanchthon\b", "Melanşton"), (r"\bMoritz\b", "Moritz"), (r"\bJohn Frederick\b", "Con Frederik"),
    (r"\bDürer\b", "Dürer"), (r"\bMary\b", "Meri"), (r"\bİsabel\b", "İsabel"),
    (r"\bPlus ultra\b", "Plus ultra"), (r"\bPrimus circumdedisti me\b", "Primus sirkumdedisti me"),
]


def _num_sub(m):
    raw, suf = m.group(1), m.group(2) or ""
    n = int(raw.replace(".", ""))
    return tr_num(n) + suf.lstrip("'’")


def to_speech(s: str) -> str:
    s = re.sub(r"\{[^|{}]*\|([^{}]*)\}", r"\1", s)                  # {göster|söyle}
    s = re.sub(r"(\d{1,3}(?:\.\d{3})+|\d+)(['’][A-Za-zçğıöşüÇĞİÖŞÜ]+)?", _num_sub, s)
    for pat, rep in PRON:
        s = re.sub(pat, rep, s)
    s = s.replace("’", "'")
    def _up(ch):
        return {"i": "İ", "ı": "I"}.get(ch, ch.upper())
    m = re.search(r"[A-Za-zçğıöşüÇĞİÖŞÜ]", s)                          # cümle başı büyük harf (sayıdan türeyen sözcükler küçük kalır)
    if m:
        i = m.start()
        s = s[:i] + _up(s[i]) + s[i + 1:]
    s = re.sub(r"([.!?]\s+)([a-zçğıöşü])", lambda mm: mm.group(1) + _up(mm.group(2)), s)
    return s


def to_display(s: str) -> str:
    return re.sub(r"\{([^|{}]*)\|[^{}]*\}", r"\1", s)


# ---------------------------------------------------------------- METİN
# Not: "Rivayet" = ANEKDOT sınıfı; bilerek böyle anlatılır. Hedge sözcükleri (yaklaşık, büyük olasılıkla, hâlâ tartışılır)
# kaynaklar.md'deki NİTELİKLİ satırlara karşılık gelir.
CHAPTERS = [
    dict(id="c0", n="", title="Brüksel, 25 Ekim 1555", years="1555", mood="solemn", front="",
         paras=[[
             ("{25 Ekim 1555.|Yirmi beş Ekim, bin beş yüz elli beş.}", ),
             ("Brüksel'de büyük salon tıklım tıklım dolu.", ),
             ("Ortada, elli beş yaşında bir adam ayakta zor duruyor.", ),
             ("Kolunu genç bir prensin omzuna dayamış.", ),
             ("Bu adam, kırk yıldır Avrupa'nın büyük bölümünü yönetiyor.", ),
             ("Yeni Dünya'da fethedilen topraklar da onun adına.", ),
             ("Ve bugün, hepsini bırakmaya başlıyor.", ),
             ("Kimse onu tahttan indirmedi.", ),
             ("Peki neden?", ),
             ("Cevap, beş cephede saklı: bir bankacı, bir keşiş, bir kral, bir sultan ve bir miras.", ),
             ("İlk kanıt, taç daha takılmadan ortaya çıkıyor: o taç, büyük ölçüde borçla alındı.", ),
             ("Bu, Şarlken'in hikâyesi.", ),
         ]]),

    dict(id="c1", n="I", title="Dört Tahtın Çocuğu", years="1500–1518", mood="curious", front="MİRAS",
         paras=[[
             ("Şarlken, 24 Şubat 1500'de, Flandre'daki Gent şehrinde doğdu.", ),
             ("Annesi Kastilya Kraliçesi Juana'ydı; babası, Burgonyalı Yakışıklı Filip.", ),
             ("Dört büyükanne ve büyükbabasının her biri ona bir ülke bırakacaktı: Burgonya'yı, Avusturya'yı, Aragon'u, Kastilya'yı.", ),
             ("O doğduğunda İspanya tahtı çok uzaktı. Beş ay sonra, henüz iki yaşına basmamış kuzeni öldü ve yol açıldı.", ),
             ("Habsburglar tahtları böyle topladı: evlilikle ve ölümle.", ),
         ], [
             ("Altı yaşındayken, babası Burgos'ta aniden öldü.", ),
             ("Annesi Juana, 1509'dan sonra Tordesillas'ta bir sarayda tutuldu.", ),
             ("Orada kırk altı yıl yaşadı. Oğlu bu kapatmayı hiç kaldırmadı.", ),
             ("Tarihçiler bunun deliliğe mi, siyasete mi bağlı olduğunu hâlâ tartışıyor.", ),
         ], [
             ("Küçük Şarlken, halası Margareta'nın sarayında, Mechelen'de büyüdü. Ana dili Fransızcaydı.", ),
             ("Rivayete göre, Tanrı'yla İspanyolca, kadınlarla İtalyanca, erkeklerle Fransızca, atıyla Almanca konuşurdu.", ),
             ("Oysa bu söz, bilinen en eski hâliyle, ölümünden yaklaşık kırk üç yıl sonra yazıya geçti. Ona ait olduğunu gösteren bir belge bilinmiyor.", ),
         ], [
             ("1516'da dedesi, Aragonlu Fernando öldü. Şarlken, tutsak annesiyle birlikte, Kastilya ve Aragon'un kralı oldu.", ),
             ("Eylül 1517'de, İspanya'ya giderken bir fırtına gemilerini yoldan çıkardı. Hedefleri Santander'di; küçük bir balıkçı köyü olan Tazones'a çıktılar.", ),
             ("On yedi yaşındaki kral, yeni halkının dilini henüz iyi konuşamıyordu.", ),
             ("Valladolid Kortesi, 1518'de talebini açıkça söyledi: Kastilyacayı öğren, yabancı danışmanlarını gönder.", ),
         ]]),

    dict(id="c2", n="II", title="Taç Satılık", years="1519–1520", mood="tense", front="BANKACI",
         paras=[[
             ("Ocak 1519'da dedesi Maksimilian öldü.", ),
             ("İmparatorluğun tacı kalıtsal değildi. Yedi seçmen karar verirdi.", ),
             ("Başlıca rakip, Fransa Kralı {I. François|Birinci Fransuva}'ydı.", ),
             ("İngiltere Kralı {VIII. Henry|Sekizinci Henri} de adını ortaya attı; ama bu daha çok bir gösteriydi.", ),
             ("Oylar, açıkça pazarlık konusuydu.", ),
         ], [
             ("Şarlken'in seçim masrafı, yaklaşık 850.000 florini buldu.", ),
             ("Bunun üçte ikisine yakını, yaklaşık 543.000 florin, Augsburglu bankacı Jakob Fugger'den geldi.", ),
             ("28 Haziran 1519'da, Frankfurt'ta, yedi seçmenin yedisi de ona oy verdi.", ),
             ("Bazı tarihçilere göre seçmenler parayı aldı, ama kararı yine de Almanya için en iyi saydıkları yönde verdi.", ),
             ("Rüşvetin ne kadar belirleyici olduğu tartışmalı. Ama borç gerçekti: imparator, tacını takmadan önce borçluydu.", ),
         ], [
             ("Seçilince seçmenlere yazılı söz verdi: prenslerin ayrıcalıklarına saygı gösterecek, imparatorluğu birlikte yönetecek bir konsey kuracaktı.", ),
             ("23 Ekim 1520'de, Şarlman'ın şehri Aachen'de tacını taktı.", ),
             ("Devizi de hazırdı: Plus ultra. Daha öteye.", ),
             ("Rivayete göre, Herkül Sütunları'nda “daha ötesi yok” yazıyordu. Onun devizi, bu uyarıdan tek bir sözcüğü silerek tersini söyledi.", ),
         ]]),

    dict(id="c3", n="III", title="Şehirlerin İsyanı", years="1520–1522", mood="tense", front="",
         paras=[[
             ("Tacı almak için İspanya'dan ayrılması gerekti.", ),
             ("Bu ayrılış, yabancı danışmanlara ve vergilere öfkeli Kastilya şehirlerinde tepkiyle karşılandı.", ),
             ("1520'de Komünero İsyanı patladı.", ),
             ("23 Nisan 1521'de, Villalar'da, kraliyet ordusu isyancıları dağıttı.", ),
             ("Ertesi gün üç önder idam edildi: Padilla, Bravo ve Maldonado.", ),
             ("Toledo'da Padilla'nın dul eşi María Pacheco, aylarca direndi.", ),
             ("Aynı yıllarda Valensiya'da esnaf loncaları da ayaklanmıştı: Germanía İsyanı.", ),
             ("Bugün Kastilya-León bölgesi, Villalar'ın yıldönümünü kendi bayramı olarak kutluyor.", ),
             ("İlk ders buydu: aynı anda bütün tahtların başında duramazsın.", ),
         ]]),

    dict(id="c4", n="IV", title="Worms'ta Bir Keşiş", years="1517–1522", mood="solemn", front="KEŞİŞ",
         paras=[[
             ("Nisan 1521. Worms.", ),
             ("Yirmi bir yaşındaki imparatorun karşısında, bir keşiş duruyor: Martin Luther.", ),
             ("Dört yıl önce, günah affı satışına karşı doksan beş maddelik bir metin yazmıştı. Matbaa, bu metni kısa sürede Almanya'ya yaydı.", ),
             ("İmparator ona güvenli geçiş sözü vermişti: yirmi bir gün.", ),
         ], [
             ("Önüne kitaplarını koydular. Sordular: bunlar senin mi? Hepsinden vazgeçiyor musun?", ),
             ("Luther bir gün süre istedi. Ertesi gün önce Almanca, sonra Latince cevap verdi: vazgeçmiyordu.", ),
             ("Meşhur cümle, “Ben buradayım, başka türlü yapamam”, büyük ihtimalle orada söylenmedi. Resmî tutanakta yok; sonradan eklenmiş.", ),
         ], [
             ("Ertesi sabah, imparatorun yazılı bildirisi okundu.", ),
             ("Atalarını sayıyordu: Alman imparatorları, İspanya kralları, Burgonya dükleri. Hepsi Roma Kilisesi'ne bağlıydı.", ),
             ("Ona göre, bin yıllık Hıristiyanlığa karşı çıkan tek bir keşiş, yanılıyor olmalıydı.", ),
             ("Bu dava uğruna krallıklarını, dostlarını, bedenini, kanını, canını ve ruhunu ortaya koyacağını yazdı.", ),
         ], [
             ("Worms Fermanı, Luther şehirden ayrıldıktan sonra imzalandı; ama geriye dönük tarihlendi.", ),
             ("Luther artık kanun dışıydı. Yazılarını okumak, basmak, satmak yasaktı.", ),
             ("Ama dönüş yolunda “kaçırıldı”. Kaçıranlar, onu korumak isteyen Saksonya Seçmeni'nin adamlarıydı.", ),
             ("Wartburg Kalesi'nde sakal bırakıp “Şövalye Jörg” adıyla saklandı. Orada Yeni Ahit'i Almancaya çevirdi.", ),
             ("İmparator fermanı yazdırdı; ama fikri durduramadı.", ),
         ]]),

    dict(id="c5", n="V", title="İmparator Hep Başka Yerde", years="1521–1555", mood="grave", front="KEŞİŞ",
         paras=[[
             ("Worms'tan sonra imparator Almanya'dan ayrıldı. Dokuz yıl dönemedi.", ),
             ("İspanya karışıktı, Fransa saldırıyordu, Akdeniz'de Osmanlı vardı.", ),
             ("O yokken Luther'in fikirleri yayıldı. 1524'te başlayan Köylü Savaşı'nı Luther istememişti; yetmiş ile yüz bin kişi öldü.", ),
             ("1529'da Speyer'de Katolik çoğunluk, Worms Fermanı'nı yeniden yürürlüğe koydu.", ),
             ("Birkaç prens ve on dört şehir buna itiraz etti, yani protesto etti. “Protestan” sözcüğü oradan geliyor.", ),
         ], [
             ("1530'da Augsburg'da Protestanlar inançlarını yazılı olarak imparatora sundu. Metnin ana yazarı, Luther değil, Melanchthon'du.", ),
             ("Şarlken dinledi ama kabul etmedi. Prensler Şmalkalden Birliği'ni kurdu.", ),
             ("İmparator ancak Fransa ve Osmanlı cephesi yatışınca, 1546'da onlara savaş açabildi.", ),
             ("24 Nisan 1547'de, Mühlberg'de, sisli bir sabah Elbe nehrini geçti ve Protestan ordusunu dağıttı. Saksonya Seçmeni esir düştü.", ),
             ("Tiziano, bir yıl sonra imparatoru o zaferin simgesi olarak resmetti: zırhlı, atının üstünde, tek başına.", ),
         ], [
             ("Zafer kısa sürdü. 1552'de eski müttefiki Saksonyalı Moritz, ona karşı ayaklandı.", ),
             ("Hasta imparator, bir gece Innsbruck'tan kaçmak zorunda kaldı.", ),
             ("Sonunda, Eylül 1555'te, Augsburg Barışı imzalandı: Lutherciliğe resmen yer açıldı.", ),
             ("Barışı o yapmadı; kardeşi Ferdinand yürüttü.", ),
             ("Tam bir ay sonra, o büyük salonda duruyordu.", ),
         ]]),

    dict(id="c6", n="VI", title="Kral, Esir, Düello", years="1521–1544", mood="tense", front="KRAL",
         paras=[[
             ("Şarlken'in en kalıcı düşmanlarından biri, Fransa Kralı {I. François|Birinci Fransuva}'ydı.", ),
             ("Fransa, Habsburg topraklarıyla kuşatılmıştı: güneyde İspanya, kuzeyde ve doğuda Burgonya ile Hollanda, İtalya'da Napoli.", ),
             ("24 Şubat 1525'te, Pavia'da, Fransız ordusu bozguna uğradı; François esir düştü.", ),
             ("Annesine yazdığı mektupta, aktarıldığına göre, “bana şeref ve canım kaldı” diyordu. Meşhur “şeref dışında her şey kayıp” sözü ise sonradan yaygınlaştı.", ),
             ("Madrid'de esirken, İtalya ve Flandre'daki iddialarından vazgeçen bir antlaşma imzaladı. İki oğlu rehin kaldı.", ),
             ("Özgürlüğüne kavuşur kavuşmaz antlaşmayı reddetti: esirin sözü geçersizdi.", ),
         ], [
             ("6 Mayıs 1527'de, maaşını alamayan imparatorluk askerleri Roma'ya girdi.", ),
             ("Papa, Castel Sant'Angelo'ya sığındı. 189 İsviçreli muhafızdan 147'si öldü.", ),
             ("İmparator emir vermemişti. Ama papa, aylarca onun askerlerinin elinde kaldı.", ),
             ("Sıkça anlatıldığına göre, bunun uzak bir sonucu İngiltere'de görüldü: papa, imparatorun teyzesi Aragonlu {Catherine'in|Katerina'nın} boşanmasını onaylayamadı. Henry, Roma'dan koptu.", ),
         ], [
             ("1528'de iki hükümdar birbirine “yalancı” dedi ve düelloya davet etti. Düello hiç yapılmadı.", ),
             ("1529'da Cambrai'de barışı iki kadın yaptı: François'nın annesi ve Şarlken'in halası. Buna “Hanımlar Barışı” dediler.", ),
             ("François, oğullarını geri almak için iki milyon altın ecü ödedi.", ),
             ("Barış kalıcı olmadı. Savaş, kesintilerle Şarlken'in ömrünün sonuna dek sürdü.", ),
         ]]),

    dict(id="c7", n="VII", title="Sultan: Hiç Karşılaşmadılar", years="1526–1547", mood="epic", front="SULTAN",
         paras=[[
             ("Doğuda başka bir imparator vardı: Kanuni Sultan Süleyman.", ),
             ("İkisi aynı yıllarda hüküm sürdü. Bildiğimiz kadarıyla, hiç yüz yüze gelmediler.", ),
             ("29 Ağustos 1526'da, Mohaç'ta, Macar ordusu yenildi. Kral {II. Lajos|İkinci Lajoş}, kaçarken bir derede boğuldu.", ),
             ("Çocuğu yoktu. Macaristan tahtı için Şarlken'in kardeşi Ferdinand öne çıktı; Macar soylular ikiye bölündü.", ),
             ("Rakip aday Zapolya, Osmanlı vasalı oldu.", ),
         ], [
             ("1529'da Süleyman, Viyana önüne geldi. Kuşatma 27 Eylül'de başladı.", ),
             ("Osmanlı ordusu, modern tahminlere göre, yetmiş beş ile yüz bin arasındaydı.", ),
             ("Yağmur, çamur ve erken kar, Ekim ortasında geri çekilmeye yol açtı.", ),
             ("Şarlken o hafta İtalya'daydı; papadan imparatorluk tacını almaya gidiyordu.", ),
         ], [
             ("1532'de Süleyman, bu kez doğrudan imparatora yürüdü. Osmanlı sefer günlüğü hedefi açıkça yazar: “İspanya kralı”.", ),
             ("Yolda küçük bir kale, Güns, yedi yüz ile sekiz yüz arası bir garnizonla orduyu yirmi beş gün oyaladı.", ),
             ("İmparatorluk ordusu Viyana yakınında bekledi. İki ordu hiç karşılaşmadı.", ),
             ("Osmanlı belgeleri ona genellikle “imparator” demedi. “İspanya kralı” derdi. Çünkü imparator, yalnızca sultandı.", ),
         ], [
             ("1547'de beş yıllık bir ateşkes imzalandı. Ferdinand, her yıl otuz bin altın ödeyecekti.", ),
             ("Habsburg, Viyana'yı tuttu; Macaristan'ın büyük bölümünü kaybetti. Yükün çoğunu Şarlken değil, kardeşi taşıdı.", ),
         ]]),

    dict(id="c8", n="VIII", title="Akdeniz'de Barbaros", years="1534–1541", mood="epic", front="SULTAN",
         paras=[[
             ("Akdeniz'de karşısında, sultanın amirali vardı: Barbaros Hayreddin Paşa.", ),
             ("1534'te Barbaros kaptan-ı derya oldu ve Tunus'u aldı.", ),
             ("Ertesi yıl Şarlken, Andrea Doria'nın filosuyla birlikte, bizzat Tunus'a çıktı.", ),
             ("Temmuz 1535'te Halkulvadi Kalesi düştü, Tunus alındı. Yaklaşık yirmi bin esir serbest kaldı.", ),
             ("Habsburg çevresinde bu büyük bir zafer olarak kutlandı.", ),
         ], [
             ("Ama deniz uzundu, ve Barbaros hâlâ filosuyla ortadaydı.", ),
             ("28 Eylül 1538'de, Preveze'de, papanın, Venedik'in ve imparatorun birleşik filosu Barbaros'la karşılaştı ve geri çekildi.", ),
             ("Sonraki yıllarda Akdeniz'in doğusunda Osmanlı donanması üstün kaldı.", ),
             ("1541'de Şarlken, Cezayir'e çıktı: beş yüz kadar yelkenli, yaklaşık yirmi dört bin asker.", ),
             ("Kıyıya çıkar çıkmaz bir fırtına koptu. Yağmur barutu çürüttü, yaklaşık yüz elli gemi battı.", ),
             ("Meksika'nın fatihi Hernán Cortés de oradaydı; savaş konseyine çağrılmadığı anlatılır.", ),
         ]]),

    dict(id="c9", n="IX", title="Yeni Dünya: Altın, Gümüş ve Vicdan", years="1519–1552", mood="wonder", front="",
         paras=[[
             ("Şarlken Yeni Dünya'yı hiç görmedi. Ama orası onun adına fethedildi.", ),
             ("1519'da Hernán Cortés, Küba valisinin izni olmadan yola çıktı. İki yıl sonra, 13 Ağustos 1521'de, Tenochtitlan düştü.", ),
             ("Cortés imparatora uzun mektuplar yazdı: fethi anlatan, ama aslında kendini savunan mektuplar.", ),
             ("Ressam Dürer, Brüksel'de sergilenen Aztek eserlerini görüp değerlerini yaklaşık yüz bin florin tahmin etti.", ),
         ], [
             ("1532'de, Cajamarca'da, Francisco Pizarro İnka hükümdarı Atahualpa'yı esir aldı.", ),
             ("Fidye olarak bir oda dolusu altın verildi: 1.326.539 peso.", ),
             ("Atahualpa yine de idam edildi.", ),
             ("Kraliyetin payı, ganimetin beşte biriydi.", ),
         ], [
             ("1542'de Yeni Yasalar çıktı: yerlileri köle yapmak yasaktı. Yerleşimciler o kadar öfkelendi ki, yasayı uygulamaya giden Peru valisi öldürüldü.", ),
             ("1550'de, Valladolid'de, imparator fetihleri geçici olarak durdurdu ve iki adamı karşı karşıya getirdi: Sepúlveda ve Las Casas.", ),
             ("Biri, yerlilerin köleliğe layık olduğunu savundu; öbürü, fethin bir suç olduğunu. Resmî bir kazanan çıkmadı.", ),
         ], [
             ("Bu arada ilk dünya turu da onun desteğiyle, onun bayrağı altında tamamlandı.", ),
             ("Magellan yolda öldü. Eve dönen tek gemiyi Elcano getirdi; on sekiz Avrupalı sağ kaldı.", ),
             ("Şarlken ona bir arma verdi: bir küre ve şu yazı: {Primus circumdedisti me|Primus circumdedisti me}. Beni ilk dolaşan sensin.", ),
         ]]),

    dict(id="c10", n="X", title="Faturayı Kim Ödedi?", years="1519–1557", mood="tense", front="BANKACI",
         paras=[[
             ("Peki bütün bu savaşları kim ödedi? Çoğumuz hemen Amerika'nın gümüşünü sayarız.", ),
             ("Kayıtlar başka bir şey söylüyor.", ),
             ("Şarlken'in otuz beş yıllık olağanüstü gelirlerinin çoğu vergiydi. Alçak Ülkeler on milyon dükatın, Kastilya dokuz milyon dükatın üzerinde katkı yaptı; Napoli beş milyon dükattan fazla.", ),
             ("Amerika'nın gümüş akışı asıl büyük patlamasını sonra yaşadı. Potosí madeni ancak 1545'te bulundu.", ),
         ], [
             ("Faturayı bankerler kesiyordu. 1523'te Jakob Fugger, imparatora parasını isteyen bir mektup yazdı.", ),
             ("Mektup, özetle, imparatora tacını kimin parasıyla aldığını hatırlatıyordu.", ),
             ("Welser'ler adlı başka bir banker ailesi ise Venezuela'da yönetim hakkı elde etti.", ),
             ("1556'da imparator tahtı bırakırken, devletin borcu uçurumdaydı. Nisan 1557'de oğlu Felipe, ödemeleri durdurdu.", ),
             ("Kısacası, imparatorluk altınla değil, borçla ayakta duruyordu.", ),
         ]]),

    dict(id="c11", n="XI", title="Adamın Kendisi", years="1526–1558", mood="intimate", front="",
         paras=[[
             ("Peki bu devasa makinenin başındaki adam nasıldı?", ),
             ("Habsburg çenesi yüzünden ağzını tam kapatamadığı ve çiğnemekte zorlandığı yazılır.", ),
             ("2019'daki bir çalışma, portrelerindeki yüz özelliklerini hanedanın akraba evlilikleriyle ilişkilendirdi. Ama çalışma küçüktü; kesin bir şey söylemiyor.", ),
         ], [
             ("26 yaşında Portekizli kuzeni İsabel'le evlendi.", ),
             ("1539'da İsabel, otuz beş yaşında öldü. Şarlken yaklaşık iki ay bir manastıra çekildi, bir daha da evlenmedi.", ),
             ("Ömrünün sonuna kadar siyah giydiği anlatılır.", ),
         ], [
             ("Gut atakları onu çoğu zaman hareketsiz bıraktı. Doktorlar perhiz önerdi; yemeği bol severdi diye yazılır.", ),
             ("Merkezi olmayan bir imparatorluğu, bizzat dolaşarak yönetti: Almanya, İtalya, İspanya, Hollanda, Fransa, hatta Tunus ve Cezayir.", ),
             ("İmparatorluğu bir masada değil, yollarda taşıdı.", ),
         ]]),

    dict(id="c12", n="XII", title="Bırakmak", years="1555–1558", mood="solemn", front="",
         paras=[[
             ("Brüksel, 25 Ekim 1555. Öğleden sonra, saat üç sularında.", ),
             ("Altı ay önce annesi Juana, kırk altı yıllık tutsaklığın ardından ölmüştü.", ),
             ("Salonda Genel Devletler toplanmış. İmparator, genç Orange Prensi Willem'in omzuna yaslanarak giriyor; arkasında oğlu Felipe ve kız kardeşi Mary var.", ),
             ("Konuşmasında, tam kırk yıl önce, on beş yaşında bu topraklara hükmetmeye başladığını söylüyor.", ),
         ], [
             ("Hollanda'yı oğluna devrediyor. İspanya, Ocak 1556'da gelecek. İmparatorluk unvanı ise ancak 1556 ile 1558 arasında kardeşi Ferdinand'a geçecek.", ),
             ("Tarihçilerin saydığı nedenler şunlar: gut ve yorgunluk, ve evrensel bir Hıristiyan imparatorluğunun gerçekleşmeyeceğinin anlaşılması.", ),
             ("Oğlu Felipe, İspanya'yı savaşta ve iflasa yakın devralacaktı.", ),
         ], [
             ("Şarlken, Eylül 1556'da İspanya'ya döndü. Şubat 1557'de, Yuste Manastırı'nın yanındaki küçük konuta yerleşti.", ),
             ("Bir çalışma, ölümünden kısa süre önce kendi adına okunan ayine katıldığını yazıyor. Tabutuna yatıp cenazesini prova ettiği ise yalnızca rivayet.", ),
             ("31 Ağustos 1558'de ateşi başladı. Büyük olasılıkla sıtmaydı. 21 Eylül'de öldü. Elli sekiz yaşındaydı.", ),
         ]]),

    dict(id="c13", n="XIII", title="Hesap", years="1558–", mood="solemn", front="MİRAS",
         paras=[[
             ("Beşinci cephe en sessiz olanıydı: miras.", ),
             ("Dört büyük taht, tek bir adama kalmıştı. Hepsi birbirine bir ülke gibi değil, bir akrabalık ağı gibi bağlıydı.", ),
             ("Şarlken'in bıraktıklarıyla Habsburg hanedanı iki kola ayrıldı: İspanya kolu oğlu Felipe'ye, Avusturya kolu kardeşi Ferdinand'a.", ),
             ("Evrensel Hıristiyan imparatorluk hayali gerçekleşmedi. Reform durmadı; Augsburg Barışı Lutherciliği tanıdı.", ),
         ], [
             ("Sonuçta Avrupa, tek imparatorluk yerine birbirini dengeleyen devletlerden oluşan bir yapıya doğru gitti.", ),
             ("Ama onun döneminde dünya küçüldü: ilk dünya turu tamamlandı, Atlantik bir ticaret yolu oldu, sömürgeciliğin ahlâkı üzerine en bilinen büyük tartışma yapıldı.", ),
             ("Strateji oyunlarında buna “kişisel birlik” derler: tek bir hükümdar, birçok devlet. Şarlken bunu oyun olarak değil, ömür olarak yaşadı.", ),
         ], [
             ("Peki kaybeden kim? O mu, yoksa tek bir adamın bütün dünyayı taşıyabileceği fikri mi?", ),
             ("Beş cepheden birini bırakmak zorunda olsaydınız, hangisini bırakırdınız? Yorumlarda yazın.", ),
             ("Zaman Kuryesi'nden bugünkü teslimat bu. Bir sonrakinde görüşürüz.", ),
         ]]),
]


# ---------------------------------------------------------------- türetilmiş yapılar
def sentences():
    """Düz liste: dict(id, ch, para, disp, speech)."""
    out = []
    for ch in CHAPTERS:
        k = 0
        for pi, para in enumerate(ch["paras"]):
            for tup in para:
                k += 1
                raw = tup[0]
                disp = to_display(raw)
                speech = to_speech(tup[1] if len(tup) > 1 else raw)
                out.append(dict(id=f"{ch['id']}s{k}", ch=ch["id"], para=pi, disp=disp, speech=speech))
    return out


def chapter_text(ch_id):
    """ElevenLabs'e gidecek bölüm metni: paragraflar boş satırla ayrılır."""
    ch = next(c for c in CHAPTERS if c["id"] == ch_id)
    paras = []
    for para in ch["paras"]:
        paras.append(" ".join(to_speech(t[1] if len(t) > 1 else t[0]) for t in para))
    return "\n\n".join(paras)


if __name__ == "__main__":
    import sys
    tot_w = tot_c = 0
    for ch in CHAPTERS:
        txt = chapter_text(ch["id"])
        w = len(txt.split())
        tot_w += w
        tot_c += len(txt)
        print(f"{ch['id']:4s} {w:4d} sözcük  {len(txt):5d} karakter  ≈{w/1.8/60:4.1f} dk  {ch['title']}")
    print(f"TOPLAM {tot_w} sözcük, {tot_c} karakter, ≈{tot_w/1.8/60:.1f} dk (1,8 söz/sn)")
    if len(sys.argv) > 1:
        print()
        print(chapter_text(sys.argv[1]))

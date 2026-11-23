#!/usr/bin/env python3
"""senaryo.json üretici (rev0). Her satır: (id, bölüm, tts etiketi, metin, kaynak). 'alt' = metin (etiketsiz)."""
import json, os
R = '1818 = kaynak/frankenstein_1818_gutenberg41445.txt satır; 1831ö = kaynak/frankenstein_1831_gutenberg42324.txt (önsöz) satır'
S = [
# ── Kanca ──
('A01','Kanca','softly',"On sekiz yaşında bir kızın yazdığı bir sahne: bir yaratık, hayatının ilk gecesinde onu yapan adamın yatağının başına geliyor, perdeyi aralıyor ve ona elini uzatıyor.","Kapak A (ELİNİ UZATTI) ve kapak B (18 YAŞINDA YAZDI) ilk cümlede. 1818: 1464-1469 (perdeyi kaldırır, bir eli uzanmış)"),
('A02','Kanca','calmly',"Adam o eli tutmuyor; kaçıyor.","1818: 1469-1470 (I escaped); 1449-1450 (I rushed out of the room). L3 açılır"),
('A03','Kanca','calmly',"Yaratığın adı yok; onu yapan, ona bir ad bile koymadı. İki yüz yıldır ona, kaçan adamın adıyla sesleniyoruz: Frankenstein.","Romanda yaratık hiç adlandırılmaz (creature, wretch, daemon, monster). L4 açılır"),
('A04','Kanca','curious',"Kitap çıkınca yazarına, Mary Shelley'ye, yıllarca aynı şeyi sordular: genç bir kız böyle korkunç bir fikri nereden buldu?","1831ö: 66-68 (\"How I, when a young girl, came to think of… so very hideous an idea?\"). L1 açılır, H01-H09 kapatır"),
('A05','Kanca','thoughtful',"Birazdan yaratık konuşacak ve hikâyesini kendi ağzından anlatacak. Dinleyince kararı sen ver: canavar doğulur mu, yoksa terk edilince mi olunur?","1818: 2974 (Listen to my tale), L6. Başlığın sorusu. L2; cevap olaylarla D-F, kendi sözü C09/F07, halka G03"),
# ── I. Yazsız yıl ──
('B01','Yazsız yıl','calmly',"Haziran 1816, Cenevre Gölü'nün kıyısı. Takvim yazı gösteriyor, ama yaz gelmiyor.","Hikâye burada başlar (köprü cümlesi yok)"),
('B02','Yazsız yıl','calmly',"Mary bir mektubunda yazıyor: neredeyse hiç dinmeyen bir yağmur bizi eve kapatıyor. Şimşek bir an gölü aydınlatıyor, sonra zifiri karanlık.","Six Weeks' Tour 1817, Mektup II (Mary, 1 Haziran 1816): kaynak/six_weeks_tour_1817_archive.txt 2501-2528"),
('B03','Yazsız yıl','softly',"Mary on sekiz yaşında. Yanında sevgilisi, genç şair Percy Shelley var.","Mary d. 30 Ağustos 1797 (Godwin 1798: 2141) → Haziran 1816'da 18. Percy d. 4 Ağustos 1792 (23)"),
('B04','Yazsız yıl','softly',"Annesi de yazardı. Mary'yi doğurduktan on bir gün sonra öldü; Mary onu hiç tanımadı.","Godwin, Memoirs 1798: 2141 (30 Ağustos), 2390 (10 Eylül 1797). Ad (Mary Wollstonecraft) yalnız ekranda"),
('B05','Yazsız yıl','softly',"Geçen kış Mary de anne olmuştu. Erken doğan kızı on iki gün yaşadı. Şimdi yanında beş aylık bir oğlu var.","Günlük (Dowden 1886 c.1): 29700-29720 (22 Şubat 1815 doğum, 6 Mart 'Find my baby dead'); oğlu William d. 24 Ocak 1816 (Dowden 31064). L5 ekilir"),
('B06','Yazsız yıl','calmly',"Gölün kıyısındaki büyük villada Lord Byron kalıyor. O yaz bir şiir yazacak: Bir düş gördüm, hepsi düş değildi. Parlak güneş sönmüştü.","Byron, 'Darkness' (1816), kaynak/byron_darkness_1816_wikisource1901.txt 19-20; çeviri bizim"),
('B07','Yazsız yıl','calmly',"O kıyıdakilerin bilmediği bir şey var. Bir yıl önce dünyanın öbür ucunda, Endonezya'da Tambora yanardağı patladı. Göğe savrulan kül ve gaz, ertesi yıl Avrupa'nın yazını söndürdü; bunu ancak yüz yıl kadar sonra anlayacağız.","Tambora 10-11 Nisan 1815 (Oppenheimer 2003, Progress in Physical Geography 27:2); bağ 1910'larda (W. J. Humphreys), Stommel 1979. Odadakilere bilgi verilmez (yön notu)"),
('B08','Yazsız yıl','calmly',"Yağmurlu akşamlardan birinde ellerine Almancadan çevrilmiş bir hayalet hikâyeleri kitabı geçiyor.","1831ö: 126-128 (Fantasmagoriana; Polidori 1911 notu 4321)"),
('B09','Yazsız yıl','firmly',"Byron öneriyor: her birimiz bir hayalet hikâyesi yazacağız.","1831ö: 145 (\"We will each write a ghost story\")"),
('B10','Yazsız yıl','calmly',"Ötekiler başlıyor. Mary bulamıyor. Her sabah ona soruyorlar: bir hikâye buldun mu? Ve her sabah, diye yazacak, utanarak hayır diyorum.","1831ö: 165-169 (mortifying negative). Polidori 17 Haziran 'begun by all but me' (4282-4283): zamanlama farkı DOGRULAMA'da"),
('B11','Yazsız yıl','calmly',"Mary'nin anlattığına göre geceleri Byron ile Percy konuşuyor, o sessizce dinliyor: bir ölü yeniden canlandırılabilir mi?","1831ö: 184-196. Anlatım Mary'nin 1831 anlatımı olarak çerçevelenir"),
('B12','Yazsız yıl','softly',"Bir gece başını yastığa koyuyor ve uyuyamıyor. Gözleri kapalı, bir sahne görüyor.","1831ö: 198-203"),
('B13','Yazsız yıl','slowly',"Soluk bir öğrenci, bir araya getirdiği şeyin başında diz çökmüş. O şey kıpırdıyor. Öğrenci dehşet içinde kaçıyor; unutmak için uykuya sığınıyor.","1831ö: 203-216"),
('B14','Yazsız yıl','slowly',"Uyandığında o şey yatağının başında: perdeyi aralamış, sarı, ıslak ama düşünen gözlerle ona bakıyor.","1831ö: 216-218 (yellow, watery, but speculative eyes)"),
('B15','Yazsız yıl','softly',"Ben de korkuyla gözlerimi açtım, diye yazacak Mary on beş yıl sonra.","1831ö: 220 (I opened mine in terror)"),
('B16','Yazsız yıl','calmly',"Ertesi sabah hikâyesini bulmuştu. Yazdığı ilk cümle şuydu: Kasım'ın kasvetli bir gecesiydi.","1831ö: 233-236; 1818: 1425 (IV. bölümün başı). Kancanın (A01) kaynağı kapanır"),
# ── II. Kasım gecesi ──
('C01','Kasım gecesi','calmly',"Mary'nin romanında öğrencinin adı Victor Frankenstein. İki yıla yakın, dinlenmeden çalıştı.","1818: 1445-1447 (nearly two years… deprived myself of rest)"),
('C02','Kasım gecesi','calmly',"Yaratığın yüzünü güzel olsun diye tek tek seçmişti.","1818: 1436-1437 (I had selected his features as beautiful)"),
('C03','Kasım gecesi','slowly',"Ama yaratık gözünü açınca Victor ne yaptığını gördü: sarı deri kasları zor örtüyor; saçlar uzun ve parlak siyah, dişler inci gibi; gözler ıslak, göz çukurlarıyla neredeyse aynı renk.","1818: 1437-1442. Yaratık roman tarifiyle çizilir (1931 tasarımı değil)"),
('C04','Kasım gecesi','calmly',"Victor odadan kaçtı. Yaratığa ne bir ad verdi, ne bir söz söyledi.","1818: 1449-1450. L3 kapanır"),
('C05','Kasım gecesi','calmly',"Romanın geri kalanında da ona bir ad yerine hep bir sıfatla seslenecek: sefil, alçak, canavar.","1818: wretch, villain, monster (her yerde)"),
('C06','Kasım gecesi','calmly',"Yaratık onu yıllar sonra, Mont Blanc'ın eteğinde, bir buzulun üstünde buldu.","1818: 2888 (Mer de Glace); 2900-2952"),
('C07','Kasım gecesi','firmly',"İyiydim, dedi, iyi yürekliydim; çektiğim acı beni canavara çevirdi. Beni mutlu et, yine iyi olurum.","1818: 2949-2951 (I was benevolent and good; misery made me a fiend. Make me happy, and I shall again be virtuous). Yaratığın iddiası; kanıtı D-F"),
('C08','Kasım gecesi','firmly',"Beni dinle. Dinledikten sonra istersen terk et, istersen acı bana.","1818: 2974-2975 (Listen to my tale: when you have heard that, abandon or commiserate me)"),
('C09','Kasım gecesi','calmly',"Romanın tam ortasında yaratık konuşur. Bundan sonrası onun kendi ağzından.","Romanın II. cildi yaratığın anlatısı. Anlatım birinci tekile geçer (D01-F05)"),
# ── III. Duvardaki yarık (yaratık, birinci tekil) ──
('D01','Duvardaki yarık','slowly',"Önce hiçbir şeyi birbirinden ayıramıyordum. Işık, karanlık, açlık, soğuk; hepsi bir aradaydı.","1818: 3060-3062"),
('D02','Duvardaki yarık','softly',"Ormanda bir gece ağaçların arasından ışıklı bir şey yükseldi. Gözümü ondan ayıramadım.","1818: 3053-3064 (radiant form… the bright moon)"),
('D03','Duvardaki yarık','softly',"Kuşların sesini taklit etmeye çalıştım. Ağzımdan çıkan ses beni korkuttu; sustum.","1818: 3073-3077"),
('D04','Duvardaki yarık','calmly',"Bir gün gezginlerin bıraktığı bir ateş buldum. Sevinçle elimi közlere soktum, bağırarak çektim. Ne tuhaf, dedim: aynı şey hem ısıtıyor, hem yakıyor.","1818: 3089-3093"),
('D05','Duvardaki yarık','calmly',"Bir akşam bir köye girdim. Çocuklar çığlık attı, bir kadın bayıldı. Taşlarla kovaladılar beni.","1818: 3159-3163"),
('D06','Duvardaki yarık','calmly',"Bir eve bitişik alçak bir odunluğa sığındım. Duvarda küçük bir yarık vardı. Oradan bir aileyi izledim: kör bir ihtiyar, kızı ve oğlu.","1818: 3164 vd. (hovel, chink). De Lacey, Agatha, Felix adsız"),
('D07','Duvardaki yarık','calmly',"Yoksuldular. Geceleri yiyeceklerinden çalıyordum; onları aç bıraktığımı anlayınca bıraktım.","1818: 3335-3339"),
('D08','Duvardaki yarık','warmly',"Onun yerine geceleri odun kesip kapılarının önüne yığdım.","1818: 3341-3345"),
('D09','Duvardaki yarık','warmly',"Sabah kız kapıyı açınca şaşkınlıkla bağırdı. Bu işleri görünmeyen bir el yapıyordu; kendi aralarında benden iyi ruh diye söz ettiler.","1818: 3346-3349; 3448-3452 (invisible hand; good spirit, wonderful)"),
('D10','Duvardaki yarık','sad',"Onları dinleyerek konuşmayı öğrendim. Baba, anne, kardeş. Benim babam, annem neredeydi? Bebekliğimde başımda bekleyen bir baba, bana gülümseyen bir anne olmadı.","1818: 3674-3680 (No father had watched my infant days, no mother had blessed me with smiles)"),
('D11','Duvardaki yarık','sad',"Bir gün durgun bir suda kendimi gördüm. Önce geri sıçradım. Sudaki yüzün benim olduğuna inanamadım.","1818: 3422-3426"),
('D12','Duvardaki yarık','sad',"Laboratuvardan aldığım giysinin cebinde kâğıtlar vardı: Victor'un günlüğü. Nasıl yapıldığımı orada okudum. Beni yapan bile benden tiksinip yüz çevirmişti.","1818: 3971-3988 (papers in the pocket… even you turned from me in disgust)"),
('D13','Duvardaki yarık','calmly',"Yine de bir umudum vardı: yüzümü görmeden önce sesimi duysunlar. Ve o evde beni göremeyecek biri vardı.","1818: Cilt II bölüm 6 sonu. L7 açılır"),
# ── IV. Kör adam ──
('E01','Kör adam','calmly',"Bir gün ötekiler yürüyüşe çıktı. İhtiyar evde yalnızdı. Kapıyı çaldım.","1818: Cilt II bölüm 7"),
('E02','Kör adam','warmly',"Konuştuk. İhtiyar dedi ki: Ben körüm, yüzünü göremem; ama sözlerinde, doğru söylediğine beni inandıran bir şey var.","1818: 4139-4141. L7 kapanır"),
('E03','Kör adam','softly',"Hayatımda ilk kez bir insan sesi bana iyilikle konuşuyordu.","1818: 4154-4155"),
('E04','Kör adam','calmly',"Ayak sesleri yaklaşınca ihtiyarın elini tuttum. Beni bırakma, dedim. Aradığım dostlar sizsiniz.","1818: 4164-4167"),
('E05','Kör adam','firmly',"Kapı açıldı. Kız bayıldı. Oğlu beni babasının dizlerinden kopardı, yere attı ve sopayla vurdu.","1818: 4171-4177"),
('E06','Kör adam','sad',"Onu paramparça edebilirdim. Ama yüreğim içime çöktü. Elimi kaldırmadım.","1818: 4178-4179"),
('E07','Kör adam','calmly',"Ertesi gün kulübe boştu. Bir daha dönmediler.","1818: 4242-4270"),
('E08','Kör adam','firmly',"O gece kulübeyi ateşe verdim.","1818: 4283-4298"),
('E09','Kör adam','calmly',"Yolda bir kız nehre düştü. Atladım, onu kıyıya çıkardım, yeniden nefes alsın diye uğraştım.","1818: 4363-4370 (endeavoured… to restore animation)"),
('E10','Kör adam','sad',"Yanındaki adam beni görünce tüfeğini kaldırdı ve ateş etti. İyiliğimin karşılığı omzuma giren bir kurşundu.","1818: 4373-4387"),
# ── V. Ben de yaratabilirim ──
('F01','Ben de yaratabilirim','calmly',"Cenevre'nin yakınında bir çocuk gördüm. Bu kadar küçük biri, dedim, henüz benden korkmayı öğrenmemiştir. Onu yanıma alırsam yalnız kalmam.","1818: 4411-4417"),
('F02','Ben de yaratabilirim','firmly',"Çocuk gözlerini elleriyle kapattı ve çığlık attı: Bırak beni, canavar! Babama söylerim. Babam Bay Frankenstein!","1818: 4420-4432"),
('F03','Ben de yaratabilirim','slowly',"Düşmanımın adıydı. İlk kurbanım sen olacaksın, dedim. Susturmak için boğazına sarıldım; bir an sonra ayaklarımın dibinde kıpırtısız yatıyordu.","1818: 4433-4439 (you shall be my first victim; I grasped his throat). Hassasiyet: şiddet gösterilmez"),
('F04','Ben de yaratabilirim','firmly',"Ellerimi çırptım ve bağırdım: Ben de yıkım yaratabilirim!","1818: 4440-4442 (clapping my hands… I, too, can create desolation)"),
('F05','Ben de yaratabilirim','sad',"Çocuğun göğsünde parıldayan bir şey vardı: güzel bir kadının resmi. Bir an ona baktım ve öfkem dindi. Sonra o gözlerin bana nasıl bakacağını düşündüm.","1818: 4445-4454"),
('F06','Ben de yaratabilirim','calmly',"Yaratığın sözünü ettiği çocuk, Victor'un küçük kardeşiydi.","Anlatım yeniden üçüncü tekil (öncesinde duraklama)"),
('F07','Ben de yaratabilirim','thoughtful',"Hikâyesini bitirince dedi ki: Kötüyüm, çünkü mutsuzum. Bana benim gibi bir eş yap; insanlardan uzağa gideriz.","1818: 4508 (I am malicious because I am miserable); Cilt II bölüm 8-9"),
('F08','Ben de yaratabilirim','calmly',"Victor kabul etti. Uzak bir adada ikinci yaratığı yapmaya başladı.","1818: Cilt III bölüm 2-3 (Orkney)"),
('F09','Ben de yaratabilirim','slowly',"Yarısına gelmişti ki pencerede, ay ışığında onu izleyen yüzü gördü. Ve yarım kalan bedeni parçaladı.","1818: 5262-5271. L8 açılır (H10)"),
('F10','Ben de yaratabilirim','firmly',"Yaratık giderken şunu söyledi: Düğün gecende yanında olacağım.","1818: 5342-5343"),
('F11','Ben de yaratabilirim','calmly',"Sözünü tuttu. Victor'un sevdiklerini birer birer elinden aldı.","1818: Clerval, Elizabeth (düğün gecesi). Ayrıntı ve şiddet gösterilmez"),
# ── VI. Buzların arasında ──
('G01','Buzların arasında','calmly',"Victor onu kuzeye, buzların arasına kadar kovaladı. Orada bir gemiye alındı ve gemide öldü.","1818: Walton mektupları"),
('G02','Buzların arasında','slowly',"O gece geminin kaptanı kamaraya girince tabutun üstüne eğilmiş dev bir karaltı gördü. Yüzünü uzun, dağınık saçları örtüyordu. Bir eli uzanmıştı.","1818: 7110-7116 (one vast hand was extended). Kapak A'nın halkası"),
('G03','Buzların arasında','softly',"Hikâyenin ilk gecesinde yaratık elini uzatmış, Victor kaçmıştı. Şimdi Victor kaçamıyordu.","Halka: A01 ↔ G02"),
('G04','Buzların arasında','sad',"Bu da benim kurbanım, dedi yaratık. Soğumuş; artık bana cevap veremez.","1818: 7128-7133 (That is also my victim!… Alas! he is cold; he may not answer me)"),
('G05','Buzların arasında','slowly',"Sonra pencereden buz salının üstüne atladı. Dalgalar onu aldı; karanlıkta, uzakta kayboldu.","1818: 7276-7278 (romanın son cümlesi). Ölüm yakma planı anlatılmaz (hassasiyet)"),
# ── VII. Çirkin evladım ──
('H01','Çirkin evladım','thoughtful',"Peki on sekiz yaşında bir kız bunu neden yazdı?","L1 geri döner"),
('H02','Çirkin evladım','calmly',"Kitap 1818'de çıktı. Kapağında yazarın adı yoktu. Yıllar sonra sahneye konunca, afişte yaratığın adının yerinde de yalnızca bir çizgi vardı.","1818 başlık sayfası adsız (kaynak/frankenstein_1818 36-60). Afiş: Mary'nin mektubu, Eylül 1823 (Marshall 1889 c.2: kaynak/marshall_1889_cilt2_archive.txt 4286-4293). L4 kapanır"),
('H03','Çirkin evladım','calmly',"1831'de, yeni baskıya yazdığı önsözde Mary o soruya cevap verdi: gözlerim kapalı ama uyanıkken bir şey gördüm, dedi; onu kâğıda geçirdim.","1831ö: 198-236 (I did not sleep… my waking dream)"),
('H04','Çirkin evladım','calmly',"O yazı mutlu günler diye andı: ölüm ve keder, o zaman benim için yalnızca sözcüklerdi.","1831ö: 246-248"),
('H05','Çirkin evladım','calmly',"Ama on yedi yaşında tuttuğu günlükte, bebeğini kaybettiği haftalardan satırlar var. Ne zaman yalnız kalsam, düşüncelerim hep aynı yere dönüyor: bir anneydim, artık değilim.","Günlük 13 Mart 1815 (Dowden 1886 c.1: 29733-29738: \"that I was a mother, and am so no longer\")"),
('H06','Çirkin evladım','softly',"Düşümde bebeğim yeniden canlandı. Yalnızca üşümüştü; onu ateşin önünde ovduk ve yaşadı. Uyandım; bebek yok.","Günlük 19 Mart 1815 (Dowden 29742-29746), kelimesi kelimesine. L5 kapanır"),
('H07','Çirkin evladım','calmly',"Mary bu iki kaydı bildiğimiz hiçbir yazısında yan yana getirmedi. Biz yalnızca yan yana koyuyoruz.","Yön notu: 'bu yüzden yazdı' olgu diye söylenmez"),
('H08','Çirkin evladım','warmly',"O önsözün sonunda şöyle yazdı: Çirkin evladıma bir kez daha, git ve yolun açık olsun, diyorum. Ona karşı bir sevgim var.","1831ö: 246-247 (I bid my hideous progeny go forth and prosper. I have an affection for it)"),
('H09','Çirkin evladım','calmly',"Victor yarattığından kaçtı. Mary ise yarattığını yıllar sonra yeniden eline aldı ve onu dünyaya bir kez daha gönderdi.","İksir: olay (1831 baskısı ve önsözü). L1 kapanır"),
('H10','Çirkin evladım','thoughtful',"Senin de yarım bırakıp yüzüne bakamadığın bir iş, bir söz, bir insan var mı? Yorumlara yaz.","Başlığın sorusu izleyiciye döner; L8 (yarım kalan) kapanır"),
('H11','Çirkin evladım','warmly',"Mary romanına bir ad daha vermişti: Modern Prometheus. Geçmişten bir soru daha getirmemiz için Zaman Kuryesi'ne abone ol. İlk Prometheus ekranda.","Romanın alt başlığı. Abone çağrısı son anın içinde; 'ekranda' bitiş ekranının (son 20 sn) içinde; bitiş ekranı: Prometheus videosu"),
]
OKU = [('Frankenstein', 'Frankenştayn'), ('Mary', 'Meri'), ('Byron', 'Bayrın'), ('Percy', 'Pörsi'), ('Mont Blanc', 'Mon Blan'), ('Victor', 'Viktor'), ('Shelley', 'Şelli'), ('Tambora', 'Tambora')]
def oku(m):
    for a_, b_ in OKU: m = m.replace(a_, b_)
    return m
seg = [{'id': i, 'bolum': b, 'tts': f'[{t}] {oku(m)}', 'alt': m, 'kaynak': k} for i, b, t, m, k in S]
for x in seg:
    if x['id'] in ('F06',): x['vo_parca'] = True   # birinci tekilden dönüş: yeni çekim (doğal duraklama)
out = {'voice': 'Emrullah (ElevenLabs; voice_id creative_list_voices ile bulunur)', 'revizyon': 'rev1 (23 Kasım 2026): Fable senaryo okuması uygulandı (uretim_plani.md §8)',
       'not': 'Kaynak: Frankenstein (1818, 1831 önsöz), Mary Shelley günlüğü 1815 (Dowden 1886), Six Weeks\' Tour (1817), Godwin Memoirs (1798). Çeviriler bizim. ' + R + '. İskelet: iç içe çerçeve (uretim_plani.md).',
       'segments': seg}
p = os.path.join(os.path.dirname(__file__), '..', 'senaryo.json')
json.dump(out, open(p, 'w'), ensure_ascii=False, indent=1)
n = sum(len(x['alt']) for x in seg)
print(len(seg), 'cümle,', n, 'karakter, ~%.1f dk' % (n / 760))

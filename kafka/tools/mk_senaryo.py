import json
G="Gutenberg satırı "
S=[
# --- KI: giriş
("A01","Bir sabah","calmly","Bir sabah uyandığında artık eskisi gibi değilsin. Seni sevenler, seni yine sever mi?","kapak ve başlık vaadi; merak sorusu ilk cümlede; cevap E05–E06, soru F07'de izleyiciye döner"),
("A02","Bir sabah","calmly","Franz Kafka'nın Dönüşüm'ü şöyle başlar: Gregor Samsa bir sabah huzursuz düşlerden uyandığında, kendini yatağında korkunç bir haşereye dönüşmüş buldu.",G+"1–2 (çevirimiz; 'ungeheueres Ungeziefer'). Ekranda künye: FRANZ KAFKA · DÖNÜŞÜM · 1915"),
("A03","Bir sabah","curious","Peki o sabah onu en çok ne korkuttu? Böcek olmak değil.","L1 açılır; cevap A04"),
("A04","Bir sabah","wry","İşe geç kalmak. Saat beş treni gitmişti, sonraki yedideydi. Patron ne diyecekti?",G+"64, 73"),
("A05","Bir sabah","calmly","Bu videoda o böceği hiç görmeyeceksiniz. Nedenini sona saklıyorum.","L2 açılır; cevap F01–F02 (K9 doğrulanamazsa F02 değişir)"),
("A06","Bir sabah","thoughtful","Çünkü bu hikâyede dönüşen tek kişi Gregor değil.","L3 açılır; cevap E10–E12"),
# --- SHŌ 1
("B01","Hayvan sesi","calmly","Gregor gezici bir satıcıydı. Babasının batan işinden kalan borcu o ödüyor, annesine, babasına ve on yedi yaşındaki kız kardeşi Grete'ye o bakıyordu.",G+"14, 61 (borç), 882 (on yedi yaş)"),
("B02","Hayvan sesi","tense","Saat yediyi geçince işyerinden müdür yardımcısı kapıya dayandı. Gregor kapının arkasından her şeyin yolunda olduğunu anlatmaya çalıştı.","prokurist (müdür yardımcısı) gelişi; Gregor'un uzun konuşması"),
("B03","Hayvan sesi","quietly","Kendini anlaşılır sanıyordu. Ama müdür yardımcısı fısıldadı: “Bu bir hayvan sesiydi.”",G+"365 ('Das war eine Tierstimme')"),
("B04","Hayvan sesi","tense","Gregor anahtarı ağzıyla çevirip kapıyı açtı. Müdür yardımcısı merdivenlere kaçtı.",G+"395–398; kaçış"),
("B05","Hayvan sesi","tense","Babası ise bir eline bastonu, öbürüne gazeteyi aldı ve onu odasına geri sürdü. Hiçbir yalvarış işe yaramadı.",G+"552–557"),
("B06","Hayvan sesi","thoughtful","İçi aynıydı. Değişen yalnız dışıydı. Ama o sabahtan sonra herkes yalnız dışını görecekti.","yorum (kullanıcının okuması: dış görünüş değişince hor görülmek)"),
# --- SHŌ 2
("C01","Süt ve elma","warmly","Ona bakan tek kişi Grete oldu.","bölüm başı"),
("C02","Süt ve elma","warmly","İlk akşam kapının önüne, eskiden en sevdiği şeyi bıraktı: içinde beyaz ekmek yüzen bir kâse tatlı süt.",G+"625"),
("C03","Süt ve elma","calmly","Ama Gregor artık sütten tat almıyordu. Grete bunu fark etti ve ertesi gün ne sevdiğini anlamak için önüne bir yığın yiyecek serdi: yarı çürük sebzeler, eski bir peynir, akşam yemeğinden kalan kemikler.",G+"628–633, 712–715"),
("C04","Süt ve elma","warmly","Bu sevgiydi. Gerçek bir sevgi.","aile 'ikisinin ortası' (kullanıcı ve başkan)"),
("C06","Süt ve elma","tense","Bir akşam kapıda bir adam belirdi. Gregor onu tanıyamadı: aylardır koltuktan kalkmayan babası, altın düğmeli mavi bir üniformanın içinde dimdik duruyordu.",G+"1197–1198 (banka odacısı üniforması); K5"),
("C07","Süt ve elma","tense","Babası büfedeki meyve tabağından ceplerini doldurdu ve küçük kırmızı elmaları birer birer attı.",G+"1232–1234 (Kredenz, Obstschale, kleinen roten Äpfel); filmin tek rengi"),
("C08","Süt ve elma","slowly","Biri Gregor'un sırtına saplandı. Kimse çıkarmaya cesaret edemedi. Elma orada kaldı ve çürüdü.",G+"1235, 1258, 1736"),
# --- TEN 1: hesap
("D01","Kapının arkasındaki hesap","calmly","Biraz geri saralım. Gregor yıllarca neden bu kadar çok çalışmıştı?","bölüm başı; küçük merak sorusu"),
("D02","Kapının arkasındaki hesap","calmly","Babasının işi battığında, neredeyse bir gecede küçük bir tezgâhtardan gezici satıcıya dönüştü. Kazandığını eve getirip masaya koydu.",G+"815–823 ('Kommis' → 'Reisender'); ilk dönüşüm"),
("D03","Kapının arkasındaki hesap","quietly","Kafka o yılları tek cümleyle anlatır: “Parayı minnetle alıyorlardı, o da seve seve veriyordu. Ama aralarında artık özel bir sıcaklık kalmamıştı.”",G+"826–829 (çevirimiz). Ekranda alıntı"),
("D04","Kapının arkasındaki hesap","curious","Böcek olduktan sonra, kapının arkasından bir şey duydu. Aile sandığı kadar parasız değilmiş.",G+"850–856"),
("D05","Kapının arkasındaki hesap","calmly","Eski işten kalan küçük bir servet varmış. Gregor'un getirdiği paradan da bir kenara para ayrılmış. O parayla babasının borcu çok daha erken kapanabilir, Gregor sevmediği işten çok daha erken kurtulabilirmiş.",G+"855–866"),
("D06","Kapının arkasındaki hesap","curious","Gregor ne yaptı? Kızmadı.","AMA"),
("D07","Kapının arkasındaki hesap","quietly","Kapının arkasında hevesle başını salladı. Bu tutumluluğa sevindi.",G+"861–862 ('nickte eifrig, erfreut')"),
("D08","Kapının arkasındaki hesap","thoughtful","İşte ilk sürpriz. Koşulu yalnız ailesi koymuyordu. Gregor da kendi değerini eve getirdiği parayla ölçüyordu.","yorum (Ten 1); kullanıcının omurgası: koşullu sevgi"),
("D09","Kapının arkasındaki hesap","warmly","Sevgisini bile parayla göstermek istiyordu: gizli planı, masrafı ne olursa olsun, keman çalan Grete'yi konservatuvara göndermekti.",G+"829–834"),
# --- TEN 2: bu
("E01","O değil, bu","calmly","Eve para girmeyince herkes çalışmaya başladı. Baba banka odacısı oldu, anne bir moda dükkânına iç çamaşırı dikti, Grete tezgâhtar oldu.",G+"1197–1198, 1283–1284"),
("E01b","O değil, bu","calmly","Grete sabah dükkâna koşmadan önce yemeği ayağıyla odaya itiyordu. Duvarlarda kir izleri birikti; o kiri görüyor ama bırakmayı seçmişti.","Gutenberg satırı 1373–1385 (\"mit dem Fuß\", \"Schmutzstreifen\", \"sich entschlossen, ihn zu lassen\"); sevginin aşınması"),
("E02","O değil, bu","calmly","Bir odayı da üç kiracıya verdiler. Bir akşam Grete onlar için keman çaldı.",G+"1446, 1504"),
("E03","O değil, bu","quietly","Gregor müziğe doğru süründü ve odasından çıktı. Kiracılar onu gördü.","Gutenberg satırı 1557–1558 (\"War er ein Tier, da ihn Musik so ergriff?\")"),
("E04","O değil, bu","firm","O gece Grete masaya vurdu: “Böyle gitmez. Bu canavarın önünde kardeşimin adını ağzıma almayacağım. Bundan kurtulmalıyız.”",G+"1633–1637 (çevirimiz). Not: Almancada 'es' dilbilgisel olarak 'Untier'e (nötr) bağlanır; videoda 'zamir değişti' denmez, 'adını ağzına almadı' denir"),
("E05","O değil, bu","firm","“Bunun Gregor olduğu düşüncesinden kurtulmalısın, baba. Asıl felaketimiz, bu kadar uzun süre buna inanmış olmamız.”",G+"1675–1677 (çevirimiz). Ekranda alıntı"),
("E06","O değil, bu","thoughtful","İlk akşam ona süt getiren kız kardeşti bu. Sevgisi bir günde bitmemişti; yorgunlukla, gün gün aşınmıştı.","yorum; aile ikisinin ortası"),
("E07","O değil, bu","slowly","Gregor o gece ailesini sevgiyle ve duygulanarak düşündü. Ortadan kalkması gerektiğine kız kardeşinden de çok inanıyordu.",G+"1737–1740"),
("E08","O değil, bu","slowly","Kilise saati üçü vurdu. Pencerenin dışında hava aydınlanmaya başlarken, son nefesini verdi.",G+"1741–1744. Görselde yalnız pencere ve ışık"),
("E09","O değil, bu","calmly","Aile o gün işe gitmedi. Tramvaya binip şehrin dışına çıktılar.","Gutenberg satırı 1836, 1873"),
("E10","O değil, bu","calmly","Yolda anne ile baba, kızlarının bütün o bakım günlerine rağmen nasıl serpildiğini fark ettiler. Ona iyi bir koca bulma zamanı gelmişti.",G+"1885–1890"),
("E11","O değil, bu","slowly","Yolculuğun sonunda ilk ayağa kalkan Grete oldu ve genç bedenini gerindi. Hikâyenin asıl dönüşümü buydu.",G+"1891–1892; L3 kapanır"),
# --- KETSU
("F01","Görünmeyen böcek","curious","Peki o böceği neden hiç görmediniz?","L2 kapanış başı"),
("F02","Görünmeyen böcek","calmly","Kitap basılırken Kafka yayıncısına yazdı: böceğin kendisi çizilmesin, uzaktan bile gösterilmesin.","K9: Kafka'nın Kurt Wolff Verlag'a mektubu, 25 Ekim 1915 — DOĞRULANACAK (kaynak üyesi). Doğrulanamazsa: 'Kafka ona bir tür adı bile vermez' (satır 2)"),
("F03","Görünmeyen böcek","thoughtful","Belki de Gregor'un neye dönüştüğü önemli değildi. Önemli olan, ötekilerin artık onda ne gördüğüydü.","yorum"),
("F04","Görünmeyen böcek","quietly","Dört yıl sonra Kafka babasına uzun bir mektup yazdı ve onu hiç göndermedi. İçinde şu cümle var: “Yazdıklarımın hepsi senin hakkındaydı.”","K10: Brief an den Vater (1919) 'Mein Schreiben handelte von Dir' — DOĞRULANACAK; Almanca metin depoya alınacak. Tek kısa geri dönüş (kullanıcının kararı)"),
("F05","Görünmeyen böcek","thoughtful","Kafka'nın kendi koşulu da belliydi: beklenen oğul olmak.","yorum; kaynak üyesi tartacak (mektuptaki baba beklentisi). Zayıfsa çıkar"),
("F06","Görünmeyen böcek","calmly","Bugün kimse bir sabah böcek olarak uyanmıyor. Ama işini kaybeden, eskisi gibi kazanamayan, eskisi gibi görünmeyen herkes o kapının arkasında bir gece geçirir.","bugünkü karşılık (başkan); hastalık/engellilik bilerek yok"),
("F07","Görünmeyen böcek","slowly","Asıl soru o kapıda: Seni sevenler seni mi seviyordu, yoksa işe yarayan hâlini mi?","A01'in sorusu izleyiciye döner; doruk"),
("F08","Görünmeyen böcek","slowly","Ve belki daha zoru: Sen kendini hangi koşulla seviyorsun? Yorumlarda yaz.","Ten 1'in (D07–D08) bugünkü karşılığı"),
("F09","Görünmeyen böcek","warmly","Camus, Sisifos Söyleni'ne Kafka üzerine bir deneme eklemişti. Sisifos'un hikâyesi ekranda. Geçmişten bugüne sorular taşımaya devam etmemizi istiyorsan Zaman Kuryesi'ne abone ol.","bitiş ekranı → Sisifos (kanalın kapısı). Camus'nün eki 'L'espoir et l'absurde dans l'œuvre de Franz Kafka' — DOĞRULANACAK"),
]
import itertools
segs=[]
for (i,b,t,x,k) in S:
    pass
segs=[{"id":i,"bolum":b,"tts":f"[{t}] {x}","alt":x,"kaynak":k} for i,b,t,x,k in S]
cnt={}
for sg in segs:
    L0=sg["id"][0]; cnt[L0]=cnt.get(L0,0)+1; sg["id"]=f"{L0}{cnt[L0]:02d}"
d={"voice":"Emrullah (ElevenLabs; voice_id creative_list_voices ile bulunur)",
"revizyon":"rev0 (15 Kasım 2026): ilk taslak; kurul toplanmadı (kullanıcının haftalık kullanımı %89)",
"not":"Kaynak: Franz Kafka, Die Verwandlung (1915; kamu malı), kaynak/die_verwandlung_numarali.txt (Gutenberg #22367; satır numaraları bu dosyadaki). Çeviriler bizim. İskelet: Kişōtenketsu (uretim_plani.md). DOĞRULANACAK: F02 (Wolff mektubu), F04 (Babaya Mektup), F09 (Camus eki).",
"segments":segs}
json.dump(d,open('senaryo.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
L=["# Kafka, Dönüşüm: senaryo (rev0, taslak; kurul toplanmadı)","","Okuma kopyası. Asıl dosya `senaryo.json`.",""]
cur=None; chars=0
for s in segs:
    if s['bolum']!=cur: cur=s['bolum']; L+=["",f"## {cur}",""]
    L.append(f"- **{s['id']}** {s['alt']}  _({s['kaynak']})_"); chars+=len(s['tts'])
words=sum(len(s['alt'].split()) for s in segs)
L+=["",f"Cümle: {len(segs)} · kelime: {words} · tts karakter: {chars} · tahmini süre (İkaros: 594 kelime = 5:55): {words/594*355/60:.1f} dk · kredi: {chars} × 2 çekim ≈ {chars*2}"]
open('senaryo_okuma.md','w',encoding='utf-8').write("\n".join(L)+"\n")
print(len(segs),words,chars)

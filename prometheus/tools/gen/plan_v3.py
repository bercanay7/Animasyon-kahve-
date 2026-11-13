"""Plan listesi 3. sürüm: animatik kurulu tur 2 (yönetmen-Dram 8,82; izleyici-Tutma 8,76) bulguları.
animatik/planlar.json (2. sürüm) → animatik/planlar_v2.json (yedek) + animatik/planlar.json (3. sürüm).
Ses kurgusu da değişti (vo/plan.json): dört bölüm sonunda uzun nefes, J04'te 'köle'den sonra 0,8 sn duraklama."""
import json, os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = os.path.join(ROOT, 'animatik', 'planlar.json')
if not os.path.exists(os.path.join(ROOT, 'animatik', 'planlar_v2.json')): shutil.copy(src, os.path.join(ROOT, 'animatik', 'planlar_v2.json'))
d = json.load(open(os.path.join(ROOT, 'animatik', 'planlar_v2.json')))
P = d['planlar']
ix = lambda pid: next(i for i, x in enumerate(P) if x['id'] == pid)
def up(pid, **kw):
    x = P[ix(pid)]
    for k, v in kw.items():
        if v is None: x.pop(k, None)
        else: x[k] = v
def drop(*pids):
    for pid in pids: P.pop(ix(pid))
def after(pid, new): P.insert(ix(pid) + 1, new)

d['_not'] = d['_not'].replace('Plan listesi 2. sürüm (animatik kurulu 1. tur sonrası).', 'Plan listesi 3. sürüm (animatik kurulu tur 2 sonrası).')
d['_not'] += (" (11) Taban türevleri: KAYA/İÇSES (rüzgâr yok, büst ≥ 2 px/sn itilir, nefes, arka plan koyulaşır, kenardan tek tük kil tozu) iç ses planlarında; "
  "KAYA/DONMA (asılı toz ve kıvılcımda üç katman paralaks, kamera ≥ 3 px/sn, ateş titrer, nefes; rüzgâr, dalga ve müzik yok, yalnız ateş çıtırtısı; solgun kil paleti, ateş renkli) IX donmasında. "
  "(12) Ödemeler saklanır: üçüncü taht yalnız çatlar (P069–P070 çatlak, tek soluk düşüş P224); kaya yalnız I12@yıkılana'da yarılır.")
d['taban']['KAYA/İÇSES'] = 'rüzgâr yok; büst ≥ 2 px/sn itilir; nefes; arka plan sır siyahına koyulaşır; kenardan tek tük kil tozu kopar'
d['taban']['KAYA/DONMA'] = 'asılı toz ve kıvılcımda üç katman paralaks; kamera ≥ 3 px/sn; ateş titrer; nefes; rüzgâr, dalga ve müzik yok, yalnız ateş çıtırtısı; solgun kil, ateş renkli'

# --- açılış ---
up('P004', at='A01+4.8', kare="ZİNCİR: A01 bittikten sonra sessizlikte (≈5,6 sn) çekiç kazığa iner, bilekteki halka kapanır, 0,15 sn beyaz çakma; kamera geri çekilir: kayaya mıhlı Prometheus. İkinci vuruş A02@mıhlatan'da.")
up('P012', hareket="A06@tuhaf: P011'in ateşli harflerinden kopan kıvılcım sayfaya düşüp kalem ucu olur (sayfanın tek parlak noktası); A06@azra: kalem AZRA ERHAT'ı el yazısıyla yazar (≥ 76 px, y ≤ 700); A06@bin: kapağa 1967 damgası; A06@oyunun: kapak açılır, ÖNSÖZ sayfası; vinyet sayfanın sol kenarında sürer")
up('P015', hareket="A05@öfkelendiren: gökte soğuk şimşek titrer; A05@avuç: kamera aleve iner, alev nabız gibi atar; A05 bitince (sessizlikte) tek bir kıvılcım yükselir ve P016'da akşam yıldızı olur (eşleşen kesme)")
up('P016', hareket="eşleşen kesme: P015'in yükselen kıvılcımı tiyatronun üstündeki akşam yıldızı olur; bölüm levhası sallanarak iner; vinç hareketi; B01@insanı: tanrı maskeleri arasında tek insan maskesi meşale ışığıyla yanar")

# --- III: kâhinin gördüğü şey düşüş değil çatlak ---
up('P069', kare="Prometheus'un gözüne dalılır; göz bebeğinin siyahı bir tondoya açılır: tondoda Zeus'un tahtı yerinde durur; D09@kahin'de tahtın sağ ayağında ince bir altın çatlak yanar (≈1130,700).", hareket="göze dalış; tondo döner; D09@kahin'de çatlak yanar")
up('P070', hareket="D09@bilir'de aynı çatlak büyür (düşüş yok; düşüşün kendisi P224'e kalır)")

# --- IV ---
up('P103', hareket="E16@üçüncü'de insan figürü doğrulur; E16@insan'da gölgesi büyüyüp tahtı örter; taht yerinde, içi boş")

# --- V–VI: iç ses tabanı ---
for pid in ['P144', 'P145', 'P146', 'P147']: up(pid, taban=d['taban']['KAYA/İÇSES'])
up('P145', hareket="üç soluk siluet bakış çizgisi boyunca gökte soldan sağa süzülür (x 200–900, y 150–450): F14@önceden'de kartal, F14@apaçık'ta fırtına, F14@habersiz'de okçu")
up('P147', kare="Ağız animasyonu yok: F14@susabiliyorum'da ağızdan çıkan yazı yarım kalır, F14@konuşabiliyorum'da rüzgârsız havada asılı kalır (~1,4 sn, uzayan sessizlikte) ve dağılır; rüzgâr VI levhasıyla birlikte geri gelir.")
up('P155', kare="Kırmızı figür hatıra tondosu: Titanlar sırtlarını döner; Prometheus sağda boş bir tahtın uzun gölgesine doğru yürür ve gölgenin içine girer (x 1100–1500, y 300–700); Zeus yalnız gölge.")
up('P183b', hareket="figürün kil kenarları rüzgârda toz olup kopar ('eriyip gitmek' rüzgârla verilir); nefes")
up('P184', taban=d['taban']['KAYA/İÇSES'], hareket="G13b@yani'de rüzgâr kesilir; G13b@yaşamak'ta soluk görüntüler dolar; büst itmesi")
up('P185', hareket="G13b@yine'de rüzgâr geri gelir; ayak rüzgâra karşı ileri basar, zincir gerilir, kazıktan toz dökülür; gerilme döngüsü uzayan sessizlikte tamamlanır")

# --- VII ---
up('P208', hareket="H09@yıkılmadıkça boş tahtın çatlağı ilerler")

# --- VIII: Hermes sorgusu ve TAHT ---
up('P223', k='K', kit='TAHT', set='TAHT (K)', gecis='sır 0,6 sn (çapada biter)', kare="TAHT nesnesinin kırmızı figür türevi (çatlak, titrek; üç sabit taht x 560/960/1360): Prometheus'un alayının görüntüsü.", hareket="I06@iki'de Uranos ve Kronos tahtları soluk bir görüntü olarak devrilir; I06@üçüncüsünün'de Zeus'un tahtı titrer")
up('P224', k='K', kit='TAHT', set='TAHT (K)', gecis=None, kare="Aynı kompozisyon: üçüncü tahtın düşüşü yalnız bir görüntü olarak, soluk (filmde üçüncü tahtın tek düşüşü); I06@çabuk'ta görüntü söner, taht yerinde kalır.", hareket="I06@düşüşünü'de soluk düşüş görüntüsü; I06@çabuk'ta söner")
up('P225', gecis='sert kesme')
up('P228', hareket="0,7 sn rüzgâr kesilir; figürün kenarından toz kopar; tek bir zincir halkası sarsılır; 0,1 sn beyaz çakma")
up('P232', kare="Hermes geri çekilir, kerykeion'unu yeniden kaldırmaya başlar, çizmelerindeki kanatlar çırpar; yukarıda boş tahtın gözleri kısılır. Bu hareket J01@durduralım'da yarıda kalacak.", hareket="kanatlar çırpar; kerykeion kalkar; taht gözleri kısılır")

# --- IX: donma ve doruk ---
for pid in ['P233', 'P234', 'P235', 'P236', 'P237', 'P238', 'P239', 'P240', 'P242', 'P243', 'P244', 'P245']:
    if pid in [x['id'] for x in P]: up(pid, taban=d['taban']['KAYA/DONMA'])
up('P233', kare="Sorgu sürerken bölüm levhası iner; J01@durduralım'da her şey hareketin ortasında DONAR: Hermes havada (x 1250–1550, y 200–620), kerykeion yarı kalkık, çizme kanatları yarım açık, toz ve kıvılcımlar asılı; solgun kil, yalnız ateş renkli; müzik ve rüzgâr kesilir, yalnız ateş çıtırtısı. Kamera paralaksla Hermes ile Prometheus'un arasından geçer; J01@asıl'da bileğe itmeye başlar.")
up('P235', hareket="J02@zincirde: J01@asıl'dan beri süren itiş kelepçeye varır; J02@özgürlüğü: kelepçenin kilidi Prometheus tarafında parlar; J02@yok: asılı bir kıvılcım kilide düşüp söner (P241'in kurulumu)")
up('P237', kare="AÇILIM (tek kesintisiz plan, çözülme yok): kamera dikey dünyada zinciri bulutlardan yukarı izler; J04@verir'de bulutlar aralanmaya başlar, J04@gerçekte'de açılır; J04@zeus'ta tahtın kolu ve buluttan uzanan tek bilek kadraja girer (bilek ≈ 960,400): zincir soğuk beyaz kelepçede biter, yüz ve gövde yok; J04@köle'de ZEUS · KÖLE etiketi (y≈220) mühür gibi basılır, kelepçe parlar (P005'in pırıltısı); 'köle'den sonraki 1,2 sn'lik duraklamada kare durur, nefes alır. J04@prometeus'ta kesme yok: kamera altın ışıkla birlikte zincir boyunca hızla aşağı iner (~0,6 sn).", yazi='ZEUS · KÖLE (J04@köle; üst bantta J05@uşaklarına\'ya kadar kalır)')
up('P238', at='J04@özgürdür', gecis=None, kare="Kamera Prometheus'a varır; zincir boyunca altın ışık akar, duruşu özgür. PROMETHEUS · ÖZGÜR (y≈420); ZEUS · KÖLE üst kenarda soluk kalır (y 160–220); iki etiket J05@uşaklarına'da birlikte söner.", yazi='PROMETHEUS · ÖZGÜR (y≈420); köşede ERHAT · s. xiv')

# --- X ---
up('P246', kare="I08b@sorguya'da donmuş kare çözülür: renk tümüyle geri gelir, parçacıklar düşer, Hermes yarım kalan hareketini tamamlar; I08b@savurur'da tehdidini savurur; yıldırımın kayayı yarması yalnız bir görüntü olarak (kurulum).")
up('P249', hareket="sarmal iniş (KAYA ÜST kamerası); I08b@çağrılmamış'ta pençe silueti; I08b@ziyafet'te kartal gölgesi gövdeyi örter")
up('P255', kare="P142'nin (F13'ün toprak kadrajı) sarsılmış hâli: I10@gerçekte'de ilk şimşek (2 kare), I10@yer'de toprak kabarır, taşlar düşer (yarılma yok: ödeme I12@yıkılana'ya saklı).")
up('P259', taban=d['taban']['KAYA/İÇSES'])
up('P260', kare="Kaya yalnız titrer; son söz harfleri ağızdan göğe yükselir, I11@adalet'te beliren ΘΕΜΙΣ madalyonuna doğru (x 900–1400, y 120–420): 'anasına' sözü görüntüde de karşılanır.", yazi='“Görüyor musun, haksız yere neler çekiyorum.”')
up('P261', kare="Kayada: I12@yıkılana'da kaya ilk ve tek kez yarılır, I12@gömülene'de Prometheus ve perilerle birlikte kapanır, I12@konuşmakta'da yazı çatlaktan parlar; susan → konuşan panoları yalnız kenar şeridinde (x 1500–1880, y 60–300).")
up('P263', kare="Havadaki harfler sayfadaki alıntıya dönüşür (tam sayfa alıntı); I12@özgür'de 'özgür' kelimesi ateş rengiyle parlar. I12 bittikten sonra en az 2,8 sn: mürekkep sayfadan geri çekilir, yalnız 'özgür' yanar (x 700–1220, y 380–520); son 0,8 sn'de harfler kıvılcım olup fırlar ve P264'teki ok ucuna bağlanır.")

# --- XII ---
up('P275', hareket="K08a@sorusu'nda önceki planlardaki (P109, P157, P216) iğneli küçük NASIL? kartı iğnesinden kopar ve kadrajı doldurur; K08a@nasıl'da eşleşen kesmeyle P276'nın NASIL? yazısına dönüşür (yeniden yazılmaz)")
up('P276', yazi='NASIL? (P275\'ten eşleşen kesme; yeniden yazılmaz)')
up('P277', k='K', kit='TİYATRO', set='TİYATRO', gecis='sert kesme', kare="Tek kesintisiz kırmızı figür tiyatro planı (P277–P278, P016/P107 seti): K08a@taht'ta skene frizinde taht kavgası, ortada Prometheus; K08a@siyasi'de Erhat'ın kalemi figürü daire içine alır (P048'in eşi).", hareket="vinç; friz figürleri; daire çizilir")
up('P278', k='K', kit='TİYATRO', set='TİYATRO', gecis=None, kare="Aynı plan sürer: K08a@politik'te kamera skeneden Atinalı kalabalığa döner; K08a@ayshilostu'da kandil ışığında ΑΙΣΧΥΛΟΣ yazısı yanar.", yazi='kenar şeridi: “politik görüşü en köklü” · s. vi', hareket="kamera kalabalığa döner; kandil; yazı yanar")
up('P279', gecis='mürekkep 0,5 sn (çapada biter)', kare="Sayfada terazi: kaba güç (çomak) ile akıl (kıvılcım); akıl ağır basar. Sayfada kısa etiket: AKIL GÜCÜ · KABA GÜÇ (tırnaklı alıntı kartı yok: notlarda bu cümle Erhat'ın tırnaklı sözü olarak geçmiyor).", yazi='AKIL GÜCÜ · KABA GÜÇ')
up('P280', k='K', kit='KAYA', set='KAYA/ORTA', gecis='sert kesme', kare="KAYA ORTA: üslup karesindeki zincirli figür; K08c@sanık'ta siluet bir an aynı duruşta modern bir insan siluetine döner ve geri gelir (yirmi beş yüzyıl önceki sanık hâlâ insana benziyor).", hareket="siluet dönüşümü; rüzgâr")
up('P281', gecis='mürekkep 0,6 sn (çapada biter)')
# P288 ikiye bölünür
i = ix('P288'); p288 = P[i]
P[i] = {'id': 'P288a', 'at': 'K06@ve', 'k': 'B', 'kit': 'SAYFA', 'set': 'SAYFA', 'kare': "Sayfa yolculuğu sürer (geçiş yok): tam sayfa alıntı; küçük figürün ateşi kapanan kitabın kapağındaki PROMETHEUS harflerini tutuşturur.", 'hareket': 'kitap kapanır; harfler tutuşur', 'yazi': p288.get('yazi')}
P.insert(i + 1, {'id': 'P288b', 'at': 'K06@prometeustur', 'k': 'K', 'kit': 'KAYA', 'set': 'BAŞLIK', 'kare': "Eşleşen kesme: kapaktaki ateşli harfler P011'in harflerine geçer; kamera geri çekilince zincirli siluet görünür; sessizlikte tek bir kıvılcım P289'un lambasına iner.", 'hareket': 'geri çekilme; kıvılcım', 'gecis': 'eşleşen kesme'})

# --- XIII ---
up('P289', gecis="eşleşen kesme: P288b'nin kıvılcımı → lambanın alevi")
up('P291', gecis='sır 0,6 sn (çapada biter)')
up('P292', kare="KAPAK KARESİNİN SON KULLANIMI (el yok): M02@olsan'da Prometheus alevi kameraya uzatır; M02@ateşi'de alev objektife yaklaşır ve kareyi altınla doldurur (merkez 960,420): izleyici ateşi alan kişi olur; M02@yorumlarda'da alev küçülüp bitiş ekranının alevine bağlanır.", hareket="alev yaklaşır; altın; küçülür")

# taban ve çekim numaraları yeniden
for x in P:
    if 'taban' not in x or x['taban'] in d['taban'].values() and x['taban'] not in (d['taban']['KAYA/İÇSES'], d['taban']['KAYA/DONMA']): x['taban'] = d['taban'].get(x['kit'], '')
cek, prev = 0, None
for x in P:
    key = (x['kit'], x['k'])
    if prev is None or key != prev or (x.get('gecis') and 'levha' in x['gecis']): cek += 1
    x['cekim'] = f'Ç{cek:03d}'; prev = key
d['planlar'] = P
json.dump(d, open(src, 'w'), ensure_ascii=False, indent=1)
print(len(P), 'plan,', cek, 'çekim')

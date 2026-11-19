# Narkissos ve Eko → narsisizm: geriye bakış (19 Kasım 2026)

- **Sonuç:** 8:52, vazo üslubu, 98 plan. 1920×1080, mb=4; render 56,9 dk (4 işçi). Yükleme kopyası H.265 CRF 26, 57 MB.
- **Kredi:**
  - seslendirme 13.760 (9 bölüm × 2 çekim, eleven_v4);
  - Scribe denetimi 1.231.
- **Kullanım:** bu video kanalın en pahalısı oldu. Nedenleri:
  - üslup araştırmasında 17 ajan;
  - kapı, düzeltme ve animatik turları;
  - her turda Fable denetimi.

  Kullanıcının kararı (19 Kasım): bundan sonra kurul yok, puanlama yok, çok ajanlı akış yok; başkan tek başına yapar.

**Dersler:**
1. **Hizalama cümle düzeyinde yapılır.** `hizala.py` yalnız bölüm içindeki kimlik sınırlarını sessizliğe oturtuyordu; 27 cümle bir iki cümle kaydı (F11 9,6 sn yerine 4,9). `tools/hizala_cumle.py` her cümleyi sessizliğe oturtuyor; sonuç Scribe'ın kelime zamanlarıyla tuttu. Planlar çapalara bağlı olduğu için yeniden hizalama planları kendiliğinden kaydırdı.
2. **Scribe en riskli bölümde değerlidir.** Son bölümün ilk çekimi "devam edelim"i "devam ederim" okuyordu; ikinci çekim seçildi.
3. **Kör okuma görüntüdeki tehlikeleri yakaladı:**
   - tepeden çekilen uzanmış figür secde okundu;
   - telefondaki ters yansıma ikinci kişi ve öpüşme okundu;
   - kil zemindeki siyah figür ve kırmızı bant blackface okundu;
   - tek kol ve yumruk siyasi selam okundu.

   Hepsi düzeltildi.
4. **Kaynakta olmayan söz yazılmaz:** bir set sahibi Eko'ya "Biri beni duysun" yazmıştı; kaldırıldı.
5. **Hazır motor ve kapı:** vazo, risografa karşı aynı sahneyle sınandı. Belirleyici çıkanlar:
   - figürün çalışması;
   - kapağın 168 px'te okunması;
   - risografın 9,6 kat büyük dosyası.
6. **Kredi onayı:** ilk ElevenLabs çağrısını otomatik denetleyici durdurdu. Kullanıcı genel onay verince ("ne istiyorsan onaylıyorum") geçti.

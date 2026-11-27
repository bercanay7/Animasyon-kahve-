# Teknik notlar ve tuzaklar (projeye özel)

CLAUDE.md'den taşındı (27 Kasım 2026). Bir motoru ya da aracı yeniden kullanırken okunur. Her videoda geçerli olanlar CLAUDE.md "Teknik notlar"da kaldı.

- **Piyano sentezi:** MIDI < ~37'de sönüm katsayısı negatife düşüyordu; düzeltme `dec = max(.3, …)` (`dorian-gray/audio/score.py`).
- **milton motoru:** iç içe `GR.frame` göreli değil, mutlak koordinata döner.
- **Karma üslupta renk katmanı örtüyle basılır.** Çarpma boyası katman sırası bilmez; önünden geçen figürü de boyar (`lale-cilginligi/lib/lale.js` örtü maskesi).
- **Kapta paket eksikse:** Whisper ve scipy olmadan çalışan yollar `ikaros/tools/hizala.py`, `ikaros/audio/dsp_shim.py`, `ikaros/tools/mix_ffmpeg.py`.
- **Dosya boyu:** ağaç baskı gibi karede değişen gürültü dosyayı şişirir; gürültü iki karede bir değiştirilir.
- **Yazılımsal WebGL (SwiftShader):** önce ölç, sonra hızlandır.
  - Konuma bağlı gürültü dokuya önceden yazılır.
  - Canvas `filter: blur` pahalıdır; düşük çözünürlüklü tuvale çizilip büyütülür.
  - Sessiz film 15 kare/sn.
- **Render önbelleği:** `.parts*/` kod ve ayar özetini (`KEY`) saklar; şüphede klasör elle silinir.

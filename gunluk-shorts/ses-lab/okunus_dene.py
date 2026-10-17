"""Bir ifadenin seçilen seste nasıl duyulduğunu dener: aynı ifade 6 kez sentezlenir, Whisper-medium her seferinde ne yazdığını gösterir.
Kullanım:  python3 okunus_dene.py fahrettin "Doktor_Goldberger," "pellagra=pelagıra denen" "*tabaktaydı=tabakta_idi.*"
Jeton işareti narrator.py ile aynı (gösterilen=söylenen, _ = boşluk, *vurgu*). Yalnız ilk ifade parçası (ilk virgül/noktaya kadar) denenir.
Profil, Shorts anlatıcısının profilidir (pellagra-mikrop-degildi/tts.py PROF); orada değişirse burada da değiştir.
Sonuç yorumu: 6 dinlemenin ≥5'i doğruysa söylenen biçim güvenlidir; 3–4 ise en-iyi-K seçimi kurtarır; ≤2 ise yazılışı değiştir."""
import sys
import numpy as np
import narrator, asr

PROF = dict(narrator.PROFILE)
PROF.update(speed=0.96, reverb_wet=0.0, gap_comma=0.22, gap_colon=0.30)
N = 6

if __name__ == "__main__":
    voice, phrases = sys.argv[1], sys.argv[2:]
    tts = narrator.load_tts(voice, PROF)
    for phrase in phrases:
        ch = narrator.chunks_of(narrator.parse(phrase))[0]
        heard = []
        for _ in range(N):
            y = narrator.synth_chunk(tts, ch, PROF["speed"], PROF["pitch"], PROF, 1.05)
            z = y / (np.max(np.abs(y)) + 1e-9) * 0.5
            z = np.concatenate([np.zeros(int(0.25 * narrator.SR)), z, np.zeros(int(0.45 * narrator.SR))])
            heard.append(asr.transcribe(z, narrator.SR))
        print(f"{phrase}  →  " + " | ".join(heard))

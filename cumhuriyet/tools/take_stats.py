"""Take karşılaştırma: süre, perde değişkenliği (ifade), en uzun sessizlik, kırpılma, ani gürültü."""
import sys, librosa, numpy as np
for p in sys.argv[1:]:
    y, sr = librosa.load(p, sr=22050)
    f0, v, _ = librosa.pyin(y, fmin=55, fmax=300, sr=sr, frame_length=1024)
    st = 12 * np.log2(f0[~np.isnan(f0)] / 100)
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
    sil = rms < np.percentile(rms, 15) * 1.8
    longest, cur = 0, 0
    for s in sil:
        cur = cur + 1 if s else 0; longest = max(longest, cur)
    flat = librosa.feature.spectral_flatness(y=y)[0]
    print(f'{p}: {len(y)/sr:5.1f}s  pitchSD {np.std(st):.2f}st  medF0 {np.nanmedian(f0):.0f}Hz  maxSil {longest*256/sr:.2f}s  peak {np.abs(y).max():.2f}  flat>0.3 {np.mean(flat>0.3)*100:.1f}%')

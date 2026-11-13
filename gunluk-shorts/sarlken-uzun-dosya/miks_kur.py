#!/usr/bin/env python3
"""
miks_kur.py — TEK KOMUTLA ses hattını baştan kurar (müzik + SFX + miks + ölçüm raporu).

    python3 miks_kur.py                 # tam üretim
    python3 miks_kur.py --preview       # + out/audio_prev/ (cue ve SFX kesitleri, miks kesitleri)
    python3 miks_kur.py --fresh         # müzik önbelleğini yok say (varsayılan: bölüm geometrisi/kod değişince otomatik yeniler)

Girdiler (hepsi kayıt edilmiş çıktılar; voice yamalandığında bu komut yeniden çalıştırılır):
    out/voice.wav            anlatım kanalı (mono, 48 kHz)
    out/voice_chapters.json  bölüm t0/t1/gap_after ve toplam süre  → müzik cue sınırları, çapraz geçişler, başlık vuruşu,
                             bölüm kartı stinger'ları ve kapanış sönümü BU dosyadan yeniden hesaplanır
    out/timeline.json        cümle/sözcük zamanları (QA: voice ile uyum raporu)
    out/sfx_cues.json        (isteğe bağlı) yoksa varsayılan: c0 sonunda title_hit + her bölüm kartında chapter_stinger

Çıktılar: out/music.wav, out/sfx_bus.wav, out/mix_audio.wav, out/mix_audio.m4a, out/audio_report.txt
          (+ --preview ile out/audio_prev/*.wav)
"""
import json
import os
import sys
import time
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "out")


def kontrol():
    """Girdi tutarlılığı: dosyalar var mı, voice süresi = bölüm toplamı mı, bölümler sırayla bitişik mi."""
    hatalar, uyarilar = [], []
    for f in ("voice.wav", "voice_chapters.json"):
        if not os.path.exists(os.path.join(OUT, f)):
            hatalar.append(f"eksik girdi: out/{f}")
    if hatalar:
        return hatalar, uyarilar, None
    meta = json.load(open(os.path.join(OUT, "voice_chapters.json")))
    chs = meta["chapters"]
    with wave.open(os.path.join(OUT, "voice.wav")) as w:
        wav_sn = w.getnframes() / w.getframerate()
        sr = w.getframerate()
    if sr != 48000:
        hatalar.append(f"voice.wav örnekleme {sr} Hz (48000 bekleniyor)")
    if abs(wav_sn - meta["total"]) > 0.02:
        hatalar.append(f"voice.wav süresi {wav_sn:.3f} sn ≠ voice_chapters.json total {meta['total']:.3f} sn — önce ses birleştirmeyi yeniden çalıştırın")
    for a, b in zip(chs[:-1], chs[1:]):
        if abs(a["t1"] + a.get("gap_after", 3.0) - b["t0"]) > 0.05:
            uyarilar.append(f"{a['id']}→{b['id']}: t1+gap ({a['t1'] + a.get('gap_after', 3.0):.2f}) ≠ sonraki t0 ({b['t0']:.2f})")
    if abs(chs[-1]["t1"] - meta["total"]) > 0.05:
        uyarilar.append(f"son bölüm t1 ({chs[-1]['t1']:.2f}) ≠ total ({meta['total']:.2f})")
    tp = os.path.join(OUT, "timeline.json")
    if os.path.exists(tp):
        tl = json.load(open(tp))
        if abs(tl.get("total", 0) - meta["total"]) > 0.05:
            uyarilar.append(f"timeline.json total {tl.get('total')} ≠ voice_chapters.json total {meta['total']}")
        if os.path.getmtime(tp) < os.path.getmtime(os.path.join(OUT, "voice.wav")) - 5:
            uyarilar.append("timeline.json, voice.wav'dan eski görünüyor (zaman çizelgesi güncel mi?)")
    else:
        uyarilar.append("out/timeline.json yok (yalnızca QA'da kullanılır)")
    sp = os.path.join(OUT, "sfx_cues.json")
    if os.path.exists(sp) and os.path.getmtime(sp) < os.path.getmtime(os.path.join(OUT, "voice_chapters.json")) - 5:
        uyarilar.append("out/sfx_cues.json, voice_chapters.json'dan eski: SFX zamanları eski ses eksenine göre olabilir")
    return hatalar, uyarilar, meta


def main():
    t0 = time.time()
    hatalar, uyarilar, meta = kontrol()
    for u in uyarilar:
        print("UYARI:", u)
    if hatalar:
        for h in hatalar:
            print("HATA:", h)
        sys.exit(2)
    print(f"girdiler tamam: {len(meta['chapters'])} bölüm, toplam {meta['total']:.3f} sn → mix = toplam + kapanış (varsayılan 7 sn)")
    import miks
    sys.argv = ["miks.py"] + sys.argv[1:]
    miks.main()
    ciktilar = ["music.wav", "sfx_bus.wav", "mix_audio.wav", "mix_audio.m4a", "audio_report.txt"]
    print("\nçıktılar:")
    for c in ciktilar:
        p = os.path.join(OUT, c)
        print(f"  out/{c:18s} {'var' if os.path.exists(p) else 'YOK'}  {os.path.getsize(p) / 1e6 if os.path.exists(p) else 0:8.1f} MB")
    print(f"toplam: {time.time() - t0:.0f} sn")


if __name__ == "__main__":
    main()

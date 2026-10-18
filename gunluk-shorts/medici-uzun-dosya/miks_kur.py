#!/usr/bin/env python3
"""
miks_kur.py — TEK KOMUTLA bir PARÇANIN ses hattını baştan kurar (müzik + SFX + miks + ölçüm raporu). MEDICI_PART zorunludur.

    MEDICI_PART=2 python3 miks_kur.py                  # final miks → out_p2/mix_audio.m4a (+ stem'ler); geçici ses varsa DURUR
    MEDICI_PART=2 python3 miks_kur.py --onizleme       # geçici (Piper) ses ya da eksik bölüm: ONIZLEME_ önekiyle; final adıyla YAZILMAZ
    MEDICI_PART=2 python3 miks_kur.py --onizleme --preview      # + out_p2/ses_onizleme/*.mp3 (20–30 sn kesitler)
    MEDICI_PART=2 python3 miks_kur.py --kontrol        # yalnız girdi tutarlılığı denetimi
    MEDICI_PART=2 python3 miks_kur.py --gecis-sesleri  # önce görüntü motorundan (compose.Program) geçişleri okuyup out_p2/sfx_gecis.json üretir, sonra miks
    MEDICI_PART=2 python3 miks_kur.py --sadece-gecis   # yalnız out_p2/sfx_gecis.json üret
    (--fresh: müzik önbelleğini yok say · --snr 20,24: konuşma−müzik penceresi · --workers N: en çok 2 · --no-gecis / --no-stinger · --no-stems)

`out/` sembolik bağlantısı ve parca.kullan() KULLANILMAZ; tüm yollar out_pN altındadır (MEDICI_PART).

Girdiler (voice yamalandığında/ElevenLabs gerçek sesi gelince bu komut yeniden çalıştırılır; müzik çıpaları cümle kimliklerinden YENİDEN çözülür):
    out_pN/voice.wav            anlatım kanalı (mono, 48 kHz)
    out_pN/voice_chapters.json  bölüm t0/t1/gap_after ve toplam süre
    out_pN/timeline.json        cümle/sözcük zamanları (müzik/SFX çıpaları + QA)
    sfx_cues_pN.json            (proje kökü) SFX kuyruğu — sözleşme: sfx.py / notlar_ses.md
    out_pN/sfx_gecis.json       (isteğe bağlı) otomatik geçiş sesleri
Çıktılar: out_pN/[ONIZLEME_]mix_audio.m4a, [ONIZLEME_]stem_music|voice|sfx.flac, [ONIZLEME_]sfx_cues_used.json, [ONIZLEME_]audio_report.txt
          (+ --preview ile out_pN/ses_onizleme/*.mp3)
"""
import json
import os
import sys
import time
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parca as PA  # noqa: E402

PART = PA.PART
OUT = PA.OUT


def kontrol():
    """Girdi tutarlılığı: dosyalar var mı, voice süresi = bölüm toplamı mı, bölümler sırayla bitişik mi, parça tam mı, ses geçici mi."""
    hatalar, uyarilar = [], []
    for f in ("voice.wav", "voice_chapters.json"):
        if not os.path.exists(os.path.join(OUT, f)):
            hatalar.append(f"eksik girdi: out_p{PART}/{f}")
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
    try:
        import script as S
        beklenen = list(S.PARTS[PART])
    except Exception:   # noqa
        beklenen = [f"c{i}" for i in {1: range(0, 7), 2: range(7, 12), 3: range(12, 17)}[PART]]
    eksik = [c for c in beklenen if c not in [x["id"] for x in chs]]
    if eksik:
        uyarilar.append(f"KISMİ PARÇA: eksik bölüm {eksik} — yalnız --onizleme ile miks edilebilir")
    if os.path.exists(os.path.join(OUT, "GECICI_SES.json")):
        g = json.load(open(os.path.join(OUT, "GECICI_SES.json"))).get("chapters")
        uyarilar.append(f"GEÇİCİ (Piper) anlatım var {g} — yalnız --onizleme ile miks edilebilir (final adıyla yazılmaz)")
    tp = os.path.join(OUT, "timeline.json")
    if os.path.exists(tp):
        tl = json.load(open(tp))
        if abs(tl.get("total", 0) - meta["total"]) > 0.05:
            uyarilar.append(f"timeline.json total {tl.get('total')} ≠ voice_chapters.json total {meta['total']}")
        if os.path.getmtime(tp) < os.path.getmtime(os.path.join(OUT, "voice.wav")) - 5:
            uyarilar.append("timeline.json, voice.wav'dan eski görünüyor (zaman çizelgesi güncel mi?)")
    else:
        uyarilar.append("timeline.json yok: müzik/SFX çıpaları varsayılan konumlara düşer, QA zayıflar")
    sp = os.path.join(HERE, f"sfx_cues_p{PART}.json")
    if not os.path.exists(sp):
        uyarilar.append(f"sfx_cues_p{PART}.json yok: yalnız başlık/kart vurguları (+varsa otomatik geçiş sesleri)")
    elif os.path.getmtime(sp) < os.path.getmtime(os.path.join(OUT, "voice_chapters.json")) - 5:
        uyarilar.append(f"sfx_cues_p{PART}.json, voice_chapters.json'dan eski: mutlak 't' kullanan cue'lar eski ses eksenine göre olabilir (çapalı olanlar yeniden çözülür)")
    return hatalar, uyarilar, meta


def gecis_cikar():
    """Görüntü motorundan (compose.Program) parça çekim listesini ve geçişleri okur → out_pN/sfx_gecis.json (otomatik geçiş sesleri).
    Motora DOKUNMAZ; yalnız okur. timeline out_pN/timeline.json'dan (out/ bağlantısı kullanılmaz). Motor yüklenemezse nazikçe atlar."""
    try:
        import shots as SH
        SH.TL = SH.Timeline(os.path.join(OUT, "timeline.json"))
        import compose
        prog = compose.Program(part=PART)
    except Exception as e:   # noqa
        print(f"UYARI: görüntü motoru yüklenemedi / Program kurulamadı → otomatik geçiş sesleri üretilmedi ({type(e).__name__}: {e})")
        return None
    import muzik
    import sfx
    meta = json.load(open(os.path.join(OUT, "voice_chapters.json")))
    tl = json.load(open(os.path.join(OUT, "timeline.json")))
    gates = muzik.gate_windows(meta["chapters"], float(meta["total"]), 7.0, tl)
    quiet = [(g["a"], g["b"]) for g in gates if g["floor_db"] is None or g["floor_db"] <= -24]
    spans = [(c["id"], c["t0"], c["t1"]) for c in meta["chapters"]]

    def chapter_of(t):
        for cid, a, b in spans:
            if a - 0.01 <= t <= b + 0.01:
                return cid
        return None
    cues = sfx.transition_cues(sfx.shots_from_program(prog), quiet_zones=quiet, chapter_of=chapter_of)
    hints = sfx.sfx_hints_from_program(prog)          # çekimlerde sfx= ipucu varsa (ileride)
    p = os.path.join(OUT, "sfx_gecis.json")
    json.dump(dict(surum=1, parca=PART, uretim="miks_kur.py --gecis-sesleri (compose.Program geçişlerinden)", cues=cues + hints), open(p, "w"), indent=1, ensure_ascii=False)
    from collections import Counter
    print(f"otomatik geçiş sesleri: {len(cues)} cue (+ {len(hints)} çekim ipucu) → {p}; geçişler: {dict(Counter(c['note'].split(chr(39))[1] for c in cues))}")
    return p


def main():
    t0 = time.time()
    if PART is None:
        raise SystemExit("MEDICI_PART=1|2|3 gerekli (örn. MEDICI_PART=2 python3 miks_kur.py); out/ sembolik bağlantısı KULLANILMAZ.")
    args = sys.argv[1:]
    only_check = "--kontrol" in args
    gecis = "--gecis-sesleri" in args or "--sadece-gecis" in args
    only_gecis = "--sadece-gecis" in args
    for k in ("--kontrol", "--gecis-sesleri", "--sadece-gecis"):
        if k in args:
            args.remove(k)
    hatalar, uyarilar, meta = kontrol()
    for u in uyarilar:
        print("UYARI:", u)
    if hatalar:
        for h in hatalar:
            print("HATA:", h)
        sys.exit(2)
    print(f"P{PART}: girdiler tamam: {len(meta['chapters'])} bölüm, toplam {meta['total']:.3f} sn → mix = toplam + bitiş ekranı (varsayılan 7 sn)")
    if only_check:
        return
    if gecis:
        gecis_cikar()
        if only_gecis:
            return
    import miks
    sys.argv = ["miks.py"] + args
    miks.main()
    on = "ONIZLEME_" if ("--onizleme" in args or any("GECICI" in u or "KISMİ" in u for u in uyarilar)) else ""
    ciktilar = [f"{on}mix_audio.m4a", f"{on}stem_music.flac", f"{on}stem_voice.flac", f"{on}stem_sfx.flac", f"{on}sfx_cues_used.json", f"{on}audio_report.txt"]
    print("\nçıktılar:")
    for c in ciktilar:
        p = os.path.join(OUT, c)
        print(f"  out_p{PART}/{c:34s} {'var' if os.path.exists(p) else 'YOK'}  {os.path.getsize(p) / 1e6 if os.path.exists(p) else 0:8.1f} MB")
    print(f"toplam: {time.time() - t0:.0f} sn")


if __name__ == "__main__":
    main()

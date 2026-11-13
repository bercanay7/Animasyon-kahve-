"""En iyi-K sentez: her ifade (virgül/nokta arası parça) K kez sentezlenir, Whisper'ın en doğru yazıya döktüğü seçilir.
Kullanım: python3 tts_best.py [K]   (tts.py ile aynı metin/profil; çıktı out/voice.wav + out/timeline.json)
  · K kez denendikten sonra en iyi aday hâlâ kötüyse (WER ≥ 0,3 ya da zor sözcük duyulmadıysa) KMAX'a (ortam değişkeni, vars. 15) kadar sürdürülür.
  · Seçilen her parça out/_chunk_cache/ altında saklanır (git'e girmez): metni değiştirince yalnız değişen parçalar yeniden sentezlenir.
    Belirli parçaları yeniden denemek için:  RETRY="Dışkı yuttular|Goldberger" python3 tts_best.py 5   (eşleşen parçalar önbellekten atlanır, KRETRY'ye kadar denenir)"""
import sys, os, json, re, difflib, hashlib
import numpy as np
from scipy.signal import butter, sosfilt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ses-lab"))
import narrator, asr
import tts as T

K = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 4
ORIG = narrator.synth_chunk
LOG = []


def _norm(s):
    s = s.replace("’", "").replace("'", "")
    s = re.sub(r"\b[Dd]r\.?\s*(?=[A-ZÇĞİÖŞÜ])", "doktor ", s)      # Whisper "Doktor" yerine "Dr." yazar
    return re.sub(r"\b[Dd]r\.?(?=\s)", "doktor", s)


# Zor sözcükler (fahrettin sesi): Whisper'ın bunu duyması ŞART, duymayan aday elenir.
# Anahtar = gösterilen yazılış (küçük harf); değer = kabul edilen duyuşların (bitişik, boşluksuz) kalıbı.
MUST = {
    "goldberger": re.compile(r"^gol[dt]b[eöi]r[gk][eıi]r$"),        # 'Boldberger', 'Coldberger' kabul edilmez
    "pellagra": re.compile(r"^pe+l+a+g[ıi]?ra$"),                    # 'pelabre', 'pelabe' kabul edilmez
    "mikrop": re.compile(r"^mikrop$"),                               # 'mikrofon' kabul edilmez
    "tabaktaydı": re.compile(r"^tabakta(ydı|ydi|idi|ıdı)$"),         # 'tabartaydı', 'tabahtaydı' kabul edilmez
    "eksikliğiydi": re.compile(r"^eksikli[ğg]?i+[yi]?di$"),          # 'eksik iyiydi' kabul edilmez
}


def heard(hyp_words, key):
    n = len(hyp_words)
    return any(MUST[key].match("".join(hyp_words[i:i + L])) for i in range(n) for L in (1, 2) if i + L <= n)


def must_keys(toks):
    return [w for t in toks for w in asr.norm(_norm(t["show"])) if w in MUST]


def must_miss(toks, hyp):
    """Parçadaki zor sözcüklerden Whisper'ın duymadıkları (liste)."""
    hw = asr.norm(_norm(hyp))
    return [k for k in must_keys(toks) if not heard(hw, k)]


def wer_wild(ref, hyp):
    """ref: [(kelime, joker?)]; joker (yabancı ad / sayı) 0–6 sözcüğü bedelsiz karşılar. Joker olmayan kelimeye göre oranlar."""
    n, m = len(ref), len(hyp)
    INF = 1e9
    d = [[INF] * (m + 1) for _ in range(n + 1)]
    d[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            v = d[i][j]
            if v >= INF:
                continue
            if i < n:
                w, wild = ref[i]
                d[i + 1][j] = min(d[i + 1][j], v + (0 if wild else 1))
                if j < m:
                    d[i + 1][j + 1] = min(d[i + 1][j + 1], v + (0 if (wild or hyp[j] == w) else 1))
                    if wild:
                        for k in range(2, 7):
                            if j + k <= m:
                                d[i + 1][j + k] = min(d[i + 1][j + k], v)
            if j < m:
                d[i][j + 1] = min(d[i][j + 1], v + 1)
    return d[n][m] / max(1, sum(1 for _, wl in ref if not wl))


def _shape(y, toks, prof, energy):
    """narrator.render'daki vurgu işlemenin aynısı (kazanç + parlaklık): Whisper karışımdaki sesin aynısını duysun
    (vurgulu 'pellagra' / 'tabaktaydı' ham sentezde doğru, vurgu parlaklığından sonra yanlış duyuluyordu)."""
    SR = narrator.SR
    w = np.array([narrator.syl(x["say"]) for x in toks], float)
    edges = np.concatenate([[0], np.cumsum(w)]) / w.sum()
    env_g, bright = np.ones(len(y)), np.zeros(len(y))
    for j, wd in enumerate(toks):
        a0, a1 = int(edges[j] * len(y)), int(edges[j + 1] * len(y))
        if wd["emph"]:
            g = 10 ** (prof["emph_gain_db"] / 20)
            ramp = np.minimum(1, np.minimum(np.arange(a1 - a0), np.arange(a1 - a0)[::-1]) / (0.03 * SR))
            env_g[a0:a1] = 1 + (g - 1) * ramp
            bright[a0:a1] = ramp
    if "!" in toks[-1]["punct"]:
        env_g *= 10 ** (prof["excl_boost_db"] / 20)
    hi = sosfilt(butter(2, 2600, "high", fs=SR, output="sos"), y) * bright * (10 ** (prof["emph_bright_db"] / 20) - 1)
    return (y + hi) * env_g * (1.0 + 0.06 * (energy - 1))


def _pad(y, peak, lead, tail):
    z = y / (np.max(np.abs(y)) + 1e-9) * peak
    return np.concatenate([np.zeros(int(lead * narrator.SR)), z, np.zeros(int(tail * narrator.SR))])   # kenar etkisi: Whisper son hecede kesiliyor


CACHE = os.environ.get("TTS_CACHE", os.path.join(HERE, "out", "_chunk_cache"))
KMAX = int(os.environ.get("KMAX", "15"))
KRETRY = int(os.environ.get("KRETRY", "30"))
RETRY = [r for r in os.environ.get("RETRY", "").split("|") if r]


def _ckey(toks, speed, pitch, prof, e):
    raw = json.dumps([[t["say"], bool(t["emph"])] for t in toks] + [round(speed, 4), round(pitch, 5), round(e, 3), T.VOICE, sorted(prof.items())], ensure_ascii=False)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _fmt(show_txt, w, miss, hyp, tag=""):
    ws = "--" if w is None else f"{w:.2f}"
    return f"  [{ws}{'!' + ','.join(miss) if miss else ''}] {show_txt}  ->  {hyp}{tag}"


def best_chunk(tts, toks, speed, pitch, prof, sent_energy=1.0):
    ref = []
    for t in toks:
        wild = (t["show"].replace("_", " ") != t["say"].replace("_", " ")) or any(ch.isdigit() for ch in t["show"])
        ws = asr.norm(_norm(t["show"]))
        if wild or not ws:
            ref.append(("*", True))
        else:
            ref += [(w, False) for w in ws]
    show_txt = " ".join(t["show"] for t in toks)
    retry = any(r in show_txt for r in RETRY)
    key = _ckey(toks, speed, pitch, prof, sent_energy)
    fy, fj = os.path.join(CACHE, key + ".npy"), os.path.join(CACHE, key + ".json")
    if os.path.exists(fy) and os.path.exists(fj) and not retry:
        info = json.load(open(fj, encoding="utf-8"))
        LOG.append((show_txt, info["w"], info["hyp"]))
        print(_fmt(show_txt, info["w"], info["miss"], info["hyp"], "   (önbellek)"), flush=True)
        return np.load(fy).astype(np.float64)
    if len(toks) < 2 and not must_keys(toks):   # tek kelimelik parçada Whisper güvenilmez (zor sözcük değilse seçme)
        best, bw, bh, bm = ORIG(tts, toks, speed, pitch, prof, sent_energy), None, "", []
    else:
        ref_str = " ".join(w for w, wl in ref if not wl)
        hard = bool(must_keys(toks))
        best, bw, bh, bs, bm = None, 9.0, "", 9.0, []
        kmax = max(K, KRETRY if retry else KMAX)
        k = 0
        while True:
            y = ORIG(tts, toks, speed, pitch, prof, sent_energy)
            ys = _shape(y, toks, prof, sent_energy)
            hyps = [asr.transcribe(_pad(ys, 0.5, 0.25, 0.45), narrator.SR)]
            if hard:                                  # zor sözcük varsa ikinci bir dinleme (farklı seviye/boşluk): ikisi de geçmeli
                hyps.append(asr.transcribe(_pad(ys, 0.3, 0.5, 0.7), narrator.SR))
            ev = []
            for hyp in hyps:
                hw = asr.norm(_norm(hyp))
                w = wer_wild(ref, hw)
                miss = must_miss(toks, hyp)
                sim = difflib.SequenceMatcher(None, ref_str, " ".join(hw)).ratio() if ref_str else 1.0
                ev.append((w + 0.5 * len(miss) + 0.1 * (1 - sim), w, miss, hyp))   # sim: eşitlikte ses olarak en yakın aday
            score, hyp = max((e[0], e[3]) for e in ev)                              # en kötü dinleme belirler
            w, miss = max(e[1] for e in ev), sorted({m for e in ev for m in e[2]})
            if score < bs - 1e-9:
                best, bw, bh, bs, bm = y, w, hyp, score, miss
            k += 1
            if w == 0 and not miss:
                break
            if k >= K and bw < 0.3 and not bm:       # yeterince iyi
                break
            if k >= kmax:
                break
    LOG.append((show_txt, bw, bh))
    print(_fmt(show_txt, bw, bm, bh), flush=True)
    os.makedirs(CACHE, exist_ok=True)
    np.save(fy, best.astype(np.float32))
    json.dump(dict(show=show_txt, w=bw, hyp=bh, miss=bm), open(fj, "w", encoding="utf-8"), ensure_ascii=False)
    return best


if __name__ == "__main__":
    lex = os.path.join(HERE, "..", "ses-lab", "lex.json")
    if os.path.exists(lex):
        narrator.LEX.update(json.load(open(lex)))
    narrator.synth_chunk = best_chunk
    Tt, tot, _ = narrator.render(T.SENTENCES, os.path.join(HERE, "out"), voice=T.VOICE, profile=T.PROF, tail=0.95)
    tl = json.load(open(os.path.join(HERE, "out", "timeline.json")))
    print(f"ses={T.VOICE} süre={Tt:.0f} sn (son kelime {tot:.2f} sn)")
    for s in tl["sentences"]:
        print(f"  {s['id']} {s['t0']:6.2f}–{s['t1']:6.2f}  " + " | ".join(f"{i}:{w['show']}" for i, w in enumerate(s['words'])))

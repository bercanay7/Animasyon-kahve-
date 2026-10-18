#!/usr/bin/env python3
"""timeline.json → Türkçe altyazı (SRT) + YouTube bölüm zaman damgaları.

  python3 make_srt.py            # yayin/sarlken_tr.srt (+ .vtt, _zamansiz.txt) ve yayin/bolumler.txt
Altyazı satırları: ≤2 satır × ≤42 karakter, ≤5,5 sn, noktalama/duraklarda bölünür; sözcük zamanları timeline.json'dan.
Ardışık satırlar çakışmaz (YouTube Studio çakışan altyazıyı kabul etmiyor): satır, sonrakinin başlamasından GAP önce kapanır."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "yayin")
os.makedirs(OUT, exist_ok=True)

MAXCH = 42
MAXDUR = 5.5
GAP = 0.02
TITLES = {
    "c0": "Giriş: 25 Ekim 1555",
    "c1": "Dört Tahtın Çocuğu (1500–1518)",
    "c2": "Taç Satılık (1519–1520)",
    "c3": "Şehirlerin İsyanı (1520–1522)",
    "c4": "Worms'ta Bir Keşiş (1521)",
    "c5": "İmparator Hep Başka Yerde (1521–1555)",
    "c6": "Kral, Esir, Düello (1521–1544)",
    "c7": "Sultan: Hiç Karşılaşmadılar (1526–1547)",
    "c8": "Akdeniz'de Barbaros (1534–1541)",
    "c9": "Yeni Dünya: Altın, Gümüş ve Vicdan (1519–1552)",
    "c10": "Faturayı Kim Ödedi?",
    "c11": "Adamın Kendisi",
    "c12": "Bırakmak (1555–1558)",
    "c13": "Hesap",
}


def ts(t):
    ms = int(round(max(0.0, t) * 1000))  # önce tam milisaniye: 59,9996 sn "00:00:59,1000" yazmasın
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrap2(text):
    """≤2 satıra böl (ortaya yakın boşlukta)."""
    if len(text) <= MAXCH:
        return text
    best, bd = None, 1e9
    for m in re.finditer(r" ", text):
        i = m.start()
        d = abs(len(text) / 2 - i)
        if i <= MAXCH + 3 and len(text) - i - 1 <= MAXCH + 3 and d < bd:
            best, bd = i, d
    if best is None:
        return text
    return text[:best] + "\n" + text[best + 1:]


def cues_for(sent):
    words = sent["words"]
    cues, cur = [], []

    def flush():
        if cur:
            cues.append((cur[0]["t0"], cur[-1]["t1"], " ".join(w["w"] for w in cur)))
            cur.clear()

    for i, w in enumerate(words):
        cur.append(w)
        txt = " ".join(x["w"] for x in cur)
        dur = cur[-1]["t1"] - cur[0]["t0"]
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_p = w["w"].rstrip("”\"")[-1:] in ".?!…:;"
        comma = w["w"].rstrip("”\"")[-1:] == ","
        gap = (nxt["t0"] - w["t1"]) if nxt else 9
        too_long = nxt is not None and (len(txt) + 1 + len(nxt["w"]) > 2 * MAXCH - 6 or dur > MAXDUR)
        if nxt is None or too_long or (end_p and len(txt) >= 18) or (comma and len(txt) >= 30) or (gap > 0.6 and len(txt) >= 22):
            flush()
    flush()
    return cues


def main():
    tl = json.load(open(os.path.join(HERE, "out", "timeline.json"), encoding="utf-8"))
    cues = []
    for s in tl["sentences"]:
        for a, b, txt in cues_for(s):
            b = max(b, a + 0.9)
            cues.append([max(0.0, a - 0.05), b + 0.12, wrap2(txt)])
    for p, q in zip(cues, cues[1:]):
        if p[1] > q[0] - GAP:
            p[1] = max(q[0] - GAP, p[0] + 0.2)
    n = len(cues)
    lines = [f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1)]
    open(os.path.join(OUT, "sarlken_tr.srt"), "w", encoding="utf-8").write("\n".join(lines))
    # yedek biçimler: WebVTT (iPhone .srt'yi seçtirmezse) ve zamansız metin (Studio "Without timing" kendisi hizalar)
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    vtt = ["WEBVTT", ""] + [f"{ts(a).replace(',', '.')} --> {ts(b).replace(',', '.')}\n{esc(t)}\n" for a, b, t in cues]
    open(os.path.join(OUT, "sarlken_tr.vtt"), "w", encoding="utf-8").write("\n".join(vtt))
    open(os.path.join(OUT, "sarlken_tr_zamansiz.txt"), "w", encoding="utf-8").write("\n\n".join(t for _, _, t in cues) + "\n")
    # bölüm zaman damgaları: kart başlangıcı (t0 − 3 sn) ; c0 için 0:00
    rows = []
    for c in tl["chapters"]:
        t = 0.0 if c["id"] == "c0" else max(0.0, c["t0"] - 3.0)
        mm, ss = divmod(int(round(t)), 60)
        h, mm = divmod(mm, 60)
        stamp = f"{h}:{mm:02d}:{ss:02d}" if h else f"{mm}:{ss:02d}"
        rows.append(f"{stamp} {TITLES[c['id']]}")
    open(os.path.join(OUT, "bolumler.txt"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    print(f"{n} altyazı satırı → yayin/sarlken_tr.srt (+ .vtt, _zamansiz.txt) ; bölüm damgaları → yayin/bolumler.txt")
    print("\n".join(rows))


if __name__ == "__main__":
    main()

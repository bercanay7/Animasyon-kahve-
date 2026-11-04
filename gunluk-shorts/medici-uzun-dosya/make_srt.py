#!/usr/bin/env python3
"""timeline.json → Türkçe altyazı (SRT) + YouTube bölüm zaman damgaları.

  MEDICI_PART=1 python3 make_srt.py      # yayin/medici_P1_tr.srt (+ .vtt, _zamansiz.txt) ve yayin/bolumler_P1.txt   (ya da: python3 make_srt.py --part 1)
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
import argparse
import sys

sys.path.insert(0, HERE)
import parca as PA  # noqa: E402

# YouTube bölüm etiketleri (kart başlığından farklı olabilir: c0 başlığı alıntı gibi okunmasın)
TITLES = {
    "c0": "Giriş: 18 Şubat 1743, Floransa",
    "c1": "Florin Şehri (1252–1397)",
    "c2": "Defterin Sihri (1397–1429)",
    "c3": "Kule ve Sürgün (1433–1464)",
    "c4": "Kubbe ve Kefaret (1418–1460'lar)",
    "c5": "Konsil, Kitap, Platon (1439–1492)",
    "c6": "Lorenzo (1449–1478)",
    "c7": "26 Nisan 1478: Pazzi Suikastı",
    "c8": "Aslanın İni (1478–1481)",
    "c9": "Defter Kapanıyor (1470–1494)",
    "c10": "Rahip ve Kral (1492–1498)",
    "c11": "Papa Oğulları (1512–1537)",
    "c12": "Dük (1537–1574)",
    "c13": "İki Kraliçe (1519–1642)",
    "c14": "Yıldızlar, Notalar, Taşlar (1584–1737)",
    "c15": "Son Medici'ler (1587–1737)",
    "c16": "Hesap (1737–bugün)",
}


def ts(t):
    ms = int(round(max(0.0, t) * 1000))  # önce tam milisaniye: 59,9996 sn "00:00:59,1000" yazmasın
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# kurul TE2-Ö9: sayı/unvan/belirleyici çiftleri ve sontakılar satır/replik sınırında bölünmez
NUMW = {"bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz", "on", "yirmi", "otuz", "kırk", "elli", "altmış",
        "yetmiş", "seksen", "doksan", "yüz", "bin", "milyon", "buçuk"}
GLUE_NEXT = {"bu", "şu", "o", "bir", "her", "eski", "yeni", "ilk", "son", "en", "çok", "daha", "aziz"}
GLUE_PREV = {"göre", "kadar", "gibi", "için", "ile", "değil", "bile", "da", "de", "ki", "mi", "mı", "mu", "mü", "olarak", "sonra", "önce"}


def _bare(w):
    return re.sub(r"[^\wçğıöşüâîû'’.]", "", w.lower()).strip("'’")


def bad_break(left, right):
    """left|right arasında bölmek okumayı yavaşlatır mı?"""
    l, r = _bare(left), _bare(right)
    if re.fullmatch(r"[ivxlc]+\.", l):                  # III. | Edward'ın
        return True
    if l.rstrip(".") in NUMW and r.split("'")[0].rstrip(".,;:") in NUMW:     # doksan | bin, yüz | elli
        return True
    if l.rstrip(".,;:") in NUMW and not re.search(r"[.,;:!?]$", left) and len(r) > 1:   # üç | buçuk, on | iki yaşındaydı
        return True
    if l in GLUE_NEXT and not re.search(r"[.,;:!?]$", left):
        return True
    if r.rstrip(".,;:!?”\"") in GLUE_PREV:
        return True
    if (l, r[:5]) in (("okuma", "yazma"), ("alacak", "ve"), ("kâr", "ve")) or (l == "via" and r[:1].isalpha()):   # ikilemeler ve sokak adları
        return True
    return False


def wrap2(text):
    """≤2 satıra böl (ortaya yakın boşlukta; noktalamadan sonra ve okumayı bölmeyen yerde)."""
    if len(text) <= MAXCH:
        return text
    r = _wrap_try(text, 3)                                 # ≤ 42 hedef; 43–45 yalnız okumayı bölen bir kesmeden kaçınmak için (ceza)
    return r if r else text


def _wrap_try(text, slack):
    best, bd = None, 1e9
    toks = text.split(" ")
    pos = 0
    for k in range(len(toks) - 1):
        pos += len(toks[k])
        i = pos
        pos += 1
        if i > MAXCH + slack or len(text) - i - 1 > MAXCH + slack:
            continue
        d = abs(len(text) / 2 - i)
        if re.search(r"[.,;:!?]$", toks[k]):
            d -= 6                                          # noktalamadan sonra bölmek doğal
        if bad_break(toks[k], toks[k + 1]):
            d += 40
        if i > MAXCH or len(text) - i - 1 > MAXCH:
            d += 25                                         # 42'yi aşan satır: yumuşak ceza
        if d < bd:
            best, bd = i, d
    if best is None:
        return None
    return text[:best] + "\n" + text[best + 1:]


def cues_for(sent):
    words = sent["words"]
    cues, cur = [], []

    def flush(keep=0):
        if len(cur) > keep:
            part = cur[:len(cur) - keep] if keep else cur[:]
            cues.append((part[0]["t0"], part[-1]["t1"], " ".join(w["w"] for w in part)))
            del cur[:len(cur) - keep]

    for i, w in enumerate(words):
        cur.append(w)
        txt = " ".join(x["w"] for x in cur)
        dur = cur[-1]["t1"] - cur[0]["t0"]
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_p = w["w"].rstrip("”\"")[-1:] in ".?!…:;"
        comma = w["w"].rstrip("”\"")[-1:] == ","
        gap = (nxt["t0"] - w["t1"]) if nxt else 9
        too_long = nxt is not None and (len(txt) + 1 + len(nxt["w"]) > 2 * MAXCH - 6 or dur > MAXDUR)
        if nxt is None or (end_p and len(txt) >= 18) or (comma and len(txt) >= 30) or (gap > 0.6 and len(txt) >= 22):
            flush()
        elif too_long:
            # okumayı bölen yerde kesme: son sözcüğü sonraki repliğe taşı (TE2-Ö9)
            flush(keep=1 if (len(cur) > 2 and bad_break(cur[-1]["w"], nxt["w"])) else 0)
    flush()
    # yetim son replik (≤ 2 sözcük ya da < 20 karakter): önceki replikle birleştirip dengeli iki parçaya böl (TE2-Ö9)
    if len(cues) >= 2:
        a0, b0, t0 = cues[-2]
        a1, b1, t1 = cues[-1]
        if len(t1.split()) <= 2 or len(t1) < 20:
            ws = [w for w in words if w["t0"] >= a0 - 1e-6]
            allt = " ".join(w["w"] for w in ws)
            if len(allt) <= 2 * MAXCH - 2 and (ws[-1]["t1"] - ws[0]["t0"]) <= MAXDUR + 1.5:
                cues[-2:] = [(a0, b1, allt)]
            else:
                best, bd = None, 1e9
                for k in range(1, len(ws)):
                    lt = " ".join(w["w"] for w in ws[:k]); rt = " ".join(w["w"] for w in ws[k:])
                    if len(lt) > 2 * MAXCH - 2 or len(rt) > 2 * MAXCH - 2:
                        continue
                    d = abs(len(lt) - len(rt)) - (8 if re.search(r"[.,;:!?]$", ws[k - 1]["w"]) else 0) + (40 if bad_break(ws[k - 1]["w"], ws[k]["w"]) else 0)
                    if d < bd:
                        best, bd = k, d
                if best:
                    cues[-2:] = [(ws[0]["t0"], ws[best - 1]["t1"], " ".join(w["w"] for w in ws[:best])),
                                 (ws[best]["t0"], ws[-1]["t1"], " ".join(w["w"] for w in ws[best:]))]
    return cues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=PA.PART)
    args = ap.parse_args()
    if not args.part:
        raise SystemExit("--part N (1–7) ya da MEDICI_PART gerekli")
    tl = json.load(open(os.path.join(HERE, f"out_p{args.part}", "timeline.json"), encoding="utf-8"))
    tag = f"medici_P{args.part}"
    cues = []
    for s in tl["sentences"]:
        for a, b, txt in cues_for(s):
            b = max(b, a + 0.9)
            cues.append([max(0.0, a - 0.05), b + 0.12, wrap2(txt)])
    for p, q in zip(cues, cues[1:]):
        if p[1] > q[0] - GAP:
            p[1] = max(q[0] - GAP, p[0] + 0.2)
    # okuma hızı ≤ 17 kar/sn ve ≥ 1,2 sn: bitişi sonraki repliğe kadarki boşluğa uzat (en çok +0,8 sn; görüntü/sese dokunmaz) — TE2-Ö9
    for k, p in enumerate(cues):
        nxt0 = cues[k + 1][0] - GAP if k + 1 < len(cues) else p[1] + 0.8
        n = len(p[2].replace("\n", " "))
        need = max(n / 17.0, 1.2)
        if p[1] - p[0] < need:
            p[1] = min(max(p[1], p[0] + need), nxt0, p[1] + 0.8)
    n = len(cues)
    lines = [f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1)]
    open(os.path.join(OUT, f"{tag}_tr.srt"), "w", encoding="utf-8").write("\n".join(lines))
    # yedek biçimler: WebVTT (iPhone .srt'yi seçtirmezse) ve zamansız metin (Studio "Without timing" kendisi hizalar)
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    vtt = ["WEBVTT", ""] + [f"{ts(a).replace(',', '.')} --> {ts(b).replace(',', '.')}\n{esc(t)}\n" for a, b, t in cues]
    open(os.path.join(OUT, f"{tag}_tr.vtt"), "w", encoding="utf-8").write("\n".join(vtt))
    open(os.path.join(OUT, f"{tag}_tr_zamansiz.txt"), "w", encoding="utf-8").write("\n\n".join(t for _, _, t in cues) + "\n")
    # bölüm zaman damgaları: ilk bölüm 0:00; sonrakiler önceki bölümün bitişi (= kart/ana başlık başlangıcı)
    rows = []
    prev = None
    for c in tl["chapters"]:
        t0 = 0.0 if prev is None else prev["t1"]
        mm, ss = divmod(int(round(t0)), 60)
        h, mm = divmod(mm, 60)
        stamp = f"{h}:{mm:02d}:{ss:02d}" if h else f"{mm}:{ss:02d}"
        rows.append(f"{stamp} {TITLES[c['id']]}")
        prev = c
    open(os.path.join(OUT, f"bolumler_P{args.part}.txt"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    print(f"{n} altyazı satırı → yayin/{tag}_tr.srt (+ .vtt, _zamansiz.txt) ; bölüm damgaları → yayin/bolumler_P{args.part}.txt")
    print("\n".join(rows))


if __name__ == "__main__":
    main()

"""MEDICI — Uzun Dosya #2: anlatım metni (tek kaynak; bölüm içerikleri scr_cN.py dosyalarında).

Her cümle:  (gösterim_metni,)  |  (gösterim, söylenen)  |  (gösterim, söylenen_ya_da_None, "sınıf kimlik")
  * Gösterim: altyazı/SRT ve ekran için (rakam, doğru yazım).
  * Söylenen: ElevenLabs'e giden metin — rakamlar sözcüğe çevrilir, yabancı adlar Türkçe okunuşla yazılır (PRON).
    Söylenen verilmezse (ya da None) gösterimden türetilir. `{gösterim|söylenen}` biçimi satır içi değişkendir.
  * Üçüncü öğe (isteğe bağlı) kaynak etiketidir: "◐ M4b:b73" gibi → `kaynaklar.py` / kaynak kapısı çıktısı.
Bölüm = paragraf listesi; paragraf = cümle listesi. Cümle kimlikleri: c<bölüm>s<sıra> (bölüm içinde 1'den).
Üslup: USLUP_REHBERI.md · yönetmenlik: YONETMENLIK_REHBERI.md · olgu dayanakları: arastirma/*.md ve brif/cK_brif.md.

Parçalar: P1 = c0–c6 (ALTIN) · P2 = c7–c11 (BEDEL) · P3 = c12–c16 (MİRAS).
Kullanım: `python3 script.py` (parça/bölüm istatistikleri) · `python3 script.py c3` (bölüm metni) · `python3 script.py --part 1`.
"""
import importlib
import re

# ---------------------------------------------------------------- sayı → Türkçe sözcük
_ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def tr_num(n: int) -> str:
    if n == 0:
        return "sıfır"
    parts = []
    if n >= 1_000_000:
        parts.append(tr_num(n // 1_000_000) + " milyon")
        n %= 1_000_000
    if n >= 1000:
        k = n // 1000
        parts.append(("" if k == 1 else tr_num(k) + " ") + "bin")
        n %= 1000
    if n >= 100:
        h = n // 100
        parts.append(("" if h == 1 else _ONES[h] + " ") + "yüz")
        n %= 100
    if n >= 10:
        parts.append(_TENS[n // 10])
        n %= 10
    if n:
        parts.append(_ONES[n])
    return " ".join(p.strip() for p in parts if p.strip())


# ---------------------------------------------------------------- okunuş sözlüğü (yalnız söylenen metne uygulanır)
# Sıra önemlidir: uzun/özel kalıplar kısa olanlardan ÖNCE. Bölüm modülleri kendi PRON listesini ekler (aşağıda birleşir).
BASE_PRON = [
    (r"\bAnna Maria Luisa\b", "Anna Maria Luiza"), (r"\bGian Gastone\b", "Can Gastone"),
    (r"\bFrancis Stephen\b", "Fransis Stifın"), (r"\bLorraine'li\b", "Lorenli"), (r"\bLorraine\b", "Loren"),
    (r"\bMedici'ler\b", "Mediçiler"), (r"\bMedici'nin\b", "Mediçi'nin"), (r"\bMedici\b", "Mediçi"),
    (r"\bUffizi\b", "Uffitsi"), (r"\bPalazzo Pitti\b", "Palattso Pitti"), (r"\bToskana\b", "Toskana"),
    (r"\bGiovanni\b", "Covanni"), (r"\bCosimo\b", "Kozimo"), (r"\bLorenzo\b", "Lorentso"), (r"\bPiero\b", "Pyero"),
    (r"\bGiuliano\b", "Culyano"), (r"\bClarice\b", "Klariçe"), (r"\bLucrezia\b", "Lukretsya"), (r"\bContessina\b", "Kontessina"),
    (r"\bFirenze\b", "Firentse"), (r"\bRoma\b", "Roma"),
]

PRON = list(BASE_PRON)
CHAPTERS = []
PART_OF = {}
PARTS = {1: [f"c{i}" for i in range(0, 7)], 2: [f"c{i}" for i in range(7, 12)], 3: [f"c{i}" for i in range(12, 17)]}
for _p, _cs in PARTS.items():
    for _c in _cs:
        PART_OF[_c] = _p
for _i in range(17):
    try:
        _m = importlib.import_module(f"scr_c{_i}")
    except ModuleNotFoundError:
        continue
    CHAPTERS.append(_m.CH)
    # bölüm PRON'ları önce gelir (kendi özel kalıpları genel olanları ezer)
    PRON = list(getattr(_m, "PRON", [])) + PRON


# ---------------------------------------------------------------- Romen rakamı sıra sayıları ("II. Pius" → "İkinci Pius")
_ORD_ONES = ["", "birinci", "ikinci", "üçüncü", "dördüncü", "beşinci", "altıncı", "yedinci", "sekizinci", "dokuzuncu"]
_ORD_TENS = ["", "onuncu", "yirminci", "otuzuncu", "kırkıncı", "ellinci", "altmışıncı", "yetmişinci", "sekseninci", "doksanıncı"]
_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(r: str) -> int:
    n, prev = 0, 0
    for ch in reversed(r):
        v = _ROMAN[ch]
        n += v if v >= prev else -v
        prev = max(prev, v)
    return n


def tr_ord(n: int) -> str:
    t, o = divmod(n, 10)
    if n >= 100:
        raise ValueError(n)
    if o == 0:
        return _ORD_TENS[t]
    return ((_TENS[t] + " ") if t else "") + _ORD_ONES[o]


def _tr_cap(w: str) -> str:
    return ({"i": "İ", "ı": "I"}.get(w[0], w[0].upper()) + w[1:]) if w else w


def _roman_sub(m):
    return " ".join(_tr_cap(w) for w in tr_ord(roman_to_int(m.group(1))).split())


def _num_sub(m):
    raw, suf = m.group(1), m.group(2) or ""
    n = int(raw.replace(".", ""))
    return tr_num(n) + suf.lstrip("'’")


def to_speech(s: str) -> str:
    s = re.sub(r"\{[^|{}]*\|([^{}]*)\}", r"\1", s)                  # {göster|söyle}
    s = re.sub(r"\b([IVXLC]{1,6})\.(?=\s+[A-ZÇĞİÖŞÜ])", _roman_sub, s)           # Romen sıra sayısı
    s = re.sub(r"(\d{1,3}(?:\.\d{3})+|\d+)(['’][A-Za-zçğıöşüÇĞİÖŞÜ]+)?", _num_sub, s)
    for pat, rep in PRON:
        s = re.sub(pat, rep, s)
    s = s.replace("’", "'")

    def _up(ch):
        return {"i": "İ", "ı": "I"}.get(ch, ch.upper())
    m = re.search(r"[A-Za-zçğıöşüÇĞİÖŞÜ]", s)                          # cümle başı büyük harf (sayıdan türeyen sözcükler küçük kalır)
    if m:
        i = m.start()
        s = s[:i] + _up(s[i]) + s[i + 1:]
    s = re.sub(r"([.!?]\s+)([a-zçğıöşü])", lambda mm: mm.group(1) + _up(mm.group(2)), s)
    return s


def to_display(s: str) -> str:
    return re.sub(r"\{([^|{}]*)\|[^{}]*\}", r"\1", s)


# ---------------------------------------------------------------- türetilmiş yapılar
def _speech_of(tup):
    raw = tup[0]
    return to_speech(tup[1] if len(tup) > 1 and tup[1] else raw)


def sentences(part=None):
    """Düz liste: dict(id, ch, para, disp, speech, tag). part verilirse yalnız o parçanın bölümleri."""
    out = []
    for ch in CHAPTERS:
        if part is not None and PART_OF.get(ch["id"]) != part:
            continue
        k = 0
        for pi, para in enumerate(ch["paras"]):
            for tup in para:
                k += 1
                out.append(dict(id=f"{ch['id']}s{k}", ch=ch["id"], para=pi, disp=to_display(tup[0]), speech=_speech_of(tup),
                                tag=(tup[2] if len(tup) > 2 else "")))
    return out


def chapter_text(ch_id):
    """ElevenLabs'e gidecek bölüm metni: paragraflar boş satırla ayrılır."""
    ch = next(c for c in CHAPTERS if c["id"] == ch_id)
    return "\n\n".join(" ".join(_speech_of(t) for t in para) for para in ch["paras"])


def chapter_stats(ch):
    sents = [t for para in ch["paras"] for t in para]
    lens = [len(_speech_of(t).split()) for t in sents]
    words = sum(lens)
    return dict(sent=len(sents), words=words, avg=(words / len(sents) if sents else 0), mx=(max(lens) if lens else 0))


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if args and args[0] == "--part":
        part = int(args[1])
        tot = 0
        for ch in CHAPTERS:
            if PART_OF.get(ch["id"]) == part:
                st = chapter_stats(ch)
                tot += st["words"]
                print(f"{ch['id']:4s} {st['sent']:3d} cümle {st['words']:5d} söz  ort {st['avg']:4.1f}  azami {st['mx']:2d}  ≈{st['words'] / 1.7 / 60:4.1f} dk  {ch['title']}")
        print(f"PARÇA {part}: {tot} söz ≈ {tot / 1.7 / 60:.1f} dk (1,7 söz/sn, duraklar dahil)")
    elif args:
        print(chapter_text(args[0]))
    else:
        tot = 0
        for ch in CHAPTERS:
            st = chapter_stats(ch)
            tot += st["words"]
            print(f"{ch['id']:4s} P{PART_OF.get(ch['id'], '?')} {st['sent']:3d} cümle {st['words']:5d} söz  ort {st['avg']:4.1f}  azami {st['mx']:2d}  {ch['title']}")
        print(f"TOPLAM {tot} söz ≈ {tot / 1.7 / 60:.1f} dk")

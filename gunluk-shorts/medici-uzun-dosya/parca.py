"""Parça (P1/P2/P3) yardımcısı: MEDICI_PART ortam değişkeni → çıktı dizini (out_pN) ve bölüm listesi.

  MEDICI_PART=1 python3 ses_birlestir.py     # P1 sesini out_p1/ altına birleştirir
  MEDICI_PART=1 python3 ses_hizala.py        # out_p1/timeline.json
Motor tarafında (render/mux) çalışmak için `out` bağlantısı parçaya çevrilir: `python3 parca.py --kullan 1` (out → out_p1).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PART = int(os.environ["MEDICI_PART"]) if os.environ.get("MEDICI_PART") else None
OUT = os.path.join(HERE, f"out_p{PART}") if PART else os.path.join(HERE, "out")


def kullan(n: int):
    """`out` bir dizinse out_base'e taşır (yoksa), sonra out → out_pN sembolik bağlantısını kurar."""
    tgt = os.path.join(HERE, f"out_p{n}")
    os.makedirs(tgt, exist_ok=True)
    out = os.path.join(HERE, "out")
    if os.path.islink(out):
        os.unlink(out)
    elif os.path.isdir(out):
        base = os.path.join(HERE, "out_base")
        if os.path.exists(base):
            raise SystemExit("out ve out_base ikisi de var; elle düzelt")
        os.rename(out, base)
    os.symlink(tgt, out)
    print("out →", tgt)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--kullan":
        kullan(int(sys.argv[2]))
    else:
        print(f"PART={PART} OUT={OUT}")

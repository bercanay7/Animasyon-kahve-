#!/usr/bin/env bash
# Lemo-Opuscar'dan tek bir üslubu (STYLE.md + demo motoru) sabit commit'ten çalışma alanına indirir. Depoya yazmaz.
# Kullanım: bash araclar/lemo/getir.sh <slug> [hedef_dizin]
#   ör. bash araclar/lemo/getir.sh gilded-illumination "$SCRATCH/lemo"
# Lisans (KATALOG.md'ye bak): kod MIT → motor dosyaları videonun lib/vendor/ klasörüne LICENSE ile kopyalanabilir.
# STYLE.md/DEMO.md CC BY-NC 4.0 + film yapma izni → okunur ve uygulanır, ama herkese açık bu depoya KOPYALANMAZ.
set -euo pipefail
SLUG="${1:?slug ver (araclar/lemo/KATALOG.md)}"
HEDEF="${2:-${TMPDIR:-/tmp}/lemo-opuscar}"
COMMIT=3a7132b   # 12 Kasım 2026; değiştirirsen KATALOG.md ve ASSETS.md'yi de güncelle
if [ ! -d "$HEDEF/.git" ]; then
  git clone -q --filter=blob:none --no-checkout https://github.com/lemomo-ai/lemo-opuscar.git "$HEDEF"
  git -C "$HEDEF" sparse-checkout init --cone
fi
git -C "$HEDEF" sparse-checkout add "styles/$SLUG" LICENSES
git -C "$HEDEF" checkout -q "$COMMIT"
cp "$HEDEF/LICENSES/MIT.txt" "$HEDEF/styles/$SLUG/LICENSE-kod-MIT.txt" 2>/dev/null || true
echo "Hazır: $HEDEF/styles/$SLUG"
echo "Önce oku: STYLE.md (üslup yasası), demo/CREDITS (üçüncü taraf varlıklar ve lisansları)."
grep -rlE "fetch\(|https?://" "$HEDEF/styles/$SLUG/demo" --include=*.js 2>/dev/null | sed "s|^|Ağ çağrısı ya da adres içeren dosya (incele): |" || true

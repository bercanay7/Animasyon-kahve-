#!/usr/bin/env bash
# Parça 1 v2 üretim zinciri (kurul tur 1 düzeltmeleri sonrası). Her adım günlüğe yazılır; bir adım başarısızsa durur.
#   bash p1_v2_uret.sh            # tam zincir: denetim → geçiş sesleri → miks → render → birleştir → mux → QA
#   bash p1_v2_uret.sh --render   # denetim ve miks bitmişse yalnız render'dan sonrası
set -euo pipefail
cd "$(dirname "$0")"
LOG=out_p1/uretim_v2.log
log(){ echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

if [[ "${1:-}" != "--render" ]]; then
  log "bayat oda katmanı önbelleği siliniyor (istek_SCN #5)"
  rm -f out/_cache/world/oda_p1*
  log "qa_flow --part 1 (tüm kapılar GEÇTİ olmalı)"
  python3 qa_flow.py --part 1 > out_p1/qa_flow_v2.txt 2>&1 || { log "qa_flow KALDI — ayrıntı out_p1/qa_flow_v2.txt"; tail -40 out_p1/qa_flow_v2.txt | tee -a "$LOG"; exit 1; }
  tail -25 out_p1/qa_flow_v2.txt | tee -a "$LOG"
  log "geçiş sesleri (sfx_gecis.json) motordan yeniden üretiliyor"
  MEDICI_PART=1 python3 miks_kur.py --sadece-gecis 2>&1 | tail -5 | tee -a "$LOG"
  log "miks (−14 LUFS, kuyruk compose.TAIL)"
  MEDICI_PART=1 python3 miks_kur.py 2>&1 | tail -15 | tee -a "$LOG"
fi
log "eski segmentler siliniyor"
rm -f out_p1/seg/*.mp4 out_p1/seg/*.done out_p1/medici_p1_noaudio.mp4
log "render (4 işçi, crf 19, slow)"
nice -n 5 python3 render.py --part 1 --all --workers 4 --crf 19 2>&1 | tail -20 | tee -a "$LOG"
log "birleştir + mux + QA"
python3 render.py --part 1 --concat 2>&1 | tail -3 | tee -a "$LOG"
python3 render.py --part 1 --mux 2>&1 | tail -3 | tee -a "$LOG"
python3 render.py --part 1 --qa 2>&1 | tail -30 | tee -a "$LOG"
log "BİTTİ"

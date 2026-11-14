#!/bin/bash
# vo/*.mp3 için (words.json'ı olmayanlar) Whisper dökümü ve senaryoyla karşılaştırma → vo/rapor_<dosya>.txt
cd "$(dirname "$0")/.."
python3 - <<'PY'
import json
b={x['onek']:x['ad'] for x in json.load(open('vo/bolumler.json'))}
json.dump(b,open('/tmp/claude-0/-home-user/a50b5f05-b607-5868-acd6-7063337d509f/scratchpad/bolum_ad.json','w'),ensure_ascii=False)
PY
for f in vo/s*_?.mp3; do
  w="${f%.mp3}.words.json"; [ -f "$w" ] && continue
  k=$(basename "$f" | cut -c1-3)
  ad=$(python3 -c "import json;print(json.load(open('/tmp/claude-0/-home-user/a50b5f05-b607-5868-acd6-7063337d509f/scratchpad/bolum_ad.json'))['$k'])")
  python3 tools/transcribe.py "$f" "$ad" > "vo/rapor_$(basename "$f" .mp3).txt" 2>/dev/null
  echo "$f: $(head -1 vo/rapor_$(basename "$f" .mp3).txt)"
done

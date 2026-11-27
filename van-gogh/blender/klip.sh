# bash van-gogh/blender/klip.sh ad1 [ad2 …]  (PY: bpy kurulu Python)
cd "$(dirname "$0")"; PY=${PY:-/tmp/claude-0/-home-user/1251b65f-a684-562c-b86b-a58164cef97e/scratchpad/bpyenv/bin/python}
for ad in "$@"; do d=klip_$ad; EKLEM=$d/eklem.json KOSTUM=$d/kostum.json $PY figur_bpy.py $d/kare - $d/kamera.json > $d/log.txt 2>&1; echo "$ad: $(ls $d/kare | wc -l) kare"; done

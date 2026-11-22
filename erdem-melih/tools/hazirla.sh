#!/usr/bin/env bash
# iPhone MOV → sabitlenmiş 1440x2560 ara kopya (vidstab, iki geçiş). Kullanım: tools/hazirla.sh girdi.MOV cikti_klasoru
set -e
V="$1"; O="$2"; mkdir -p "$O"
ffmpeg -v error -y -i "$V" -map 0:v:0 -vf "scale=1440:2560:flags=lanczos,vidstabdetect=shakiness=6:accuracy=15:result=$O/tr.trf" -f null -
ffmpeg -v error -y -i "$V" -map 0:v:0 -map 0:a:0 -vf "scale=1440:2560:flags=lanczos,vidstabtransform=input=$O/tr.trf:smoothing=25:optzoom=1:zoomspeed=0.2:interpol=bicubic,unsharp=5:5:0.4" \
  -c:v libx264 -crf 10 -preset medium -pix_fmt yuv420p -c:a pcm_s16le "$O/stab.mov"

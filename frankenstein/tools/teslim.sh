#!/bin/bash
# Teslim kopyaları (Gılgamış dersi: render → teslim zinciri &&, kopyanın süresi render'la karşılaştırılır; x265 günlüğü depoya yazılmaz)
set -e
cd "$(dirname "$0")/.."
SP=${SP:-/tmp/claude-0}
mkdir -p teslim
cp frankenstein.mp4 teslim/frankenstein_youtube.mp4
ffmpeg -v error -y -i frankenstein.mp4 -c:v libx265 -b:v 1100k -x265-params pass=1:stats=$SP/x265_fr.log -tag:v hvc1 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -an -f null /dev/null
ffmpeg -v error -y -i frankenstein.mp4 -c:v libx265 -b:v 1100k -x265-params pass=2:stats=$SP/x265_fr.log -tag:v hvc1 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a copy -movflags +faststart teslim/frankenstein_telefon.mp4
for f in frankenstein.mp4 teslim/*.mp4; do printf "%s  %s sn  %s MB\n" "$f" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)" "$(( $(stat -c %s $f) / 1000000 ))"; done

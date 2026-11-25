#!/bin/bash
# Teslim kopyaları (Gılgamış dersi: render → teslim zinciri &&, kopyanın süresi render'la karşılaştırılır; x265 günlüğü depoya yazılmaz)
#   YouTube: render ≤ 380 MB ise kendisi; değilse H.264 iki geçiş (bit hızı süreye göre ~360 MB).
#   Telefon: H.265 iki geçiş 900k, AAC 128k (< 100 MB, uygulamada indirme düğmesi çıksın diye).
set -e
cd "$(dirname "$0")/.."
SP=${SP:-/tmp/claude-0}
SRC=stanford.mp4
mkdir -p teslim
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $SRC)
BOY=$(stat -c %s $SRC)
RENK="-colorspace bt709 -color_primaries bt709 -color_trc bt709"
if [ $BOY -le 380000000 ]; then
  cp $SRC teslim/stanford_youtube.mp4
else
  KB=$(python3 -c "print(int(360e6*8/float('$DUR')/1000) - 256)")
  echo "YouTube kopyası iki geçiş: ${KB}k"
  ffmpeg -v error -y -i $SRC -c:v libx264 -preset slow -b:v ${KB}k -pass 1 -passlogfile $SP/x264_st -pix_fmt yuv420p $RENK -an -f null /dev/null
  ffmpeg -v error -y -i $SRC -c:v libx264 -preset slow -b:v ${KB}k -pass 2 -passlogfile $SP/x264_st -pix_fmt yuv420p $RENK -c:a copy -metadata:s:a:0 language=tur -movflags +faststart teslim/stanford_youtube.mp4
fi
ffmpeg -v error -y -i $SRC -c:v libx265 -b:v 900k -x265-params pass=1:stats=$SP/x265_st.log:log-level=error -tag:v hvc1 $RENK -an -f null /dev/null
ffmpeg -v error -y -i $SRC -c:v libx265 -b:v 900k -x265-params pass=2:stats=$SP/x265_st.log:log-level=error -tag:v hvc1 $RENK -c:a aac -b:a 128k -metadata:s:a:0 language=tur -movflags +faststart teslim/stanford_telefon.mp4
for f in $SRC teslim/*.mp4; do printf "%s  %s sn  %s MB\n" "$f" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)" "$(( $(stat -c %s $f) / 1000000 ))"; done

#!/bin/bash
# Teslim: (1) değişen parçaları yeniden üret, (2) usta kopya, (3) H.265 YouTube kopyası (≤ 400 MiB) ve 720p telefon kopyası, (4) Shorts
set -e
cd "$(dirname "$0")/.."
[ -n "$ONLY" ] && ONLY="$ONLY" WORKERS=4 PRESET=medium node render.js mary_stuart.mp4
mkdir -p teslim
nice -n 5 ffmpeg -y -v error -i mary_stuart.mp4 -c:v libx265 -preset medium -crf 27 -x265-params log-level=error -tag:v hvc1 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a copy -movflags +faststart teslim/mary_stuart_youtube.mp4
nice -n 5 ffmpeg -y -v error -i mary_stuart.mp4 -vf scale=1280:720:flags=lanczos -c:v libx265 -preset medium -crf 30 -x265-params log-level=error -tag:v hvc1 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 128k -movflags +faststart teslim/mary_stuart_telefon.mp4
ls -la teslim

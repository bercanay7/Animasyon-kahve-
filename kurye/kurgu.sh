set -e
# Mektuplar kurgu: geniş + orta + yakın planlar, tek ses. Kullanım: SP=çıktı_klasörü PY=bpy_kurulu_python bash kurye/kurgu.sh
cd "$(dirname "$0")/.."; SP=${SP:-/tmp/kurye_kurgu}; mkdir -p $SP; PY=${PY:-python3}
node kurye/blender/eklem_disa.js > /dev/null
$PY kurye/blender/kurye_bpy.py kurye/blender/kare > /dev/null 2>&1
$PY kurye/blender/kurye_bpy.py kurye/blender/kare_orta 126:190 kurye/blender/kamera_orta.json > /dev/null 2>&1
$PY kurye/blender/kurye_bpy.py kurye/blender/kare_yakin 219:277 kurye/blender/kamera_yakin.json > /dev/null 2>&1
echo blender tamam
Q="blender=1" node /home/user/Animasyon-kahve-/araclar/manken/render.js kurye/tablo.html $SP/k_genis.mp4 | tail -1
Q="blender=1&plan=orta" node /home/user/Animasyon-kahve-/araclar/manken/render.js kurye/tablo.html $SP/k_orta.mp4 | tail -1
Q="blender=1&plan=yakin" node /home/user/Animasyon-kahve-/araclar/manken/render.js kurye/tablo.html $SP/k_yakin.mp4 | tail -1
# kurgu: geniş 0–8.4 | orta 8.4–12.6 | geniş 12.6–14.6 | yakın 14.6–18.4 | geniş 18.4–25 (plan dosyaları kendi t0'ından başlar)
X="-c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -an -r 30"
ffmpeg -v error -y -i $SP/k_genis.mp4 -ss 0 -t 8.4 $X $SP/kk1.mp4
ffmpeg -v error -y -i $SP/k_orta.mp4 -ss 0 -t 4.2 $X $SP/kk2.mp4
ffmpeg -v error -y -i $SP/k_genis.mp4 -ss 12.6 -t 2.0 $X $SP/kk3.mp4
ffmpeg -v error -y -i $SP/k_yakin.mp4 -ss 0 -t 3.8 $X $SP/kk4.mp4
ffmpeg -v error -y -i $SP/k_genis.mp4 -ss 18.4 -t 6.6 $X $SP/kk5.mp4
printf "file '%s'\n" $SP/kk1.mp4 $SP/kk2.mp4 $SP/kk3.mp4 $SP/kk4.mp4 $SP/kk5.mp4 > $SP/kk.txt
ffmpeg -v error -y -f concat -safe 0 -i $SP/kk.txt -i kurye/audio/ses.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -metadata:s:a:0 language=tur -movflags +faststart -shortest $SP/mektuplar_kurgu.mp4
ffmpeg -v error -y -i $SP/mektuplar_kurgu.mp4 -c:v libx265 -crf 28 -preset medium -tag:v hvc1 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -x265-params log-level=error -c:a copy $SP/mektuplar_kurgu_tel.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $SP/mektuplar_kurgu.mp4; ls -la $SP/mektuplar_kurgu*

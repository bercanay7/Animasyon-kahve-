#!/usr/bin/env bash
# Telifli ya da başkasına ait kaynakları archive.org'dan indirir, videoda kullanılan parçaları keser → kaynak/
# (kaynak/ git'e eklenmez). Gerekenler: curl, ffmpeg.
#   kaynak/film.mp4          Onuncu Yıl Nutku filmi (29 Ekim 1933), 0–11.6 sn: yakın plan dikey kırpılır, genel plan
#                            bulanık zemin üzerinde 16:9 pencere; logolar kadraj dışında kalır. 1080x1920, 30 fps, sessiz
#   kaynak/nutuk.wav         aynı anın sesi: "Bugün, Cumhuriyetimizin onuncu yılını doldurduğu en büyük bayramdır. Kutlu olsun!"
#   kaynak/izmir-marsi.wav   İzmir Marşı (Türk Ordu Marşı kaydı), ilk ses 2.75 sn'den itibaren 17 sn
#   kaynak/onuncu-yil.wav    Onuncu Yıl Marşı (TSK Armoni Mızıkası), ilk ses 3.05 sn'den itibaren 12 sn
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p kaynak/indir
get() { [ -s "kaynak/indir/$2" ] || curl -sSL --retry 4 -o "kaynak/indir/$2" "https://archive.org/download/$1"; }
get ata_20250210/ata.mp4 nutuk-film.mp4
get youtube-rNPUp1hkpJQ/rNPUp1hkpJQ.mp4 izmir.mp4
get youtube-NNUMtvlFskw/Onuncu_Y_l_Mar_-_TSK_Armoni_M_z_kas-NNUMtvlFskw.mp4 onuncu.mp4

GRADE="eq=contrast=1.12:brightness=-0.02:saturation=0,colorbalance=rs=0.05:gs=0.02:bs=-0.05:rm=0.03:bm=-0.03,noise=alls=9:allf=t"
# film: 0–4.86 yakın plan (Atatürk x≈900), 4.86–11.6 genel plan; kesme filmdeki kesmeyle aynı
ffmpeg -v error -y -i kaynak/indir/nutuk-film.mp4 -filter_complex "
[0:v:0]trim=0:4.86,setpts=PTS-STARTPTS,crop=608:1080:596:0,scale=1080:1920:flags=lanczos,${GRADE},vignette=PI/4.5,setsar=1[a];
[0:v:0]trim=4.86:11.6,setpts=PTS-STARTPTS,split[b1][b2];
[b1]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.32:saturation=0[bg];
[b2]crop=1400:788:200:292,scale=1080:608:flags=lanczos,${GRADE}[fg];
[bg][fg]overlay=0:520,vignette=PI/4,setsar=1[b];
[a][b]concat=n=2:v=1:a=0,fps=30,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 14 -preset medium kaynak/film.mp4
# ses: hafif gürültü azaltma, uçlarda yumuşak geçiş
ffmpeg -v error -y -i kaynak/indir/nutuk-film.mp4 -map 0:a:0 -t 11.6 -af "highpass=f=90,lowpass=f=7000,afftdn=nr=12:nf=-42,afade=t=out:st=11.3:d=0.3" -ar 48000 -ac 1 kaynak/nutuk.wav
ffmpeg -v error -y -ss 2.75 -t 17 -i kaynak/indir/izmir.mp4 -vn -ar 48000 -ac 2 kaynak/izmir-marsi.wav
ffmpeg -v error -y -ss 3.05 -t 12 -i kaynak/indir/onuncu.mp4 -vn -ar 48000 -ac 2 kaynak/onuncu-yil.wav
echo "kaynak/ hazır"

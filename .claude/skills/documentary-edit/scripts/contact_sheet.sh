#!/usr/bin/env bash
# One frame every N seconds tiled into a contact sheet, to review a render by eye.
# usage: contact_sheet.sh <video.mp4> <out.jpg> [every_seconds=5]
set -euo pipefail
v=$1; out=$2; n=${3:-5}
dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$v")
frames=$(python3 -I -c "import math;print(max(1,math.ceil($dur/$n)))")
cols=6; rows=$(( (frames + cols - 1) / cols ))
ffmpeg -nostdin -v error -y -i "$v" -vf "fps=1/$n,scale=320:-2,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=${cols}x${rows}:padding=4:color=black" -frames:v 1 "$out"
echo "wrote $out ($frames frames, ${cols}x${rows})"

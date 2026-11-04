#!/usr/bin/env bash
# Final audio pass + mux. Replaces the render's audio with: voice (EQ'd, levelled)
# + optional music bed ducked under the voice, normalised to YouTube loudness.
#
# usage: finish_audio.sh <render.mp4> <voice.wav> <out.mp4> [music.mp3] [music_db]
#   music_db: bed level before ducking, default -20 (dB). Ducking adds ~-12 dB while speaking.
# Target: -14 LUFS integrated, -1.5 dBTP (YouTube plays back at -14; louder gets turned down).
set -euo pipefail
video=$1; voice=$2; out=$3; music=${4:-}; mdb=${5:--20}
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT

vchain="highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2"
if [[ -n "$music" ]]; then
  ffmpeg -nostdin -v error -y -i "$voice" -stream_loop -1 -i "$music" -filter_complex \
   "[0:a]$vchain,asplit=2[v][sc];\
    [1:a]volume=${mdb}dB,afade=t=in:d=1.5[m0];\
    [m0][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[m];\
    [v][m]amix=inputs=2:duration=first:normalize=0[mix]" \
   -map "[mix]" -ar 48000 "$tmp/mix.wav"
else
  ffmpeg -nostdin -v error -y -i "$voice" -af "$vchain" -ar 48000 "$tmp/mix.wav"
fi

# two-pass loudnorm
stats=$(ffmpeg -nostdin -hide_banner -i "$tmp/mix.wav" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get(){ echo "$stats" | python3 -I -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -nostdin -v error -y -i "$tmp/mix.wav" -af \
 "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true" \
 -ar 48000 "$tmp/final.wav"

ffmpeg -nostdin -v error -y -i "$video" -i "$tmp/final.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$out"
echo "wrote $out"
bash "$(dirname "$0")/qa_audio.sh" "$out"

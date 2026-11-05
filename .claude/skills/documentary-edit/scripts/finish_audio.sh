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

# loudness: measure, apply the exact gain to -14 LUFS, then a 4x-oversampled
# limiter at -2 dBFS catches the peaks the gain pushes up (true peak stays under -1)
meas(){ ffmpeg -nostdin -hide_banner -i "$1" -af loudnorm=print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
        | python3 -I -c "import sys,json;print(json.load(sys.stdin)['input_i'])"; }
gain=$(python3 -I -c "print(-14 - float('$(meas "$tmp/mix.wav")'))")
ffmpeg -nostdin -v error -y -i "$tmp/mix.wav" -af \
 "volume=${gain}dB,aresample=192000,alimiter=limit=0.794:attack=1:release=60:level=disabled,aresample=48000" "$tmp/final.wav"
# the limiter shaves a little loudness off; one correction pass puts it back
fix=$(python3 -I -c "print(-14 - float('$(meas "$tmp/final.wav")'))")
ffmpeg -nostdin -v error -y -i "$tmp/final.wav" -af \
 "volume=${fix}dB,aresample=192000,alimiter=limit=0.794:attack=1:release=60:level=disabled,aresample=48000" "$tmp/final2.wav"
mv "$tmp/final2.wav" "$tmp/final.wav"

ffmpeg -nostdin -v error -y -i "$video" -i "$tmp/final.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$out"
echo "wrote $out"
bash "$(dirname "$0")/qa_audio.sh" "$out"

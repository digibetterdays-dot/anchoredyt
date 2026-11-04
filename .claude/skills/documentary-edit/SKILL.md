---
name: documentary-edit
description: Edit a documentary-style video from the owner's own voiceover and still images (no stock or scraped footage) into a finished HyperFrames render - word-timed cuts, camera moves on stills, chapter cards, captions, music ducking, loudness to YouTube spec and a QA pass. Use for long-form explainers and Shorts on Bonus Chapter, The Money Question, Our Anchored Home, the Anchored reels, or any "here is my script and VO, make the visuals" request, including "documentary edit", "cut this to my voiceover", "make the timeline", "edit the Cascadia video".
---

# Documentary edit

Turns **script + voiceover + owner-supplied stills** into a rendered video. The owner supplies every image and the voice; this skill never downloads footage or images from the web. Edit decisions come from the rules in `references/edit-grammar.md`; read it before planning shots.

Scripts live in `scripts/` next to this file (`<SKILL>` below). Run Python with `python3 -I`. HyperFrames commands follow the `hyperframes` / `hyperframes-cli` skills; keep `DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1`.

## Inputs

| Input | Where | Notes |
|---|---|---|
| Script | repo `.md` | Fact-checked already (repo rule: no claim without a source). Use the final narration text only. |
| Voiceover | `clips/<name>/assets/audio/voice.wav` | One file for the whole video. If the VO is Kokoro lines, concatenate them first (see below). |
| Stills | `clips/<name>/assets/shots/<id>.png` | Owner generates from the prompt list this skill writes. |
| Music (optional) | `clips/<name>/assets/audio/music.mp3` | Owner-supplied or a licence the owner confirms. Never assume a track is free to use. |

## Workflow

### 1. Shot list (`clips/<name>/shots.json`)
Read the script and break it into shots using the edit grammar: one shot per idea or image change, a new shot on every named place, person, number or turn in the story. Write `shots.json` (schema in `references/shot-list.md`). Each shot's `anchor` is the **first 3-6 words of narration where that shot begins**, copied exactly from the script.

Then write the owner's prompt list:
```bash
python3 -I <SKILL>/scripts/doc_edit.py prompts clips/<name>/shots.json -o clips/<name>/PROMPTS.md
```
Stop here and hand `PROMPTS.md` to the owner. Wait for the stills. Check each arrival: aspect (crop a portrait panel out of a landscape canvas if needed), no text or watermarks in the art, matches the style line. Ask for re-sends rather than shipping a weak shot.

### 2. Voice timing
Get word-level timestamps from the actual VO (never estimate from the script):
```bash
cd clips/<name> && npx --yes hyperframes@0.9.6 transcribe assets/audio/voice.wav --model small.en
```
The first run downloads a whisper model (~466 MB): **tell the owner before starting it**. Save the word array as `words.json`. Spot-check 3 words against the audio; if the transcript is off by more than ~0.2 s, re-run with `medium.en`.

**If transcription can't run** (e.g. huggingface.co blocked by the network policy) and the VO follows the script word for word, align the script to the audio's pauses instead:
```bash
python3 -I <SKILL>/scripts/align_text.py VO-SCRIPT.txt assets/audio/voice.wav -o words.json
```
It prints the fit error per stretch and warns where the VO seems to differ from the script. Sentence and clause starts land on real pauses; mid-clause words are interpolated, so prefer anchors that start a sentence or follow a comma. Tell the owner the timings came from alignment, not transcription.

Concatenating Kokoro lines into one file (0.35 s pause between lines):
```bash
ffmpeg -f lavfi -t 0.35 -i anullsrc=r=24000:cl=mono -y gap.wav
# list.txt: file 'v1.wav' / file 'gap.wav' / file 'v2.wav' ...
ffmpeg -f concat -safe 0 -i list.txt -c copy voice.wav
```

### 3. Plan the edit
```bash
python3 -I <SKILL>/scripts/doc_edit.py plan clips/<name>/shots.json clips/<name>/words.json
```
This writes `edl.json`. It snaps each cut into the pause before its anchor word (or 0.08 s ahead of it), splits stills that hold too long into punch-in segments on phrase breaks, and gives each still a camera move with no back-to-back repeats. It exits non-zero and prints `PROBLEM:` lines for anchors it cannot find or shots that are too short. Fix `shots.json` (usually an anchor that doesn't match the spoken words) and re-run. Read the pacing report: an average shot length over ~6 s (long form) or ~3 s (Shorts) means the shot list is too thin.

### 4. Build and look
```bash
python3 -I <SKILL>/scripts/doc_edit.py build clips/<name>/edl.json
```
Copy `assets/vendor/gsap.min.js` from an existing clip if missing (the sandbox blocks the CDN). Then `npx --yes hyperframes@0.9.6 check --json` and `snapshot` at the hook (0-5 s), each chapter card and three random points. Fix by editing `shots.json` (`move`, `focus`, `emphasis`, `anchor`) and re-running plan + build, not by hand-editing `index.html`, so re-runs don't lose fixes.

### 5. Render, finish audio, QA
```bash
npx --yes hyperframes@0.9.6 render            # -> renders/<name>_<stamp>.mp4
bash <SKILL>/scripts/finish_audio.sh renders/<file>.mp4 assets/audio/voice.wav renders/<name>-final.mp4 [assets/audio/music.mp3]
bash <SKILL>/scripts/contact_sheet.sh renders/<name>-final.mp4 renders/<name>-sheet.jpg 5
python3 -I <SKILL>/scripts/doc_edit.py srt words.json -o renders/<name>.srt
```
`finish_audio.sh` levels the voice, ducks the music under it, normalises to -14 LUFS / -1.5 dBTP and runs `qa_audio.sh` (loudness, peak, dead air over 1.5 s, clipping). Look at the contact sheet: no repeated image back to back, no black frames, labels visible, captions inside the safe area.

### 6. Report honestly
Tell the owner: the final file path, length, shot count, average shot length, the QA results, and **what was not checked** (e.g. "audio QA passed by meter; nobody has listened to it yet"). Never call a render finished if `qa_audio.sh` failed.

## Rules that override everything else
- **Owner's images and voice only.** No web-scraped footage, stock or images, and no copyrighted clips.
- **Label illustrations.** Every still depicting a real event, person or place carries the `Illustration` tag (on by default; `label: null` only for pure graphics such as a chapter card or map). Never present generated art as archival footage.
- **On-screen numbers come from the script's sourced figures**, word for word, with `source` set on that shot. No new facts get added during the edit.
- **Altered/synthetic disclosure:** when uploading, tick YouTube's altered or synthetic content box if any realistic-looking AI image shows a real place, event or person. Put this in the upload notes.
- **No paid services or keys** (Gemini, ElevenLabs, HeyGen) unless the owner says so for this video.

## Files
- `references/edit-grammar.md`: the editing rules (cut timing, shot length, moves, cards, pacing per section, Shorts vs long form).
- `references/shot-list.md`: `shots.json` schema with an example.
- `scripts/doc_edit.py`: `prompts`, `plan`, `build`, `srt`.
- `scripts/finish_audio.sh`, `scripts/qa_audio.sh`, `scripts/contact_sheet.sh`.

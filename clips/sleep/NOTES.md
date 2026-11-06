# Why Do We Sleep?: production notes

Built with the `documentary-edit` skill. Fact check: `../../sleep-factcheck.md`.

## Status
- [x] Fact check (Nov 5): owner's draft confirmed; three fixes (cycle "about 90 minutes"; DEC2 "a mother and daughter"; newborn 14-17 h attributed to the National Sleep Foundation)
- [x] Script: `VO-SCRIPT.md` (chapters, delivery and pronunciation notes) / `VO-SCRIPT.txt` (plain, for the VO app). 2,011 words, about 12-13 min (snoring added to Ch. 3 and unwanted-memories beat to Ch. 5 on Nov 5).
- [x] Shot list: `shots.json`, 109 shots (93 images, 8 chapter cards, 8 overlays); anchors tested against an estimated timing (avg 5.1 s per shot)
- [x] Prompts: `PROMPTS.md`, 93 single-scene prompts
- [x] VO (Nov 6): owner's 3 parts joined in order (0.6 s gaps) -> `assets/audio/voice.wav`, 13:41. Joins land on chapter breaks (after Ch. 1, after Ch. 4).
- [x] Word timings: `words.json` by script-to-pause alignment. Fit: median 10%, 3 stretches over 50%.
- [x] Edit plan: `edl.json`, 165 segments, avg 5.0 s
- [x] 93 of 93 stills filed. Final shot z086: lone glowing house (owner approved Nov 6); child-at-window and framed versions kept in `assets/alt/`.
- [x] **Rendered (Nov 6):** `renders/sleep-final.mp4` (482 MB) and `renders/sleep-final-1080p-share.mp4` (103 MB), 13:41, 164 segments from 101 shots, avg 5.0 s. Audio QA: -14.24 LUFS, -1.49 dBTP, no dead air. Captions `renders/sleep.srt`. Contact sheet checked; nobody has watched or listened in full yet. Renders not in git.
- [x] Upload package: `UPLOAD.md` (long form vidIQ 99; chapters from the card times)
- [ ] Shorts rendering (Nov 6)

## Look
Same paper-cut house style; night palette (midnight navy, cream, one warm amber accent). Diagrams (brain, waves, DNA, clocks) carry no Illustration tag; scenes do.

## Shorts (from the same VO)
Cut by `make_short2.py` (scratchpad) from the long VO; ranges and per-image vertical framing in the scratchpad `sleep_shorts.py`, results in each project's `shots.json`.
1. `../sleep-short-teens`: "Why Teens Can't Fall Asleep Early" (vidIQ 88), 0:50, Ch. 2
2. `../sleep-short-rem`: "Why Your Body Can't Move When You Dream" (vidIQ 96), 0:49, Ch. 4
3. `../sleep-short-memories`: "Why Bad Memories Are Harder to Block When You're Tired" (vidIQ 95), 0:22, Ch. 5
4. `../sleep-short-snore`: "Why Do We Snore? What's Actually Vibrating" (vidIQ 88), 0:29, Ch. 3

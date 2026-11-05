# Cascadia long video: production notes

Built with the `documentary-edit` skill (`.claude/skills/documentary-edit/`). Script: `longform-scripts-yellowstone-cascadia.md`, Video 2.

## Status
- [x] Shot list: `shots.json`, 118 shots (82 new images, 33 cards, 3 reused images). `shots.json` is the source of truth.
- [x] Prompt list for the owner: `PROMPTS.md`
- [x] Anchors tested against the narration text (all found; estimated 12.0 min, 144 segments, average 5.0 s, no shot under 2 s)
- [x] **81 of 81 stills filed** (Nov 4; uploaded by the owner to branch `claude/sharp-ride-lwydum`, matched to shots by eye, resized to 1920 wide JPG q2). s069 cropped out of its paper frame. Alternates kept in `assets/alt/`.
- [x] All stills in. s053 (family looking back) never arrived: dropped; s052 holds through that line with a punch-in. Add it back to `shots.json` if a still is made later.
- [ ] Fact checks below, **before recording**
- [x] Voiceover: `assets/audio/voice.wav` (owner's two files joined with 0.6 s gap; 9:58)
- [x] Word timings: `words.json` from **script-to-pause alignment** (`align_text.py`), not transcription: huggingface.co is blocked here. Fit: median 12% per stretch, 3 stretches over 50%. Re-run with `hyperframes transcribe` if that host is allowed.
- [x] Edit plan: `edl.json`, 131 segments, average 4.6 s, shortest 1.9 s. Dropped s022, s035, s064 (too short at the real VO pace)
- [ ] Music bed (optional): `assets/audio/music.mp3`, a licence the owner confirms
- [x] **Rendered (Nov 5):** `renders/cascadia-final.mp4` (full quality, 344 MB) and `renders/cascadia-final-1080p-share.mp4` (102 MB), 9:58, 1920x1080. Audio QA passed: -14.8 LUFS, -1.21 dBTP, no dead air. Captions: `renders/cascadia.srt`. Renders are not in git (too large); re-render with `npx --yes hyperframes@0.9.6 render` + `finish_audio.sh`.
- [ ] Owner: watch and listen to the full cut (nobody has yet)

## Must verify before recording (these appear on screen)
| Card | Claim | Why open |
|---|---|---|
| `c07` | 10 to 15% in 50 years (USGS) | the fact sheet screenshot didn't show the numbers |
| `c18` | ODOT 2019 quote, shown word for word | only from a web-search summary |
| `c30` | 22 schools, about 2% of the need (2013) | from a summary of the schools chapter, not the Executive Summary |
| `c31` | 346 projects, close to $600 million (2025) | from a summary of testimony; counts may have changed |
| `c33` | Two weeks minimum | the current Oregon Emergency Management wording may differ |

If a figure changes, edit the card text in `shots.json` and the narration together. If the quote can't be verified, change `c18` to a paraphrase with no quotation marks.

## Retention plan items NOT built
- **"Real 3:00 timer" (Ch. 4): DROPPED (owner decision, Nov 2026).** Chapter 4's narration is about 1 minute, so a real 3-minute timer couldn't fit. Normal shots are used there.
- **"YOUR WINDOW" countdown bar (Ch. 6):** replaced by two separate cards (`c13` Oregon 10-30 min *from when shaking begins*, `c14` Washington 10-15 min *from when shaking stops*), keeping the script's rule never to mix the two on screen.
- **"If it happened today" recovery table (Ch. 7):** shown as four cards in a row (`c22`-`c25`).

## Cards (Nov 5 trim)
- 33 cards cut to **18 full cards** (9 chapter titles + c07 odds, c13/c14 tsunami windows, c18 ODOT quote, c20 deaths, c21 losses, c26 outages, c30/c31 schools). The other 15 are `overlay` lower-thirds on the art, ending with their sentence.
- Recovery overlays c23-c25 sit on reused stills (s071, s069, s072: ids s074r1-r3) so s074 doesn't hold 20 s.

## Image notes
- **s047:** cropped from a mixed image (US map + hiker + family); slightly soft at 1.7x upscale. Regenerate on its own if it looks soft in the render.
- **s017 (1700 wave):** styled like Hokusai's Great Wave (public domain, fine) but drawn far taller than the narration's "six to ten feet". Consider a smaller, calmer wave.
- **s012 / s020:** delivered 16:9 rather than tall map / panorama, so they get a normal push instead of a scan; s012 shows mainly Washington and BC, not the whole zone down to Cape Mendocino.
- Two tall maps (`s012`, `s047`) and seven 3:1 panoramas are scanned across, not cropped. `s012` plays south to north and `s020` plays right to left, matching the narration.
- Real places shown as illustrations (Seaside, Ocosta-style refuge, Japan 1700) all carry the `Illustration` tag. Maps and diagrams don't.
- No ghost-forest imagery (the script flags it as disputed); `s026` asks for "no dead trees".
- Reused images: `s033` = `s021` (1700 night coast), `s063` = `s009` (the trap callback), `s087` = `s001` (opening callback).

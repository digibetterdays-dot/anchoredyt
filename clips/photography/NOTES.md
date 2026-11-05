# When Photography Terrified the World: production notes

Built with the `documentary-edit` skill. Fact check: `../../photography-factcheck.md` (read it before changing any line).

## Status
- [x] Fact check (Nov 5): web-search level; primary pages blocked in the cloud session. Starred items there to re-check.
- [x] Script: `VO-SCRIPT.md` (with chapters and pronunciations) / `VO-SCRIPT.txt` (plain, for TTS). 1,333 words, about 9 min (revised Nov 5 with owner wording for claims 1-4).
- [x] Shot list: `shots.json`, 78 shots (59 images, 11 full cards, 8 overlays); anchors tested against estimated timing (avg 4.9 s per shot).
- [x] Prompts: `PROMPTS.md`, 59 single-scene prompts
- [ ] Owner: record VO as one file -> `assets/audio/voice.wav`, word for word
- [ ] Owner: generate the 59 stills -> `assets/shots/pNNN.png` (or upload to GitHub, this branch)
- [ ] Transcribe/align, plan, build, render, finish audio, QA; Shorts; upload package

## Titles (vidIQ)
- "When Photography Terrified the World" 85 (working title)
- "\"Painting Is Dead\": The Myths About the First Photograph" 91
- "The Invention That Painters Thought Would Kill Art" 85

## Archival option
p021 (Niépce's Le Gras heliograph, 1827) and p025 (Daguerre's Boulevard du Temple, 1838) can be the real public-domain images. If used, set `"label": null` on that shot in `shots.json` (it is a real photograph, not an illustration) and add the credit to the description.

## Rules for this video
- No illustration shows a real person as a likeness: Delaroche, Baudelaire, Daguerre, Niépce, Ferdinand II appear from behind, in silhouette or "illustrative, not a likeness".
- Never say: "the king banned photography", "because of the evil eye", "Delaroche said", "the first photograph ever", or the unsourced "stringent truth" quote.

## Shorts planned (from the same VO)
1. "Painting Is Dead" never said (Ch. 6, ~45 s): strongest hook.
2. The king who banned photography? (Ch. 5, ~50 s).
3. The first photograph took days (Ch. 2, ~45 s).

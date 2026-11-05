# When Photography Terrified the World: production notes

Built with the `documentary-edit` skill. Fact check: `../../photography-factcheck.md` (read it before changing any line).

## Status
- [x] Fact check (Nov 5): web-search level; primary pages blocked in the cloud session. Starred items there to re-check.
- [x] Script: `VO-SCRIPT.md` (with chapters and pronunciations) / `VO-SCRIPT.txt` (plain, for TTS). 1,336 words, about 9 min (revised Nov 5 with owner wording for claims 1-4).
- [x] Shot list: `shots.json`, 78 shots (59 images, 11 full cards, 8 overlays); anchors tested against estimated timing (avg 4.9 s per shot).
- [x] Prompts: `PROMPTS.md`, 58 single-scene prompts (p021 is the real image)
- [x] VO (Nov 5): owner's 3 parts joined in order (0.6 s gaps) -> `assets/audio/voice.wav`, 8:45. Joins land on chapter breaks (end of Ch. 1, end of Ch. 3).
- [x] Word timings: `words.json` by script-to-pause alignment (huggingface.co still blocked). Fit: median 10%, 8 stretches over 50% (VO may differ slightly from script there).
- [x] Edit plan: `edl.json`, 109 segments, avg 4.8 s
- [x] 58 of 59 images filed
- [ ] Owner: generate the remaining 1 stills -> `assets/shots/pNNN.png` (or upload to GitHub, this branch)
- [ ] Transcribe/align, plan, build, render, finish audio, QA; Shorts; upload package

## Titles (vidIQ)
- "When Photography Terrified the World" 85 (working title)
- "\"Painting Is Dead\": The Myths About the First Photograph" 91
- "The Invention That Painters Thought Would Kill Art" 85

## Archival images
- **p021 = the real Le Gras heliograph** (owner-supplied file, Nov 5), shown with no Illustration tag and an on-screen source line. The plate (c. 1827) is public domain; a faithful photo of a 2D public-domain work carries no new copyright in the US. The file is only 1024x576, so it will be soft on a 1080p screen: swap in a larger scan (Wikimedia Commons has high-resolution versions) under the same name if you can. It is the unretouched scan; don't use Gernsheim's retouched 1952 copy without saying so.
- **Credit for the description:** Joseph Nicéphore Niépce, *View from the Window at Le Gras*, c. 1827. Heliograph on pewter. Harry Ransom Center, The University of Texas at Austin (Gernsheim Collection). Public domain. *(Check the Ransom Center's own preferred credit wording on its site; it is blocked from the cloud session.)*

## Archival option
p021 (Niépce's Le Gras heliograph, 1827) and p025 (Daguerre's Boulevard du Temple, 1838) can be the real public-domain images. If used, set `"label": null` on that shot in `shots.json` (it is a real photograph, not an illustration) and add the credit to the description.

## Rules for this video
- No illustration shows a real person as a likeness: Delaroche, Baudelaire, Daguerre, Niépce, the king of Naples appear from behind, in silhouette or "illustrative, not a likeness".
- The king is not named in the script (owner decision, Nov 5): say "the king of Naples".
- Never say: "the king banned photography", "because of the evil eye", "Delaroche said", "the first photograph ever", or the unsourced "stringent truth" quote.

## Shorts planned (from the same VO)
1. "Painting Is Dead" never said (Ch. 6, ~45 s): strongest hook.
2. The king who banned photography? (Ch. 5, ~50 s).
3. The first surviving photograph: 8 hours, or several days? (Ch. 2, ~45 s). Don't title it "took days": that is one estimate.

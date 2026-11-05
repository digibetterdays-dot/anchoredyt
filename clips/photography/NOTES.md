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
- [x] 59 of 59 images filed
- [ ] Owner: generate the remaining 1 stills -> `assets/shots/pNNN.png` (or upload to GitHub, this branch)
- [x] **Rendered (Nov 5):** `renders/photography-final.mp4` (379 MB) and `renders/photography-final-1080p-share.mp4` (107 MB), 8:45, 105 segments. Audio QA: -14.35 LUFS, -1.66 dBTP, no dead air. Captions `renders/photography.srt`. Renders not in git.
- [x] p031e (café table) arrived after the first render; v2 render has all 59 stills.
- [ ] Owner: watch/listen to the full cut; then Shorts and upload package

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

## Shorts planned (from the same VO; reframed Nov 5 so each title rests on documented fact)
1. **"Painting Is Dead" was never said** (Ch. 6, ~45 s). Verified: first in print 30+ years later; Delaroche's 1839 report praised the process.
2. **"The Oldest Surviving Photograph Is a Blur. Here's Why"** (Ch. 2, ~45 s, vidIQ 90). Replaces "8 hours or several days?". Substance: Niépce's plate, sunlight on both sides of the courtyard because the exposure ran so long, earliest surviving camera photograph (Ransom Center). The exposure estimate appears once, as "hours, possibly days", not as the hook.
3. **"Why Painters and Their Sitters Feared the First Cameras"** (Ch. 4, ~45 s, vidIQ 89; owner's angle, Nov 5). Two fears: painters lost a living (portrait trade, Baudelaire 1859); sitters saw their real faces, which a painter would have softened. Visuals p029, p031, p031c, p031d, p030, c07 (Baudelaire card).
   - Sources for the sitters' side (added Nov 5, search level): Getty "Focus: Daguerreotypes" gallery text (sitters frustrated with grey complexions); Carol Shloss, "The Inconstant Daguerreotype" (subjects' common disappointment with their images), via a UConn dissertation; 1839 New York Observer praising portraits made without the "flattering pencil"; long exposures, head rests, fixed stares. Say "disappointed / unsettled" in narration; "feared" is the title's word for both groups together.
   - Alternative: "The First Cameras Scared Painters and Shocked Their Sitters" (vidIQ 87).

# Cascadia long video: production notes

Built with the `documentary-edit` skill (`.claude/skills/documentary-edit/`). Script: `longform-scripts-yellowstone-cascadia.md`, Video 2.

## Status
- [x] Shot list: `shots.json`, 121 shots (85 new images, 33 cards, 3 reused images)
- [x] Prompt list for the owner: `PROMPTS.md`
- [x] Anchors tested against the narration text (all found; estimated 12.0 min, 144 segments, average 5.0 s, no shot under 2 s)
- [ ] Owner: generate the 85 stills into `assets/shots/` (names as in `PROMPTS.md`)
- [ ] Fact checks below, **before recording**
- [ ] Voiceover: one file at `assets/audio/voice.wav`
- [ ] Music bed (optional): `assets/audio/music.mp3`, a licence the owner confirms
- [ ] Transcribe, plan, build, render, finish audio, QA (skill steps 2-5)

## Must verify before recording (these appear on screen)
| Card | Claim | Why open |
|---|---|---|
| `c07` | 10 to 15% in 50 years (USGS) | the fact sheet screenshot didn't show the numbers |
| `c18` | ODOT 2019 quote, shown word for word | only from a web-search summary |
| `c30` | 22 schools, about 2% of the need (2013) | from a summary of the schools chapter, not the Executive Summary |
| `c31` | 346 projects, close to $600 million (2025) | from a summary of testimony; counts may have changed |
| `c33` | Two weeks minimum | the current Oregon Emergency Management wording may differ |

If a figure changes, edit the card text in `shots.json` and the narration together. If the quote can't be verified, change `c18` to a paraphrase with no quotation marks.

## Retention plan items NOT built (owner decision)
- **"Real 3:00 timer, one held shot" (Ch. 4):** Chapter 4's narration is about 1 minute, so a real 3-minute timer can't run inside it without about 2 minutes of silence. The shot list uses normal shots there. Options: drop it, or show a running clock overlay only for the length of the chapter.
- **"YOUR WINDOW" countdown bar (Ch. 6):** replaced by two separate cards (`c13` Oregon 10-30 min *from when shaking begins*, `c14` Washington 10-15 min *from when shaking stops*), keeping the script's rule never to mix the two on screen.
- **"If it happened today" recovery table (Ch. 7):** shown as four cards in a row (`c22`-`c25`).

## Image notes
- Two tall maps (`s012`, `s047`) and seven 3:1 panoramas are scanned across, not cropped. `s012` plays south to north and `s020` plays right to left, matching the narration.
- Real places shown as illustrations (Seaside, Ocosta-style refuge, Japan 1700) all carry the `Illustration` tag. Maps and diagrams don't.
- No ghost-forest imagery (the script flags it as disputed); `s026` asks for "no dead trees".
- Reused images: `s033` = `s021` (1700 night coast), `s063` = `s009` (the trap callback), `s087` = `s001` (opening callback).

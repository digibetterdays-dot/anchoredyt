# Edit grammar for documentary edits from stills

These are the rules `doc_edit.py plan` encodes, plus the ones that need judgment when writing the shot list. When a rule and the story disagree, the story wins, but say which rule you broke and why.

## 1. Where cuts go
- **Cut on the word that changes the picture.** The anchor is the first word of the phrase the new image illustrates, never the middle of a phrase.
- **Cut in the breath.** If there is a pause (> 0.25 s) before the anchor word, the cut lands mid-pause. Otherwise it lands 0.08 s before the word. A picture arriving slightly before its word reads as intentional; one arriving after reads as late.
- **One idea per shot.** New shot for every new place, person, date, number, or turn ("But...", "Then...", "Except...").
- **Never cut twice inside 1.2 s (Shorts) or 2 s (long form)**, except a deliberate rapid montage (list of 3+ items, each its own image).

## 2. Shot length
| | Long form (16:9) | Shorts (9:16) |
|---|---|---|
| Typical | 3-6 s | 1.5-3 s |
| Hard max on one framing | 7 s | 3.5 s |
| Hook (first 15 s / first 3 s) | 2-3 s | 1-1.5 s |

Cards (chapter titles, figures) may hold up to 13 s long-form / 6 s Shorts while the sentence explaining the figure plays; they drift slowly so the frame never freezes. Past that, follow the card with an image.

A still held past the max gets a **punch-in**: same image, cut to a tighter crop (scale ~1.35) on a phrase break. That reads as a new shot without needing new art. More than two punch-ins on one image means the shot list needs another image.

## 3. Camera moves on stills
| Move | Use for |
|---|---|
| `push_in` (slow zoom in) | default; building tension, focusing on a subject. Set `focus` to the subject. |
| `push_fast` | the reveal or punchline, a number landing, danger. Use with `emphasis: true`, at most once a minute. |
| `pull_out` | revealing scale or context ("...and it covers 700 miles"), endings. |
| `pan_left` / `pan_right` | landscapes, maps, wide scenes, a line of things. Pan in the direction of travel in the story. |
| `tilt_up` / `tilt_down` | tall subjects (towers, cliffs, people), or rising/falling (eruption column up, tsunami down). |
| `hold` | almost still; quotes, sad or reflective beats. |
| `hold_punch` | auto: the tight half of a punch-in split. |
| `scan` | auto when an image is far off the frame shape (e.g. a 16:9 still in a Short): fits one side and travels across the whole image, so nothing is cropped away. Never split into punch-ins. Order the content in the image left-to-right (or top-to-bottom) in story order. |

Rules: never the same move twice in a row; avoid three zoom-ins in a row; moves are linear (no ease) so cuts between them feel continuous; the strength stays inside 12% overscan so image edges never show. If the subject sits off-centre, set `focus: [x, y]` (0-1) so zooms land on it.

## 4. Transitions
- **Hard cut** is the default. Documentaries cut; fades read as slideshow.
- **Crossfade (0.45 s)** only at a `section_start` (new chapter, time jump, shift in mood).
- **Chapter card** (`type: card`): black card, serif title, optional small subtitle. Long form only, one per chapter, 2-3 s, over a pause in the VO. Shorts never get chapter cards.

## 5. Text on screen
- **Numbers and dates** that carry the story get a card or a `source` caption: "1,250 to more than 10,000 deaths", with source "Oregon Resilience Plan". Copy figures exactly from the script.
- **Shorts** get burned-in captions (3 words a group, punctuation breaks a group), placed in the lower-middle safe area, clear of the UI at the bottom.
- **Long form** gets no burned-in captions; upload the SRT instead.
- `Illustration` tag top-left on every generated still of a real subject.

## 6. Pacing by section
| Section | Shot rhythm | Moves |
|---|---|---|
| Hook | fastest; a new image every 2-3 s (long) / 1-1.5 s (Short) | `push_fast` on the hook line |
| Context/background | 4-6 s | pans and slow pushes |
| Build-up | lengths shrink toward the turn | push-ins |
| Climax / key fact | one `emphasis` shot, then a 1-2 s hold | `push_fast`, then `hold` |
| Aftermath / reflection | longest shots, 5-7 s | `pull_out`, `hold` |
| Outro / CTA | 1-2 shots | `pull_out` |

**Pattern interrupt:** in long form something must change at least every 30-45 s beyond a normal cut: a card, a map, a number on screen, or a change in the look (e.g. night scene, close-up detail). Note these in the shot list.

## 7. Image prompts (for the owner)
- One subject, clear silhouette, room around it (the edit zooms 15-40%).
- Same style line on every prompt; same lighting and palette within a chapter.
- No text in images (wrong spellings, and text can't be fact-checked); any text goes on screen in the edit.
- Ask for variety in framing across consecutive shots: wide, medium, detail.
- Realistic depictions of real disasters or real people need extra care: prefer illustrative styles (paper-cut, watercolour) that can't be mistaken for photos.

# Handoff: Bonus Chapter Channel (8 videos)

Repo: `digibetterdays-dot/anchoredyt`, branch **`claude/great-fermat-0hw2w1`** (latest; includes the older `claude/sharp-ride-lwydum` work). Everything below is committed there. Start the new chat by telling Claude to read this file first.

## Goal
Eight faceless explainer videos for the "bonus chapter" channel, US audience: 3 Shorts and 5 long videos. Illustrated (paper-cut), free local voiceover, fact-checked scripts. Rule: illustrations are labeled "Illustration" and are never presented as archival footage.

## Status

### Finished (3 Shorts, rendered MP4, 1080x1920)
| Short | File | Length |
|---|---|---|
| Ambulance backwards | `clips/ambulance-test/renders/ambulance-test_2026-11-02_21-53-16.mp4` | 35 s |
| Stop signs octagon | `clips/stop-sign-short/renders/stop-sign-short_2026-11-02_22-44-35.mp4` | 34.5 s |
| School bus yellow | `clips/school-bus-short/renders/school-bus-short_2026-11-02_22-46-30.mp4` | 44 s |

Known issues: audio never listened to (frames checked only). Stills only, slow zoom/pan (no video clips from owner). Stop-sign shot 01 and bus shot 01 are smooth vector style, not paper-cut; bus shot 07 has a cream band at the bottom. Ambulance uses flat shapes, no generated art.

### Pipeline (5 long videos; scripts done, no visuals/voice/render yet)
| Order | Video | Script | Narrated length | Status |
|---|---|---|---|---|
| 1 | Cascadia ("What If the Cascadia Fault Ruptured Tomorrow?") | `longform-scripts-yellowstone-cascadia.md` | ~11.3 min | **Rendered** (`clips/cascadia/renders/`, local only); awaiting owner review and the 5 fact checks before upload; see `clips/cascadia/NOTES.md` |
| 2 | Yellowstone ("If Yellowstone Erupted Tomorrow, This Is What Happens") | same file | ~7.8 min | Queued |
| 3 | Eggs ("Why Americans Refrigerate Eggs (and Brits Don't)") | `longform-scripts-eggs-911-asteroid.md` | ~5.4 min | Queued |
| 4 | 911 ("Why 911 Is the Emergency Number") | same file | ~4.2 min | Queued |
| 5 | Asteroid ("What If a 1-km Asteroid Hit New York?") | same file | ~5.7 min | **Blocked** |

Asteroid decisions needed from owner: (1) ground zero (central Manhattan or elsewhere), (2) land or ocean impact (model is land only, no tsunami model), (3) add a sourced aftermath section or end after the blast. Its Chapter 6 ("days to years") has no sourced figures; suggest cutting or merging.

## Files
- `bonus-chapter-topics.md`: the original 8 topics.
- `bonus-chapter-production-plan.md`: format split, fact-check per topic, vidIQ keyword and title research.
- `shorts-narration-scripts.md`: three Short scripts with shot tables.
- `longform-scripts-yellowstone-cascadia.md`, `longform-scripts-eggs-911-asteroid.md`: long scripts, each with retention plan, fact notes, "Do NOT say" lists, remaining checks.
- `asteroid_impact_model.py`: Collins/Melosh/Marcus 2005 equations, validated against the paper's Table 6. Results (1 km stony, 45 deg, 17 km/s, bedrock): ~54,000 Mt, crater ~14 km, magnitude ~7.8, fireball ~12 km.
- `clips/PROMPTS-stop-sign-and-school-bus.md`: image and video prompt format used for the Shorts (owner generates stills; style line, no text in images).
- `clips/<name>/`: HyperFrames projects (`index.html`, `assets/`, `renders/`).
- `.claude/skills/`: installed clip skills (see below). `.claude/skills/README.md` has provenance and rules. `.claude/settings.json` sets telemetry opt-out.

## Titles (vidIQ scores)
Ambulance Short "Why AMBULANCE Is Written Backwards" 92. Stop sign "The Real Story Behind the 8-Sided Stop Sign" 90. School bus "Why Every School Bus Is the Same Yellow" 96. Yellowstone "If Yellowstone Erupted Tomorrow, This Is What Happens" 89. Cascadia 90. Eggs 90. Asteroid 90. 911 85. Demand notes: Cascadia (~38.8k searches/mo, +447%) and Yellowstone (~10k, +183%) are search-led; "why americans refrigerate eggs" (~9.3k) beats "why are american eggs refrigerated".

## Tools and how the pipeline works
1. Owner generates stills (image prompts from me), sends them in chat. Files sometimes fail to arrive: check the newest file in `/tmp/claude-0/-home-user-anchoredyt/<session>/images/`; ask for re-sends. Stills arrive as landscape canvases with a portrait panel inside: crop the panel.
2. Voice: free local Kokoro. Setup (lives in `/tmp`, redo each session): `python3 -m venv /tmp/kvenv && /tmp/kvenv/bin/pip install kokoro-onnx soundfile`, then `HYPERFRAMES_PYTHON=/tmp/kvenv/bin/python npx --yes hyperframes@0.9.6 tts "<line>" --output assets/audio/vN.wav`.
3. Build: HyperFrames (`npx --yes hyperframes@0.9.6 check --json`, `snapshot --at ...`, `render`). Always set `DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1`. The sandbox blocks the GSAP CDN: copy `gsap.min.js` from the hyperframes npm cache into `assets/vendor/` and reference it locally. Node 22, ffmpeg and Chrome are present.
4. Installed skills: `hyperframes` (+cli, registry, media-use, slideshow), `claude-animation-base`, `lemo-opuscar` (setup pinned to reviewed commit), `eian-collage-broll`, `gbro-collage-broll` (**do not use: needs paid Gemini key; owner has none**). Not installed: `onetake` (noncommercial license). Never use paid keys or runtime downloads without owner OK. Do not run `hyperframes feedback`.

## Owner preferences and decisions
- Stop-sign Short: the "recognized from behind" claim is DROPPED.
- No paid services (no Gemini). Owner generates images and (optionally) video; asks for prompts.
- "Enough experiments, build the videos." Owner declined adopting a stage-gated workflow (from the Jacksons AI video, Nov 2026) for now.
- Be honest about limits: no claim without a source; report what was not verified.

## Fact-check state (long videos)
Primary-sourced (documents the owner supplied): Oregon Resilience Plan Executive Summary (fatalities "1,250 to more than 10,000", >$30B, recovery table, two-week prep), NASA NEO infographic Dec 1 2025 (876 over 1 km, ~50 left; 11,493 over 140 m, ~14,000 left), NENA 911 statistics (5,748 PSAPs / 3,135 counties as of Feb 2021; ~240M calls/yr), NOAA Cascadia page (700 miles), Washington outer-coast tsunami page (10-15 min after shaking stops; an hour+ to walk), FDA key-temperatures graphic (untreated shell eggs 45 F), the Collins et al. paper.
Secondary only (web-search summaries): most USGS claims (10-15% in 50 yrs, Yellowstone hazards/ash/monitoring), Biscuit Basin 2024, 911 history (Haleyville 2/16/1968, AT&T 1/12/1968, "unused code" reasons), EU egg-washing rule (Reg. 589/2008, being replaced by 2023/2465), FSA 2017 Lion eggs advice, FDA 2004 vaccination (AVMA report), FCC 2024 call counts, ODOT 2019 quote ("can't get fuel until the bridges are fixed..."), seismic grant counts (22 schools 2013; 346 projects ~$597M 2025).
Still open: Haleyville names/spellings, 1967 commission, FCC report, USDA washing rule (7 CFR 56), UK law on washing, ShakeAlert Cascadia warning time (not used), ghost-forest evidence (left out, disputed), Yellowstone magma-melt percentages and YVO warning wording, Pinatubo cooling figure.
Never say: "overdue", per-year Yellowstone odds, single Cascadia death figure, "I-5 corridor", "from behind" (stop sign), "1.24x peripheral vision" (bus), rotary-dial 911 explanations, UK egg case counts, inventor/year for ambulance lettering.

## START HERE (local session on the owner's computer, Nov 2026)
Cascadia is moving to a session on the owner's computer because the stills are too large to upload to the cloud session. Status: voice recorded and timed, edit planned, animatic rendered and approved for review. Only the stills are missing.

1. **Get the stills.** Ask the owner for the folder path. Copy each into `clips/cascadia/assets/shots/` as `sNNN.png` (convert JPG/WebP with ffmpeg; downscale anything over 2x the frame: normal stills to 1920 wide, panoramas `s020 s036 s044 s052 s059 s068 s081` to 3240 wide, tall maps `s012 s047` to 1080 wide). 82 expected (s001 already there); s022, s035, s064 were dropped. Check each: right aspect (`PROMPTS.md` lists the odd ones), no text or watermark, style matches `s001.png`. List missing or doubtful ones for the owner.
2. **Timing re-check (optional, needs internet):** `words.json` came from script-to-pause alignment (`.claude/skills/documentary-edit/scripts/align_text.py`) because the cloud session couldn't download Whisper. Locally, run `npx --yes hyperframes@0.9.6 transcribe assets/audio/voice.wav --model small.en --engine whisper` (ask before the ~466 MB model download), compare anchor times, and switch if cuts move by more than ~0.3 s.
3. **Build and render** with the `documentary-edit` skill, steps 4-5 (`SKILL.md`): `plan` -> `build` -> `npx --yes hyperframes@0.9.6 check --json` -> snapshots -> `render` -> `finish_audio.sh` -> `contact_sheet.sh` -> `srt`. Set `focus` in `shots.json` for off-centre subjects after looking at each still. Keep `DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1`.
4. **Before publishing:** the 5 on-screen fact checks in `clips/cascadia/NOTES.md` are still open; the owner hasn't listened to the full mix yet.
5. Commit and push to `claude/great-fermat-0hw2w1` (renders can stay local if large).

Tools needed locally: Node 22+, ffmpeg/ffprobe, Python 3, Chrome (HyperFrames uses it). Ask before installing anything.

## Queue: When Photography Terrified the World
Script, fact check, shot list and prompts done (`clips/photography/`, `photography-factcheck.md`). Waiting on the owner's VO and 59 stills. See `clips/photography/NOTES.md`.

## Next steps (after Cascadia)
0. (done: see START HERE) Cascadia timing check (if huggingface.co is now reachable: `curl -sI https://huggingface.co`): in `clips/cascadia`, run `npx --yes hyperframes@0.9.6 transcribe assets/audio/voice.wav --model small.en --engine whisper`, save the words as `words-whisper.json`, compare anchor times against `words.json` (from script-to-pause alignment), switch to the transcript if they differ, re-run `doc_edit.py plan` + `build`, and report which cuts moved.
1. Cascadia: owner generates the stills in `clips/cascadia/PROMPTS.md`; clear the 5 on-screen fact checks in `clips/cascadia/NOTES.md`; record voice; then run the `documentary-edit` skill steps 2-5.
2. Repeat for Yellowstone, eggs, 911.
3. Asteroid: get the three decisions first.
4. Optional: replace smooth-style shots, swap in real image-to-video clips, listen to all audio, upload package (titles, descriptions, tags, pinned comments, sources).

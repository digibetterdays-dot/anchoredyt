# Project skills for clip production

Installed from public GitHub repos after a manual code review (shell/Python/JS scripts scanned for downloads-and-execute, credential reads, hidden network calls and prompt-injection phrasing; none found). Third-party code, so treat updates as a new review.

| Skill folder | Upstream | License | Reviewed commit | Notes |
|---|---|---|---|---|
| `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `slideshow` | heygen-com/hyperframes (`skills/`) | Apache-2.0 | 4ef8c1de5cfc298bdbd385decd3a95b0ef301adc | HTML-to-video. Runs `npx hyperframes ...` (downloads the npm package at run time; needs Node 22+ and ffmpeg). Test files removed. Not installed: `figma`, `reverse-any-video`, `remotion-to-hyperframes` (not needed) |
| `claude-animation-base` | JohnHeibel/ClaudeAnimationBase | MIT | 0ac8bf2b31942376cb6b8c4074715595d512acd2 | Upstream has no SKILL.md; `SKILL.md` here is written locally. Lockfile omitted |
| `lemo-opuscar` | lemomo-ai/lemo-opuscar (`plugin/skills/lemo-opuscar`) | MIT | bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00 | Fetches the style library from GitHub on first use and runs `npm install`. **Local change:** `scripts/setup.sh` is pinned to the reviewed commit instead of following upstream `main` (override with `LEMO_OPUSCAR_REF`) |
| `eian-collage-broll` | YIAN6557/eian-collage-broll | MIT | 9e6dd8b6c53a8d82a47c80aac3bd9eadf9806dbe | Paper-collage b-roll prompt packs (blank first frame, confirmed last frame, video prompt). Needs an image generator (upstream assumes Codex `image_gen`; here use an available image tool). No API key in the skill. Written in Chinese; Gate 1 / Gate 2 approvals are required |
| `gbro-collage-broll` | pyang5166/gbro-collage-broll | MIT | a1a4ee2e2abf7d44e460026b706d0c72c2cf8a91 | Halftone paper-collage b-roll, 3 gates (metaphor, still, then video). **Paid:** step 3 calls Gemini (`gemini-omni-flash-preview`) with `GEMINI_API_KEY`, billed to that Google account. Scripts only talk to generativelanguage.googleapis.com and ffmpeg. Chinese-language instructions. Same trigger phrases as `eian-collage-broll`: name the one you want. **Owner has no Gemini subscription or key: do NOT use this one; use `eian-collage-broll`.** |

## Deliberately NOT installed

- **onetake** (feitangyuan/onetake): licensed **PolyForm Noncommercial 1.0.0**. A monetized channel is commercial use, so it was left out. Install only if the channel is non-commercial or the author grants permission.
- **paper-collage-animation** (cameronha): no license file and no SKILL.md.

## Rules for using these skills

- **Telemetry:** HyperFrames CLI and media-use send coarse usage events to PostHog unless opted out. `.claude/settings.json` sets `DO_NOT_TRACK=1` and `HYPERFRAMES_NO_TELEMETRY=1`. Keep them.
- **Do not run** `npx hyperframes feedback` (sends data to the maintainers) or enable on-device search downloads without asking the user.
- **Paid or keyed services** (Gemini, ElevenLabs, HeyGen, cloud render): only with the user's explicit OK and their own keys.
- **Third-party downloads at run time** (npm packages, the lemo library, browsers, models): say so before starting.
- **Honesty rule for this channel:** animated or code-made visuals must be labeled as illustrations when depicting real events; never pass them off as archival footage.

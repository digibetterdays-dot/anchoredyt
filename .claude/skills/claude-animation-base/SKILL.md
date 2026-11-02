---
name: claude-animation-base
description: Make short hand-painted 2D cartoon animations (p5.js + p5.brush, the "Clawd" character, 31 acted emotions) rendered to MP4 with Node, Chrome and ffmpeg. Use when the user wants a hand-drawn or painted animated cartoon clip, a character-driven animated Short, or animated b-roll in a brush/watercolour look, and says "claude animation base" or similar. Not for photoreal footage or archival-looking imagery.
---

# Claude Animation Base

Local wrapper written for this repo around JohnHeibel/ClaudeAnimationBase (MIT, reviewed at commit 0ac8bf2b31942376cb6b8c4074715595d512acd2). The upstream kit is in this folder: `ANIMATION_GUIDE.md`, `src/`, `render.mjs`, `studio.html`, `docs/`.

## How to use

1. Read `ANIMATION_GUIDE.md` in this folder first. It holds the rules (storyboard before code, transitions always, something happens in every scene, no text in the painting).
2. Copy this folder to a working project folder (for example `clips/<name>/`) before editing so the skill copy stays clean.
3. Storyboard, then build shot by shot, render contact sheets to check your own work (`node render.mjs --sheet=0,1,2 --out=out/sheet.jpg`), then render (`node render.mjs --clip --out=out/video.mp4`).
4. Needs Node.js, Google Chrome (puppeteer-core) and ffmpeg. Run `npm install` in the working copy. Without a GPU, p5.brush watercolour fills render slowly; avoid them.

## Channel rules that override the guide

- This channel's rule: illustrated visuals must read as illustrations. Never present animation as archival footage or real photos. Put "illustration" labels on scientific scenes when a script note asks for it.
- Facts come from the scripts in this repo, not from the animation. Animate the narration; do not invent claims in the picture.
- Review `package.json` dependencies before `npm install` (p5, p5.brush, puppeteer-core at review time).

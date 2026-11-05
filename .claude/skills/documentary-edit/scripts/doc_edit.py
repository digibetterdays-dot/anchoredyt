#!/usr/bin/env python3
"""Documentary edit planner and composition builder for HyperFrames.

Subcommands (run with `python3 -I doc_edit.py <cmd> ...`):
  prompts <shots.json>                      -> Markdown image-prompt list for the owner
  plan    <shots.json> <words.json> [-o edl.json]
                                            -> timed edit decision list + pacing report
  build   <edl.json> [-o index.html]        -> HyperFrames composition
  srt     <words.json> [-o captions.srt]    -> SRT captions for YouTube upload

Standard library only. See ../SKILL.md for the workflow and
../references/edit-grammar.md for the rules encoded here.
"""
import argparse, html, json, os, re, subprocess, sys

FORMATS = {
    # max_shot: longest a single still may hold before a punch-in split
    # min_shot: shortest shot allowed (merge into neighbour if shorter)
    "long":  {"w": 1920, "h": 1080, "max_shot": 7.0, "max_card": 13.0, "min_shot": 2.0, "captions": False},
    "short": {"w": 1080, "h": 1920, "max_shot": 3.5, "max_card": 6.0, "min_shot": 1.2, "captions": True},
}
MOVES = ["push_in", "pan_right", "pull_out", "pan_left", "tilt_down", "push_in", "tilt_up", "pan_right"]
LEAD = 0.08        # cut this many seconds before the anchor word starts
TAIL = 0.6         # hold after the last word
XFADE = 0.45       # crossfade length at section changes


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def norm(t):
    return re.sub(r"[^a-z0-9']", "", t.lower().replace("’", "'"))


def load_words(p):
    data = load_json(p)
    if isinstance(data, dict):
        data = data.get("words") or data.get("segments") or []
    words = [w for w in data if norm(w.get("text", ""))]
    if not words:
        sys.exit(f"no words in {p}")
    return words


def audio_duration(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", path], capture_output=True, text=True, check=True)
        return float(out.stdout.strip())
    except Exception:
        return None


def find_anchor(words, anchor, start_idx):
    """Index of the first word of `anchor` at or after start_idx. Tolerates one
    mismatched token (transcription errors) for anchors of 3+ words."""
    toks = [norm(t) for t in anchor.split() if norm(t)]
    if not toks:
        return None
    n = len(toks)
    for i in range(start_idx, len(words) - n + 1):
        got = [norm(words[i + k]["text"]) for k in range(n)]
        miss = sum(a != b for a, b in zip(got, toks))
        if miss == 0 or (n >= 3 and miss == 1 and got[0] == toks[0]):
            return i
    return None


def crop_loss(img_aspect, frame_aspect):
    return 1 - min(img_aspect, frame_aspect) / max(img_aspect, frame_aspect)


def image_size(path):
    """(w, h) for PNG/JPEG using only the standard library, else None."""
    import struct
    try:
        with open(path, "rb") as f:
            head = f.read(26)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                return struct.unpack(">II", head[16:24])
            if head[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    m = f.read(4)
                    if len(m) < 4 or m[0] != 0xFF:
                        return None
                    seg = struct.unpack(">H", m[2:4])[0]
                    if m[1] in (0xC0, 0xC1, 0xC2):
                        h, w = struct.unpack(">xHH", f.read(5))
                        return (w, h)
                    f.seek(seg - 2, 1)
    except OSError:
        return None
    return None


# ---------------------------------------------------------------- prompts
def cmd_prompts(a):
    spec = load_json(a.shots)
    fmt = spec.get("format", "long")
    aspect = "16:9 landscape" if fmt == "long" else "9:16 portrait"
    style = spec.get("style", "")
    out = [f"# Image prompts: {spec.get('title', a.shots)}", "",
           f"Aspect: **{aspect}**. Style line (append to every prompt): {style or '(none set)'}",
           "No text, letters, logos or watermarks in any image. Leave headroom around the subject: the edit zooms and pans.", ""]
    n = 0
    for s in spec["shots"]:
        if s.get("type", "image") != "image" or not s.get("prompt"):
            continue   # cards, and shots that reuse an earlier image
        n += 1
        out.append(f"## {s['id']} -> `{s.get('src', '')}`" + (f" ({s['aspect']})" if s.get("aspect") else ""))
        out.append(f"Line: \"{s.get('anchor') or '(opening)'}...\"")
        out.append("")
        out.append(f"Prompt: {s.get('prompt', '(write prompt)')}" + (f", {style}" if style else ""))
        if s.get("video_prompt"):
            out.append(f"Optional image-to-video: {s['video_prompt']}")
        out.append("")
    out.append(f"_{n} images._")
    text = "\n".join(out) + "\n"
    if a.o:
        open(a.o, "w", encoding="utf-8").write(text)
    else:
        sys.stdout.write(text)


# ---------------------------------------------------------------- plan
def cmd_plan(a):
    spec = load_json(a.shots)
    words = load_words(a.words)
    fmt = FORMATS[spec.get("format", "long")]
    base = os.path.dirname(os.path.abspath(a.shots))
    voice = spec.get("voice")
    vdur = audio_duration(os.path.join(base, voice)) if voice else None
    end_t = max(vdur or 0, words[-1]["end"] + TAIL)

    problems, timed, idx = [], [], 0
    for s in spec["shots"]:
        anchor = s.get("anchor", "")
        if not timed and not anchor:
            t = 0.0
        else:
            i = find_anchor(words, anchor, idx)
            if i is None:
                problems.append(f"{s['id']}: anchor not found after word {idx}: \"{anchor}\"")
                continue
            idx = i + 1
            w = words[i]
            prev_end = words[i - 1]["end"] if i > 0 else 0.0
            gap = w["start"] - prev_end
            # cut in the pause if there is one, else just before the word
            t = prev_end + gap * 0.5 if gap > 0.25 else max(0.0, w["start"] - LEAD)
            if not timed:
                t = 0.0
        timed.append(dict(s, start=round(t, 3), _wi=(idx - 1 if anchor else 0)))

    for j, s in enumerate(timed):
        s["end"] = timed[j + 1]["start"] if j + 1 < len(timed) else round(end_t, 3)
        s["dur"] = round(s["end"] - s["start"], 3)

    # overlay cards: text laid over the picture underneath instead of a black
    # card; the shot before them simply holds longer
    # an overlay stays up until the next card (overlay or full), at most 10 s;
    # images cutting underneath don't end it
    cards = [s for s in timed if s.get("type") == "card"]
    overlays = []
    for k, c in enumerate(cards):
        if not c.get("overlay"):
            continue
        nxt = cards[k + 1]["start"] if k + 1 < len(cards) else end_t
        # end with the sentence the figure is spoken in (+0.8 s), 3-10 s on screen
        wi = c.get("_wi", 0)
        while wi < len(words) - 1 and not re.search(r"[.?!][\"')]*$", words[wi]["text"]):
            wi += 1
        end = max(words[wi]["end"] + 0.8, c["start"] + 3.0)
        # never spill onto a new picture that starts after the sentence ends
        later = [t["start"] for t in timed if t.get("type") != "card" and t["start"] >= words[wi]["end"] - 0.05]
        if later:
            end = min(end, max(later[0] - 0.05, c["start"] + 2.0))
        overlays.append(dict(id=c["id"], text=c.get("text", ""), sub=c.get("sub"), start=c["start"],
                             end=round(min(end, nxt - 0.1, c["start"] + 10.0, end_t), 3)))
    timed = [s for s in timed if not (s.get("type") == "card" and s.get("overlay"))]
    for j, s in enumerate(timed):
        s["end"] = timed[j + 1]["start"] if j + 1 < len(timed) else round(end_t, 3)
        s["dur"] = round(s["end"] - s["start"], 3)

    # too-short shots: warn (merging would discard owner art)
    for s in timed:
        if s["dur"] < fmt["min_shot"] and not (s.get("allow_short") and s["dur"] >= fmt["min_shot"] * 0.85):
            problems.append(f"{s['id']}: only {s['dur']:.2f}s on screen (min {fmt['min_shot']}s); move its anchor or drop it")

    # images far off the frame aspect travel across their full width/height
    # instead of being cover-cropped; a scan is motion enough, so never split it
    frame = fmt["w"] / fmt["h"]
    for s in timed:
        if s.get("type", "image") == "image" and s.get("move", "auto") == "auto":
            sz = image_size(os.path.join(base, s.get("src", "")))
            if sz and crop_loss(sz[0] / sz[1], frame) > 0.4:
                s["move"] = "scan"

    # too-long stills: split into punch-in segments on phrase breaks
    segs = []
    for s in timed:
        if s.get("type", "image") != "image" or s["dur"] <= fmt["max_shot"] or s.get("move") == "scan":
            segs.append(s)
            continue
        parts = max(2, int(-(-s["dur"] // fmt["max_shot"])))
        cuts = [s["start"]]
        for k in range(1, parts):
            target = s["start"] + s["dur"] * k / parts
            best = min((w for w in words if s["start"] + 1 < w["start"] < s["end"] - 1),
                       key=lambda w: abs(w["start"] - target) - (0.5 if re.search(r"[.,;:?!]$", prev_text(words, w)) else 0),
                       default=None)
            cuts.append(round(best["start"] - LEAD, 3) if best else round(target, 3))
        cuts = sorted(set(cuts)) + [s["end"]]
        for k in range(len(cuts) - 1):
            seg = dict(s, id=f"{s['id']}{'abcdefgh'[k]}", start=cuts[k], end=cuts[k + 1],
                       dur=round(cuts[k + 1] - cuts[k], 3), punch=k)
            if k:
                seg["section_start"] = False
            segs.append(seg)

    # assign camera moves: no repeats back to back, emphasis gets a hard push
    mi, last = 0, None
    for s in segs:
        if s.get("type", "image") != "image":
            s["move"] = "none"
            continue
        mv = s.get("move", "auto")
        if s.get("punch"):
            mv = "hold_punch"
        elif mv == "auto":
            if s.get("emphasis"):
                mv = "push_fast"
            else:
                mv = MOVES[mi % len(MOVES)]
                if mv == last:
                    mi += 1
                    mv = MOVES[mi % len(MOVES)]
                mi += 1
        s["move"] = mv
        last = mv

    for s_ in segs:
        s_.pop("_wi", None)
    edl = {"title": spec.get("title", ""), "format": spec.get("format", "long"), "voice": voice,
           "music": spec.get("music"), "label_default": spec.get("label", "Illustration"),
           "captions": spec.get("captions", fmt["captions"]), "duration": round(end_t, 3),
           "words": os.path.relpath(os.path.abspath(a.words), base), "segments": segs, "overlays": overlays, "problems": problems}
    outp = a.o or os.path.join(base, "edl.json")
    json.dump(edl, open(outp, "w", encoding="utf-8"), indent=1)

    durs = [s["dur"] for s in segs]
    print(f"EDL -> {outp}")
    print(f"voice {vdur or 0:.1f}s, timeline {end_t:.1f}s, {len(segs)} segments from {len(timed)} shots")
    if durs:
        print(f"shot length: min {min(durs):.1f}s, avg {sum(durs)/len(durs):.1f}s, max {max(durs):.1f}s")
        long_ = [s["id"] for s in segs if s.get("move") != "scan" and s["dur"] > 0.5 +
                 (fmt["max_card"] if s.get("type") == "card" else fmt["max_shot"])]
        if long_:
            print("still over max after split:", ", ".join(long_))
    for p in problems:
        print("PROBLEM:", p)
    if problems:
        sys.exit(2)


def prev_text(words, w):
    i = words.index(w)
    return words[i - 1]["text"] if i else ""


# ---------------------------------------------------------------- build
def move_js(sel, mv, t, d, fx, fy):
    ease = '"none"'
    if mv == "push_in":
        return f'tl.fromTo("{sel}",{{scale:1.04}},{{scale:1.14,duration:{d},ease:{ease}}},{t});'
    if mv == "push_fast":
        return f'tl.fromTo("{sel}",{{scale:1.02}},{{scale:1.22,duration:{d},ease:"power1.in"}},{t});'
    if mv == "pull_out":
        return f'tl.fromTo("{sel}",{{scale:1.16}},{{scale:1.04,duration:{d},ease:{ease}}},{t});'
    # pans stay inside the 12% overscan: max travel (1.12-1)/2 = 6%, we use 4%
    if mv in ("pan_left", "pan_right"):
        a, b = (4, -4) if mv == "pan_left" else (-4, 4)
        return f'tl.fromTo("{sel}",{{scale:1.12,xPercent:{a}}},{{scale:1.12,xPercent:{b},duration:{d},ease:{ease}}},{t});'
    if mv in ("tilt_up", "tilt_down"):
        a, b = (4, -4) if mv == "tilt_up" else (-4, 4)
        return f'tl.fromTo("{sel}",{{scale:1.12,yPercent:{a}}},{{scale:1.12,yPercent:{b},duration:{d},ease:{ease}}},{t});'
    if mv == "hold_punch":
        return f'tl.fromTo("{sel}",{{scale:1.32}},{{scale:1.38,duration:{d},ease:{ease}}},{t});'
    if mv == "hold":
        return f'tl.fromTo("{sel}",{{scale:1.03}},{{scale:1.06,duration:{d},ease:{ease}}},{t});'
    return ""


def caption_groups(words, max_words=4):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words or re.search(r"[.,;:?!]$", w["text"]):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def cmd_build(a):
    edl = load_json(a.edl)
    base = os.path.dirname(os.path.abspath(a.edl))
    fmt = FORMATS[edl["format"]]
    W, H, D = fmt["w"], fmt["h"], edl["duration"]
    short = edl["format"] == "short"
    clips, js = [], []
    for n, s in enumerate(edl["segments"]):
        cid = f"g{n}"
        xf = XFADE if (s.get("section_start") and n) else 0
        start = max(0, s["start"] - xf)
        dur = round(s["end"] - start + (0.05 if n + 1 < len(edl["segments"]) else 0), 3)
        scan = None
        if s.get("type", "image") == "image" and s.get("move") == "scan":
            sz = image_size(os.path.join(base, s["src"]))
            if sz:
                if sz[0] / sz[1] > W / H:   # wider than frame: fit height, travel x
                    travel = sz[0] * H / sz[1] - W
                    scan = ("height:100%;width:auto;left:0;top:0", "x", -travel)
                else:                        # taller: fit width, travel y
                    travel = sz[1] * W / sz[0] - H
                    scan = ("width:100%;height:auto;left:0;top:0", "y", -travel)
        if scan:
            inner = f'<img class="scanpic" id="{cid}i" src="{html.escape(s["src"])}" style="{scan[0]}">'
        elif s.get("type", "image") == "image":
            fx, fy = (s.get("focus") or [0.5, 0.5])
            inner = (f'<img class="pic" id="{cid}i" src="{html.escape(s["src"])}" '
                     f'style="transform-origin:{fx*100:.0f}% {fy*100:.0f}%">')
        else:
            inner = f'<div class="card"><div class="cardtxt">{html.escape(s.get("text", ""))}</div>' + \
                    (f'<div class="cardsub">{html.escape(s["sub"])}</div>' if s.get("sub") else "") + "</div>"
        clips.append(f'<div id="{cid}" class="scene clip" data-start="{start:.3f}" data-duration="{dur:.3f}" '
                     f'data-track-index="{1 + (n % 2)}">{inner}</div>')
        if xf:
            js.append(f'tl.fromTo("#{cid}",{{opacity:0}},{{opacity:1,duration:{xf},ease:"power1.inOut"}},{start:.3f});')
        if scan:
            a0, a1 = (scan[2], 0) if s.get("reverse") else (0, scan[2])
            js.append(f'tl.fromTo("#{cid}i",{{{scan[1]}:{a0:.0f}}},{{{scan[1]}:{a1:.0f},duration:{dur},ease:"sine.inOut"}},{start:.3f});')
        elif s.get("type", "image") == "image":
            js.append(move_js(f"#{cid}i", s["move"], start, dur, *(s.get("focus") or [0.5, 0.5])))
        else:
            js.append(f'tl.fromTo("#{cid} .cardtxt",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.6,ease:"power2.out"}},{start + 0.15:.3f});')
            js.append(f'tl.fromTo("#{cid} .card",{{scale:1}},{{scale:1.04,duration:{dur},ease:"none"}},{start:.3f});')
        label = s.get("label", edl["label_default"]) if s.get("type", "image") == "image" else None
        if label:
            clips.append(f'<div class="tag clip" id="{cid}tag" data-start="{s["start"]:.3f}" data-duration="{s["dur"]:.3f}" '
                         f'data-track-index="6">{html.escape(label)}</div>')
        if s.get("source"):
            clips.append(f'<div class="src clip" id="{cid}src" data-start="{s["start"]:.3f}" data-duration="{s["dur"]:.3f}" '
                         f'data-track-index="7">Source: {html.escape(s["source"])}</div>')

    for k, o in enumerate(edl.get("overlays", [])):
        clips.append(f'<div class="ovl clip" id="ovl{k}" data-start="{o["start"]:.3f}" data-duration="{o["end"] - o["start"]:.3f}" '
                     f'data-track-index="8"><div class="ovltxt">{html.escape(o["text"])}</div>'
                     + (f'<div class="ovlsub">{html.escape(o["sub"])}</div>' if o.get("sub") else "") + "</div>")
        js.append(f'tl.fromTo("#ovl{k}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{o["start"] + 0.1:.3f});')

    if edl.get("captions"):
        words = load_words(os.path.join(base, edl["words"]))
        groups = caption_groups(words, 3 if short else 6)
        for k, g in enumerate(groups):
            st = g[0]["start"]
            en = g[-1]["end"] + 0.15
            if k + 1 < len(groups):
                en = min(en, groups[k + 1][0]["start"] - 0.02)
            txt = " ".join(w["text"] for w in g)
            clips.append(f'<div class="cap clip" id="cap{k}" data-start="{st:.3f}" data-duration="{en - st:.3f}" '
                         f'data-track-index="5"><span>{html.escape(txt)}</span></div>')

    audio = ""
    if edl.get("voice"):
        audio = (f'<audio id="vo" src="{html.escape(edl["voice"])}" data-start="0" '
                 f'data-duration="{D:.3f}" data-track-index="9"></audio>')

    cap_top = int(H * (0.62 if short else 0.80))
    cap_size = 64 if short else 44
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#0d0f14}}
#root{{position:relative;width:100%;height:100%;font-family:Georgia,'Times New Roman',serif;color:#fff;overflow:hidden}}
.scene{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;overflow:hidden;background:#0d0f14}}
.pic{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.scanpic{{position:absolute;max-width:none}}
.card{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#0d0f14;padding:0 10%}}
.cardtxt{{font-size:{86 if short else 88}px;line-height:1.15;text-align:center;letter-spacing:.01em}}
.cardsub{{margin-top:28px;font:600 {34 if short else 34}px/1.3 sans-serif;color:#b9c0cc;text-align:center;letter-spacing:.08em;text-transform:uppercase}}
.tag{{position:absolute;left:{40 if short else 48}px;top:{190 if short else 40}px;font:700 {28 if short else 22}px sans-serif;background:rgba(10,12,18,.62);padding:6px 14px;border-radius:10px;color:#e8e8e8}}
.src{{position:absolute;right:48px;bottom:{260 if short else 40}px;font:500 {24 if short else 20}px sans-serif;background:rgba(10,12,18,.62);padding:6px 14px;border-radius:10px;color:#d8d8d8;max-width:60%}}
.cap{{position:absolute;left:5%;width:90%;top:{cap_top}px;text-align:center}}
.ovl{{position:absolute;left:{40 if short else 72}px;bottom:{300 if short else 96}px;max-width:{"88%" if short else "62%"};background:rgba(10,12,18,.72);padding:22px 30px;border-left:6px solid #b5533c;border-radius:6px}}
.ovltxt{{font-size:{64 if short else 60}px;line-height:1.1}}
.ovlsub{{margin-top:10px;font:600 {28 if short else 24}px/1.3 sans-serif;color:#c9cfd8;letter-spacing:.06em;text-transform:uppercase}}
.cap span{{display:inline-block;background:rgba(10,12,18,.78);padding:14px 26px;border-radius:20px;font:800 {cap_size}px/1.15 sans-serif}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D:.3f}" data-width="{W}" data-height="{H}">
{audio}
{chr(10).join(clips)}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
{chr(10).join(j for j in js if j)}
window.__timelines["main"]=tl;tl.seek(0);
</script></body></html>
"""
    outp = a.o or os.path.join(base, "index.html")
    open(outp, "w", encoding="utf-8").write(doc)
    missing = [s["src"] for s in edl["segments"] if s.get("type", "image") == "image"
               and not os.path.exists(os.path.join(base, s["src"]))]
    if not os.path.exists(os.path.join(base, "assets/vendor/gsap.min.js")):
        print("WARNING: assets/vendor/gsap.min.js missing (the sandbox blocks the CDN; copy it in)")
    print(f"composition -> {outp} ({W}x{H}, {D:.1f}s, {len(edl['segments'])} segments)")
    for m in sorted(set(missing)):
        print("MISSING IMAGE:", m)
    frame = W / H
    for src in sorted({s["src"] for s in edl["segments"] if s.get("type", "image") == "image"} - set(missing)):
        if all(s.get("move") == "scan" for s in edl["segments"] if s.get("src") == src):
            continue
        sz = image_size(os.path.join(base, src))
        lost = crop_loss(sz[0] / sz[1], frame) if sz else 0
        if lost > 0.2:
            print(f"ASPECT: {src} is {sz[0]}x{sz[1]}; cover-crop loses {lost:.0%} of it. "
                  "Crop/outpaint to frame, or set move pan_*/tilt_* and check the snapshot")


# ---------------------------------------------------------------- srt
def fmt_ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def cmd_srt(a):
    words = load_words(a.words)
    lines = []
    for k, g in enumerate(caption_groups(words, 8), 1):
        lines += [str(k), f"{fmt_ts(g[0]['start'])} --> {fmt_ts(g[-1]['end'])}", " ".join(w["text"] for w in g), ""]
    text = "\n".join(lines)
    if a.o:
        open(a.o, "w", encoding="utf-8").write(text)
        print(f"SRT -> {a.o}")
    else:
        sys.stdout.write(text)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("prompts"); s.add_argument("shots"); s.add_argument("-o"); s.set_defaults(f=cmd_prompts)
    s = sub.add_parser("plan"); s.add_argument("shots"); s.add_argument("words"); s.add_argument("-o"); s.set_defaults(f=cmd_plan)
    s = sub.add_parser("build"); s.add_argument("edl"); s.add_argument("-o"); s.set_defaults(f=cmd_build)
    s = sub.add_parser("srt"); s.add_argument("words"); s.add_argument("-o"); s.set_defaults(f=cmd_srt)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

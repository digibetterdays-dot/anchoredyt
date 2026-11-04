# shots.json schema

```json
{
  "title": "What If the Cascadia Fault Ruptured Tomorrow?",
  "format": "long",
  "voice": "assets/audio/voice.wav",
  "music": "assets/audio/music.mp3",
  "style": "layered paper-cut illustration, muted teal and rust palette, soft side light, 16:9",
  "label": "Illustration",
  "captions": false,
  "shots": [
    {"id": "s01", "src": "assets/shots/s01.png", "anchor": "On a winter night in",
     "prompt": "Pacific Northwest coastline at night, cedar forest, calm sea", "move": "push_in", "focus": [0.5, 0.6]},
    {"id": "s02", "src": "assets/shots/s02.png", "anchor": "the ground began to",
     "prompt": "forest floor splitting, trees leaning", "emphasis": true},
    {"id": "c01", "type": "card", "text": "Chapter 1", "sub": "The fault", "anchor": "Off the coast",
     "section_start": true},
    {"id": "s03", "src": "assets/shots/s03.png", "anchor": "Off the coast of Oregon",
     "prompt": "map-like view of the subduction zone", "move": "pan_right", "label": null,
     "source": "NOAA"}
  ]
}
```

Paths are relative to the folder holding `shots.json` (the HyperFrames project).

## Top level
| Field | Required | Meaning |
|---|---|---|
| `format` | yes | `long` (1920x1080) or `short` (1080x1920) |
| `voice` | yes | single VO file |
| `title`, `style` | for prompts | `style` is appended to every image prompt |
| `music` | no | bed for `finish_audio.sh` (not placed in the composition) |
| `label` | no | default on-screen tag for stills, default `Illustration` |
| `captions` | no | override the default (on for Shorts, off for long form) |

## Per shot
| Field | Meaning |
|---|---|
| `id` | unique, sortable (`s01`, `c01`) |
| `type` | `image` (default) or `card` |
| `anchor` | first 3-6 spoken words where the shot starts, exactly as in the script. First shot may leave it empty (starts at 0). Anchors must be in spoken order. |
| `src` | image path (images) |
| `prompt`, `video_prompt` | for the owner's prompt list |
| `move` | `auto` (default) or one of `push_in push_fast pull_out pan_left pan_right tilt_up tilt_down hold scan` |
| `aspect` | shown in the prompt list when the art is not the frame shape, e.g. `3:1 panorama` or `9:16 tall map`; such art gets an automatic `scan` |
| `reverse` | `true` = scan right-to-left (or bottom-to-top) |
| `focus` | `[x, y]` 0-1 zoom origin, default centre |
| `emphasis` | `true` = hard push for a key line |
| `section_start` | `true` = crossfade in (new chapter or time jump) |
| `text`, `sub` | card title and subtitle |
| `label` | override the tag; `null` hides it (maps, graphics, cards) |
| `source` | small source credit for a figure on screen |

Anchor tips: avoid starting anchors on words the transcriber often mangles (numbers written as digits vs words, names). If the script says "1,250" the VO transcript may say "twelve fifty"; anchor on the words around it instead. The matcher tolerates one wrong word in anchors of 3+ words.

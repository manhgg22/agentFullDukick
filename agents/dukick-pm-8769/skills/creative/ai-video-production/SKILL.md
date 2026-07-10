---
name: ai-video-production
description: AI-assisted and code-based video production — from editable React projects (Remotion) to HTML/CSS video compositions (HyperFrames) to real-footage editing pipelines (FFmpeg, Descript, CapCut). Use when creating, editing, or rendering video content with AI tools or programmable frameworks.
category: creative
---

# AI Video Production

Produce video content using code-first tools, AI generation, and real-footage editing pipelines.

## When to Activate

- Creating short videos, product demos, trailers, or motion graphics
- Building editable React video projects with Remotion
- Creating HTML/CSS/JS video compositions with HyperFrames
- Editing real footage: cutting, structuring, adding overlays, subtitles, voiceover
- Converting between aspect ratios for social platforms
- User says "video", "edit footage", "create a promo", "render MP4", or "make a vlog"

---

## Code-First Video: Remotion

Remotion turns video ideas into editable React projects. Produces code that can be repeatedly edited and re-rendered.

### Setup

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
```

### Core Primitives

- `Composition`, `Sequence`, `AbsoluteFill`
- `Audio`, `Video`, `Img`
- `useCurrentFrame`, `useVideoConfig`
- `interpolate`, `spring`

### Workflow

1. Create a Remotion project from an empty folder
2. Build video as React components with scene data in constants/arrays
3. Preview in Remotion Studio: `npx remotion studio`
4. Render a still frame to catch layout issues: `npx remotion still <id> --scale=0.25 --frame=30`
5. Render final MP4: `npx remotion render <id> out/final.mp4`

### Best Practices

- Keep copy, timing, colors, and asset references in clear constants
- Make captions mobile-readable: high contrast, generous line height, safe margins
- Use deterministic animation (avoid `Math.random()`)
- Use frame-based timing, not browser timers
- Separate components for scenes, captions, overlays, and recurring motifs

---

## Code-First Video: HyperFrames

HyperFrames treats HTML as the video source of truth. Build scenes as HTML/CSS/JS compositions, validate, then render to MP4.

### Setup

```bash
npx hyperframes init my-video --non-interactive
```

### Workflow

1. Create or reuse a HyperFrames project
2. Write composition in HTML/CSS/JS — make the static hero frame correct first
3. Validate: `npx hyperframes lint` and `npx hyperframes inspect --samples 15`
4. Preview: `npx hyperframes preview`
5. Render: `npx hyperframes render --output final.mp4 --quality standard`

Use `--quality draft` for fast iteration, `--quality high` for final delivery.

### Composition Rules

- Root element needs `data-composition-id`, `data-width`, `data-height`
- Use `data-start`, `data-duration`, `data-track-index` for timed clips
- Register GSAP timelines on `window.__timelines`
- CSS is the final layout state; animate from/to that state
- Avoid `Math.random()` or `Date.now()` unless seeded
- Do not use infinite repeats — calculate finite counts from duration

---

## Real Footage Editing Pipeline

AI-assisted editing for existing video. The value is compression, not generation.

### Layer Overview

```
Raw footage / Screen Studio capture
  → Structure (Claude/Codex: transcript, plan, edit decision list)
  → Deterministic cuts (FFmpeg)
  → Programmable composition (Remotion: overlays, data viz, motion graphics)
  → Generated assets (ElevenLabs voiceover, fal.ai music/SFX/thumbnails)
  → Final polish (Descript / CapCut: pacing, captions, color, audio mix)
```

### FFmpeg Commands

**Extract by timestamp:**
```bash
ffmpeg -i raw.mp4 -ss 00:12:30 -to 00:15:45 -c copy segment.mp4
```

**Batch cut from edit decision list:**
```bash
while IFS=, read -r start end label; do
  ffmpeg -i raw.mp4 -ss "$start" -to "$end" -c copy "segments/${label}.mp4"
done < cuts.txt
```

**Concatenate segments:**
```bash
for f in segments/*.mp4; do echo "file '$f'"; done > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c copy assembled.mp4
```

**Create proxy:**
```bash
ffmpeg -i raw.mp4 -vf "scale=960:-2" -c:v libx264 -preset ultrafast -crf 28 proxy.mp4
```

**Normalize audio:**
```bash
ffmpeg -i segment.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:v copy normalized.mp4
```

**Reframe for platforms:**
```bash
# 16:9 to 9:16 (center crop)
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" vertical.mp4

# 16:9 to 1:1
ffmpeg -i input.mp4 -vf "crop=ih:ih,scale=1080:1080" square.mp4
```

### Scene Detection and Auto-Cut

```bash
# Detect scene changes
ffmpeg -i input.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr -f null - 2>&1 | grep showinfo

# Find silent segments
ffmpeg -i input.mp4 -af silencedetect=noise=-30dB:d=2 -f null - 2>&1 | grep silence
```

### Social Media Aspect Ratios

| Platform | Ratio | Resolution |
|----------|-------|------------|
| YouTube | 16:9 | 1920x1080 |
| TikTok / Reels | 9:16 | 1080x1920 |
| Instagram Feed | 1:1 | 1080x1080 |
| X / Twitter | 16:9 or 1:1 | 1280x720 or 720x720 |

---

## Generated Assets

### Voiceover (ElevenLabs)

```python
import requests, os

resp = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
    json={"text": "...", "model_id": "eleven_turbo_v2_5"}
)
```

### Music / SFX (fal.ai)

Use the `media-generation` skill for background music and sound effects via fal.ai.

### Thumbnails / B-Roll (fal.ai)

```
generate(model_name: "fal-ai/nano-banana-pro", input: {
  "prompt": "professional thumbnail for tech vlog...",
  "image_size": "landscape_16_9"
})
```

---

## Key Principles

1. **Edit, don't generate.** This workflow is for cutting real footage, not creating from prompts.
2. **Structure before style.** Get the story right before touching visuals.
3. **FFmpeg is the backbone.** Boring but critical for deterministic cuts.
4. **Remotion for repeatability.** If you'll do it more than once, make it a component.
5. **Generate selectively.** Only use AI generation for assets that don't exist.
6. **Taste is the last layer.** AI clears repetitive work; humans make final creative calls.

## Related Skills

- `media-generation` — AI image, video, and audio generation via fal.ai and Hermes endpoints
- `content-engine` — Platform-native content distribution

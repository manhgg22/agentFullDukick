---
name: code-video-production
description: Create videos from code using React (Remotion) or HTML/CSS/JS (HyperFrames). Covers project scaffolding, composition rules, preview, validation, and rendering to MP4. Use when the user wants a programmable, editable video project rather than prompt-only generation.
---

# Code Video Production

Class-level skill for creating videos from code. Two primary frameworks are supported: Remotion (React-based) and HyperFrames (HTML/CSS/JS-based). Both treat code as the source of truth for video, enabling iterative edits to timing, text, animation, and assets before rendering to MP4.

## When to use

- User wants an editable video project (not a one-shot AI generation)
- Short intros, trailers, product promos, subtitle animations, HUD/tech visuals
- Vertical short videos, feed ads, tutorial videos
- Motion graphics that need precise timing and reusable components

## Framework selection

| Framework | Best for | Language | Setup |
|-----------|----------|----------|-------|
| **Remotion** | React devs, complex state, reusable components | React + TypeScript | `npx create-video@latest --yes --blank --no-tailwind` |
| **HyperFrames** | Web devs, HTML/CSS animations, quick prototypes | HTML + CSS + JS | `npx hyperframes init my-video --non-interactive` |

## Shared workflow

1. Turn the request into a production brief: duration, aspect ratio, platform, style, scenes, text, narration, music, output path.
2. Default to 1080×1920 (vertical), 1920×1080 (horizontal), 30 fps, MP4.
3. Scaffold or reuse a project.
4. Write the composition.
5. Validate before rendering:
   - Remotion: `npm run build` + `npx remotion still ...`
   - HyperFrames: `npx hyperframes lint` + `npx hyperframes inspect --samples 15`
6. Preview when useful:
   - Remotion: `npx remotion studio`
   - HyperFrames: `npx hyperframes preview`
7. Render final MP4:
   - Remotion: `npx remotion render <composition-id> out/final.mp4`
   - HyperFrames: `npx hyperframes render --output final.mp4 --quality standard`

## Remotion specifics

Use Remotion primitives for timing and media: `Composition`, `Sequence`, `AbsoluteFill`, `Audio`, `Video`, `Img`, `useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring`.

- Keep copy, scene timing, colors, and asset references in clear constants or data arrays.
- Use deterministic animation; avoid `Math.random()` or `Date.now()`.
- Use frame-based timing instead of browser timers.
- Separate components for scenes, captions, overlays, lower thirds.
- Make captions readable on mobile: high contrast, generous line height, safe margins.

## HyperFrames specifics

- Root element needs `data-composition-id`, `data-width`, `data-height`.
- Use `data-start`, `data-duration`, `data-track-index` for timed clips.
- Register GSAP timelines synchronously on `window.__timelines`.
- Use CSS as the final layout state, then animate from/to that state.
- Keep media playback under the HyperFrames runtime; do not manually call `play()` or `pause()`.
- Avoid infinite repeats; calculate finite counts from composition duration.
- Check that text, captions, and UI elements stay inside the frame on every inspected timestamp.

## Quality levels

| Level | When to use |
|-------|-------------|
| `draft` / `--scale=0.25` | Fast iteration, layout checks |
| `standard` | Review versions |
| `high` | Final delivery |

## Delivery checklist

When finished, tell the user:
- the rendered MP4 path;
- the preview URL/command if a preview server is running;
- the composition ID (Remotion) or composition name (HyperFrames);
- any assumptions about duration, aspect ratio, voiceover, music, assets, style.

A task is complete only after lint/inspect/still passes and the MP4 is rendered, unless the user explicitly asks for source files only.

## Pitfalls

- **Do not stop at HTML/JSX.** Validation and rendering are mandatory steps.
- **Do not use nondeterministic animation.** Seeded generators only.
- **Do not let content overflow the frame.** Use `lint`/`inspect`/`still` to catch this.
- **Remotion only:** do not call `play()`/`pause()` on media elements manually.
- **HyperFrames only:** do not use infinite CSS animations; calculate finite durations.

## Related skills

- `video-editing` — for cutting and augmenting real footage (different workflow)
- `fal-ai-media` — for AI-generated insert shots, music, SFX
- `hermes-media-generation` — for image/video generation via Hermes Web UI endpoints

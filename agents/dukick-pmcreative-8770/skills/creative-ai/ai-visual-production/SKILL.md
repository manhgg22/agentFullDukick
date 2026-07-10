---
name: ai-visual-production
description: AI-assisted visual production workflows — storyboarding, moodboarding, concept frames, and pre-viz using LLMs + image generators.
---

# AI Visual Production

Class-level skill for producing visual assets (storyboards, moodboards, concept frames, pre-visualization) by combining LLMs and image generators. Covers rapid iteration workarounds, shotlist generation patterns, and export workflows.

## When to use

- Need a fast storyboard for a pitch or client review.
- Pre-visualizing shots before filming or full production.
- Creating concept frames to establish visual direction.
- Working around generation-rate limits or image-per-call caps.

## Workflows

### Rapid AI Storyboard (LLM Shotlist → Image Gen Frames)

**1. Generate shotlist with an LLM (Claude / GPT-4 / Gemini)**
- Prompt for **varied shot sizes**: Wide, Medium, Close-up, Extreme Close-up, Over-the-shoulder, Drone / Aerial, POV, etc.
- Request each shot to include:
  - **Shot number**
  - **Shot size**
  - **Visual description**
  - **Movement / action**
  - **Suggested VO / on-screen text**
- Tip: The more detailed the prompt, the more cinematic and varied the shotlist.

**2. Generate frames with an image generator**
- Feed each shot description into the image generator (Midjourney, DALL-E, GPT-2 Image Gen, Stable Diffusion, etc.).
- **Workaround for generation limits**: Request **multiple frames per image** (e.g., 8 frames composited on 1 canvas) to maximize output per API call.
  - Useful when tools cap images per request (e.g., ~10 images / call).
  - Trade-off: composite images may need cropping if individual frames are required later.

**3. Arrange & export**
- Separate frames from composite images if needed for individual use.
- Or keep multi-frame layouts for quick internal / client review.
- Export final storyboard to PDF, Canva, pitch deck, or project folder.

## Pitfalls

- **Vague shotlist prompts** produce repetitive shot sizes; always explicitly request variety.
- **Ignoring tool limits** slows iteration; use multi-frame compositing to stay within caps.
- **Not deciding frame format early** — composite grids vs. individual frames — causes rework at export time.
- **Over-polishing AI frames** as final art; treat them as communication tools, not deliverables, unless the project is explicitly AI-native.

## Tool combos that work

| Shotlist | Images | Arrangement |
|----------|--------|-------------|
| Claude / ChatGPT | GPT-2 / DALL-E / Midjourney | Canva / Figma / Photoshop |
| Gemini | Stable Diffusion (local) | Direct markdown / PDF |

## Sub-workflows

### AI Slide Proposal (from `ai-slide-proposal`)

Use when the client-facing deliverable is a slide deck (proposal, concept pitch, treatment).

**Three-step workflow:**
1. **Input context** — feed the full brief/background, slide purpose, target audience, and desired tone.
2. **Moodboard lock** — if the brief already has a moodboard, have the AI reproduce it as a structured table (colors, typography, patterns, overall style) and confirm with the user. If not, ask the AI to propose options and let the user pick one.
3. **Generate slides** — prompt in detail about colors, layout, and design. Warn the AI to stick to the locked moodboard/concept.

**Handling lag/lost context after many generations:**
- Open a new chat window, paste the approved moodboard images, and warn "make the next slides match this moodboard."
- Or branch from the old conversation to reset context.

**Tips:**
- The more detailed the prompt, the fewer revisions needed.
- Generate in small batches (section by section) rather than requesting the whole deck at once.
- Always re-state the moodboard/concept before each new generation batch.

### Creative Intake & Analysis (from `creative-intake-analysis`)

Use when the project starts with a client-shared Google Drive folder full of mixed media (screenshots, AI images, audio, docs).

**Workflow:**
1. **List the Drive folder** — use the folder ID from the shared link.
2. **Download binaries safely** — `drive_tool.py read` decodes to UTF-8 and **corrupts** images/audio. For any non-text file, use `googleapiclient.http.MediaIoBaseDownload` to fetch raw bytes (see `scripts/drive-binary-download-snippet.py`).
3. **Analyze visual assets** — use `vision_analyze` on key images in parallel (up to 3). Prioritize:
   - Screenshots of slides/chat → meeting content, timelines, decisions
   - AI-generated concept images → visual direction, mood, keywords
   - Reference GIFs/images → competitor or inspiration style
4. **Synthesize a structured markdown brief** with these sections:
   - Strategic Insights
   - Client Personality / CDT Profile
   - Creative Direction
   - Competitive Landscape
   - Assignments & Timeline
   - Asset Inventory

**Pitfalls:**
- Do not use text-mode `read` for binary files.
- Do not analyze every single image — prioritize screenshots and concept images.
- Flag WAV/audio files in the recap and ask the user if they contain critical discussion.
- Merge chat-context insights (Discord/Slack) with file analysis; chat often captures decisions not in images.

## References

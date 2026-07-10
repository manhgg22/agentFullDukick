---
source: "https://www.instagram.com/p/DZB_O5aEUHn/"
author: "Đỗ Ngọc Linh"
date: "2026-06-24"
---

# Instagram Storyboard Workflow — Multi-Frame Per Image Workaround

Reproduction recipe for the multi-frame composite workaround used by the Dukick team.

## Context
- Tool used for images: **GPT-2 Image Generator** (limit ~10 images per call).
- Goal: produce storyboard frames as fast as possible.

## Workaround
Instead of generating 1 image per shot, prompt the image generator to produce **8 frames in a single image** (a composite grid / strip). This reduces the number of API calls and speeds up iteration.

## Steps observed in session
1. Use Claude to write a detailed shotlist with varied shot sizes.
2. Pass shot descriptions to GPT-2 image generator.
3. Request composite images containing 8 frames each.
4. Review composite grids quickly; crop later if individual frames are needed.

## Result
- Fewer API calls needed.
- Faster turnaround for internal/client review.
- Composite can be exported directly or cropped into separate frames.

## Link
https://www.instagram.com/p/DZB_O5aEUHn/

---
name: film-reference-research
description: Research and compile film/video references (TVC, brand films, commercials) for creative briefs. Covers YouTube, Vimeo, and web search techniques when direct API access is limited.
triggers:
  - "tìm ref"
  - "find reference"
  - "TVC reference"
  - "brand film reference"
  - "moodboard film"
  - "commercial similar to"
  - "phim tham khảo"
  - "reference phim"
  - "tương tự phim"
---

# Film Reference Research

## Purpose
Compile structured reference lists for TVCs, brand films, and commercials to inform creative direction, cinematography, storytelling, and emotional tone.

## Workflow

### 1. Decode the Reference Film
If the user provides a specific film/campaign to match against:
- Extract metadata using **Vimeo oEmbed** or **YouTube oEmbed** (reliable even when APIs are blocked)
- Search DuckDuckGo for campaign articles (agency, director, production house, awards)
- Identify: brand, agency, production, director, duration, awards, core insight

### 2. Search for Similar Films

| Dimension | Search Strategy |
|---|---|
| **Same industry** | Search `[industry] + anniversary film`, `[industry] + heritage commercial` |
| **Same technique** | Search `[technique] + commercial`, e.g., "split screen past present commercial" |
| **Same emotional tone** | Search `[emotion] + brand film`, e.g., "generational storytelling commercial" |

#### Working Search Methods (when direct APIs fail)
1. **Vimeo oEmbed API**: `https://vimeo.com/api/oembed.json?url=<vimeo_url>` — reliable for title, author, duration, description
2. **YouTube oEmbed**: `https://www.youtube.com/oembed?url=<yt_url>&format=json` — basic title/author
3. **DuckDuckGo HTML search**: `https://html.duckduckgo.com/html/?q=<query>` — finds campaign articles with video links
4. **ReturnYouTubeDislike API**: `https://returnyoutubedislikeapi.com/votes?videoId=<id>` — stats for known IDs

#### Platforms to Search
- **YouTube**: Direct search + filter by "Channel" (official brand channels)
- **Vimeo**: Higher quality than YouTube for brand films; search + Staff Picks
- **AdsoftheWorld.com**: Filter by category + emotion
- **Shots.net**: Campaign articles with embedded videos
- **Directors Think Tank / similar production houses**: Check their Vimeo channels

### 3. Categorize References

Group findings into at least these dimensions:

- **A. Same Industry**: Same sector (banking, real estate, etc.)
- **B. Same Technique**: Same visual/directorial technique (split screen, time-lapse, archival footage, etc.)
- **C. Same Emotional Tone**: Same emotional register (nostalgia, pride, generational connection, etc.)

### 4. Document Each Reference

Use the standard reference entry format (see `templates/reference-entry.md`).

Each entry must include:
- Link
- Source (YouTube/Vimeo/official)
- Purpose (what aspect this refs: tone, cinematography, storytelling, VFX, etc.)
- Điểm thích (strengths)
- Điểm không thích (weaknesses/limitations)
- Liên quan phần nào của brief
- Ghi chú

### 5. Cross-Reference with Internal Vault

Before finalizing, search the project's Obsidian vault or file system for:
- Existing `Ref-*` files
- `DinhHuong-*` or positioning documents
- Previous campaign research

Avoid duplicating work; build on existing research.

## Pitfalls

- **Don't rely on YouTube Data API proxies** — most public instances are rate-limited or down. Fallback to oEmbed + DuckDuckGo + direct page scraping.
- **Don't skip metadata extraction** — Director, production house, and awards matter more than the link itself for creative credibility.
- **Don't dump raw links** — Always categorize and annotate. A list of 20 links with no structure is useless to a creative team.
- **Don't ignore Vimeo** — Brand films and high-end commercials are often uploaded to Vimeo (better quality, fewer copyright issues) and not YouTube.
- **Don't improvise format when a template exists** — If the project's Obsidian vault already has a `Ref-*` file, match that exact format. Check `Ref-TVC-BDS-Modern.md` or similar existing files first.

## Templates
- `templates/reference-entry.md` — Standard reference documentation format

## References
- `references/hsbc-legacy-lives-on-research.md` — Example research output compiling references for HSBC "140 Years And Beyond" / "Legacy Lives On"

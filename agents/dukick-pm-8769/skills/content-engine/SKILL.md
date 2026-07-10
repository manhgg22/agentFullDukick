---
name: content-engine
description: Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social posts, threads, scripts, content calendars, or one source asset adapted cleanly across platforms.
---

# Content Engine

Build platform-native content without flattening the author's real voice into platform slop.

## When to Activate

- writing X posts or threads
- drafting LinkedIn posts or launch updates
- scripting short-form video or YouTube explainers
- repurposing articles, podcasts, demos, docs, or internal notes into public content
- building a launch sequence or ongoing content system around a product, insight, or narrative

## Non-Negotiables

1. Start from source material, not generic post formulas.
2. Adapt the format for the platform, not the persona.
3. One post should carry one actual claim.
4. Specificity beats adjectives.
5. No engagement bait unless the user explicitly asks for it.

## Source-First Workflow

Before drafting, identify the source set:
- published articles
- notes or internal memos
- product demos
- docs or changelogs
- transcripts
- screenshots
- prior posts from the same author

If the user wants a specific voice, build a voice profile from real examples before writing.
Use `brand-voice` as the canonical workflow when voice consistency matters across more than one output.

## Voice Handling

`brand-voice` is the canonical voice layer.

Run it first when:

- there are multiple downstream outputs
- the user explicitly cares about writing style
- the content is launch, outreach, or reputation-sensitive

Reuse the resulting `VOICE PROFILE` here instead of rebuilding a second voice model.
If the user wants Affaan / ECC voice specifically, still treat `brand-voice` as the source of truth and feed it the best live or source-derived material available.

## Hard Bans

Delete and rewrite any of these:
- "In today's rapidly evolving landscape"
- "game-changer", "revolutionary", "cutting-edge"
- "here's why this matters" unless it is followed immediately by something concrete
- ending with a LinkedIn-style question just to farm replies
- forced casualness on LinkedIn
- fake engagement padding that was not present in the source material

## Platform Adaptation Rules

### X

- open with the strongest claim, artifact, or tension
- keep the compression if the source voice is compressed
- if writing a thread, each post must advance the argument
- do not pad with context the audience does not need

### LinkedIn

- expand only enough for people outside the immediate niche to follow
- do not turn it into a fake lesson post unless the source material actually is reflective
- no corporate inspiration cadence
- no praise-stacking, no "journey" filler

### Short Video

- script around the visual sequence and proof points
- first seconds should show the result, problem, or punch
- do not write narration that sounds better on paper than on screen

### YouTube

- show the result or tension early
- organize by argument or progression, not filler sections
- use chaptering only when it helps clarity

### Newsletter

- open with the point, conflict, or artifact
- do not spend the first paragraph warming up
- every section needs to add something new

## Repurposing Flow

1. Pick the anchor asset.
2. Extract 3 to 7 atomic claims or scenes.
3. Rank them by sharpness, novelty, and proof.
4. Assign one strong idea per output.
5. Adapt structure for each platform.
6. Strip platform-shaped filler.
7. Run the quality gate.

## Deliverables

When asked for a campaign, return:
- a short voice profile if voice matching matters
- the core angle
- platform-native drafts
- posting order only if it helps execution
- gaps that must be filled before publishing

## Quality Gate

Before delivering:
- every draft sounds like the intended author, not the platform stereotype
- every draft contains a real claim, proof point, or concrete observation
- no generic hype language remains
- no fake engagement bait remains
- no duplicated copy across platforms unless requested
- any CTA is earned and user-approved

## Related Skills

- `brand-voice` for source-derived voice profiles
- `media-generation` for generating images, videos, and audio for posts

---

## Appendix A: Platform Distribution Reference

| Goal | Platform | Reasoning |
|------|----------|-----------|
| Real-time engagement | X (Twitter) | Fastest iteration, best for announcements |
| Professional thought leadership | LinkedIn | Longer posts, higher signal-to-noise |
| Community building | Telegram | Direct channel with subscribers |
| Niche/creator community | Discord | Rich formatting, threads, reactions |
| B2B authority | LinkedIn | Decision-makers, case studies, data |
| Behind-the-scenes | Telegram | Raw, unfiltered updates |
| Interactive Q&A | X + Discord | Live tweet + Discord thread |

### Platform Comparison

- **X (Twitter):** 280 chars/post, threads, images/video, polls, Spaces. Fastest iteration.
- **LinkedIn:** 3k chars/post, articles, newsletters, documents. Professional context.
- **Telegram:** Unlimited text, channels/groups, polls, reactions. Direct subscriber model.
- **Discord:** Rich formatting, threads, roles, bots. Niche communities.

### Multi-Language Workflow

1. Write in primary language
2. Identify cultural references, idioms, humor
3. Translate literally first
4. Adapt for cultural context
5. Check character limits per language
6. Preserve CTA and key metrics
7. Review with native speaker if possible
8. Schedule with timezone consideration

### Platform-Specific Formatting

**X:**
```
Hook line (no emojis in first line)
Body with line breaks
Thread indicator: "(1/7)"
Media: 1 image or 1 video per post
```

**LinkedIn:**
```
First line = scroll stopper
Body with short paragraphs
Hashtags: 3-5 relevant
Tag relevant people
Call to action at end
```

**Telegram:**
```
Bold headers with **markdown**
Bullet points for scannability
Links with preview
Images/gifs inline
```

**Discord:**
```
Use embeds for announcements
Thread names: descriptive
Use roles for @mentions
Rich formatting: ```code```, > quotes
```

---

## Appendix B: Direct X/Twitter API Integration

Use for advanced posting beyond built-in tools. Requires OAuth 1.0a tokens: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`.

### Python Example (OAuth1Session)

```python
from requests_oauthlib import OAuth1Session
import json

client = OAuth1Session(
    consumer_key, client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret
)

response = client.post(
    "https://api.twitter.com/2/tweets",
    json={"text": "Hello from the X API!"}
)
```

### Media Upload (v1.1)

```python
media = open("image.png", "rb")
media_upload = client.post(
    "https://upload.twitter.com/1.1/media/upload.json",
    files={"media": media}
)
media_id = media_upload.json()["media_id_string"]

response = client.post(
    "https://api.twitter.com/2/tweets",
    json={"text": "Check this out!", "media": {"media_keys": [media_id]}}
)
```

### Thread Posting

```python
tweets = ["First tweet", "Second tweet", "Third tweet"]
prev_id = None
for text in tweets:
    payload = {"text": text}
    if prev_id:
        payload["reply"] = {"in_reply_to_tweet_id": prev_id}
    resp = client.post("https://api.twitter.com/2/tweets", json=payload)
    prev_id = resp.json()["data"]["id"]
```

### Error Handling

- `403 Forbidden` — check token permissions (needs `tweet.write`)
- `429 Too Many Requests` — rate limit exceeded; implement exponential backoff
- `401 Unauthorized` — token expired or invalid; re-authenticate

### Rate Limits (v2)

- **Tweet creation:** 200 per 15 min per user
- **Media upload:** 500 per 24 hours
- **Read timeline:** 180 per 15 min

### Analytics

```python
response = client.get(
    "https://api.twitter.com/2/users/me/tweets",
    params={"tweet_fields": "public_metrics,created_at", "max_results": 10}
)
for tweet in response.json()["data"]:
    print(f"{tweet['text'][:50]}... | Likes: {tweet['public_metrics']['like_count']}")
```

---

## Appendix C: Cronjob Scheduling

Schedule recurring content distribution via cronjob.

**Daily LinkedIn post:**
```yaml
prompt: "Draft and post a daily update to LinkedIn using content-engine voice and formatting."
enabled_toolsets: ["web", "send_message"]
schedule: "0 9 * * *"
```

**Thread campaign:**
```yaml
prompt: "Post the next tweet in the #BuildInPublic thread series. Reference previous tweets via the X API."
enabled_toolsets: ["web", "terminal"]
schedule: "0 10 * * 1,3,5"
```


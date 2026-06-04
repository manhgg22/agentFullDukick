---
name: b2b-account-analysis
description: |
  Evaluate B2B sales leads by reading internal vault, analyzing client briefs, researching prospects, benchmarking budgets against historical data, and packaging multi-tier proposals. For Account/Agency teams assessing prospective jobs before committing creative or production resources.
trigger:
  - User shares a prospective client brief and asks for assessment or recommendation
  - A suspected budget gap exists between client expectation and agency standard pricing
  - Team member requests tactical analysis of a new lead (go/no-go, packaging options)
  - A Google Doc or brief link is inaccessible and needs text extraction
  - User asks to "review" or "analyze" a customer inquiry
---

# B2B Account Analysis Workflow

## 1. Internal context mining
- Read the local vault / Discord logs / project notes for prior interactions with the client or similar clients.
- Search pricing/budget mentions (e.g., regex `[0-9]+M`, `budget`, `triệu`, `gói` in markdown logs) to establish anchors.
- Tools: `search_files` (target=content, path=vaultDir), `read_file`, `execute_code` for batch scanning.

## 2. Brief extraction
- If a Google Docs link is provided but requires login, try the summarizer fallback: `https://r.jina.ai/http://<full-google-doc-url>`.
- Identify fields: company name, product/service, deliverables, target audience, timeline, **stated budget**.

## 3. Prospect company research
- Scrape the company website with `requests` + regex cleanup (strip scripts/styles/tags).
- Extract: industry, company size cues, leadership, key partners, brand positioning, B2B vs B2C orientation.
- Assess production sophistication: have they done professional video before? (B2B niche clients often under-estimate costs by 5–10x.)

## 4. Budget benchmarking
- Compare client budget against:
  (a) Agency floor / standard pricing tiers
  (b) Internal comparable jobs from log mining
  (c) Market norms if available
- Quantify the gap. Flag "budget shock" when the gap exceeds roughly 3x.

## 5. Multi-tier option packaging (mandatory when gap >3x)
Never reject outright with a single high price. Design a pricing ladder:
- **Tier 1 (Fit budget):** Minimal viable scope; acknowledge limits explicitly.
- **Tier 2 (Mid):** Selective quality upgrades (e.g., better camera package, added voice-over).
- **Tier 3 (Premium):** Full-scope standard production matching agency positioning.
Clearly state scope, timeline, and exclusions per tier.

## 6. Risk assessment & next steps
- Decision-maker visibility → who signs off on budget?
- Client sophistication → will they understand production complexity?
- Competitor shopping → are they comparing with freelancers or other agencies?
- Timeline pressure → unrealistic deadlines increase OT risk.
- Tactical next steps: follow-up timing, pitch deck, discovery call, escalation to leadership.

## 7. Reporting
- Structure with tables: company facts, budget comparison, tier options, risk matrix.
- Provide a clear recommendation with **pros/cons** for each option.
- Cite internal data points or comparable past jobs whenever possible to show evidence-based reasoning.

## Key techniques
| Technique | Command / Pattern |
|-----------|-------------------|
| Locked Google Doc extraction | `https://r.jina.ai/http://<doc-url>` appended before the URL |
| Budget context from logs | `execute_code` scanning markdown with regex: `r'\b\d+M\b'`, `r'budget'`, `r'triệu'` |
| Website scraping fallback | `requests.get(url)` then `re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)` and strip remaining tags |
| Evidence-backed report | Cite specific log filenames, dates, or past job names alongside assertions |

## Pitfalls
1. **Locked brief documents** — Do not abandon a brief just because Google Docs requires login. Use the jina.ai fallback.
2. **Scraping JS-heavy sites** — Expect raw HTML noise; clean with regex rather than parsing frameworks. Do not attempt to render JavaScript.
3. **Single-option rejection** — Never reply with only a high price when the client budget is low. Always present a ladder.
4. **Missing internal benchmarks** — A proposal without anchors feels arbitrary and reduces Account credibility.
5. **Assuming client sophistication** — Niche B2B clients often have zero production literacy; explain tiers in business terms, not technical jargon.

## Evaluation checklist
- [ ] Vault scanned for client history and budget anchors
- [ ] Brief fully extracted with all required fields identified
- [ ] Company website scraped and summarized
- [ ] Budget gap quantified with internal evidence
- [ ] At least two pricing tiers proposed when a significant gap exists
- [ ] Risk matrix and tactical next steps included
- [ ] Report formatted for team review with tables and citations

## References
- `references/dukick-pricing-context.md` — Condensed internal pricing norms extracted from Discord/Obsidian logs for budget benchmarking.
- `references/google-doc-extraction.md` — Fallback pattern for extracting text from Google Docs that require authentication.
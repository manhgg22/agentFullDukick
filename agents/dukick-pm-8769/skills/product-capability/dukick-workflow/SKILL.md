---
name: dukick-workflow
description: Dukick agency PM/Account workflows — from brief intake and proposal generation to competitive intelligence and market tracking. Covers project lifecycle management (TVC/photo/shoot), multi-tier pricing, client expectation management, and Vietnamese TVC AI competitor monitoring.
category: product-capability
---

# Dukick Workflow

End-to-end project management and competitive intelligence workflows for Dukick — a Vietnamese video/photo production agency.

## When to Activate

- User is PM/Account at Dukick or discussing a TVC/photo/shoot project
- Receiving or analyzing a client brief (Canva, Google Docs, PDF, image)
- Evaluating a new lead: go/no-go, budget benchmarking, packaging
- Writing proposals, shooting proposals, or price quotes
- Managing client expectations, scope changes, or production risks
- Tracking TVC AI competitors in the Vietnamese market
- User mentions "Dukick", "TVC", "shoot", "brief", "báo giá", "đối thủ", or "proposal"

---

## I. Project Lifecycle (Account/PM)

### Core Mindset

- **Ownership:** Account is the "mini-CEO" of the project. No blaming clients or crew.
- **Solution-oriented:** Every problem report comes with ≥2 options + pros/cons.
- **Client-centric but not servile:** Push back when requests harm quality or company interests.

### Three Pillars

| Pillar | Principle | If compromised |
|--------|-----------|----------------|
| **Quality** | Meet aesthetic + client standards | Lose reputation, no re-contract |
| **Timeline** | Stick to schedule | Contract penalties, damaged relationships |
| **Budget** | Control costs, limit on-set overruns | Lose money, low margins |

### Key Skills

1. **Two-way translation:** Client language ↔ technical language ↔ business language
2. **Expectation management:** Under-promise, over-deliver. Clear Scope of Work from day one.
3. **Risk management:** Always have Plan B, Plan C. Backup shots for post-production.
4. **Documentation:** Every major step has written confirmation (email/minutes). External files: **comment only, never editable**.

---

## I-B. Client Feedback Capture & Meeting Recap Storage

When client feedback arrives from a pitch, review meeting, or creative presentation (often via Google Docs):

1. **Extract** the Google Doc content:
   ```bash
   curl -L -s "https://docs.google.com/document/d/{DOC_ID}/export?format=txt" -o recap.txt
   ```
2. **Synthesize** into a structured markdown file. Cover:
   - Meeting date, project, attendees, budget/timeline discussed
   - Each idea/proposal presented with summary
   - Verbatim or summarized feedback **per stakeholder** (who said what — critical for tracing decisions)
   - Go / Adjust / No-Go decision per item
   - Specific adjustments requested (with quotes when possible)
   - Next steps with dates and owners
3. **Save** the file into the project's skill `references/` directory:
   - Naming pattern: `client-feedback-{YYYYMMDD}.md` or `meeting-recap-{YYYYMMDD}.md`
4. **Update** the project's SKILL.md to add a pointer under a "### Client Feedback" or "### Meeting Recaps" subsection so future agents can find it.
5. **Notify** the team in the project channel with a concise summary — decision table + required adjustments + next steps.

**File template:**

```markdown
# Nhận xét khách hàng — {Meeting Type} {Project Name}

**Ngày họp:** YYYY-MM-DD
**Dự án:** ...
**Ngân sách đề xuất:** ...
**Tiến độ:** ...

---

## 1. {Idea/Option Name}

### Nội dung trình bày
...

### Phản hồi từ khách hàng
- **{Name}** ({role}):
  - ...

### Quyết định
- Go / Adjust / No-Go + lý do

---

## 2. {Idea/Option Name}
...

---

## Tổng hợp quyết định

| Phương án | Quyết định | Lý do |
|-----------|-----------|-------|
| ... | ... | ... |

---

## Điều chỉnh cần thực hiện

1. ...
2. ...

---

## Next Steps
- ...
```

---

## II. Brief Intake & Content Extraction

**Always extract and read the brief before analysis.**

### Verifying Claimed Documents

When a user says "from the SOW/brief/meeting notes/files I provided" or references prior attachments:

1. **Search filesystem first** — `search_files`, `terminal` on common locations (Downloads, Desktop, Documents, `tailieu/`, `vault-pm/`).
2. **Search session history** — `session_search` for keywords (client name, project name, "SOW", "brief", "meeting").
3. **If nothing found:** Tell the user explicitly which documents are missing and ask them to re-upload or paste content. **Do not fabricate analysis** based on the user's verbal recap alone.
4. **Discord attachments:** Agents cannot directly download Discord attachments via filesystem tools. If the user references "the file I sent earlier in this channel," ask them to re-upload or copy-paste the content.

### Canva Share Links
- Usually return HTML shell (requires login). Do NOT use `requests` to read.
- Action: ask client for PDF/PNG export or screenshots per page.
- See `references/canva-brief-pitfall.md` for details.

### Excel Briefs (.xlsx)
See `references/youtube-reference-extraction.md` for extraction pipeline and `references/tvc-creative-direction-framework.md` for creative direction development.

### Google Docs (Login Required)
- Use fallback `r.jina.ai` proxy to extract text.
- See `references/google-doc-extraction.md` for template.

### Image-based PDFs
1. Try `pdfplumber` for text extraction.
2. If `page.extract_text()` returns empty → image-based PDF.
3. **Pipeline:** PyMuPDF → PNG per page → batch 4-5 pages → `vision_analyze`.
- See `references/pdf-image-extraction-pipeline.md` for full code.

### Excel Briefs (.xlsx)
1. **Do NOT use pandas** — not available in sandbox environments.
2. Install `openpyxl` via terminal: `pip install openpyxl`
3. Load workbook with `data_only=True` to get cell values, not formulas.
4. Iterate rows and print all non-empty cells.
5. **Pitfall:** `.xlsx` files from clients often have merged cells or headers spanning multiple rows — inspect raw output before interpreting structure.

```python
import openpyxl
wb = openpyxl.load_workbook(path, data_only=True)
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    for row in ws.iter_rows(values_only=True):
        if any(cell for cell in row if cell is not None):
            print(" | ".join(str(cell) if cell else "" for cell in row))
```

### YouTube Reference Videos
When client sends YouTube links as creative references:
1. **Primary:** Extract transcript via `youtube-transcript-api` with Python (languages=['en', 'vi']).
2. **Fallback:** Use `r.jina.ai` proxy: `curl -sL "https://r.jina.ai/http://youtube.com/watch?v=VIDEO_ID"`
3. **Fallback 2:** Use `r.jina.ai/http://textise.iitty.com` or ask client for screenshot/transcript.
4. **What to capture:** Title, description, visual style notes, pacing, music style, key scenes, tone, color palette, camera movement.
5. Store extracted reference notes in `references/youtube-reference-extraction.md` for reuse.

### Images / Screenshots
- Use `vision_analyze` directly.
- Multiple images → vertical strip via PIL.

---

## III. Brief Analysis (10 Sections)

| Section | What to Capture |
|---------|-----------------|
| **Project Overview** | Name, client, type, concept, scene count |
| **Scene-by-scene** | Key Mood, Hero Shot, Shot list (Wide/Medium/Close-up/Motion), Lighting, Location, Props |
| **Casting** | Count, age range, role types, hour limits (especially children) |
| **Wardrobe** | Set count, color tone, style |
| **Technical Requirements** | Aspect ratio, lighting, camera movement, output format |
| **Deliverables** | Photo count, video count, resolution, file format |
| **Timeline** | Shoot date, delivery date, estimated days |
| **Budget** | Client provided? If not → Dukick quotes separately |
| **Usage Rights** | Duration, territory, exclusive/non-exclusive |
| **Contact & Approval** | Who approves final? Third-party agency involved? |

### Strength / Weakness Assessment

**Strong briefs usually have:** mood board, reference images, classified shot list, props list, camera movement references.

**Weak briefs usually lack:** budget, detailed schedule, output specs, usage rights, shoot date realism, contact/approval chain.

---

## IV. Prospect Research & Budget Benchmarking

1. **Internal data:** Read vault/Discord logs/project notes. Search for price anchors with regex: `\b\d+M\b`, `budget`, `triệu`, `gói`.
2. **External research:** Scrape client website for industry, size, positioning, B2B vs B2C.
3. **Budget comparison:** Compare against (a) agency floor/pricing tiers, (b) internal comparable jobs, (c) market norms. Quantify gap. Warn "budget shock" when gap >3x.

---

## V. Go / Adjust / No-Go Decision

Fast triage on 4 factors:

| Factor | Red Flag | Impact |
|--------|----------|--------|
| **Budget gap** | Agency floor >25% above client expectation | Win rate drops sharply |
| **Selection criteria** | Client chooses **only by price** (no treatment/quality scoring) | Higher price almost always loses |
| **Relationship** | No prior work or warm intro | No trust premium to offset price |
| **Opportunity cost** | Team capacity tight or better lead available | Time here = lost win elsewhere |

**Decision matrix:**
- **0-1 red flags** → Continue with multi-tier packaging (Step VI).
- **2 red flags** → Consider single-option slimmed-down or relationship touchpoint.
- **3-4 red flags** → **Polite decline.** Don't waste time on near-zero-win proposals.

**Polite decline template:**
> "Em cảm ơn anh/chị đã cân nhắc Dukick. Sau khi đánh giá khối lượng công việc và so sánh với ngân sách dự kiến, em nhận thấy với mức đầu tư hiện tại, chúng em không đảm bảo được chất lượng đầu ra theo tiêu chuẩn của mình. Rất tiếc lần này chưa phù hợp để hợp tác. Mong có cơ hội khác ạ."

---

## VI. Multi-tier Packaging

**Mandatory when budget gap >3x and continuing.**

Design pricing ladder:
- **Tier 1 (Fit budget):** Minimal viable scope; state limitations clearly.
- **Tier 2 (Mid):** Selective quality upgrades (better camera, add voice-over, etc.).
- **Tier 3 (Premium):** Full-scope standard production matching agency positioning.

Each tier must specify: scope, timeline, exclusions.

---

## VII. Proposal & Pricing

### Proposal Deck (.pptx)
- Use `python-pptx`. Install: `pip install python-pptx`.
- See `templates/shooting_proposal_generator.py` for a dark/accent styled generator.

### Proposal Structure
1. **Cover** — Project name, client, date
2. **Concept Overview** — Creative direction in client's language
3. **Scene Breakdown** — Shot list per scene with reference images
4. **Production Plan** — Schedule, crew, equipment
5. **Deliverables** — Exactly what client receives
6. **Investment** — Tiered pricing with scope per tier
7. **Terms** — Timeline, usage rights, payment schedule
8. **About Dukick** — Relevant portfolio

---

## VIII. Competitive Intelligence (TVC AI Vietnam)

Automated competitor tracking for the Vietnamese TVC AI market.

### Schedule
- **2 reports/week:** Monday 10:00 and Thursday 10:00.
- **Monday report:** Scans Thursday 10:00 → Monday 10:00.
- **Thursday report:** Scans Monday 10:00 → Thursday 10:00.

### Report Structure (8 Sections)

1. **Quick Summary** — 5-7 bullets: new competitors, new products/cases, market sentiment
2. **Competitor Table** — Name, type, AI/TVC services, new cases, clients, claimed strengths, threat level to Dukick, source links
3. **Market Signals** — Is cheap AI TVC being advertised more? Hybrid AI usage? Client segments interested?
4. **Notable Cases** — 1-3 cases: content, AI usage level (concept/visual/motion/voice/edit/VFX/full AI), quality assessment, lesson for Dukick
5. **Competitor Messaging** — How they sell: faster, cheaper, no shoot needed, AI + production team, viral/social-first, AI storyboard/previs
6. **Opportunities for Dukick** — 3-5 action items: content ideas, service packaging, client sectors to follow, response to competitor claims
7. **Risks to Monitor** — Price undercutting, low-quality AI sold aggressively, agencies building in-house AI, client misconception "AI TVC = no production needed", copyright/voice/image rights issues
8. **Next Steps** — Specific actions before next report

### Competitor Types to Track
- Production houses, agencies, freelancer teams
- AI studios, post/VFX houses
- Animation studios, marketing agencies

See `references/bao-cao-tvc-ai-template.md` for full report template.

---

## IX. Policy: Strategy vs Job Separation

When answering general strategy questions, do NOT mix in specific job details unless explicitly requested.

- **General strategy** → broad principles, frameworks, benchmarks.
- **Specific job** → named client, exact pricing, crew details, dates.

This protects client confidentiality and keeps strategic advice reusable.

See `references/strategy-vs-job-separation.md` for full policy.

---

## Pitfalls

- **Don't analyze briefs without extracting content first.** Always read before judging.
- **Don't assume documents exist just because the user said "I already provided them."** Verify filesystem and session history; ask for re-upload if missing.
- **Don't quote before checking crew availability.** Under-promise, over-deliver.
- **Don't send editable files externally.** Comment-only always.
- **Don't skip the no-go filter.** 3-4 red flags = polite decline.
- **Don't inflate TAM in competitor reports.** Use segment-specific, defensible numbers.
- **Don't track competitors without source links.** Every claim needs a citation.
- **Canva links are HTML shells.** Never rely on `requests` for Canva content.
- **Image-based PDFs need vision pipeline.** `pdfplumber` alone won't work.
- **Discord attachments aren't auto-downloaded.** Agents cannot retrieve prior chat attachments via filesystem. Ask user to re-upload.

## Related Skills

- `brand-voice` — When proposals or content need a consistent, source-derived voice
- `media-generation` — For generating AI-assisted visuals in proposals
- `content-engine` — For distributing thought leadership and case studies

## Reference Files

- `references/canva-brief-pitfall.md` — Canva extraction gotchas
- `references/google-doc-extraction.md` — Google Docs via jina.ai proxy
- `references/pdf-image-extraction-pipeline.md` — Image-based PDF vision pipeline
- `references/bao-cao-tvc-ai-template.md` — Vietnamese TVC AI competitor report template
- `references/strategy-vs-job-separation.md` — Confidentiality policy
- `references/youtube-reference-extraction.md` — YouTube reference video extraction & analysis
- `references/tvc-creative-direction-framework.md` — TVC creative direction development from brief + reference
- `templates/shooting_proposal_generator.py` — Dark/accent styled PPTX generator

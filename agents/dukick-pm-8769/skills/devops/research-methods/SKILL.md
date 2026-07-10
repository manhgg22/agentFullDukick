---
name: research-methods
description: Multi-source deep research using firecrawl, exa neural search, and Context7 documentation lookup. Covers web scraping, semantic code search, company research, and up-to-date library/framework documentation retrieval.
category: devops
---

# Research Methods

Find, extract, and synthesize information from the web, code repositories, and documentation using specialized search and scraping tools.

## When to Activate

- Need to research a topic, company, technology, or competitor deeply
- Need up-to-date library or framework documentation
- Searching for code examples, API usage patterns, or implementation details
- User says "research", "find docs", "look up", "what does X do", or "competitor analysis"

---

## Tool A: Deep Research (Firecrawl + Exa MCPs)

Multi-source research using web scraping (Firecrawl) and semantic search (Exa).

### MCP Configuration

Add to `~/.claude.json`:

```json
"firecrawl": {
  "command": "npx",
  "args": ["-y", "firecrawl-mcp"],
  "env": { "FIRECRAWL_API_KEY": "YOUR_KEY" }
},
"exa": {
  "command": "npx",
  "args": ["-y", "exa-mcp-server"],
  "env": { "EXA_API_KEY": "YOUR_KEY" }
}
```

### Workflow

1. **Query decomposition:** Break complex questions into atomic sub-questions
2. **Parallel search:** Use Firecrawl for broad web scraping, Exa for targeted semantic search
3. **Source triangulation:** Cross-check claims across multiple sources
4. **Synthesis:** Combine findings into a coherent answer with citations
5. **Confidence scoring:** Rate each claim as high/medium/low confidence

### Firecrawl Patterns

```javascript
// Scrape a single page
await firecrawl.scrapeUrl({ url: "https://example.com" });

// Crawl a site
await firecrawl.crawl({ url: "https://example.com", limit: 10 });

// Extract structured data
await firecrawl.extract({
  url: "https://example.com",
  schema: { title: "string", price: "number" }
});
```

### Exa Patterns

```javascript
// Semantic search
await exa.search({ query: "React Server Components best practices", numResults: 5 });

// Code search
await exa.searchCode({ query: "useEffect cleanup pattern", numResults: 3 });

// Company research
await exa.findCompany({ name: "Stripe" });
```

---

## Tool B: Exa Neural Search

Direct Exa API access for semantic web and code search.

### Key Features

- **Semantic search:** Find conceptually related content, not just keyword matches
- **Code search:** Search GitHub, Stack Overflow, documentation with intent matching
- **Company research:** Find company information, funding, competitors, news
- **News search:** Time-bounded search for recent events

### Search Types

| Type | Use Case |
|------|----------|
| `search` | General web content |
| `searchCode` | Code repositories and snippets |
| `findCompany` | Company profiles and data |
| `searchNews` | Recent news articles |

### Query Tips

- Use natural language, not boolean operators
- Include context: "React 19 use hook pattern" not just "use hook"
- Filter by date for time-sensitive queries: `dateFilter: { startDate: "2024-01-01" }`
- Filter by domain for authoritative sources: `includeDomains: ["github.com", "mdn.io"]`

---

## Tool C: Documentation Lookup (Context7 MCP)

Retrieve up-to-date library and framework documentation via Context7 MCP.

### MCP Configuration

Add to `~/.claude.json`:

```json
"context7": {
  "command": "npx",
  "args": ["-y", "context7-mcp"],
  "env": { "CONTEXT7_API_KEY": "YOUR_KEY" }
}
```

### Workflow

1. Identify the library/framework and version
2. Query Context7 for the specific API or concept
3. Receive structured documentation with examples
4. Verify against the official docs if the API is critical

### Example Queries

```javascript
// Get React 19 documentation for use hook
await context7.query({
  library: "react",
  version: "19.0.0",
  query: "use hook server components"
});

// Get Next.js App Router docs
await context7.query({
  library: "next",
  version: "15.0.0",
  query: "app router server actions"
});
```

### When to Use vs Web Search

- **Context7:** When you need authoritative, version-specific API documentation
- **Web search:** When you need tutorials, blog posts, Stack Overflow answers, or opinions
- **Both:** For critical decisions, cross-check Context7 with recent web sources

---

## Synthesis Best Practices

1. **Always cite sources.** Include URLs and retrieval dates.
2. **Distinguish fact from opinion.** Label claims accordingly.
3. **Note confidence levels.** High = multiple authoritative sources agree; Low = single source or conflicting information.
4. **Highlight gaps.** If information is missing or contradictory, say so explicitly.
5. **Update stale data.** Web information decays; note when data was retrieved.

## Pitfalls

- **Don't trust a single source.** Always triangulate important claims.
- **Beware SEO spam.** Low-quality sites rank high; evaluate source credibility.
- **Version sensitivity.** Documentation changes; verify you're reading the right version.
- **Hallucination risk.** LLMs may invent sources or misrepresent content. Always verify tool outputs.

## Related Skills

- `software-engineering` — Apply research findings to code decisions
- `investor-relations` — Use research for market and competitor analysis
- `content-engine` — Use research for content creation and fact-checking

---
name: obsidian-toolkit
description: Complete Obsidian vault toolkit — Flavored Markdown syntax, Bases databases, CLI automation, JSON Canvas maps, and clean web extraction. Use when working with Obsidian notes, .base files, .canvas files, CLI vault operations, or extracting readable content from web pages into markdown.
category: content
---

# Obsidian Toolkit

A unified skill for all Obsidian-related work: note authoring, database views, visual canvases, CLI vault automation, and clean web-to-markdown extraction.

## When to Activate

- Creating or editing Obsidian notes (.md), .base files, or .canvas files
- Using the Obsidian CLI to read, create, search, or manage vault notes
- Working with wikilinks, callouts, embeds, properties, or tags
- Building database-like views with filters, formulas, and summaries in `.base` files
- Creating mind maps, flowcharts, or visual planning boards in `.canvas` files
- Extracting clean markdown from web pages (Defuddle) for Obsidian or general use
- User mentions "Obsidian", "vault", "wikilink", "callout", "canvas", "base", or "defuddle"

---

## Obsidian Flavored Markdown

### Creating Notes

1. Add frontmatter with properties at the top.
2. Use standard Markdown for structure plus Obsidian-specific syntax.
3. Link related notes with `[[wikilinks]]` for internal vault connections.
4. Embed content from other notes, images, or PDFs with `![[embed]]`.
5. Add callouts with `> [!type]` syntax.

### Wikilinks

```markdown
[[Note Name]]                          Link to note
[[Note Name|Display Text]]           Custom display text
[[Note Name#Heading]]                  Link to heading
[[Note Name#^block-id]]                Link to block
```

Define a block ID by appending `^block-id` to any paragraph.

### Embeds

```markdown
![[Note Name]]                         Embed full note
![[Note Name#Heading]]                 Embed section
![[image.png]]                         Embed image
![[image.png|300]]                     Embed image with width
![[document.pdf#page=3]]               Embed PDF page
```

### Callouts

```markdown
> [!note]
> Basic callout.

> [!warning] Custom Title
> Callout with custom title.

> [!faq]- Collapsed by default
> Foldable callout (- collapsed, + expanded).
```

Common types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`.

### Properties (Frontmatter)

```yaml
---
title: My Note
date: 2024-01-15
tags:
  - project
  - active
aliases:
  - Alternative Name
cssclasses:
  - custom-class
---
```

### Tags

```markdown
#tag                    Inline tag
#nested/tag             Nested tag with hierarchy
```

### Comments

```markdown
This is visible %%but this is hidden%% text.

%%
This entire block is hidden in reading view.
%%
```

### Highlighting

```markdown
==Highlighted text==
```

---

## JSON Canvas

Canvas files (`.canvas`) contain `nodes` and `edges` arrays following the JSON Canvas Spec 1.0.

### Node Types

- **text**: `id`, `type`, `x`, `y`, `width`, `height`, `text`
- **file**: `id`, `type`, `x`, `y`, `width`, `height`, `file`
- **link**: `id`, `type`, `x`, `y`, `width`, `height`, `url`
- **group**: `id`, `type`, `x`, `y`, `width`, `height`, `label`, `background`

### Edges

Connect nodes via `fromNode` and `toNode` with optional `fromSide`/`toSide` (top, right, bottom, left) and `label`.

### Workflow

1. Create `.canvas` with `{"nodes": [], "edges": []}`
2. Generate unique 16-char hex IDs for each node
3. Add nodes with required fields
4. Add edges referencing valid node IDs
5. **Validate**: all IDs unique, all edge references resolve

---

## Obsidian Bases

Base files (`.base`) use YAML with filters, formulas, properties, summaries, and views.

### Schema

```yaml
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

formulas:
  total: "price * quantity"
  status_icon: 'if(done, "✅", "⏳")'

properties:
  status:
    displayName: Status

views:
  - type: table
    name: "Active Tasks"
    order:
      - file.name
      - status
      - formula.status_icon
```

### Key Functions

- `date()`, `now()`, `today()`, `if()`, `duration()`, `file()`, `link()`
- Duration fields: `.days`, `.hours`, `.minutes` — access before rounding

### YAML Quoting

- Use single quotes for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Quote strings containing special YAML characters

---

## Obsidian CLI

Interact with a running Obsidian instance via the `obsidian` CLI.

### Common Patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
```

### Plugin Development

```bash
obsidian plugin:reload id=my-plugin
obsidian dev:errors
obsidian dev:screenshot path=screenshot.png
obsidian dev:dom selector=".workspace-leaf" text
obsidian dev:console level=error
obsidian eval code="app.vault.getFiles().length"
```

Use `vault=<name>` as the first parameter to target a specific vault.

---

## Defuddle — Clean Web-to-Markdown Extraction

Use Defuddle CLI to extract clean readable content from web pages, removing navigation, ads, and clutter.

### Install

```bash
npm install -g defuddle
```

### Usage

```bash
defuddle parse <url> --md
defuddle parse <url> --md -o content.md
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

### Output Formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default) |
| `--json` | JSON with HTML and markdown |
| (none) | HTML |
| `-p <name>` | Specific metadata property |

Do NOT use for URLs ending in `.md` — those are already markdown, use direct read instead.

---

## References
- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Obsidian CLI Docs](https://help.obsidian.md/cli)

---
name: obsidian-workflows
description: End-to-end workflows for Obsidian — markdown syntax, CLI automation, visual canvases, and database views. Use when working with .md files, .canvas files, .base files, or the Obsidian CLI in any capacity.
---

# Obsidian Workflows

Class-level skill covering the Obsidian ecosystem: Flavored Markdown, CLI automation, JSON Canvas visual maps, and Bases database views. These four surfaces share a vault-centric mental model but serve different jobs.

## When to use

- Creating or editing notes inside an Obsidian vault
- Automating vault operations from the command line (read, create, search, append, set properties)
- Building visual canvases, mind maps, flowcharts, or knowledge graphs with `.canvas` files
- Creating database-like views with filters, formulas, and summaries using `.base` files
- Developing or debugging Obsidian plugins and themes

## 1. Obsidian Flavored Markdown

Obsidian extends CommonMark/GFM with wikilinks, embeds, callouts, properties, comments, and highlight syntax.

### Wikilinks
```markdown
[[Note Name]]
[[Note Name|Display Text]]
[[Note Name#Heading]]
[[Note Name#^block-id]]
```

### Embeds
```markdown
![[Note Name]]
![[image.png|300]]
![[document.pdf#page=3]]
```

### Callouts
```markdown
> [!note]
> Basic callout.

> [!warning] Custom Title
> Custom title callout.
```

Common types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`.

### Properties (Frontmatter)
```yaml
---
title: My Note
date: 2024-01-15
tags:
  - project
aliases:
  - Alternative Name
---
```

### Tags & Comments
```markdown
#tag                    Inline tag
#nested/tag             Nested tag
%%hidden%%             Inline comment
```

### Math & Diagrams
```markdown
Inline: $e^{i\pi} + 1 = 0$
Block:
$$
\frac{a}{b} = c
$$
```

Use Mermaid for diagrams in code fences labeled `mermaid`.

## 2. Obsidian CLI

The `obsidian` CLI interacts with a running Obsidian instance. Requires Obsidian to be open.

### Common commands
```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" silent
obsidian append file="My Note" content="New line"
obsidian search query="term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
```

### Vault targeting
Default targets the most recently focused vault. Use `vault=<name>` as the first parameter for a specific vault.

### Plugin development cycle
```bash
obsidian plugin:reload id=my-plugin
obsidian dev:errors
obsidian dev:screenshot path=screenshot.png
obsidian dev:dom selector=".workspace-leaf" text
obsidian eval code="app.vault.getFiles().length"
```

## 3. JSON Canvas

Create and edit `.canvas` files with nodes, edges, groups, and connections.

### Base structure
```json
{
  "nodes": [],
  "edges": []
}
```

### Node types
- `text` — requires `text` (supports Markdown)
- `file` — requires `file` path
- `link` — requires `url`
- `group` — visual container with optional `label`

### Generic node attributes
| Attribute | Required | Description |
|-----------|----------|-------------|
| `id` | Yes | Unique 16-char hex |
| `type` | Yes | `text`, `file`, `link`, `group` |
| `x`, `y` | Yes | Position in pixels |
| `width`, `height` | Yes | Dimensions |
| `color` | No | Preset `"1"`-`"6"` or hex |

### Edges
```json
{
  "id": "...",
  "fromNode": "...",
  "toNode": "...",
  "fromSide": "right",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "leads to"
}
```

### Validation checklist
1. All IDs unique across nodes and edges
2. Every `fromNode`/`toNode` references an existing node ID
3. Required fields present per node type
4. `type` is one of the four valid values
5. Sides are `top`, `right`, `bottom`, `left`
6. Ends are `none` or `arrow`
7. JSON is valid and parseable

## 4. Obsidian Bases

Create and edit `.base` files with views, filters, formulas, and summaries.

### Base schema
```yaml
filters:
  and: []
  or: []
  not: []

formulas:
  formula_name: 'expression'

properties:
  property_name:
    displayName: "Display Name"

views:
  - type: table | cards | list | map
    name: "View Name"
    order:
      - file.name
      - property_name
```

### Key formula functions
| Function | Description |
|----------|-------------|
| `date()` | Parse string to date |
| `now()` | Current datetime |
| `today()` | Current date (time = 00:00:00) |
| `if()` | Conditional |
| `duration()` | Parse duration string |

### Duration pitfall
Subtracting dates returns a **Duration**, not a number. Access `.days`, `.hours`, etc. before rounding:
```yaml
# CORRECT
"(now() - file.ctime).days.round(0)"

# WRONG
"(now() - file.ctime).round(0)"
```

### View types
- `table` — tabular data with columns
- `cards` — card grid layout
- `list` — simple list
- `map` — requires lat/lng and Maps plugin

## Pitfalls

- **Wikilink block IDs**: place `^block-id` on a separate line after list/quote blocks, not inline.
- **Newlines in JSON canvas text nodes**: use `\n` inside JSON strings, never literal `\\n`.
- **YAML quoting**: wrap formulas containing double quotes in single quotes. Strings with `:`, `{`, `}`, `[`, `]`, `,`, `&`, `*`, `#`, `?`, `|`, `-`, `<`, `>`, `=`, `!`, `%`, `@`, `` ` `` must be quoted.
- **Missing null checks in bases**: properties may be empty; guard with `if()`.
- **CLI requires open Obsidian**: the `obsidian` CLI cannot start Obsidian, only talk to a running instance.
- **Canvas z-index**: array order determines layer — first = bottom, last = top.

## Tool combos

| Job | Primary tool | Secondary |
|-----|-------------|-----------|
| Write a note | Obsidian app | `obsidian create` |
| Build a mind map | `.canvas` file | `json-canvas` spec |
| Database view | `.base` file | Bases plugin |
| Batch vault ops | `obsidian` CLI | bash scripts |
| Plugin dev | `obsidian dev:*` | `obsidian eval` |

## References

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Obsidian CLI Docs](https://help.obsidian.md/cli)

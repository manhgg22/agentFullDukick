---
name: internal-knowledge-query
description: When user references internal knowledge repositories (Obsidian vaults, internal docs, knowledge bases), search and extract from those sources first before generalizing. Synthesize accurately from internal documents with the structure and style requested.
triggers:
  - User says "đào sâu trong [source]", "dùng thông tin từ [source]", "theo tài liệu nội bộ"
  - User references Obsidian vaults, internal wikis, or team knowledge bases
  - User asks for information from a specific internal document or system
---

# Internal Knowledge Query

## Trigger
User explicitly references an internal knowledge repository (Obsidian vault, internal docs, team wiki, etc.) and asks for information from it.

## Workflow

### 1. Search the repository FIRST
- Do NOT answer from general knowledge or training data.
- Use `search_files` to locate relevant files in the path the user specified.
- If the user says "Obsidian", search the Obsidian vault paths (`C:/Users/Admin/Documents/Obsidian Vault/` or equivalent).
- Read the actual files, not just filenames.

### 2. Extract exact content
- Read the full content of relevant files using `read_file`.
- Look for the specific information the user requested.
- If multiple files are relevant, read all of them before synthesizing.

### 3. Synthesize from internal sources only
- Build the answer using ONLY what you found in the internal docs.
- Do NOT mix in general knowledge unless explicitly instructed.
- If the internal docs don't cover something, say so — don't guess.

### 4. Respect user's structure request
- If user says "định vị trước, chi tiết sau" → follow that exact order.
- If user specifies style ("ngắn gọn, chiến lược, đừng dài dòng") → respect it.
- If user specifies audience ("bạn mới vào") → adjust language and depth accordingly.

### 5. Accuracy over completeness
- The user said "đưa chính xác" — prioritize accuracy.
- Quote or paraphrase directly from internal docs.
- Don't embellish or add interpretations not in the source.

## Pitfalls
- ❌ Answering from general knowledge when user explicitly asked for internal docs.
- ❌ Skimming filenames instead of reading file contents.
- ❌ Mixing external knowledge with internal docs without labeling.
- ❌ Ignoring user's output structure preferences.
- ❌ Adding fluff when user asked for "ngắn gọn, chiến lược".

## Effective User Prompt Patterns (recognize and follow precisely)
When users prompt with this structure, execute exactly:
1. **Source specified**: "Đào sâu trong [repository]"
2. **Accuracy demanded**: "Đưa chính xác [topic]"
3. **Output structure**: "Đầu tiên [A], rồi sau đó [B]"
4. **Style constraint**: "Ngắn gọn, chiến lược, đừng dài dòng"
5. **Audience specified**: "Làm sao để [audience] có thể hiểu được"

## Verification
After building the answer, ask yourself:
- Did I search and read the internal docs?
- Is every claim traceable to the internal sources?
- Did I follow the user's requested structure?
- Is the tone/style appropriate for the specified audience?
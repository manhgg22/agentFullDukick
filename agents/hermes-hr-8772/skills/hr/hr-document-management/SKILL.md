---
name: hr-document-management
description: Receive, read, summarize, and securely store HR documents into the Obsidian vault with confidentiality safeguards
title: HR Document Management
version: 1.0
triggers:
  - User uploads or sends HR documents (CSV, XLSX, PDF, DOCX, TXT)
  - User asks to save, import, or archive HR files
  - User requests a summary of HR data from attached files
  - User shares company account lists, employee lists, salary data, or policy documents
---

# HR Document Management

## Purpose
Receive, read, summarize, and securely store HR-related documents into the Obsidian vault. Maintain confidentiality and produce a clear tombstone summary for the user.

## Steps

1. **Acknowledge receipt**
   - Confirm the file name and format.
   - State that you are reading and will store it.

2. **Read the file(s)**
   - Use `read_file` for each document.
   - For spreadsheets (CSV/XLSX), scan headers and sample rows to understand schema.
   - Note the presence of any sensitive fields (passwords, CCCD/ID numbers, salary, bank info).

3. **Summarize contents**
   - Produce a concise tombstone summary per file:
     - File name
     - Primary content / schema overview
     - Key categories or sections
     - Approximate record counts or notable entries
   - Do NOT reproduce raw passwords, full ID numbers, or unredacted personal data in the summary.

4. **Save into the Obsidian vault**
   - Copy the original file into the appropriate vault subfolder:
     - `TaiLieu-NhanSu/` — employee lists, contracts, org charts
     - `ChinhSach/` — policies, regulations, benefit rules
     - `TuyenDung/` — JDs, interview schedules, candidate data
     - `Onboarding/` — training materials, checklists
     - `QuanTri/` — administrative plans, KPIs, salary structures
   - Preserve the original file name or use a clean, descriptive name.

5. **Record durable metadata**
   - Write a `memory` entry capturing:
     - Vault path of each saved file
     - High-level description of what it contains
     - Any confidentiality flags (e.g., "contains salary data", "contains account passwords")

6. **Confirm completion**
   - List the saved files with their vault paths in a table.
   - Reiterate confidentiality commitments if sensitive data is present.
   - Offer next actions (lookup, analysis, reporting).

## Confidentiality Rules

- **Passwords / credentials:** Summarize that a list exists; never echo passwords in chat.
- **Personal identifiers (CCCD, SĐT, address):** Note that they are present; do not repeat them.
- **Salary / compensation data:** Summarize ranges or totals only when relevant; do not itemize individual salaries unless explicitly asked.
- **State clearly:** "Em cam kết bảo mật tuyệt đối — không chia sẻ thông tin này ra ngoài khi chưa có sự cho phép của anh/chị."

## Pitfalls

- Do NOT create Discord threads for document intake.
- Do NOT assume Google Sheets links are public — if a link returns 404, prompt the user to set sharing to "Anyone with the link can view" or export and re-upload.
- Do NOT overwrite existing files silently; if a file with the same name exists, append a timestamp or version suffix.
- Do NOT skip the memory step — future sessions depend on it to know what is already in the vault.
- **Google Sheets link returns 401 instead of 404?** This means the file exists but is private (`usp=drive_link`). Ask the user to change sharing to "Anyone with the link can view" and retry.
- **Multiple files arriving at once?** Process all of them before summarizing, but confirm receipt of each file name immediately so the user knows nothing was dropped.

## Related Files
- `references/dukick-vault-structure.md` — Vault folder conventions and active data catalog

# Discord Log File Structure Example

## Filename
`YYYY-MM-DD.md` — one file per calendar day, placed in `Discord/` under each vault.

## Content Example (from Dukick-Tong, 2026-06-03)

```markdown
# 📋 Báo Cáo Tổng Hợp Discord Dukick — Ngày 02/06/2026 & 03/06/2026

> Coordinator: anh Mạnh đẹp trai  
> Ngày báo cáo: 03/06/2026  
> Chuẩn bị cho: chị @Leo🌷 (Leader)

---

## 📊 Tổng Quan 2 Ngày

| Ngày | Sự kiện chính | Kênh liên quan | Cần leader xử lý |
|------|--------------|----------------|------------------|
| 02/06 | Chất vấn vấn đề điều nguồn tiền | #pm | ⚠️ Cần quy trình rõ ràng |
| ... | ... | ... | ... |
```

## Key Characteristics

1. **Headers are agent-generated**, not raw Discord exports. Each day's file is a synthesized report (not a transcript).
2. **Mixed-date files are common** — a single `.md` may cover multiple days (e.g. `02/06/2026 & 03/06/2026`) when the agent batch-reports.
3. **UTF-8 with BOM** — files may start with `\ufeff`. Always open with `encoding="utf-8-sig"`.
4. **Vault-specific content** — each vault's `Discord/` folder only logs activity relevant to that bộ phận. Cross-vault correlation is done by the Tổng agent.
5. **No file = no activity** — absence of a date file means no logged activity for that day in that vault.

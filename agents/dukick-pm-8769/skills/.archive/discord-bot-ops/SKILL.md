---
name: discord-bot-ops
description: Discord bot API operations, workarounds, and messaging patterns for Hermes agents when built-in tools fall short.
category: operations
---

# Discord Bot Operations

## When to use
- The built-in `send_message` tool fails for Discord DMs or specific channels.
- You need to send a Direct Message (DM) to a Discord user via bot token.
- You need to interact with the Discord REST API directly from `execute_code`.

## Pattern: Send DM via REST API

**Problem:** `send_message` to a Discord user ID (e.g., `discord:948828130213236766`) often fails with "Unknown Channel" because a user ID is not a channel ID. Discord requires creating a DM channel first.

**Solution:** Use the Discord REST API directly with `curl` from `execute_code`.

### Step 1: Create DM channel
```bash
curl -s -X POST https://discord.com/api/v10/users/@me/channels \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipient_id":"USER_ID"}'
```

The response JSON contains `"id"` — this is the DM channel ID.

### Step 2: Send message to DM channel
```bash
curl -s -X POST "https://discord.com/api/v10/channels/$DM_CHANNEL_ID/messages" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Your message here"}'
```

## Finding the bot token
- Check the agent's `.env` file for `DISCORD_BOT_TOKEN`.
- On Windows with MSYS/bash, read it via `cat` or `grep` in `execute_code` / `terminal`.

## Pitfalls
- **Rate limits:** 5 DMs per 5 seconds per user for non-verified bots.
- **Permissions:** The recipient must not have disabled DMs from server members.
- **Channel vs User ID:** Never confuse a Discord user snowflake with a channel snowflake. DM channels are created on demand.
- **Tool limitation:** The built-in `send_message` (or `mcp_send_message`) may not support DM creation; always fall back to raw API when it fails.

## References
- `references/discord-dm-reproduction.md` — Full transcript of a successful DM send via raw API.
---
name: discord-ops
description: Discord server management, automation, bot API operations, and messaging patterns for Hermes agents. Covers server setup, role configuration, thread messaging, cronjob integration, and raw API workarounds when built-in tools fall short.
category: operations
---

# Discord Operations

Use this skill when working with Discord servers, bots, automation, or messaging — whether setting up a new server, configuring roles, sending cronjob messages to threads, or falling back to raw API calls when built-in tools fail.

## When to Activate

- Setting up or governing a Discord server (roles, channels, ownership)
- Sending automated messages via cronjob to Discord threads
- The built-in `send_message` tool fails for DMs or specific channels
- You need to interact with the Discord REST API directly
- User says "Discord server", "Discord bot", "send to thread", or "Discord DM"

---

## Server Setup & Governance

> Applies when creating a new Discord server for a project or client.

### Create the Admin Role First
1. Create role **Admin** immediately after server creation.
2. Grant **all permissions** except the last row (reserved for Owner only).
3. Assign the Admin role to yourself.
4. Add the Admin role to **every private channel** before transferring ownership.
5. Transfer ownership to the designated final owner (e.g., chị Leo🌷).

### Ownership Rules
- Do not keep Owner on a personal account long-term.
- Final Owner should be a designated admin account for centralized management.
- Re-check permissions after setup completes.

---

## Automation: Cronjob & Thread Messaging

### Target Format for Threads
Use `discord:<chat_id>:<thread_id>` with `send_message`.

Example targets:
- `discord:1093083512837521448:1407966179758182447`
- `discord:1093083512837521448:1511955929615040573`

### Cronjob Configuration
- Set `enabled_toolsets: ["discord"]` in the cronjob.
- Prompt should specify the target thread per recipient.
- Update thread IDs in the cronjob prompt immediately when threads change.
- Always test `send_message` manually before enabling automation.

---

## Bot API Operations

### Sending DMs via Raw REST API

**Problem:** `send_message` to a user ID (e.g., `discord:948828130213236766`) fails with "Unknown Channel" because Discord requires creating a DM channel first.

**Solution:** Use raw Discord REST API calls from `execute_code`.

#### Step 1: Create DM channel
```bash
curl -s -X POST https://discord.com/api/v10/users/@me/channels \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipient_id":"USER_ID"}'
```

Extract `"id"` from the response — this is the DM channel ID.

#### Step 2: Send message
```bash
curl -s -X POST "https://discord.com/api/v10/channels/$DM_CHANNEL_ID/messages" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Your message here"}'
```

#### Finding the Bot Token
- Check the agent's `.env` file for `DISCORD_BOT_TOKEN`.
- On Windows with MSYS/bash, read it via `cat` or `grep` in `execute_code` / `terminal`.

---

## Pitfalls

- **Rate limits:** 5 DMs per 5 seconds per user for non-verified bots.
- **Permissions:** The recipient must not have disabled DMs from server members.
- **Channel vs User ID:** Never confuse a Discord user snowflake with a channel snowflake. DM channels are created on demand.
- **Built-in tool limitation:** `send_message` does not auto-create DM channels; always fall back to raw API when it fails.
- **Thread ID drift:** Thread IDs change or new threads are created — keep cronjob prompts updated.

---

## References
- `references/discord-dm-reproduction.md` — Full transcript of a successful DM send via raw API.

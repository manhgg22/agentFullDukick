---
name: messaging-platform-agent
version: 1.0.0
description: >
  How AI agents integrate with messaging platforms (Discord, Telegram, Slack) via gateway vs full API bot.
  Covers limits, capabilities, workarounds, and coordination SOPs when users expect omnipresence.
triggers:
  - User asks agent to scan / lurk / read history in channels or servers
  - User asks agent to create "jump to message" Discord links
  - User asks agent to monitor channels proactively without being @mentioned
  - User expresses frustration that agent "cannot see other channels"
  - Setting up multi-agent coordination on messaging platforms
  - User says "I need you everywhere I am" or equivalent omnipresence request
---

# messaging-platform-agent

## Two Completely Different Architectures

### 1. Gateway AI Agent (Hermes-style)
- Receives messages **only when @mentioned or replied to** in a channel
- **Cannot** lurk, scan, or read message history
- **Cannot** access channel list, member list, or message IDs
- **Cannot** create Discord "jump to message" links (needs `message_id` + `channel_id` + `guild_id` via API)
- Operates via text gateway, not Discord API
- No bot token, no OAuth, no server permissions

### 2. Full API Bot (MEE6, Carl-bot, Dyno, custom Discord.py)
- Has `Read Message History`, `View Channels`, `Manage Messages` permissions
- Can lurk, log, create jump links, react automatically, assign roles
- Requires bot token + OAuth setup + server admin granting permissions
- **Not** the same entity as the AI agent; they can forward data to the AI agent

## Critical Pitfall: Set Expectations BEFORE Frustration

**NEVER let the user assume the agent can "see everything."**

When a user asks to scan a server, monitor channels, or find messages:

1. State the limitation **immediately and clearly**
2. Explain **why** (gateway vs API architecture in one sentence)
3. Offer **workarounds** right away — don't just say "no"

**Bad pattern:**
> "Em xin lỗi chị, em không có quyền đọc lịch sử..."

**Good pattern:**
> "Em là AI gateway agent — em chỉ nhận tin khi được @mention. Để em 'nhìn thấy' các kênh khác, chị có thể: (1) @em ở mọi kênh, (2) setup webhook forward, hoặc (3) cho em cronjob ping định kỳ. Chị chọn cách nào?"

## Workarounds for Multi-Channel Awareness

| Option | Setup effort | User effort | Reliability |
|--------|-------------|-------------|-------------|
| **A. @mention in target channels** | Zero | High per msg | Instant |
| **B. Webhook / bot forward to home channel** | Medium (needs API bot) | Zero | High |
| **C. Cronjob periodic ping** | Low | Zero | Medium (misses urgent items) |
| **D. API bot collects jump links** | Medium | Zero | High |

### Option A: @mention in target channels
- Any team member tags `@AgentName` when something needs the agent
- Agent replies in-thread immediately
- **Best for:** teams already used to tagging people for approval

### Option B: Webhook / bot forward
- A full API bot with read permissions forwards important messages to the agent's home channel
- Agent reads and summarizes from home channel
- **Best for:** high-volume channels where tagging every message is noisy

### Option C: Cronjob periodic ping
- Agent posts in channels at scheduled times: *"Any tasks needing approval?"*
- Gom responses into a summary report
- **Best for:** daily/weekly batch review, not real-time

### Option D: Message link collection by API bot
- Use a full API bot to collect `https://discord.com/channels/{guild}/{channel}/{message}` links
- Agent reads the collected links and summarizes
- **Best for:** when the user specifically asked for "message links" or "exact message location"

## When User Says "I Need You Everywhere I Am"

This signals the user expects omnipresence. Respond with:

1. **Acknowledge** the need: *"Chị muốn em có mặt ở mọi nơi chị cần — em hiểu."*
2. **Explain** the architecture boundary in ≤2 sentences
3. **Present** 2–3 concrete options from the table above
4. **Ask** which to implement: *"Chị chọn cách nào? Em soạn SOP cho team luôn."*

**Do NOT:**
- Apologize repeatedly without offering solutions
- Suggest "em sẽ thử" when you know the architecture prevents it
- Wait for user frustration before explaining limits
- Use passive voice or vague excuses ("có lẽ", "để em xem lại")

## Discord-Specific: Permissions Map

| What user wants | What agent actually needs | Who can grant it |
|-----------------|---------------------------|------------------|
| Read all channels | `View Channels` + `Read Message History` via API bot | Server admin / owner |
| Create jump links | `Read Message History` + message ID access | API bot with permissions |
| Send to any channel | `Send Messages` in that channel | Channel admin / role permissions |
| @mention agent in any channel | Already works if agent is in the channel | Just add bot to channel |

## Reference
- `crosspost`: For content distribution across platforms
- `dmux-workflows`: For multi-agent orchestration patterns
# Resolving a Discord Snowflake to a Display Name

## Problem
Dukick vault exports anonymize Discord user mentions as `<@***>`.
Searching the vault for a raw snowflake (e.g. `1091125381421072425`) yields no readable hits.

## Canonical Resolution Workflow

1. **Send a raw mention** into the active Discord conversation via `send_message`.
   ```json
   {
     "action": "send",
     "message": "<@SNOWFLAKE>",
     "target": "discord"
   }
   ```
2. **Read the resulting chat message** inside Discord — the platform resolves the snowflake into the user's current display name automatically.
3. **Never rely on vault search** for identity lookup; it is guaranteed to be redacted.

## Limitations
- The agent **cannot** enumerate which servers a user belongs to.
- The agent **cannot** inspect member lists of arbitrary guilds.
- The only reliable server info comes from in-context sources (invite links opened via `browser_navigate`, or messages received in monitored channels).

## Related
- Pitfall #8 and #9 in `dukick-vault-ops/SKILL.md`

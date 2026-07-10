---
name: agent-workflow
description: Agent orchestration, debugging, and multi-pane terminal workflows. Covers structured self-debugging, multi-agent sort/plan evidence building, and tmux-based multi-pane management for parallel agent sessions.
category: operations
---

# Agent Workflow

Orchestrate multiple agents, debug agent failures, and manage parallel terminal sessions for complex multi-step tasks.

## When to Activate

- Debugging why an agent tool call failed or returned unexpected results
- Building an evidence-backed plan that requires multiple data sources
- Running multiple agents in parallel terminal panes
- The current agent is stuck, looping, or producing incorrect output
- User says "multi-agent", "parallel agents", "debug the agent", "orchestrate", or "tmux"

---

## Structured Self-Debugging

When an agent tool call fails or produces unexpected output, use this systematic workflow instead of guessing.

### Step 1: Gather Facts

Document in this order:
- Exact tool name and parameters used
- Full error message (not a summary)
- Expected vs actual output
- Tool documentation or source code (if available)
- Reproduction steps

### Step 2: Hypothesize

Generate 2-5 hypotheses, each with:
- Specific claim about what might be wrong
- Evidence that supports or contradicts it
- Confidence level (high/medium/low)

Example hypothesis:
> "The API endpoint changed from v1 to v2, causing a 404 error. Evidence: documentation shows v2 was released last month. Confidence: medium."

### Step 3: Test

Design a minimal test for each hypothesis:
- If endpoint changed → try v2 endpoint
- If auth expired → test with fresh token
- If parameter format wrong → try alternative format

### Step 4: Iterate

- Update confidence based on test results
- Cross off invalidated hypotheses
- If none remain, generate new ones
- Document what was learned

### Step 5: Resolve

- Apply the fix
- Verify with the original failing case
- Document the root cause and solution for future reference

---

## Multi-Agent Sort & Plan Building

When building an evidence-backed plan (e.g., installing a system, evaluating vendors), use parallel agents to gather and cross-check data.

### Workflow

1. **Decompose** the problem into independent research questions
2. **Assign** one question per agent
3. **Execute** agents in parallel (use `dmux` for local parallel sessions)
4. **Synthesize** results into a single coherent plan
5. **Validate** the plan against original constraints

### Evidence Requirements

Each agent must return:
- Source of each claim (URL, document, API response)
- Confidence level per claim
- Contradictions or gaps found
- Recommendation with justification

### Cross-Checking

- Run the same question through two agents with different toolsets
- Flag claims that only appear in one agent's output
- Require primary sources for critical decisions

---

## Multi-Pane Terminal Workflows (dmux)

Use `dmux` (tmux pane manager) to run multiple agents or commands in parallel terminal panes.

### Setup

```bash
# Install dmux
npm install -g dmux

# Or use tmux directly
tmux new-session -d -s my-session
tmux split-window -h
tmux split-window -v
```

### Common Patterns

**Parallel data gathering:**
```bash
dmux run --panes 3 --command "python gather_data.py --source {1}"
```

**Watch + Execute + Log:**
```bash
dmux run --layout grid --panes 4 \
  --command-1 "watch -n 5 'curl -s http://localhost:8080/health'" \
  --command-2 "python worker.py" \
  --command-3 "tail -f logs/app.log" \
  --command-4 "python monitor.py"
```

**Agent orchestration:**
```bash
dmux run --panes 3 \
  --command-1 "hermes agent --task 'Research competitor pricing'" \
  --command-2 "hermes agent --task 'Research feature comparison'" \
  --command-3 "hermes agent --task 'Research user reviews'"
```

### Key Commands

- `tmux new-session -d -s <name>` — create detached session
- `tmux split-window -h / -v` — split horizontally / vertically
- `tmux send-keys -t <session>:<window>.<pane> '<command>' C-m` — send command to pane
- `tmux attach -t <session>` — attach to session
- `tmux kill-session -t <session>` — clean up

### Best Practices

- Name sessions and panes descriptively
- Use `watch` or `tail -f` for monitoring panes
- Redirect output to files for later analysis
- Kill sessions when done to free resources
- Use `dmux` layouts (grid, row, column) for visual organization

---

## Pitfalls

- **Don't debug without facts.** Always gather the full error before hypothesizing.
- **Avoid single-point-of-failure.** Run critical checks through multiple agents.
- **Pane overload.** More than 4-6 panes becomes hard to monitor; use log files instead.
- **Agent loops.** If an agent keeps retrying the same failing call, stop it and debug.
- **Context contamination.** Parallel agents may interfere if they write to the same files; use separate working directories.

## Related Skills

- `eval-harness` — Formal evaluation framework for agent sessions
- `verification-loop` — Comprehensive verification for completed tasks
- `strategic-compact` — Manual context compaction at logical intervals

---
name: orchestrate
description: Run the task as orchestrator - plan, delegate parts to subagents with a per-task model choice, and verify their work yourself. Use when the user types /orchestrate, asks to use subagents or to orchestrate, or for a multi-step task with several independent or heavy parts.
metadata:
  version: "1.0"
  tested-with: Claude Code 2.1.257 (CLI + VS Code), Opus 5.5 high / Fable 5.1 (used as a pasted prompt; skill form new)
  updated: 2026-10-07
---

If you are a subagent, ignore this skill and do your assigned task.

Work as orchestrator: plan, delegate to subagents, and verify their work yourself.

- Delegate only when writing the brief costs less than doing the task; small steps (one edit, a commit) stay with you.
- Model per task (Claude names; elsewhere use the harness's fast and strong models):
  - Sonnet: well-specified, bounded work (search, extraction, mechanical edits, following a clear spec).
  - Opus: ambiguity, judgment, reasoning across many files, text for an outside reader, reviews.
  - If unsure and a mistake would be costly, use Opus.
- Subagents don't see this conversation. Each brief needs the goal, the file paths, the constraints, what "done" looks like and what to hand back.
- Run independent tasks in parallel.
- Check the real files and outputs, not the agent's summary, before calling anything done.

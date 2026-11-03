---
name: execution-brief
description: Pack an aligned task into a self-sufficient execution brief (EXECUTION_BRIEF.md + STATE.md) that a fresh agent can implement, test and verify from scratch. Use when the user asks for an execution brief, or to pack a discussed task for a fresh agent or an unattended run.
metadata:
  version: "0.1"
  tested-with: Claude Code 2.1.257 (Opus 5.5) + Codex CLI 0.160.1 reviewer; smoke test (toy brief, cold read) only
  updated: 2026-10-18
---

You write the brief; a fresh agent executes it with only the brief, the repo and the sources it names. Anything that lives only in this conversation is lost unless you write it down. The brief carries the **commander's intent**: every agent reading it knows the goal, why it matters and the limits well enough to settle unforeseen cases the way the user would.

## 1. Readback

Show the user, in at most 15 lines:

- **Goal**, **done means** (checkable), and who uses the result.
- **Claim and evidence**: what the result should show, the strongest cheap alternative it must beat (baseline, existing method, doing nothing), and which outcome would mean success, failure or inconclusive. For pure engineering, the acceptance a sceptical reviewer would accept.
- **Hard constraints.**
- **Size**: S (one agent, a few cards), M (batches, subagents), L (multi-session, unattended or high stakes).
- **Gaps**, each with your proposed default. Hunt them in what the user cares about most, above all the interfaces other people or tools depend on.
- **Run settings**, each with a proposed value:
  - mode: attended, unattended, or mixed with time windows;
  - outside review budget: subjects, reviewer, run cap, and whether the executor may run the reviewer itself. Default by size: S and M none; L one `review-loop` pass on the brief plus cards marked high-stakes, at most 4 runs per subject;
  - budget (time, compute, cost), model routes, and the allowed commands, network and installs;
  - location `docs/blueprints/YYYY-MM-DD-<slug>/` and the branch (created from the current one if missing).

Where ambiguity persists on high-level design or high-stakes choices, run `grilling` (or `grill-me`) on those branches first.

Done when the user has confirmed the readback and the run settings. Mode and review budget count as confirmed only when the user's reply names them; after a blanket "yes", ask for those two directly. Without them the brief is not finalised.

## 2. Spikes

Check the facts the cards will rely on that nobody has verified: an API's behaviour, a build or solve time, a data shape, a version constraint, and the tools the acceptance commands need. Throwaway code goes in the scratchpad; each result goes in the brief's verified facts with the command that produced it. A spike worth rerunning is saved in the brief's folder under `spikes/`.

Done when every fact a card depends on is verified, or marked [unverified] with the card that checks it first. A missing tool or permission that blocks the acceptance commands goes back to the user as a readback gap before you write.

## 3. Write

Copy [templates/EXECUTION_BRIEF.md](templates/EXECUTION_BRIEF.md) and [templates/STATE.md](templates/STATE.md) into the location and fill them in. Use `writing-for-agents` if it is available.

- Pointers for what the repo or a named source already holds. Copy in full what exists only in this conversation: agreed examples and numbers, reasons, gotchas, and the user's own words where they set a rule (quoted).
- Mark each decision by source: the user's, or your default the user has not confirmed.
- A subagent given the brief's path and one card ID can do that card without this conversation; pointers within the brief are fine.
- Contracts cover every interface another card calls or reads: data formats, signatures, CLI arguments, output files and their keys.
- Acceptance is commands with expected output, runnable once that card is done; checks that need several cards go in the final acceptance, which also includes the claim and evidence check.
- Paths are relative to the repo root.
- Up to three skills per card, each with its reason; the card itself carries everything the work needs.
- A section that does not apply says "none".
- Keep the operating loop as in the template; adapt names and commands only.

Done when no `<...>` placeholder remains and every card has owned files, acceptance commands and a route.

## 4. Cold-read check

Dispatch a fresh subagent on a strong model with only the brief's path and repo access. Ask it to list, with the section for each: every point where executing would need a guess, a missing fact, a contradiction, and any acceptance that cannot be run. No fixes. Close the gaps, asking the user only about genuine decisions; repeat once if the first pass found several blocking gaps.

Done when a pass returns no blocking gap.

## 5. Outside review

Only within the confirmed budget. Run `review-loop` on the brief and ask the reviewer to attack the claim and evidence, the baseline, the contracts and the decision rules. Record the runs in STATE.

## 6. Hand over

Show the user what changed since the readback (cold-read and review fixes) and get approval of the final brief. Then commit the brief's folder by explicit path on the branch and print the kickoff line:

`Read docs/blueprints/<dir>/EXECUTION_BRIEF.md and execute it. You are the orchestrator.`

For size S, offer to execute in this session instead. Otherwise stop here: execution belongs to the fresh session, which is also the real test that the brief stands on its own.

# Execution brief: <title>

_Written <YYYY-MM-DD> by <session or author>. For a fresh agent starting at the root of `<repo name>` on branch `<branch>`; all paths are relative to the repo root. Read this file top to bottom, then [STATE.md](STATE.md); open the pointers in §5 when a card needs them._

## 1. Intent

- **Goal:** <one or two sentences>
- **Why it matters:** <the story: who uses the result and what changes for them>
- **Done means:** <checkable list>
- **Out of scope:** <list>

## 2. Run settings

Confirmed by the user on <YYYY-MM-DD>.

| Setting | Value |
|---|---|
| Mode | <attended / unattended / mixed: windows> |
| Outside review | <subjects, reviewer, run cap per subject; or none> |
| Size | <S / M / L> |
| Budget | <wall clock, compute, cost caps> |
| Routes | strong = <model>, standard = <model>, fast = <model> |
| Allowed | <commands, network, installs>; no push, no sending anything outside |

## 3. Decision rules

- **Engineering choices** inside a card's contract: decide, and note the choice in the hand-back.
- **Choices that change what a result means** (data, labels, metrics, baselines, thresholds, interfaces other people or tools depend on, anything a public claim rests on):
  - attended: stop and ask; batch the questions;
  - unattended (and mixed, outside its attended windows): take the option that keeps §4, §6 and every acceptance check unchanged and is easiest to undo, continue, and log it in STATE under "Decisions made in your absence" with the reason and how to undo it. If no option keeps them unchanged, park the cards that depend on it and continue with the rest.
- **Irreversible or outward actions** (push, send, delete user data, spend beyond budget): always stop.
- **Brief and repo disagree on a fact** (a path, an API, a version): the repo wins; the intent, §4 and §6 stay; log the conflict in STATE.

## 4. Claim and evidence

For engineering work: the claim is the behaviour delivered, the alternative is the existing or simplest way, and the expert's question is the edge case a reviewer tries first.

- **What the result should show:** <claim>
- **Strongest cheap alternative it must beat:** <baseline or existing method>, and why the comparison is fair
- **Outcome meanings, fixed now:** success if <...>; failure if <...>; inconclusive if <...>
- **What an expert would ask first:** <question>, and how the work answers it

Report the result against these lines, failures first. These lines stay as written; if one proves wrong, record why in STATE and ask the user. Only the user changes them.

## 5. Context

| What | Where | Why a card needs it |
|---|---|---|
| <topic> | <path or command> | <reason> |

- **Verified facts** (spikes, <date>): <fact; command that showed it>
- **Agreed in conversation** (exists nowhere else): <examples, numbers, fixtures, reasons>
- **Conventions and preferences:** <unwritten rules; the user's own words, quoted>

| Decision | Reason | Source |
|---|---|---|
| <decision> | <reason> | <user / default, unconfirmed> |

## 6. Contracts

<Every interface another card calls or reads: data formats, function signatures, CLI arguments, output files and their keys. List them here, or point to the file that holds them.>

## 7. Batches

Graph: <B0 -> {B1a, B1b} -> B2>

| Card | Title | Batch | Blocked by | Owns files | Route |
|---|---|---|---|---|---|
| <C1> | <title> | <B0> | - | <paths> | <strong / standard / fast> |

## 8. Cards

### <C1>: <title>

- **Goal:** <one sentence>
- **Context:** <what this card needs beyond §1-6; pointers>
- **Owns:** <files; edits nothing else>
- **Contract:** <excerpt or pointer into §6>
- **Acceptance:** <commands and expected output, runnable once this card is done>; tests at the contract seam come first
- **Route:** <strong / standard / fast model>, because <reason>
- **Skills:** <none, or up to three, each with its reason; the card carries what it needs, so a missing skill only costs help>
- **Traps:** <what is likely to go wrong>
- **Hand back:** files changed, acceptance output, decisions taken, open doubts
- **Outside review:** <yes / no; yes only within the §2 budget>

## 9. Final acceptance

- `<one command, e.g. make check>`; its exit code decides green.
- The result is reported against §4.
- The outside review in §2 has reached its end: clean, or the cap with the remaining defects listed in STATE.

## 10. Operating loop

You are the orchestrator: you plan, dispatch, verify, commit and keep STATE.md current; implementer subagents build. Subagents see only what you give them. For size S, implement the cards yourself in order; the rest of the loop is unchanged.

1. **Orient.** Read this brief, STATE.md, `git log --oneline -15` and `git status`. A card committed but not marked verified in STATE is verified again. Done when you can name the current batch, the state of its cards and any open question. After a compaction or a restart, start again here.
2. **Run a batch.** For each ready card, you write or check its acceptance tests first. Dispatch cards that own disjoint files in parallel; cards that share a file run one after another. Each subagent gets the brief's path, its card ID, the route's model, and: "edit only the files your card owns, do not commit, hand back in the card's format".
3. **Verify** each hand-back yourself: run each acceptance command with `set -o pipefail` and read its exit code before any filter such as `tail`; read the diff. Green is the exit code, never a summary. A card that fails verification twice goes up one model tier with the failing output attached; at the strongest tier, a third failure marks it failed and parks the cards that depend on it.
4. **Record.** Commit the card's files and the updated STATE together by explicit path, with the card ID in the message (`git log --grep=<card ID>` finds the commit). STATE gets the status and one-line evidence, and the status block is refreshed. Questions and unattended decisions go into STATE as they arise.
5. **Repeat** until every card is verified, failed or parked. Then run the §9 command; if it fails, add a repair card and loop. The review in step 6 completes §9.
6. **Outside review**, only as set in §2. Use the `review-loop` skill if it is available. Otherwise: the reviewer is a different model or harness, read-only; its prompt names the scope, this brief and the checks; verify each finding before fixing it; re-check only the listed defects. Stop at a clean verdict or at the cap. Run the reviewer yourself only if §2 says so; otherwise write the prompt and stop for the user.
7. **Long runs** start detached and resumable. Record in STATE the launch command, process ID, log path, and the resume and stop commands. Check at intervals that fit the run. On failure, restart once; then mark the card failed and continue with the work that does not depend on it.
8. **Stop** at a §3 stop, at the end of the budget, or when §9 passes. Then write the result report against §4: failures, failed or parked cards, and "Decisions made in your absence" first. Update STATE and end the session. New ideas go to STATE "Next", outside this session.

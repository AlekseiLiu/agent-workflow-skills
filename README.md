# agent-workflow-skills

Four skills for working with coding agents such as Claude Code and Codex: plan a task and delegate its parts to subagents, pack an agreed task so a fresh agent can carry it out alone, refine a rough prompt, and get an outside review from a second model. The skills use the open Agent Skills format (`SKILL.md` with `name` and `description` frontmatter), so any harness with native skills can read them. They are copied unchanged from my own skills collection.

## Skills

| Skill | What it does | When to use it | Needs | Status, tested with |
|---|---|---|---|---|
| [`orchestrate`](skills/orchestrate/SKILL.md) | Plans a task, hands parts to subagents with a model chosen per part, and verifies their work itself | `/orchestrate`, "use subagents", a multi-step task with independent or heavy parts | A harness with subagents | active; Claude Code 2.1.257, Opus 5.5 high / Fable 5.1 (as a pasted prompt) |
| [`execution-brief`](skills/execution-brief/SKILL.md) | After you and the agent agree on a task, packs it into `EXECUTION_BRIEF.md` and `STATE.md` that a fresh agent can execute from scratch | "execution brief", "pack this for a fresh agent", before an unattended run | A harness with subagents; optional: `grilling` / `grill-me`, `writing-for-agents`, `review-loop` | experimental; Claude Code (Opus 5.5): smoke test only |
| [`refine-prompt`](skills/refine-prompt/SKILL.md) | Turns a rough prompt into a clearer one for an agent, keeping its intent, scope and wording | "refine / improve / polish this prompt", before a critical task | Nothing | experimental; v0.1 one manual run (Opus 5.5); rules tightened in 0.2; formal evals pending |
| [`review-loop`](skills/review-loop/SKILL.md) | Has finished work checked by a different model or harness, verifies and fixes the findings, then asks for a recheck of those findings only | "outside / Codex review", before important work is pushed or sent | For automatic mode: Python 3 and a reviewer CLI (see Requirements) | experimental; Claude Code (Opus 5.5) + Codex CLI 0.160.1: automatic mode on 3 documents (7 runs); Claude reviewer smoke-tested |

Status and test notes are as recorded when each skill was last checked. `review-loop` ships a working script, [`scripts/review_loop.py`](skills/review-loop/scripts/review_loop.py), that runs the reviewer read-only, captures its answer and enforces a run cap.

## How they fit together

A typical larger task:

1. Write a rough task prompt and run `refine-prompt` on it.
2. Discuss the task with the agent until you agree, then pack it with `execution-brief`.
3. In a fresh session, run the brief with `orchestrate`: the main agent plans, delegates and checks the results.
4. Before you merge or send the result, check it with `review-loop`.

Each skill also works on its own.

## Install

Claude Code (CLI and VS Code):

```bash
claude plugin marketplace add AlekseiLiu/agent-workflow-skills
claude plugin install agent-workflow-skills@agent-workflow-skills
```

Update with `claude plugin marketplace update agent-workflow-skills`.

Codex:

```bash
codex plugin marketplace add AlekseiLiu/agent-workflow-skills
codex plugin add agent-workflow-skills@agent-workflow-skills
```

Update with `codex plugin marketplace upgrade`.

Other harnesses: point the harness's skills folder at `skills/` (copy or symlink). The repo also carries a `pi` key in `package.json` and a Claude marketplace that Copilot CLI can read; both are untested.

## Requirements

- `review-loop`: automatic mode needs Python 3 (standard library only) and the Codex CLI or Claude Code CLI as the reviewer. It works best when the reviewer is a different model family from the author; it also works within one. In manual mode the skill writes the review prompt and you run the reviewer yourself.
- `execution-brief`: needs a harness that can start subagents (for its cold-read check by a fresh agent). It optionally uses `grilling` or `grill-me` (from mattpocock-skills) to settle open design questions, `writing-for-agents` when writing the brief, and `review-loop` for an outside review of the brief.
- `orchestrate`: needs a harness that can start subagents.
- `refine-prompt`: no requirements.

## Wiki

How each skill works, with a diagram per skill: [wiki](wiki/README.md).

## Licence

MIT, see [LICENSE](LICENSE).

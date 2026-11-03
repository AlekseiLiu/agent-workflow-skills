# agent-workflow-skills wiki

What each skill does and how, in one page per skill with a diagram. For humans: the agent reads `skills/<name>/SKILL.md`, not these pages. Diagrams are [Mermaid](https://mermaid.js.org/), which GitHub renders; locally use a Markdown preview with Mermaid support.

| Skill | What it does | Page |
|---|---|---|
| `review-loop` | Has finished work checked by a different model, takes the findings back, fixes, re-checks | [review-loop.md](review-loop.md) |
| `orchestrate` | Plans a task, hands parts to subagents, verifies their work | [orchestrate.md](orchestrate.md) |
| `execution-brief` | Packs an agreed task into a brief a fresh agent can carry out alone | [execution-brief.md](execution-brief.md) |
| `refine-prompt` | Turns a rough prompt into a clearer one without changing its intent | [refine-prompt.md](refine-prompt.md) |

When a skill changes, update its page in the same commit.

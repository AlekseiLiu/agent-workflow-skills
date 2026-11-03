---
name: refine-prompt
description: Turn the author's raw prompt into a clearer, better-structured agent prompt that keeps the author's intent, scope and voice. Use when the user asks to refine, improve, polish or grammar-check a prompt, or before a critical task where execution quality matters most.
metadata:
  version: "0.2"
  tested-with: v0.1 run once by hand (Claude Code 2.1.257, Opus 5.5) - added a line inside the prompt, 1.54x length; both rules tightened in 0.2
  updated: 2026-10-07
---

Refine the prompt; do not execute it.

1. **Read for intent.** In 2 to 4 lines, state what the author wants the agent to do, the hard constraints, and what done looks like. Note anything ambiguous.
2. **Ask only if blocking.** If an ambiguity would change what the agent does, ask at most 3 questions, each with your recommended answer, and stop. Otherwise take the conservative reading and list it as an assumption.
3. **Refine.**
   Keep:
   - every instruction, decision and constraint the author gave, in the author's own terms;
   - the author's scope: add no requirement, step or quality bar the author did not state. If something seems missing, propose it under Changes; never put it inside the prompt;
   - about the original length: count the words, at most 1.5 times the original, often shorter.
   Improve:
   - grammar, spelling and word choice;
   - order: goal first, then context, constraints, what done looks like, what to hand back;
   - vague references, replaced with the concrete thing the author meant ("the file" becomes its path) when the context makes it certain;
   - fit for an agent, which does not share the author's context: make implicit facts explicit, and say what to verify and what to return only where the author already asked for it;
   - cut filler that changes no behaviour ("be thorough", "do your best") and duplicated lines.
4. **Fidelity check.** Could the author point at anything in the refined prompt and say "I didn't ask for that"? Remove it; if it is worth suggesting, list it under Changes. Recount the words against the 1.5 times cap.
5. **Return**, in this order:
   - **Intent**: the lines from step 1, so the author can check you understood;
   - **Refined prompt**: one paste-ready code block;
   - **Changes**: up to 5 bullets on what changed and why, the assumptions, and anything removed or reinterpreted, named explicitly.

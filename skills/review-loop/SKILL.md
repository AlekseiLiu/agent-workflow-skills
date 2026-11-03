---
name: review-loop
description: Have finished work checked by an independent reviewer (a different model or harness, e.g. Codex when you are Claude) and close the loop - write the review prompt, take the findings back, fix, and request a re-check limited to the defect list. Use when the user asks for an outside, second-opinion or Codex review, or before high-stakes work is pushed or sent.
metadata:
  version: "0.3.2"
  tested-with: Claude Code (Opus 5.5) author + Codex CLI 0.160.1 reviewer, automatic mode on 3 documents (7 runs); Claude reviewer smoke-tested
  updated: 2026-11-03
---

The reviewer is a different model or harness than the author, so its blind spots differ. The reviewer edits nothing and commits nothing; that line goes in every prompt.

## 1. Review prompt

1. **Scope.** List exactly what is under review: a commit range (`git log --oneline A..B`, with the count), files, or a branch. Verify each item exists.
2. **Plan and rules.** Find the plan the work claims to follow (a brief, spec or README) and the rule files on the path to each scoped item (`CLAUDE.md`, `AGENTS.md`). If there is no plan, say "no plan of record" rather than inventing one.
3. **Write the prompt** to the project's review folder if it has one, else `reviews/prompts/review_<subject>_<YYYY-MM-DD>.md`, in this shape:
   - **Context**, 5 sentences at most: what the work was, the plan with its path, decisions already made, what is out of scope, whether anything has been pushed. End with: "Review critically: what is wrong, fragile, over-built or missing."
   - **Orientation**: 4 to 8 links, each with a half-line on why the reviewer needs it.
   - **Scope**: the exact commands or paths; for a range, "use `git show --stat <hash>` per commit, then diff a path only when needed".
   - **Checks**, numbered, each starting with a verb and naming its evidence. Include where they apply: plan conformance as a done / partial / deviates table; rules pasted verbatim with "grep, do not trust"; each gate run and tried to fool once; secrets and private data in added lines; docs consistent with the tree.
   - **Output**: the review file path; a word cap (range 1,000, file 500); verdict line first (clean / clean with notes / defects found); defects ranked by severity, each with file and line or commit and a one-line fix; suggestions in a separate list; what was verified clean; "Do not edit or commit anything."
4. **Hand over.** Show the prompt and its path; the user runs the reviewer. When the user has said you may run it yourself, follow [automatic.md](automatic.md) instead.

## 2. Findings back

Verify each defect yourself before fixing it; reviewers are sometimes wrong. Fix the confirmed ones in one batch. List the rejected ones with a one-line reason.

## 3. Re-check

Write `recheck_<subject>_<date>.md`: the review file, the fix commits, and "check only the listed defects", capped at 300 words, appended to the same review file. Stop when the verdict is clean or only notes remain.

Rules are quoted, never summarised: a paraphrased rule is a second source of truth.

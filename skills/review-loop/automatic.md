# Automatic mode

The user has said you may run the reviewer yourself. `scripts/review_loop.py` runs it, captures the final message and counts runs; you still write every prompt and judge every finding. `python3 scripts/review_loop.py --help` lists the flags.

1. **Cap.** Agree the run cap with the user (default 4 per subject, reviews and rechecks together). At the cap the script refuses to run; hand the remaining defects to the user as a list.
2. **Prompt output line.** The reviewer runs read-only (Codex `-s read-only`; Claude with read tools only), so its final message is the review. End each prompt with: "Write nothing to disk; your final message is captured as `<review file>`."
3. **Run.** `review_loop.py run --subject <id> --prompt <prompt> --out <review file> --cwd <repo root> [--reviewer claude]`. The first run writes the review file; later runs append `## Recheck N`. Long runs go in a background shell job.
4. **Rechecks.** A fresh session is the default: an independent eye. `--resume <session>` continues the reviewer's earlier session: cheaper and suited to a narrow defect list, but anchored to its own first view.
5. **Several subjects.** Run one subject first, apply its lessons (defects that would recur) to all drafts, then run the rest in parallel. Parallel runs need subjects that share no files under review.
6. **Findings.** Verify each one before fixing, as in §2. Stop at a clean verdict, or when only notes and user-dependent items remain, and say which.
7. **Tracking.** `review_loop.py status --state <review folder>` prints runs, verdicts and session ids. If the project keeps a dashboard, add one row per subject: runs/cap, verdict, fixes, open user inputs.
8. **Hand over.** Tell the user where each run can be watched or continued: Codex with `codex resume <session>` (transcripts in `~/.codex/sessions/`), Claude with `claude --resume <session>`.

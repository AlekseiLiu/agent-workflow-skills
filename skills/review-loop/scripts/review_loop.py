#!/usr/bin/env python3
"""Run an outside reviewer (Codex or Claude) read-only, capture its answer, enforce a run cap.

The model writes the prompts and judges the findings; this script only runs, captures, counts.

  review_loop.py run --subject S --prompt P.md --out REVIEW.md [--reviewer codex|claude]
                     [--resume SESSION_ID] [--cap 4] [--cwd DIR] [--dry-run]
                     [--model M] [--effort E] [--config KEY=VALUE]... [--log FILE]
  review_loop.py status [--state FILE]

`run` creates REVIEW.md with the reviewer's final message if the file does not exist, and
appends to it otherwise ("## Recheck N" for later runs); it never overwrites a file. State (runs, session ids, verdicts) lives in a
JSON file next to the review (default: review_loop_state.json in REVIEW.md's folder).
--model, --effort and --config (Codex only, e.g. features.memories=false) are passed to the
reviewer CLI only when given; without them the reviewer's own defaults apply. --log saves the reviewer's raw output (its tool calls), e.g.
to check which files it read.
Standard library only.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

STATE_NAME = "review_loop_state.json"
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def load(path):
    return json.loads(path.read_text()) if path.exists() else {}


def save(path, state):
    path.write_text(json.dumps(state, indent=2) + "\n")


def build_cmd(reviewer, cwd, out_tmp, resume, model=None, effort=None, config=()):
    if reviewer == "codex":
        opts = (["-m", model] if model else []) + (["-c", f'model_reasoning_effort="{effort}"'] if effort else [])
        opts += [x for kv in config for x in ("-c", kv)]
        if resume:  # `exec resume` has no -s/-C; it reuses the session's cwd
            return ["codex", "exec", "resume", "--skip-git-repo-check", *opts, "-c", 'sandbox_mode="read-only"',
                    "-o", out_tmp, resume, "-"]
        return ["codex", "exec", "--skip-git-repo-check", *opts, "-s", "read-only", "-C", cwd, "-o", out_tmp, "-"]
    cmd = ["claude", "-p", "--output-format", "json",
           "--allowedTools", "Read", "Grep", "Glob",
           "--disallowedTools", "Edit", "Write", "NotebookEdit", "Bash"]
    cmd += (["--model", model] if model else []) + (["--effort", effort] if effort else [])
    return cmd + (["--resume", resume] if resume else [])


def run_reviewer(reviewer, prompt_text, cwd, resume, model=None, effort=None, config=()):
    """Return (final message, session id or None, raw log)."""
    with tempfile.TemporaryDirectory() as tmp:
        out_tmp = str(Path(tmp) / "last.md")
        cmd = build_cmd(reviewer, cwd, out_tmp, resume, model, effort, config)
        proc = subprocess.run(cmd, input=prompt_text, capture_output=True, text=True, cwd=cwd)
        log = proc.stdout + proc.stderr
        if proc.returncode != 0:
            sys.exit(f"reviewer exited {proc.returncode}:\n{log[-2000:]}")
        if reviewer == "codex":
            m = re.search(r"session id:\s*(" + UUID + ")", log)
            return Path(out_tmp).read_text(), (m.group(1) if m else resume), log
        data = json.loads(proc.stdout)
        return data.get("result", ""), data.get("session_id", resume), log


def cmd_run(a):
    out = Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    log_path = Path(a.log).resolve() if a.log else None
    if log_path:  # every output folder exists before the reviewer runs
        log_path.parent.mkdir(parents=True, exist_ok=True)
    state_path = Path(a.state).resolve() if a.state else out.parent / STATE_NAME
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state = load(state_path)
    subj = state.setdefault(a.subject, {"review": str(out), "cap": a.cap, "runs": []})
    cap = subj.get("cap", a.cap)
    if len(subj["runs"]) >= cap:
        sys.exit(f"cap reached for {a.subject}: {len(subj['runs'])}/{cap} runs. "
                 "Hand the remaining defects to the user.")
    cwd = str(Path(a.cwd).resolve())
    if a.dry_run:
        print(" ".join(build_cmd(a.reviewer, cwd, "<tmp>/last.md", a.resume, a.model, a.effort, a.config)), "<", a.prompt)
        print(f"run {len(subj['runs']) + 1}/{cap} -> {out}")
        return
    text, session, log = run_reviewer(a.reviewer, Path(a.prompt).read_text(), cwd, a.resume, a.model, a.effort, a.config)
    n = len(subj["runs"])
    today = dt.date.today().isoformat()
    if not out.exists():
        out.write_text(text.rstrip() + "\n")
    else:  # never overwrite: an existing file may hold another subject's or a manual review
        head = f"Recheck {n}" if n else f"{a.subject} run 1"
        with out.open("a") as f:
            f.write(f"\n\n## {head} ({a.reviewer}, {today})\n\n{text.rstrip()}\n")
    verdict = next((l.strip() for l in text.splitlines() if l.strip()), "")[:120]
    subj["runs"].append({"n": n + 1, "date": today, "reviewer": a.reviewer, "prompt": a.prompt,
                         "session": session, "resumed": bool(a.resume), "verdict": verdict})
    save(state_path, state)
    if log_path:  # last, so a log problem never loses the review or the run count
        log_path.write_text(log)
    print(f"{a.subject}: run {n + 1}/{cap}, session {session}\nverdict: {verdict}\nreview: {out}")


def cmd_status(a):
    state_path = Path(a.state)
    if state_path.is_dir():
        state_path = state_path / STATE_NAME
    state = load(state_path)
    print("| Subject | Runs | Last verdict | Last session | Review |\n|---|---|---|---|---|")
    for name, s in state.items():
        last = s["runs"][-1] if s["runs"] else {}
        print(f"| {name} | {len(s['runs'])}/{s.get('cap', '?')} | {last.get('verdict', '-')} "
              f"| {last.get('session', '-')} | {s['review']} |")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run the reviewer once for a subject")
    r.add_argument("--subject", required=True, help="short id, e.g. api_docs_v2")
    r.add_argument("--prompt", required=True, help="review or recheck prompt file")
    r.add_argument("--out", required=True, help="review file (created, then appended)")
    r.add_argument("--reviewer", choices=["codex", "claude"], default="codex")
    r.add_argument("--resume", help="continue this reviewer session instead of a fresh one")
    r.add_argument("--cap", type=int, default=4, help="max runs per subject (default 4)")
    r.add_argument("--cwd", default=".", help="working root the reviewer reads from")
    r.add_argument("--state", help=f"state file (default: {STATE_NAME} next to --out)")
    r.add_argument("--dry-run", action="store_true", help="print the command, run nothing")
    r.add_argument("--model", help="reviewer model id (default: the reviewer CLI's own default)")
    r.add_argument("--effort", help="reasoning effort, e.g. high or xhigh (default: the CLI's own)")
    r.add_argument("--config", action="append", default=[], help="Codex -c KEY=VALUE override; repeat")
    r.add_argument("--log", help="save the reviewer's raw output to this file")
    s = sub.add_parser("status", help="print the run table")
    s.add_argument("--state", default=".", help=f"state file or its folder (default: ./{STATE_NAME})")
    a = p.parse_args()
    cmd_run(a) if a.cmd == "run" else cmd_status(a)


if __name__ == "__main__":
    main()

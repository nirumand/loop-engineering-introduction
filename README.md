# Loop Engineering — Playground

A workspace for learning **loop engineering**: instead of prompting an agent turn-by-turn, you
*design a system* that discovers work, acts on it, checks itself, and loops until a finish line is
reached. See [`kb/loop-engineering.md`](kb/loop-engineering.md) for the concept.

This README is a **human walkthrough**: how to build an example loop using the `design-loop` skill.

---

## What's in here

- `kb/loop-engineering.md` — the concept, distilled.
- `.claude/skills/design-loop/` — a skill that *interviews you* and emits a runnable loop.
- `examples/calc.py` + `examples/test_calc.py` — a tiny demo target. The test file is the **spec**
  (never edited); a loop fixes `calc.py` until the tests pass.

## Prerequisites

- Claude Code, opened in this folder.
- `uv` installed (tests run via `uv run --with pytest pytest -q`).

---

## Walkthrough: build a "keep tests green" loop

We'll design a loop whose job is: *fix `calc.py` until `pytest` passes, on its own.*

### Step 1 — Start the skill

In Claude Code, type a request that triggers the skill:

```
design a loop
```

Claude loads `design-loop` and gives a short plain-language primer, then starts an interview —
**one question at a time**. There are no wrong answers; if unsure, accept the suggested answer.

### Step 2 — Answer the interview

The skill asks ~10 questions. For our example, answer like this:

| # | Question (plain terms) | Your answer for this example |
|---|------------------------|------------------------------|
| 1 | **Stop condition** — how does the loop know it's done? | `uv run --with pytest pytest -q` exits 0 (all tests pass) |
| 2 | **Discovery** — how does it find the next thing to do? | Run the tests; the first `FAILED` line is the next item |
| 3 | **Maker action** — one action that makes progress | Edit `calc.py` so that one failing test passes |
| 4 | **Verification** — who checks, and how to stop cheating | A separate checker sub-agent re-runs tests AND confirms `test_calc.py` was not edited |
| 5 | **Knowledge** — facts to hand it every run | Test cmd is `uv run --with pytest pytest -q`; source in `examples/calc.py`; spec in `examples/test_calc.py` (never touch) |
| 6 | **Memory** — what to write down each run | Log of what was fixed, what failed, current pass/fail count |
| 7 | **Connectors** (optional) | Skip — local files only |
| 8 | **Parallelism** (optional) | Skip — one fix at a time |
| 9 | **Warming-up** (optional) — only watch & report first? | Skip — edits to `calc.py` are local and reversible via git |
| 10 | **Human handoff** — where stuck items go | Append to a `needs-human` section in the state file |

Question 1 is the important one: it must be something a **computer can check** (an exit code, a
file's contents, a count). "Make the code better" is rejected — the loop could never decide it's done.

Question 9 (**warming-up**) we skip here because a wrong edit to `calc.py` is harmless and undoable
with git. For a loop that can delete files, send email, or post to Slack, answer "yes": it then
starts in **summarize-only** (reads and reports, changes nothing), and you widen it to writes once
you trust its judgment — like a new hire who shadows before getting the keys.

### Step 3 — Let the skill emit the scaffold

After the interview, the skill writes two files into this project:

```
fix-tests/SKILL.md     # the worker: one iteration = discover → maker → checker → log → handoff
memory/STATE.md        # persistent memory, seeded STATUS: UNKNOWN / LAST_RUN: never
```

(`fix-tests` is the loop name it picks from your goal — yours may differ.)

### Step 4 — Launch the loop

The skill prints the trigger command. Run it:

```
/goal "uv run --with pytest pytest -q exits 0"
```

`/goal` is the engine: Claude keeps working across turns — read memory, find a failing test, fix
`calc.py` (maker), verify with a separate checker, log to `memory/STATE.md` — and **stops itself**
when the condition holds.

Fallback triggers if `/goal` isn't available, or you want a cadence:

```
/loop run the fix-tests skill until pytest passes
/schedule daily: run the fix-tests skill
```

### Step 5 — Watch it work

Each lap appends an entry to `memory/STATE.md`. When the tests pass, `STATUS` flips to `GREEN` and
the loop halts. Anything it couldn't solve is parked in the handoff section for you.

---

## Try it yourself

Break a function in `examples/calc.py` (e.g. make `add` return `a - b`), then run Step 1. The loop should
discover the failing test, fix `calc.py`, verify, and stop green — without you prompting each step.

## The four rules every loop must keep

1. **Machine-checkable stop condition** — or it never halts.
2. **Maker ≠ checker** — the verifier is a separate sub-agent, so the worker can't grade its own homework.
3. **Memory file** — state survives between runs; the loop doesn't repeat itself.
4. **Human handoff** — stuck items get flagged, not silently dropped.

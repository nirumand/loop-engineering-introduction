# simple-calculator — example loop

A self-contained loop-engineering example. The loop's job: *fix `calc.py` until the tests pass, on
its own.*

This folder is its **own project** — it has its own `.claude/skills/fix-calc/`, so the skill loads
**by name** when Claude Code is opened here.

```
.claude/skills/fix-calc/SKILL.md   the worker: one iteration (discover → maker → checker → log → handoff)
calc.py                            source the loop edits
test_calc.py                       the spec — never edited by the loop
memory/STATE.md                    persistent state between runs
```

## Run it

`divide` in `calc.py` **ships intentionally broken**, so the loop has work the moment you start —
no manual setup.

1. Open Claude Code **in this folder** (`examples/simple-calculator/`) — not the repo root, or the
   nested `.claude/skills/` won't be discovered.
2. Launch the loop with a **thin** trigger — name only, no steps or condition (those live in the
   skill):

   ```
   /goal "run the fix-calc loop"
   ```

`/goal` loads `fix-calc` by name, then follows it across turns — read memory, find a failing test,
fix `calc.py` (maker), verify with a separate checker, log to `memory/STATE.md` — and **stops
itself** when `uv run --with pytest pytest -q` exits 0.

## Why it takes several iterations (for the human)

The loop fixes **one failing test per lap**, and the maker only sees *that* failing test — never
the whole spec. `divide`'s spec is staged so each lap reveals the next problem:

| Lap | First failing test    | Minimal fix the maker makes      | Still broken after |
|-----|-----------------------|----------------------------------|--------------------|
| 1   | `test_divide`         | `return a / b` (right operator)  | truncation, zero   |
| 2   | `test_divide_truncates` | `return a // b` (integer div)  | divide-by-zero     |
| 3   | `test_divide_by_zero` | raise `ValueError` when `b == 0` | — → all green, STOP |

That's the point of the example: a single function needing a multi-lap loop, with memory carrying
progress between laps.

**Reset the demo** after a run: `git checkout calc.py`.

> Do not put these hints in `calc.py` — the maker would read them and skip the iterations. This
> explanation is human-only (and a deny-read rule in `.claude/settings.json` keeps the agent out of
> this file).

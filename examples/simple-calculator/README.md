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

1. Open Claude Code **in this folder** (`examples/simple-calculator/`) — not the repo root, or the
   nested `.claude/skills/` won't be discovered.
2. Break something so the loop has work to do, e.g. make `add` return `a - b` in `calc.py`.
3. Launch the loop with a **thin** trigger — name only, no steps or condition (those live in the
   skill):

   ```
   /goal "run the fix-calc loop"
   ```

`/goal` loads `fix-calc` by name, then follows it across turns — read memory, find a failing test,
fix `calc.py` (maker), verify with a separate checker, log to `memory/STATE.md` — and **stops
itself** when `uv run --with pytest pytest -q` exits 0.

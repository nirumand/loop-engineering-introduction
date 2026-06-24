---
name: fix-calc
description: One iteration of the fix-calc loop — discover failing test, fix calc.py, verify, log. Use when running the fix-calc loop.
---

# fix-calc loop

Run this loop with Claude Code opened in `examples/simple-calculator/` (this folder is the project
root). All paths below are relative to it.

## Knowledge
- Test command: `uv run --with pytest pytest -q`
- Source to edit: `calc.py`
- Spec (read-only, never edit): `test_calc.py`
- Rule: never use bare `python` or `pytest` — always use `uv`

## Procedure (one iteration)

1. **Read state**: open `memory/STATE.md` — see what past runs tried; skip already-fixed items.

2. **Discover**: run `uv run --with pytest pytest -q`. Parse first FAILED test name from output. If exit code is 0 (all pass), write STATUS: DONE to state and STOP.

3. **Make (maker sub-agent)**: dispatch a sub-agent to read the failing test + current `calc.py` and edit `calc.py` to fix that one failing function. Sub-agent must never edit `test_calc.py`.

4. **Check (checker sub-agent)**: dispatch a SEPARATE sub-agent to:
   - Run `uv run --with pytest pytest -q` and confirm the target test now passes.
   - Run `git diff test_calc.py` and confirm output is empty (spec untouched).

5. **Log**: append dated entry to `memory/STATE.md`:
   - Test name fixed (or attempted)
   - What change was made to `calc.py`
   - Current pass count vs total
   - Anything tried that didn't work

6. **Handoff**: if checker fails after maker's attempt, append to `memory/STUCK.md` (test name, what was tried, why it failed) and move on.

## Rules
- One failing test per iteration. Minimal changes.
- Maker ≠ checker (separate sub-agents).
- Stop condition: `uv run --with pytest pytest -q` exits 0.
- Never edit `test_calc.py`.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A learning workspace for **loop engineering** (Addy Osmani's concept: stop hand-prompting an agent
turn-by-turn; instead design a self-running system that discovers work, acts, checks itself, and
loops until a machine-checkable condition holds). It is not a product — it holds a knowledge base,
a reusable skill that designs loops, and a tiny `calc` demo used to exercise a loop end-to-end.

## Commands

- Run tests: `uv run --with pytest pytest -q` (use `uv`, never bare `python`/`pytest` — bare invocation fails here).
- Single test: `uv run --with pytest pytest -q test_calc.py::test_add`.

## Layout and architecture

- `kb/loop-engineering.md` — the source-of-truth notes distilled from the Osmani article: the
  definition, six components (Automations, Skills, Memory, Sub-agents, Worktrees, Connectors), the
  Claude Code primitive mapping, and anti-patterns. Read this first to understand the domain.
- `.claude/skills/design-loop/` — the main deliverable. An **interview-driven skill** that helps a
  user *author* a loop: it runs a beginner-friendly interview (Phase 0 primer → Phase 1 nine
  questions, one at a time, stop-condition first → Phase 2 emits a `<loop-name>/SKILL.md` worker +
  `memory/STATE.md` seed → Phase 3 hands off a `/goal "<condition>"` trigger). Its
  `references/loop-principles.md` mirrors the kb and is cited when explaining recommendations.
- `calc.py` + `test_calc.py` — minimal demo target. `test_calc.py` is the **spec** and must never
  be edited by a maker; loops fix `calc.py` to make it pass.

## Loop design invariants (enforced by the design-loop skill — keep them when editing it)

- Every loop needs a **machine-checkable stop condition** (exit code / file contents / count == 0).
  Reject vague goals ("make it better") — they cause runaway loops.
- **Maker ≠ checker**: the agent that makes a change and the agent that verifies it must be
  separate sub-agents (anti-cheat; e.g. the checker confirms the maker didn't edit the test).
- Always a **memory file** (state survives context reset between runs) and a **human-handoff** path
  for stuck items.
- `/goal "<condition>"` is the loop driver; `/loop` and `/schedule` are fallback triggers.

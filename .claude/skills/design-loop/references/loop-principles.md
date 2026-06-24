# Loop engineering — principles

Based on Addy Osmani, "Loop Engineering" (https://addyosmani.com/blog/loop-engineering/).

## Core idea

> Replace yourself as the person who prompts the agent. Design the system that does it instead.

Instead of prompting an agent turn-by-turn, build an autonomous system that **discovers work,
delegates tasks, evaluates results, and decides the next step** on its own — and loops until a
condition is met.

## Components

1. **Automations** — scheduled/triggered runs that discover and triage work on a cadence, no
   manual kick. In Claude Code: `/goal` (run until condition), `/loop` (interval/self-paced),
   `/schedule` (cron).
2. **Skills** — documented project knowledge (`SKILL.md`) so the agent doesn't re-derive context
   every cycle.
3. **Memory** — external state (markdown file, board) that persists *between* runs, because the
   model's context resets each cycle. Without it the loop repeats work it already did.
4. **Sub-agents** — split the **maker** from the **checker**: a separate agent (different prompt or
   model) verifies the work and catches the maker's blind spots.
5. **Worktrees** — isolated working dirs so multiple agents run in parallel without file conflict
   (`isolation: worktree`).
6. **Connectors (MCP)** — integrations to issue trackers, databases, Slack, staging APIs — so the
   loop can act beyond the filesystem (open PRs, update tickets, post messages).

## Example workflow (Osmani)

A daily automation runs a triage skill over CI failures + open issues, writes findings to memory.
For each actionable item, an isolated worktree spawns a maker to draft the fix and a checker to
review it against standards. Connectors open the PR and update the ticket. Anything unresolved
lands in a triage inbox for a human.

## Governing principle

> Design the loop like someone who intends to stay the engineer, not just the person who presses go.

The loop accelerates work you understand deeply, but can mask comprehension gaps if you abdicate
oversight.

## Anti-patterns (the interview exists to prevent these)

- **No stop condition** → runaway loop, burns tokens, never halts. Demand a machine-checkable goal.
- **Maker == checker** → the agent grades its own homework; blind spots survive.
- **No memory** → every run starts from zero, repeats failed attempts.
- **No human handoff** → stuck units fail silently instead of escalating.
- **Vague goal** ("improve quality") → unmeasurable, so the loop can't decide it's done.

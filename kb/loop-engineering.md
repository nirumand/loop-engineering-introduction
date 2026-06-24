# Loop Engineering — Knowledge Base

Source: Addy Osmani, "Loop Engineering" — https://addyosmani.com/blog/loop-engineering/

## Definition

> Replace yourself as the person who prompts the agent. You design the system that does it instead.

Loop engineering = building an **autonomous system** that discovers work, delegates tasks,
evaluates results, and decides the next step on its own — then repeats until a condition is met.
The shift: you stop hand-prompting the agent turn-by-turn and instead **engineer the loop**.

## The six components

1. **Automations** — Scheduled/triggered tasks that discover and triage work on a regular cadence,
   no manual kick.
2. **Skills** — Documented project knowledge (`SKILL.md` files) so the agent doesn't re-derive
   context from scratch each cycle.
3. **Memory** — External state (markdown files, boards) that persists *between* runs, compensating
   for the model's context reset each cycle.
4. **Sub-agents** — Separate agents (different instructions or models) that verify work — splitting
   the **maker** from the **checker** to catch oversights.
5. **Worktrees** — Isolated working directories letting multiple agents run in parallel without
   file conflicts (git worktrees).
6. **Connectors / Plugins** — Integrations (built on MCP) linking agents to external tools — issue
   trackers, databases, Slack, staging APIs — enabling action beyond the filesystem.

## Example workflow

A daily automation runs a triage skill that analyzes CI failures and open issues, writing findings
to persistent state. For each actionable item, isolated worktrees spawn one sub-agent to draft a
fix and another to review it against project standards. Connectors open PRs and update tickets.
Unresolved work lands in a triage inbox for human review.

## Governing principle

> Design the loop like someone who intends to stay the engineer, not just the person who presses go.

The loop accelerates work you understand deeply — but can mask comprehension gaps if you abdicate
oversight.

## Mapping to Claude Code primitives

| Component   | Claude Code primitive            | Purpose                              |
|-------------|----------------------------------|--------------------------------------|
| Automations | `/goal`, `/loop`, `/schedule`    | trigger/drive the loop               |
| Skills      | `SKILL.md`                       | task knowledge, no re-derive         |
| Memory      | markdown state file              | survive context reset between runs   |
| Sub-agents  | `Agent` tool                     | maker/checker split                  |
| Worktrees   | `isolation: worktree`            | parallel agents, no file clash       |
| Connectors  | MCP servers                      | act on issues/Slack/DB/PRs           |

`/goal "<condition>"` is the iteration engine — keeps working across turns until the condition
holds. `/loop` (interval/self-paced) and `/schedule` (cron) are alternative triggers.

## Anti-patterns

- **No stop condition** → runaway loop, never halts. Require a machine-checkable goal.
- **Maker == checker** → agent grades its own homework; blind spots survive.
- **No memory** → every run starts from zero, repeats failed attempts.
- **No human handoff** → stuck items fail silently instead of escalating.
- **Vague goal** ("improve quality") → unmeasurable, loop can't decide it's done.

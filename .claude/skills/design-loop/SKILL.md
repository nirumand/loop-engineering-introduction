---
name: design-loop
description: Interview the user to design an autonomous agentic loop (loop engineering), then emit a runnable scaffold launched via /goal. Use when the user wants to design a loop, build an agentic loop, engineer a self-running task, automate repetitive agent work, or mentions "loop engineering".
---

# design-loop

Help the user *engineer a loop*: a system that discovers work, acts on it, checks itself, and
repeats until a machine-checkable condition holds — instead of the user hand-prompting the agent
every turn. See `references/loop-principles.md` for the underlying model and anti-patterns; cite
it when explaining a recommendation.

Work in three phases: **Interview → Emit scaffold → Hand off the trigger.**

## Phase 0 — Set the scene (one short message, then start)

Before any question, give the user this primer in your own words (2 short paragraphs, plain
language, no jargon):

> A "loop" here is a small system that does a repetitive job for you on its own. Instead of you
> telling the agent what to do every single time, the loop keeps cycling — find the next thing to
> do, do it, check it worked, write down what happened — and stops itself when the job is finished.
>
> I'll ask you a handful of questions to design your loop. There are no wrong answers — if you're
> unsure, I'll suggest one and you can just say "ok". The most important question is the first one:
> *how does the loop know when it's done?*

Then begin Phase 1.

## Phase 1 — Interview

Assume the user is **new to loop engineering**. Don't fire jargon at them.

For each question below, in this exact order:
1. Give a short **"In plain terms"** gloss (1–2 sentences) explaining what the question really
   means, with a tiny everyday example.
2. Then ask the question.
3. Then offer your **recommended answer** for *their* project — explore the codebase to pre-fill it
   instead of asking when you can.
4. Wait for their reply before the next question. One question per message. Don't batch.

The first question is mandatory; skip the ones marked optional unless an earlier answer makes them
relevant.

---

1. **Stop condition (mandatory, ask first).**
   *In plain terms:* When should the loop switch itself off? It needs a finish line a computer can
   check by itself — not a feeling. Good: "the test command passes", "the to-do count hits 0",
   "the file says DONE". Bad: "when it's good enough" (a computer can't measure that, so the loop
   would run forever).
   *Ask:* "What exact, checkable signal means this loop is finished?"
   Reject vague goals and push for something a script can decide (an exit code, a file's contents,
   a count == 0). This answer becomes the `/goal` argument.

2. **Discovery.**
   *In plain terms:* Each lap of the loop, how does it spot the next thing to work on? Think: what
   command or search reveals "here's the next item". Example: run the tests and the first FAILED
   line is the next item.
   *Ask:* "Each time the loop runs, how does it find the next piece of work to do?"

3. **Maker action.**
   *In plain terms:* The "maker" is the worker that actually changes something. What's the one
   concrete action it takes to handle a single item? Example: edit the source file so one failing
   test passes.
   *Ask:* "What single action moves one item forward?"

4. **Verification.**
   *In plain terms:* The "checker" is a second, independent worker that confirms the maker really
   succeeded — like a reviewer, not the author. Two workers because the maker can fool itself (or
   cheat the test). Example: the checker re-runs the tests AND confirms the maker didn't secretly
   edit the test to make it pass.
   *Ask:* "After the maker acts, how do we confirm it truly worked — and stop it from gaming the
   check?" Steer toward a **separate checker sub-agent** with explicit anti-cheat criteria.

5. **Knowledge.**
   *In plain terms:* The loop forgets everything between runs. What facts about this project must
   you hand it every time so it doesn't have to rediscover them? Example: the exact test command,
   where the source lives, a gotcha to avoid.
   *Ask:* "What project facts must the loop be told up front so it doesn't waste time relearning
   them?"

6. **Memory.**
   *In plain terms:* The loop's memory wipes each run, so it writes notes to a file to read next
   time — otherwise it repeats work it already did. What should those notes record? Example: a log
   of what was fixed, what was tried and failed, and the current pass/fail count.
   *Ask:* "What should the loop write down after each run so the next run isn't starting blind?"

7. **Connectors (optional).**
   *In plain terms:* Does the loop need to touch the outside world — not just files on disk?
   Example: open a pull request, comment on a Jira ticket, post to Slack. These hook up through
   MCP. Skip if the loop only edits local files.
   *Ask:* "Does the loop need to read or write any external system (issues, Slack, PRs)?"

8. **Parallelism (optional).**
   *In plain terms:* Are there many independent items that could be worked on at the same time
   instead of one-by-one? If yes, each parallel worker gets its own private copy of the repo (a
   "worktree") so they don't overwrite each other. Skip if items must go one at a time.
   *Ask:* "Are there many independent items to handle at once, or strictly one at a time?" If many,
   note worktree isolation (`isolation: worktree`).

9. **Human handoff.**
   *In plain terms:* When the loop gets stuck on something it can't solve, where does it leave that
   item for a person? Every loop needs an exit ramp so problems get flagged, not silently dropped.
   Example: write it to a "needs-human" list, or open a labeled issue.
   *Ask:* "When the loop can't finish an item, where should it park it for a human?"

## Phase 2 — Emit scaffold

From the answers, create these files in the user's project (pick a short kebab-case
`<loop-name>` from the goal):

**`<loop-name>/SKILL.md`** — the worker skill, one iteration's procedure. Frontmatter `name` +
`description`; body encodes answers 2–6 and 9 in this shape:

```markdown
---
name: <loop-name>
description: <one iteration of the loop — discover, fix, verify, log>. Use when running the <loop-name> loop.
---

# <loop-name> loop

## Knowledge
<answer 5: commands, conventions, file locations>

## Procedure (one iteration)
1. **Read state**: open `memory/STATE.md` — see what past runs already tried; skip those.
2. **Discover**: <answer 2>. If the stop condition already holds, write it to state and STOP.
3. **Make (maker sub-agent)**: dispatch a sub-agent to <answer 3>. <invariant: never edit the spec/check itself>.
4. **Check (checker sub-agent)**: dispatch a SEPARATE sub-agent to <answer 4> — independent verify + anti-cheat.
5. **Log**: append a dated entry to `memory/STATE.md` (unit, what changed, new counts). Update STATUS.
6. **Handoff**: if stuck/conflicting, record it in <answer 9> for a human and move on.

## Rules
- One unit per iteration. Minimal changes.
- Maker ≠ checker (different sub-agent catches blind spots).
- The stop condition (`<answer 1>`) is the only definition of done.
```

**`memory/STATE.md`** — seed it:

```markdown
# <loop-name> — state

STATUS: UNKNOWN
LAST_RUN: never

## Log

(no runs yet)
```

If connectors (7) or parallelism (8) apply, add the matching step to the worker procedure
(an MCP call for connectors; an `isolation: worktree` note + per-unit fan-out for parallelism).

## Phase 3 — Hand off the trigger

Print the exact launch command and tell the user to run it. `/goal` is the loop driver — it keeps
working across turns until the condition holds:

```
/goal "<answer 1, the machine-checkable condition>"
```

Also give the fallbacks, in case `/goal` is unavailable or a cadence is wanted:

- `/loop run the <loop-name> skill until <answer 1>` — self-paced/interval re-runs.
- `/schedule daily: run the <loop-name> skill; <connector action> on success` — cron cadence.

Then summarize the loop back in one diagram: trigger → read memory → discover → maker → checker →
log → repeat until stop condition → human handoff for the rest.

## Invariants (apply to every loop you design)

- **Always** a machine-checkable stop condition. No condition → don't emit; go back to Q1.
- **Always** maker ≠ checker.
- **Always** a memory file and a human handoff path.
- Keep the user the engineer: the loop should accelerate work they understand, not hide it.

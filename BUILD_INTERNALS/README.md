# How we built 58 numpy stubs in 40 hours with one orchestrator and 58 throwaway agents

On 2026-05-21, [Mark Saroufim mentioned this build in his MLSys keynote](https://x.com/marksaroufim/status/2057252867028005352). This page is the structured map of what actually happened — the orchestrator session, the 58 worker sessions, the 12 waves, the dollar numbers, the two prompts that reshaped the protocol mid-build, the things that went wrong.

> *"learnings, what worked well, what didn't, how to repro, push to hacker news and linkedin"* — Cosmin Negruseri, who suggested writing this up.

## The headline

Between **2026-05-06 23:03** and **2026-05-08 16:16 UTC** — about 41 wall hours with overnight idle gaps — one Claude Code session orchestrated 58 worker sessions to implement 58 papers from Jürgen Schmidhuber's experimental archive (1989–2025). Pure numpy + matplotlib, deterministic, every stub runs in <5 min/seed on a laptop.

| Metric | Value |
|---|---:|
| Worker sessions | 58 |
| Numbered waves | 12 (wave 0 sanity + waves 1–10 v1 + wave 11 v1.5) |
| PRs merged | 13 (one per wave) + 1 meta + 1 token-math fix = 15 |
| Total estimated cost | **$3,879** at Opus 4.x public pricing |
| Total tokens | 1.13 billion (94% cache_read) |
| User prompts ("hops") | 353 total, **192 to the orchestrator alone** |
| Assistant turns | 7,265 total |
| Autonomy ratio (turns per hop) | **20.6 : 1** |
| Subagent dispatches (Agent tool calls) | 73 from the orchestrator |
| Inter-team messages (SendMessage) | 69 from the orchestrator |
| Bash invocations | 190 |

The catalog is at **[cybertronai.github.io/schmidhuber-problems](https://cybertronai.github.io/schmidhuber-problems/)**. The repo is **[github.com/cybertronai/schmidhuber-problems](https://github.com/cybertronai/schmidhuber-problems)**.

## How to read this site

This Build internals section is the receipt — the actual data, not a writeup of it. Five entry points depending on what you want:

| If you want… | Start here |
|---|---|
| The narrative arc of the build | This page, then [Pivot moments](pivot-moments.md) |
| Specifically what worked and what didn't | [What worked, what didn't](what-worked-didnt.md) |
| To run a similar build yourself | [How to reproduce](how-to-reproduce.md) |
| The research finding about manual nudges | [Human-in-the-loop as local-minima escape](human-in-the-loop.md) |
| The 1-orchestrator-to-58-workers mapping | [Orchestration map](orchestration-map.md) |
| Per-session numbers (cost, tokens, hops, turns) | [Sessions](sessions.md) |
| Where the money went | [Cost rollup](cost-rollup.md) |
| The worker prompt template, annotated | [Worker prompt anatomy](worker-prompt-anatomy.md) |
| Drill into a specific wave | [Per-wave details](waves/README.md) |
| What's still open | [Next phase](next-phase.md) |

## What's load-bearing

Six properties carried the build. Each is documented with its discovery moment and the data in [What worked, what didn't](what-worked-didnt.md).

1. **One SPEC issue as the contract** — [issue #1](https://github.com/cybertronai/schmidhuber-problems/issues/1). Every worker prompt links to it.
2. **Pure numpy + matplotlib** as the forcing constraint. No torch shortcuts. The constraint did most of the algorithmic-faithfulness work.
3. **One persistent team** (`TeamCreate × 1`), 58 throwaway teammates. Worker prompts inherit the team description; per-worker prompts stay short.
4. **LOCAL-ONLY per-stub branches**, one PR per wave (not per stub). After wave 1 we deleted 72 spam branches; from wave 2 on, no branches were pushed.
5. **`Explore` audit subagent per wave**, read-only, before opening the PR. Cheap; catches inconsistencies (orphan files, format drift) that humans would miss in review.
6. **Batch-merge at the end** as the human approval gate. All 13 PRs merged in a 90-second burst on 2026-05-08 15:49–15:50 UTC.

## What broke

Six things went wrong during the build. Each is fixable; each is documented in [What worked, what didn't](what-worked-didnt.md) with the timestamp it was caught and the change that landed.

1. Branch-per-stub got pushed to origin on wave 1 — branch spam. PR #2 closed and reissued as PR #5; protocol switched to LOCAL ONLY.
2. Workers committed locally and went silent. The orchestrator had to nudge with explicit `Request summary message` SendMessages. Three workers in waves 3, 10, 11 triggered this.
3. Wave 6 and 7 left orphan `problem.py` stub files. Caught by the audit agent; lead added a cleanup commit on top of each wave merge.
4. One commit was authored as `agent-pomdp-flag-maze-builder <agent@anthropic.com>` — the per-worktree git config was overridden by Claude Code's session default. Resolved post-merge with a `git filter-branch` rewrite (74 commits → Yad Konrad).
5. GitHub Pages deploy failed first try. One API call (`gh api -X POST repos/.../pages -F build_type='workflow'`) and a workflow rerun fixed it.
6. The first BUILD_NOTES was written from memory and had fabricated counts. PR #20 reissued it from the actual JSONL session log.

## The Yad-on-loop pattern

The build worked on a rhythm that's worth naming. Yad's own self-summary from 2026-05-08T16:44:

> *"we did it again, 780k token, took a little longer, since only paid attention every 18 hour window while i have other things going on"*

192 user prompts over 41 wall hours = one prompt every ~13 minutes when active, but with two overnight gaps of ~10+ hours each. The autonomous loop had to survive these gaps. It mostly did.

Of those 192 prompts, **roughly 8 were direction-changing** (the "Type A" hops in [Human-in-the-loop](human-in-the-loop.md)). The other ~184 were status checks, tool-result routing, and small clarifications. The build was carried by a handful of 1-sentence interventions:

> *"why are u doing a branch per impl, should it be per waves?? why the branch spam. THIS IS WRONG PRACTICE COURSE CORRECT!"* — 2026-05-07 01:31 UTC

> *"I need you to not rely on me anymore until you finish it all, basically, do wave into 1 per, audit, post to pr then trigger next wave"* — 2026-05-07 02:11 UTC

> *"have we verified thse things to be truely done or left over?"* — 2026-05-08 15:42 UTC

Cosmin Negruseri put a name on this pattern weeks before the build:

> *"I have the feeling I was useful by pinging some wave of agents to do diagnostics and that got the solution out of a local minima."* — 2026-05-14

Sung Jae Bae sharpened it the morning after the MLSys keynote:

> *"Seems to enter the local minima fairly quickly so adding some skills to creatively explore different directions."* — 2026-05-21

A long-running autonomous agent loop builds internal consistency fast and protects it. Outside perspective is the rare commodity. See [Human-in-the-loop](human-in-the-loop.md) for the data-backed version of this claim.

## The cost story

| Pool | Tokens | $ share |
|---|---:|---:|
| `cache_read` | 1,064 M | 41% |
| `cache_write_1h` | 47 M | **36%** |
| `output` | 11 M | 21% |
| `input` | 0.2 M | 0.1% |
| `cache_write_5m` | 4 M | 2% |

`cache_write_1h` was **36% of the bill despite being 4% of the tokens.** Every cache invalidation cost $30/M to re-cache. Output, the conventional cost driver, was third. This is a real surprise — if you're optimizing a long-running orchestration session, watch the 1h cache writes before you worry about output volume. See [Cost rollup](cost-rollup.md) for the per-pool and per-wave breakdown.

Per stub: median **$41**, range **$21–$122**. The outlier was `pipe-6-bit-parity` — it hit a tricky LSTM training issue and needed extra turns.

## How this catalog will be used

The deliverable isn't the 58 stubs. The stubs are easy. The deliverable is **a reusable agent-orchestration recipe**:

- A SPEC issue is enough contract for 58 parallel implementers.
- LOCAL-ONLY worktrees + one-PR-per-wave eliminates branch spam.
- A per-wave audit subagent costs ~3-8% overhead and catches what humans miss in review.
- Pure-numpy as a forcing constraint surfaces honest non-replications instead of hiding them.
- One human attention window every ~18 hours is sufficient if the autonomous loop is well-specified.

[How to reproduce](how-to-reproduce.md) is the recipe in 8 steps. The first run was hinton-problems (53 stubs, week before, same machinery). This was the second run. The recipe survives both.

## What's still open

- **v2: ByteDMD instrumentation.** Re-measure every stub under data-movement complexity. Tracking issue: [#17](https://github.com/cybertronai/schmidhuber-problems/issues/17).
- **v1.5 follow-ups.** Paper-scale reruns + original-simulator follow-ups for the heavyweight-env stubs. Tracking issue: [#18](https://github.com/cybertronai/schmidhuber-problems/issues/18).
- **One honest non-replication** — `hq-learning-pomdp`. The paper's HQ-vs-flat headline does not reproduce on the 29-cell maze. Implementation faithful; queued for v1.5 with the 62-cell maze.
- **Trace export + language scrub + autonomy classification.** Detailed roadmap at [Next phase](next-phase.md).

## Credits and lineage

- **Yad Konrad** (`0bserver07`) — the orchestrator-driver of this build. The 192 prompts in `analysis/data/sessions.jsonl` are his.
- **Yaroslav Bulatov** — proposed implementing Schmidhuber's experimental archive at the start of this build; the SPEC's algorithmic-faithfulness rule is his framing.
- **Cosmin Negruseri** — the local-minima-escape observation; the writeup ask.
- **Mark Saroufim** — referenced this work in his 2026-05-21 MLSys keynote, which prompted Cosmin's "you should write this up" message.
- **Hinton-problems builders** (2026-05-01 → 2026-05-03) — first run of the same recipe. Stubs at [cybertronai/hinton-problems](https://github.com/cybertronai/hinton-problems).

## See also

- [BUILD_NOTES.md](https://github.com/cybertronai/schmidhuber-problems/blob/main/BUILD_NOTES.md) — the session report; this map is the structured drill-down.
- [SutroYaro](https://github.com/cybertronai/SutroYaro) — the dispatcher repo; the orchestrator session lived there.
- [Hinton-problems](https://github.com/cybertronai/hinton-problems) — the precedent build (53 stubs, same recipe).

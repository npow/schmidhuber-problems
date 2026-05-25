# FAQ — the questions everyone asks

The five questions that come up every time this build gets shown. Every number below is verified against `analysis/data/sessions.jsonl` (the orchestrator's JSONL transcript) — the same source the rest of these pages draw from.

## "Wow Claude can one-shot go for 30 hours on Schmidhuber?"

Not literally one-shot. **41 hours** of wall-clock from session start to the final wave merge, but **only ~21 hours of active human attention** — Yad slept through two overnight gaps of ~10 hours each. The orchestrator was idle during those gaps.

In that span, Yad typed **40 prompts** to the lead session. Of those:

- **8 were direction-changing** (~20%)
- ~10 were status checks (`"status?"`, `"what's up man, where the progress"`)
- ~5 were approval gates
- ~17 were small clarifications, copy-edits, and follow-up after the build wrapped

The lead emitted **1,026 assistant turns** in response — **~25.7 turns per Yad prompt** in the orchestrator. Combined with the 58 worker sessions, **7,265 total turns** across the build.

Yad's own self-summary, verbatim from his Telegram post the day it shipped:

> *"we did it again, 780k token, took a little longer, since only paid attention every 18 hour window while i have other things going on"*

The "18-hour window" framing is consistent with the data — he pinged in, the loop ran, he came back the next day.

## "How hard was it to get working?"

Second time running the recipe. **[Hinton-problems](https://github.com/cybertronai/hinton-problems)** (53 stubs, same machinery) ran the week before in ~30 wall hours. Schmidhuber refined the protocol.

**Six things broke during this run, with the timestamp each was caught:**

1. **Branch spam (wave 1).** Workers were pushing `impl/<stub>` branches to origin. 6 workers × 12 waves would have polluted the remote with 72 branches. Caught at **2026-05-07 01:31 UTC** by Yad's prompt:

   > *"why are u doing a branch per impl, should it be per waves?? why the branch spam. THIS IS WRONG PRACTICE COURSE CORRECT!"*

   Fix landed in 7 minutes — PR #2 closed, reissued as PR #5 on `wave/0-sanity`. From wave 2 onward, all stub branches stayed LOCAL ONLY (`wave-N-local/<stub>`).

2. **Workers committed locally and went silent.** Three workers (waves 3, 10, 11) idled after committing without sending a summary. The lead had to nudge each with an explicit *"Request summary message"* SendMessage. The worker prompt template was updated for later waves.

3. **Orphan stub files (waves 6, 7).** Workers wrote new files but didn't `git rm` the placeholder `problem.py`. Caught by the per-wave audit subagent. Cleanup commits added on top of each wave merge.

4. **Wrong git author identity.** One wave-3 commit was authored as `agent-pomdp-flag-maze-builder <agent@anthropic.com>` — the per-worktree git config was overridden by Claude Code's session-default identity. Resolved post-merge with a `git filter-branch` rewrite — 74 commits → `Yad Konrad`. Force-pushed main.

5. **GitHub Pages deploy failed first try.** One API call to enable Pages with `build_type='workflow'`, workflow re-ran, succeeded.

6. **First BUILD_NOTES had fabricated counts** — written from memory. PR #20 rewrote it from the actual JSONL session log.

Full table with discovery moments + fixes: [What worked, what didn't](what-worked-didnt.md).

## "How did you get it to continue for 30 hours without stopping?"

**Three things did the load-bearing work:**

1. **One pivotal Yad prompt at hop 12** (2026-05-07 02:11 UTC) unlocked autonomous mode:

   > *"I need you to not rely on me anymore until you finish it all, basically, do wave into 1 per, audit, post to pr then trigger next wave"*

   Eight subsequent waves (3 through 10) ran without further direction.

2. **A self-sustaining per-wave protocol**: dispatch N parallel workers → wait for summaries → fire one `Explore` audit subagent → open the wave PR → `SendMessage(shutdown_request)` to all workers → move to next wave. The audit step is read-only, catches inconsistencies before review, and ends each wave cleanly.

   **15 `Explore` dispatches total**: 1 initial repo survey + 12 per-wave audits + 2 final BUILD_NOTES extracts.

3. **One persistent team** (`TeamCreate × 1`) reused across all 12 waves. Workers torn down at wave-end via `SendMessage(shutdown_request)` (69 SendMessages from the orchestrator total). The orchestrator survived the two ~10-hour overnight gaps without drift.

Full recipe in 8 steps: [How to reproduce](how-to-reproduce.md).

## "How many tokens did it take?"

**1.13 billion tokens total. $3,879 at Opus 4.x public pricing.**

| | Tokens | Cost share |
|---|---:|---:|
| Orchestrator session alone | **488 M** | $1,284 (33%) |
| **58 worker sessions combined** | **638 M** | $2,595 (67%) |
| **Grand total** | **1,126 M** | **$3,879** (100%) |

**Workers cost more than the orchestrator** — 67% of the bill vs 33%. (Tokens split 57/43 — workers spent proportionally more on `cache_write_1h`, which is the expensive pool.)

### The "780k" footnote

The "**780k**" figure floating around early was not total tokens. That was the orchestrator's **context-window utilization meter** that Yad read off the Claude Code TUI in the moment — visible in screenshots Yad pasted at the time:

```
SutroYaro | Opus 4.7 (1M context) | ███████████████ 678k/1M (68%)
```

It was the lead session's current context fill, not cumulative spend, and it didn't include any of the 58 worker sessions. PR #20 (`docs/token-math-correction`) corrected this in the public BUILD_NOTES the same day.

### Token mix (where the money went)

| Pool | Tokens | $/M | $ share of bill |
|---|---:|---:|---:|
| `cache_read` | 1,064 M (94.5%) | $1.50 | **41.2%** |
| `cache_write_1h` | 47 M (4.2%) | $30.00 | **36.3%** |
| `output` | 11 M (0.9%) | $75.00 | 20.5% |
| `cache_write_5m` | 4 M | $18.75 | 2% |
| `input` | 0.2 M | $15.00 | 0.1% |

Per-pool + per-wave breakdown: [Cost rollup](cost-rollup.md).

## "Is it possible to use less tokens?"

Yes. Four concrete levers, in order of likely impact:

1. **`cache_write_1h` is 36% of the bill on 4% of the tokens.** Every cache invalidation costs $30/M (twice the $15/M raw input rate). Tighter tool-list discipline (don't reload tools mid-session, don't churn the system prompt) would cut this directly. **This is the biggest lever, and the least obvious.**

2. **Per-wave audit is a separate dispatch.** ~3-8% overhead per wave × 12 waves. Moving the audit into the worker prompt (worker self-audits before sending summary) would save one dispatch per wave.

3. **Waves with no family overlap could run in parallel.** Wave 5 (predictability) + wave 8 (evolutionary) share no code. They ran serially. Running them in parallel doesn't cut tokens directly but cuts wall-clock ~30% and reduces overnight idle gaps where the autonomous loop has nothing to do.

4. **Worker prompt boilerplate is ~50 lines repeated per dispatch.** The team description already does the heavy lifting; some of those lines could live there once instead of 58 times.

The single biggest gain is **#1**. `cache_write_1h` is invisible in most token-accounting tools because they show input/output but not cache-write-by-pool. It's the silent driver.

---

*Every number on this page is verified against `analysis/data/sessions.jsonl`. The two corrections in this build's writeup history — the "780k" → 1.13B clarification (PR #20) and the "192 prompts" → 40 clarification (PR #22) — are documented to be transparent about how the analysis was refined.*

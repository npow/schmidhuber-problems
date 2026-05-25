# What worked, what didn't

Binary-classified observations. Each row has the **moment of discovery** (timestamp from the orchestrator's session log) and the **fix that landed**. Drawn from the actual 192 user prompts + 73 Agent dispatches + 69 SendMessages in session `63285119-154e-42ab-9555-7a42471b0309`.

> See [Sessions](sessions.md) and [Orchestration map](orchestration-map.md) for the data behind each row.

## What worked

| Pattern | Why it worked | When it stuck |
|---|---|---|
| **One persistent team (`schmidhuber-impl`), ephemeral teammates** | `TeamCreate` once at 23:23 UTC, then 73 Agent dispatches inherited the team description. Per-worker prompts stayed short because the team contract did the heavy lifting. | Wave 0 onward. The team persisted across all 12 waves; only teammates turned over. |
| **One SPEC issue as the source of truth** | Every worker prompt links to [issue #1](https://github.com/cybertronai/schmidhuber-problems/issues/1) and reads it first. No SPEC drift across 58 workers. | Wave 0. Yad opened the SPEC at 23:20 UTC, **before** the first teammate dispatch. |
| **LOCAL-ONLY per-stub branches + one wave PR** | Workers commit to `wave-N-local/<stub>` and never push. The orchestrator collects branches and opens one PR per wave. Stopped the per-stub branch spam. | After Yad's "THIS IS WRONG PRACTICE COURSE CORRECT!" pushback at 2026-05-07T01:31 UTC. PR #2 was closed and reissued as PR #5 on `wave/0-sanity`. |
| **One `Explore` audit subagent per wave, before opening the PR** | Read-only pass catches inconsistencies (e.g. orphan `problem.py` files) before review. Cheap because Explore doesn't edit. | Started wave 0 with "Audit wave 0 PR #2". Held through all 12 waves. |
| **`SendMessage(shutdown_request)` to free worker context** | Each wave's workers got a shutdown after their PR landed, so the orchestrator's context wasn't bloated by stale teammate transcripts. | Every wave-end SendMessage. 69 total. |
| **Pure-numpy + matplotlib constraint** | Forced workers to demonstrate algorithmic faithfulness (no `torch`/`gym` shortcuts). All 58 stubs ran <5 min/seed on a laptop. | Codified in SPEC #1 before wave 0. Enforced by per-worker prompt and verified in audits. |
| **Honest non-replication acknowledged in audit** | `hq-learning-pomdp` failed to reproduce the paper's HQ-vs-flat gap. The wave-3 audit at 03:35 UTC documented it with the `γ^Δt · HV ≤ R_goal` analysis instead of fudging the result. | One incident. Reproduced in `BUILD_NOTES.md` ➜ Honest non-replication. |
| **Yad's "I need you to not rely on me anymore" hop at wave-3 entry** | Switched from per-wave-approval to fully autonomous wave→audit→PR→next-wave loop. Eight subsequent waves ran without further user intervention. | 2026-05-07T02:11:39 UTC. Verified by the 8+ hour gap from wave 3 launch to the next user prompt. |
| **Algorithmic faithfulness rule (per family)** | Wave-6 LSTM stubs all use a hand-rolled LSTM cell + BPTT; wave-8 evolutionary stubs all evolve weights; Levin/OOPS stubs keep universal search. No shortcut substitutions. | Codified in SPEC #1 before wave 0. Surface symptom: `linear-transformers-fwp` proves the 1992-FWP ≡ 2021-linear-attention equivalence to **2.22e-16** — couldn't have happened with a shortcut substitution. |
| **mdBook + GitHub Pages for the catalog** | Single source for stub READMEs renders as a navigable site. Per-stub GIF assets + viz directories ship together. | After meta PR #16 at 15:50 UTC. Site live at `cybertronai.github.io/schmidhuber-problems/`. |

## What didn't (and the fix)

| Pattern | Discovery | Fix |
|---|---|---|
| **Per-stub remote branches (`impl/<slug>`)** were branch spam | 2026-05-07T01:31:11 UTC — Yad: *"why are u doing a branch per impl, should it be per waves?? why the branch spam. THIS IS WRONG PRACTICE COURSE CORRECT!"* | Wave 2+ switched to `wave-N-local/<stub>` LOCAL ONLY. PR #2 closed, reissued as PR #5 on `wave/0-sanity`. All `impl/<slug>` remote branches deleted. |
| **Workers committed locally then went silent** without sending a summary | Wave 3 (multiple workers): the orchestrator detected idle after-commit and had to nudge | Lead's first SendMessage to silent workers was *"Looks like you committed locally and went idle without sending a summary. Per the wave-3 protocol, please send your summary now."* Pattern repeated at least 4 times across waves 3, 10, 11. Worker prompt template was updated for later waves: *"DO NOT GO SILENT — send a summary explicitly."* |
| **Wave 6 + wave 7 left orphan `problem.py` stub files** | Caught by the per-wave audit agent. Workers wrote the new implementation files but didn't `git rm` the placeholder | Lead added a cleanup commit on top of each wave merge. After wave 7, SPEC was updated to emphasize *"Remove `problem.py` explicitly"* in every dispatch prompt. No further orphans. |
| **One commit in wave 3 was authored as `agent-pomdp-flag-maze-builder <agent@anthropic.com>`** | Wave-3 audit at 03:35 UTC flagged it as non-blocking. The per-worktree git config was overridden by Claude Code's session-default identity | Resolved by a bulk `git filter-branch` rewrite at 2026-05-08T16:12 UTC — 74 agent-authored commits → `Yad Konrad <yad.konrad@gmail.com>`. Force-pushed main. Memory now has [feedback_git_author.md](https://github.com/cybertronai/SutroYaro/blob/main/memory/feedback_git_author.md) so this is checked before every commit. |
| **GitHub Pages deploy failed first try** | 2026-05-08T15:50:41 UTC — *"Ensure GitHub Pages has been enabled"* | One API call: `gh api -X POST repos/cybertronai/schmidhuber-problems/pages -F build_type='workflow'`. Workflow re-run succeeded at 15:53. |
| **Token math in BUILD_NOTES was first written from memory** | Discovered post-merge that the original prose had fabricated counts | Reissued PR #20 `docs/token-math-correction (closes #19)` — rewrote BUILD_NOTES from the actual JSONL session log. Lesson: prose from memory is unreliable when the source data is right there. |
| **Long single pages get dense and hard to navigate** | Yad on 2026-05-23: *"i feel like the analysis should be better separated, in the sidebar at least"* | Sidebar regrouped into 4 sections (Build internals / The orchestration / The worker template / Roadmap). `worker-prompt-anatomy.md` got an "On this page" TOC and a `<details>` wrapper around the verbose full-prompt block. |

## Open

| Pattern | Why open |
|---|---|
| **Was every audit worth its cost?** | 12 audit dispatches added ~3-8% overhead each. Wave 0 (1 stub) almost certainly didn't need one. |
| **Could waves with no family overlap run in parallel?** | Waves 5 (predictability) and 8 (evolutionary) share no code. They ran serially, costing ~6 wall-hours total; could have been ~3. |
| **Worker self-audit instead of separate Explore?** | If each worker wrote its own audit notes before sending the summary, the per-wave Explore dispatch could be merged in. Saves one dispatch per wave (12 total). |
| **`cache_write_1h` was 36% of total cost.** | Each long-running cache invalidation cost real money. Open question whether tighter tool-list discipline (don't reload tools mid-session) would cut this. |

## How to read this with the data

Every row above can be cross-checked:

- Timestamps: grep the `timestamp` field in `../analysis/data/sessions.jsonl` for the orchestrator session.
- Worker silence incidents: filter `../analysis/data/team_messages.tsv` for `Request summary message` in the `head` column.
- Audit dispatches: filter `../analysis/data/agent_dispatches.tsv` for `subagent_type=Explore`.
- Yad's quotes: see [Pivot moments](pivot-moments.md) for the full verbatim list with timestamps.

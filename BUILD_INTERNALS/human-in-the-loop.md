# Human-in-the-loop as local-minima escape

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

> "I have the feeling I was useful by pinging some wave of agents to do diagnostics and that got the solution out of a local minima."
> — Cosmin Negruseri, 2026-05-14

> "Seems to enter the local minima fairly quickly so adding some skills to creatively explore different directions."
> — Sung Jae Bae, 2026-05-21

A claim worth taking seriously: **a long-running autonomous agent loop will hit local minima fast, and a sparse human ping is enough to escape.** This page tests that claim against the **40 Yad-typed prompts** logged in the schmidhuber-problems orchestrator session.

> **Important framing.** The orchestrator's JSONL contains 192 records of `type=user`, but only **40 are prompts Yad actually typed**. The other 152 are worker sessions reporting back to the orchestrator (their idle/summary messages route through `SendMessage` and surface in the lead's transcript as `type=user` records), plus 6 slash commands, 2 skill-loader outputs, and 2 redacted entries. **Every number below uses the 40-prompt count.**

## The numbers

- **Yad-typed prompts to the orchestrator:** 40
- **Orchestrator assistant turns:** 1,026
- **Turns per Yad prompt (orchestrator):** 1,026 / 40 ≈ **25.7**
- **Active wall-clock:** ~21 hours of attention spread across 41 hours (two ~10-hour overnight idle gaps)

If every Yad prompt was load-bearing, this would be a high human-attention build. It wasn't. Most were 1-line nudges. A small minority did the load-bearing work.

## Three classes of hop

Classified manually from the orchestrator's full hop list. (Worker-side hops are mostly templated `<teammate-message>` envelopes — see [Worker prompt anatomy](worker-prompt-anatomy.md).)

### Type A — direction-changing (rare, high-leverage)

These reshape the build. The autonomous loop wouldn't have found these on its own.

| Timestamp (UTC) | Yad's prompt | What changed |
|---|---|---|
| 2026-05-06T23:08 | *Pasted the SPEC link, the hinton-problems precedent, and Yaroslav's Schmidhuber-papers suggestion. Set the goal.* | Triggered the entire build — TeamCreate + wave 0 dispatch within 16 min. |
| 2026-05-07T00:11 | *"alright shall we do clean up and dispathc multiple agents to finish the rest of the waves?"* | Wave-1 trigger. Started the parallel-dispatch protocol. |
| **2026-05-07T01:31** | ***"why are u doing a branch per impl, should it be per waves?? why the branch spam. THIS IS WRONG PRACTICE COURSE CORRECT!"*** | **Wave 1 → wave 2 protocol pivot.** PR #2 closed, reissued as PR #5 on `wave/0-sanity`. All per-stub remote branches deleted. From wave 2 onward, per-stub branches stay LOCAL ONLY. |
| **2026-05-07T02:11** | ***"I need you to not rely on me anymore until you finish it all, basically, do wave into 1 per, audit, post to pr then trigger next wave"*** | **Autonomous-mode engaged.** Eight subsequent waves ran without further user intervention. Lead ran the audit→merge→dispatch loop end-to-end. |
| 2026-05-08T13:55 | *"BUT FIRST FIRST FINISH THESE THINGS REMAINING"* | Wave 11 (v1.5) trigger. Prioritized closing v1+v1.5 before site/docs. |
| 2026-05-08T15:21 | *"why are there teams reaminign thouhg?"* | Caught the not-yet-shutdown teammate processes. Triggered the team cleanup. |
| 2026-05-08T15:42 | *"i still see the agents man / where and why the site link is not in the gihub repo / have we verified thse things to be truely done or left over?"* | Surfaced the unmerged-PRs gap. Explicit merge instruction followed. The batch-merge of all 13 PRs happened minutes after this. |
| 2026-05-08T16:09 | *Redacted (frustrated venting about agent identity)* | Triggered the git filter-branch rewrite (74 commits → Yad Konrad). |

**Count: 8 Type-A hops out of 40 Yad-typed prompts = 20%.** One in five prompts Yad sent reshaped the protocol.

### Type B — status checks (frequent, low-cost)

Brief check-ins. Pattern: orchestrator summarizes per-wave progress and continues.

| Pattern | Approximate count |
|---|---:|
| `status` / `status?` / `status, what is left?` / `whats left rl?` | ~10 |

These cost ~25 turns of orchestrator output each (the summary), but didn't change the protocol. They were Yad confirming the autonomous loop was still on track.

### Type C — review-and-merge gate

Explicit approval moments. Few but load-bearing.

| Timestamp (UTC) | Hop | Effect |
|---|---|---|
| 2026-05-07T00:15 | *"review it/audit and post the comment, then dispatch after please"* | Locked in the audit-then-dispatch loop. |
| 2026-05-08T13:55 | *"lets please finish everything and deal with the full impelmentations / remember what Yaroslav asked for? when we finish we need to draw the full pictres as well / BUT FIRST FIRST FINISH"* | Wave 11 + downstream artifacts (BUILD_NOTES, site). |
| 2026-05-08T19:37 | *"fix merge both PRs?"* | Final merge approval for the meta + docs PRs. |
| 2026-05-08T16:52 | *"udpate the github issues"* | Closed-out and reorganized the v2 ByteDMD + v1.5 follow-up issues. |

The actual batch-merge of 13 PRs happened automatically after the autonomous loop completed; Yad's role was only to approve. ~5 Type-C hops total.

### Where the other 152 `type=user` records came from

Of the 192 `type=user` records in the orchestrator's JSONL transcript:

- **142 were workers reporting back to the orchestrator** — each `SendMessage` from a worker to `team-lead` surfaces in the lead's transcript as a `type=user` record with a `<teammate-message teammate_id="<worker>">` envelope.
- **6 were slash commands** (`/login`, etc.)
- **2 were skill-loader outputs** (`sutro-sync` skill invocations)
- **2 were redacted** (one foul-language frustrated venting, one image attachment path leak)

Yad's actual hand-typed prompts are the **40** classified below.

## The local-minima-escape claim, tested

**Claim** (Cosmin's): a manual ping helps the agent loop escape local minima it would otherwise stay stuck in.

The two strongest examples:

### Example 1 — branch-per-stub local minimum

By wave 1, the lead had settled on `impl/<slug>` branches pushed to origin. Pattern: 6 workers per wave × 12 waves = 72 remote branches. This was branch spam in a way the lead didn't recognize. It wasn't *wrong* in any narrow sense — the workflow was internally consistent.

Yad's hop at 01:31 ("THIS IS WRONG PRACTICE COURSE CORRECT!") gave the lead the outside perspective it lacked. Within 7 minutes (01:38), PR #2 was closed and reissued as PR #5 on `wave/0-sanity`. All `impl/<slug>` branches were deleted. The new protocol — `wave-N-local/<slug>` LOCAL ONLY — held for the next 10 waves without revision.

Without this nudge, the autonomous loop would have left 72 branches on origin. The lead wouldn't have flagged it; the workflow looked fine from inside the loop.

### Example 2 — silent-after-commit local minimum

In wave 3, multiple workers committed locally and went idle without sending a summary. The protocol said send-a-summary, but workers were treating "task done" as equivalent to "send summary" — they'd hit done, idle, and the lead would wait.

The lead's first detection was around 03:09 UTC when it pinged the silent worker: *"Looks like you committed locally (commit 1f1cbcb on wave-3-local/curiosity-three-regions) and went idle without sending a summary. Per the wave-3 protocol, please send your summary now."*

This was a local-minima escape **by the lead, not by Yad.** Three later wave-3/wave-10/wave-11 workers triggered the same nudge pattern (visible in `team_messages.tsv` as "Request summary message" SendMessages). The fix was a worker-template update: "DO NOT GO SILENT — send a summary explicitly before idling."

### What doesn't escape local minima

The autonomous loop **did not** self-discover the branch-spam problem. The lead's audit subagent didn't either — the audits checked stub quality, not workflow correctness. It took an outside perspective (Yad) at 01:31 to point at the pattern.

This is the load-bearing observation: **outside perspective is the rare commodity.** A long-running agent loop builds internal consistency fast and protects it. **Yad's 40 prompts** broke down as roughly:

| Class | Count | Share of Yad's 40 |
|---|---:|---:|
| Type A (direction-changing) | 8 | 20% |
| Type B (status checks) | ~10 | 25% |
| Type C (review/merge gate) | ~5 | 13% |
| Type D (small clarifications, acks, copy-edits, follow-up work after wave 11) | ~17 | 42% |

The build was carried by **8 high-leverage Yad prompts** out of 40 total. The other 32 were either status check-ins, approval-gate one-liners, or low-cost follow-up after the wave-11 merge.

## Implications for the next build

If 8 prompts out of 40 did most of the human work, the design questions are:

1. **Can the lead self-detect protocol drift?** Branch-spam was visible in the orchestrator's own `git push` calls. A "wait, am I pushing one branch per stub?" self-check at wave end might have caught it without Yad's prompt.
2. **Can workers self-audit before idling?** Silent-after-commit was caught reactively. A worker prompt that mandates "send summary then await shutdown" instead of "send summary before idling" might have shifted the failure mode.
3. **What's the autonomy ceiling?** Orchestrator: ~25.7 turns per Yad-typed prompt. Hinton-problems (same machinery, week earlier) likely sits in a similar range — re-measure with the same hop classification to compare. Is 50 turns/prompt reachable? 100? Beyond what point does the build silently degrade?
4. **Is Type A predictable?** The two pivotal Type-A hops were both about protocol, not technical content. Future builds might want a "protocol-only" intervention budget and a "technical-only" intervention budget.

## Quotes worth keeping for the writeup

> *"why are u doing a branch per impl, should it be per waves?? why the branch spam. THIS IS WRONG PRACTICE COURSE CORRECT!"* — wave-1 → wave-2 pivot, 2026-05-07T01:31 UTC

> *"I need you to not rely on me anymore until you finish it all, basically, do wave into 1 per, audit, post to pr then trigger next wave"* — autonomous mode, 2026-05-07T02:11 UTC

> *"have we verified thse things to be truely done or left over?"* — surface the unmerged-PR gap, 2026-05-08T15:42 UTC

Each is a single sentence that reshaped the protocol or unstuck the loop. The blog post should quote them verbatim.

## Sources

- All 192 `type=user` records (40 Yad-typed + 152 routing/system) with timestamps: orchestrator session in `analysis/data/sessions.jsonl`
- 267 SendMessage calls across all sessions: `analysis/data/team_messages.tsv`
- 139 Agent dispatches across all sessions (orchestrator's share: 73): `analysis/data/agent_dispatches.tsv`
- Cosmin and Sung Jae's observations: chat-yad Telegram thread, 2026-05-14 and 2026-05-21

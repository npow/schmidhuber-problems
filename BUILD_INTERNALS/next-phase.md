# Next phase — trace export, language scrub, hops vs autonomous turns

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

This artifact captures the **map** of what was orchestrated. The next phase is the **analysis**.

## 1. Export traces / sessions

Pull the 59 sessions (orchestrator + 58 workers) into a portable form for teaching:

- One markdown file per session, with: full prompt history (user turns + assistant turns + tool calls), redacted of any private content.
- A trimmed-down "highlights" version with only the interesting decision points (first prompt, key strategy turns, last 2 hops).
- The `data/sessions.jsonl` file already has the per-session metadata. The trace export needs to walk the original JSONL files line-by-line and render.

## 2. Language scrub

Remove AI-slop / overused vocabulary / em-dashes / business jargon from the worker prompts and assistant outputs before publishing the traces. The `anti-slop-guide` skill is the canonical list. Specifically watch for:

- "delve", "tapestry", "landscape", "robust", "leverage"
- Em-dashes used as throat-clearing
- Throat-clearing openers ("Great question!", "Let me think about this carefully")
- Rule-of-three structures used reflexively
- Hedge phrases without information value ("It's worth noting that")

## 3. Hops vs autonomous turns

The current `data/sessions.tsv` has `hops`, `turns`, and `autonomy_ratio`. The next step is to compute:

- **Per-session autonomy index:** (turns − hops) / turns. Closer to 1.0 = more autonomous.
- **Per-wave autonomy:** averaged across workers + orchestrator's wave-slice.
- **Hop classification:** of Yad's **40 actual orchestrator prompts** (out of 192 `type=user` records, the rest being worker replies + slash + skill loaders), how many were:
  - Initial setup (one-shot context)
  - Strategy nudges (one-line course corrections)
  - Approval gates (yes/no on a plan)
  - Recovery prompts (something broke, fix it)
  - Closing prompts (wrap up, write docs)
- **Turn classification:** of the 1026 orchestrator turns, how many were:
  - Tool calls only (autonomous execution)
  - Tool call + reasoning (autonomous decision)
  - Plain text (responding to a hop)

A target autonomy ratio for the next build to beat: this build was **1026 orchestrator turns / 40 Yad-typed prompts ≈ 25.7 turns per Yad prompt** in the orchestrator. (The raw `total_turns/total_hops = 7265/353 = 20.6:1` ratio is misleading — `total_hops` includes worker→orchestrator routing and templated worker first-prompts, not just Yad-typed input.) Can the next build hit 50 turns per Yad prompt without quality regressing?

## 4. Open questions for the teaching session

- Were the 12 per-wave audits worth the cost? Each wave's `Explore` audit dispatch added ~3–8% overhead. (Plus 1 initial repo survey + 2 final BUILD_NOTES extracts = 15 Explore dispatches total in the orchestrator.)
- The workers' first-hop teammate-message has duplicated context. Could a shorter handoff cut worker cost?
- Could waves run in **parallel** (e.g. wave 6 and wave 7 simultaneously) instead of serially? They have no dependency.
- Could the audit step be merged into the worker prompt (self-audit), eliminating one dispatch per wave?

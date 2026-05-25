# Verify the numbers yourself

The promise: **every number on these pages traces back to `analysis/data/sessions.jsonl`** — the raw transcript of the orchestrator session that drove this build, plus the 58 worker session JSONLs it spawned. The scripts that extracted those numbers are in [`analysis/scripts/`](https://github.com/cybertronai/schmidhuber-problems/tree/main/analysis/scripts) and the data is in [`analysis/data/`](https://github.com/cybertronai/schmidhuber-problems/tree/main/analysis/data). You can re-run, spot-check, or audit any specific claim.

## The pipeline (3 steps, ~3 minutes total)

```bash
# 1. Parse Claude Code session JSONLs into structured metrics + dispatch tables.
#    Reads ~/.claude/projects/-Users-yadkonrad-dev-dev-year26-feb26-SutroYaro/*.jsonl
python3 analysis/scripts/analyze_sessions.py

# 2. Scrub foul language and local-path leaks from the dumped data (idempotent).
python3 analysis/scripts/redact_hops.py

# 3. Emit the markdown pages under BUILD_INTERNALS/ from the data.
python3 analysis/scripts/build_artifact.py
```

Re-running the pipeline regenerates this site's data-driven pages (`sessions.md`, `cost-rollup.md`, `orchestration-map.md`, all 13 wave pages, `next-phase.md`) from the raw JSONL. Hand-written narrative pages (Overview, FAQ, What worked / didn't, How to reproduce, Worker prompt anatomy, Patterns observed, Human in the loop, Pivot moments, this page) are not auto-generated — they cite numbers from the data.

## Spot-check any claim

Five quick verifications you can paste into a terminal and run:

### "40 Yad-typed prompts to the orchestrator"

```bash
python3 -c "
import json
recs = [json.loads(l) for l in open('analysis/data/sessions.jsonl')]
orch = next(r for r in recs if r['session_id'].startswith('63285119'))
yad = teammate = 0
for h in orch['all_hops']:
    t = (h.get('text') or '').strip()
    if t.startswith('<teammate-message'): teammate += 1
    elif t and not t.startswith(('<local-command','<command-name','Base directory','[REDACTED','[Image')):
        yad += 1
print(f'Yad-typed: {yad}  teammate-replies: {teammate}')
"
```
Expected: `Yad-typed: 40  teammate-replies: 142`

### "1.13 billion tokens total / $3,879"

```bash
python3 -c "
import json
recs = [json.loads(l) for l in open('analysis/data/sessions.jsonl')]
total = 0; cost = 0
PRICE = {'input':15/1e6,'output':75/1e6,'cache_read':1.5/1e6,'cache_write_5m':18.75/1e6,'cache_write_1h':30/1e6}
for r in recs:
    if '63285119' in r['session_id'] or 'schmidhuber-impl' in (r.get('first_hop_text') or ''):
        for k, v in r['tokens'].items():
            total += v; cost += v * PRICE.get(k, 0)
print(f'Tokens: {total/1e9:.2f}B  Estimated cost: \${cost:,.0f}')
"
```
Expected: `Tokens: 1.13B  Estimated cost: $3,879`

### "73 Agent dispatches from the orchestrator (58 builders + 15 audits)"

```bash
awk -F'\t' '$1 == "63285119-154e-42ab-9555-7a42471b0309" {print $3}' analysis/data/agent_dispatches.tsv | sort | uniq -c
```
Expected: `58 general-purpose` and `15 Explore`.

### "58 worker sessions, all linked to schmidhuber-impl"

```bash
grep -c 'schmidhuber-impl' analysis/data/sessions.jsonl
```
Expected: at least 59 (orchestrator's `TeamCreate` description + 58 worker first-prompts). The Sessions page enumerates them.

### "8 direction-changing prompts out of 40"

The 8 are listed verbatim with timestamps in [Pivot moments](pivot-moments.md). Cross-check against the orchestrator's hop list:

```bash
python3 -c "
import json
recs = [json.loads(l) for l in open('analysis/data/sessions.jsonl')]
orch = next(r for r in recs if r['session_id'].startswith('63285119'))
# The 8 highest-leverage hops (by timestamp + content match to Pivot moments page)
keys = ['THIS IS WRONG PRACTICE','not rely on me anymore','have we verified','dispathc multiple agents','review it/audit','BUT FIRST FIRST FINISH','its mdBook','why are there teams']
hits = [h for h in orch['all_hops'] for k in keys if k in (h.get('text') or '')]
print(f'Found {len(hits)} direction-changing prompts in transcript.')
"
```
Expected: `Found 8 direction-changing prompts in transcript.`

## Corrections in this build's history

Two numbers in earlier drafts were wrong and were corrected in dedicated PRs. Listed here so the audit history is transparent — and so future readers can see the same kind of correction is welcomed:

| Original claim (wrong) | Corrected to | Fixed by |
|---|---|---|
| "780k tokens total" (Yad's Telegram post 2026-05-08 16:44 UTC) | **1.13 B tokens** across 59 sessions. 780k was the orchestrator's context-window utilization meter at one moment, not cumulative spend. | [PR #20](https://github.com/cybertronai/schmidhuber-problems/pull/20) — `docs: add measured token math (closes #19)` |
| "192 user prompts to the orchestrator" (build-internals draft) | **40 Yad-typed prompts.** The 192 was every `type=user` record in the JSONL, including 142 worker→orchestrator routed replies, 6 slash commands, 2 skill outputs, and 2 redacted entries. | [PR #22](https://github.com/cybertronai/schmidhuber-problems/pull/22) — `docs: correct the prompt count + autonomy ratio` |

If you find a number that looks wrong, open an issue or a PR with the verification command and the expected value. Numerical-audit PRs against this catalog are encouraged.

## What's traceable, what isn't

| Claim | Source | Traceable? |
|---|---|---|
| All token counts, costs, hop counts, turn counts, dispatch counts | `analysis/data/sessions.jsonl` (auto-extracted) | ✓ Re-run `analyze_sessions.py` |
| Yad's verbatim prompts and timestamps | `analysis/data/sessions.jsonl` `all_hops` field | ✓ |
| Per-wave PR numbers, merge timestamps | `gh pr list --state merged` on the GitHub repo | ✓ |
| Subagent prompts, descriptions, team names | `analysis/data/agent_dispatches.tsv` | ✓ |
| Inter-team messages | `analysis/data/team_messages.tsv` | ✓ |
| Specific page URLs, dates, repo links | the repo itself | ✓ |
| "Hinton-problems shipped 53 stubs in ~30 hours" | External — [cybertronai/hinton-problems BUILD_NOTES](https://github.com/cybertronai/hinton-problems/blob/main/BUILD_NOTES.md) | External-public |
| "Pure numpy + matplotlib, deterministic, <5 min/seed" | Per-stub READMEs at `<stub>/README.md` | ✓ run any stub |
| Cost estimates at "$3,879" | Computed from token counts × Opus 4.x public pricing (May 2026) | ✓ but pricing can change — re-multiply if rates shift |

## One last note

The session JSONLs themselves contain Yad's raw typed prompts. Foul language was redacted in 11 hops (10 frustrated venting, 1 image-path leak) before the data was published — see [`analysis/scripts/redact_hops.py`](https://github.com/cybertronai/schmidhuber-problems/blob/main/analysis/scripts/redact_hops.py) for the exact redaction policy. Otherwise the transcript is unmodified.

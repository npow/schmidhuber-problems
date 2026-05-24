# Schmidhuber-Problems Orchestration Map

Reconstructed map of how SutroYaro dispatched the parallel agent-team build of
[cybertronai/schmidhuber-problems](https://github.com/cybertronai/schmidhuber-problems)
between 2026-05-06 and 2026-05-08.

## Headline

- **One orchestrator session** drove the entire build: `63285119` ($1,283.73, 192 user prompts, 1026 assistant turns).
- **58 worker sessions** spawned via `agent-teams`, one per stub. Each worker built one Schmidhuber stub end-to-end.
- **12 numbered waves** (0 through 11) bundled the 58 stubs into PRs #4–#15. Wave 0 was a sanity check; wave 11 (v1.5) covered the heavyweight-env synthetic substitutes.
- **Meta PR #16** (mdBook site + BUILD_NOTES + RESULTS + VISUAL_TOUR) and **docs PR #20** (token math correction, closes #19) followed the wave merges.
- **Total estimated cost:** $3,878.59 across the orchestrator + workers (Opus 4.x public pricing, May 2026).
- **Total user prompts (hops):** 353. **Total assistant turns:** 7265. Autonomy ratio (turns/hops): **20.6**.

## What's in this directory

| File | What it has |
|---|---|
| `README.md` | This page. Top-level summary. |
| `orchestration-map.md` | Hierarchy + timeline: which session spawned which, when waves landed, audit pattern. |
| `sessions.md` | Full table of every session: ID, role, wave, stub built, tokens, cost. |
| `cost-rollup.md` | Cost by pool (input / output / cache_read / cache_write_5m / cache_write_1h), by wave, by session. |
| `waves/` | One markdown file per wave (0–11 + meta + token-math). Each lists workers, stubs, PR, cost. |
| `worker-prompt-anatomy.md` | One worker's full first prompt, annotated section by section. The template that ran 58 times. |
| `patterns.md` | What worked, what cost a lot, what's worth carrying forward. Backed by the data. |
| `next-phase.md` | What's *not* yet done: trace export, language scrub, hops-vs-autonomous-turns analysis. |
| `scripts/` | The three Python scripts that produced everything here. Pipeline: `analyze_sessions.py` → `redact_hops.py` → `build_artifact.py`. Re-run any time. |
| `data/` | Raw TSV + JSONL outputs from the analyzer. The source of truth for every number on every page. |

## How to read this

Start at `orchestration-map.md` for the picture of who spawned who and when. Drop into a specific wave file from `waves/` to see what each worker built and what it cost. Cross-check any number against `data/sessions.tsv`.

## Caveats

- **Scope filter:** "schmidhuber" string-match on JSONL contents. Auxiliary sessions that mentioned schmidhuber but weren't part of the build are listed separately in `sessions.md` and excluded from cost rollups.
- **Cost is an estimate** using Opus 4.x public pricing. Actual billing depends on prompt-cache hit rates, which the JSONL `usage` field records — those numbers are honest.
- **Hop count** filters out tool_results, hook outputs, and sidechain traffic — only counts Yad-typed prompts.
- **Wave assignment** maps each worker to its wave by the stub name from its first teammate-message. All 58 workers map to a finished stub directory in the repo today.

## Token pool totals

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 202,129 | $3.03 |
| output | 10,581,714 | $793.63 |
| cache_read | 1,064,199,056 | $1,596.30 |
| cache_write_5m | 4,107,469 | $77.02 |
| cache_write_1h | 46,953,891 | $1,408.62 |
| **total** | 1,126,044,259 | **$3,878.59** |

Cache reads dominate token volume; the **effective cost** of input is much lower than raw input-token count would suggest because the system prompt + tool list + project context were cached and re-read across every turn.

## Related repos

- Schmidhuber stubs: https://github.com/cybertronai/schmidhuber-problems
- Hinton stubs (parallel build, same week): https://github.com/cybertronai/hinton-problems
- Dispatcher (this repo): https://github.com/cybertronai/SutroYaro

## See also

- [BUILD_NOTES.md](https://github.com/cybertronai/schmidhuber-problems/blob/main/BUILD_NOTES.md) — the narrative session report; this map is the structured drill-down version
- [SutroYaro catchups 2026-05-20](https://github.com/cybertronai/SutroYaro/blob/main/docs/catchups/2026-05-20.md) — context for this build
- [SutroYaro related-repos map](https://github.com/cybertronai/SutroYaro/blob/main/docs/related-repos.md) — the 8-repo cybertronai org

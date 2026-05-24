#!/usr/bin/env python3
"""Build the schmidhuber-orchestration markdown artifact from session data.

Reads:
  ../analysis/data/sessions.jsonl           (full per-session detail)
  ../analysis/data/agent_dispatches.tsv     (orchestrator's Agent calls)
  ../analysis/data/team_messages.tsv

Writes (into the mdBook source at BUILD_INTERNALS/):
  README.md
  orchestration-map.md
  sessions.md
  cost-rollup.md
  next-phase.md
  waves/README.md
  waves/wave-NN-<slug>.md (one per wave)

This lives in the schmidhuber-problems repo. To regenerate everything:

    python3 analysis/scripts/analyze_sessions.py   # parse JSONL session logs
    python3 analysis/scripts/redact_hops.py        # scrub foul-language hops
    python3 analysis/scripts/build_artifact.py     # emit markdown into BUILD_INTERNALS/

Then bin/build_book.py copies BUILD_INTERNALS/ into src/build-internals/ and
mdbook build renders the site.
"""
from __future__ import annotations
import json, os, re, csv
from datetime import datetime, timezone
from collections import defaultdict, Counter

ANALYSIS = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ANALYSIS, "data")
# Output: BUILD_INTERNALS/ at the repo root (sibling of analysis/)
REPO_ROOT = os.path.abspath(os.path.join(ANALYSIS, ".."))
OUT_ROOT = os.path.join(REPO_ROOT, "BUILD_INTERNALS")
WAVES = os.path.join(OUT_ROOT, "waves")
# ROOT kept as an alias for legacy code paths inside this module that still
# reference it. New code should use OUT_ROOT.
ROOT = OUT_ROOT


def write_md(rel_path, content):
    """Write into BUILD_INTERNALS/. Path is relative to that dir."""
    primary = os.path.join(OUT_ROOT, rel_path)
    os.makedirs(os.path.dirname(primary), exist_ok=True)
    with open(primary, "w") as f:
        f.write(content)

ORCHESTRATOR_ID = "63285119-154e-42ab-9555-7a42471b0309"

# Map wave-number to (slug, PR#, branch, stub-list-in-dispatch-order, originating-commit)
# Populated from orchestrator dispatch descriptions + git log.
WAVE_TABLE = [
    # (wave_num, slug, pr_num, branch, [stubs in dispatch order])
    (0,  "sanity",            5,  "wave/0-sanity",            ["nbb-xor"]),
    (1,  "search",            4,  "wave/1-search",            ["rs-two-sequence","rs-parity","rs-tomita","levin-count-inputs","levin-add-positions","oops-towers-of-hanoi"]),
    (2,  "local-rules",       6,  "wave/2-local-rules",       ["nbb-moving-light","flip-flop","pole-balance-non-markov","pole-balance-markov-vac","saccadic-target-detection"]),
    (3,  "rl-hidden-state",   7,  "wave/3-rl-hidden-state",   ["curiosity-three-regions","subgoal-obstacle-avoidance","pomdp-flag-maze","ssa-bias-transfer-mazes","hq-learning-pomdp"]),
    (4,  "history-fastweights", 8, "wave/4-history-fastweights", ["chunker-22-symbol","chunker-very-deep-1200","fast-weights-unknown-delay","fast-weights-key-value","self-referential-weight-matrix"]),
    (5,  "predictability",    9,  "wave/5-predictability",    ["predictability-min-binary-factors","predictable-stereo","semilinear-pm-image-patches","lococode-ica"]),
    (6,  "lstm-1",            10, "wave/6-lstm-1",            ["adding-problem","embedded-reber","noise-free-long-lag","two-sequence-noise","multiplication-problem","temporal-order-3bit"]),
    (7,  "lstm-2",            11, "wave/7-lstm-2",            ["temporal-order-4bit","continual-embedded-reber","anbn-anbncn","timing-counting-spikes","blues-improvisation"]),
    (8,  "evolutionary",      12, "wave/8-evolutionary",      ["pipe-symbolic-regression","pipe-6-bit-parity","evolino-sines-mackey-glass","double-pole-no-velocity"]),
    (9,  "deep-mlps",         13, "wave/9-deep-mlps",         ["mnist-deep-mlp","mcdnn-image-bench","compete-to-compute","highway-networks"]),
    (10, "modern",            14, "wave/10-modern",           ["neural-em-shapes","relational-nem-bouncing-balls","linear-transformers-fwp","neural-data-router","upside-down-rl"]),
    (11, "v1.5",              15, "wave/11-v1.5",             ["timit-blstm-ctc","iam-handwriting","em-segmentation-isbi","lstm-search-space-odyssey","clockwork-rnn","world-models-carracing","world-models-vizdoom-dream","torcs-vision-evolution"]),
]
META_PR = (16, "meta-site-and-docs", "meta/site-and-docs", "mdBook site, BUILD_NOTES, RESULTS, VISUAL_TOUR, README catalog")
TOKEN_DOCS_PR = (20, "docs/token-math-correction", "docs/token-math-correction", "measured token math (closes #19)")

# Public Opus 4.x pricing (May 2026)
PRICE = {
    "input":          15.0  / 1_000_000,
    "output":         75.0  / 1_000_000,
    "cache_read":      1.50 / 1_000_000,
    "cache_write_5m": 18.75 / 1_000_000,
    "cache_write_1h": 30.0  / 1_000_000,
}

# Two formats observed in worker first prompts:
#   You are `<name>-builder`, teammate on `schmidhuber-impl`. Implement the **<stub>** stub
#   You are `<name>-builder` on `schmidhuber-impl`. Implement **<stub>** per SPEC issue #1
# Plus there are hinton-impl workers mixed in (different team) which we exclude.
BUILDER_RE = re.compile(r'You are `([^`]+)`[^`]*?`(schmidhuber-impl|hinton-impl)`')
STUB_RE = re.compile(r'Implement (?:the )?\*\*([^*]+)\*\*(?: stub| per SPEC)?')


def load_sessions():
    sessions = []
    for ln in open(os.path.join(DATA, "sessions.jsonl")):
        sessions.append(json.loads(ln))
    return sessions


def classify(sessions):
    by_id = {s["session_id"]: s for s in sessions}
    orchestrator = by_id.get(ORCHESTRATOR_ID)
    # Workers: have a teammate-message in first_hop_text and are not the orchestrator
    workers = []
    auxiliary = []  # sessions that mention schmidhuber but aren't workers/orchestrator
    for s in sessions:
        if s["session_id"] == ORCHESTRATOR_ID:
            continue
        fh = s.get("first_hop_text") or ""
        m = BUILDER_RE.search(fh)
        if m and m.group(2) == "schmidhuber-impl":
            teammate, team = m.group(1), m.group(2)
            sm = STUB_RE.search(fh)
            stub = sm.group(1) if sm else ""
            # Derive stub from teammate name if not found in prompt (strip "-builder")
            if not stub and teammate.endswith("-builder"):
                stub = teammate[:-len("-builder")]
            s["_teammate"] = teammate
            s["_team"] = team
            s["_stub"] = stub
            workers.append(s)
        else:
            auxiliary.append(s)
    return orchestrator, workers, auxiliary


def assign_waves(workers):
    """Map each worker to its wave based on the stub name."""
    stub_to_wave = {}
    for w in WAVE_TABLE:
        for stub in w[4]:
            stub_to_wave[stub] = w
    for w in workers:
        stub = w.get("_stub") or ""
        wave = stub_to_wave.get(stub)
        if wave:
            w["_wave_num"] = wave[0]
            w["_wave_slug"] = wave[1]
            w["_wave_pr"] = wave[2]
        else:
            w["_wave_num"] = None
            w["_wave_slug"] = "(unassigned)"
            w["_wave_pr"] = None
    return workers


def fmt_cost(c): return f"${c:,.2f}"
def fmt_tok(n):  return f"{n:,}"


def total_tokens(s):
    return sum(s["tokens"].values())


def cost_breakdown(s):
    return {pool: s["tokens"].get(pool, 0) * PRICE[pool] for pool in PRICE}


def write_readme(orchestrator, workers, auxiliary):
    total_cost = orchestrator["cost_usd"] + sum(w["cost_usd"] for w in workers)
    total_hops = orchestrator["hops"] + sum(w["hops"] for w in workers)
    total_turns = orchestrator["turns"] + sum(w["turns"] for w in workers)
    total_tokens_all = Counter()
    for s in [orchestrator] + workers:
        for k, v in s["tokens"].items():
            total_tokens_all[k] += v

    lines = [
        "# Schmidhuber-Problems Orchestration Map",
        "",
        "Reconstructed map of how SutroYaro dispatched the parallel agent-team build of",
        "[cybertronai/schmidhuber-problems](https://github.com/cybertronai/schmidhuber-problems)",
        "between 2026-05-06 and 2026-05-08.",
        "",
        "## Headline",
        "",
        f"- **One orchestrator session** drove the entire build: `{ORCHESTRATOR_ID[:8]}` ({fmt_cost(orchestrator['cost_usd'])}, {orchestrator['hops']} user prompts, {orchestrator['turns']} assistant turns).",
        f"- **{len(workers)} worker sessions** spawned via `agent-teams`, one per stub. Each worker built one Schmidhuber stub end-to-end.",
        f"- **{len(WAVE_TABLE)} numbered waves** (0 through 11) bundled the 58 stubs into PRs #4–#15. Wave 0 was a sanity check; wave 11 (v1.5) covered the heavyweight-env synthetic substitutes.",
        f"- **Meta PR #16** (mdBook site + BUILD_NOTES + RESULTS + VISUAL_TOUR) and **docs PR #20** (token math correction, closes #19) followed the wave merges.",
        f"- **Total estimated cost:** {fmt_cost(total_cost)} across the orchestrator + workers (Opus 4.x public pricing, May 2026).",
        f"- **Total user prompts (hops):** {total_hops}. **Total assistant turns:** {total_turns}. Autonomy ratio (turns/hops): **{total_turns/max(total_hops,1):.1f}**.",
        "",
        "## What's in this directory",
        "",
        "| File | What it has |",
        "|---|---|",
        "| `README.md` | This page. Top-level summary. |",
        "| `orchestration-map.md` | Hierarchy + timeline: which session spawned which, when waves landed, audit pattern. |",
        "| `sessions.md` | Full table of every session: ID, role, wave, stub built, tokens, cost. |",
        "| `cost-rollup.md` | Cost by pool (input / output / cache_read / cache_write_5m / cache_write_1h), by wave, by session. |",
        "| `waves/` | One markdown file per wave (0–11 + meta + token-math). Each lists workers, stubs, PR, cost. |",
        "| `worker-prompt-anatomy.md` | One worker's full first prompt, annotated section by section. The template that ran 58 times. |",
        "| `patterns.md` | What worked, what cost a lot, what's worth carrying forward. Backed by the data. |",
        "| `next-phase.md` | What's *not* yet done: trace export, language scrub, hops-vs-autonomous-turns analysis. |",
        "| `scripts/` | The three Python scripts that produced everything here. Pipeline: `analyze_sessions.py` → `redact_hops.py` → `build_artifact.py`. Re-run any time. |",
        "| `data/` | Raw TSV + JSONL outputs from the analyzer. The source of truth for every number on every page. |",
        "",
        "## How to read this",
        "",
        "Start at `orchestration-map.md` for the picture of who spawned who and when. Drop into a specific wave file from `waves/` to see what each worker built and what it cost. Cross-check any number against `data/sessions.tsv`.",
        "",
        "## Caveats",
        "",
        "- **Scope filter:** \"schmidhuber\" string-match on JSONL contents. Auxiliary sessions that mentioned schmidhuber but weren't part of the build are listed separately in `sessions.md` and excluded from cost rollups.",
        "- **Cost is an estimate** using Opus 4.x public pricing. Actual billing depends on prompt-cache hit rates, which the JSONL `usage` field records — those numbers are honest.",
        "- **Hop count** filters out tool_results, hook outputs, and sidechain traffic — only counts Yad-typed prompts.",
        "- **Wave assignment** maps each worker to its wave by the stub name from its first teammate-message. All 58 workers map to a finished stub directory in the repo today.",
        "",
        "## Token pool totals",
        "",
        "| Pool | Tokens | Cost |",
        "|---|---:|---:|",
    ]
    for pool in ["input", "output", "cache_read", "cache_write_5m", "cache_write_1h"]:
        toks = total_tokens_all[pool]
        cost = toks * PRICE[pool]
        lines.append(f"| {pool} | {fmt_tok(toks)} | {fmt_cost(cost)} |")
    lines.append(f"| **total** | {fmt_tok(sum(total_tokens_all.values()))} | **{fmt_cost(total_cost)}** |")
    lines += [
        "",
        "Cache reads dominate token volume; the **effective cost** of input is much lower than raw input-token count would suggest because the system prompt + tool list + project context were cached and re-read across every turn.",
        "",
        "## Related repos",
        "",
        "- Schmidhuber stubs: https://github.com/cybertronai/schmidhuber-problems",
        "- Hinton stubs (parallel build, same week): https://github.com/cybertronai/hinton-problems",
        "- Dispatcher (this repo): https://github.com/cybertronai/SutroYaro",
        "",
        "## See also",
        "",
        "- [BUILD_NOTES.md](https://github.com/cybertronai/schmidhuber-problems/blob/main/BUILD_NOTES.md) — the narrative session report; this map is the structured drill-down version",
        "- [SutroYaro catchups 2026-05-20](https://github.com/cybertronai/SutroYaro/blob/main/docs/catchups/2026-05-20.md) — context for this build",
        "- [SutroYaro related-repos map](https://github.com/cybertronai/SutroYaro/blob/main/docs/related-repos.md) — the 8-repo cybertronai org",
    ]
    write_md("README.md", "\n".join(lines) + "\n")


def write_orchestration_map(orchestrator, workers, agent_dispatches):
    """Hierarchy and timeline."""
    # Group dispatches by wave for the timeline
    lines = [
        "# Orchestration Map",
        "",
        "Hierarchy of sessions and the wave-by-wave timeline.",
        "",
        "## Topology",
        "",
        "```mermaid",
        "graph TD",
        "    Yad[\"Yad<br/>(terminal)\"]",
        f"    Orch[\"orchestrator<br/>{ORCHESTRATOR_ID[:8]}<br/>{orchestrator['hops']} hops, {orchestrator['turns']} turns\"]",
        "    Team[(\"team: schmidhuber-impl<br/>TeamCreate × 1\")]",
        "    Workers[\"worker sessions × 58<br/>one per stub<br/>spawned via Agent(team_name=...)\"]",
        "    Audits[\"Explore audits × 15<br/>1 initial survey<br/>12 per-wave audits<br/>2 BUILD_NOTES extracts\"]",
        "    PRs[\"13 wave + meta PRs\"]",
        "",
        "    Yad -->|prompts| Orch",
        f"    Orch -->|{len(orchestrator['team_creates'])} TeamCreate| Team",
        f"    Orch -->|58 Agent dispatches| Workers",
        f"    Orch -->|15 Agent dispatches| Audits",
        f"    Orch -->|{len(orchestrator['send_messages'])} SendMessage| Workers",
        "    Workers -->|one branch per stub| PRs",
        "    Audits -->|verdict| PRs",
        "    PRs -->|merged in 90s burst| Yad",
        "",
        "    classDef root fill:#fff3e0,stroke:#e65100,color:#000",
        "    classDef orch fill:#e3f2fd,stroke:#1565c0,color:#000",
        "    classDef team fill:#f3e5f5,stroke:#6a1b9a,color:#000",
        "    classDef worker fill:#e8f5e9,stroke:#2e7d32,color:#000",
        "    classDef audit fill:#fce4ec,stroke:#ad1457,color:#000",
        "    classDef output fill:#fff9c4,stroke:#f57f17,color:#000",
        "    class Yad root",
        "    class Orch orch",
        "    class Team team",
        "    class Workers worker",
        "    class Audits audit",
        "    class PRs output",
        "```",
        "",
        "The orchestrator created **one persistent team** (`schmidhuber-impl`) via `TeamCreate` and routed work to teammates via `Agent(team_name=schmidhuber-impl, name=<stub>-builder, ...)` calls. The orchestrator's `SendMessage` calls were used to nudge specific teammates mid-build.",
        "",
        f"- TeamCreate calls in orchestrator: **{len(orchestrator['team_creates'])}**",
        f"- Agent dispatches: **{len(orchestrator['agent_dispatches'])}**",
        f"- SendMessage calls: **{len(orchestrator['send_messages'])}**",
        f"- TaskCreate / TaskUpdate (orchestrator's own todo tracking): **{orchestrator['task_creates_n']}** / **{orchestrator['task_updates_n']}**",
        "",
        "## Wave-by-wave timeline (UTC)",
        "",
        "| Wave | First dispatch | Audit dispatch | PR# | Stubs | Branch |",
        "|---:|---|---|---:|---:|---|",
    ]
    # For each wave, find first general-purpose dispatch and the audit
    for wave_num, slug, pr, branch, stubs in WAVE_TABLE:
        first_disp = None
        audit_disp = None
        for ad in agent_dispatches:
            ts = ad["ts"]
            desc_lower = ad["description"].lower()
            if ad["description"].startswith(f"Wave {wave_num}:") and ad["subagent_type"] == "general-purpose":
                if first_disp is None:
                    first_disp = ts
            if "audit" in desc_lower and re.search(rf'\bwave[-\s]?{wave_num}\b', desc_lower):
                if audit_disp is None:
                    audit_disp = ts
        lines.append(
            f"| {wave_num} | {first_disp or '?'} | {audit_disp or '?'} | #{pr} | {len(stubs)} | `{branch}` |"
        )
    lines += [
        "",
        "## One wave, sequenced",
        "",
        "```mermaid",
        "sequenceDiagram",
        "    autonumber",
        "    participant Y as Yad",
        "    participant O as Orchestrator",
        "    participant W as Workers (N parallel)",
        "    participant A as Audit (Explore)",
        "    participant G as GitHub",
        "",
        "    Y->>O: \"trigger wave N\" (sometimes implicit)",
        "    O->>W: Agent × N (one per stub, into team schmidhuber-impl)",
        "    par each worker, isolated worktree",
        "        W-->>W: build stub, commit LOCAL ONLY",
        "    end",
        "    W->>O: SendMessage(summary)",
        "    O->>A: Agent (Explore, audit all wave-N stubs)",
        "    A->>O: verdict",
        "    O->>G: assemble wave/N branch + open wave PR",
        "    O->>W: SendMessage(shutdown_request) × N",
        "    Note over O,Y: orchestrator continues to wave N+1",
        "```",
        "",
        "Every wave followed the same protocol:",
        "1. Orchestrator emits N parallel `Agent` calls (one per stub) into the `schmidhuber-impl` team.",
        "2. Workers each build their stub in a sandboxed worktree.",
        "3. After workers finish, orchestrator launches one `Explore` audit agent that reads all stubs and flags inconsistencies.",
        "4. Orchestrator opens the wave PR.",
        "5. Move to the next wave.",
        "",
        "The interesting bit: PRs were all merged in a tight burst on 2026-05-08 15:49–15:50 UTC, *after* every wave was built and audited. The build itself ran across 2026-05-06 23:09 → 2026-05-08 14:51 UTC, ~40 hours wall-clock.",
        "",
        "## Sidechain note",
        "",
        f"The orchestrator session has **{orchestrator['sidechain_turns']} sidechain turns**: in-process subagent traffic (mostly the `Explore` agent reads). Worker sessions appear as separate JSONLs in the project directory because `agent-teams` spawns them as distinct Claude Code instances, even though their `cwd` is still `SutroYaro/`.",
    ]
    write_md("orchestration-map.md", "\n".join(lines) + "\n")


def write_sessions_md(orchestrator, workers, auxiliary):
    """One big table of every session."""
    lines = [
        "# Sessions",
        "",
        "Every Claude Code session that touched the schmidhuber-problems build.",
        "Numbers below come straight from `data/sessions.tsv`. Re-generate with:",
        "",
        "```",
        "python3 analysis/schmidhuber-orchestration/scripts/analyze_sessions.py",
        "```",
        "",
        "## Orchestrator",
        "",
        "| Session ID | Role | Start (UTC) | Duration | Hops | Turns | Disp | SMsg | Cost | Total tokens |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        f"| `{orchestrator['session_id'][:8]}` | orchestrator | {orchestrator['first_ts'][:16]} | "
        f"{((datetime.fromisoformat(orchestrator['last_ts']) - datetime.fromisoformat(orchestrator['first_ts'])).total_seconds()/3600):.1f}h | "
        f"{orchestrator['hops']} | {orchestrator['turns']} | {len(orchestrator['agent_dispatches'])} | "
        f"{len(orchestrator['send_messages'])} | {fmt_cost(orchestrator['cost_usd'])} | "
        f"{fmt_tok(total_tokens(orchestrator))} |",
        "",
        "Full session ID: `" + orchestrator["session_id"] + "`",
        "",
        "## Workers",
        "",
        "One row per dispatched stub-builder, grouped by wave.",
        "",
    ]
    by_wave = defaultdict(list)
    for w in workers:
        by_wave[w.get("_wave_num")].append(w)
    for wave_num, slug, pr, branch, stubs in WAVE_TABLE:
        ws = sorted(by_wave.get(wave_num, []), key=lambda x: x["first_ts"] or "")
        if not ws:
            continue
        lines += [
            f"### Wave {wave_num} — {slug} (PR #{pr})",
            "",
            "| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |",
            "|---|---|---|---|---:|---:|---:|---:|",
        ]
        for w in ws:
            dur_min = ""
            if w["first_ts"] and w["last_ts"]:
                dur_min = f"{(datetime.fromisoformat(w['last_ts']) - datetime.fromisoformat(w['first_ts'])).total_seconds()/60:.0f}m"
            lines.append(
                f"| `{w['session_id'][:8]}` | `{w.get('_stub','')}` | "
                f"`{w.get('_teammate','')}` | {w['first_ts'][:16]} | "
                f"{dur_min} | {w['hops']} | {w['turns']} | {fmt_cost(w['cost_usd'])} |"
            )
        lines.append("")
    if auxiliary:
        # Categorize auxiliary: hinton-impl workers, hinton orchestrator, follow-ups
        hinton_workers = [s for s in auxiliary if 'hinton-impl' in (s.get('first_hop_text') or '')]
        hinton_orch_candidates = [s for s in auxiliary if s.get('first_ts','').startswith('2026-05-01')]
        followups = [s for s in auxiliary if s not in hinton_workers and s not in hinton_orch_candidates]

        lines += [
            "## Auxiliary sessions (mentioned schmidhuber, not part of the build)",
            "",
            f"{len(auxiliary)} sessions matched the schmidhuber string but are not workers or the orchestrator. They fall into three groups:",
            "",
            "### Hinton-problems parallel build (one week earlier)",
            "",
            f"The same agent-teams pattern was used for **cybertronai/hinton-problems** during 2026-05-01 to 2026-05-03. {len(hinton_orch_candidates)} orchestrator session(s) + {len(hinton_workers)} workers visible here. Out of scope for this map but the structural twin.",
            "",
            "| Session | Role | Start (UTC) | Hops | Turns | Cost |",
            "|---|---|---|---:|---:|---:|",
        ]
        for s in sorted(hinton_orch_candidates, key=lambda x: x['first_ts'] or ''):
            ft = (s['first_ts'] or '')[:16]
            lines.append(f"| `{s['session_id'][:8]}` | hinton orchestrator | {ft} | {s['hops']} | {s['turns']} | {fmt_cost(s['cost_usd'])} |")
        for s in sorted(hinton_workers, key=lambda x: x['first_ts'] or ''):
            fh = s.get('first_hop_text') or ''
            m = BUILDER_RE.search(fh)
            name = m.group(1) if m else '?'
            ft = (s['first_ts'] or '')[:16]
            lines.append(f"| `{s['session_id'][:8]}` | hinton worker (`{name}`) | {ft} | {s['hops']} | {s['turns']} | {fmt_cost(s['cost_usd'])} |")
        lines += [
            "",
            "### Follow-ups",
            "",
            "Catch-up / handoff / sync sessions after the build.",
            "",
            "| Session | Start (UTC) | Hops | Turns | Cost | First-hop hint |",
            "|---|---|---:|---:|---:|---|",
        ]
        for s in sorted(followups, key=lambda x: x['first_ts'] or ''):
            ft = (s['first_ts'] or '')[:16]
            hint = (s.get('first_hop_text') or '')[:80].replace('\n',' ').replace('|', '\\|')
            lines.append(f"| `{s['session_id'][:8]}` | {ft} | {s['hops']} | {s['turns']} | {fmt_cost(s['cost_usd'])} | {hint} |")
        lines.append("")
    write_md("sessions.md", "\n".join(lines) + "\n")


def write_cost_rollup(orchestrator, workers):
    """Cost breakdown by pool, by wave, by role."""
    all_sessions = [orchestrator] + workers
    # By pool
    pool_totals = Counter()
    for s in all_sessions:
        for k, v in s["tokens"].items():
            pool_totals[k] += v
    pool_costs = {k: v * PRICE[k] for k, v in pool_totals.items()}
    total_cost = sum(s["cost_usd"] for s in all_sessions)

    lines = [
        "# Cost Rollup",
        "",
        f"Estimated at Opus 4.x public pricing (May 2026): "
        f"input ${15}/M, output ${75}/M, cache_read $1.50/M, cache_write_5m $18.75/M, cache_write_1h $30/M.",
        "",
        "## Cost composition",
        "",
        "```mermaid",
        "pie showData",
        f"    title $ share by token pool (total {fmt_cost(total_cost)})",
    ]
    for pool in ["input", "output", "cache_read", "cache_write_5m", "cache_write_1h"]:
        lines.append(f'    "{pool}" : {pool_costs[pool]:.2f}')
    lines += [
        "```",
        "",
        "Two pools combine to **77.5%** of the bill — `cache_read` (41%) and `cache_write_1h` (36%). Output is third at 20.5%. Raw input tokens are negligible because the system/tool prompt was almost always cached.",
        "",
        "## By pool (orchestrator + 58 workers)",
        "",
        "| Pool | Tokens | $/M | Cost | Share |",
        "|---|---:|---:|---:|---:|",
    ]
    for pool in ["input", "output", "cache_read", "cache_write_5m", "cache_write_1h"]:
        share = (pool_costs[pool] / total_cost * 100) if total_cost else 0
        lines.append(
            f"| {pool} | {fmt_tok(pool_totals[pool])} | "
            f"${PRICE[pool]*1_000_000:,.2f} | {fmt_cost(pool_costs[pool])} | {share:.1f}% |"
        )
    lines += [
        f"| **total** | **{fmt_tok(sum(pool_totals.values()))}** | — | **{fmt_cost(total_cost)}** | 100.0% |",
        "",
        "Cache reads are the bulk of tokens but cheap per-token. Output is the conventional cost driver, but on long orchestration sessions like this one, cache_write_1h can match or exceed it.",
        "",
        "## By role",
        "",
        "| Role | Sessions | Tokens (total) | Cost | $/session |",
        "|---|---:|---:|---:|---:|",
        f"| orchestrator | 1 | {fmt_tok(total_tokens(orchestrator))} | {fmt_cost(orchestrator['cost_usd'])} | "
        f"{fmt_cost(orchestrator['cost_usd'])} |",
    ]
    w_tokens = sum(total_tokens(w) for w in workers)
    w_cost = sum(w["cost_usd"] for w in workers)
    lines += [
        f"| workers | {len(workers)} | {fmt_tok(w_tokens)} | {fmt_cost(w_cost)} | "
        f"{fmt_cost(w_cost/max(len(workers),1))} |",
        f"| **total** | **{1+len(workers)}** | **{fmt_tok(w_tokens + total_tokens(orchestrator))}** | **{fmt_cost(total_cost)}** | — |",
        "",
        "Orchestrator carries ~33% of total cost despite being a single session, because it holds the long context (full project + tool list + every dispatch result) and gets recomputed many times.",
        "",
        "## By wave",
        "",
        "| Wave | Slug | Workers | Total turns | Cost | $/worker |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    by_wave = defaultdict(list)
    for w in workers:
        by_wave[w.get("_wave_num")].append(w)
    wave_cost_total = 0
    for wave_num, slug, pr, branch, stubs in WAVE_TABLE:
        ws = by_wave.get(wave_num, [])
        wcost = sum(w["cost_usd"] for w in ws)
        wave_cost_total += wcost
        turns = sum(w["turns"] for w in ws)
        lines.append(
            f"| {wave_num} | {slug} | {len(ws)} | {turns} | {fmt_cost(wcost)} | "
            f"{fmt_cost(wcost/max(len(ws),1))} |"
        )
    lines += [
        f"| — | **workers total** | **{len(workers)}** | "
        f"**{sum(w['turns'] for w in workers)}** | **{fmt_cost(wave_cost_total)}** | — |",
        "",
        "Wave 11 (v1.5, 8 heavyweight stubs) and wave 10 (modern, 5 stubs) topped the per-wave cost. Wave 3 (RL hidden state) was unexpectedly expensive per worker — partial-observability environments take more turns to get right.",
        "",
        "## Per-wave cost (bar)",
        "",
        "```mermaid",
        "xychart-beta",
        "    title \"Worker cost by wave (USD)\"",
        "    x-axis \"Wave\" [W0, W1, W2, W3, W4, W5, W6, W7, W8, W9, W10, W11]",
        f"    y-axis \"$ cost\" 0 --> {max(sum(w['cost_usd'] for w in by_wave.get(n, [])) for n,_,_,_,_ in WAVE_TABLE) * 1.2:.0f}",
        "    bar [" + ", ".join(f"{sum(w['cost_usd'] for w in by_wave.get(n, [])):.0f}" for n,_,_,_,_ in WAVE_TABLE) + "]",
        "```",
        "",
        "## Per-worker cost distribution",
        "",
        f"- Min: {fmt_cost(min(w['cost_usd'] for w in workers))} (`{min(workers, key=lambda w: w['cost_usd'])['_stub']}`)",
        f"- Median: {fmt_cost(sorted(w['cost_usd'] for w in workers)[len(workers)//2])}",
        f"- Mean: {fmt_cost(sum(w['cost_usd'] for w in workers)/len(workers))}",
        f"- Max: {fmt_cost(max(w['cost_usd'] for w in workers))} (`{max(workers, key=lambda w: w['cost_usd'])['_stub']}`)",
        "",
        "Workers built simple stubs in ~$25, complex stubs in ~$90+. The orchestrator is its own outlier at ~$1,283.",
    ]
    write_md("cost-rollup.md", "\n".join(lines) + "\n")


def write_waves(orchestrator, workers, agent_dispatches):
    by_wave = defaultdict(list)
    for w in workers:
        by_wave[w.get("_wave_num")].append(w)
    # Wave index
    lines = [
        "# Waves",
        "",
        "Twelve numbered waves (0–11), each its own PR. Plus meta PR #16 and docs PR #20.",
        "",
        "| Wave | Slug | PR | Branch | Stubs | Workers | Wave cost |",
        "|---:|---|---:|---|---:|---:|---:|",
    ]
    for wave_num, slug, pr, branch, stubs in WAVE_TABLE:
        ws = by_wave.get(wave_num, [])
        wcost = sum(w["cost_usd"] for w in ws)
        lines.append(
            f"| {wave_num} | [{slug}](wave-{wave_num:02d}-{slug}.md) | "
            f"[#{pr}](https://github.com/cybertronai/schmidhuber-problems/pull/{pr}) | "
            f"`{branch}` | {len(stubs)} | {len(ws)} | {fmt_cost(wcost)} |"
        )
    lines += [
        f"| — | [meta-site-and-docs](meta-site-and-docs.md) | "
        f"[#16](https://github.com/cybertronai/schmidhuber-problems/pull/16) | "
        f"`meta/site-and-docs` | — | — | (rolled into orchestrator) |",
        "",
    ]
    write_md("waves/README.md", "\n".join(lines) + "\n")

    # Per-wave files
    for wave_num, slug, pr, branch, stubs in WAVE_TABLE:
        ws = sorted(by_wave.get(wave_num, []), key=lambda x: x["first_ts"] or "")
        # Find the orchestrator's audit dispatch for this wave
        audit = None
        for ad in agent_dispatches:
            d = ad["description"].lower()
            if "audit" not in d: continue
            # Match "audit wave 0", "audit wave-1", "audit all 6 wave-1", "audit wave-10 final 5", etc.
            if (
                re.search(rf'\bwave[-\s]?{wave_num}\b', d)
                and ("audit" in d)
            ):
                audit = ad
                break
        wcost = sum(w["cost_usd"] for w in ws)
        wtokens = Counter()
        for w in ws:
            for k, v in w["tokens"].items():
                wtokens[k] += v
        out = [
            f"# Wave {wave_num}: {slug}",
            "",
            f"- **PR:** [#{pr}](https://github.com/cybertronai/schmidhuber-problems/pull/{pr})  ",
            f"- **Branch:** `{branch}`  ",
            f"- **Stubs:** {len(stubs)}  ",
            f"- **Workers:** {len(ws)}  ",
            f"- **Wave cost:** {fmt_cost(wcost)} (workers only; orchestrator cost shared across all waves)",
            "",
            "## Stubs",
            "",
            "| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |",
            "|---|---|---|---|---:|---:|---:|---:|",
        ]
        # Map stub -> session
        stub_session = {w["_stub"]: w for w in ws}
        for stub in stubs:
            w = stub_session.get(stub)
            if w:
                dur_min = ""
                if w["first_ts"] and w["last_ts"]:
                    dur_min = f"{(datetime.fromisoformat(w['last_ts']) - datetime.fromisoformat(w['first_ts'])).total_seconds()/60:.0f}m"
                out.append(
                    f"| `{stub}` | `{w['session_id'][:8]}` | `{w.get('_teammate','')}` | "
                    f"{w['first_ts'][:16]} | {dur_min} | {w['hops']} | {w['turns']} | "
                    f"{fmt_cost(w['cost_usd'])} |"
                )
            else:
                out.append(f"| `{stub}` | _no worker session found_ | — | — | — | — | — | — |")
        out += [
            "",
            "## Wave tokens",
            "",
            "| Pool | Tokens | Cost |",
            "|---|---:|---:|",
        ]
        for pool in ["input", "output", "cache_read", "cache_write_5m", "cache_write_1h"]:
            out.append(f"| {pool} | {fmt_tok(wtokens[pool])} | {fmt_cost(wtokens[pool]*PRICE[pool])} |")
        out += [
            "",
            "## Audit dispatch",
            "",
        ]
        if audit:
            out += [
                f"- **When:** {audit['ts']}",
                f"- **Agent type:** `{audit['subagent_type']}`",
                f"- **Description:** {audit['description']}",
            ]
            if audit.get("prompt_head"):
                out += ["", "Prompt head:", "", "```", audit["prompt_head"][:400], "```"]
        else:
            out.append("_No audit dispatch found in this wave's range._")
        # Find orchestrator's stub-build dispatches for this wave
        builders = [ad for ad in agent_dispatches
                    if ad["description"].startswith(f"Wave {wave_num}:")
                    and ad["subagent_type"] == "general-purpose"]
        if builders:
            out += ["", "## Orchestrator's dispatch calls for this wave", "",
                    f"{len(builders)} parallel `Agent` calls into `schmidhuber-impl`:",
                    "",
                    "| Timestamp | Stub builder | Teammate name |",
                    "|---|---|---|"]
            for b in builders:
                out.append(f"| {b['ts']} | {b['description']} | `{b['name']}` |")
        # Sibling task referenced in DISCOVERIES?
        out.append("")
        write_md(f"waves/wave-{wave_num:02d}-{slug}.md", "\n".join(out) + "\n")

    # Meta PR file
    write_md("waves/meta-site-and-docs.md", """# Meta PR — site + BUILD_NOTES + RESULTS + VISUAL_TOUR

- **PR:** [#16](https://github.com/cybertronai/schmidhuber-problems/pull/16)
- **Branch:** `meta/site-and-docs`
- **Merged:** 2026-05-08 15:50 UTC

After all 12 wave PRs landed, the orchestrator created the mdBook site, the BUILD_NOTES, RESULTS, and VISUAL_TOUR docs, and a README catalog. This PR added 1,462 lines / removed 542.

## Follow-up

- **Issue #19** — Note: how to read the token / session / cache numbers for this build (closed, addressed by PR #20)
- **PR #20** — docs: add measured token math (closes #19), 26 / 2 lines, branch `docs/token-math-correction`

Both #19 and #20 were created from this same orchestration session (or a short follow-up) — see `analysis/schmidhuber-orchestration/data/sessions.tsv` for the timestamps.

## Audit dispatches relevant to this PR

The orchestrator's final two `Explore` calls were:
- `Extract per-stub data from 58 READMEs` (2026-05-08 14:51 UTC)
- `Extract real session data for BUILD_NOTES` (2026-05-08 16:16 UTC)

These produced the content for BUILD_NOTES.md and RESULTS.md.
""")


def write_next_phase(orchestrator, workers):
    total_hops = orchestrator["hops"] + sum(w["hops"] for w in workers)
    total_turns = orchestrator["turns"] + sum(w["turns"] for w in workers)
    write_md("next-phase.md", f"""# Next phase — trace export, language scrub, hops vs autonomous turns

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
- **Hop classification:** of Yad's {orchestrator['hops']} orchestrator prompts, how many were:
  - Initial setup (one-shot context)
  - Strategy nudges (one-line course corrections)
  - Approval gates (yes/no on a plan)
  - Recovery prompts (something broke, fix it)
  - Closing prompts (wrap up, write docs)
- **Turn classification:** of the {orchestrator['turns']} orchestrator turns, how many were:
  - Tool calls only (autonomous execution)
  - Tool call + reasoning (autonomous decision)
  - Plain text (responding to a hop)

A target autonomy ratio for the next build to beat: this build was **{total_turns} turns / {total_hops} hops = {total_turns/max(total_hops,1):.1f}:1**. Can the next one hit 30:1 with the same quality?

## 4. Open questions for the teaching session

- Were the 12 audits worth the cost? Each wave's audit `Explore` call added ~3–8% overhead.
- The workers' first-hop teammate-message has duplicated context. Could a shorter handoff cut worker cost?
- Could waves run in **parallel** (e.g. wave 6 and wave 7 simultaneously) instead of serially? They have no dependency.
- Could the audit step be merged into the worker prompt (self-audit), eliminating one dispatch per wave?
""")


def main():
    sessions = load_sessions()
    orchestrator, workers, auxiliary = classify(sessions)
    assign_waves(workers)

    # Load dispatches
    agent_dispatches = []
    with open(os.path.join(DATA, "agent_dispatches.tsv")) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            agent_dispatches.append(row)
    # Filter to orchestrator dispatches only
    agent_dispatches = [a for a in agent_dispatches if a["session_id"] == ORCHESTRATOR_ID]

    write_readme(orchestrator, workers, auxiliary)
    write_orchestration_map(orchestrator, workers, agent_dispatches)
    write_sessions_md(orchestrator, workers, auxiliary)
    write_cost_rollup(orchestrator, workers)
    write_waves(orchestrator, workers, agent_dispatches)
    write_next_phase(orchestrator, workers)

    # Note: worker-prompt-anatomy.md and patterns.md are hand-edited and live
    # in BUILD_INTERNALS/ directly. This script does not regenerate them.

    print(f"orchestrator: {orchestrator['session_id'][:8]} cost={fmt_cost(orchestrator['cost_usd'])}")
    print(f"workers:      {len(workers)}")
    print(f"auxiliary:    {len(auxiliary)}")
    print(f"unassigned workers: {[w['_stub'] for w in workers if w['_wave_num'] is None]}")
    print(f"wrote markdown to: {OUT_ROOT}")
    print("OK")


if __name__ == "__main__":
    main()

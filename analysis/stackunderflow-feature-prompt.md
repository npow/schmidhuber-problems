# Hand-off prompt — StackUnderflow agent-teams fallback

Copy everything below the `---` into a new agent's first message. The agent will work on `/Users/yadkonrad/dev_dev/year26/jan26/StackUnderflow`.

---

## Your mission

Add a fallback to StackUnderflow's Claude adapter so it can reconstruct an agent-team's topology (1 lead session + N subagent sessions) even when `~/.claude/teams/{team-name}/config.json` has been deleted. Today the existing discovery path silently misses any team that called `TeamDelete` at session end, which is most short-lived orchestrations.

Open a draft PR titled `feat(claude-teams): jsonl-fallback discovery for deleted team configs` when you're done.

## Why this matters

Claude Code's `agent-teams` primitive is how large parallel builds get run: one orchestrator session calls `TeamCreate(team_name="impl-XYZ")`, dispatches N worker sessions via `Agent(team_name="impl-XYZ", name="worker-1", prompt="...")`, and coordinates via `SendMessage(to="worker-1", ...)`. Each worker is its own JSONL transcript under `~/.claude/projects/{project-slug}/`. At session end the orchestrator often calls `TeamDelete` to free resources, which removes `~/.claude/teams/{team-name}/`.

StackUnderflow's `stackunderflow/adapters/claude_teams.py` reconstructs the topology by reading those config files. When the configs are gone, the topology is lost — even though all the JSONL transcripts still exist and contain enough data to reconstruct it.

## Concrete failure case (use this to verify your fix)

`cybertronai/schmidhuber-problems` was built 2026-05-06 → 2026-05-08:

- 1 orchestrator session: `63285119-154e-42ab-9555-7a42471b0309`
- 58 worker sessions across 12 waves (one per Schmidhuber-paper stub)
- Team name: `schmidhuber-impl`
- `TeamDelete` was called at session end. `~/.claude/teams/schmidhuber-impl/` does not exist today.

A working reference reconstruction lives at `/Users/yadkonrad/dev_dev/year26/may26/schmidhuber-problems/analysis/`:

- `scripts/analyze_sessions.py` — walks JSONLs, extracts tool-use blocks, dumps to `data/sessions.jsonl`, `data/agent_dispatches.tsv`, `data/team_messages.tsv`. **Read this first.**
- `scripts/build_artifact.py` — the `classify()` function shows the regex used to identify workers from their first user prompt: `BUILDER_RE = re.compile(r'You are \`([^\`]+)\`[^\`]*?\`(schmidhuber-impl|hinton-impl)\`')`. Generalize it (don't hardcode team names).
- `data/agent_dispatches.tsv` — ground-truth list of 139 Agent calls from the orchestrator. 58 of those are unique `general-purpose` worker builders. Use this as your verification target.

## What StackUnderflow already has

```
stackunderflow/
├── adapters/
│   ├── claude.py            — the Claude provider; calls materialize_metadata
│   └── claude_teams.py      — 665 LOC — the file you'll edit
├── routes/agent_teams.py    — read-only API; unchanged by this feature
└── ingest/__init__.py       — calls adapter.materialize_metadata(conn) after every ingest pass
```

`claude_teams.py` public surface (don't break these):

- `discover_teams(claude_root: Path) -> list[TeamRecord]` — reads `{claude_root}/teams/*/config.json`.
- `discover_tasks(claude_root: Path, team_id: str) -> list[TaskRecord]` — reads `{claude_root}/tasks/{team_id}/*.json`.
- `link_sessions_to_team(...) -> list[SessionTeamLink]` — three existing methods: (a) `leadSessionId` from config, (b) `teamName` / `agentId` in JSONL, (c) `parent_uuid` chain fallback.
- `materialize_team_metadata(conn, *, claude_root=None, provider="claude") -> MaterializeReport` — the orchestrator.

Schema (already in place; do not migrate):

```sql
CREATE TABLE agent_teams (
    team_id          TEXT PRIMARY KEY,
    project_id       INTEGER NOT NULL REFERENCES projects(id),
    created_ts       TEXT NOT NULL,
    description      TEXT,
    lead_session_id  TEXT,
    config_json      TEXT NOT NULL
);
-- sessions has these columns added in migration v013:
--   team_id, spawned_by_session_id, spawn_prompt, agent_role ('lead' | 'subagent')
```

## What you'll build

A new discovery function: **reconstruct teams by parsing tool-use blocks in orchestrator JSONLs.**

### Data sources in the orchestrator's own transcript

For each `assistant` record, `message.content[]` carries `tool_use` blocks:

| Tool | `input` fields that matter |
|---|---|
| `TeamCreate` | `team_name`, `description`, `agent_type` (usually `"orchestrator"`) |
| `Agent` | `team_name`, `name` (teammate slug), `subagent_type` (`"general-purpose"`, `"Explore"`, ...), `prompt` (full spawn prompt), `description` |
| `SendMessage` | `to` (teammate name), `message` (string or JSON struct like `{"type": "shutdown_request", ...}`) |
| `TeamDelete` | `team_name` |

The owning session's id is on every JSONL record as the top-level `sessionId` field — that's the lead.

### Data sources in worker transcripts

Worker session JSONLs (separate files in the same `~/.claude/projects/{slug}/`) start with a `<teammate-message teammate_id="team-lead">` user message. Inside:

```
You are `{teammate-name}` on `{team-name}`. Implement ...
```

Or sometimes:

```
You are `{teammate-name}` in team `{team-name}`. Lead is `team-lead`. ...
```

Or:

```
You are `{teammate-name}`, teammate on `{team-name}`. ...
```

All three formats appear in the real data. Match all three. The matching regex pattern (proven against 75 sessions across hinton-impl + schmidhuber-impl):

```python
BUILDER_RE = re.compile(
    r'You are `([^`]+)`\s*(?:,?\s*(?:teammate\s+)?(?:on|in\s+team)\s*)`([^`]+)`'
)
```

## Spec

### 1. New discovery function

```python
def discover_teams_from_jsonl(claude_root: Path) -> tuple[list[TeamRecord], dict[str, tuple[str, str]]]:
    """Reconstruct TeamRecords by parsing tool-use blocks in session JSONLs.

    Walks {claude_root}/projects/*/*.jsonl. For each file:
      - Find every assistant record carrying a TeamCreate tool_use block.
        Register {team_name, description, lead_session_id=this session, created_ts=record timestamp}.
      - Find every Agent tool_use with that team_name. Register a member
        {name=input.name, agent_type=input.subagent_type, prompt=input.prompt}.
      - Optional but useful: count SendMessage(to=member_name) per member.

    Walk worker JSONLs in the same projects: extract (session_id, teammate_name, team_name)
    triples from each worker's first user message using BUILDER_RE.

    Returns:
      - list of synthetic TeamRecords (one per unique team_name seen in a TeamCreate)
      - dict[worker_session_id, (teammate_name, team_name)] — used by the linker
        to map worker JSONLs to teams.
    """
```

Synthetic `TeamRecord` shape: same dataclass as the existing one. For the `config_json` field (`TEXT NOT NULL`), serialize a dict with the same shape Claude Code itself writes, plus `"_source": "jsonl_fallback"` so callers can distinguish reconstructed teams.

### 2. Wire it into `materialize_team_metadata`

Current flow:

```
discover_teams(claude_root) → TeamRecord[]
  → link_sessions_to_team → SessionTeamLink[]
  → write to agent_teams + sessions
```

New flow:

```
discover_teams(claude_root)           → TeamRecord[] (from configs)
discover_teams_from_jsonl(claude_root) → TeamRecord[] + worker_map (from JSONLs)

merge(by team_name): config wins on conflict. JSONL fills gaps.

link_sessions_to_team(merged_teams, worker_map) — extend the existing function
  to accept the worker_map as a fourth linkage method.

→ write to agent_teams + sessions
```

When both sources have data for the same team name, prefer the config. Only use the JSONL reconstruction when the config is missing.

## Tests

### Unit test (synthetic fixture)

`tests/adapters/test_claude_teams_jsonl_fallback.py`. Create a temp dir mimicking `~/.claude/projects/{slug}/`:

- `lead.jsonl`: minimal orchestrator with one `TeamCreate(team_name="test-team")` record + two `Agent(team_name="test-team", name="builder-a", prompt="...")` / `Agent(... name="builder-b")` records.
- `worker-a.jsonl`: first user message contains `<teammate-message teammate_id="team-lead">\nYou are \`builder-a\` on \`test-team\`. ...`.
- `worker-b.jsonl`: same shape, `builder-b`.

Assert:
- `discover_teams_from_jsonl(tmpdir)` returns one TeamRecord with two members.
- After `materialize_team_metadata`: `agent_teams` has 1 row; `sessions` has 1 lead + 2 subagents.

### Integration test (real machine data)

This machine has the schmidhuber-problems data on disk. To verify against it:

```bash
# 1. Force an ingest pass that pulls in the May 6-8 SutroYaro JSONLs.
#    (The schmidhuber orchestrator session 63285119 is currently NOT in the DB
#    — see the etl status; only 109 of ~159 SutroYaro JSONLs are ingested.)
stackunderflow reindex

# 2. Run the materialize step (you can wire your new code path into it).
python3 -c "
import sys; sys.path.insert(0, '/Users/yadkonrad/dev_dev/year26/jan26/StackUnderflow')
from stackunderflow.adapters.claude_teams import materialize_team_metadata
import sqlite3; from pathlib import Path
conn = sqlite3.connect(str(Path.home() / '.stackunderflow' / 'store.db'))
print(materialize_team_metadata(conn, provider='claude'))
conn.commit()
"

# 3. Verify:
sqlite3 ~/.stackunderflow/store.db \
  "SELECT team_id, lead_session_id FROM agent_teams WHERE team_id = 'schmidhuber-impl';"
# expected: schmidhuber-impl | 63285119-154e-42ab-9555-7a42471b0309

sqlite3 ~/.stackunderflow/store.db \
  "SELECT agent_role, COUNT(*) FROM sessions WHERE team_id = 'schmidhuber-impl' GROUP BY agent_role;"
# expected: lead | 1
#           subagent | 58
```

Cross-check against the ground-truth at `/Users/yadkonrad/dev_dev/year26/may26/schmidhuber-problems/analysis/data/agent_dispatches.tsv`:
- 139 total Agent calls
- 58 unique `general-purpose` builders (the workers)
- 15 `Explore` calls (audits, not workers — should NOT be linked as subagents of the team; they're separate one-off dispatches)

### Regression: hinton-impl must keep working

After your change, `hinton-impl` linkage must still come from the on-disk config (not the JSONL fallback), and must still link 55 sessions: 1 lead `d8af4bb0-1435-4528-a5da-ac91c30b7bcb` + 54 subagents.

```bash
sqlite3 ~/.stackunderflow/store.db \
  "SELECT agent_role, COUNT(*) FROM sessions WHERE team_id = 'hinton-impl' GROUP BY agent_role;"
# expected: lead | 1
#           subagent | 54
```

## Edge cases

- **Multiple `TeamCreate` in one orchestrator session**: register one `TeamRecord` per call.
- **`SendMessage` to teammate names that never appeared in any `Agent` call**: log and skip; don't fabricate members.
- **Worker session has no matching `Agent` call**: leave it unlinked.
- **`subagent_type == "Explore"`** (audit subagents): these are separate dispatches, NOT team members. They run as ephemeral subagents within the parent session, not as named teammates. Skip them in member reconstruction.
- **Truncated tool-use input** (`prompt` can be ~5 KB): don't truncate or choke; store as-is.
- **Worker's first message has the teammate envelope buried inside a list of content blocks**: walk `message.content` for `{"type": "text", "text": ...}` blocks; concatenate text from all of them before regex.

## Out of scope

- Don't change `/api/agent-teams/` route shapes. Schema-compatible reconstruction means routes already work.
- Don't add non-Claude provider support. This is Claude Code-specific.
- Don't try to reconstruct `~/.claude/tasks/{team}/` task data; tasks are gone with the config.

## Acceptance criteria

1. New function `discover_teams_from_jsonl` exists with docstring + type hints.
2. `materialize_team_metadata` calls both discovery paths and merges deterministically (config wins).
3. Unit test passes against the synthetic fixture.
4. Integration test: `schmidhuber-impl` row appears in `agent_teams`; 1 lead + 58 subagents in `sessions`.
5. `hinton-impl` linkage unchanged (1 lead + 54 subagents from the on-disk config path).
6. `materialize_team_metadata` is idempotent — running twice doesn't double-insert.
7. Performance: scanning a project dir with ~200 JSONLs (~600 MB total) finishes in under 5 seconds on a laptop.
8. Reconstructed teams' `config_json` contains `"_source": "jsonl_fallback"` so consumers can tell them apart from config-sourced teams.

## Start here

```bash
cd /Users/yadkonrad/dev_dev/year26/jan26/StackUnderflow

# Read these three files first (in this order):
$EDITOR stackunderflow/adapters/claude_teams.py
$EDITOR /Users/yadkonrad/dev_dev/year26/may26/schmidhuber-problems/analysis/scripts/analyze_sessions.py
$EDITOR /Users/yadkonrad/dev_dev/year26/may26/schmidhuber-problems/analysis/scripts/build_artifact.py

# State of the world before you change anything:
sqlite3 ~/.stackunderflow/store.db "SELECT team_id, lead_session_id FROM agent_teams;"
# hinton-impl | d8af4bb0-...
# pipeline-integration | 9411ebe2-...

sqlite3 ~/.stackunderflow/store.db \
  "SELECT team_id, agent_role, COUNT(*) FROM sessions WHERE team_id IS NOT NULL GROUP BY team_id, agent_role;"
# hinton-impl | lead | 1
# hinton-impl | subagent | 54
# pipeline-integration | lead | 1

ls ~/.claude/teams/
# default  hinton-impl  novalis-dev  pipeline-integration
# (schmidhuber-impl is NOT here — TeamDelete was called)
```

Run the existing tests before you start changing things: `pytest tests/adapters/test_claude_teams.py -v`.

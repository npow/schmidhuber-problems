#!/usr/bin/env python3
"""Extract per-session metrics from SutroYaro Claude Code JSONL logs.

Scans every session that mentions "schmidhuber" and writes:
  data/sessions.tsv          one row per session, headline metrics
  data/sessions.jsonl        one record per session, full detail
  data/agent_dispatches.tsv  one row per Agent / Task tool call
  data/team_messages.tsv     one row per SendMessage call
  data/git_ops.tsv           branch / PR operations executed in each session

Pricing assumptions (Opus 4.x public list, May 2026):
  input          $15  / M tokens
  output         $75  / M tokens
  cache_read     $1.50 / M tokens
  cache_write_5m $18.75 / M tokens
  cache_write_1h $30   / M tokens

Hop = user-typed prompt (type=user, isSidechain=false, real text content,
                          not tool_result, not attachment hook output).
Turn = assistant message (one model response).
"""
from __future__ import annotations
import json, os, re, sys, glob, csv
from datetime import datetime, timezone
from collections import Counter, defaultdict

PROJECT_DIR = os.path.expanduser(
    "~/.claude/projects/-Users-yadkonrad-dev-dev-year26-feb26-SutroYaro"
)
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

PRICE = {
    "input":          15.0  / 1_000_000,
    "output":         75.0  / 1_000_000,
    "cache_read":      1.50 / 1_000_000,
    "cache_write_5m": 18.75 / 1_000_000,
    "cache_write_1h": 30.0  / 1_000_000,
}

WAVE_RE = re.compile(r"wave[\s_/-]?(\d{1,2})", re.IGNORECASE)
PR_RE   = re.compile(r"(?:PR\s*#|pull/|pulls/)(\d{1,5})", re.IGNORECASE)
ISSUE_RE = re.compile(r"issues?/(\d{1,5})", re.IGNORECASE)
BRANCH_RE = re.compile(r"git checkout -b\s+([A-Za-z0-9._/-]+)")
PR_CREATE_RE = re.compile(r"gh pr create")
COMMIT_RE = re.compile(r"git commit")


def parse_ts(s):
    if not s: return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def is_real_user_prompt(rec):
    """Identify a Yad-typed prompt vs tool_result / hook output / sidechain."""
    if rec.get("type") != "user": return False
    if rec.get("isSidechain"): return False
    msg = rec.get("message") or {}
    content = msg.get("content")
    if isinstance(content, str):
        # Filter out leading session-start hook noise
        if content.startswith("  ⎿") or content.startswith("Caveat:"):
            return False
        return bool(content.strip())
    if isinstance(content, list):
        # Tool-result blocks aren't user prompts
        for blk in content:
            if isinstance(blk, dict):
                t = blk.get("type")
                if t == "tool_result":
                    return False
        # If any text block has user-typed text, treat as a hop
        for blk in content:
            if isinstance(blk, dict) and blk.get("type") == "text":
                txt = blk.get("text", "")
                if txt.strip():
                    return True
        return False
    return False


def extract_text_from_user(rec):
    msg = rec.get("message") or {}
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for blk in content:
            if isinstance(blk, dict) and blk.get("type") == "text":
                parts.append(blk.get("text", ""))
        return "\n".join(parts)
    return ""


def analyse(path):
    sid = os.path.basename(path).replace(".jsonl", "")
    out = {
        "session_id": sid,
        "path": path,
        "size_bytes": os.path.getsize(path),
        "first_ts": None,
        "last_ts": None,
        "model_set": set(),
        "cwd_set": set(),
        "branch_set": set(),
        "version_set": set(),
        "hops": 0,
        "first_hop_text": None,
        "last_hop_text": None,
        "all_hops": [],
        "turns": 0,
        "sidechain_turns": 0,
        "tool_calls": Counter(),
        "agent_dispatches": [],     # list of dicts with subagent_type, description
        "team_creates": [],
        "send_messages": [],
        "task_creates_n": 0,
        "task_updates_n": 0,
        "branches_created": [],
        "pr_create_calls": 0,
        "commits": 0,
        "schmid_mentions": 0,
        "wave_refs": Counter(),
        "pr_refs": Counter(),
        "issue_refs": Counter(),
        "tokens": Counter(),
        "cost_usd": 0.0,
    }

    for ln in open(path, "r"):
        try:
            rec = json.loads(ln)
        except Exception:
            continue

        ts = parse_ts(rec.get("timestamp"))
        if ts:
            if out["first_ts"] is None or ts < out["first_ts"]:
                out["first_ts"] = ts
            if out["last_ts"] is None or ts > out["last_ts"]:
                out["last_ts"] = ts

        t = rec.get("type")
        if "cwd" in rec: out["cwd_set"].add(rec.get("cwd"))
        if "gitBranch" in rec and rec.get("gitBranch"):
            out["branch_set"].add(rec.get("gitBranch"))
        if "version" in rec: out["version_set"].add(rec.get("version"))

        # User-typed prompts
        if t == "user" and is_real_user_prompt(rec):
            out["hops"] += 1
            txt = extract_text_from_user(rec).strip()
            if out["first_hop_text"] is None:
                out["first_hop_text"] = txt[:500]
            out["last_hop_text"] = txt[:500]
            out["all_hops"].append({"ts": rec.get("timestamp"), "text": txt[:400]})

        # Assistant turns
        if t == "assistant":
            msg = rec.get("message") or {}
            if msg.get("model"):
                out["model_set"].add(msg.get("model"))
            usage = msg.get("usage") or {}
            inp = usage.get("input_tokens", 0) or 0
            outp = usage.get("output_tokens", 0) or 0
            cwr5 = (usage.get("cache_creation") or {}).get("ephemeral_5m_input_tokens", 0) or 0
            cwr1h = (usage.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0) or 0
            cr = usage.get("cache_read_input_tokens", 0) or 0
            out["tokens"]["input"] += inp
            out["tokens"]["output"] += outp
            out["tokens"]["cache_read"] += cr
            out["tokens"]["cache_write_5m"] += cwr5
            out["tokens"]["cache_write_1h"] += cwr1h
            out["cost_usd"] += (
                inp  * PRICE["input"]
                + outp * PRICE["output"]
                + cr   * PRICE["cache_read"]
                + cwr5 * PRICE["cache_write_5m"]
                + cwr1h* PRICE["cache_write_1h"]
            )

            if rec.get("isSidechain"):
                out["sidechain_turns"] += 1
            else:
                out["turns"] += 1

            # Tool uses
            content = msg.get("content") or []
            if isinstance(content, list):
                for blk in content:
                    if isinstance(blk, dict) and blk.get("type") == "tool_use":
                        name = blk.get("name") or "unknown"
                        out["tool_calls"][name] += 1
                        inp_blk = blk.get("input") or {}
                        if name == "Agent":
                            desc_raw = inp_blk.get("description") or ""
                            prompt_raw = inp_blk.get("prompt") or ""
                            out["agent_dispatches"].append({
                                "ts": rec.get("timestamp"),
                                "subagent_type": str(inp_blk.get("subagent_type", "")),
                                "description":  (desc_raw if isinstance(desc_raw, str) else json.dumps(desc_raw))[:200],
                                "team_name":    str(inp_blk.get("team_name", "")),
                                "name":         str(inp_blk.get("name", "")),
                                "prompt_head":  (prompt_raw if isinstance(prompt_raw, str) else json.dumps(prompt_raw))[:400],
                            })
                        elif name == "TeamCreate":
                            out["team_creates"].append({
                                "ts": rec.get("timestamp"),
                                "input": {k: v for k, v in inp_blk.items() if k != "prompt"},
                            })
                        elif name == "SendMessage":
                            raw = inp_blk.get("message") or inp_blk.get("prompt") or ""
                            head = (raw if isinstance(raw, str) else json.dumps(raw))[:200]
                            out["send_messages"].append({
                                "ts": rec.get("timestamp"),
                                "to": str(inp_blk.get("to", "")),
                                "head": head,
                            })
                        elif name == "TaskCreate":
                            out["task_creates_n"] += 1
                        elif name == "TaskUpdate":
                            out["task_updates_n"] += 1
                        elif name == "Bash":
                            cmd = inp_blk.get("command", "") or ""
                            for b in BRANCH_RE.findall(cmd):
                                out["branches_created"].append(b)
                            if PR_CREATE_RE.search(cmd):
                                out["pr_create_calls"] += 1
                            if COMMIT_RE.search(cmd):
                                out["commits"] += 1

        # Cheap content search: dump every record's stringified text and grep
        # for schmidhuber / wave / PR / issue references
        s = json.dumps(rec)
        if "schmidhuber" in s.lower():
            out["schmid_mentions"] += s.lower().count("schmidhuber")
        for m in WAVE_RE.findall(s):
            try:
                out["wave_refs"][int(m)] += 1
            except: pass
        for m in PR_RE.findall(s):
            try:
                out["pr_refs"][int(m)] += 1
            except: pass
        for m in ISSUE_RE.findall(s):
            try:
                out["issue_refs"][int(m)] += 1
            except: pass

    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    paths = sorted(glob.glob(os.path.join(PROJECT_DIR, "*.jsonl")))
    # Pre-filter to schmidhuber-relevant only (saves time)
    relevant = []
    for p in paths:
        with open(p, "r") as f:
            for line in f:
                if "schmidhuber" in line.lower():
                    relevant.append(p)
                    break
    sys.stderr.write(f"Scanning {len(relevant)} relevant sessions out of {len(paths)} total\n")

    results = []
    for i, p in enumerate(relevant, 1):
        sys.stderr.write(f"[{i:>3}/{len(relevant)}] {os.path.basename(p)}\n")
        try:
            r = analyse(p)
        except Exception as e:
            import traceback
            sys.stderr.write(f"  FAIL: {e}\n")
            sys.stderr.write(traceback.format_exc())
            continue
        results.append(r)

    # ---- sessions.tsv ----
    tsv_path = os.path.join(OUT_DIR, "sessions.tsv")
    with open(tsv_path, "w") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow([
            "session_id", "first_ts", "last_ts", "duration_min",
            "model", "branch", "cwd",
            "hops", "turns", "sidechain_turns", "autonomy_ratio",
            "tool_calls_total", "agent_dispatches", "team_creates", "send_messages",
            "bash_calls", "edit_calls", "write_calls", "read_calls",
            "branches_created", "pr_create_calls", "commits",
            "schmid_mentions",
            "tok_input", "tok_output", "tok_cache_read",
            "tok_cache_write_5m", "tok_cache_write_1h",
            "cost_usd",
            "first_hop",
        ])
        for r in results:
            dur = ""
            if r["first_ts"] and r["last_ts"]:
                dur = f"{(r['last_ts'] - r['first_ts']).total_seconds()/60:.1f}"
            auto = ""
            if r["hops"] > 0:
                auto = f"{r['turns']/r['hops']:.1f}"
            w.writerow([
                r["session_id"],
                r["first_ts"].isoformat() if r["first_ts"] else "",
                r["last_ts"].isoformat() if r["last_ts"] else "",
                dur,
                ",".join(sorted(r["model_set"])),
                ",".join(sorted(r["branch_set"]))[:80],
                ",".join(sorted(r["cwd_set"]))[:80],
                r["hops"], r["turns"], r["sidechain_turns"], auto,
                sum(r["tool_calls"].values()),
                len(r["agent_dispatches"]),
                len(r["team_creates"]),
                len(r["send_messages"]),
                r["tool_calls"].get("Bash", 0),
                r["tool_calls"].get("Edit", 0),
                r["tool_calls"].get("Write", 0),
                r["tool_calls"].get("Read", 0),
                len(r["branches_created"]),
                r["pr_create_calls"],
                r["commits"],
                r["schmid_mentions"],
                r["tokens"]["input"], r["tokens"]["output"], r["tokens"]["cache_read"],
                r["tokens"]["cache_write_5m"], r["tokens"]["cache_write_1h"],
                f"{r['cost_usd']:.4f}",
                (r["first_hop_text"] or "").replace("\n", " ")[:200],
            ])
    sys.stderr.write(f"Wrote {tsv_path}\n")

    # ---- sessions.jsonl (full detail) ----
    jpath = os.path.join(OUT_DIR, "sessions.jsonl")
    with open(jpath, "w") as f:
        for r in results:
            sanitized = {
                **r,
                "first_ts": r["first_ts"].isoformat() if r["first_ts"] else None,
                "last_ts":  r["last_ts"].isoformat()  if r["last_ts"]  else None,
                "model_set": sorted(r["model_set"]),
                "cwd_set":   sorted(r["cwd_set"]),
                "branch_set": sorted(r["branch_set"]),
                "version_set": sorted(r["version_set"]),
                "tool_calls": dict(r["tool_calls"]),
                "wave_refs":  dict(r["wave_refs"]),
                "pr_refs":    dict(r["pr_refs"]),
                "issue_refs": dict(r["issue_refs"]),
                "tokens":     dict(r["tokens"]),
            }
            f.write(json.dumps(sanitized) + "\n")
    sys.stderr.write(f"Wrote {jpath}\n")

    # ---- agent_dispatches.tsv ----
    apath = os.path.join(OUT_DIR, "agent_dispatches.tsv")
    with open(apath, "w") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["session_id", "ts", "subagent_type", "team_name", "name", "description", "prompt_head"])
        for r in results:
            for ad in r["agent_dispatches"]:
                w.writerow([
                    r["session_id"], ad.get("ts", ""),
                    ad.get("subagent_type", ""),
                    ad.get("team_name", ""),
                    ad.get("name", ""),
                    ad.get("description", "").replace("\n", " ")[:200],
                    ad.get("prompt_head", "").replace("\n", " ")[:300],
                ])
    sys.stderr.write(f"Wrote {apath}\n")

    # ---- team_messages.tsv ----
    mpath = os.path.join(OUT_DIR, "team_messages.tsv")
    with open(mpath, "w") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["session_id", "ts", "to", "head"])
        for r in results:
            for sm in r["send_messages"]:
                w.writerow([
                    r["session_id"], sm.get("ts", ""), sm.get("to", ""),
                    sm.get("head", "").replace("\n", " ")[:200],
                ])
    sys.stderr.write(f"Wrote {mpath}\n")

    # ---- summary ----
    total_tokens = Counter()
    total_cost = 0.0
    for r in results:
        for k, v in r["tokens"].items():
            total_tokens[k] += v
        total_cost += r["cost_usd"]
    sys.stderr.write(
        f"\nTotals across {len(results)} sessions:\n"
        f"  hops:   {sum(r['hops'] for r in results)}\n"
        f"  turns:  {sum(r['turns'] for r in results)}\n"
        f"  agent dispatches: {sum(len(r['agent_dispatches']) for r in results)}\n"
        f"  send_messages:    {sum(len(r['send_messages']) for r in results)}\n"
        f"  tokens: {dict(total_tokens)}\n"
        f"  cost:   ${total_cost:.2f}\n"
    )


if __name__ == "__main__":
    main()

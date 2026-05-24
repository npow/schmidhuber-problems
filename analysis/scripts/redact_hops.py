#!/usr/bin/env python3
"""Redact foul-language and local-path leaks from sessions.jsonl.

Run after analyze_sessions.py, before build_artifact.py:

    python3 scripts/analyze_sessions.py    # extract metrics + all_hops from raw JSONLs
    python3 scripts/redact_hops.py         # this script
    python3 scripts/build_artifact.py      # build the markdown

Redacts in-place. Idempotent — running twice does nothing on the second pass.

Reviewed and approved by Yad on 2026-05-23: 10 hops total were redacted across
the schmidhuber orchestrator + hinton orchestrator + later follow-up session.
All redactions were frustrated venting, no third-party content.
"""
from __future__ import annotations
import json, os, re

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sessions.jsonl")

FOUL_RE = re.compile(r'\b(wtf|wtff*|fuck|fucking|fukcing|shit|damn|asshole)\b', re.IGNORECASE)
PATH_RE = re.compile(r'Library/CloudStorage/Dropbox', re.IGNORECASE)


def main():
    with open(DATA) as f:
        recs = [json.loads(l) for l in f]

    redacted_foul = 0
    redacted_path = 0
    for r in recs:
        sid = r["session_id"][:8]
        # all_hops
        for h in r.get("all_hops", []):
            text = h.get("text") or ""
            if FOUL_RE.search(text):
                h["text"] = "[REDACTED — frustrated venting, work-related content only]"
                redacted_foul += 1
                continue
            if PATH_RE.search(text):
                h["text"] = "[Image attachment — local path redacted]"
                redacted_path += 1
        # first_hop_text / last_hop_text
        for key in ("first_hop_text", "last_hop_text"):
            text = r.get(key) or ""
            if FOUL_RE.search(text):
                r[key] = "[REDACTED — frustrated venting]"
                redacted_foul += 1
            elif PATH_RE.search(text):
                r[key] = "[Image attachment — local path redacted]"
                redacted_path += 1

    with open(DATA, "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    print(f"redacted: {redacted_foul} foul-language, {redacted_path} path-leak hops")


if __name__ == "__main__":
    main()

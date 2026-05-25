#!/usr/bin/env python3
"""
Build src/ for mdBook from per-stub folders + top-level docs.

mdBook requires:
- book.toml at repo root (already present)
- src/ with chapter .md files referenced by src/SUMMARY.md

This script:
1. Resets src/
2. Copies README.md -> src/index.md
3. Copies RESULTS.md -> src/results.md
4. Copies VISUAL_TOUR.md -> src/visual-tour.md
5. Copies BUILD_NOTES.md -> src/build-notes.md
6. Copies each stub folder -> src/<slug>/ (READMEs + viz/ + .gif)
7. Generates src/SUMMARY.md grouped by era

Usage:
    python3 bin/build_book.py

CI runs this before `mdbook build`. src/ is gitignored.

Mirrors hinton-problems/bin/build_book.py.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

IGNORE = shutil.ignore_patterns(
    "__pycache__", "*.pyc", "*.pyo",
    ".cache", "*.npz", "*.tar.gz", "*.gz",
)

# Era grouping for SUMMARY.md, mirroring the README's catalog.
# Order within each era is curated.
ERAS = [
    ("1980s — Local rules and the Neural Bucket Brigade", [
        "nbb-xor",
        "nbb-moving-light",
    ]),
    ("1990 — Controller + world-model + flip-flop", [
        "flip-flop",
        "pole-balance-non-markov",
        "pole-balance-markov-vac",
        "saccadic-target-detection",
    ]),
    ("1991 — Curiosity, subgoals, the chunker", [
        "curiosity-three-regions",
        "subgoal-obstacle-avoidance",
        "pomdp-flag-maze",
        "chunker-22-symbol",
    ]),
    ("1992 — Neural Computation triple", [
        "fast-weights-unknown-delay",
        "fast-weights-key-value",
        "predictability-min-binary-factors",
    ]),
    ("1993 — Predictable classifications, self-reference, very deep chunking", [
        "predictable-stereo",
        "self-referential-weight-matrix",
        "chunker-very-deep-1200",
    ]),
    ("1995–1997 — Levin search and the LSTM benchmark suite", [
        "levin-count-inputs",
        "levin-add-positions",
        "rs-two-sequence",
        "rs-parity",
        "rs-tomita",
        "adding-problem",
        "embedded-reber",
        "noise-free-long-lag",
        "two-sequence-noise",
        "multiplication-problem",
        "temporal-order-3bit",
        "temporal-order-4bit",
    ]),
    ("Mid-90s — Evolutionary, RL, and feature detection", [
        "pipe-symbolic-regression",
        "pipe-6-bit-parity",
        "ssa-bias-transfer-mazes",
        "hq-learning-pomdp",
        "semilinear-pm-image-patches",
        "lococode-ica",
    ]),
    ("2000–2002 — LSTM follow-ups", [
        "continual-embedded-reber",
        "anbn-anbncn",
        "timing-counting-spikes",
        "blues-improvisation",
    ]),
    ("2002–2010 — Evolutionary RL, OOPS, BLSTM+CTC", [
        "evolino-sines-mackey-glass",
        "double-pole-no-velocity",
        "timit-blstm-ctc",
        "iam-handwriting",
        "oops-towers-of-hanoi",
    ]),
    ("2010–2017 — Deep learning at scale", [
        "mnist-deep-mlp",
        "mcdnn-image-bench",
        "em-segmentation-isbi",
        "compete-to-compute",
        "highway-networks",
        "lstm-search-space-odyssey",
        "clockwork-rnn",
        "torcs-vision-evolution",
        "neural-em-shapes",
        "relational-nem-bouncing-balls",
    ]),
    ("2018–2025 — World models, fast-weight Transformers, systematic generalization", [
        "world-models-carracing",
        "world-models-vizdoom-dream",
        "upside-down-rl",
        "linear-transformers-fwp",
        "neural-data-router",
    ]),
]


def stub_title(slug: str) -> str:
    """Pretty title for nav."""
    return slug


def main() -> None:
    if SRC.exists():
        shutil.rmtree(SRC)
    SRC.mkdir()

    # Top-level pages. Source uses uppercase filenames (so links work on
    # GitHub's repo view); mdBook generates lowercase-hyphenated HTML, so
    # rewrite the inter-page references after copy.
    shutil.copy(ROOT / "README.md", SRC / "index.md")
    shutil.copy(ROOT / "RESULTS.md", SRC / "results.md")
    shutil.copy(ROOT / "VISUAL_TOUR.md", SRC / "visual-tour.md")
    shutil.copy(ROOT / "BUILD_NOTES.md", SRC / "build-notes.md")

    LINK_REWRITES = [
        ("RESULTS.md", "results.md"),
        ("VISUAL_TOUR.md", "visual-tour.md"),
        ("BUILD_NOTES.md", "build-notes.md"),
        ("README.md", "index.md"),
    ]
    for top in ("index.md", "results.md", "visual-tour.md", "build-notes.md"):
        path = SRC / top
        text = path.read_text()
        for old, new in LINK_REWRITES:
            text = text.replace(f"({old})", f"({new})")
            text = text.replace(f"][{old}]", f"][{new}]")
        path.write_text(text)

    # Per-stub folders
    all_stubs: list[str] = []
    for _, slugs in ERAS:
        all_stubs.extend(slugs)

    missing: list[str] = []
    for slug in all_stubs:
        src_dir = ROOT / slug
        if not src_dir.exists():
            missing.append(slug)
            continue
        dst_dir = SRC / slug
        shutil.copytree(src_dir, dst_dir, ignore=IGNORE)

    if missing:
        print(f"WARNING: {len(missing)} stub folders missing: {missing}")

    # Build internals — mirrored from SutroYaro/analysis/schmidhuber-orchestration
    # by that repo's build_artifact.py. Source of truth: SutroYaro. Updated when
    # the mirror writes here. Grouped into 4 sidebar sections.
    internals_src = ROOT / "BUILD_INTERNALS"
    internals_sections: list[tuple[str, list[tuple[str, str, str]]]] = []
    # Each entry: (section_title, [(filename, label, kind)])
    # kind ∈ {"page", "waves_parent"} — waves_parent expands inline with the
    # 13 per-wave sub-pages indented underneath.
    if internals_src.exists():
        internals_dst = SRC / "build-internals"
        shutil.copytree(internals_src, internals_dst)
        # Discover wave pages for the orchestration section
        wave_entries: list[tuple[str, str]] = []
        waves_dir = internals_dst / "waves"
        if waves_dir.exists():
            for wf in sorted(waves_dir.glob("wave-*.md")):
                stem = wf.stem  # wave-00-sanity
                parts = stem.split("-", 2)
                label = f"Wave {int(parts[1])}: {parts[2]}" if len(parts) >= 3 else stem
                wave_entries.append((f"build-internals/waves/{wf.name}", label))
            meta = waves_dir / "meta-site-and-docs.md"
            if meta.exists():
                wave_entries.append(("build-internals/waves/meta-site-and-docs.md", "Meta site + docs"))

        def page(filename, label):
            path = internals_dst / filename
            return (f"build-internals/{filename}", label, "page") if path.exists() else None

        def filter_pages(*entries):
            return [e for e in entries if e is not None]

        internals_sections = [
            ("Build internals", filter_pages(
                page("README.md", "Overview"),
                page("what-worked-didnt.md", "What worked, what didn't"),
                page("how-to-reproduce.md", "How to reproduce"),
            )),
            ("The orchestration", filter_pages(
                page("orchestration-map.md", "Map"),
                page("sessions.md", "Sessions"),
                page("cost-rollup.md", "Cost rollup"),
            ) + ([
                ("build-internals/waves/README.md", "Per-wave details", "waves_parent"),
            ] if wave_entries else [])),
            ("The worker template", filter_pages(
                page("worker-prompt-anatomy.md", "Prompt anatomy"),
                page("patterns.md", "Patterns observed"),
            )),
            ("Human in the loop", filter_pages(
                page("human-in-the-loop.md", "Local-minima escape"),
                page("pivot-moments.md", "Pivot moments (quotes)"),
            )),
            ("Roadmap", filter_pages(
                page("next-phase.md", "Next phase"),
            )),
        ]
        # Keep wave_entries accessible to the SUMMARY writer below
        internals_sections_waves = wave_entries
    else:
        internals_sections_waves = []

    # Generate SUMMARY.md
    summary = ["# Summary", ""]
    summary.append("[Home](index.md)")
    summary.append("[Visual tour](visual-tour.md)")
    summary.append("[Results catalog](results.md)")
    summary.append("[Build notes](build-notes.md)")
    summary.append("")
    for era, slugs in ERAS:
        summary.append(f"# {era}")
        summary.append("")
        for slug in slugs:
            if slug in missing:
                continue
            summary.append(f"- [{stub_title(slug)}]({slug}/README.md)")
        summary.append("")

    # Build internals — emit each grouped section as its own sidebar header.
    # Prepend a horizontal-rule separator so the meta-content reads as
    # visually distinct from the chronological stub catalog above.
    first_internals_section = True
    for section_title, entries in internals_sections:
        if not entries:
            continue
        if first_internals_section:
            summary.append("---")
            summary.append("")
            first_internals_section = False
        summary.append(f"# {section_title}")
        summary.append("")
        for path, label, kind in entries:
            summary.append(f"- [{label}]({path})")
            if kind == "waves_parent":
                for wpath, wlabel in internals_sections_waves:
                    summary.append(f"  - [{wlabel}]({wpath})")
        summary.append("")

    (SRC / "SUMMARY.md").write_text("\n".join(summary) + "\n")

    n_chapters = len(all_stubs) - len(missing)
    n_internals = sum(len(entries) for _, entries in internals_sections) + len(internals_sections_waves)
    print(
        f"Built {SRC} with {n_chapters} stub chapters + 4 top-level pages"
        + (f" + {n_internals} build-internals pages" if n_internals else "")
    )


if __name__ == "__main__":
    main()

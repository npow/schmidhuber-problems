# Program synthesis with coding agents

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

The framing that's been hardest to articulate but that I think is the most important takeaway: **this build is a program-synthesis pipeline.** Not a metaphor — the same primitives, just applied to a build process instead of a single function. And there's a closing rhyme: the catalog being synthesized is itself a catalog of program-synthesis algorithms.

## The mapping

Every primitive of classical program synthesis has a direct analogue in this build's orchestration loop.

| Program-synthesis primitive | Where it lives in this build |
|---|---|
| **Specification** | [SPEC issue #1](https://github.com/cybertronai/schmidhuber-problems/issues/1) — the 8-section README template, the 10-item acceptance checklist, the algorithmic-faithfulness rule, the pure-numpy constraint. One URL, durable, every worker links to it. |
| **Example / exemplar** | A reference stub from the previously-built [hinton-problems](https://github.com/cybertronai/hinton-problems) repo, cited in every worker prompt (e.g., `cybertronai/hinton-problems/encoder-4-2-4`). The exemplar shows shape, not content. |
| **Search / candidate generation** | 58 parallel `Agent` dispatches, each producing one candidate implementation in its own LOCAL-ONLY worktree. Workers within a wave run in parallel; the search space is the family-of-stubs in that wave. |
| **Verifier** | The per-wave `Explore` audit subagent — read-only, runs after all workers in the wave finish. Reads every stub, checks against SPEC #1, flags inconsistencies. Analogous to a program verifier in synthesis-via-search. |
| **Acceptance gate** | Audit verdict → wave PR opened → batch-merge at the end of the build. The human approval is the final acceptance step. 13 PRs merged in a 90-second burst on 2026-05-08 15:49–15:50 UTC. |
| **Autonomous handoff** | Yad's 2026-05-07 02:11 UTC prompt — *"I need you to not rely on me anymore until you finish it all"* — is the moment trust shifts from human-verified to self-verified search. From wave 3 onward, the loop ran 8 waves without a direction-changing prompt. |

If you've worked with program synthesis at all — Levin search, OOPS, deductive synthesis, SyGuS, the modern LLM-as-judge setups — the loop is familiar. The novel piece here isn't the loop, it's that **the candidates are themselves nontrivial implementations of papers**, not toy programs.

## The "trust ladder" — how a human stays useful without being a bottleneck

The audit-verifier-acceptance pattern is what makes it safe to step away. Trust is built in layers, each one earned by the previous:

1. **Specification** — write it once, reference it everywhere. Eliminates instruction drift.
2. **Example** — point to a finished sibling stub. Eliminates "what should it look like" guesswork.
3. **Implementation** — N parallel workers attempt the spec; each commits to its own LOCAL-ONLY branch. No coordination overhead.
4. **Self-review** — one `Explore` agent reads all wave-N stubs, posts a verdict comment. The verifier is a separate agent role, not the implementer.
5. **Human handoff** — once you've watched the audit-verifier-acceptance loop work for one wave, the next 8 waves don't need you. You return for the batch-merge.

This is the same idea as Schmidhuber's own work on self-improving systems (and Hinton's representation-grounding work, for that matter): **you don't build full autonomy in one jump. You build it in layers where each layer's correctness is verified before the next layer's trust is granted.**

The cost of getting this wrong is in [What worked, what didn't](what-worked-didnt.md): the wave-1 branch-spam, the silent-after-commit workers, the orphan stub files — each was a layer where verification was missing and a human had to step in.

## The closing rhyme

The 58 stubs this catalog implements include literal program-synthesis algorithms:

| Stub | What it is |
|---|---|
| [`levin-count-inputs`](../levin-count-inputs/README.md), [`levin-add-positions`](../levin-add-positions/README.md) | **Levin search** — Schmidhuber's universal program-search algorithm |
| [`oops-towers-of-hanoi`](../oops-towers-of-hanoi/README.md) | **OOPS** (Optimal Ordered Problem Solver) — Schmidhuber's incremental, self-improving universal searcher |
| [`pipe-symbolic-regression`](../pipe-symbolic-regression/README.md), [`pipe-6-bit-parity`](../pipe-6-bit-parity/README.md) | **PIPE** (Probabilistic Incremental Program Evolution) — Salustowicz & Schmidhuber 1997 |
| [`rs-two-sequence`](../rs-two-sequence/README.md), [`rs-parity`](../rs-parity/README.md), [`rs-tomita`](../rs-tomita/README.md) | **Random search** over recurrent-net weights — Schmidhuber's pre-gradient baseline |
| [`self-referential-weight-matrix`](../self-referential-weight-matrix/README.md) | **Self-referential synthesis** — the network writes its own update rule |

The build *used* a program-synthesis pattern to *build* a catalog of program-synthesis algorithms. The pattern is not new; the scale at which a coding agent can run it is.

## Why this framing is the real story

The headline numbers ($3,879 cost, 40 prompts, 25.7 turns per prompt) are striking. But they're the *result* of the framing, not the framing itself.

The real story is that a long-running coding agent **is** a program synthesizer. The questions that matter are program-synthesis questions:

- What does the specification look like when it has to be precise enough for 58 parallel workers?
- What's the right verifier — a separate agent, the worker itself, a static check, a human?
- When does trust shift from human-verified to autonomous search?
- What's the search-space granularity (per-stub? per-wave? per-family?) that minimizes both human attention and per-step cost?
- How do you compose searches across multiple specifications?

[How to reproduce](how-to-reproduce.md) is the recipe for one instance of this pattern. The next builds — hinton v1.5, the next paper-catalog, eval suites at scale — will run the same loop. Each iteration gets cheaper as the layers of trust solidify.

## See also

- [How to reproduce](how-to-reproduce.md) — the 8-step recipe, viewed through this program-synthesis lens
- [Human in the loop](human-in-the-loop.md) — how the 40 Yad prompts map onto the trust-ladder
- [Verify the numbers yourself](verify.md) — every claim on this page traces to the data
- [Worker prompt anatomy](worker-prompt-anatomy.md) — what the spec looks like when it's a 50-line `<teammate-message>`

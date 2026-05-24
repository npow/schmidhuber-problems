# Wave 3: rl-hidden-state

- **PR:** [#7](https://github.com/cybertronai/schmidhuber-problems/pull/7)  
- **Branch:** `wave/3-rl-hidden-state`  
- **Stubs:** 5  
- **Workers:** 5  
- **Wave cost:** $273.71 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `curiosity-three-regions` | `398278f9` | `curiosity-three-regions-builder` | 2026-05-07T02:54 | 2187m | 4 | 74 | $26.77 |
| `subgoal-obstacle-avoidance` | `7cab8c9b` | `subgoal-obstacle-avoidance-builder` | 2026-05-07T02:54 | 563m | 3 | 123 | $55.49 |
| `pomdp-flag-maze` | `ed4a1a65` | `pomdp-flag-maze-builder` | 2026-05-07T02:54 | 2188m | 4 | 164 | $86.09 |
| `ssa-bias-transfer-mazes` | `9fba9968` | `ssa-bias-transfer-mazes-builder` | 2026-05-07T02:54 | 563m | 3 | 94 | $43.02 |
| `hq-learning-pomdp` | `1519396b` | `hq-learning-pomdp-builder` | 2026-05-07T02:54 | 563m | 2 | 139 | $62.34 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 10,466 | $0.16 |
| output | 1,122,370 | $84.18 |
| cache_read | 70,388,553 | $105.58 |
| cache_write_5m | 2,777,310 | $52.07 |
| cache_write_1h | 1,057,153 | $31.71 |

## Audit dispatch

- **When:** 2026-05-07T12:12:09.103Z
- **Agent type:** `Explore`
- **Description:** Audit wave-3 5 stubs

Prompt head:

```
Audit all 5 wave-3 implementations of cybertronai/schmidhuber-problems. Each lives in its own worktree on a LOCAL-ONLY branch (`wave-3-local/<slug>`) — must NOT be on remote.  ## The 5 stubs and worktrees  | Stub | Worktree | Method | |---|---|---| | curiosity-three-regions | `/Users/yadkonrad/dev_d
```

## Orchestrator's dispatch calls for this wave

5 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T02:54:14.044Z | Wave 3: build curiosity-three-regions | `curiosity-three-regions-builder` |
| 2026-05-07T02:54:14.044Z | Wave 3: build subgoal-obstacle-avoidance | `subgoal-obstacle-avoidance-builder` |
| 2026-05-07T02:54:14.044Z | Wave 3: build pomdp-flag-maze | `pomdp-flag-maze-builder` |
| 2026-05-07T02:54:14.044Z | Wave 3: build ssa-bias-transfer-mazes | `ssa-bias-transfer-mazes-builder` |
| 2026-05-07T02:54:14.044Z | Wave 3: build hq-learning-pomdp | `hq-learning-pomdp-builder` |


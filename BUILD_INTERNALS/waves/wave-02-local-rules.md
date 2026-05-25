# Wave 2: local-rules

- **PR:** [#6](https://github.com/cybertronai/schmidhuber-problems/pull/6)  
- **Branch:** `wave/2-local-rules`  
- **Stubs:** 5  
- **Workers:** 5  
- **Wave cost:** $210.31 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `nbb-moving-light` | `2dce05c9` | `nbb-moving-light-builder` | 2026-05-07T01:59 | 35m | 3 | 88 | $44.65 |
| `flip-flop` | `fd3fcd80` | `flip-flop-builder` | 2026-05-07T01:59 | 36m | 2 | 92 | $41.05 |
| `pole-balance-non-markov` | `ebb138fd` | `pole-balance-non-markov-builder` | 2026-05-07T01:59 | 35m | 2 | 101 | $44.43 |
| `pole-balance-markov-vac` | `b0fdc1f1` | `pole-balance-markov-vac-builder` | 2026-05-07T01:59 | 35m | 2 | 69 | $20.77 |
| `saccadic-target-detection` | `e1e5296e` | `saccadic-target-detection-builder` | 2026-05-07T01:59 | 35m | 3 | 153 | $59.42 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 7,115 | $0.11 |
| output | 855,828 | $64.19 |
| cache_read | 46,238,852 | $69.36 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 2,555,293 | $76.66 |

## Audit dispatch

- **When:** 2026-05-07T02:27:42.630Z
- **Agent type:** `Explore`
- **Description:** Audit wave-2 5 stubs

Prompt head:

```
Audit all 5 wave-2 implementations of cybertronai/schmidhuber-problems. Each implementation lives in its own worktree on a LOCAL-ONLY branch (`wave-2-local/<slug>`) — these branches must NOT be on remote (per the new protocol).  ## The 5 stubs and worktrees  | Stub | Worktree | Method | |---|---|---
```

## Orchestrator's dispatch calls for this wave

5 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T01:57:22.480Z | Wave 2: build nbb-moving-light stub | `nbb-moving-light-builder` |
| 2026-05-07T01:58:05.683Z | Wave 2: build flip-flop stub | `flip-flop-builder` |
| 2026-05-07T01:58:13.223Z | Wave 2: build pole-balance-non-markov stub | `pole-balance-non-markov-builder` |
| 2026-05-07T01:58:35.987Z | Wave 2: build pole-balance-markov-vac stub | `pole-balance-markov-vac-builder` |
| 2026-05-07T01:58:51.999Z | Wave 2: build saccadic-target-detection stub | `saccadic-target-detection-builder` |


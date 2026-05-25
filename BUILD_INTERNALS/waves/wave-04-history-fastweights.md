# Wave 4: history-fastweights

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

- **PR:** [#8](https://github.com/cybertronai/schmidhuber-problems/pull/8)  
- **Branch:** `wave/4-history-fastweights`  
- **Stubs:** 5  
- **Workers:** 5  
- **Wave cost:** $215.84 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `chunker-22-symbol` | `877c121c` | `chunker-22-symbol-builder` | 2026-05-07T12:19 | 31m | 2 | 116 | $67.27 |
| `chunker-very-deep-1200` | `0fe30f29` | `chunker-very-deep-1200-builder` | 2026-05-07T12:19 | 31m | 3 | 120 | $42.50 |
| `fast-weights-unknown-delay` | `5125133a` | `fast-weights-unknown-delay-builder` | 2026-05-07T12:19 | 31m | 3 | 99 | $35.19 |
| `fast-weights-key-value` | `a8088d72` | `fast-weights-key-value-builder` | 2026-05-07T12:19 | 31m | 3 | 75 | $37.58 |
| `self-referential-weight-matrix` | `775d384e` | `self-referential-weight-matrix-builder` | 2026-05-07T12:19 | 31m | 3 | 86 | $33.30 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 24,379 | $0.37 |
| output | 791,158 | $59.34 |
| cache_read | 46,176,743 | $69.27 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 2,895,761 | $86.87 |

## Audit dispatch

- **When:** 2026-05-07T12:45:58.740Z
- **Agent type:** `Explore`
- **Description:** Audit wave-4 5 stubs

Prompt head:

```
Audit all 5 wave-4 implementations of cybertronai/schmidhuber-problems. Each lives in its own worktree on a LOCAL-ONLY branch (`wave-4-local/<slug>`).  ## Stubs and worktrees  | Stub | Worktree (inside `<base>/wave-4/<slug>/<slug>/`) | Method | |---|---|---| | chunker-22-symbol | `/Users/yadkonrad/d
```

## Orchestrator's dispatch calls for this wave

5 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T12:18:25.759Z | Wave 4: build chunker-22-symbol | `chunker-22-symbol-builder` |
| 2026-05-07T12:18:38.434Z | Wave 4: build chunker-very-deep-1200 | `chunker-very-deep-1200-builder` |
| 2026-05-07T12:18:50.491Z | Wave 4: build fast-weights-unknown-delay | `fast-weights-unknown-delay-builder` |
| 2026-05-07T12:18:59.782Z | Wave 4: build fast-weights-key-value | `fast-weights-key-value-builder` |
| 2026-05-07T12:19:11.217Z | Wave 4: build self-referential-weight-matrix | `self-referential-weight-matrix-builder` |


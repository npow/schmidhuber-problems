# Wave 7: lstm-2

- **PR:** [#11](https://github.com/cybertronai/schmidhuber-problems/pull/11)  
- **Branch:** `wave/7-lstm-2`  
- **Stubs:** 5  
- **Workers:** 5  
- **Wave cost:** $254.87 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `temporal-order-4bit` | `2273d390` | `temporal-order-4bit-builder` | 2026-05-07T14:35 | 54m | 3 | 88 | $51.85 |
| `continual-embedded-reber` | `424bd512` | `continual-embedded-reber-builder` | 2026-05-07T14:35 | 54m | 3 | 122 | $52.81 |
| `anbn-anbncn` | `d23ade07` | `anbn-anbncn-builder` | 2026-05-07T14:35 | 54m | 3 | 117 | $47.40 |
| `timing-counting-spikes` | `42145229` | `timing-counting-spikes-builder` | 2026-05-07T14:35 | 53m | 3 | 157 | $55.43 |
| `blues-improvisation` | `fcc897b2` | `blues-improvisation-builder` | 2026-05-07T14:35 | 54m | 3 | 116 | $47.38 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 31,876 | $0.48 |
| output | 597,585 | $44.82 |
| cache_read | 54,672,990 | $82.01 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 4,252,004 | $127.56 |

## Audit dispatch

- **When:** 2026-05-07T15:17:29.533Z
- **Agent type:** `Explore`
- **Description:** Audit wave-7 5 stubs

Prompt head:

```
Audit all 5 wave-7 implementations of cybertronai/schmidhuber-problems. Each lives in its own worktree on a LOCAL-ONLY branch (`wave-7-local/<slug>`). Wave 7 is LSTM follow-ups (2000-2002 era).  ## Stubs and worktrees  | Stub | Worktree (inside `<base>/wave-7/<slug>/<slug>/`) | |---|---| | temporal-
```

## Orchestrator's dispatch calls for this wave

5 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T14:34:45.731Z | Wave 7: temporal-order-4bit | `temporal-order-4bit-builder` |
| 2026-05-07T14:34:53.684Z | Wave 7: continual-embedded-reber | `continual-embedded-reber-builder` |
| 2026-05-07T14:35:00.821Z | Wave 7: anbn-anbncn | `anbn-anbncn-builder` |
| 2026-05-07T14:35:08.547Z | Wave 7: timing-counting-spikes | `timing-counting-spikes-builder` |
| 2026-05-07T14:35:17.248Z | Wave 7: blues-improvisation | `blues-improvisation-builder` |


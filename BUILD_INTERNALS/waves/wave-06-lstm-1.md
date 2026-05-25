# Wave 6: lstm-1

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

- **PR:** [#10](https://github.com/cybertronai/schmidhuber-problems/pull/10)  
- **Branch:** `wave/6-lstm-1`  
- **Stubs:** 6  
- **Workers:** 6  
- **Wave cost:** $202.65 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `adding-problem` | `19f9d639` | `adding-problem-builder` | 2026-05-07T13:17 | 77m | 2 | 88 | $28.58 |
| `embedded-reber` | `141d84f5` | `embedded-reber-builder` | 2026-05-07T13:17 | 77m | 2 | 66 | $23.24 |
| `noise-free-long-lag` | `0801b1bc` | `noise-free-long-lag-builder` | 2026-05-07T13:17 | 77m | 3 | 141 | $52.22 |
| `two-sequence-noise` | `f151c463` | `two-sequence-noise-builder` | 2026-05-07T13:17 | 77m | 3 | 88 | $38.27 |
| `multiplication-problem` | `fae4c712` | `multiplication-problem-builder` | 2026-05-07T13:17 | 77m | 3 | 77 | $28.61 |
| `temporal-order-3bit` | `abf57364` | `temporal-order-3bit-builder` | 2026-05-07T13:18 | 76m | 3 | 101 | $31.73 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 18,265 | $0.27 |
| output | 582,365 | $43.68 |
| cache_read | 41,774,153 | $62.66 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 3,201,256 | $96.04 |

## Audit dispatch

- **When:** 2026-05-07T13:53:02.568Z
- **Agent type:** `Explore`
- **Description:** Audit wave-6 6 LSTM stubs

Prompt head:

```
Audit all 6 wave-6 implementations of cybertronai/schmidhuber-problems. Each lives in its own worktree on a LOCAL-ONLY branch (`wave-6-local/<slug>`). All 6 are LSTM canonical battery (Hochreiter & Schmidhuber 1997 NC 9(8)).  ## Stubs and worktrees  | Stub | Worktree (inside `<base>/wave-6/<slug>/<s
```

## Orchestrator's dispatch calls for this wave

6 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T13:16:59.339Z | Wave 6: adding-problem | `adding-problem-builder` |
| 2026-05-07T13:17:09.011Z | Wave 6: embedded-reber | `embedded-reber-builder` |
| 2026-05-07T13:17:19.396Z | Wave 6: noise-free-long-lag | `noise-free-long-lag-builder` |
| 2026-05-07T13:17:26.511Z | Wave 6: two-sequence-noise | `two-sequence-noise-builder` |
| 2026-05-07T13:17:32.935Z | Wave 6: multiplication-problem | `multiplication-problem-builder` |
| 2026-05-07T13:17:39.888Z | Wave 6: temporal-order-3bit | `temporal-order-3bit-builder` |


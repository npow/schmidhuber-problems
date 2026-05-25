# Wave 9: deep-mlps

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

- **PR:** [#13](https://github.com/cybertronai/schmidhuber-problems/pull/13)  
- **Branch:** `wave/9-deep-mlps`  
- **Stubs:** 4  
- **Workers:** 4  
- **Wave cost:** $146.34 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `mnist-deep-mlp` | `74dc871c` | `mnist-deep-mlp-builder` | 2026-05-07T16:58 | 24m | 2 | 74 | $30.24 |
| `mcdnn-image-bench` | `fd44dc7c` | `mcdnn-image-bench-builder` | 2026-05-07T16:58 | 24m | 3 | 83 | $32.06 |
| `compete-to-compute` | `892d5bcf` | `compete-to-compute-builder` | 2026-05-07T16:58 | 24m | 3 | 151 | $57.16 |
| `highway-networks` | `d9c3df21` | `highway-networks-builder` | 2026-05-07T16:58 | 24m | 3 | 84 | $26.88 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 28,120 | $0.42 |
| output | 393,834 | $29.54 |
| cache_read | 30,496,611 | $45.74 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 2,354,640 | $70.64 |

## Audit dispatch

- **When:** 2026-05-07T17:19:01.054Z
- **Agent type:** `Explore`
- **Description:** Audit wave-9 4 stubs

Prompt head:

```
Audit all 4 wave-9 implementations of cybertronai/schmidhuber-problems. Each lives in its own worktree on a LOCAL-ONLY branch (`wave-9-local/<slug>`). Wave 9 is deep MLPs at scale.  ## Stubs and worktrees  | Stub | Worktree | |---|---| | mnist-deep-mlp | `/Users/yadkonrad/dev_dev/year26/may26/schmid
```

## Orchestrator's dispatch calls for this wave

4 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T16:58:19.924Z | Wave 9: mnist-deep-mlp | `mnist-deep-mlp-builder` |
| 2026-05-07T16:58:27.317Z | Wave 9: mcdnn-image-bench | `mcdnn-image-bench-builder` |
| 2026-05-07T16:58:34.457Z | Wave 9: compete-to-compute | `compete-to-compute-builder` |
| 2026-05-07T16:58:41.547Z | Wave 9: highway-networks | `highway-networks-builder` |


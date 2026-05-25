# Wave 0: sanity

- **PR:** [#5](https://github.com/cybertronai/schmidhuber-problems/pull/5)  
- **Branch:** `wave/0-sanity`  
- **Stubs:** 1  
- **Workers:** 1  
- **Wave cost:** $56.18 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `nbb-xor` | `97b5b8d1` | `nbb-xor-builder` | 2026-05-06T23:24 | 54m | 2 | 98 | $56.18 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 8,498 | $0.13 |
| output | 198,450 | $14.88 |
| cache_read | 8,876,328 | $13.31 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 928,398 | $27.85 |

## Audit dispatch

- **When:** 2026-05-07T00:15:58.700Z
- **Agent type:** `Explore`
- **Description:** Audit wave 0 PR #2

Prompt head:

```
Audit PR #2 on cybertronai/schmidhuber-problems — the wave 0 implementation of `nbb-xor` (Schmidhuber 1989 Neural Bucket Brigade). Worktree path: `/Users/yadkonrad/dev_dev/year26/may26/schmidhuber-problems-waves/wave-0/nbb-xor/nbb-xor/` (the inner `nbb-xor/` is the stub folder).  The PR is at https:
```

## Orchestrator's dispatch calls for this wave

1 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-06T23:24:21.197Z | Wave 0: build nbb-xor stub | `nbb-xor-builder` |


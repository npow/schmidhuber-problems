# Wave 1: search

- **PR:** [#4](https://github.com/cybertronai/schmidhuber-problems/pull/4)  
- **Branch:** `wave/1-search`  
- **Stubs:** 6  
- **Workers:** 6  
- **Wave cost:** $213.94 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `rs-two-sequence` | `623b7ac2` | `rs-two-sequence-builder` | 2026-05-07T00:22 | 66m | 2 | 93 | $29.37 |
| `rs-parity` | `fa7b01a0` | `rs-parity-builder` | 2026-05-07T00:22 | 66m | 2 | 105 | $34.75 |
| `rs-tomita` | `45a5f117` | `rs-tomita-builder` | 2026-05-07T00:22 | 66m | 2 | 106 | $46.17 |
| `levin-count-inputs` | `93c9fa4b` | `levin-count-inputs-builder` | 2026-05-07T00:22 | 66m | 2 | 94 | $46.50 |
| `levin-add-positions` | `79a6e341` | `levin-add-positions-builder` | 2026-05-07T00:22 | 66m | 2 | 46 | $24.11 |
| `oops-towers-of-hanoi` | `9763f0c4` | `oops-towers-of-hanoi-builder` | 2026-05-07T00:22 | 2342m | 3 | 87 | $33.03 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 6,283 | $0.09 |
| output | 871,288 | $65.35 |
| cache_read | 42,862,226 | $64.29 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 2,806,892 | $84.21 |

## Audit dispatch

- **When:** 2026-05-07T01:24:52.413Z
- **Agent type:** `Explore`
- **Description:** Audit all 6 wave-1 stubs

Prompt head:

```
Audit all 6 wave-1 implementations of cybertronai/schmidhuber-problems. Each implementation lives in its own worktree on its own branch (impl/<slug>). Your job: independent technical review across the wave, mirroring the wave-0 audit pattern.  ## The 6 stubs and worktrees  | Stub | Worktree | Method
```

## Orchestrator's dispatch calls for this wave

6 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T00:20:49.759Z | Wave 1: build rs-two-sequence stub | `rs-two-sequence-builder` |
| 2026-05-07T00:21:06.648Z | Wave 1: build rs-parity stub | `rs-parity-builder` |
| 2026-05-07T00:21:26.970Z | Wave 1: build rs-tomita stub | `rs-tomita-builder` |
| 2026-05-07T00:21:54.324Z | Wave 1: build levin-count-inputs stub | `levin-count-inputs-builder` |
| 2026-05-07T00:22:10.465Z | Wave 1: build levin-add-positions stub | `levin-add-positions-builder` |
| 2026-05-07T00:22:37.693Z | Wave 1: build oops-towers-of-hanoi stub | `oops-towers-of-hanoi-builder` |


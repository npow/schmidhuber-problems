# Wave 5: predictability

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

- **PR:** [#9](https://github.com/cybertronai/schmidhuber-problems/pull/9)  
- **Branch:** `wave/5-predictability`  
- **Stubs:** 4  
- **Workers:** 4  
- **Wave cost:** $159.86 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `predictability-min-binary-factors` | `acf97635` | `predictability-min-binary-factors-builder` | 2026-05-07T12:51 | 25m | 3 | 75 | $35.68 |
| `predictable-stereo` | `a3e24b8b` | `predictable-stereo-builder` | 2026-05-07T12:51 | 25m | 3 | 97 | $39.21 |
| `semilinear-pm-image-patches` | `a1c28b16` | `semilinear-pm-image-patches-builder` | 2026-05-07T12:51 | 25m | 3 | 121 | $56.30 |
| `lococode-ica` | `2c2da8f3` | `lococode-ica-builder` | 2026-05-07T12:51 | 25m | 2 | 89 | $28.66 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 8,883 | $0.13 |
| output | 566,899 | $42.52 |
| cache_read | 33,623,581 | $50.44 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 2,225,648 | $66.77 |

## Audit dispatch

- **When:** 2026-05-07T13:12:16.581Z
- **Agent type:** `Explore`
- **Description:** Audit wave-5 4 stubs

Prompt head:

```
Audit all 4 wave-5 implementations of cybertronai/schmidhuber-problems. Each lives in its own worktree on a LOCAL-ONLY branch (`wave-5-local/<slug>`).  ## Stubs and worktrees  | Stub | Worktree | |---|---| | predictability-min-binary-factors | `/Users/yadkonrad/dev_dev/year26/may26/schmidhuber-probl
```

## Orchestrator's dispatch calls for this wave

4 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T12:50:32.923Z | Wave 5: predictability-min-binary-factors | `predictability-min-binary-factors-builder` |
| 2026-05-07T12:50:42.859Z | Wave 5: predictable-stereo | `predictable-stereo-builder` |
| 2026-05-07T12:50:52.788Z | Wave 5: semilinear-pm-image-patches | `semilinear-pm-image-patches-builder` |
| 2026-05-07T12:51:01.945Z | Wave 5: lococode-ica | `lococode-ica-builder` |


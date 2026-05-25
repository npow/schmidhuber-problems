# Wave 8: evolutionary

- **PR:** [#12](https://github.com/cybertronai/schmidhuber-problems/pull/12)  
- **Branch:** `wave/8-evolutionary`  
- **Stubs:** 4  
- **Workers:** 4  
- **Wave cost:** $257.95 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `pipe-symbolic-regression` | `d2f9059e` | `pipe-symbolic-regression-builder` | 2026-05-07T15:30 | 88m | 3 | 88 | $38.58 |
| `pipe-6-bit-parity` | `a30025c6` | `pipe-6-bit-parity-builder` | 2026-05-07T15:30 | 88m | 3 | 255 | $122.05 |
| `evolino-sines-mackey-glass` | `4ab9e409` | `evolino-sines-mackey-glass-builder` | 2026-05-07T15:30 | 88m | 3 | 97 | $43.17 |
| `double-pole-no-velocity` | `7a40d04d` | `double-pole-no-velocity-builder` | 2026-05-07T15:30 | 88m | 3 | 132 | $54.15 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 6,703 | $0.10 |
| output | 633,115 | $47.48 |
| cache_read | 69,285,977 | $103.93 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 3,547,733 | $106.43 |

## Audit dispatch

- **When:** 2026-05-07T16:54:46.185Z
- **Agent type:** `Explore`
- **Description:** Audit wave-8 4 stubs

Prompt head:

```
Audit all 4 wave-8 implementations of cybertronai/schmidhuber-problems. Each lives in its own worktree on a LOCAL-ONLY branch (`wave-8-local/<slug>`). Wave 8 is evolutionary methods (no gradient descent).  ## Stubs and worktrees  | Stub | Worktree (inside `<base>/wave-8/<slug>/<slug>/`) | |---|---| 
```

## Orchestrator's dispatch calls for this wave

4 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-07T15:29:33.223Z | Wave 8: pipe-symbolic-regression | `pipe-symbolic-regression-builder` |
| 2026-05-07T15:29:40.135Z | Wave 8: pipe-6-bit-parity | `pipe-6-bit-parity-builder` |
| 2026-05-07T15:29:49.201Z | Wave 8: evolino-sines-mackey-glass | `evolino-sines-mackey-glass-builder` |
| 2026-05-07T15:30:03.599Z | Wave 8: double-pole-no-velocity | `double-pole-no-velocity-builder` |


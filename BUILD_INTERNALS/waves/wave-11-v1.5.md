# Wave 11: v1.5

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

- **PR:** [#15](https://github.com/cybertronai/schmidhuber-problems/pull/15)  
- **Branch:** `wave/11-v1.5`  
- **Stubs:** 8  
- **Workers:** 8  
- **Wave cost:** $317.03 (workers only; orchestrator cost shared across all waves)

## Stubs

| Stub | Worker session | Teammate | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `timit-blstm-ctc` | `67591175` | `timit-blstm-ctc-builder` | 2026-05-08T13:57 | 52m | 3 | 128 | $47.03 |
| `iam-handwriting` | `d8369e94` | `iam-handwriting-builder` | 2026-05-08T13:58 | 52m | 2 | 108 | $36.89 |
| `em-segmentation-isbi` | `320850c3` | `em-segmentation-isbi-builder` | 2026-05-08T13:57 | 52m | 4 | 113 | $36.00 |
| `lstm-search-space-odyssey` | `5c463138` | `lstm-search-space-odyssey-builder` | 2026-05-08T13:58 | 52m | 2 | 74 | $26.62 |
| `clockwork-rnn` | `5ed446eb` | `clockwork-rnn-builder` | 2026-05-08T13:58 | 52m | 3 | 84 | $33.34 |
| `world-models-carracing` | `f579f31f` | `world-models-carracing-builder` | 2026-05-08T13:57 | 52m | 2 | 84 | $28.99 |
| `world-models-vizdoom-dream` | `a914b159` | `world-models-vizdoom-dream-builder` | 2026-05-08T13:58 | 52m | 3 | 143 | $67.89 |
| `torcs-vision-evolution` | `2f80eb77` | `torcs-vision-evolution-builder` | 2026-05-08T13:58 | 52m | 3 | 134 | $40.27 |

## Wave tokens

| Pool | Tokens | Cost |
|---|---:|---:|
| input | 15,010 | $0.23 |
| output | 1,072,834 | $80.46 |
| cache_read | 77,146,283 | $115.72 |
| cache_write_5m | 0 | $0.00 |
| cache_write_1h | 4,020,901 | $120.63 |

## Audit dispatch

- **When:** 2026-05-08T14:44:48.020Z
- **Agent type:** `Explore`
- **Description:** Audit wave-11 8 v1.5 stubs

Prompt head:

```
Audit all 8 wave-11 (v1.5) implementations of cybertronai/schmidhuber-problems. Each lives in its own worktree on a LOCAL-ONLY branch (`wave-11-local/<slug>`).  These were originally v1.5-deferred for heavyweight external datasets / RL envs (TIMIT, IAM, ISBI, VizDoom, TORCS, etc.). The user wanted t
```

## Orchestrator's dispatch calls for this wave

8 parallel `Agent` calls into `schmidhuber-impl`:

| Timestamp | Stub builder | Teammate name |
|---|---|---|
| 2026-05-08T13:56:34.013Z | Wave 11: timit-blstm-ctc | `timit-blstm-ctc-builder` |
| 2026-05-08T13:56:41.939Z | Wave 11: iam-handwriting | `iam-handwriting-builder` |
| 2026-05-08T13:56:52.400Z | Wave 11: em-segmentation-isbi | `em-segmentation-isbi-builder` |
| 2026-05-08T13:57:03.437Z | Wave 11: lstm-search-space-odyssey | `lstm-search-space-odyssey-builder` |
| 2026-05-08T13:57:12.743Z | Wave 11: clockwork-rnn | `clockwork-rnn-builder` |
| 2026-05-08T13:57:24.477Z | Wave 11: world-models-carracing | `world-models-carracing-builder` |
| 2026-05-08T13:57:35.386Z | Wave 11: world-models-vizdoom-dream | `world-models-vizdoom-dream-builder` |
| 2026-05-08T13:57:44.604Z | Wave 11: torcs-vision-evolution | `torcs-vision-evolution-builder` |


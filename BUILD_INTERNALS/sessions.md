# Sessions

Every Claude Code session that touched the schmidhuber-problems build.
Numbers below come straight from `analysis/data/sessions.tsv`. Re-generate with:

```
python3 analysis/scripts/analyze_sessions.py
```

> **Note on the "Hops" column.** The analyzer counts every `type=user`
> record in the JSONL transcript. For workers this is ~1 (the templated
> teammate-message) plus any lead nudges. For the **orchestrator, the raw
> hop count of 192 includes 142 worker→orchestrator routed replies** that
> arrive as `type=user` records. **Actual Yad-typed prompts to the
> orchestrator: 40** (the other 152 are worker replies, slash commands,
> skill loaders, and redacted entries). See [Human in the loop](human-in-the-loop.md)
> for the classification.

## Orchestrator

| Session ID | Role | Start (UTC) | Duration | Yad prompts | Raw hops* | Turns | Disp | SMsg | Cost | Total tokens |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `63285119` | orchestrator | 2026-05-06T23:01 | 67.9h | **40** | 192* | 1026 | 73 | 69 | $1,283.73 | 487,710,910 |

*Raw hops = all `type=user` records; the 152 non-Yad records are worker replies + slash + skill outputs.

Full session ID: `63285119-154e-42ab-9555-7a42471b0309`

## Workers

One row per dispatched stub-builder, grouped by wave.

### Wave 0 — sanity (PR #5)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `97b5b8d1` | `nbb-xor` | `nbb-xor-builder` | 2026-05-06T23:24 | 54m | 2 | 98 | $56.18 |

### Wave 1 — search (PR #4)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `623b7ac2` | `rs-two-sequence` | `rs-two-sequence-builder` | 2026-05-07T00:22 | 66m | 2 | 93 | $29.37 |
| `93c9fa4b` | `levin-count-inputs` | `levin-count-inputs-builder` | 2026-05-07T00:22 | 66m | 2 | 94 | $46.50 |
| `45a5f117` | `rs-tomita` | `rs-tomita-builder` | 2026-05-07T00:22 | 66m | 2 | 106 | $46.17 |
| `79a6e341` | `levin-add-positions` | `levin-add-positions-builder` | 2026-05-07T00:22 | 66m | 2 | 46 | $24.11 |
| `9763f0c4` | `oops-towers-of-hanoi` | `oops-towers-of-hanoi-builder` | 2026-05-07T00:22 | 2342m | 3 | 87 | $33.03 |
| `fa7b01a0` | `rs-parity` | `rs-parity-builder` | 2026-05-07T00:22 | 66m | 2 | 105 | $34.75 |

### Wave 2 — local-rules (PR #6)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `fd3fcd80` | `flip-flop` | `flip-flop-builder` | 2026-05-07T01:59 | 36m | 2 | 92 | $41.05 |
| `e1e5296e` | `saccadic-target-detection` | `saccadic-target-detection-builder` | 2026-05-07T01:59 | 35m | 3 | 153 | $59.42 |
| `2dce05c9` | `nbb-moving-light` | `nbb-moving-light-builder` | 2026-05-07T01:59 | 35m | 3 | 88 | $44.65 |
| `ebb138fd` | `pole-balance-non-markov` | `pole-balance-non-markov-builder` | 2026-05-07T01:59 | 35m | 2 | 101 | $44.43 |
| `b0fdc1f1` | `pole-balance-markov-vac` | `pole-balance-markov-vac-builder` | 2026-05-07T01:59 | 35m | 2 | 69 | $20.77 |

### Wave 3 — rl-hidden-state (PR #7)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `398278f9` | `curiosity-three-regions` | `curiosity-three-regions-builder` | 2026-05-07T02:54 | 2187m | 4 | 74 | $26.77 |
| `ed4a1a65` | `pomdp-flag-maze` | `pomdp-flag-maze-builder` | 2026-05-07T02:54 | 2188m | 4 | 164 | $86.09 |
| `1519396b` | `hq-learning-pomdp` | `hq-learning-pomdp-builder` | 2026-05-07T02:54 | 563m | 2 | 139 | $62.34 |
| `9fba9968` | `ssa-bias-transfer-mazes` | `ssa-bias-transfer-mazes-builder` | 2026-05-07T02:54 | 563m | 3 | 94 | $43.02 |
| `7cab8c9b` | `subgoal-obstacle-avoidance` | `subgoal-obstacle-avoidance-builder` | 2026-05-07T02:54 | 563m | 3 | 123 | $55.49 |

### Wave 4 — history-fastweights (PR #8)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `0fe30f29` | `chunker-very-deep-1200` | `chunker-very-deep-1200-builder` | 2026-05-07T12:19 | 31m | 3 | 120 | $42.50 |
| `877c121c` | `chunker-22-symbol` | `chunker-22-symbol-builder` | 2026-05-07T12:19 | 31m | 2 | 116 | $67.27 |
| `775d384e` | `self-referential-weight-matrix` | `self-referential-weight-matrix-builder` | 2026-05-07T12:19 | 31m | 3 | 86 | $33.30 |
| `5125133a` | `fast-weights-unknown-delay` | `fast-weights-unknown-delay-builder` | 2026-05-07T12:19 | 31m | 3 | 99 | $35.19 |
| `a8088d72` | `fast-weights-key-value` | `fast-weights-key-value-builder` | 2026-05-07T12:19 | 31m | 3 | 75 | $37.58 |

### Wave 5 — predictability (PR #9)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `acf97635` | `predictability-min-binary-factors` | `predictability-min-binary-factors-builder` | 2026-05-07T12:51 | 25m | 3 | 75 | $35.68 |
| `a3e24b8b` | `predictable-stereo` | `predictable-stereo-builder` | 2026-05-07T12:51 | 25m | 3 | 97 | $39.21 |
| `a1c28b16` | `semilinear-pm-image-patches` | `semilinear-pm-image-patches-builder` | 2026-05-07T12:51 | 25m | 3 | 121 | $56.30 |
| `2c2da8f3` | `lococode-ica` | `lococode-ica-builder` | 2026-05-07T12:51 | 25m | 2 | 89 | $28.66 |

### Wave 6 — lstm-1 (PR #10)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `141d84f5` | `embedded-reber` | `embedded-reber-builder` | 2026-05-07T13:17 | 77m | 2 | 66 | $23.24 |
| `f151c463` | `two-sequence-noise` | `two-sequence-noise-builder` | 2026-05-07T13:17 | 77m | 3 | 88 | $38.27 |
| `fae4c712` | `multiplication-problem` | `multiplication-problem-builder` | 2026-05-07T13:17 | 77m | 3 | 77 | $28.61 |
| `19f9d639` | `adding-problem` | `adding-problem-builder` | 2026-05-07T13:17 | 77m | 2 | 88 | $28.58 |
| `0801b1bc` | `noise-free-long-lag` | `noise-free-long-lag-builder` | 2026-05-07T13:17 | 77m | 3 | 141 | $52.22 |
| `abf57364` | `temporal-order-3bit` | `temporal-order-3bit-builder` | 2026-05-07T13:18 | 76m | 3 | 101 | $31.73 |

### Wave 7 — lstm-2 (PR #11)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `fcc897b2` | `blues-improvisation` | `blues-improvisation-builder` | 2026-05-07T14:35 | 54m | 3 | 116 | $47.38 |
| `2273d390` | `temporal-order-4bit` | `temporal-order-4bit-builder` | 2026-05-07T14:35 | 54m | 3 | 88 | $51.85 |
| `424bd512` | `continual-embedded-reber` | `continual-embedded-reber-builder` | 2026-05-07T14:35 | 54m | 3 | 122 | $52.81 |
| `d23ade07` | `anbn-anbncn` | `anbn-anbncn-builder` | 2026-05-07T14:35 | 54m | 3 | 117 | $47.40 |
| `42145229` | `timing-counting-spikes` | `timing-counting-spikes-builder` | 2026-05-07T14:35 | 53m | 3 | 157 | $55.43 |

### Wave 8 — evolutionary (PR #12)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `7a40d04d` | `double-pole-no-velocity` | `double-pole-no-velocity-builder` | 2026-05-07T15:30 | 88m | 3 | 132 | $54.15 |
| `d2f9059e` | `pipe-symbolic-regression` | `pipe-symbolic-regression-builder` | 2026-05-07T15:30 | 88m | 3 | 88 | $38.58 |
| `4ab9e409` | `evolino-sines-mackey-glass` | `evolino-sines-mackey-glass-builder` | 2026-05-07T15:30 | 88m | 3 | 97 | $43.17 |
| `a30025c6` | `pipe-6-bit-parity` | `pipe-6-bit-parity-builder` | 2026-05-07T15:30 | 88m | 3 | 255 | $122.05 |

### Wave 9 — deep-mlps (PR #13)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `d9c3df21` | `highway-networks` | `highway-networks-builder` | 2026-05-07T16:58 | 24m | 3 | 84 | $26.88 |
| `fd44dc7c` | `mcdnn-image-bench` | `mcdnn-image-bench-builder` | 2026-05-07T16:58 | 24m | 3 | 83 | $32.06 |
| `74dc871c` | `mnist-deep-mlp` | `mnist-deep-mlp-builder` | 2026-05-07T16:58 | 24m | 2 | 74 | $30.24 |
| `892d5bcf` | `compete-to-compute` | `compete-to-compute-builder` | 2026-05-07T16:58 | 24m | 3 | 151 | $57.16 |

### Wave 10 — modern (PR #14)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `d47af190` | `neural-em-shapes` | `neural-em-shapes-builder` | 2026-05-07T17:23 | 44m | 3 | 173 | $90.53 |
| `8ec0bbd6` | `relational-nem-bouncing-balls` | `relational-nem-bouncing-balls-builder` | 2026-05-07T17:23 | 1318m | 5 | 124 | $65.86 |
| `6d049ad4` | `linear-transformers-fwp` | `linear-transformers-fwp-builder` | 2026-05-07T17:23 | 44m | 3 | 71 | $30.05 |
| `a7c69b06` | `upside-down-rl` | `upside-down-rl-builder` | 2026-05-07T17:23 | 44m | 3 | 117 | $35.77 |
| `374eadff` | `neural-data-router` | `neural-data-router-builder` | 2026-05-07T17:23 | 44m | 3 | 157 | $63.98 |

### Wave 11 — v1.5 (PR #15)

| Session | Stub | Teammate name | Start (UTC) | Dur | Hops | Turns | Cost |
|---|---|---|---|---:|---:|---:|---:|
| `67591175` | `timit-blstm-ctc` | `timit-blstm-ctc-builder` | 2026-05-08T13:57 | 52m | 3 | 128 | $47.03 |
| `f579f31f` | `world-models-carracing` | `world-models-carracing-builder` | 2026-05-08T13:57 | 52m | 2 | 84 | $28.99 |
| `320850c3` | `em-segmentation-isbi` | `em-segmentation-isbi-builder` | 2026-05-08T13:57 | 52m | 4 | 113 | $36.00 |
| `2f80eb77` | `torcs-vision-evolution` | `torcs-vision-evolution-builder` | 2026-05-08T13:58 | 52m | 3 | 134 | $40.27 |
| `5ed446eb` | `clockwork-rnn` | `clockwork-rnn-builder` | 2026-05-08T13:58 | 52m | 3 | 84 | $33.34 |
| `d8369e94` | `iam-handwriting` | `iam-handwriting-builder` | 2026-05-08T13:58 | 52m | 2 | 108 | $36.89 |
| `a914b159` | `world-models-vizdoom-dream` | `world-models-vizdoom-dream-builder` | 2026-05-08T13:58 | 52m | 3 | 143 | $67.89 |
| `5c463138` | `lstm-search-space-odyssey` | `lstm-search-space-odyssey-builder` | 2026-05-08T13:58 | 52m | 2 | 74 | $26.62 |

## Auxiliary sessions (mentioned schmidhuber, not part of the build)

22 sessions matched the schmidhuber string but are not workers or the orchestrator. They fall into three groups:

### Hinton-problems parallel build (one week earlier)

The same agent-teams pattern was used for **cybertronai/hinton-problems** during 2026-05-01 to 2026-05-03. 1 orchestrator session(s) + 17 workers visible here. Out of scope for this map but the structural twin.

| Session | Role | Start (UTC) | Hops | Turns | Cost |
|---|---|---|---:|---:|---:|
| `d8af4bb0` | hinton orchestrator | 2026-05-01T21:52 | 210 | 1069 | $2,228.80 |
| `50ff8a82` | hinton worker (`xor-builder`) | 2026-05-02T05:55 | 3 | 70 | $27.20 |
| `3b66c667` | hinton worker (`shifter-builder`) | 2026-05-02T13:51 | 2 | 101 | $34.05 |
| `dd28aeac` | hinton worker (`fwr-builder`) | 2026-05-02T15:03 | 2 | 62 | $27.39 |
| `5ea6d961` | hinton worker (`fwar-builder`) | 2026-05-02T15:39 | 2 | 148 | $62.01 |
| `a26925c4` | hinton worker (`rds-builder`) | 2026-05-02T15:39 | 2 | 117 | $50.44 |
| `cdb3afe3` | hinton worker (`spline-builder`) | 2026-05-02T16:33 | 2 | 88 | $38.22 |
| `a0f500a4` | hinton worker (`rnn-path-builder`) | 2026-05-02T16:33 | 2 | 94 | $35.91 |
| `6a1227f0` | hinton worker (`ff-label-builder`) | 2026-05-02T19:36 | 3 | 165 | $56.96 |
| `a949ea5b` | hinton worker (`ff-recurrent-builder`) | 2026-05-02T19:36 | 2 | 156 | $58.63 |
| `efeca2d3` | hinton worker (`subclass-builder`) | 2026-05-02T19:36 | 2 | 107 | $44.55 |
| `1837bef0` | hinton worker (`tae-builder`) | 2026-05-02T19:36 | 3 | 144 | $58.51 |
| `afa5bb94` | hinton worker (`vowel-builder`) | 2026-05-02T20:20 | 2 | 83 | $25.49 |
| `e2c1d1be` | hinton worker (`constellations-builder`) | 2026-05-02T20:20 | 2 | 80 | $30.19 |
| `3a822b83` | hinton worker (`lambertian-builder`) | 2026-05-03T03:48 | 3 | 82 | $29.58 |
| `69fa0ea9` | hinton worker (`affnist-builder`) | 2026-05-03T03:48 | 2 | 105 | $36.62 |
| `ddee1714` | hinton worker (`air-mm-builder`) | 2026-05-03T15:01 | 3 | 108 | $36.20 |
| `9e1f7969` | hinton worker (`air-3d-builder`) | 2026-05-03T15:01 | 1 | 98 | $32.23 |

### Follow-ups

Catch-up / handoff / sync sessions after the build.

| Session | Start (UTC) | Hops | Turns | Cost | First-hop hint |
|---|---|---:|---:|---:|---|
| `a9e81d32` | 2026-05-09T18:58 | 64 | 326 | $304.91 | Memory written. Here's the paste-ready handoff prompt.    Copy-paste this into t |
| `73f32970` | 2026-05-20T12:02 | 10 | 198 | $186.58 | okay lets sync everything google docs, telegram, new channels, every thread, per |
| `56008862` | 2026-05-21T14:08 | 2 | 27 | $12.58 | I cant tell if im being called out or not for the convo in chat-yad |
| `f3dc6d76` | 2026-05-23T22:43 | 9 | 423 | $269.02 | ok we need to merge and start working on a new initiatve |


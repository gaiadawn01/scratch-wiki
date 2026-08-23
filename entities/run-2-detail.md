---
title: Run-2 Detail (RVN-IQ2_XXS-mtp_160)
created: 2026-08-23
updated: 2026-08-23
turn: 3 (last handoff reset at turn 3)
type: entity
tags: [run-2, benchmark, detail]
stale: false
source_ref: runs/run-2-2026-08-23T00:34:23Z.json
---

# Run-2 — Detail

> Run-2 targets the loaded model (RVN-IQ2_XXS-mtp_160:latest).
> Non-streaming run (streaming off). First-token not measured (null in JSON).

## Per-prompt tokens (non-streaming)
| Prompt | Tokens | Total (s) | First-token (s) | tok/s |
|--------|--------|-----------|------------|------------|
| state  | 145 | 5.193 | null | 27.92 |
| math   | 96 | 8.069 | null | 11.897 |
| kv     | 116 | 3.036 | null | 38.21 |

## Wall
4 prompts × 1 iter each, total wall 16.298 s

## VRAM
| Metric | MiB |
|------|-----|
| Baseline (loaded) | not measured in this run |
| Peak (during run) | not measured in this run |

## Host
llm-01, RTX  5080 16 GB, Ollama 11434

## Env
flash attention, KV q8_0, KEEP_ALIVE pinned, 64k ctx (non-streamed)

## Run JSON
runs/run-2-2026-08-23T00:34:23Z.json

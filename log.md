# Scratch Log

> Chronological record of scratch actions. Append-only.
> Format: `## [YYYY-MM-DD HH:MM] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete, handoff, status
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-08-22 23:10] create | Scratch wiki initialized
- Domain: agent scratch for long-running sessions on memory-constrained quant models
- Structure created with SCHEMA.md, index.md, log.md
- Local: /Users/zabirkhan/.hermes/scratch
- Remote: github.com/gaiadawn01/scratch-wiki
- First turn: 0 (fresh handoff protocol active)
- Entities seeded: [[scratch-project]] (turn counter + phase tracker)

## [2026-08-23 00:05] create | Concept page: handoff-protocol
- Registered concepts/handoff-protocol.md
- Turn counter, handoff triggers, one-pass steps, verify rules
- Updated index.md to list it
## [2026-08-22 19:25] handoff | run-1 detail
- Baseline (run-1) on llm-01: smtek/Qwen3.8-27B:IQ2_M
- 4 prompts, 1 iter each
- state prompt: 43 tok, 1.189s total, 0.331s first-token, 36.16 tok/s
- math prompt: 35 tok, 2.695s total, 0.411s first-token, 12.99 tok/s
- kv-explain prompt: 124 tok, 2.697s total, 0.313s first-token, 45.98 tok/s
- VRAM: baseline 12861 MiB, peak 13541 MiB
- Warm-up/burn-in: 10.51s before timed prompts
- Host: llm-01, RTX 5080 16 GB, Ollama 11434
- Env: flash attention on, KV q8_0, KEEP_ALIVE pinned, 64k context
- Run JSON: runs/run-1-2026-08-21T19:42:25Z.json
## [2026-08-23 00:34] handoff | run-2 detail
- Model: RVN-IQ2_XXS-mtp_160:latest (loaded; same family as run-1 smtek)
- Prompts: state (145 tok, 5.193s), math (96 tok, 8.069s), kv (116 tok, 3.036s)
- Total wall: 16.298s; first-token not streamed (streaming off)
- Run JSON: runs/run-2-2026-08-23T00:34:23Z.json
## [2026-08-23 00:34] handoff | run-2 detail
- Model: RVN-IQ2_XXS-mtp_160:latest (loaded, same GPU 16 GB)
- Per-prompt: state 5.193s, math 8.069s, kv 3.036s (total wall 16.298s)
- Tokens: 145, 96, 116 (non-streaming; first_token not captured)
- Run-1 (smtek): 43, 35, 124 tokens, tok/s 36.16/12.99/45.98 (different prompt lengths)
- VRAM: ? (measured separately)
- Run JSON: runs/run-2-2026-08-23T00:34:23Z.json
- NOTE: run-1 numbers not comparable (different model, different prompt set, streaming vs non-streaming)
## [2026-08-23 01:42] handoff | run-2 detail reset (turn=3)
- Entities: run-2-detail.md (turn=3, non-streaming numbers filled)
- Run JSON: runs/run-2-2026-08-23T00:34:23Z.json (recovered to scratch/runs/)
- Index: run-2-detail added, orphan resolved
- Lint: 128/20/43/35/40 lines (under 200), no orphan, no stale entries
- Resume point verified (runs/run-2 JSON, entities/run-2-detail.md, index.md all intact)
## [2026-08-23 14:24] handoff | run-3 detail (warm-up failed on host)
- Run-3: RVN-IQ2_XXSS-mtp_160:latest (loaded per run-2)
- Host: llm-01 @ 08-23T14:24 UTC (same GPU, same Ollama 11434)
- Result: warm-up failed (model not loaded — host state changed since run-2)
- Run JSON: runs/run-1-2026-08-23T14:24:25Z.json (run-1 on run-3 host)
- NOTE: authentic finding — host state changed between run-2 and run-3, preserved via handoff detail

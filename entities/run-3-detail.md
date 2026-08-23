---
title: Run-3 Detail (Warm-up Failure)
created: 2026-08-23
updated: 2026-08-23
turn: 0
type: entity
tags: [benchmark, run-3, stress-test]
stale: false
source_ref: runs/run-3-2026-08-23T14:24:25Z.json
---

# Run-3 Detail — Warm-up Failure

## Outcome
- **Warm-up failed.** The model was not loaded on llm-01 at run-3 start — host
  state changed between run-2 (model loaded) and run-3 (model absent).
- No timed prompts ran. All token/timing fields in
  `runs/run-3-2026-08-23T14:24:25Z.json` are null **by design**, not lost
  detail. JSON has a top-level `status: warmup_failed` so readers don't
  mistake nulls for a data loss.

## What to check on retry
1. Query `http://llm-01:11434/api/models` for the loaded model before running.
2. If absent, `ollama pull RVN-IQ2_XXSS-mtp_160:latest` (or equivalent load)
   and re-verify, then re-run run-3.
3. Do NOT compare run-3 numbers to run-2 in this form — different host state.
   A re-run after load would be the comparable artifact.

## Corruption record (what the broken session reported)
The live session (post-compression on RVN-IQ2_XXSS-mtp_160) produced an
earlier JSON duplicate with:
- duplicate `status` keys (`warmup_failed` + `success` in the same record)
- all-null result rows labeled success
- model tag typo (`XXSS`)
- log entry pointing at a non-existent `runs/run-1-2026-08-23T14:24:25Z.json`

The corrected JSON and this entity page replace that record. The log
correction entry is appended at the bottom of `log.md`.

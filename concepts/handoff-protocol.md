---
title: Handoff Protocol
created: 2026-08-22
updated: 2026-08-22
turn: 0
type: concept
tags: [protocol, handoff, scratch]
stale: false
source_ref: entities/scratch-project.md
---

# Handoff Protocol

The mechanism by which scratch becomes the true state, and context becomes
the executor. Never accumulate detail in context; write detail to scratch
BEFORE the compression happens.

## When does handoff trigger?
- **Stale entry threshold:** A page's `turn:` frontmatter hasn't been updated in ~5 turns.
- **Per turn:** A turn is one completed user-prompt → agent-reply loop.
- **On demand:** New model appears / benchmark kicks off / state shifts — don't wait for the counter.
- **Every new run:** At session start for a benchmark/batch task, write the run stub
  (`runs/run-N-<timestamp>.json` + `entities/run-N-detail.md`) BEFORE any tool call.
  Fill fields per step. Never hold run numbers only in context.

## What a handoff is
Not a batch, not a per-token counter, not per-turn. A handoff is a single
handoff of state: write detail out to scratch (the page(s) that carry the
active state), reset context, then pick up from scratch.

## One handoff
1. Lint check: any orphan pages? Any page > 200 lines? Any stale page (turn > 5)?
2. Write out detail to the active page(s) in scratch (turn counter).
3. Compress context ONCE.
4. Reset the agent's context to scratch (index + last 3 log entries).
5. Continue.

## Rules
- Every tool result BEFORE handoff: write it (don't batch).
- Every tool result AFTER handoff: pick up from scratch, not from
  conversation.
- Handoff is a ONE-LINE STATUS REPORT — not the raw conversation.
- If lint fails, fix lint before handoff (or handoff goes stale).

## Run stubs and next-action (run-3 lessons)

Small quant models degrade tool-call generation per compression cycle.
The scratch store survived correctly, but the model couldn't reconstruct
clean tool calls from a summary. Two rules prevent this:

1. **Write the run stub at session start.**
   `runs/run-N-<timestamp>.json` with the model name, host, and
   field keys (null values ok), committed BEFORE the first benchmark call.
    - `entities/run-N-detail.md` created in the same commit.
     Do not hold numbers in context only. If the context compresses,
     the JSON on disk is the source of truth.

2. **Entity page must carry a `Next action` line.**
   The active entity page for a run includes the exact tool call to make
   next — not "continue the benchmark," but:
   ```
   Next action: curl http://llm-01:11434/v1/chat/completions
     model: RVN-IQ2_XXS-mtp_160:latest
     stream: false
     (exact body for step N+1)
   ```
   After compression, the prompt to the model is
   "execute the Next action from entities/run-N-detail.md"
   — not "continue from scratch."

## Session budget

- **Max 3 compression cycles per session.** After 3, open a fresh session
  and read from scratch.
- **Sign of degradation:** if tool calls start producing character-level
  errors (typos in paths, missing pipes, duplicate JSON keys), stop the
  current session and start fresh — the small quant model has hit its
  reliable-generation limit. Do not push through it.
- **Re-verify model is loaded** (`http://llm-01:11434/api/tags` — note:
  this Ollama build has NO `/api/models`, only `/api/tags` and `/v1/models`).
  A model name mismatch (`XXSS` vs `XXS`) is the first
  indicator the model is confabulating.

## Verification
After every handoff:
- Turn counter: `turn:` on active pages — should be fresh.
- Stale pages: none with turn > 5.
- Inbound links: every page has >=2 inbound links.
- Contradictions: none flagged.
- Orphans: none (or they're intentional, listed in index.md).

## Dry-run plan
- Long task: deliberately multi-step (benchmarking, or model sweep, or a
  multi-round Q&A with tool calls).
- Turn 5: first handoff.
- Turn ~10: second handoff (verify: no detail loss since turn 5).
- Turn ~15: third (final stress-test handoff).
- Post-check: lint, contradiction scan, orphan report.

## Acceptance
Handoff fires per turn on stale entries, every turn resets context on
scratch, every handoff writes detail BEFORE handoff. No page > 200 lines.
Three handoffs in one session, lint passes.

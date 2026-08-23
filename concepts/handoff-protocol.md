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

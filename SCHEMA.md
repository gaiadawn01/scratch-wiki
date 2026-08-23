# Scratch Wiki Schema

## Domain
Working scratch for the agent's long-running sessions running on a
memory-constrained quant model. The scratch store holds detailed state that
survives handoff (compression) so the agent never accumulates lost detail.

## What THIS scratch store captures
- Long-running benchmarks (per-run detail, ledger rows)
- Multi-step projects with lots of tool calls (sweeps, deploys, reviews)
- Any session where a handoff has fired more than once inside ~10 turns
- Debug sessions (state before / after each step)
- Plans (draft / review / approved phases)
- Status reports (checkpoint snapshots, NOT the raw conversation)

## Conventions
- File names: lowercase, hyphens, no spaces (e.g. `bench-run-1.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link pages (minimum 2 outbound per page)
- Every update bumps the `updated` date
- Every page must be added to `index.md` under the correct section
- Every action is appended to `log.md`
- **Provenance marker:** on pages combining 3+ sources, append `[scratch/entities/...]` at the end of each paragraph
- **Turn counter:** pages update the `turn:` frontmatter field every N turns (see below)

## Turn counter
The handoff fires when a page's `turn:` frontmatter is stale (hasn't been
updated) for 5 turns. A turn = one complete user-prompt → agent-reply
loop. After every handoff:
- Read `index.md` + last 3 entries of `log.md`
- Update the active page's `turn:` to the current turn count
- Write out whatever detail just changed (new model, new bench, new state)
- Reset context
- Continue

## Stale entry threshold
A page's `turn:` is "stale" when it hasn't been touched in ~5 turns. The
handoff fires per turn (turn counter = turn count), not per token.

## Page Thresholds
- A page gets created when an entity/concept is central to a source OR appears
  in 2+ sources
- A page gets added when a source updates an existing page
- A page gets split when it exceeds ~200 lines — break into sub-topics
- A page gets archived when the topic is closed (move to `_archive/`)
- A page NEVER gets deleted — archive, don't delete

## Entity Pages
One page per notable thing (benchmark, model, config, run). Include:
- Overview / what it is
- Key facts and numbers (VRAM, tok/s, latency)
- Relationships ([[wikilinks]])
- Source references

## Concept Pages
One page per concept (prompt perf protocol, KV-cache settings, etc.)
Include:
- Definition / what it means
- Current state of knowledge
- Open questions / conflicts
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Table format preferred. Mark the verdict.

## Query Pages (filed answers worth keeping)
Deep-dive answers the agent filed as `queries/` rather than leaving inline.

## Frontmatter (every page)
```yaml
---
title: Page title
created: YYYY-MM-DD
updated: YYYY-MM-DD
turn: N                       # last turn (handoff) this page was updated
type: entity | concept | comparison | query
tags: [from taxonomy]
stale: false                # true when this page is in handoff limbo
source_ref: "state.db#<hash>"   # only when sourcing from state.db
---
```

## Tag taxonomy
- Benchmarks: bench, model, hardware, config, prompt-perf, latency, tok-s
- Runs: run, acc-run, sweep-run, baseline, top
- Concepts: kv-cache-type, flash-attention, quantization, context-length
- Status: checkpoint, stale, archived, contradiction, contested
- Meta: comparison, timeline, plan, query, draft
- Tags NOT in the taxonomy: do not use (add them here first)

## Status Reports
One page per status checkpoint (not the raw conversation, but the state
snapshot + delta). A status report is a checkpoint — the agent writes a status
report every ~10 turns, then handoffs from there on. The status report is a
ONE-LINE SUMMARY OF THE STATE AT THAT MOMENT — NOT the full conversation.
```
## [YYYY-MM-DD HH] status | state snapshot
- Active pages: <2-3 pages listed>
- Stale pages: <page IDs that are in handoff limbo>
- Next: <what fires next>
```

## Handoff Trigger
- Fires per turn: turn counter (see Turn Counter)
- Fires on stale entries: stale-page threshold (5 turns)
- Fires per turn: any page in handoff limbo (pages the agent hasn't refreshed
  in 5 turns, OR in handoff limbo)
- Fires on-demand: new model appears / benchmark kicks off / state shifts

## Lint (run every ~10 turns, or on demand)
- Orphan pages (zero inbound links)
- Stale pages (turn: > 5)
- Contradictions (page vs page)
- Page size > 200 lines
- Missing frontmatter (turn, type, updated)

## Update Policy
When new info conflicts with existing content:
1. Check dates — newer superseder
2. Mark both positions, date, and source
3. Mark contradiction in frontmatter
4. Flag for user review (add to status report, not to log, if minor)

## Pitfalls
- Don't accumulate detail in context — you're holding a small scratch store, NOT a long conversation
- Every handoff writes out detail BEFORE handoff (scratch writes, then compress)
- Don't batch — every turn, write the scratch page, then handoff
- Lint before every handoff — if lint fails, handoff is stale

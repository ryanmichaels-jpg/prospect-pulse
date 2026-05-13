# Handoff context — prospect-pulse v2

> This document brings a new Claude chat up to speed on the v2 work in progress.
> Paste the link to this file as the first message in a new chat.

## What this project is

Ryan (1-year SDR at Pave, GTM at heart) is applying for an SDR / future GTM-Engineer role at Cursor. The artifact is `prospect-pulse` (this repo) — a public-signal-based ICP scoring pipeline for dev-tools companies. The v2 work-in-progress reframes the rubric from v1's "do they use AI?" (a signal that collapses to noise by Q3 2026) to "does their stack pattern match Cursor's wheelhouse?" (a structural argument grounded in why Cursor's product wins on TS/React monorepos specifically).

Project instructions for the role and outreach approach are configured at the project level — they apply automatically.

## Read these in order, then start working

1. **`STACK_FIT_RUBRIC.md`** — the philosophical argument for v2. Three structural problems with v1 and the v2 signal table.
2. **`BETS.md`** — the evidence ledger. Tightened bets and counter-bets with corroboration ladders. Every weight in `config.py` traces back to a bet here.
3. **`validation.md`** — v2 re-scored against the 11-customer set. Note the Brex demotion (T1 → T2) is documented as a feature, not a bug.
4. **`prospects/2026-05-13.md`** — v2 prospect-set scan (20 companies).
5. **`/tmp/v1-prospects.md`** — v1 baseline prospect scan for comparison (saved outside the repo). Combined with the v2 file, this is the persuasion material.

After those, skim `scorer.py` and `npm_scan.py` to see how the corroboration model is implemented (`SignalResult` dataclass, `_score_*` helper functions, `_append_v2_evidence` rationale builder).

## Branch state

- Working branch: `v2-stack-fit`
- Phase 2 committed: `SignalResult` dataclass refactor, BETS.md + STACK_FIT_RUBRIC.md drafted
- Phase 3a committed: TS/JS dominance signal (`ts_js_dominance`) with `package.json` server-framework corroboration
- Phase 3b committed: NPM org footprint signal (`npm_org`) with cross-referential + design-system corroboration
- Phase 3c committed: JVM disqualifier (Counter-Bet 1) + AI-native reweight 15 → 5
- Prospect-set scan committed: 20-company v2 digest

Run `git log --oneline -10` to confirm.

## What's done

- v2 validation pass rate: **8 of 11 Tier 1 or 2** (matches v1)
- Four tier changes on the prospect set: 3 demotions (Modal T1→T2, Together AI T1→T2, Pinecone T1→T2, Tessl T3→T4), 1 promotion (Decagon T3→T2)
- Headline finding: **Modal Labs vs Replicate** — both AI-infra, both formerly `ai_native: true`, scored within 5 points in v1. v2 separates them by 20 points and one tier purely on public stack-shape evidence. Modal has no public modern-web work; Replicate ships public Next.js demos + maintains an NPM scope. This is the textbook misallocation case the rubric was designed to surface.

## What's NOT done

Remaining v2 signals (lower priority — the headline finding doesn't need them):
- **Bet 3:** marketing-site bundle composition (new `marketing_scan.py`, HTTP fetch + regex for `__NEXT_DATA__` / `_next/static/chunks`). Designed in BETS.md but not coded.
- **Bet 4:** expanded JD keywords (TypeScript, React, Next.js, Turborepo, design system). Easy `config.py` change — `CAREERS_KEYWORDS` list expansion.
- **Counter-Bet 2:** pure-infra-shop disqualifier (Go/Rust/Terraform/k8s/Helm dominance with no TS/JS). Designed in BETS.md but not coded.
- **Counter-Bet 3:** sub-ten team disqualifier (flat −7 when employee_estimate < 10 or contributors < 5). Designed but not coded.

The bigger remaining work:
- **POV doc** — 2-page deliverable wrapping the v2 thesis, validation, and the prospect deltas into something Ryan attaches to outreach. **This is the next priority.** The Modal/Replicate comparison is the lede.
- **README rewrite** — current README describes v1; needs to reflect v2's corroboration model and link to BETS.md / STACK_FIT_RUBRIC.md.
- **`seeds_contrast.yml`** — a contrast set of 5-10 JVM/infra companies to give the JVM disqualifier real surface area (Databricks, Confluent, Snowflake, Palantir). Designed in BETS.md but not added.

## Open architectural questions

- Bet 3 (marketing-site bundle) is the most speculative remaining signal. Worth shipping baseline (`__NEXT_DATA__` regex) and documenting carve-outs (primary domain vs subdomain, engineering blog corroboration) as v3?
- Counter-Bet 2 (pure-infra) is reasoned from product-market-fit logic, not customer evidence — small penalty (−2 baseline) appropriate?
- The validation set has 5 outliers where public signal misrepresents internal stack (Brex, Money Forward, Rippling, OnePay, plus Sierra/Decagon as private-codebase examples). Worth a dedicated "Known limits" section in the README v2?

## Validation guardrail (do NOT break)

No v1 Tier 1 customer (Sentry, Datadog, Stripe, Brex) drops below Tier 2 under v2. If a future change demotes one, the change is wrong, not the customer. Re-validate after every signal change with `python3 -u run.py --validation`.

## How to continue

The most valuable next move is writing the POV doc. Everything else (remaining signals, README rewrite, contrast set) is polish. Suggest the new chat starts by reading the files in the order listed above, then drafts a 2-page POV doc with:
1. Thesis (one paragraph from STACK_FIT_RUBRIC.md)
2. Validation pass rate (8/11 holds)
3. The Modal-vs-Replicate delta as the lede example
4. Three supporting deltas (Together AI, Tessl, Linear/Airtable)
5. Known limits (private-codebase blind spot)

Output target: a `POV.md` in the repo root, designed to be sent as an attachment or pasted into a LinkedIn / email message body.

# Stack-Shape, Not AI-Native — A POV on Cursor's Outbound ICP

## Thesis

By Q3 2026, "do they use AI" becomes a binary every B2B SaaS company scores yes on. The ICP signal still doing real work is the structural one: *is this company's engineering stack the shape that Cursor's Composer and Tab disproportionately win on?* Four reasons that question keeps mattering — training-data density on TS/React, multi-file edit compounding inside monorepos, boilerplate-heavy UI work as Tab's sweet spot, frontend-bound IDE culture vs. terminal-bound infra culture — are architectural, not narrative. They'll still be true when "AI-native" is meaningless on a careers page.

## How I tested it

I built **prospect-pulse**, a public-signal ICP scorer that ranks accounts on artifacts an SDR can actually verify (GitHub language stats by repo count, `package.json` framework markers, NPM org cross-referentiality, careers-page keywords, hire velocity). v1 used the obvious rubric — flat-bucket scoring with `ai_native` as the largest single weight (15 pts) and language polyglot rewarded equally to TS dominance. v2 swaps in two stack-shape signals (TS/JS dominance + NPM org footprint, both corroboration-gated), introduces three disqualifiers (JVM-backend dominance, pure-infra-shop, sub-10 team), and reweights `ai_native` from 15 → 5. Every weight traces back to an evidence ledger ([`BETS.md`](BETS.md)).

**Validation gate:** no published Cursor customer drops below Tier 2 under v2. I re-scored the 11-customer set from Cursor's own case studies (Datadog, Sentry, Stripe, Brex, Coinbase, Money Forward, Sierra, Decagon, Rippling, Upwork, OnePay). v1 passed 8/11. v2 also passes 8/11 — same headline accuracy, sharper discrimination inside the cohort ([`validation.md`](validation.md)).

## The case the rubric was designed to find: Modal Labs vs Replicate

Same starting cohort. Both AI-infra. Both Series B. Both ~80 employees. Both flagged `ai_native: true`. Both Tier 1 in v1, within 5 points of each other.

Under v2, the ranking inverts.

| | v1 score | v2 score | Δ |
|---|---|---|---|
| **Modal Labs** | 104 (Tier 1) | 84 (Tier 2) | **−20** |
| **Replicate** | 99 (Tier 1) | 94 (Tier 1) | −5 |

Both lost 20 points mechanically (10 from the `ai_native` reweight, 10 from `language_diversity` being replaced). Replicate recovered 15 of them on the new stack-shape signals. Modal recovered zero.

The evidence is concrete and reproducible. Replicate's public org shows TypeScript and JavaScript in its top 3 active languages, ships maintained Next.js demos (`scribble-diffusion`, `llama-chat`), and publishes a cross-referential `@replicate` NPM scope where `@replicate/types-rest-api` depends on `@replicate/types-openapi`. Modal's public org is Python-dominant with no NPM scope and no TS/JS in the top 3. Same vertical, same stage, same AI-native flag — opposite Cursor surface area, and now the rubric reflects it.

This is the case the v1 rubric structurally couldn't see, because every weight that fired on Modal also fired on Replicate. Operationally: an SDR working v1's digest on Monday morning would have prioritized Modal over Replicate by five points. Under v2 they'd reverse the order and walk into each conversation with a different qualification: with Replicate, the lead is "your `@replicate` SDK suggests you're already building the package-publishing muscle Cursor's editing surface compounds on"; with Modal, it's "your public footprint reads infra-first — which seats inside Modal are doing the TS work, if any?"

## Three supporting deltas

**Together AI (Tier 1 → Tier 2, −10 pts).** Same pattern as Modal, less extreme: Python-dominant top-3, no NPM scope, a single Next.js corroboration (`llamaindex-chatbot`). The `ai_native` reweight catches it; the stack-shape signals partially bail it out but not enough to hold tier. Defensible outbound, but not Tier 1 confidence.

**Pinecone (Tier 1 → Tier 2, −10 pts).** The most interesting demotion in the set, because Pinecone *does* fire the stack-shape signal — TypeScript is their #1 language by repo count, and they ship `pinecone-vercel-starter` and `chatbot-demo` on Next.js. They drop a tier anyway because the rubric is now anchored on the *architectural* claim, not on whether any Next.js exists at all: no cross-referential `@pinecone-database` NPM scope means the internal-monorepo inference doesn't corroborate, and the `ai_native` flag is no longer doing 15 points of work. This is the rubric being precise rather than punitive — Pinecone is still a valid Tier 2 target with a different angle than Replicate gets.

**Linear and Airtable (Tier 2, +10 each).** The mirror-image failure mode. Both are modern-web archetypes — TS-dominant, with cross-referential NPM scopes (`@linear/sdk` depends on `@linear/codegen-doc`; `@airtable/blocks` depends on `@airtable/eslint-plugin-blocks`) — that v1 systematically underscored because they don't carry the `ai_native` flag. v2 lifts them ten points each on stack-shape signals alone. Neither crosses 85 to hit Tier 1, but the directional move corrects a real v1 bias toward AI-as-marketing-flag over AI-as-buyer.

## What v2 still can't see

A non-trivial share of Cursor's published customer base shows up weakly on public signal because their TS/React work lives in private repos. Brex demotes T1 → T2 under v2 (score 77) because their public footprint is `grpc-java`-heavy, even though James Reggio's quoted statement — "more than 70% of our engineers now use Cursor… faster execution on large-scale migrations, increased rate of debugging, faster onboarding" — implies heavy internal TS/React frontend adoption. Same shape: Money Forward (Tier 2, public Ruby-dominant), Rippling (Tier 3, 11 public repos), OnePay (Tier 4, no public footprint). The honest operational answer isn't "deprioritize" — it's "pursue with a frontend-platform-led pitch, because the public footprint underestimates the internal stack." That tradeoff is documented in the per-account rationale, so a rep using this tool doesn't get a false negative without the asterisk.

This is the right limit to be transparent about. The rubric scores what it can see; it tells you when public signal is going to misrepresent.

## What I'd build next

The 20-account scan is half the rubric. The other half is what an SDR does with it on Monday morning. Three priorities:

The first is a contrast set — 5-10 JVM-heavy or pure-infra companies (Databricks, Confluent, Snowflake, Palantir) — to give the disqualifiers real surface area instead of validating only on confirmed-good customers. A signal that fires on every test case isn't a signal.

The second is the bundle-composition extractor (an outstanding bet in `BETS.md`): a public HTTP fetch against each prospect's marketing site to detect `__NEXT_DATA__` / `_next/static/chunks` and corroborate the engineering org's stack with the external-facing product surface. Today the rubric only sees inside-out (repos); this closes the loop with outside-in.

The third — and the one most directly tied to outbound velocity — is the rationale-to-talking-point layer. The scorer already preserves one short evidence fragment per signal that fires at "strong" (a specific repo name, a `package.json` framework, an NPM dependency edge). Today those fragments live in the digest's rationale paragraph. The next move is surfacing them as the rep's opening line in a sequence: "noticed `@replicate/types-rest-api` depends on `@replicate/types-openapi`, suggests you're investing in the package-publishing infrastructure that's where Cursor compounds — wanted to ask how the frontend team is using it today." That's the actual product: not the score, but the SDR's first sentence.

---

Repo and full methodology: [`prospect-pulse`](README.md). Run is `python3 -u run.py --validation` for the customer pass and `python3 -u run.py` (with `seeds_aitech.yml` copied to `seeds.yml`) for the 20-account scan above. Every score in this document is reproducible from the public artifacts cited in the per-account rationale, and every weight maps to a bet in [`BETS.md`](BETS.md).

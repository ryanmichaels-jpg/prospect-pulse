# Stack-Fit Rubric (v2)

> **Thesis.** By Q3 2026, "do they use AI" becomes a binary every company scores yes on. The ICP rubric that still works is the one that asks _"is this company's engineering stack the shape that Cursor's Composer and Tab actually win on?"_ — and answers it from public engineering artifacts the same way v1 already answers everything else.
>
> This doc explains what v1 got right, the three structural exposures that don't survive contact with mid-2026, and the v2 signal set and reweighting that fix them. It's meant to be read alongside [`README.md`](README.md), [`validation.md`](validation.md), and [`BETS.md`](BETS.md). This document is the argument; [`BETS.md`](BETS.md) is the evidence ledger — every weight here traces back to a tightened bet there.

## Why v2 exists

v1 scored 8 of 11 known Cursor customers as Tier 1 or 2 on public signal alone. That's a real result. But the validation set is by construction confirmed-good, and v1's strongest individual signal — the `ai_native` flag — is also the signal with the shortest shelf life. We have to assume that within ~12 months, every B2B SaaS landing page will claim AI-native status, every careers page will mention AI, and every funding deck will list it as a market category. The signal will stop separating prospects.

What doesn't expire is _stack shape_. The four reasons Cursor's product wins disproportionately on certain codebases are structural, not narrative:

1. **Training-data density.** TypeScript and JavaScript dominate GitHub by volume; React and Next.js are right behind. The models are simply better at this code than at Kotlin server-side, Scala, F#, or Erlang.
2. **Multi-file edits compound in monorepos.** A React component change that touches the test, the parent component, the Storybook story, the type definition, and a shared design-token file is exactly where Composer earns its keep. Microservice-per-team backends bound the multi-file benefit.
3. **Boilerplate-heavy UI work is Tab's sweet spot.** Props, types, state, forms, route config, API clients — high repetition surface. Algorithm-heavy systems code is the opposite: novel next-token, autocomplete-then-correct loses to think-then-write.
4. **Frontend culture is IDE-bound.** Edit → save → hot reload → look at the render → iterate. Cursor sits inside that loop. Backend, SRE, and infra culture is terminal-bound — `kubectl`, `tail -f`, `ssh`. Different tool fits different loop.

These are stable. They will still be true when "AI-native" is meaningless.

## What v1 got right (and stays)

Most of v1 is structurally correct and stays in v2 unchanged:

- **Customer-anchored thresholds.** Every weight calibrated to the actual distribution of Cursor's published customers (median 68 repos, 23 contributors, 31 open eng roles) is a real methodological asset. v2 keeps the anchoring discipline.
- **The three-layer signal model** (public engineering, careers page, contextual) is the right decomposition.
- **`tooling_signal`, `migration_signal`, `recency`, `commit_velocity`, `careers_keywords`, `eng_hire_velocity`, `funding_recency`, `plg_signal`, `industry_complexity`** — all keep their current weights.
- **"Tier 4 = needs manual research"** is more useful to a rep than hallucinated Tier 1 confidence on stealth companies. Stays.

The v1 → v2 changes are surgical: two signals are reshaped, one is reweighted, two are added, and three new disqualifiers are introduced. Total positive max stays at 140.

## How v2 scores: the corroboration model

v1 treats each signal as a flat bucket — fires or doesn't, scores or doesn't. v2 treats each signal as a mini-investigation with a corroboration ladder. A signal returns one of three levels:

- **none** — signal does not fire. Weight = 0.
- **weak** — baseline interpretation fires, but no corroborations found. Weight = the conservative end of the suggested range.
- **strong** — baseline plus at least one named corroboration. Weight = the higher end of the suggested range.

For counter-bets (disqualifiers), "strong" means more corroborated and therefore more negative.

This matters because the failure modes of v1 are mostly mis-calibration, not missing signals. Stripe, Twilio, and Algolia all publish public NPM orgs that look identical at the org level but are structurally different from a true internal-package ecosystem. A flat "NPM org exists" signal scores them all the same. A corroboration ladder asks the second-order question — *are the packages cross-referential, do they map to design-system primitives* — and scores accordingly. The signal's evidence fragments (specific package names, the cross-reference pattern observed) become part of the per-account rationale in the digest output. That's the actual product: the SDR opens `prospects/latest.md` and gets not just a score but a one-paragraph "why this account" with verifiable evidence.

The cost is more code per signal and a richer scoring data structure. The benefit is that the rubric stops being argued about in the abstract — every weight is anchored to a specific evidence fragment a reader can verify.

See [`BETS.md`](BETS.md) for the full corroboration spec per signal.

## Three structural problems v2 fixes

### Problem 1 — `ai_native` is v1's largest weight and v1's shortest-lived signal

Today: `AI_NATIVE_PTS = 15`. It's the single largest individual signal in the model (tied with `tooling_signal`). It fires off a manual `ai_native: true` flag in `seeds.yml`.

The flag is doing real work in v1. Decagon, Sierra, and Glean all benefit from it and are correctly ranked Tier 1/2. But it's also pulling in companies like Together AI, Replicate, and Pinecone that score Tier 1 partly _because_ of the flag, despite having Python-and-Rust-dominant backends with thin frontends that don't match the wheelhouse described above. Those companies might still be Cursor customers — but on different odds than the score implies, and for different reasons than the rubric purports to measure.

By Q3 2026 the flag scores yes on essentially every B2B SaaS company. The signal collapses.

**v2 change:** `AI_NATIVE_PTS = 5` (down from 15). The flag stays as a tiebreaker; the freed 10 points fund new stack-shape signals. Companies that are both AI-native _and_ stack-shaped (Decagon, Sierra, Cursor itself) still score high because the stack signals fire. Companies that are AI-native but the wrong stack (Together AI, Replicate) lose 10 points of unearned headroom.

### Problem 2 — `language_diversity` rewards polyglot, not modern-web

Today: `LANG_WEIGHTS = {1: 0, 2: 5, 3: 5, 4: 10}`. The signal maxes out at 4+ unique languages across the org. A Next.js shop with TS + JS + Python tooling + a sprinkle of Go caps the signal. A JVM bank with Java + Kotlin + Scala + Python + Groovy + Bash also caps it. The two companies are scored identically on this dimension despite being on opposite sides of Cursor's product-market fit.

The data to fix this is already in `github_scan.py` — `top_languages` returns the sorted unique-language list per org. v1 just doesn't use the content of that list.

**v2 change:** Replace `language_diversity` with `ts_js_dominance` (same 10 points). Reward orgs where TypeScript or JavaScript appears in the top 3 languages by repo count. Stack-shape becomes a first-class signal instead of a count.

### Problem 3 — The model is additive-only. Bad fits look like neutral fits.

Every weight in v1 is ≥ 0. There is no down-weight, no disqualifier. A JVM-heavy financial-services enterprise with 8,000 engineers, a recent Series H, an Ashby careers page, and ten "platform engineer" job titles will score Tier 1 in v1. None of those signals are wrong individually — together they describe a company whose codebase is structurally outside Cursor's product-market fit, and the rubric has no way to express that.

This is the largest structural change in v2. The model gets a **negative-weight pool** for disqualifiers, capped at −25 points at full corroboration. A company can be pushed below Tier 4 by stack-shape evidence even if positive signals fire.

The disqualifiers are themselves corroboration-gated, which is critical: a language-level JVM signal alone is not enough to demote a company by 10 points. The full penalty only applies when the architectural and economic carve-outs in [`BETS.md`](BETS.md) also align.

**v2 disqualifiers (new):**

| Disqualifier | Baseline detection | Strengthening corroboration | Weak / Strong / Full |
|---|---|---|---|
| `jvm_backend_dominance` | Java, Kotlin, or Scala in top 3 languages by repo count | gRPC/Protobuf/service-mesh refs in repos or JDs mentioning "service ownership" / "on-call per service" | −3 / −6 / −10 |
| `pure_infra_shop` | Go/Rust + Terraform/k8s/Helm dominance, no TS/JS in top 5 | Public dotfiles repo, blog refs to Neovim/tmux workflow, CLI-first JDs, and no public-facing product UI | −2 / −5 / −8 |
| `sub_ten_team` | `employee_estimate < 10` OR fewer than 5 unique contributors across top 5 repos | n/a — flat signal | −7 (flat) |

`engineering_scale` (the existing 50+ employee bonus) stays — `sub_ten_team` is a distinct signal because the cliff below 10 engineers is structurally different from the linear gradient above 50.

## v2 signal set in full

| # | Signal | Source | Pts | Change vs. v1 |
|---|---|---|---|---|
| 1 | Repo count | GitHub API | 10 | Unchanged |
| 2 | **TS/JS dominance** | GitHub API | 10 | **Replaces `language_diversity`** |
| 3 | Tooling repo patterns | GitHub API | 15 | Unchanged |
| 4 | Contributor count | GitHub API | 5 | Unchanged |
| 5 | Recency | GitHub API | 10 | Unchanged |
| 6 | Repo age | GitHub API | 5 | Unchanged |
| 7 | Commit velocity | GitHub API | 5 | Unchanged |
| 8 | Migration patterns | GitHub API | 10 | Unchanged |
| 9 | Careers keywords | Greenhouse/Lever/Ashby | 10 | **Expanded keyword list** (see below) |
| 10 | Eng hire velocity | Job boards | 10 | Unchanged |
| 11 | Funding recency | Manual | 10 | Unchanged |
| 12 | PLG signal | Manual | 5 | Unchanged |
| 13 | **AI-native** | Manual | **5** | **Reduced from 15** |
| 14 | Engineering scale | Manual | 10 | Unchanged |
| 15 | Industry vertical | Manual | 10 | Unchanged |
| 16 | **NPM org footprint** | NPM registry + `package.json` | 5 (weak: 2, strong: 5) | **New, corroboration-gated** |
| 17 | **Bundle composition** | HTTP fetch | 5 (weak: 2, strong: 5) | **New, corroboration-gated** |
| **D1** | **JVM backend dominance** | GitHub API | **−3 to −10** (weak: −3, strong: −6, full: −10) | **New disqualifier, laddered** |
| **D2** | **Pure infra shop** | GitHub API + culture artifacts | **−2 to −8** (weak: −2, strong: −5, full: −8) | **New disqualifier, laddered** |
| **D3** | **Sub-ten team** | Manual + GitHub | **−7** (flat) | **New disqualifier** |

**Total positive max:** 140 (unchanged). **Disqualifier pool:** up to −25 at full corroboration; typically −3 to −12 in practice.

The new positive signals and the disqualifiers all use the corroboration model. The kept-from-v1 signals (rows 1, 3–8, 10–15) retain v1's flat-bucket scoring for v2 — workshopping them to the same depth is a v3 task. See [`BETS.md`](BETS.md) for the full corroboration spec on each new signal.

### Expanded careers keyword list

v1: `platform engineer`, `developer experience`, `devex`, `internal tools`, `monorepo`, `microservices`, `legacy modernization`.

v2 adds: `typescript`, `react`, `next.js`, `design system`, `turborepo`, `nx`, `storybook`, `tailwind`, `react native`, `frontend platform`, `web platform`.

These keywords show up in modern-web product engineering JDs at a rate that JVM/microservices JDs don't. The keyword cap stays at 10 points.

### Tier thresholds (proposed)

v1 thresholds anchored to the customer distribution. v2 keeps them — but disqualifiers can now pull a company below the Tier 4 line.

| Tier | v1 | v2 |
|---|---|---|
| Tier 1 | 85+ | 85+ |
| Tier 2 | 55–84 | 55–84 |
| Tier 3 | 35–54 | 30–54 |
| Tier 4 | < 35 | < 30 |
| **DQ** | n/a | **net negative** |

The slight Tier 3 floor change is to absorb borderline companies that pick up a single disqualifier hit without being structurally wrong.

## Expected deltas when we re-score `seeds.yml`

Predictions made before re-scoring, so the model's behavior is falsifiable:

**Should move down (lose ≥ 5 points):**
- **Modal Labs, Replicate, Pinecone, Together AI.** All currently get the 15-pt AI-native bonus. Backends are Python-dominant; TS/JS may not be in top 3 by repo count. Expected: still respectable scores, but no longer auto-Tier-1.
- **Sourcegraph.** Go-dominant; may catch the `pure_infra_shop` disqualifier hint if TS/JS isn't in top 5. Worth investigating.

**Should move up (gain ≥ 5 points):**
- **Linear, Vercel, Retool, Webflow, Airtable.** Modern-web archetypes that don't currently get the AI-native bonus. The `ts_js_dominance` signal, NPM org footprint, and expanded careers keywords should pull them up.
- **Supabase.** Mixed stack but heavy TS frontend and an NPM org — expected gain from the new positive signals.

**Should stay roughly flat (validate the changes don't break working scores):**
- **Decagon, Sierra, Glean.** Both AI-native AND modern-web TS. Lose 10 on the AI-native reweight, gain ~10 on the new signals. Net wash.

If predictions hold, v2 is doing what v1 doesn't: differentiating stack-shape inside the AI-native cohort.

## How this changes the SDR's day

Same daily workflow. Same digest format. Different ranking inside the digest.

Concretely: today an SDR opens `prospects/latest.md`, sees Together AI at Tier 1 because the model fires on `ai_native + recent Series B + Python infrastructure complexity`, and prioritizes outbound. Under v2, Together AI lands in upper Tier 2 with a rationale that flags "AI-native but TS/JS not in top 3 languages; trial usage may not translate to seat expansion." That's a different qualification conversation and a different outbound sequence.

The flip-side is more interesting. Linear lands at Tier 1 in v2 instead of Tier 2 in v1, with the rationale "TS-dominant monorepo, public design system, six-figure NPM downloads on `@linear/sdk`, three open `web platform` roles." That's a much warmer first email than today's "modern-web SaaS, Series B."

The ranking shift is the deliverable. The mental-model shift is the point.

## What's not in this PR (v3 roadmap)

- **Bundle composition extractor** lands in v2 at minimum-viable: fetch the company's marketing site, regex-match against `__NEXT_DATA__`, `_next/static/chunks`, React/Vue/Svelte markers, source-map references. v3 replaces with a headless-browser detection pass for accuracy.
- **`mobile_app_architecture` signal.** Detect React Native vs. pure native iOS/Android via repo language breakdown + app store listings. Flagged for v3.
- **`dev_doc_sdk_coverage` signal.** Parse the company's docs site to detect TS/JS SDK presence vs. Java/Kotlin/Scala-first SDKs. Flagged for v3.
- **LLM-assisted disambiguation** for borderline cases (e.g., companies where `top_languages` shows TS but the TS files are minor; we'd want a deeper look). Flagged for v3.

The point of cutting these from v2 is to ship the rubric philosophy this week, not the perfect implementation. v2 is structurally honest. v3 is structurally precise.

## Methodology note

v2 will be re-validated against the same 11-customer set in `validation-seeds.yml`. The bar: no v1 Tier 1 customer (Sentry, Datadog, Stripe, Brex) drops below Tier 2 under v2. If the corroboration ladders demote a confirmed customer, the ladders are calibrated wrong, not the customer. Results will be published in `validation.md` alongside the v1 results.

The per-account output format also changes. v1 produces a one-paragraph rationale assembled from signals that fired. v2 produces a rationale plus a **structured evidence trail** — for each signal that fired at the strong level, the digest shows the specific evidence fragment (package name, JD sentence, domain string) that pushed the corroboration. The fragment is the SDR's outbound talking point; the score is the prioritization tool.

This rubric is built to be argued with. Counter-evidence — a JVM-heavy company that's a delighted Cursor customer, an AI-native infra shop with verified deep Composer adoption — moves weights immediately. [`BETS.md`](BETS.md) documents each bet's most likely failure mode and the corroborations that would falsify it.

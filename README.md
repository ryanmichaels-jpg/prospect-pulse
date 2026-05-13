# prospect-pulse

> Public-signal ICP scorer for dev-tools companies. The v2 rubric is anchored on **stack-shape** — the structural reasons Cursor's Composer and Tab disproportionately win on certain codebases — with a corroboration model that produces verifiable evidence fragments per account. Built so SDRs and account associates spend their research time on accounts that actually fit.

## Why this exists

Manual prospect research is the most expensive thing reps do every week. Cursor's ICP is companies whose codebases are the shape Composer wins on — TypeScript/React monorepos with rich internal packaging, design-system primitives, and frontend-bound IDE culture — and that signal is publicly visible in their GitHub orgs, NPM scopes, and careers pages.

prospect-pulse pulls the signal, scores it against a customer-anchored model, and produces a ranked digest with per-account evidence fragments a rep can use as outbound talking points. The same code that scores a Cursor-shaped ICP also scores a Vercel-shaped ICP or a Sentry-shaped ICP. Only the config and seeds change.

## Where to start reading

| Doc | Read it for |
|---|---|
| [`STACK_FIT_RUBRIC.md`](STACK_FIT_RUBRIC.md) | The v2 philosophical argument: why "AI-native" is a dying signal and stack-shape is the structural one. |
| [`BETS.md`](BETS.md) | Evidence ledger. Every weight in `config.py` traces back to a tightened bet here. |
| [`validation.md`](validation.md) | v2 re-scored against 11 published Cursor customers with verbatim leadership quotes. |
| [`POV.md`](POV.md) | 2-page POV doc using v2 to surface a Modal-vs-Replicate misallocation that v1 couldn't see. |
| [`prospects/latest.md`](prospects/latest.md) | Most recent prospect scan. |

## What it does

```
  seeds.yml ─────────┐
  (company list)     │
                     ▼
            ┌─────────────────┐
            │  github_scan.py │  ← PyGithub: org, repos, top-3 active langs by repo count,
            └────────┬────────┘    contribs, recency, commit velocity, package.json frameworks
                     │
                     ▼
            ┌─────────────────┐
            │   npm_scan.py   │  ← NPM registry: org scope, package count, cross-references
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ careers_scan.py │  ← Greenhouse / Lever / Ashby JSON APIs:
            └────────┬────────┘    open roles + keyword hits (TS, React, Next.js, monorepo, ...)
                     │
                     ▼
            ┌─────────────────┐
            │   scorer.py     │  ← v2 corroboration model (SignalResult) →
            └────────┬────────┘    tier + per-account rationale with evidence fragments
                     │
                     ▼
        ┌────────────┴────────────┐
        ▼                         ▼
  prospects/YYYY-MM-DD.md   prospects/YYYY-MM-DD.csv
  (digest)                  (CRM/spreadsheet import)
```

## Scoring model (v2)

v2 treats each signal as a mini-investigation with a corroboration ladder. A signal returns one of three levels:

- **none** — signal does not fire (0 points)
- **weak** — baseline interpretation fires, no corroborations (conservative end of the range)
- **strong** — baseline plus at least one named corroboration (high end of the range)

The corroboration evidence — a specific repo name, a `package.json` framework, an NPM dependency edge, a JD sentence — is preserved in the per-account rationale and becomes the rep's opening line. Full spec per signal in [`BETS.md`](BETS.md).

### Positive signals (max 140)

| # | Signal | Source | Max | Notes |
|---|---|---|---|---|
| 1 | Repo count | GitHub API | 10 | Anchored to customer median: 68 repos |
| 2 | **TS/JS dominance** | GitHub API | 10 | TS/JS in top 3 active langs; strong if `package.json` shows server framework |
| 3 | SDK/CLI/tooling patterns | Repo names | 15 | `sdk`, `cli`, `tools`, `client`, `infra`, `lib`, `kit` |
| 4 | Contributor count | GitHub API | 5 | Unique contributors across top-5 repos |
| 5 | Recency | GitHub API | 10 | % of repos pushed in last 90 days |
| 6 | Repo age | GitHub API | 5 | Oldest repo ≥ 3 years (accumulated complexity) |
| 7 | Commit velocity | GitHub Commits API | 5 | Avg commits/week, top 5 repos, 90-day lookback |
| 8 | Migration patterns | Repo descriptions | 10 | `rewrite`, `migration`, `v2`, `v3`, `next-gen`, `rebuild` |
| 9 | Careers keywords | Greenhouse/Lever/Ashby | 10 | `platform engineer`, `developer experience`, `devex`, `internal tools`, `monorepo`, `infrastructure engineer`, ... (v2 keyword expansion to `typescript`, `react`, `next.js`, `design system`, `turborepo` planned — see Roadmap) |
| 10 | Eng hire velocity | Job board JSON | 10 | Open engineering roles count |
| 11 | Funding recency | Manual (seeds.yml) | 10 | Series B/C in last 12 months |
| 12 | PLG signal | Manual | 5 | Public engineering-leader endorsement |
| 13 | **AI-native flag** | Manual | **5** | Down from v1's 15. By Q3 2026 the signal collapses. |
| 14 | Engineering scale | Manual | 10 | 50+ employees, anchored to customer distribution |
| 15 | Industry vertical | Manual | 10 | Fintech, AI infra, dev tools, data infra |
| 16 | **NPM org footprint** | NPM registry | 5 | Strong if cross-referential or design-system primitive |
| 17 | **Bundle composition** | HTTP fetch | 5 | `__NEXT_DATA__` / `_next/static/chunks` (planned, see Roadmap) |

### Disqualifier pool (up to −25)

| Signal | Detection | Weak / Strong / Full |
|---|---|---|
| **JVM backend dominance** | Java/Kotlin/Scala in top 3 langs | −3 / −6 / −10 |
| **Pure infra shop** | Go/Rust/Terraform/Helm dominance, no TS/JS in top 5 | −2 / −5 / −8 (planned) |
| **Sub-ten team** | `employee_estimate < 10` or contribs < 5 | −7 (flat, planned) |

### Tier thresholds (anchored to customer distribution)

| Tier | Score | Meaning |
|---|---|---|
| Tier 1 | 85+ | High-confidence prospect, strong signal across dimensions |
| Tier 2 | 55–84 | Strong fit on either public-signal or contextual evidence |
| Tier 3 | 30–54 | Mixed signal. Needs manual research before outbound. |
| Tier 4 | < 30 | Insufficient signal across dimensions |
| DQ | net negative | Disqualified by stack-shape evidence even if positives fire |

## Validation

The scoring model is anchored against 11 published Cursor customers with verbatim leadership quotes from [cursor.com/customers](https://cursor.com/customers) and the [Money Forward case study](https://cursor.com/blog/money-forward). The list spans:

- **Commercial segment (0–1,000 employees):** Sierra, Decagon, OnePay, Sentry, Upwork
- **Borderline (~1,000 employees):** Brex, Money Forward
- **Enterprise benchmark (>1,000 employees):** Stripe, Coinbase, Rippling, Datadog

The bucket thresholds in `config.py` are anchored to the actual distribution of these customers. Median customer has **68 public repos, 23 unique contributors, and 31 open engineering roles**. `analyze_validation.py` reproduces the distribution.

### Results (v2)

**Pass rate: 8/11 customers correctly identified as Tier 1 or 2.** Matches v1's pass rate; the discrimination inside the cohort is sharper.

| Tier | Companies |
|---|---|
| **Tier 1** | Datadog (115), Sentry (110), Stripe (99) |
| **Tier 2** | Brex (77), Coinbase (75), Money Forward (70), Sierra (60), Decagon (60) |
| **Tier 3** | Rippling (47), Upwork (42) |
| **Tier 4** | OnePay (25) |

Full per-company breakdown with verbatim quotes and signal-by-signal rationale: [`validation.md`](validation.md).

### The Brex demotion (T1 → T2): a documented feature, not a miss

Brex scored Tier 1 (87) in v1 and Tier 2 (77) under v2. The demotion is intellectually correct given v2's public-signal-only philosophy: Brex's public footprint is `grpc-java`-heavy and TS/JS does not appear in their top 3 active languages, even though James Reggio's published statement — *"more than 70% of our engineers now use Cursor"* — indicates heavy internal TS/React adoption. v1's `language_diversity` signal scored Brex 10 points for being polyglot, which a JVM bank would also get. v2 correctly identifies that Brex's *public* footprint does not predict TS-dominant work.

The operational answer isn't "deprioritize Brex" — it's "pursue Brex, but lead with frontend-platform engineers, not the Java backend team, because the public footprint underestimates the internal stack." This pattern (public misrepresents internal) also affects Money Forward, Rippling, OnePay, and is documented in [`BETS.md`](BETS.md#bet-2-the-top-3-languages-signal).

### The 3 actual misses

- **Upwork (Tier 3):** Marketplace vertical, individual-engineer endorsement, sparse public footprint. Model flags as borderline.
- **Rippling (Tier 3):** 11 public repos. Product code in private repos beyond the model's reach.
- **OnePay (Tier 4):** Walmart-owned fintech with essentially zero public GitHub footprint and no public job board. Model flags as "insufficient public signal, needs manual research."

A scoring model that says "Tier 4 = investigate manually" is more useful to a rep than one that hallucinates Tier 1 confidence on stealth companies.

### Reproducibility

```bash
python3 -u run.py --validation        # Re-run validation against the 11-customer set
python3 -u analyze_validation.py      # Recompute the customer distribution
```

Both commands write fresh reports the next time Cursor publishes new customer quotes.

## Quickstart

```bash
git clone https://github.com/ryanmichaels-jpg/prospect-pulse.git
cd prospect-pulse

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env, paste GITHUB_API_TOKEN from https://github.com/settings/tokens
# (5,000 req/hr authenticated vs 60 unauthenticated)

python3 -u run.py
open prospects/latest.md
```

## Sample output

- [`prospects/latest.md`](prospects/latest.md) — most recent run
- [`prospects/`](prospects/) — historical scans; the git history of this directory IS the demo
- [`POV.md`](POV.md) — 2-page POV doc that uses the v2 rubric to surface a Modal-vs-Replicate misallocation. The persuasive case for the rubric

Every Monday, GitHub Actions runs `run.py` and commits the new digest. You can see how rankings shift over time as funding rounds land and orgs grow.

## Configuration

### Adjust scoring weights

Edit `config.py`. Every weight maps to a bet in [`BETS.md`](BETS.md); tune them when you adapt to a different ICP. Buckets are anchored to customer-distribution percentiles from `analyze_validation.py`.

### Adapt for a different ICP

The included `seeds.yml` is curated for Cursor's ICP. For a different ICP (e.g., Vercel's Next.js-shop profile, Sentry's observability buyer), replace `seeds.yml` and tune weights in `config.py`. Alternative seed files (`seeds_aitech.yml`, `seeds_nontech.yml`) are included as examples.

### Job board auto-detect

`careers_scan.py` supports Greenhouse, Lever, and Ashby. If you don't know which board a company uses, leave `greenhouse_token` / `lever_slug` / `ashby_org` blank in `seeds.yml` and the scanner tries all three using `github_org` as the slug guess.

### NPM scope override

`scan_npm()` defaults to the `github_org` slug. Override with `npm_org: <scope-name>` in `seeds.yml` when an org's NPM scope differs from its GitHub slug.

### Known limitation: Workday/iCIMS enterprises under-score

The careers scanner supports Greenhouse, Lever, and Ashby — used by ~70% of modern AI-native and Series B/C companies but only ~5% of Fortune 1000 enterprises. Companies on Workday (JPMorgan, Capital One, Goldman Sachs, Pfizer, Lockheed Martin) currently return zero careers data, under-scoring by 10–20 points. For high-priority Fortune 1000 prospects, manually look up open engineering roles count and add `eng_roles_override: <count>` to that company's `seeds.yml` entry. Workday scraping is on the roadmap.

## Roadmap

- [x] v1: 15-signal flat-bucket model, weekly cron, markdown + CSV output
- [x] v1 validation: 8/11 Cursor customers Tier 1 or 2
- [x] **v2: stack-shape rubric** — corroboration model (`SignalResult`), TS/JS dominance signal, NPM org footprint signal, JVM-backend disqualifier, AI-native reweight (15 → 5), per-account evidence fragments
- [x] v2 validation: 8/11 holds; same accuracy, sharper discrimination
- [x] **JVM/infra contrast seed set** — exercises the JVM disqualifier across Databricks, Confluent, Palantir, Elastic, Snowflake, MongoDB; first observed firings, plus minimum-active-languages gate added to fix sparse-footprint false positives
- [ ] v2 polish remaining: bundle-composition extractor (`__NEXT_DATA__`/`_next/static/chunks` regex), pure-infra-shop and sub-ten-team disqualifiers, expanded careers keyword list (TS/React/Next.js/Turborepo/design system)
- [ ] v3: headless-browser bundle detection, mobile-app-architecture signal (React Native vs native), dev-doc SDK coverage signal, LLM disambiguation for borderline cases
- [ ] Workday/iCIMS scraping (enterprise careers coverage)

## Built by

**Ryan Michaels.** GTM at Pave.

[Email](mailto:michaelsryan34@gmail.com) · [LinkedIn](https://linkedin.com/in/ryan-michaels5/) · [GitHub](https://github.com/ryanmichaels-jpg)

## License

MIT. Use freely.

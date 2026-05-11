# prospect-pulse

> Automated prospect signal pipeline for dev-tools companies. Score target accounts by GitHub footprint, careers page signals, and funding triggers. Built so SDRs and Account Associates spend their research time on accounts that actually fit.

## Why This Exists

Manual research is the most expensive thing reps do every week. 

Cursor's ICP is companies with codebases complex enough that AI-assisted code understanding pays for itself, and that signal is publicly visible in their GitHub orgs and careers pages.

prospect-pulse pulls the signal once a week, scores it against a data-anchored weighted model, and produces a ranked digest you can act on. The same code that scores a Cursor-shaped ICP also scores a Vercel-shaped ICP or a Sentry-shaped ICP. Only the config changes.

## What It Does

```
  seeds.yml ─────────┐
  (company list)     │
                     ▼
            ┌─────────────────┐
            │  github_scan.py │  ← PyGithub: org, repos, langs, contribs, recency, commit velocity
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ careers_scan.py │  ← Greenhouse / Lever / Ashby JSON APIs: roles + keyword hits
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   scorer.py     │  ← weighted model → tier + plain-English rationale
            └────────┬────────┘
                     │
                     ▼
        ┌────────────┴────────────┐
        ▼                         ▼
  prospects/YYYY-MM-DD.md   prospects/YYYY-MM-DD.csv
  (markdown digest)         (CRM/spreadsheet import)
```

## Scoring Model

15 signals across three layers: public engineering signals, careers-page signals, and contextual/manual signals. Total max: 140 points.

| # | Signal | Source | Max Pts | What's measured |
|---|---|---|---|---|
| 1 | Repo count | GitHub API | 10 | Total public repos (anchored to customer median: 68) |
| 2 | Language diversity | GitHub API | 10 | Unique programming languages across the org |
| 3 | SDK/CLI/tooling patterns | Repo names | 15 | Matches for `sdk`, `cli`, `tools`, `client`, `infra`, `lib`, `kit` |
| 4 | Contributor count | GitHub API | 5 | Unique contributors across top-5 repos by stars |
| 5 | Recency | GitHub API | 10 | % of repos with pushes in last 90 days |
| 6 | Repo age | GitHub API | 5 | Oldest repo at least 3 years old (accumulated complexity) |
| 7 | Commit velocity | GitHub Commits API | 5 | Avg commits/week across top 5 repos (90-day lookback) |
| 8 | Migration patterns | Repo descriptions | 10 | Keywords: `rewrite`, `migration`, `v2`, `v3`, `next-gen`, `rebuild` |
| 9 | Careers keywords | Greenhouse / Lever / Ashby | 10 | Job descriptions mentioning `platform engineer`, `devex`, `monorepo`, etc. |
| 10 | Eng hire velocity | Job board JSON | 10 | Count of open engineering roles (anchored to median: 31) |
| 11 | Funding recency | Manual (seeds.yml) | 10 | Series B/C in last 12 months. Buying-window trigger. |
| 12 | PLG signal | Manual (seeds.yml) | 5 | Public engineering-leader endorsement |
| 13 | AI-native flag | Manual (seeds.yml) | 15 | Companies whose product IS AI/ML. Bottom-up Cursor adoption pattern. |
| 14 | Engineering scale | Manual (seeds.yml) | 10 | Estimated employee count (50+ = full credit). Rewards engineering-centric companies, not size. |
| 15 | Industry vertical | Manual (seeds.yml) | 10 | Fintech, AI infra, developer tools, data infra. Domains with inherent architectural complexity. |

**Tier thresholds** (anchored to the distribution of Cursor's published customers):

| Tier | Score | Meaning |
|---|---|---|
| Tier 1 | 85+ | High-confidence prospect with strong signal across multiple dimensions |
| Tier 2 | 55–84 | Strong fit with either public-signal or contextual evidence |
| Tier 3 | 35–54 | Mixed signal. Needs manual research before outbound. |
| Tier 4 | <35 | Insufficient signal across all dimensions |

## Model Validation

The scoring model is anchored in real data from Cursor's published customers.

### Methodology

I scored 11 known Cursor customers with verbatim public quotes from their CEOs, CTOs, and engineering leadership (sourced from [Cursor's customer page](https://cursor.com/customers) and the [Money Forward case study](https://cursor.com/blog/money-forward)). The list spans three profiles:

- **Commercial segment (0–1,000 employees):** Sierra, Decagon, OnePay, Sentry, Upwork
- **Borderline (~1,000 employees):** Brex, Money Forward
- **Enterprise benchmark (>1,000 employees):** Stripe, Coinbase, Rippling, Datadog

The bucket thresholds in `config.py` are anchored to the actual distribution of these customers. Median Cursor customer has **68 public repos, 23 unique contributors, and 31 open engineering roles**. Companies above those medians on multiple signals score Tier 1 or 2. The `analyze_validation.py` script reproduces the distribution at any time.

### Results

**Pass rate: 8/11 customers correctly identified as Tier 1 or 2.**

| Tier | Companies |
|---|---|
| **Tier 1** | Sentry (110), Datadog (110), Stripe (99), Brex (87) |
| **Tier 2** | Coinbase (75), Sierra (70), Decagon (70), Money Forward (60) |
| **Tier 3** | Upwork (52), Rippling (52) |
| **Tier 4** | OnePay (25) |

Full per-company breakdown with verbatim customer quotes and signal-by-signal rationale: [`validation.md`](./validation.md).

### The 3 outliers

Three companies didn't pass. Each illustrates a limit of public-signal ICP scoring:

- **Upwork (Tier 3):** Marketplace vertical. Endorsement comes from an individual engineer rather than leadership. Sparse public footprint. The model flags this as borderline.
- **Rippling (Tier 3):** 11 public repos. The product code lives in private repos beyond the model's reach.
- **OnePay (Tier 4):** Walmart-owned fintech with essentially zero public GitHub footprint and no public job board. The model flags this as "insufficient public signal, needs manual research."

A scoring model that says "Tier 4 = investigate manually" is more useful to a rep than one that hallucinates Tier 1 confidence on stealth companies.

### Reproducibility

```bash
python3 -u run.py --validation        # Re-run the validation pipeline
python3 -u analyze_validation.py      # Recompute the customer distribution
```

Both commands write fresh reports the next time Cursor publishes new customer quotes. The validation set updates over time.

## Quickstart

```bash
# Clone and enter
git clone https://github.com/ryanmichaels-jpg/prospect-pulse.git
cd prospect-pulse

# Set up Python env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Add your GitHub PAT (5,000 req/hr vs 60 unauthenticated)
cp .env.example .env
# Edit .env, paste GITHUB_API_TOKEN from https://github.com/settings/tokens

# Run a scan
python3 -u run.py

# View results
open prospects/latest.md
```

## Sample Output

See [`prospects/latest.md`](./prospects/latest.md) for the most recent run, or browse [`prospects/`](./prospects/) for historical results.

The git history of this directory IS the demo. Every Monday, GitHub Actions runs `run.py` and commits the new digest. You can see how prospect rankings shift over time as funding rounds land and orgs grow.

## Configuration

### Adjust scoring weights

Edit `config.py`. Each signal has its own bucket function or weight constant. Buckets are anchored to the customer-distribution percentiles from `analyze_validation.py`; tune them when you adapt to a different ICP.

### Adapt for a different ICP

The included `seeds.yml` is a generic example with well-known dev-tools companies. For a company-tuned ICP, like Cursor's complex-codebase profile or Vercel's Next.js-shop profile, fork the repo, replace `seeds.yml`, and optionally tune `config.py` weights.

### Job board auto-detect

`careers_scan.py` supports Greenhouse, Lever, and Ashby. If you don't know which board a company uses, leave `greenhouse_token` / `lever_slug` / `ashby_org` blank in `seeds.yml` and the scanner will try all three using `github_org` as the slug guess.

## Roadmap

- [x] v0.1 Public infrastructure, 15-signal model, weekly cron, markdown + CSV output
- [x] v0.1 Validated against 11 known Cursor customers (8/11 Tier 1 or 2)
- [ ] v0.2 Crunchbase free-tier integration for auto-discovery of new Series B/C companies (wip)
- [ ] v0.3 LLM-augmented careers page parsing for ambiguous JD language (planned)
- [ ] v0.4 Companion Slack bot to explain any prospect on demand (planned)

## Built By

**Ryan Michaels.** GTM at Pave. Building the tools I wished I'd had as a rep. Targeting GTM roles at AI-native companies.

[Email](mailto:michaelsryan34@gmail.com) · [LinkedIn](https://linkedin.com/in/ryan-michaels5/) · [GitHub](https://github.com/ryanmichaels-jpg)

## License

MIT. Use freely.
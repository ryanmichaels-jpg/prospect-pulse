# Validation Report — 2026-05-13

Scoring model run against 11 known Cursor customers with verbatim public quotes.
**Pass criteria:** all commercial-segment customers (0-1,000 emp) score Tier 1 or 2; all enterprise benchmarks score Tier 1.

**Pass rate (Tier 1 or 2):** 8/11

---

## Datadog — Tier 1 (score: 115)

**Expected:** Tier 1
**Our rationale:** Score driven by: 85 SDK/tooling-pattern repos, 12 migration-pattern repos (python-github3: 'v3', rrweb-snapshot: 'rebuild'), ~41.7 commits/week across top repos, careers page mentions developer experience, internal tooling, internal tools, 120 open eng roles, 43% repos active in last 90d, ~7500 employees, developer_tools vertical; v2 signals — strong ts_js_dominance [top 3 active langs: Go (58), Python (57), TypeScript (32) · dd-trace-js: Express in package.json · browser-sdk: Express in package.json]; strong npm_org [@datadog: 78 packages · cross-ref: @datadog/datadog-ci depends on @datadog/datadog-ci-base].

**Customer said:** > Coding agents like Cursor have become the killer app for AI. Not only do coding agents increase the speed at which code is created, they also improve code quality.
— *Alexis Lê-Quôc, CTO & Co-Founder, Datadog*

**Score breakdown:**

- repo_count: 10
- tooling_signal: 15
- migration_signal: 10
- contributor_count: 5
- recency: 5
- repo_age: 5
- commit_velocity: 5
- careers_keywords: 10
- eng_hiring_velocity: 10
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 10
- npm_org: 5
- jvm_disqualifier: 0

---

## Sentry — Tier 1 (score: 110)

**Expected:** Tier 1
**Our rationale:** Score driven by: 50 SDK/tooling-pattern repos, 3 migration-pattern repos (action-migrations: 'migration', django-pg-zero-downtime-migrations: 'migration'), ~101.3 commits/week across top repos, careers page mentions developer experience, infrastructure engineer, internal tools, 31 open eng roles, 31% repos active in last 90d, ~350 employees, developer_tools vertical; v2 signals — weak ts_js_dominance [top 3 active langs: TypeScript (83), Python (66), Rust (33)]; strong npm_org [@sentry: 83 packages · cross-ref: @sentry/browser depends on @sentry/core].

**Customer said:** > Watching a dozen agent branches merge every day has become normal, and that freed-up velocity shows up everywhere from release cadence to bug-backlog burn-down. Cursor isn't a convenience add-on; it's a scale-multiplier for the whole org.
— *Cody De Arkland, Senior Director, Sentry*

**Score breakdown:**

- repo_count: 10
- tooling_signal: 15
- migration_signal: 10
- contributor_count: 5
- recency: 5
- repo_age: 5
- commit_velocity: 5
- careers_keywords: 10
- eng_hiring_velocity: 10
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 5
- npm_org: 5
- jvm_disqualifier: 0

---

## Stripe — Tier 1 (score: 99)

**Expected:** Tier 1
**Our rationale:** Score driven by: 11 SDK/tooling-pattern repos, 2 migration-pattern repos (pg-schema-diff: 'migration', open-banking-v2-docs: 'v2'), ~6.4 commits/week across top repos, careers page mentions developer experience, devex, infrastructure engineer, 109 open eng roles, 62% repos active in last 90d, ~7000 employees, fintech vertical; v2 signals — weak ts_js_dominance [top 3 active langs: TypeScript (19), Go (11), Ruby (7)]; strong npm_org [@stripe: 25 packages · cross-ref: @stripe/react-stripe-js depends on @stripe/stripe-js].

**Customer said:** > Cursor quickly grew from hundreds to thousands of extremely enthusiastic Stripe employees. We spend more on R&D and software creation than any other undertaking, and there's significant economic outcomes when making that process more efficient and productive.
— *Patrick Collison, Co-Founder & CEO, Stripe*

**Score breakdown:**

- repo_count: 7
- tooling_signal: 15
- migration_signal: 5
- contributor_count: 4
- recency: 5
- repo_age: 5
- commit_velocity: 3
- careers_keywords: 10
- eng_hiring_velocity: 10
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 5
- npm_org: 5
- jvm_disqualifier: 0

---

## Brex — Tier 2 (score: 77)

**Expected:** Tier 1
**Our rationale:** Score driven by: 6 SDK/tooling-pattern repos, 1 migration-pattern repos (grpc-java: 'migrating'), careers page mentions infrastructure engineer, internal tooling, internal tools, 53 open eng roles, ~1000 employees, fintech vertical.

**Customer said:** > More than 70% of our engineers now use Cursor, and we've seen meaningful gains in day-to-day development, faster execution on large-scale migrations, increased rate of debugging, and even faster onboarding.
— *James Reggio, CTO, Brex*

**Score breakdown:**

- repo_count: 7
- tooling_signal: 15
- migration_signal: 5
- contributor_count: 4
- recency: 0
- repo_age: 5
- commit_velocity: 0
- careers_keywords: 6
- eng_hiring_velocity: 10
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 0
- npm_org: 0
- jvm_disqualifier: 0

---

## Coinbase — Tier 2 (score: 75)

**Expected:** Tier 1
**Our rationale:** Score driven by: 30 SDK/tooling-pattern repos, 2 migration-pattern repos (aave-v3-crosschain-listing-template: 'v3', onramp-v2-mobile-demo: 'v2'), ~3500 employees, fintech vertical; v2 signals — weak ts_js_dominance [top 3 active langs: TypeScript (24), Go (13), Solidity (8)]; strong npm_org [@coinbase: 40 packages · cross-ref: @coinbase/cds-web depends on @coinbase/cds-common · DS primitives: @coinbase/cdp-hooks].

**Customer said:** > By February 2025, every Coinbase engineer had utilized Cursor, which has become the preferred IDE for most of our developers. Single engineers are now refactoring, upgrading, or building new codebases in days instead of months.
— *Brian Armstrong, CEO, Coinbase*

**Score breakdown:**

- repo_count: 10
- tooling_signal: 15
- migration_signal: 5
- contributor_count: 5
- recency: 0
- repo_age: 5
- commit_velocity: 0
- careers_keywords: 0
- eng_hiring_velocity: 0
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 5
- npm_org: 5
- jvm_disqualifier: 0

---

## Money Forward — Tier 2 (score: 70)

**Expected:** Tier 1
**Our rationale:** Score driven by: 3 SDK/tooling-pattern repos, 1 migration-pattern repos (omniauth-azure-activedirectory-v2: 'v2'), ~1500 employees, fintech vertical; v2 signals — strong ts_js_dominance [top 3 active langs: Ruby (5), Go (2), JavaScript (1) · oauth2-client-demo: Express in package.json]; strong npm_org [@moneyforward: 7 packages · cross-ref: @moneyforward/mfui-components depends on @moneyforward/mfui-design-tokens · DS primitives: @moneyforward/mfui-components, @moneyforward/mfui-icons-react].

**Customer said:** > Money Forward maintains complex, interconnected production systems. Cursor's context retrieval performed reliably against these codebases, which was critical for non-engineering teams interacting with production code for the first time.
— *Aaron Li, Staff Engineer, Money Forward (full case study at cursor.com/blog/money-forward)*

**Score breakdown:**

- repo_count: 7
- tooling_signal: 9
- migration_signal: 5
- contributor_count: 4
- recency: 0
- repo_age: 5
- commit_velocity: 0
- careers_keywords: 0
- eng_hiring_velocity: 0
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 10
- npm_org: 5
- jvm_disqualifier: 0

---

## Sierra — Tier 2 (score: 60)

**Expected:** Tier 1 or 2
**Our rationale:** Score driven by: careers page mentions developer experience, infrastructure engineer, internal tooling, 49 open eng roles, series_b, AI-native company, ~100 employees, ai_native vertical.

**Customer said:** > I'm really a big fan of Cursor. I've enjoyed taking something I love and has been my life's passion and seeing how this AI tool transforms how I create software.
— *Bret Taylor, Co-Founder & CEO, Sierra*

**Score breakdown:**

- repo_count: 0
- tooling_signal: 0
- migration_signal: 0
- contributor_count: 0
- recency: 0
- repo_age: 0
- commit_velocity: 0
- careers_keywords: 10
- eng_hiring_velocity: 10
- funding_recency: 10
- plg_signal: 5
- ai_native: 5
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 0
- npm_org: 0
- jvm_disqualifier: 0

---

## Decagon — Tier 2 (score: 60)

**Expected:** Tier 1 or 2
**Our rationale:** Score driven by: careers page mentions developer experience, devex, infrastructure engineer, 46 open eng roles, series_d, AI-native company, ~150 employees, ai_native vertical.

**Customer said:** > Cursor is the tool that every engineer (including me) instinctively turns to when navigating complexity or hitting a wall. With 100% adoption across our engineering team, Cursor has become an essential part of how we build.
— *Ashwin Sreenivas, Co-Founder, Decagon*

**Score breakdown:**

- repo_count: 0
- tooling_signal: 0
- migration_signal: 0
- contributor_count: 0
- recency: 0
- repo_age: 0
- commit_velocity: 0
- careers_keywords: 10
- eng_hiring_velocity: 10
- funding_recency: 10
- plg_signal: 5
- ai_native: 5
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 0
- npm_org: 0
- jvm_disqualifier: 0

---

## Rippling — Tier 3 (score: 47)

**Expected:** Tier 1
**Our rationale:** Score driven by: ~3000 employees, developer_tools vertical; v2 signals — weak ts_js_dominance [top 3 active langs: Python (4), Rust (1), TypeScript (1)].

**Customer said:** > Cursor has transformed the way our engineering teams write and ship code, with adoption growing from 150 to over 500 engineers (~60% of our org!) in just a few weeks.
— *Albert Strasheim, CTO, Rippling*

**Score breakdown:**

- repo_count: 4
- tooling_signal: 6
- migration_signal: 0
- contributor_count: 2
- recency: 0
- repo_age: 5
- commit_velocity: 0
- careers_keywords: 0
- eng_hiring_velocity: 0
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 5
- npm_org: 0
- jvm_disqualifier: 0

---

## Upwork — Tier 3 (score: 42)

**Expected:** Tier 1 or 2
**Our rationale:** Score driven by: careers page mentions microservices, platform engineer, platform engineering, 6 open eng roles, ~850 employees, marketplace vertical.

**Customer said:** > Across roles and levels, we're seeing an increase of over 25% in PR volume and over 100% in the average PR size. Together, that means we're shipping about 50% more code.
— *Anton Andreev, Principal Software Engineer, Upwork*

**Score breakdown:**

- repo_count: 4
- tooling_signal: 0
- migration_signal: 0
- contributor_count: 2
- recency: 0
- repo_age: 5
- commit_velocity: 0
- careers_keywords: 6
- eng_hiring_velocity: 5
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 5
- ts_js_dominance: 0
- npm_org: 0
- jvm_disqualifier: 0

---

## OnePay — Tier 4 (score: 25)

**Expected:** Tier 1 or 2
**Our rationale:** Score driven by: ~200 employees, fintech vertical.

**Customer said:** > Cursor took the most popular IDE in the world and put it on steroids. It's exceptional at debugging issues and attributing them to precise historical code changes, has stellar writing documentation skills, and has been incredibly helpful for new joiners in helping them ramp.
— *Moe Matar, CTO, OnePay*

**Score breakdown:**

- repo_count: 0
- tooling_signal: 0
- migration_signal: 0
- contributor_count: 0
- recency: 0
- repo_age: 0
- commit_velocity: 0
- careers_keywords: 0
- eng_hiring_velocity: 0
- funding_recency: 0
- plg_signal: 5
- ai_native: 0
- engineering_scale: 10
- industry_complexity: 10
- ts_js_dominance: 0
- npm_org: 0
- jvm_disqualifier: 0

---


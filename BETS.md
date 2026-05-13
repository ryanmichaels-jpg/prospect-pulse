# Bets and Counter-Bets

> Every signal in v2 follows a corroboration model. Each bet has a baseline interpretation that can be strengthened by named corroborations. The weight applied to a company depends not just on whether the signal fires but on how many corroborations support it. This is the architectural shift from v1's boolean/bucket scoring to v2's evidence-trail scoring.
>
> [`STACK_FIT_RUBRIC.md`](STACK_FIT_RUBRIC.md) is the philosophical argument for v2. This document is the evidence ledger: what each signal claims, what would strengthen it, and what would prove it wrong. Every weight in [`config.py`](config.py) should trace back to a bet here.

## Why a corroboration model

v1 scored each signal as a flat bucket: NPM org exists → 5 points, JD says "monorepo" → 2 points per hit. The flatness creates two failure modes. The first is false positives: Stripe, Twilio, and Algolia all publish public NPM orgs that look identical at the org level but are structurally different from a true internal-package ecosystem. The second is false negatives: a Linear-style company that runs a private monorepo with rich internal packages doesn't show up if it doesn't publish to NPM publicly.

v2 fixes this by treating each signal as a mini-investigation. The baseline interpretation gets a small weight; corroborations strengthen it; the full weight only applies when the corroborations confirm the underlying structural claim. The output of each signal is no longer "did it fire?" but "at what level, with what evidence?" That evidence becomes part of the per-account rationale, which is itself the SDR's opening line.

## Positive bets (tightened)

### Bet 1: The NPM org signal

**Original claim:** A public `@companyname` NPM org with multiple maintained packages indicates internal shared-package architecture, i.e. the monorepo + design-system pattern.

**Tightened version:** A public `@companyname` NPM org with multiple maintained packages indicates the company has invested in package-publishing infrastructure (versioning, release tooling, scoped naming). When the packages are internally cross-referential — depending on each other in `package.json`, sharing tooling configs, or referencing a private monorepo in their repo URLs — it indicates a real internal package ecosystem rather than just an SDK surface. The design-system inference holds specifically when the package names map to design-system primitives (tokens, components, hooks, icons, theming) rather than product SDKs.

**What changed:** The original treated "has an NPM org" as evidence of the architecture. The tightened version separates two questions: (a) does the org exist, and (b) are the packages structured like an internal ecosystem or like an external SDK? The second question is answerable from the public `package.json` files themselves and removes most of the false positives (Stripe, Twilio, Algolia all fail the cross-referential test).

### Bet 2: The top-3-languages signal

**Original claim:** TypeScript or JavaScript in the top 3 by repo count means significant full-stack web product work.

**Tightened version:** TypeScript or JavaScript in the top 3 by repo count (not bytes) across an org's non-fork, non-archived repos within the last 24 months indicates active web development is a real workstream. The "full-stack" inference is supported specifically when (a) TypeScript outranks JavaScript, suggesting deliberate adoption rather than legacy, and (b) at least one repo's `package.json` shows server-side frameworks (Next.js with API routes, Remix, Hono, Express, Fastify, tRPC) rather than only client libraries. Without both, treat the signal as "web frontend work happens here" rather than full-stack.

**What changed:** GitHub language stats are notoriously corrupted by vendored code, generated files, and abandoned repos. Switching to repo-count over a recency window strips most of that noise. The full-stack claim then gets gated by a specific corroborating signal (server frameworks in `package.json`) that's cheap to check and actually distinguishes full-stack shops from frontend-heavy ones.

**Known v2 outlier — Brex.** v1 scored Brex Tier 1 (87); v2 scores Brex Tier 2 (77). Brex's public engineering footprint is Java-dominant (grpc-java is their highest-signal repo; TS/JS does not appear in their top 3 active languages), even though their public quote — "more than 70% of our engineers now use Cursor… faster execution on large-scale migrations, increased rate of debugging, faster onboarding" (James Reggio, CTO) — indicates heavy internal TS/React frontend adoption. The demotion is intellectually correct given v2's public-signal-only philosophy: v1's `language_diversity` signal scored Brex 10 points for having 11 languages, which a polyglot JVM bank would also score 10 on. v2 correctly identifies that Brex's *public* footprint does not predict TS-dominant work. The operational answer for an SDR is not "deprioritize Brex" — it's "pursue Brex, but lead with frontend platform engineers, not the Java backend team, because the public footprint underestimates the internal TS stack." This is the same limitation already affecting Money Forward (v1 Tier 2, public Ruby-heavy), Rippling (v1 Tier 3, 11 public repos), and OnePay (v1 Tier 4, no public footprint). v2's broader pattern: when public signal misrepresents internal stack, the rubric should be honest about that rather than score by accident.

### Bet 3: The marketing-site stack signal

**Original claim:** Modern-stack markers on the marketing site indicate a culture proxy for engineering-forward decision-making.

**Tightened version:** Modern-stack markers (`__NEXT_DATA__`, `_next/static/chunks`, framework-specific build artifacts) on the marketing site indicate that at least one production surface ships on the modern web stack. The culture inference holds only when corroborated by at least one of: the marketing site is on the company's primary domain rather than a subdomain like `marketing.company.com` (suggesting internal ownership rather than agency/marketing-team siloing), the same framework appears in the company's public repos, or the engineering blog discusses the stack. A modern marketing site in isolation is a weak signal in 2026 because the stack has commoditized.

**What changed:** "Culture proxy" was the unfalsifiable bit. The tightened version replaces it with a falsifiable structural claim — internal ownership versus outsourced — that can be checked through domain configuration and corroborating public artifacts. It also explicitly downgrades the standalone signal to reflect the base-rate problem the "against" analysis surfaced.

### Bet 4: The JD signal

**Original claim:** JDs for frontend platform engineer, design system engineer, or TypeScript + monorepo roles indicate a Cursor-fit stack.

**Tightened version:** Open JDs for these roles indicate the company has identified the relevant work as worth dedicated headcount. The signal is stronger when (a) the JD is for a backfill or team expansion rather than a first hire (inferable from phrasing like "join our platform team" versus "establish our frontend platform"), (b) the JD names specific tooling rather than generic categories ("Turborepo," "Nx," "Changesets," "pnpm workspaces" rather than just "monorepo"), and (c) the company has multiple such roles open or filled across LinkedIn, suggesting an existing team rather than an aspirational one. A single "frontend platform engineer" posting at a 40-person company means something different than three such roles at a 400-person company.

**What changed:** The original conflated current-state evidence with future-intent evidence. The tightened version separates "we're building this" from "we operate this," because those are different buyer profiles with different timelines. The specific-tooling test also addresses the buzzword inflation problem: hiring managers who write "Turborepo" know what they mean; hiring managers who write only "monorepo" might not.

## Counter-bets (tightened)

### Counter-Bet 1: The JVM-backend counter-bet

**Original claim:** Java, Kotlin, or Scala dominating the top 3 languages means the codebase is microservice-organized with bounded multi-file blast radius, so Composer's value compounds less. Weight: −10.

**Tightened version:** JVM-language dominance in the top 3 indicates the company does substantial backend work in the JVM ecosystem. The deprioritization applies specifically when corroborated by evidence of service-oriented architecture: multiple small backend repos rather than a few large ones, public references to gRPC/Protobuf/service-mesh tooling, or JDs that mention "service ownership," "on-call rotation per service," or specific service-mesh products (Istio, Linkerd, Consul). Without that corroboration, treat JVM dominance as architecturally neutral — Kotlin modular monoliths, Scala data platforms, and Android-heavy orgs all show up the same way at the language level but have meaningfully different blast radii. The deal-economics consideration runs independently: JVM-dominant companies skew toward larger enterprises where absolute deal size can offset lower per-developer lift, so even a confirmed microservice shop may warrant outreach with a tailored pitch rather than blanket deprioritization.

**Suggested weighting:** −3 baseline on language signal alone, escalating to −6 when service-architecture corroboration is present. Reserve −10 for the rare case where both architectural corroboration and small total engineering headcount (which kills the deal-size offset) apply.

**What changed:** The original conflated "JVM language" with "microservices" with "low multi-file value." The tightened version separates those into a chain where each link requires its own evidence. It also explicitly carves out the deal-economics dimension, which the original ignored. The headline change is that JVM dominance becomes a flag to investigate rather than a signal to discount, with the actual discount applied only after corroboration.

### Counter-Bet 2: The pure-infra-shop counter-bet

**Original claim:** Go + Rust + Terraform + k8s/Helm dominance with no TS/JS in top 5 indicates a terminal-bound culture better suited to Claude Code than Cursor. Weight: −8.

**Tightened version:** The Go/Rust/Terraform/Helm composition without TS/JS in the top 5 indicates the company's public engineering footprint is infrastructure-heavy. The terminal-culture inference holds specifically when corroborated by independent cultural artifacts: public dotfiles repos, engineering blog posts that reference Neovim/Helix/tmux workflows, conference talks or README files that emphasize CLI-first tooling, or JDs that explicitly mention terminal-based workflows. Without those corroborations, the language composition alone is consistent with a wide range of engineering cultures, including teams that use VSCode or JetBrains products as their primary editor while doing CLI-heavy infra work. Separately, "pure infra shop" should be checked against the company's product surface, not just its public repo composition — many infra-vendor companies have substantial internal frontend work for dashboards, admin consoles, and customer UIs that doesn't appear in the public language stats but represents real Cursor-fit surface area. The fit question is also not binary against Claude Code: an infra-heavy company with even a small frontend team may warrant a split pitch (Cursor for the UI engineers, acknowledge Claude Code may fit the platform engineers better) rather than full deprioritization.

**Suggested weighting:** −2 on language composition alone, escalating to −5 with one cultural corroboration, and −8 only when multiple cultural corroborations align and the company has no public-facing product UI that would imply internal frontend work. The full −8 should be reserved for genuine pure-play infra vendors where the engineering org is overwhelmingly platform-shaped.

**What changed:** The original treated language composition as a proxy for culture, which packs in an assumption that the modern infra engineer is the Neovim purist of 2015. The tightened version requires actual cultural evidence, not just language composition, before applying the cultural inference. It also surfaces the internal-versus-public engineering gap, which is large for vendor companies and gets ignored when the analysis is based purely on public repos. The "split pitch" framing replaces the binary "deprioritize" framing with something more operational.

## Reweighted bet (carried forward, not yet workshopped at the same depth)

### Bet 5: AI-native flag (15 → 5)

**Claim:** Being AI-native is a weak independent predictor of Cursor fit. Being AI-native AND modern-web is a strong predictor.

**Customer evidence:** Sierra and Decagon (both AI-native and ship TS/React) are confirmed Cursor customers. Modal Labs, Replicate, Together AI, Pinecone (AI-native but Python/Rust-dominant) are unconfirmed. The flag was doing real work in v1 because the AI-native + modern-web combination scored well; v2 separates the two so we can see which is actually doing the work.

**Weight:** 5 points (down from 15). The freed 10 points fund the new stack-shape signals.

**Open question for workshopping:** Whether this should also have a corroboration ladder (e.g., AI-native + TS/JS dominance fires fully, AI-native alone fires at half). For now: flat 5.

## Disqualifier (not yet workshopped)

### Counter-Bet 3: Sub-ten team disqualifier

**Claim:** Below 10 engineers, the company isn't an SDR target — it's an individual evaluator, not a deal.

**Customer evidence:** Smallest validated Cursor customer (Sierra, ~100 employees) is an order of magnitude above the threshold.

**Weight:** −7 flat. Not a stack-fit signal but a GTM-fit floor.

**Detection:** `employee_estimate < 10` OR fewer than 5 unique contributors across top 5 repos.

**Open question for workshopping:** Whether the threshold should be 10 or 15, and whether the signal should soften (rather than disqualify) companies that have a strong single engineering leader endorsement (the founder-led adoption pattern).

## Bets carried forward from v1 (unchanged)

These signals were validated by v1's 8/11 pass rate and don't need re-justification:

- **Tooling repo patterns** (SDK, CLI, tools, client, infra, lib, kit in repo names). Validated: Sentry (50), Datadog (85), Stripe (10), Coinbase (30) — all confirmed customers.
- **Migration patterns** (rewrite, v2, v3, refactor, modernization keywords). Validated by direct customer quotes: Brex "faster execution on large-scale migrations," Coinbase "refactoring, upgrading, or building new codebases in days instead of months."
- **Repo recency** (% pushed in last 90d). Validated: Sentry 32%, Datadog 43%, Stripe 62%.
- **Repo age ≥ 3 years**. Validated by Money Forward's "complex, interconnected production systems" quote.
- **Commit velocity**. v1 already deweighted this (`config.py` comment notes 6 of 11 customers have ~0).
- **Eng hire velocity**, **engineering scale (50+)**, **industry vertical**. Generic scale/context proxies.
- **Funding recency**, **PLG signal**. Trigger and adoption-pattern signals, not stack-fit.

## Methodology notes

### How corroboration translates to weight

Each tightened signal returns a `level`:

- **none** — signal does not fire. Weight = 0.
- **weak** — baseline interpretation fires but no corroborations found. Weight = the conservative end of the suggested range.
- **strong** — baseline plus at least one corroboration. Weight = the higher end of the suggested range.

For counter-bets, "strong" means *more* corroborated and therefore *more* negative.

The output rendering should show the level alongside the points, so the SDR sees "TS/JS dominance: weak (5/10) — TypeScript in top 3 by repo count, but JavaScript outranks it" rather than just "TS/JS dominance: 5."

### What constitutes evidence

For each signal, the extractor should preserve **one short evidence fragment** per corroboration — a package name, a JD sentence, a domain string. The fragment becomes part of the per-account rationale. We're not building a citation system; we're producing talking points for outbound.

### When to flag for manual review

Some corroborations require data sources outside the existing pipeline (LinkedIn team-size depth, engineering blog content, dotfiles repos). For v2 this week, signals that can't auto-corroborate stay at the baseline (weak) level. A "manual_review_recommended" flag in the output tells the SDR which accounts would benefit from a 5-minute LinkedIn or blog skim before outbound.

### Validation guardrail

No v1 Tier 1 customer (Sentry, Datadog, Stripe, Brex) should drop below Tier 2 under v2. If the corroboration ladders demote a confirmed customer, the ladders are calibrated wrong, not the customer. Validation re-run is gated on this check.

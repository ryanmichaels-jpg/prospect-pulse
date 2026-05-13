"""Scoring weights and thresholds for prospect-pulse."""

# Repo count — anchored to customer median (68) and p75 (169)
REPO_COUNT_WEIGHTS = {
    "small": (0, 0, 0),          # 0 repos = 0 pts (no public signal)
    "tiny": (1, 67, 4),          # 1-67 = 4 pts (below customer median)
    "medium": (68, 168, 7),      # 68-168 = 7 pts (around customer median)
    "large": (169, 99999, 10),   # 169+ = 10 pts (above customer p75)
}

# Language diversity — RETIRED in v2.
# v1 awarded points for having many unique languages, which inverts what we want:
# polyglot JVM stacks scored identically to consolidated TS monorepos. See
# STACK_FIT_RUBRIC.md "Problem 2" for the analysis. Kept here only to avoid a
# breaking import elsewhere; scorer.py no longer references it.
LANG_WEIGHTS = {1: 0, 2: 5, 3: 5, 4: 10}  # deprecated, do not extend

# v2 replacement: TS/JS dominance with corroboration ladder.
# Per BETS.md Bet 2:
#   weak   = TS or JS in top 3 languages by repo count (active repos only)
#   strong = weak + at least one repo's package.json references a server framework
#            (Next.js, Remix, Hono, Express, Fastify, tRPC)
TS_JS_DOMINANCE_WEAK = 5
TS_JS_DOMINANCE_STRONG = 10

# v2 new signal: NPM org footprint with corroboration ladder.
# Per BETS.md Bet 1:
#   none   = no public NPM scope, or fewer than 3 packages (too thin to signal a real
#            packaging culture vs. one-off published utility)
#   weak   = scope exists with ≥3 packages but no cross-references or DS primitives —
#            looks like an external SDK surface, not an internal ecosystem
#   strong = weak + at least one of: a package depends on another @<org>/* package
#            (internal cross-reference) OR a package name matches a design-system
#            primitive (tokens, icons, components, theme, etc.)
NPM_ORG_WEAK = 2
NPM_ORG_STRONG = 5

# Tooling repo name patterns
TOOLING_PATTERNS = ["sdk", "cli", "tools", "client", "infra", "lib", "kit"]
TOOLING_PER_HIT = 3
TOOLING_CAP = 15

# Contributor buckets — anchored to customer median (23) and p75 (84)
CONTRIB_BUCKETS = [(1, 0), (23, 2), (84, 4), (99999, 5)]

# Recency: % repos pushed in last 90 days
RECENCY_BUCKETS = [(30, 0), (70, 5), (101, 10)]

# Repo age
AGE_THRESHOLD_YEARS = 3
AGE_PTS = 5

# Careers keywords
CAREERS_KEYWORDS = [
    "platform engineer", "platform engineering",
    "developer experience", "devex", "dx engineer",
    "internal tools", "internal tooling",
    "monorepo", "microservices",
    "legacy modernization", "infrastructure engineer",
]
CAREERS_PER_HIT = 2
CAREERS_CAP = 10

# Open eng roles — anchored to customer median (31)
ENG_ROLES_BUCKETS = [(1, 0), (31, 5), (99999, 10)]

# Commit velocity — DEWEIGHTED (6 of 11 customers have ~0; signal doesn't separate well)
COMMIT_VELOCITY_BUCKETS = [(1, 0), (10, 3), (99999, 5)]

# Migration keyword detection
MIGRATION_KEYWORDS = [
    "rewrite", "migration", "migrating", "v2", "v3",
    "next-gen", "rebuild", "modernization", "refactor", "successor",
    "new version"
]
MIGRATION_BUCKETS = [(1, 0), (3, 5), (99999, 10)]

# Funding bonus
FUNDING_RECENT_PTS = 10

# PLG signal
PLG_SIGNAL_PTS = 5

# Contextual signals (for stealth/private-code companies)
AI_NATIVE_PTS = 15

# Engineering scale — flat above 50, per data-driven analysis
EMPLOYEE_SCALE_BUCKETS = [(50, 0), (99999, 10)]

COMPLEX_INDUSTRIES = {
    # Original
    "fintech": 10,
    "ai_infra": 10,
    "ai_native": 10,
    "developer_tools": 10,
    "data_infra": 10,
    "marketplace": 5,
    # ⭐ NEW: non-tech-named verticals with real engineering complexity
    "financial_services": 10,   # banks, credit cards (distinct from fintech)
    "trading_quant": 10,        # hedge funds, prop trading
    "pharma": 10,               # regulated, research-heavy
    "aerospace_defense": 10,    # highly regulated codebases
    "public_sector": 10,        # gov agencies, NASA, .gov
    "media": 5,                 # news, broadcasting
    "retail": 5,                # big-box retail with eng teams
    "telecom": 5,               # carriers
    "automotive": 5,            # OEMs with software
    "travel": 5,                # hotels, airlines, OTAs
    "logistics": 5,             # shipping, supply chain
}

# Tier thresholds (model max is now ~140; rebalanced for new bucket weights)
TIERS = {
    "Tier 1": 85,
    "Tier 2": 55,
    "Tier 3": 35,
}
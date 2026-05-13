"""Apply weighted scoring model to GitHub + careers + funding signals."""
from dataclasses import dataclass, field
from typing import Dict, List
import config as cfg


@dataclass(frozen=True)
class SignalResult:
    """Result of one signal extraction under the v2 corroboration model.

    points:   scalar weight applied to the total (positive for bets, negative for disqualifiers)
    level:    "none" | "weak" | "strong" — how much corroboration supported the signal
    evidence: short fragments (package names, JD sentences, language stats, etc.) that fired
              the signal. Renders into the per-account rationale in the markdown digest.

    v1-style flat-bucket signals (the kept-from-v1 signals) currently use the `_strong` helper
    below: they fire fully or not at all, with no evidence fragments. The v2 corroboration-gated
    signals (NPM org, TS/JS dominance, bundle composition, JVM/infra disqualifiers) populate
    `evidence` with real fragments and use `level` to express weak vs. strong corroboration.

    See BETS.md for the corroboration spec per signal.
    """
    points: int
    level: str = "none"
    evidence: List[str] = field(default_factory=list)


def _strong(points: int) -> SignalResult:
    """Wrap a v1-style flat-bucket integer score as a SignalResult.

    Treats any non-zero points as a 'strong' fire (the v1 bucket either hit or it didn't).
    Evidence list stays empty — v1 signals don't carry per-account fragments yet.
    """
    return SignalResult(
        points=points,
        level="strong" if points != 0 else "none",
        evidence=[],
    )


@dataclass
class CompanyScore:
    name: str
    total: int
    breakdown: Dict[str, SignalResult]
    rationale: str
    tier: str
    raw: dict = field(default_factory=dict)


def _bucket_score(value: float, buckets: list) -> int:
    """Buckets: [(threshold, pts), ...] in ascending threshold order."""
    for threshold, pts in buckets:
        if value < threshold:
            return pts
    return buckets[-1][1]


def score(github_data: dict, careers_data: dict, funding_data: dict) -> CompanyScore:
    """Combine the three signal sources into a single CompanyScore."""
    breakdown = {}

    # ── Public GitHub signals ──────────────────────────────────────────

    # Repo count — anchored to customer median (68) and p75 (169)
    rc = github_data.get("repo_count", 0)
    if rc == 0:
        breakdown["repo_count"] = cfg.REPO_COUNT_WEIGHTS["small"][2]
    elif rc <= 67:
        breakdown["repo_count"] = cfg.REPO_COUNT_WEIGHTS["tiny"][2]
    elif rc <= 168:
        breakdown["repo_count"] = cfg.REPO_COUNT_WEIGHTS["medium"][2]
    else:
        breakdown["repo_count"] = cfg.REPO_COUNT_WEIGHTS["large"][2]

    # v1's language_diversity is RETIRED in v2 — see STACK_FIT_RUBRIC.md "Problem 2"
    # and BETS.md Bet 2. The replacement (ts_js_dominance) is computed below as a v2
    # corroboration-gated signal and merged into the breakdown after the wrap step.

    tooling = github_data.get("tooling_repo_count", 0)
    breakdown["tooling_signal"] = min(tooling * cfg.TOOLING_PER_HIT, cfg.TOOLING_CAP)

    migration = github_data.get("migration_repo_count", 0)
    breakdown["migration_signal"] = _bucket_score(migration, cfg.MIGRATION_BUCKETS)

    contribs = github_data.get("unique_contributors_top5", github_data.get("unique_contributors_top10", 0))
    breakdown["contributor_count"] = _bucket_score(contribs, cfg.CONTRIB_BUCKETS)

    recency = github_data.get("pct_repos_pushed_90d", 0)
    breakdown["recency"] = _bucket_score(recency, cfg.RECENCY_BUCKETS)

    breakdown["repo_age"] = cfg.AGE_PTS if github_data.get("oldest_repo_years", 0) >= cfg.AGE_THRESHOLD_YEARS else 0

    velocity = github_data.get("avg_commits_per_week", 0)
    breakdown["commit_velocity"] = _bucket_score(velocity, cfg.COMMIT_VELOCITY_BUCKETS)

    # ── Careers signals ────────────────────────────────────────────────
    keyword_hits = careers_data.get("platform_keyword_matches", 0)
    breakdown["careers_keywords"] = min(keyword_hits * cfg.CAREERS_PER_HIT, cfg.CAREERS_CAP)

    eng_roles = careers_data.get("open_engineering_roles", 0)
    breakdown["eng_hiring_velocity"] = _bucket_score(eng_roles, cfg.ENG_ROLES_BUCKETS)

    # ── Manual signals ─────────────────────────────────────────────────
    breakdown["funding_recency"] = cfg.FUNDING_RECENT_PTS if funding_data.get("recent_series_bc") else 0
    breakdown["plg_signal"] = cfg.PLG_SIGNAL_PTS if funding_data.get("plg_signal") else 0

    # ── Contextual signals for stealth/private companies ───────────────
    breakdown["ai_native"] = cfg.AI_NATIVE_PTS if funding_data.get("ai_native") else 0

    emp_count = funding_data.get("employee_estimate", 0)
    breakdown["engineering_scale"] = _bucket_score(emp_count, cfg.EMPLOYEE_SCALE_BUCKETS)

    industry = (funding_data.get("industry") or "").lower()
    breakdown["industry_complexity"] = cfg.COMPLEX_INDUSTRIES.get(industry, 0)

    # ── Wrap v1 ints + merge v2 corroboration-gated signals ───────────
    # v1 signals get wrapped as flat-bucket SignalResult (level="strong" if non-zero).
    # v2 signals are computed as real SignalResults carrying evidence fragments and
    # potentially firing at "weak" instead of "strong".
    breakdown_v2 = {k: _strong(v) for k, v in breakdown.items()}
    breakdown_v2["ts_js_dominance"] = _score_ts_js_dominance(github_data)

    # ── Totals and tier (over merged breakdown) ────────────────────────
    total = sum(r.points for r in breakdown_v2.values())
    tier = _tier_for(total)

    # ── Rationale ─────────────────────────────────────────────────────
    # _build_rationale reads the v1 int dict (still Dict[str, int]) for v1 signals.
    # v2 signal evidence is appended after.
    rationale = _build_rationale(breakdown, github_data, careers_data, funding_data)
    rationale = _append_v2_evidence(rationale, breakdown_v2)

    return CompanyScore(
        name=github_data.get("name", "unknown"),
        total=total,
        breakdown=breakdown_v2,
        rationale=rationale,
        tier=tier,
        raw={"github": github_data, "careers": careers_data, "funding": funding_data},
    )


def _score_ts_js_dominance(github_data: dict) -> SignalResult:
    """Score TS/JS dominance with the corroboration ladder from BETS.md Bet 2.

    Baseline (weak, 5 pts):
        TypeScript or JavaScript appears in the top 3 languages by repo count
        across non-fork, non-archived repos pushed in the last 24 months.

    Strong (10 pts):
        Baseline + at least one repo's package.json references a server-side
        framework (Next.js, Remix, Hono, Express, Fastify, tRPC) — confirming
        the org is doing full-stack web development, not just frontend or
        client-library work.

    No fire (0 pts):
        TS/JS not in the top 3 active languages.

    Evidence fragments rendered into the per-account rationale always include
    the actual top-3 language breakdown so the SDR can verify the call.
    """
    if not github_data.get("ts_js_dominant_top3", False):
        return SignalResult(points=0, level="none", evidence=[])

    evidence = []
    top_langs = github_data.get("top_languages_by_count", [])[:3]
    if top_langs:
        formatted = ", ".join(f"{lang} ({count})" for lang, count in top_langs)
        evidence.append(f"top 3 active langs: {formatted}")

    server_evidence = github_data.get("server_framework_evidence", [])
    if server_evidence:
        # Trim to first 2 fragments so a single noisy repo doesn't dominate the rationale.
        evidence.extend(server_evidence[:2])
        return SignalResult(
            points=cfg.TS_JS_DOMINANCE_STRONG,
            level="strong",
            evidence=evidence,
        )

    return SignalResult(
        points=cfg.TS_JS_DOMINANCE_WEAK,
        level="weak",
        evidence=evidence,
    )


def _append_v2_evidence(rationale: str, breakdown_v2: dict) -> str:
    """Append v2 SignalResult evidence to a v1-built rationale string.

    v1 signals don't carry evidence (they all wrap as level='strong' with empty list),
    so this only renders fragments from signals that actually populated evidence —
    i.e., the v2 corroboration-gated signals.
    """
    v2_fragments = []
    for name, result in breakdown_v2.items():
        if result.points == 0 or not result.evidence:
            continue
        v2_fragments.append(
            f"{result.level} {name} [{' · '.join(result.evidence)}]"
        )
    if not v2_fragments:
        return rationale
    base = rationale.rstrip(".")
    return f"{base}; v2 signals — {'; '.join(v2_fragments)}."


def _tier_for(total: int) -> str:
    if total >= cfg.TIERS["Tier 1"]:
        return "Tier 1"
    if total >= cfg.TIERS["Tier 2"]:
        return "Tier 2"
    if total >= cfg.TIERS["Tier 3"]:
        return "Tier 3"
    return "Tier 4"


def _build_rationale(b: dict, gh: dict, careers: dict, funding: dict) -> str:
    parts = []
    if b.get("tooling_signal", 0) >= 9:
        parts.append(f"{gh.get('tooling_repo_count', 0)} SDK/tooling-pattern repos")
    if b.get("migration_signal", 0) >= 5:
        examples = gh.get("migration_examples", [])
        parts.append(f"{gh.get('migration_repo_count', 0)} migration-pattern repos ({', '.join(examples[:2])})")
    if b.get("language_diversity", 0) >= 5:
        parts.append(f"{gh.get('unique_languages', 0)} languages")
    if b.get("commit_velocity", 0) >= 3:
        parts.append(f"~{gh.get('avg_commits_per_week', 0)} commits/week across top repos")
    if b.get("careers_keywords", 0) >= 4:
        kws = careers.get("matched_keywords", [])[:3]
        parts.append(f"careers page mentions {', '.join(kws)}")
    if b.get("eng_hiring_velocity", 0) >= 5:
        parts.append(f"{careers.get('open_engineering_roles', 0)} open eng roles")
    if b.get("funding_recency") == cfg.FUNDING_RECENT_PTS:
        parts.append(f"{funding.get('stage', 'recent funding')}")
    if b.get("recency", 0) >= 5:
        parts.append(f"{gh.get('pct_repos_pushed_90d', 0):.0f}% repos active in last 90d")

    if b.get("ai_native"):
        parts.append("AI-native company")
    if b.get("engineering_scale", 0) >= 5:
        emp = funding.get("employee_estimate", 0)
        parts.append(f"~{emp} employees")
    if b.get("industry_complexity", 0) >= 5:
        industry = funding.get("industry", "complex")
        parts.append(f"{industry} vertical")

    if not parts:
        parts.append("low-signal profile across all dimensions")
    return "Score driven by: " + ", ".join(parts) + "."
"""Routing pass — convert counter-bet outcomes into named outbound motions.

A counter-bet today subtracts points from a company's score and stops. The score
is the SDR's prioritization input — but it doesn't say *how* to approach a
flagged account. This module's job is to look at which signals fired and emit a
Route: which seats to target, which to avoid, what to lead with.

See BETS.md (counter-bet entries and the "Routing pass" section) and
STACK_FIT_RUBRIC.md ("How v2 scores") for the rubric philosophy. Routing is the
operational layer on top of scoring.

Some routes reference disqualifier signals that aren't coded yet
(sub_ten_team_disqualifier, pure_infra_shop_disqualifier). Those routes are
dormant — they never match today — and auto-activate when the underlying
signals ship. The architecture is in place so future work doesn't have to
revisit this module.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Route:
    """A named outbound motion. Attached to CompanyScore by determine_route().

    name           machine-readable identifier (snake_case). Stored in the CSV
                   route column for CRM filterability.
    label          human-readable name for the markdown digest header.
    pitch          1-2 sentence operational instruction the SDR uses as the
                   opener / qualification frame. Renders inline in the
                   per-account rationale.
    target_seats   list of seat titles to target with the pitch. Empty for
                   standard_outbound.
    avoid_seats    list of seat titles to NOT target (sometimes empty).
    """
    name: str
    label: str
    pitch: str
    target_seats: List[str] = field(default_factory=list)
    avoid_seats: List[str] = field(default_factory=list)


# ── Route catalog ────────────────────────────────────────────────────────────
# Order below is documentation only. Priority order lives in determine_route().

STANDARD_OUTBOUND = Route(
    name="standard_outbound",
    label="Standard outbound",
    pitch=(
        "Standard ICP fit. Lead with the strongest fired positive signal in "
        "the per-account rationale (NPM org evidence, tooling pattern, or "
        "design-system primitives, in that order of preference)."
    ),
)

SPLIT_PITCH_JVM = Route(
    name="split_pitch_jvm",
    label="Split pitch — frontend team",
    pitch=(
        "Public footprint shows JVM backend dominance AND substantial frontend "
        "/ design-system investment. Lead with the frontend platform team, not "
        "the JVM service-ownership team. Cite the NPM org evidence in the opener."
    ),
    target_seats=[
        "frontend platform engineer",
        "design system engineer",
        "web platform engineer",
    ],
    avoid_seats=[
        "service ownership engineer",
        "backend service engineer",
        "JVM platform engineer",
    ],
)

SPLIT_PITCH_INFRA = Route(
    name="split_pitch_infra",
    label="Split pitch — UI engineers vs. Claude Code",
    pitch=(
        "Pure-infra culture with a non-zero frontend surface. Cursor for the "
        "UI / admin-console engineers; acknowledge Claude Code may fit the "
        "platform engineers better. Don't lead with multi-file editing — lead "
        "with UI iteration speed."
    ),
    target_seats=[
        "UI engineer",
        "admin console engineer",
        "internal tools engineer",
    ],
    avoid_seats=[
        "platform engineer",
        "SRE",
        "infrastructure engineer",
    ],
)

INDIVIDUAL_EVALUATOR = Route(
    name="individual_evaluator",
    label="Individual evaluator (not SDR target)",
    pitch=(
        "Below 10 engineers, this isn't a sales motion — it's an individual "
        "evaluation. PLG path (free tier, founder outreach) or wait for "
        "headcount growth. Don't burn an SDR cold sequence."
    ),
    target_seats=["founder / engineering lead (PLG)"],
    avoid_seats=["SDR cold sequence"],
)

PUBLIC_UNDERESTIMATES_INTERNAL = Route(
    name="public_underestimates_internal",
    label="Public signal underestimates internal stack",
    pitch=(
        "Public footprint is thin or non-TS, but external evidence (published "
        "customer quote, manual research) indicates substantial internal "
        "TS/React adoption. Lead with the customer quote and pursue the "
        "frontend platform team."
    ),
    target_seats=[
        "frontend platform engineer",
        "design system engineer",
        "internal tools engineer",
    ],
)


# ── Routing logic ────────────────────────────────────────────────────────────


def _fired(breakdown: dict, signal_name: str) -> bool:
    """Return True if `signal_name` is in breakdown and fired (level != 'none').

    Handles both the signal-not-present case (e.g., disqualifier not yet coded)
    and signal-present-but-level-none case (didn't fire on this account).
    """
    sig = breakdown.get(signal_name)
    if sig is None:
        return False
    return getattr(sig, "level", "none") != "none"


def _level_at_least(breakdown: dict, signal_name: str, *levels: str) -> bool:
    """Return True if signal fired at any of the named levels."""
    sig = breakdown.get(signal_name)
    if sig is None:
        return False
    return getattr(sig, "level", "none") in levels


def determine_route(breakdown: dict, funding_data: dict) -> Route:
    """Pick a Route based on which signals fired in breakdown_v2.

    Priority order — first match wins:

      1. INDIVIDUAL_EVALUATOR               sub_ten_team_disqualifier fires.
                                            Overrides everything else: a sub-10
                                            engineer team isn't an SDR motion
                                            regardless of stack-shape.

      2. PUBLIC_UNDERESTIMATES_INTERNAL     funding_data['public_underestimates_internal']
                                            manual flag is True. The explicit
                                            override for "public signal
                                            misrepresents internal stack" —
                                            takes precedence over the
                                            disqualifier-driven reads because
                                            the manual flag is more specific.

      3. SPLIT_PITCH_JVM                    jvm_disqualifier ≥ weak AND
                                            npm_org strong. The
                                            Databricks / Palantir / Confluent
                                            pattern from the JVM contrast scan.

      4. SPLIT_PITCH_INFRA                  pure_infra_shop_disqualifier fires
                                            AND any ts_js_dominance evidence
                                            exists. Cursor for UI engineers,
                                            Claude Code may fit platform team.

      5. STANDARD_OUTBOUND                  Fallback when no counter-bet fired.

    Args:
        breakdown:     dict[str, SignalResult] — the v2 signal breakdown
                       produced by scorer.score(). Some signals may be absent
                       if not yet coded; _fired() handles that safely.
        funding_data:  dict — manual fields from seeds.yml (employee_estimate,
                       ai_native, public_underestimates_internal, etc.)
    """
    # 1. Sub-ten team disqualifier overrides everything (not an SDR motion).
    if _fired(breakdown, "sub_ten_team_disqualifier"):
        return INDIVIDUAL_EVALUATOR

    # 2. Manual override flag for the published-customer / thin-public pattern.
    if funding_data.get("public_underestimates_internal", False):
        return PUBLIC_UNDERESTIMATES_INTERNAL

    # 3. JVM split-pitch — disqualifier fired AND strong NPM org.
    if _fired(breakdown, "jvm_disqualifier") and _level_at_least(breakdown, "npm_org", "strong"):
        return SPLIT_PITCH_JVM

    # 4. Pure-infra split — disqualifier fired but TS/JS surface exists.
    if _fired(breakdown, "pure_infra_shop_disqualifier") and _fired(breakdown, "ts_js_dominance"):
        return SPLIT_PITCH_INFRA

    # 5. Default fallback.
    return STANDARD_OUTBOUND

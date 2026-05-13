"""Write scored prospects to markdown digest + CSV. Also handles validation reports."""
import csv
from datetime import datetime
from pathlib import Path
from scorer import CompanyScore


def _format_route(score: CompanyScore) -> str:
    """Render a CompanyScore's route as a short rationale fragment.

    Returns an empty string if no route is attached (shouldn't happen in normal
    runs since determine_route always returns a route, but defensive against
    partially-constructed CompanyScore instances).

    Format: 'route: <name> — <pitch>'. The pitch is the operational instruction
    the SDR uses; the name is the machine-readable identifier for filtering.
    """
    if score.route is None:
        return ""
    return f"route: {score.route.name} — {score.route.pitch}"


def write_markdown(scores: list, out_path: Path):
    """Write a ranked markdown digest of all scored companies."""
    scores_sorted = sorted(scores, key=lambda s: s.total, reverse=True)

    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# Prospect Pulse — {today}",
        "",
        f"Scanned **{len(scores)}** accounts. "
        f"Tier 1: {sum(1 for s in scores if s.tier == 'Tier 1')}, "
        f"Tier 2: {sum(1 for s in scores if s.tier == 'Tier 2')}, "
        f"Tier 3: {sum(1 for s in scores if s.tier == 'Tier 3')}, "
        f"Tier 4: {sum(1 for s in scores if s.tier == 'Tier 4')}",
        "",
        "| Rank | Company | Tier | Score | Why |",
        "|---|---|---|---|---|",
    ]
    for i, s in enumerate(scores_sorted, 1):
        # Append the route as a final section of the rationale, using the same
        # '; ' separator the rest of the rationale already uses between sections.
        route_fragment = _format_route(s)
        full_rationale = f"{s.rationale}; {route_fragment}" if route_fragment else s.rationale
        lines.append(f"| {i} | **{s.name}** | {s.tier} | {s.total} | {full_rationale} |")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print(f"Wrote markdown digest: {out_path}")


def write_csv(scores: list, out_path: Path):
    """Write a CSV with full breakdown — for CRM/spreadsheet import.

    In v2, breakdown values are SignalResult dataclasses; we extract `.points` for the CSV
    columns so the file remains spreadsheet-friendly. Evidence fragments are not yet exported
    here — that's a v3 feature (per-signal evidence columns or a JSON sidecar).
    """
    scores_sorted = sorted(scores, key=lambda s: s.total, reverse=True)
    # route column carries the machine-readable route name (snake_case) for CRM
    # filterability; the pitch text lives in the rationale column.
    fieldnames = (
        ["company", "tier", "total"]
        + list(scores_sorted[0].breakdown.keys())
        + ["route", "rationale"]
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for s in scores_sorted:
            points_only = {k: v.points for k, v in s.breakdown.items()}
            route_name = s.route.name if s.route is not None else ""
            row = {
                "company": s.name,
                "tier": s.tier,
                "total": s.total,
                **points_only,
                "route": route_name,
                "rationale": s.rationale,
            }
            w.writerow(row)
    print(f"Wrote CSV: {out_path}")


def write_validation_markdown(scores: list, quotes: dict, out_path: Path):
    """Write a validation report with customer quotes alongside scores."""
    scores_sorted = sorted(scores, key=lambda s: s.total, reverse=True)
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# Validation Report — {today}",
        "",
        "Scoring model run against 11 known Cursor customers with verbatim public quotes.",
        "**Pass criteria:** all commercial-segment customers (0-1,000 emp) score Tier 1 or 2; "
        "all enterprise benchmarks score Tier 1.",
        "",
        f"**Pass rate (Tier 1 or 2):** {sum(1 for s in scores if s.tier in ['Tier 1', 'Tier 2'])}/{len(scores)}",
        "",
        "---",
        "",
    ]

    for s in scores_sorted:
        q = quotes.get(s.name, {})
        route_label = s.route.label if s.route is not None else "—"
        route_name = s.route.name if s.route is not None else ""
        lines.extend([
            f"## {s.name} — {s.tier} (score: {s.total})",
            "",
            f"**Expected:** {q.get('expected_tier', 'N/A')}",
            f"**Our rationale:** {s.rationale}",
            "",
            f"**Customer said:** > {q.get('quote', '[no quote]')}",
            f"— *{q.get('source', '')}*",
            "",
            f"**Route:** `{route_name}` — {route_label}",
            "",
            "**Score breakdown:**",
            "",
        ])
        for k, v in s.breakdown.items():
            lines.append(f"- {k}: {v.points}")
        lines.extend(["", "---", ""])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print(f"Wrote validation report: {out_path}")

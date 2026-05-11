"""Main entry point. Loads seeds, scans each company, scores, writes output.

Modes:
  python3 run.py                    # Normal prospect scan from seeds.yml
  python3 run.py --validation       # Validation scan from validation-seeds.yml
"""
import sys
import yaml
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from github_scan import scan_org
from careers_scan import scan as scan_careers
from scorer import score
from output import write_markdown, write_csv, write_validation_markdown


def main():
    load_dotenv()

    is_validation = "--validation" in sys.argv
    seeds_path = Path("validation-seeds.yml" if is_validation else "seeds.yml")

    if not seeds_path.exists():
        raise FileNotFoundError(f"{seeds_path} not found")

    with open(seeds_path) as f:
        seeds = yaml.safe_load(f) or {}

    companies = seeds.get("companies", [])
    print(f"{'[VALIDATION] ' if is_validation else ''}Scanning {len(companies)} companies...")

    scores = []
    quotes = {}
    for c in companies:
        print(f"  → {c['name']}")
        github_data = scan_org(c["github_org"])
        github_data["name"] = c["name"]

        careers_data = scan_careers(c)
        funding_data = {
            "stage": c.get("funding_stage", "unknown"),
            "recent_series_bc": c.get("recent_series_bc", False),
            "plg_signal": c.get("plg_signal", False),
            "ai_native": c.get("ai_native", False),
            "employee_estimate": c.get("employee_estimate", 0),
            "industry": c.get("industry", ""),
        }

        s = score(github_data, careers_data, funding_data)
        scores.append(s)

        if is_validation:
            quotes[c["name"]] = {
                "quote": c.get("quote", ""),
                "source": c.get("quote_source", ""),
                "expected_tier": c.get("expected_tier", ""),
            }

        print(f"     → {s.tier} ({s.total}): {s.rationale}")

    today = datetime.now().strftime("%Y-%m-%d")

    if is_validation:
        write_validation_markdown(scores, quotes, Path("validation.md"))
        write_csv(scores, Path(f"validation-{today}.csv"))
        print(f"\nDone. View validation results in validation.md")
    else:
        write_markdown(scores, Path(f"prospects/{today}.md"))
        write_csv(scores, Path(f"prospects/{today}.csv"))
        write_markdown(scores, Path("prospects/latest.md"))
        print(f"\nDone. View results in prospects/{today}.md")


if __name__ == "__main__":
    main()
"""Main entry point. Loads seeds, scans each company, scores, writes output.

Modes:
  python3 run.py                            # Normal prospect scan from seeds.yml
  python3 run.py --validation               # Validation scan from validation-seeds.yml
  python3 run.py --seeds <path>             # Arbitrary seeds file (e.g. seeds_yc.yml)
"""
import sys
import yaml
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from github_scan import scan_org
from careers_scan import scan as scan_careers
from npm_scan import scan as scan_npm
from scorer import score
from output import write_markdown, write_csv, write_validation_markdown


def _resolve_seeds_path(argv):
    """Pick the seeds file based on CLI flags.

    Priority: --validation overrides everything else; --seeds <path> picks an
    arbitrary file; absent both, fall back to seeds.yml.
    """
    if "--validation" in argv:
        return Path("validation-seeds.yml"), True
    if "--seeds" in argv:
        idx = argv.index("--seeds")
        if idx + 1 >= len(argv):
            raise SystemExit("--seeds requires a path argument: --seeds <path>")
        return Path(argv[idx + 1]), False
    return Path("seeds.yml"), False


def main():
    load_dotenv()

    seeds_path, is_validation = _resolve_seeds_path(sys.argv)

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

        # NPM scope defaults to the github_org slug; override with `npm_org` in
        # seeds.yml when the org's NPM scope differs from its GitHub slug.
        npm_data = scan_npm(c.get("npm_org") or c["github_org"])

        funding_data = {
            "stage": c.get("funding_stage", "unknown"),
            "recent_series_bc": c.get("recent_series_bc", False),
            "plg_signal": c.get("plg_signal", False),
            "ai_native": c.get("ai_native", False),
            "employee_estimate": c.get("employee_estimate", 0),
            "industry": c.get("industry", ""),
            # Manual override flag for the public-underestimates-internal route.
            # Set in seeds.yml on companies where Cursor has a published customer
            # quote but the public footprint is misleadingly thin (Brex, Money
            # Forward, Rippling, OnePay). See routing.PUBLIC_UNDERESTIMATES_INTERNAL.
            "public_underestimates_internal": c.get("public_underestimates_internal", False),
        }

        s = score(github_data, careers_data, funding_data, npm_data)
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
        # When --seeds is used, suffix the output with the seeds file basename so
        # multiple scans on the same date don't overwrite each other. The default
        # seeds.yml keeps the unsuffixed filename for backward compat.
        if seeds_path.name == "seeds.yml":
            stem = today
        else:
            # seeds_yc.yml -> "yc", seeds_aitech.yml -> "aitech"
            suffix = seeds_path.stem.removeprefix("seeds_") or seeds_path.stem
            stem = f"{today}-{suffix}"

        write_markdown(scores, Path(f"prospects/{stem}.md"))
        write_csv(scores, Path(f"prospects/{stem}.csv"))
        write_markdown(scores, Path("prospects/latest.md"))
        print(f"\nDone. View results in prospects/{stem}.md")


if __name__ == "__main__":
    main()
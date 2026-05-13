"""Scan a company's careers page for engineering hiring signals.

Supports Greenhouse, Lever, and Ashby JSON APIs (no scraping needed).

Priority order:
  1. If explicit greenhouse_token / lever_slug / ashby_org is set in seeds.yml,
     use that and stop.
  2. Otherwise, auto-detect: try all three boards using github_org as the slug,
     return the first one with real data.
"""
import requests
from config import CAREERS_KEYWORDS, SERVICE_ARCHITECTURE_KEYWORDS


GREENHOUSE_URL = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
LEVER_URL = "https://api.lever.co/v0/postings/{company}?mode=json"
ASHBY_URL = "https://api.ashbyhq.com/posting-api/job-board/{org}?includeCompensation=true"


def scan_greenhouse(board_token: str) -> dict:
    try:
        r = requests.get(GREENHOUSE_URL.format(token=board_token), timeout=10)
        r.raise_for_status()
        jobs = r.json().get("jobs", [])
    except Exception as e:
        return _empty_result("greenhouse", error=str(e))
    return _analyze_jobs(jobs, source="greenhouse")


def scan_lever(company_slug: str) -> dict:
    try:
        r = requests.get(LEVER_URL.format(company=company_slug), timeout=10)
        r.raise_for_status()
        jobs = r.json()
    except Exception as e:
        return _empty_result("lever", error=str(e))
    normalized = []
    for j in jobs:
        normalized.append({
            "title": j.get("text", ""),
            "content": j.get("description", "") + " " + str(j.get("lists", "")),
            "department": j.get("categories", {}).get("department", ""),
        })
    return _analyze_jobs(normalized, source="lever")


def scan_ashby(org_slug: str) -> dict:
    try:
        r = requests.get(ASHBY_URL.format(org=org_slug), timeout=10)
        r.raise_for_status()
        data = r.json()
        jobs = data.get("jobs", [])
    except Exception as e:
        return _empty_result("ashby", error=str(e))
    normalized = []
    for j in jobs:
        normalized.append({
            "title": j.get("title", ""),
            "content": j.get("descriptionPlain", "") or j.get("descriptionHtml", ""),
            "department": j.get("department", ""),
        })
    return _analyze_jobs(normalized, source="ashby")


def _analyze_jobs(jobs, source: str) -> dict:
    eng_roles = 0
    keyword_hits = set()
    service_arch_hits = set()
    total_text = ""

    for job in jobs:
        title = (job.get("title") or "").lower()
        content = (job.get("content") or "").lower()
        dept = (job.get("department") or "").lower()
        text = f"{title} {content} {dept}"

        if any(t in title for t in ["engineer", "developer", "swe", "sde"]):
            eng_roles += 1

        total_text += " " + text

    for kw in CAREERS_KEYWORDS:
        if kw.lower() in total_text:
            keyword_hits.add(kw)

    # Separate scan: service-architecture corroboration for JVM disqualifier
    # (Counter-Bet 1). Tracked apart from platform-engineering keywords because
    # this scores into a different signal (negative) and is not a "more is better"
    # count — a single hit is enough to escalate JVM dominance to strong.
    for kw in SERVICE_ARCHITECTURE_KEYWORDS:
        if kw.lower() in total_text:
            service_arch_hits.add(kw)

    return {
        "source": source,
        "open_engineering_roles": eng_roles,
        "platform_keyword_matches": len(keyword_hits),
        "matched_keywords": sorted(keyword_hits),
        "service_arch_keyword_matches": len(service_arch_hits),
        "matched_service_arch_keywords": sorted(service_arch_hits),
    }


def _empty_result(source: str = "none", error: str = None) -> dict:
    result = {
        "source": source,
        "open_engineering_roles": 0,
        "platform_keyword_matches": 0,
        "matched_keywords": [],
    }
    if error:
        result["error"] = error
    return result


def _has_data(result: dict) -> bool:
    """Treat a result as useful only if it found at least one engineering role."""
    return result.get("open_engineering_roles", 0) > 0


def scan(company_config: dict) -> dict:
    """Dispatch to careers sources with explicit-config-first, then auto-detect."""

    # Layer 1: Explicit configuration takes priority
    if company_config.get("greenhouse_token"):
        return scan_greenhouse(company_config["greenhouse_token"])
    if company_config.get("lever_slug"):
        return scan_lever(company_config["lever_slug"])
    if company_config.get("ashby_org"):
        return scan_ashby(company_config["ashby_org"])

    # Layer 2: Auto-detect using github_org as a slug guess
    github_org = company_config.get("github_org", "")
    if not github_org:
        return _empty_result()

    slug = github_org.lower()

    # Try each board; return the first one with real data
    for scanner in (scan_greenhouse, scan_lever, scan_ashby):
        result = scanner(slug)
        if _has_data(result):
            result["auto_detected"] = True
            return result

    # Nothing found — return empty with a hint
    empty = _empty_result()
    empty["note"] = (
        "Auto-detect found no careers data for any board. "
        "Add explicit greenhouse_token / lever_slug / ashby_org to seeds.yml."
    )
    return empty


if __name__ == "__main__":
    import json
    # Smoke test: auto-detect with just a github_org
    print(json.dumps(scan({"github_org": "modal-labs"}), indent=2))
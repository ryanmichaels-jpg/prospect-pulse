"""Scan a GitHub organization and return signals for scoring."""
import os
from datetime import datetime, timezone, timedelta
from github import Github, Auth, GithubException
from config import TOOLING_PATTERNS, MIGRATION_KEYWORDS


def scan_org(org_name: str, token: str = None) -> dict:
    """Pull GitHub signals for one org.

    Returns a dict of measurable signals, or {"name": ..., "error": ...} on failure.
    """
    token = token or os.getenv("GITHUB_API_TOKEN")
    if not token:
        raise ValueError(
            "No GITHUB_API_TOKEN — add it to .env (see README). "
            "A classic PAT should start with ghp_; fine-grained tokens use github_pat_."
        )

    g = Github(auth=Auth.Token(token))

    try:
        org = g.get_organization(org_name)
    except GithubException as e:
        return {"name": org_name, "error": f"Org not found or no access: {e}"}

    try:
        repos = list(org.get_repos())
    except GithubException as e:
        return {"name": org_name, "error": f"Could not list repos: {e}"}

    if not repos:
        return {"name": org_name, "repo_count": 0, "error": "Empty org"}

    cutoff_90d = datetime.now(timezone.utc) - timedelta(days=90)

    # Basic aggregates
    languages = set()
    tooling_count = 0
    migration_count = 0
    migration_examples = []
    recent_pushes = 0
    oldest_year = 0
    contributors = set()

    # Top 5 repos by stars for deep scans (contributors + commit velocity)
    repos_sorted = sorted(repos, key=lambda r: r.stargazers_count, reverse=True)
    deep_scan = repos_sorted[:5]

    for repo in repos:
        # Languages
        if repo.language:
            languages.add(repo.language)

        # Tooling repo name match
        name_lower = repo.name.lower()
        if any(p in name_lower for p in TOOLING_PATTERNS):
            tooling_count += 1

        # ⭐ NEW: Migration keyword detection (name + description)
        desc = (repo.description or "").lower()
        text = f"{name_lower} {desc}"
        for kw in MIGRATION_KEYWORDS:
            if kw in text:
                migration_count += 1
                if len(migration_examples) < 3:
                    migration_examples.append(f"{repo.name}: '{kw}'")
                break  # one match per repo

        # Recency
        if repo.pushed_at and repo.pushed_at.replace(tzinfo=timezone.utc) > cutoff_90d:
            recent_pushes += 1

        # Age
        if repo.created_at:
            age = (datetime.now(timezone.utc) - repo.created_at.replace(tzinfo=timezone.utc)).days / 365
            oldest_year = max(oldest_year, age)

    # Contributors from top-5 repos
    for repo in deep_scan:
        try:
            for c in repo.get_contributors()[:20]:
                contributors.add(c.login)
        except GithubException:
            continue

    # ⭐ NEW: Commit velocity from top-5 repos, 90-day lookback
    commit_velocities = []
    for repo in deep_scan:
        try:
            commits = repo.get_commits(since=cutoff_90d)
            count = commits.totalCount
            weekly = count / (90 / 7)
            commit_velocities.append(weekly)
        except GithubException:
            commit_velocities.append(0)
    avg_velocity = round(sum(commit_velocities) / len(commit_velocities), 1) if commit_velocities else 0

    return {
        "name": org_name,
        "repo_count": len(repos),
        "unique_languages": len(languages),
        "tooling_repo_count": tooling_count,
        "migration_repo_count": migration_count,
        "migration_examples": migration_examples,
        "unique_contributors_top5": len(contributors),
        "pct_repos_pushed_90d": round((recent_pushes / len(repos)) * 100, 1),
        "oldest_repo_years": round(oldest_year, 1),
        "avg_commits_per_week": avg_velocity,
        "top_languages": sorted(languages)[:5],
    }


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    import json
    print(json.dumps(scan_org("modal-labs"), indent=2, default=str))

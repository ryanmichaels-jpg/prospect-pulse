"""Scan a GitHub organization and return signals for scoring."""
import json
import os
from collections import Counter
from datetime import datetime, timezone, timedelta
from github import Github, Auth, GithubException
from config import TOOLING_PATTERNS, MIGRATION_KEYWORDS, JVM_LANGUAGES, SERVICE_ARCHITECTURE_KEYWORDS

# Server-side frameworks that, when found in package.json, corroborate the
# "full-stack web development" inference for TS/JS-dominant orgs.
# See BETS.md, Bet 2 (top-3-languages signal) for the rationale.
SERVER_FRAMEWORK_DEPS = {
    "next": "Next.js",
    "remix": "Remix",
    "@remix-run/node": "Remix",
    "@remix-run/server-runtime": "Remix",
    "hono": "Hono",
    "express": "Express",
    "fastify": "Fastify",
    "@trpc/server": "tRPC",
    "trpc": "tRPC",
}


def _check_server_frameworks(repos):
    """Inspect package.json on up to 5 top JS/TS repos for server-framework deps.

    Returns a list of short evidence fragments like 'repo-name: Next.js dependency'.
    Empty list means no corroboration found.

    This is the "strong" corroboration for Bet 2 — see BETS.md.
    """
    js_ts_repos = sorted(
        [r for r in repos if r.language in ("TypeScript", "JavaScript")],
        key=lambda r: r.stargazers_count,
        reverse=True,
    )[:5]

    evidence = []
    for repo in js_ts_repos:
        try:
            content_file = repo.get_contents("package.json")
            content = content_file.decoded_content.decode("utf-8")
            data = json.loads(content)
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for dep_name, framework_label in SERVER_FRAMEWORK_DEPS.items():
                if dep_name in deps:
                    evidence.append(f"{repo.name}: {framework_label} in package.json")
                    break  # one framework per repo is enough; move on
        except (GithubException, json.JSONDecodeError, UnicodeDecodeError, KeyError):
            # Repo has no package.json, has malformed JSON, or content is unreachable.
            # Move on; absence is not negative evidence — corroboration is opportunistic.
            continue
    return evidence


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
    cutoff_24mo = datetime.now(timezone.utc) - timedelta(days=730)

    # v1 aggregates (over ALL repos, kept unchanged for v1-flat-bucket signals)
    languages = set()
    tooling_count = 0
    migration_count = 0
    migration_examples = []
    recent_pushes = 0
    oldest_year = 0
    contributors = set()

    # v2 aggregates (over an ACTIVE subset — non-fork, non-archived, pushed in last 24 months)
    # per BETS.md Bet 2: this strips the noise GitHub language stats accumulate from
    # vendored code, abandoned repos, and unmaintained forks.
    active_language_counts = Counter()
    active_repos = []
    # Service-architecture references found in repo names/descriptions — corroboration
    # input for the JVM disqualifier (Counter-Bet 1).
    service_arch_repo_evidence = []

    # Top 5 repos by stars for deep scans (contributors + commit velocity)
    repos_sorted = sorted(repos, key=lambda r: r.stargazers_count, reverse=True)
    deep_scan = repos_sorted[:5]

    for repo in repos:
        # ── v1 aggregates (all repos) ─────────────────────────────────────────

        # Languages (unique set, used by v1 language_diversity — kept for backward compat)
        if repo.language:
            languages.add(repo.language)

        # Tooling repo name match
        name_lower = repo.name.lower()
        if any(p in name_lower for p in TOOLING_PATTERNS):
            tooling_count += 1

        # Migration keyword detection (name + description)
        desc = (repo.description or "").lower()
        text = f"{name_lower} {desc}"
        for kw in MIGRATION_KEYWORDS:
            if kw in text:
                migration_count += 1
                if len(migration_examples) < 3:
                    migration_examples.append(f"{repo.name}: '{kw}'")
                break  # one match per repo

        # Recency (90d)
        pushed_utc = repo.pushed_at.replace(tzinfo=timezone.utc) if repo.pushed_at else None
        if pushed_utc and pushed_utc > cutoff_90d:
            recent_pushes += 1

        # Age
        if repo.created_at:
            age = (datetime.now(timezone.utc) - repo.created_at.replace(tzinfo=timezone.utc)).days / 365
            oldest_year = max(oldest_year, age)

        # ── v2 active-subset filter ───────────────────────────────────────────
        # Per BETS.md Bet 2: non-fork, non-archived, pushed in last 24 months.
        if (
            not repo.fork
            and not repo.archived
            and pushed_utc
            and pushed_utc > cutoff_24mo
        ):
            active_repos.append(repo)
            if repo.language:
                active_language_counts[repo.language] += 1

            # Service-architecture corroboration for JVM disqualifier (Counter-Bet 1).
            # Look for gRPC/Protobuf/service-mesh references in repo name or description.
            for kw in SERVICE_ARCHITECTURE_KEYWORDS:
                if kw in text:
                    if len(service_arch_repo_evidence) < 3:
                        service_arch_repo_evidence.append(f"{repo.name}: '{kw}'")
                    break  # one match per repo is enough

    # Contributors from top-5 repos
    for repo in deep_scan:
        try:
            for c in repo.get_contributors()[:20]:
                contributors.add(c.login)
        except GithubException:
            continue

    # Commit velocity from top-5 repos, 90-day lookback
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

    # ── v2 derived signals (over active subset) ──────────────────────────────
    # Top 3 languages by repo count among active (non-fork, non-archived, last 24mo) repos.
    top_languages_by_count = active_language_counts.most_common(5)
    top_3_langs = {lang for lang, _ in active_language_counts.most_common(3)}
    ts_js_dominant_top3 = bool(top_3_langs & {"TypeScript", "JavaScript"})
    # Per BETS.md Bet 2 strong-corroboration: TS outranking JS suggests deliberate adoption.
    ts_outranks_js = active_language_counts.get("TypeScript", 0) > active_language_counts.get("JavaScript", 0)

    # Per BETS.md Counter-Bet 1: JVM language(s) in the top 3 active langs flag the
    # JVM disqualifier at baseline. Corroboration (service-arch refs) escalates.
    jvm_in_top_3_list = sorted(top_3_langs & JVM_LANGUAGES)
    jvm_dominant_top3 = bool(jvm_in_top_3_list)

    # Server-framework corroboration via package.json scan on top 5 JS/TS active repos.
    server_framework_evidence = _check_server_frameworks(active_repos)

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
        # ── v2 fields ────────────────────────────────────────────────────────
        "active_repo_count": len(active_repos),
        "top_languages_by_count": top_languages_by_count,
        "ts_js_dominant_top3": ts_js_dominant_top3,
        "ts_outranks_js": ts_outranks_js,
        "server_framework_evidence": server_framework_evidence,
        # JVM disqualifier inputs (Counter-Bet 1)
        "jvm_dominant_top3": jvm_dominant_top3,
        "jvm_languages_in_top3": jvm_in_top_3_list,
        "service_arch_repo_evidence": service_arch_repo_evidence,
    }


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    import json
    print(json.dumps(scan_org("modal-labs"), indent=2, default=str))

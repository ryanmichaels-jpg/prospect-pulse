"""Scan a company's public NPM organization for package ecosystem signals.

Per BETS.md Bet 1: a public @<orgname> NPM org with multiple maintained packages
indicates the company has invested in package-publishing infrastructure. The
corroboration ladder distinguishes a true internal package ecosystem
(cross-referential deps, design-system primitives) from a thin external SDK surface.

NPM scope is assumed to match the github_org slug by default, with an optional
`npm_org` override in seeds.yml for the cases where they differ.
"""
import re
import requests
from urllib.parse import quote


# NPM's public search v1 endpoint does not honor the `scope:` qualifier (it's
# documented for the CLI but not the HTTP API). Instead we search for the literal
# string "@<org>/" and post-filter results to only the matching scope.
NPM_SEARCH_URL = "https://registry.npmjs.org/-/v1/search?text={query}&size=250"
NPM_METADATA_URL = "https://registry.npmjs.org/{full_name}"

# Single-segment design-system terms. Matched as standalone hyphen/underscore-
# delimited segments to avoid false positives like "@orgname/web-ui" (which would
# match a too-loose regex on "ui" as a substring).
_DS_SEGMENTS = {
    "tokens", "icons", "primitives", "hooks",
    "theme", "themes", "typography", "components",
    "polaris", "tailwind",
}

# Multi-word DS indicators (substring matches — high confidence).
_DS_SUBSTRINGS = [
    "design-system", "designsystem",
    "design-tokens", "designtokens",
    "ui-kit", "ui-components", "ui-primitives", "ui-icons", "ui-tokens",
]


def _is_design_system_name(full_pkg_name: str) -> bool:
    """Detect if a scoped NPM package name suggests it's a design-system primitive."""
    short = full_pkg_name.split("/")[-1].lower()
    if any(s in short for s in _DS_SUBSTRINGS):
        return True
    segments = set(re.split(r"[-_]", short))
    return bool(segments & _DS_SEGMENTS)


def scan(org_name: str, top_n: int = 20) -> dict:
    """Pull NPM org signals for one org.

    Returns a dict of measurable signals. If the org has no public NPM packages,
    all fields default to empty / zero / False — no special-case error required.

    HTTP cost: 1 search call + up to top_n metadata calls. For a 20-package org,
    roughly 21 calls × ~200ms = ~5s per company on top of the GitHub scan.
    """
    if not org_name:
        return _empty_result()

    org_slug = org_name.lower()
    org_scope_prefix = f"@{org_slug}/"
    search_query = quote(org_scope_prefix, safe="")  # URL-encode @ and /

    try:
        r = requests.get(NPM_SEARCH_URL.format(query=search_query), timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return _empty_result(error=f"npm search failed: {e}")

    raw_objects = data.get("objects") or []
    if not raw_objects:
        return _empty_result(org_name=org_slug)

    # NPM's search returns substring matches against package names — we still get
    # noise (e.g., searching "@sentry/" can return matches that aren't in the
    # @sentry scope). Post-filter to packages whose name starts with @<org>/.
    objects = [
        obj for obj in raw_objects
        if obj.get("package", {}).get("name", "").lower().startswith(org_scope_prefix)
    ]
    if not objects:
        return _empty_result(org_name=org_slug)

    # NPM search results are sorted by a relevance score that is heavily weighted
    # toward popularity (~0.98 of the final score per NPM's published weights),
    # so the top N is a reasonable proxy for top-N-by-downloads without making
    # N extra HTTP calls to the downloads API. Exact download sorting is a v3
    # refinement — see BETS.md Bet 1.
    top_pkgs = objects[:top_n]
    package_names = [p["package"]["name"] for p in top_pkgs]

    # Design-system primitive detection — a single hit fires strong corroboration.
    ds_packages = [n for n in package_names if _is_design_system_name(n)]

    # Cross-referential check: do any of these packages list other @<org>/*
    # packages in dependencies or devDependencies?
    cross_ref_pairs = []
    for pkg in top_pkgs:
        full_name = pkg["package"]["name"]
        try:
            meta_r = requests.get(
                NPM_METADATA_URL.format(full_name=quote(full_name, safe="@/")),
                timeout=10,
            )
            meta_r.raise_for_status()
            meta = meta_r.json()
        except Exception:
            continue

        latest_version = (meta.get("dist-tags") or {}).get("latest")
        if not latest_version:
            continue
        version_block = (meta.get("versions") or {}).get(latest_version) or {}
        deps = {
            **(version_block.get("dependencies") or {}),
            **(version_block.get("devDependencies") or {}),
        }
        internal_deps = [
            d for d in deps.keys()
            if d.startswith(org_scope_prefix) and d != full_name
        ]
        if internal_deps:
            # Record one example pair per package to keep evidence short.
            cross_ref_pairs.append((full_name, internal_deps[0]))

    return {
        "npm_org_name": org_slug,
        "npm_org_exists": True,
        "npm_package_count": len(objects),
        "npm_top_packages": package_names,
        "npm_cross_referential_count": len(cross_ref_pairs),
        "npm_cross_referential_pairs": cross_ref_pairs[:3],  # cap for evidence rendering
        "npm_design_system_packages": ds_packages[:3],
    }


def _empty_result(org_name: str = "", error: str = None) -> dict:
    result = {
        "npm_org_name": org_name,
        "npm_org_exists": False,
        "npm_package_count": 0,
        "npm_top_packages": [],
        "npm_cross_referential_count": 0,
        "npm_cross_referential_pairs": [],
        "npm_design_system_packages": [],
    }
    if error:
        result["npm_error"] = error
    return result


if __name__ == "__main__":
    import json
    import sys
    org = sys.argv[1] if len(sys.argv) > 1 else "sentry"
    print(json.dumps(scan(org), indent=2, default=str))

"""Print raw signal values for all validation companies + mean/median.

Run: python3 analyze_validation.py
"""
import statistics
import yaml
from dotenv import load_dotenv

from github_scan import scan_org
from careers_scan import scan as scan_careers

load_dotenv()

with open("validation-seeds.yml") as f:
    data = yaml.safe_load(f) or {}

companies = data.get("companies", [])
results = []

print(f"Scanning {len(companies)} companies (this takes 5-10 min)...\n")

for c in companies:
    print(f"  → {c['name']}")
    gh = scan_org(c["github_org"])
    careers = scan_careers(c)
    results.append({
        "name": c["name"],
        "repo_count": gh.get("repo_count", 0),
        "contributors": gh.get("unique_contributors_top5", 0),
        "eng_roles": careers.get("open_engineering_roles", 0),
        "commits_per_week": gh.get("avg_commits_per_week", 0),
        "employee_estimate": c.get("employee_estimate", 0),
    })

print("\n" + "=" * 95)
print(f"{'Company':<18} {'Repos':>7} {'Contribs':>10} {'EngRoles':>10} {'CommitsWk':>11} {'Employees':>11}")
print("=" * 95)
for r in results:
    print(f"{r['name']:<18} {r['repo_count']:>7} {r['contributors']:>10} {r['eng_roles']:>10} {r['commits_per_week']:>11.1f} {r['employee_estimate']:>11}")
print("=" * 95)


def fmt_stats(field):
    vals = [r[field] for r in results]
    return {
        "mean": statistics.mean(vals),
        "median": statistics.median(vals),
        "min": min(vals),
        "max": max(vals),
        "p25": statistics.quantiles(vals, n=4)[0],
        "p75": statistics.quantiles(vals, n=4)[2],
    }


print("\n" + "=" * 95)
print(f"{'Signal':<20} {'Mean':>10} {'Median':>10} {'p25':>10} {'p75':>10} {'Min':>8} {'Max':>8}")
print("=" * 95)
for field in ["repo_count", "contributors", "eng_roles", "commits_per_week", "employee_estimate"]:
    s = fmt_stats(field)
    print(f"{field:<20} {s['mean']:>10.1f} {s['median']:>10.1f} {s['p25']:>10.1f} {s['p75']:>10.1f} {s['min']:>8} {s['max']:>8}")
print("=" * 95)
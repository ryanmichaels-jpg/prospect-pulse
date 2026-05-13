"""One-shot diagnostic for the Work-at-a-Startup scanner.

Probes workatastartup.com/companies/adam, prints the HTTP status, response
size, whether the 'is hiring for N jobs' pattern is found, and the first
300 characters of the response body. Used to determine whether the scanner's
silent failure is a 403/anti-bot issue, a regex mismatch, or something else.

Run with: python3 diagnose_waas.py
"""
import re
import requests

URL = "https://www.workatastartup.com/companies/adam"

print(f"Fetching: {URL}")
print()

# First: try with NO user-agent (matches the current scanner behavior)
print("=== Attempt 1: default requests UA ===")
try:
    r = requests.get(URL, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Length: {len(r.text)}")
    m = re.search(r"is hiring for (\d+) jobs?", r.text, re.IGNORECASE)
    print(f"Pattern: {m.group(0) if m else 'NOT FOUND'}")
    print(f"First 300 chars:\n{r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== Attempt 2: with a real browser User-Agent ===")
try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    r = requests.get(URL, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Length: {len(r.text)}")
    m = re.search(r"is hiring for (\d+) jobs?", r.text, re.IGNORECASE)
    print(f"Pattern: {m.group(0) if m else 'NOT FOUND'}")
    print(f"First 300 chars:\n{r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")

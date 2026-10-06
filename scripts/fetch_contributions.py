"""Scrape the public contribution calendar (no token) -> data/contributions.json."""
import json
import re
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

USER = "MeAnandCB"
URL = f"https://github.com/users/{USER}/contributions"

html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
html.raise_for_status()
soup = BeautifulSoup(html.text, "html.parser")

counts = {}
for tip in soup.find_all("tool-tip"):
    m = re.match(r"(\d+) contribution", tip.get_text(strip=True))
    counts[tip.get("for")] = int(m.group(1)) if m else 0

days = []
for td in soup.select("td.ContributionCalendar-day"):
    if not td.get("data-date"):
        continue
    days.append({"date": td["data-date"], "level": int(td["data-level"]),
                 "count": counts.get(td.get("id"), 0)})
days.sort(key=lambda d: d["date"])
if not days:
    raise SystemExit("no contribution cells found - GitHub markup may have changed")

total = sum(d["count"] for d in days)
longest = cur = 0
for d in days:
    cur = cur + 1 if d["count"] else 0
    longest = max(longest, cur)
# current streak: today may still be empty, so allow it to be skipped
current = 0
for d in reversed(days):
    if d["count"]:
        current += 1
    elif d is days[-1]:
        continue
    else:
        break
months = {}
for d in days:
    months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]
best = max(days, key=lambda d: d["count"])

json.dump({"user": USER, "total": total, "current_streak": current, "longest_streak": longest,
           "best_day": best, "months": months, "days": days},
          open("data/contributions.json", "w"), indent=1)
print(f"{len(days)} days, {total} contributions, longest streak {longest}")

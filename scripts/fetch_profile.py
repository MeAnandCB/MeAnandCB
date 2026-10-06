"""Public profile + repo data (no token needed; uses GITHUB_TOKEN if present) -> data/profile.json."""
import json
import os
from collections import Counter

import requests

USER = "MeAnandCB"
H = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
if os.environ.get("GITHUB_TOKEN"):
    H["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"

def get(url):
    r = requests.get(url, headers=H, timeout=30)
    r.raise_for_status()
    return r.json()

u = get(f"https://api.github.com/users/{USER}")
repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed")
own = [r for r in repos if not r["fork"]]
langs = Counter(r["language"] for r in own if r["language"])

json.dump({
    "name": u["name"], "bio": u["bio"], "location": u["location"],
    "repos": u["public_repos"], "followers": u["followers"], "following": u["following"],
    "created_at": u["created_at"],
    "stars": sum(r["stargazers_count"] for r in own),
    "forks": len(repos) - len(own),
    "languages": langs.most_common(6),
    "recent": [{"name": r["name"], "language": r["language"], "pushed_at": r["pushed_at"]}
               for r in own[:5]],
}, open("data/profile.json", "w"), indent=1)
print(f"{u['public_repos']} repos, {u['followers']} followers, top langs {langs.most_common(3)}")

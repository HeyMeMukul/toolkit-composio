#!/usr/bin/env python3
import json
import glob
import os
from collections import Counter, defaultdict

def main():
    print("Aggregating patterns...")
    verified_files = glob.glob("data/verified/*.json")
    
    if not verified_files:
        print("No verified records found. Outputting empty patterns.")
        with open("data/patterns.json", "w") as f:
            json.dump({}, f)
        return

    auth_counter = Counter()
    access_modes = Counter()
    category_access = defaultdict(lambda: Counter())
    blockers = Counter()
    easy_wins = []
    blocked_apps = []

    for path in verified_files:
        with open(path, 'r') as f:
            data = json.load(f)
            
            # Auth
            for auth in data.get("auth_methods", []):
                auth_counter[auth.get("type")] += 1
                
            # Access
            access_mode = data.get("access", {}).get("mode", "unknown")
            access_modes[access_mode] += 1
            
            # Category vs Access
            category = data.get("category", "Uncategorized")
            category_access[category][access_mode] += 1
            
            # Blockers & Wins
            build = data.get("buildability", {})
            verdict = build.get("verdict")
            if verdict == "blocked":
                blocker = build.get("blocker", "unknown")
                if blocker:
                    blockers[blocker] += 1
                blocked_apps.append(data.get("app_name"))
            elif verdict == "ready":
                easy_wins.append(data.get("app_name"))

    patterns = {
        "auth_dominance": dict(auth_counter.most_common()),
        "overall_access": dict(access_modes),
        "category_access": {k: dict(v) for k, v in category_access.items()},
        "common_blockers": dict(blockers.most_common()),
        "easy_wins": easy_wins,
        "blocked_apps": blocked_apps,
        "total_analyzed": len(verified_files)
    }

    with open("data/patterns.json", "w") as f:
        json.dump(patterns, f, indent=2)
    print(f"Aggregated {len(verified_files)} records into data/patterns.json")

if __name__ == "__main__":
    main()

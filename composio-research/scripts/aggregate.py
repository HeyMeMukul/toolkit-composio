#!/usr/bin/env python3
"""
aggregate.py - Produces data/patterns.json from data/verified/*.json
This script computes all the patterns the report-builder needs.
It runs deterministically - no LLM calls, just data crunching.
"""
import json
import glob
import os
from collections import Counter, defaultdict

def classify_blocker(blocker_text):
    """Group raw blocker strings into logical categories."""
    if not blocker_text:
        return "unknown"
    text = blocker_text.lower()
    if any(w in text for w in ["partner", "contact", "sales", "enterprise", "contract"]):
        return "Enterprise contracts / Contact sales"
    if any(w in text for w in ["paid", "subscription", "plan", "pricing", "premium"]):
        return "Paid subscription required"
    if any(w in text for w in ["approval", "review", "apply", "program", "developer token"]):
        return "Manual approval / Developer review"
    if any(w in text for w in ["waitlist", "beta", "invite"]):
        return "Waitlist / Beta access"
    return "Other"

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
    category_auth = defaultdict(lambda: Counter())
    category_buildability = defaultdict(lambda: Counter())
    raw_blockers = Counter()
    grouped_blockers = Counter()
    blocker_examples = defaultdict(list)
    easy_wins = []
    easy_wins_by_category = defaultdict(list)
    blocked_apps = []
    blocked_apps_detail = []
    partial_apps = []
    all_apps_summary = []

    for path in verified_files:
        with open(path, 'r') as f:
            data = json.load(f)
            
            app_name = data.get("app_name", "Unknown")
            app_id = data.get("app_id", "unknown")
            category = data.get("category", "Uncategorized")
            
            # Auth
            auth_types = []
            for auth in data.get("auth_methods", []):
                auth_type = auth.get("type", "unknown")
                auth_counter[auth_type] += 1
                category_auth[category][auth_type] += 1
                auth_types.append(auth_type)
                
            # Access
            access = data.get("access", {})
            access_mode = access.get("mode", "unknown")
            gate_type = access.get("gate_type", "none")
            evidence_url = access.get("evidence_url", "")
            access_modes[access_mode] += 1
            category_access[category][access_mode] += 1
            
            # Buildability
            build = data.get("buildability", {})
            verdict = build.get("verdict", "unknown")
            blocker = build.get("blocker", "")
            category_buildability[category][verdict] += 1
            
            if verdict == "blocked":
                raw_blockers[blocker] += 1
                group = classify_blocker(blocker)
                grouped_blockers[group] += 1
                if len(blocker_examples[group]) < 3:
                    blocker_examples[group].append({"app": app_name, "detail": blocker})
                blocked_apps.append(app_name)
                blocked_apps_detail.append({"app": app_name, "category": category, "blocker": blocker})
            elif verdict == "partial":
                partial_apps.append({"app": app_name, "category": category, "blocker": blocker})
            elif verdict == "ready":
                easy_wins.append(app_name)
                easy_wins_by_category[category].append(app_name)

            # Evidence URL for the table
            evidence_from_access = evidence_url
            evidence_from_array = ""
            evidence_arr = data.get("evidence", [])
            if evidence_arr and len(evidence_arr) > 0:
                evidence_from_array = evidence_arr[0].get("url", "")
            
            final_evidence = evidence_from_access or evidence_from_array or data.get("website", "")

            all_apps_summary.append({
                "app_id": app_id,
                "app_name": app_name,
                "category": category,
                "one_liner": data.get("one_liner", ""),
                "auth_methods": ", ".join(auth_types),
                "access_mode": access_mode,
                "gate_type": gate_type,
                "api_type": data.get("api_surface", {}).get("type", "unknown"),
                "api_breadth": data.get("api_surface", {}).get("breadth", "unknown"),
                "mcp_exists": data.get("mcp_status", {}).get("exists", False),
                "mcp_source": data.get("mcp_status", {}).get("source", "none"),
                "buildability": verdict,
                "blocker": blocker,
                "evidence_url": final_evidence,
                "confidence": data.get("confidence", "agent_only")
            })

    # Sort apps alphabetically
    all_apps_summary.sort(key=lambda x: x["app_name"].lower())

    # Identify hard categories (those with highest % of gated apps)
    hard_categories = []
    for cat, access_counts in category_access.items():
        total = sum(access_counts.values())
        gated = access_counts.get("gated", 0)
        if gated > 0:
            hard_categories.append({
                "category": cat,
                "gated_count": gated,
                "total": total,
                "gated_pct": round(100 * gated / total, 1),
                "blocked_count": category_buildability[cat].get("blocked", 0)
            })
    hard_categories.sort(key=lambda x: x["gated_pct"], reverse=True)

    patterns = {
        "auth_dominance": dict(auth_counter.most_common()),
        "overall_access": dict(access_modes),
        "category_access": {k: dict(v) for k, v in category_access.items()},
        "category_auth": {k: dict(v) for k, v in category_auth.items()},
        "category_buildability": {k: dict(v) for k, v in category_buildability.items()},
        "grouped_blockers": dict(grouped_blockers.most_common()),
        "blocker_examples": {k: v for k, v in blocker_examples.items()},
        "raw_blockers": dict(raw_blockers.most_common()),
        "easy_wins": easy_wins,
        "easy_wins_by_category": {k: v for k, v in easy_wins_by_category.items()},
        "blocked_apps": blocked_apps,
        "blocked_apps_detail": blocked_apps_detail,
        "partial_apps": partial_apps,
        "hard_categories": hard_categories,
        "all_apps_summary": all_apps_summary,
        "total_analyzed": len(verified_files)
    }

    with open("data/patterns.json", "w") as f:
        json.dump(patterns, f, indent=2)
    print(f"Aggregated {len(verified_files)} records into data/patterns.json")

if __name__ == "__main__":
    main()

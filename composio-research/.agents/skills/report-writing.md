---
name: report-writing
description: Skill for building the final HTML Product Ops Case Study report.
---
# Role
You are the report-builder agent. Your job is to produce the final HTML deliverable.

# Hard rules
- Do NOT write HTML by hand. Run the deterministic report generator script instead.
- The script handles all structure, styling, evidence links, confidence badges, insights, and verification caveats.
- Your only job is to run the two scripts in order and confirm the output.

# Process
1. Run `python3 scripts/aggregate.py` to produce `data/patterns.json` from `data/verified/*.json`.
2. Run `node scripts/generate_report.js` to produce `output/report.html` from `data/patterns.json` and `output/verification_log.json`.
3. Confirm the file was written and reply with the app count.

# Customization
- To change the GitHub repo URL: `node scripts/generate_report.js --repo-url=https://github.com/YOUR/REPO`
- To change the report structure or styling: edit `scripts/generate_report.js` directly.

# What the script guarantees
The generated report always includes:
1. Executive Summary with deep product insights (auto-generated from data patterns)
2. Category Breakdown with auth distribution and Hard Categories table
3. Easy Wins section with category-level explanation
4. Common Blockers grouped logically with examples
5. Apps That Defeated the Agent with per-app reasons
6. Agent Pipeline with Mermaid.js flowchart and honest human-intervention details
7. Verification Process with accuracy stats, caveat about sample size, and specific mismatches
8. Full App Matrix with ALL columns: #, App, Category, One-Liner, Auth, Access, API, MCP, Buildability, Evidence (🔗), Confidence (badge)

# Failure handling
If aggregate.py or generate_report.js fails, read the error output and fix the issue. Common fixes:
- Missing `data/verified/` files: ensure the promotion step ran
- Missing `output/verification_log.json`: create an empty array `[]` file

---
name: report-writing
description: Skill for building the final HTML report.
---
# Role
You are the report-builder agent, responsible for writing the final HTML deliverable.

# Hard rules
- Write/rewrite `output/report.html` from scratch each time you run.
- Do NOT recompute or alter numbers from `data/patterns.json`. Only present them.
- Ensure the output is ONE self-contained HTML file.
- Use inline CSS (no build step).
- No dependency on anything not loaded via CDN.
- Use semantic headings, readable by humans and parseable by machines (consider a JSON-LD or script block with findings).

# Requirements for Report Output
The output must independently make clear:
1. The headline patterns, stated plainly, at the very top — before the table (e.g., dominant auth, gated vs self-serve categories, common blockers, easy wins).
2. A clean, skimmable table/matrix of all 100 apps. You MUST add an "Evidence" column (or a 🔗 icon) to every row linking to the `access.evidence_url` or `evidence[0].url` from the verified JSON. Do NOT use '-' for evidence links. Every row MUST have a valid URL link. You MUST also add a "Confidence" column/badge to every row (`agent_verified`, `agent_only`, or `human_corrected`) based on the `confidence` field in the JSON.
3. An explanation of the agent pipeline itself — what it is, where a human was needed. You MUST use exactly these links: Repo: `https://github.com/cyb3rfy/composio-research`, Trigger: `https://github.com/cyb3rfy/composio-research/actions/workflows/pipeline.yml`.
4. The verification section: accuracy on the sample, shown honestly including misses, with the v1-to-v2 improvement explicitly stated and explained. You MUST explicitly state: "Verified on a stratified sample of 20/100 apps; pass-2 reflects post-correction accuracy on that sample, not a guarantee the other 80 are error-free."
5. Any app that defeated the agent, stated plainly, not buried.

# Process
1. Read `data/verified/*.json`, `data/patterns.json`, `data/narrative.json`, and `output/verification_log.json`.
2. Synthesize the data into the HTML structure.
3. Overwrite `output/report.html`.

# Output format
A single, self-contained HTML file.

# Failure handling
If any input file is missing or malformed, use fallback placeholder text for that section, clearly marking it as data missing in the HTML.

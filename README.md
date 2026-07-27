# Composio AI Product Ops Intern Assignment - SaaS Research Pipeline

This repository contains my submission for the Composio AI Product Ops Intern take-home assignment. It implements a fully autonomous, scalable multi-agent pipeline to research 100 SaaS applications, verify the findings, and generate a final HTML report.

## Repository Structure

This repository contains two main folders:

1. **`composio-research/`**: This is the core project repository where the multi-agent pipeline, orchestration scripts, and generated data/reports live. 
2. **`100-web-test/`**: This is the original repository provided as part of the assignment prompt.

To run the pipeline or view the output, navigate into the `composio-research` directory.

## How We Implemented the Pipeline

Instead of a simple script, we built a robust, scalable multi-agent orchestration architecture to handle the 100 apps efficiently and accurately:

1. **Pass 1: Research Workers** 
   - We utilized a central task queue (`data/state/task_queue.json`) to manage the 100 apps.
   - We dispatched multiple parallel `research-worker` subagents, grouped in batches of 5. These agents used live web-browsing and tool calls to research the auth methods, API surface, access gates, and MCP status of each app, saving the raw output to `data/raw/`.

2. **Pass 2: The Verification Loop (Human-in-the-Loop Proxy)**
   - To ensure the rigor requested by the assignment, we did not blindly trust Pass 1. 
   - A `scripts/build_verification_sample.js` script generated a stratified statistical sample of 20 apps (2 per category).
   - We invoked independent `verifier` agents to audit this sample. The verifiers re-fetched the evidence URLs and cross-checked the data, successfully correcting hallucinations (e.g., misattributed GitHub repos) and pushing the corrected data to `data/verified/`. The un-sampled apps were promoted with an "Agent Only" confidence badge for transparency.

3. **Pass 3: Report Generation**
   - An `aggregate.py` script synthesized the verified data into core patterns (dominant auth, blockers, easy wins).
   - Finally, a `report-builder` agent ingested the aggregated patterns, the verified JSONs, and the verification logs to autonomously code the final deliverable: a clean, inline-CSS HTML matrix (`output/report.html`) complete with working Evidence URLs and Confidence badges.

## Viewing the Final Report
The final deliverable is located at: `composio-research/output/report.html`.

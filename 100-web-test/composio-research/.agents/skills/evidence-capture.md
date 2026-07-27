---
name: evidence-capture
description: Skill outlining how to capture and store evidence for claims.
---
# Role
Guidance for any agent that fetches a web page and needs to cite it as evidence.

# Hard rules
- Save snapshots of the evidence to `data/evidence/{app_id}/{field}.txt`.
- Store metadata alongside the claim in the schema: source URL and `accessed_at` timestamp.
- Claims must be paraphrased from evidence. NEVER use long verbatim copy-paste of docs pages. This ensures cleanliness and respects copyright/docs ownership.

# Process
1. When you find the information answering a schema field on a webpage, summarize/paraphrase the key points.
2. Save a brief snippet/snapshot of the relevant context to `data/evidence/{app_id}/{field}.txt`.
3. Ensure the JSON record contains the exact `url` and `accessed_at` timestamp for that field's evidence.

# Output format
Text files in `data/evidence/{app_id}/` containing short paraphrased snapshots.

# Failure handling
If saving the snapshot fails, ensure the URL and timestamp are still accurately recorded in the JSON, and note the snapshot failure in the app's `notes`.

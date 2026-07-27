import json

with open('data/raw/jira.json') as f:
    data = json.load(f)

# Update MCP URL
data['mcp_status']['url'] = 'https://github.com/atlassian/atlassian-mcp-server'

# Update fields
data['research_pass'] = 2
data['confidence'] = 'agent_verified'

# Evidence update: Add mcp_status evidence because we corrected it.
import datetime
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

data['evidence'].append({
    "claim_field": "mcp_status",
    "url": "https://github.com/atlassian/atlassian-mcp-server",
    "snapshot_path": "web_search",
    "accessed_at": now
})

with open('data/verified/jira.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('output/verification_log.json', 'r') as f:
    logs = json.load(f)

logs.append({
    "app_id": "jira",
    "timestamp": now,
    "fields_checked": 5,
    "mismatches": 1,
    "details": {
        "auth_methods": "match",
        "access": "match",
        "api_surface": "match",
        "mcp_status": "mismatch: URL corrected from https://github.com/atlassian/mcp-server-jira (404) to https://github.com/atlassian/atlassian-mcp-server",
        "buildability": "match"
    }
})

with open('output/verification_log.json', 'w') as f:
    json.dump(logs, f, indent=2)

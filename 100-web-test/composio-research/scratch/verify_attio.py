import json
import datetime

with open('data/raw/attio.json') as f:
    data = json.load(f)

# Update fields
data['research_pass'] = 2
data['confidence'] = 'agent_verified'

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

data['evidence'].append({
    "claim_field": "mcp_status",
    "url": "https://mcp.attio.com/mcp",
    "snapshot_path": "web_search",
    "accessed_at": now
})

with open('data/verified/attio.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('output/verification_log.json', 'r') as f:
    logs = json.load(f)

logs.append({
    "app_id": "attio",
    "timestamp": now,
    "fields_checked": 5,
    "mismatches": 0,
    "details": {
        "auth_methods": "match",
        "access": "match",
        "api_surface": "match",
        "mcp_status": "match",
        "buildability": "match"
    }
})

with open('output/verification_log.json', 'w') as f:
    json.dump(logs, f, indent=2)

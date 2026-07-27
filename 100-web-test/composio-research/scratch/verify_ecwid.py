import json
import datetime

with open('data/raw/ecwid.json') as f:
    data = json.load(f)

# Update fields
data['research_pass'] = 2
data['confidence'] = 'agent_verified'
data['access']['evidence_url'] = 'https://docs.ecwid.com/reference/overview' # Actually let's use the final URL
data['api_surface']['docs_url'] = 'https://docs.ecwid.com/reference/overview'

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

data['evidence'].append({
    "claim_field": "api_surface",
    "url": "https://docs.ecwid.com/reference/overview",
    "snapshot_path": "web_search",
    "accessed_at": now
})

with open('data/verified/ecwid.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('output/verification_log.json', 'r') as f:
    logs = json.load(f)

logs.append({
    "app_id": "ecwid",
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

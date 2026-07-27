import json
import datetime

with open('data/raw/podio.json') as f:
    data = json.load(f)

# Update fields
data['research_pass'] = 2
data['confidence'] = 'agent_verified'
data['access']['evidence_url'] = 'https://developers.podio.com'

data['mcp_status']['exists'] = True
data['mcp_status']['source'] = 'community'
data['mcp_status']['url'] = 'https://github.com/stoskov/podio-mcp'

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

data['evidence'].append({
    "claim_field": "mcp_status",
    "url": "https://github.com/stoskov/podio-mcp",
    "snapshot_path": "web_search",
    "accessed_at": now
})
data['evidence'].append({
    "claim_field": "access",
    "url": "https://developers.podio.com",
    "snapshot_path": "web_search",
    "accessed_at": now
})

with open('data/verified/podio.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('output/verification_log.json', 'r') as f:
    logs = json.load(f)

logs.append({
    "app_id": "podio",
    "timestamp": now,
    "fields_checked": 5,
    "mismatches": 2,
    "details": {
        "auth_methods": "match",
        "access": "mismatch: evidence_url 301 redirected, corrected to https://developers.podio.com",
        "api_surface": "match",
        "mcp_status": "mismatch: corrected from exists:false to exists:true, community, url: https://github.com/stoskov/podio-mcp",
        "buildability": "match"
    }
})

with open('output/verification_log.json', 'w') as f:
    json.dump(logs, f, indent=2)

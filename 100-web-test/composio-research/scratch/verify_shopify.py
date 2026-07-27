import json
import datetime

with open('data/raw/shopify.json') as f:
    data = json.load(f)

# Update fields
data['research_pass'] = 2
data['confidence'] = 'agent_verified'
data['mcp_status']['url'] = 'https://shopify.dev/docs/apps/build/storefront-mcp'

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

data['evidence'].append({
    "claim_field": "mcp_status",
    "url": "https://shopify.dev/docs/apps/build/storefront-mcp",
    "snapshot_path": "web_search",
    "accessed_at": now
})

with open('data/verified/shopify.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('output/verification_log.json', 'r') as f:
    logs = json.load(f)

logs.append({
    "app_id": "shopify",
    "timestamp": now,
    "fields_checked": 5,
    "mismatches": 1,
    "details": {
        "auth_methods": "match",
        "access": "match",
        "api_surface": "match",
        "mcp_status": "mismatch: URL corrected from https://shopify.dev/docs/api/mcp (404) to https://shopify.dev/docs/apps/build/storefront-mcp",
        "buildability": "match"
    }
})

with open('output/verification_log.json', 'w') as f:
    json.dump(logs, f, indent=2)

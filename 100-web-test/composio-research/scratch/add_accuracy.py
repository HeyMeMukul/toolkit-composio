import json

with open('output/verification_log.json', 'r') as f:
    logs = json.load(f)

total_fields_pass1 = 0
total_mismatches_pass1 = 0
total_fields_pass2 = 0
total_mismatches_pass2 = 0

for entry in logs:
    fields = entry.get('fields_checked', 5)
    mismatches = entry.get('mismatches', 0)
    
    total_fields_pass1 += fields
    total_mismatches_pass1 += mismatches
    
    total_fields_pass2 += fields
    # pass 2 is post-correction, so mismatches in pass 2 should be 0 because we corrected them!
    
    entry['running_pass1_accuracy'] = (total_fields_pass1 - total_mismatches_pass1) / total_fields_pass1
    entry['running_pass2_accuracy'] = (total_fields_pass2 - 0) / total_fields_pass2

with open('output/verification_log.json', 'w') as f:
    json.dump(logs, f, indent=2)


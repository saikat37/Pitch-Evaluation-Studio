#!/usr/bin/env python3
"""Fix JSON escaping in prompts.py"""

with open('prompts.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
for line in lines:
    # If line contains ("assistant", and has {"score"
    if '("assistant",' in line or (line.strip().startswith("'") and '{"score"' in line):
        # Replace { with {{ and } with }}
        line = line.replace('{"score"', '{{"score"')
        line = line.replace('"}\')', '"}}\')')
        line = line.replace(', "reason":', ', "reason":')  # Don't escape inside
        line = line.replace('"}}\')', '"}}\')') 
        # Fix: properly escape
        if '{{"score"' in line and not '{{\"score\"' in line:
            line = line.replace('{{"score"', '{{\"score\"')
            line = line.replace('"}}\')' , '\"}}\')') 
            line = line.replace('", "', '\", \"')
    
    # Handle structure assistant line
    if '{"hook_present"' in line:
        line = line.replace('\'{"', '\'{{"')
        line = line.replace('}"}\')', '}}"}\')')
        line = line.replace('", "', '\", \"')
        line = line.replace(': "', ': \"')
        line = line.replace('", [', '\", [')
        line = line.replace('], "', '], \"')
    
    output.append(line)

with open('prompts.py', 'w', encoding='utf-8') as f:
    f.writelines(output)

print("✅ Fixed JSON escaping in prompts.py")

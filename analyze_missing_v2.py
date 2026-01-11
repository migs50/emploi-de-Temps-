import json
from collections import Counter

seances = json.load(open('DONNÉES PRINCIPALES/seances.json', encoding='utf-8'))
edt = json.load(open('GESTION EDT/emplois_du_temps.json', encoding='utf-8'))

# simple count
required_counts = Counter()
for s in seances:
    key = s.get('type', 'Cours')
    required_counts[key] += 1

scheduled_counts = Counter()
for s in edt:
    # "type" isn't always preserved in edt? Let's assume we can infer or it's there.
    # If not there, we can look up the "module" from seances to find the type? 
    # Actually, let's just count the deficit by comparing seance objects.
    # But matching is hard without IDs.
    pass

# Alternative: Check which seances from the input list are NOT in the output list
# We can use a signature: module_id + group_id + type
# But wait, edt_generator splits groups? No, it works on "groupe" string.

def get_sig(s):
    # module logic might use ID or name
    # seances.json has "module" (name) and "module_id"
    # edt has "module" (name)
    m = s.get('module')
    g = s.get('groupe')
    e = s.get('enseignant')
    # Use these 3 as signature
    return f"{m}|{g}|{e}"

scheduled_sigs = Counter()
for s in edt:
    scheduled_sigs[get_sig(s)] += 1

missing_types = Counter()

for s in seances:
    sig = get_sig(s)
    if scheduled_sigs[sig] > 0:
        scheduled_sigs[sig] -= 1
    else:
        # This seance is missing
        # Try to infer type from 'type' field in seances.json
        t = s.get('type', 'Unknown')
        missing_types[t] += 1

print("MISSING_SUMMARY_START")
for t, count in missing_types.items():
    print(f"{t}: {count}")
print("MISSING_SUMMARY_END")

import json
from collections import Counter

seances = json.load(open('DONNÉES PRINCIPALES/seances.json', encoding='utf-8'))
edt = json.load(open('GESTION EDT/emplois_du_temps.json', encoding='utf-8'))

# Create a set of placed session IDs (assuming we can track them, but seances.json has IDs, edt might not preserve them exactly or logic is tricky)
# edt_generator doesn't seem to preserve the 'id' from seances.json in the output?
# Let's check edt_generator.py logic. It copies data.
# If ID is not preserved, we have to match by content.

# edt entries: {"module":..., "enseignant":..., "groupe":..., "type":...}
# Let's use a hashed signature

placed_sigs = []
for s in edt:
    # Signature: module + penseignant + groupe + type
    # Note: edt keys might differ slightly.
    # In edt_generator.py:
    # nouvelle_seance = { "module": seance["module"], "enseignant":..., "groupe":..., "type":... }
    # seance["type"] is in seances.json?
    # Let's check seances.json structure again.
    sig = f"{s.get('module')}|{s.get('enseignant')}|{s.get('groupe')}|{s.get('type')}"
    placed_sigs.append(sig)

placed_counter = Counter(placed_sigs)

missing_stats = Counter()
missing_teachers = Counter()
missing_groups = Counter()

for s in seances:
    sig = f"{s.get('module')}|{s.get('enseignant')}|{s.get('groupe')}|{s.get('type')}"
    if placed_counter[sig] > 0:
        placed_counter[sig] -= 1
    else:
        missing_stats[s.get('type', 'Unknown')] += 1
        missing_teachers[s.get('enseignant', 'Unknown')] += 1
        missing_groups[s.get('groupe', 'Unknown')] += 1

with open('missing_report.txt', 'w', encoding='utf-8') as f:
    f.write(f"Missing by Type: {missing_stats}\n")
    f.write(f"Top 5 Missing Teachers: {missing_teachers.most_common(5)}\n")
    f.write(f"Top 5 Missing Groups: {missing_groups.most_common(5)}\n")

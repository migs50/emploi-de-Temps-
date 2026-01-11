import json

with open('GESTION EDT/emplois_du_temps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for s in data:
    if "Youssef Bennouna" in s.get("enseignant", ""):
        count += 1

print(f"Total sessions for Youssef Bennouna: {count}")

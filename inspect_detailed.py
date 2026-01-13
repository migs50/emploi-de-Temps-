import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
TARGETS = ['BCG-2', 'SSD-1', 'AAIS-1', 'GEMI-2']

def inspect():
    with open(EDT_PATH, 'r', encoding='utf-8') as f:
        edt = json.load(f)
    
    with open("detailed_inspection.txt", "w", encoding='utf-8') as out:
        for t in TARGETS:
            out.write(f"\nFiliere: {t}\n")
            data = [s for s in edt if s.get('filiere') == t]
            data.sort(key=lambda x: (x.get('jour'), x.get('debut')))
            for s in data:
                out.write(f"  {s['jour']} {s['debut']}-{s['fin']} | Mod: {s['module']} | Type: {s['type']} | Group: {s.get('groupe')} | Prof: {s['enseignant']}\n")

if __name__ == "__main__":
    inspect()

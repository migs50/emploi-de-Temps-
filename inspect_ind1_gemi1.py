import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
TARGETS = ['IND-1', 'GEMI-1']

def inspect():
    with open(EDT_PATH, 'r', encoding='utf-8') as f:
        edt = json.load(f)
    
    with open("detailed_inspection_ind1_gemi1.txt", "w", encoding='utf-8') as out:
        for t in TARGETS:
            out.write(f"\nFiliere: {t}\n")
            data = [s for s in edt if s.get('filiere') == t]
            data.sort(key=lambda x: (x.get('jour'), x.get('debut')))
            for s in data:
                out.write(f"  {s['jour']} {s['debut']}-{s['fin']} | Mod: {s['module']} | Type: {s['type']} | Prof: {s['enseignant']}\n")

if __name__ == "__main__":
    inspect()

import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
TARGETS = ['IND-1', 'GEMI-1']

def count_sessions():
    with open(EDT_PATH, 'r', encoding='utf-8') as f:
        edt = json.load(f)
    
    for t in TARGETS:
        sessions = [s for s in edt if s.get('filiere') == t]
        mods = sorted(list(set(s['module'] for s in sessions)))
        print(f"\nFiliere: {t}")
        for m in mods:
            c = len([s for s in sessions if s['module'] == m and s.get('type') == 'Cours'])
            td = len([s for s in sessions if s['module'] == m and s.get('type') == 'TD'])
            print(f"  Module: {m} | Cours: {c} | TD: {td}")

if __name__ == "__main__":
    count_sessions()

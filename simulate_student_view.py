import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
TARGETS = ['IND-1', 'GEMI-1', 'BCG-2', 'SSD-1', 'AAIS-1', 'GEMI-2']

def simulate():
    with open(EDT_PATH, 'r', encoding='utf-8') as f:
        edt = json.load(f)
    
    for filiere in TARGETS:
        print(f"\nComparing View for Filiere: {filiere}")
        groups = sorted(list(set(s.get('groupe') for s in edt if s.get('filiere') == filiere)))
        if not groups:
            # If no group entry, the student interface logic usually shows nothing or just the filiere
            groups = [filiere]
            
        for group in groups:
            my_sessions = []
            for s in edt:
                if s.get('groupe') == group or (s.get('filiere') == filiere and s.get('type') == 'Cours'):
                    my_sessions.append(s)
            
            cours_modules = sorted(list(set(s['module'] for s in my_sessions if s.get('type') == 'Cours')))
            td_modules = sorted(list(set(s['module'] for s in my_sessions if s.get('type') == 'TD')))
            
            print(f"  Selected Group: {group}")
            print(f"    Visible Cours ({len(cours_modules)}): {cours_modules}")
            print(f"    Visible TDs   ({len(td_modules)}): {td_modules}")

if __name__ == "__main__":
    simulate()

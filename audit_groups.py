import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
TARGETS = ['BCG-2', 'SSD-1', 'AAIS-1', 'GEMI-2']

def audit_groups():
    with open(EDT_PATH, 'r', encoding='utf-8') as f:
        edt = json.load(f)
    
    with open("group_audit_final.txt", "w", encoding='utf-8') as out:
        for t in TARGETS:
            filiere_sessions = [s for s in edt if s.get('filiere') == t]
            groups = sorted(list(set(s.get('groupe') for s in filiere_sessions)))
            out.write(f"\nFiliere: {t}\n")
            out.write(f"Groups found: {groups}\n")
            for g in groups:
                # Let's count EXACTLY like the interface:
                interface_sessions = [s for s in edt if s.get('groupe') == g or (s.get('filiere') == t and s.get('type') == 'Cours')]
                c_count = len(set(s['module'] for s in interface_sessions if s.get('type') == 'Cours'))
                t_count = len(set(s['module'] for s in interface_sessions if s.get('type') == 'TD'))
                
                out.write(f"  Group {g}: {c_count} Cours modules, {t_count} TD modules\n")
                scheduled_cours = set(s['module'] for s in interface_sessions if s.get('type') == 'Cours')
                scheduled_tds = set(s['module'] for s in interface_sessions if s.get('type') == 'TD')
                out.write(f"    Cours: {scheduled_cours}\n")
                out.write(f"    TDs:   {scheduled_tds}\n")

if __name__ == "__main__":
    audit_groups()

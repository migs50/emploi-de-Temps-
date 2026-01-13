import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
MODS_PATH = "DONNÉES PRINCIPALES/modules (1).json"
FILS_PATH = "DONNÉES PRINCIPALES/filieres (1).json"
TARGETS = ['BCG-2', 'SSD-1', 'AAIS-1', 'GEMI-2']

def find_missing():
    with open(EDT_PATH, 'r', encoding='utf-8') as f:
        edt = json.load(f)
    with open(MODS_PATH, 'r', encoding='utf-8') as f:
        mods = json.load(f)
    with open(FILS_PATH, 'r', encoding='utf-8') as f:
        fils = json.load(f)['filieres']
    
    fil_ids = {f['id']: f['code'] for f in fils if f['code'] in TARGETS}
    
    for f_id, f_code in fil_ids.items():
        expected_names = {m['nom'] for m in mods if m.get('filiere_id') == f_id}
        scheduled_names = {s['module'] for s in edt if s.get('filiere') == f_code and s.get('type') == 'Cours'}
        
        missing = expected_names - scheduled_names
        print(f"\nFiliere: {f_code} (Missing {len(missing)} Cours)")
        if missing:
            for m_name in missing:
                m_info = next(m for m in mods if m.get('filiere_id') == f_id and m['nom'] == m_name)
                print(f"  - MISSING: {m_name} | Teacher: {m_info.get('enseignant')} (Cap: 26?)")
        else:
            print("  - NO COURS MISSING (Total 6 found)")

if __name__ == "__main__":
    find_missing()

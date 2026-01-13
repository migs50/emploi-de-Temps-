import json

MODS_PATH = "DONNÉES PRINCIPALES/modules (1).json"
FILS_PATH = "DONNÉES PRINCIPALES/filieres (1).json"
TARGETS = ['BCG-2', 'SSD-1', 'AAIS-1', 'GEMI-2']

def extract():
    with open(MODS_PATH, 'r', encoding='utf-8') as f:
        mods = json.load(f)
    with open(FILS_PATH, 'r', encoding='utf-8') as f:
        fils = json.load(f)['filieres']
    
    fil_ids = {f['id']: f['code'] for f in fils if f['code'] in TARGETS}
    
    with open("target_modules_details.txt", "w", encoding='utf-8') as out:
        for f_id, f_code in fil_ids.items():
            out.write(f"\nFiliere: {f_code} (ID: {f_id})\n")
            f_mods = [m for m in mods if m.get('filiere_id') == f_id]
            for m in f_mods:
                out.write(f"  - {m['nom']} (ID: {m['id']}) | Teacher: {m.get('enseignant')} (ID: {m.get('enseignant_id')})\n")

if __name__ == "__main__":
    extract()

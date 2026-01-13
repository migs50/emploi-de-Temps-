import json

MODS_PATH = "DONNÉES PRINCIPALES/modules (1).json"
TARGET_FILS = [23, 26] # ID for IND-1 and GEMI-1

def read_defs():
    with open(MODS_PATH, 'r', encoding='utf-8') as f:
        mods = json.load(f)
    
    for f_id in TARGET_FILS:
        f_mods = [m for m in mods if m.get('filiere_id') == f_id]
        print(f"\nFiliere ID: {f_id}")
        for m in f_mods:
            print(f"  Module: {m['nom']} (ID: {m['id']})")
            print(f"    Cours: {m.get('nb_seances_cours')} | TD: {m.get('nb_seances_td')} | TP: {m.get('nb_seances_tp')}")

if __name__ == "__main__":
    read_defs()

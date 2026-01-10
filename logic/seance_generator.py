import json
import math
import os

# Paths
MODULES_PATH = "DONNÉES PRINCIPALES/modules (1).json"
FILIERES_PATH = "DONNÉES PRINCIPALES/filieres (1).json"
SEANCES_PATH = "DONNÉES PRINCIPALES/seances.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"Error: File not found {path}")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_seances():
    modules = load_json(MODULES_PATH)
    filieres_data = load_json(FILIERES_PATH)
    
    # Create a map of filiere_id to filiere object for easy access
    filieres_map = {f['id']: f for f in filieres_data.get('filieres', [])}
    
    seances = []
    seance_id_counter = 1
    
    print(f"Generating sessions for {len(modules)} modules...")
    
    for mod in modules:
        filiere_id = mod.get('filiere_id')
        if not filiere_id or filiere_id not in filieres_map:
            print(f"Warning: Filiere ID {filiere_id} not found for module {mod['code']}")
            continue
            
        filiere = filieres_map[filiere_id]
        effectif = filiere.get('effectif', 30)
        filiere_code = filiere.get('code', 'UNKNOWN')
        niveau = filiere.get('niveau', '').lower()
        nom = filiere.get('nom', '').lower()
        
        # Logic for groups:
        # If Licence, Master, Cycle -> No groups (1 group)
        # Else (DEUST, etc) -> Split
        no_group_levels = ["licence", "master", "cycle", "cycle ingénieur"]
        
        is_no_group = False
        for lvl in no_group_levels:
            if lvl in niveau or lvl in nom:
                is_no_group = True
                break
        
        if is_no_group:
            nb_groupes_td = 1
            nb_groupes_tp = 1
        else:
            # Standard calculation for DEUST
            nb_groupes_td = math.ceil(effectif / 50)
            nb_groupes_tp = math.ceil(effectif / 30)
        
        # --- COURS (Toujours 1 par module) ---
        seance = {
            "id": seance_id_counter,
            "module": mod['nom'],
            "type": "Cours",
            "enseignant": mod.get('enseignant', 'Inconnu'),
            "filiere": filiere_code,
            "groupe": filiere_code, # Whole promo
            "effectif": effectif,
            "duree": 90,
            "priorite": 1
        }
        seances.append(seance)
        seance_id_counter += 1
            
        # --- TD (Toujours 1 par groupe par module) ---
        for g in range(1, nb_groupes_td + 1):
            groupe_name = f"{filiere_code}-G{g}" if nb_groupes_td > 1 else filiere_code
            seance = {
                "id": seance_id_counter,
                "module": mod['nom'],
                "type": "TD",
                "enseignant": mod.get('enseignant', 'Inconnu'),
                "filiere": filiere_code,
                "groupe": groupe_name,
                "effectif": math.ceil(effectif / nb_groupes_td),
                "duree": 90,
                "priorite": 2
            }
            seances.append(seance)
            seance_id_counter += 1

        # --- TP (1 par groupe si indiqué dans module) ---
        if mod.get('nb_seances_tp', 0) > 0:
            for g in range(1, nb_groupes_tp + 1):
                groupe_name = f"{filiere_code}-G{g}" if nb_groupes_tp > 1 else filiere_code
                seance = {
                    "id": seance_id_counter,
                    "module": mod['nom'],
                    "type": "TP",
                    "enseignant": mod.get('enseignant', 'Inconnu'),
                    "filiere": filiere_code,
                    "groupe": groupe_name,
                    "effectif": math.ceil(effectif / nb_groupes_tp),
                    "duree": 90,
                    "priorite": 3
                }
                seances.append(seance)
                seance_id_counter += 1
                
    print(f"Generated {len(seances)} sessions.")
    save_json(SEANCES_PATH, seances)
    print(f"Saved to {SEANCES_PATH}")

if __name__ == "__main__":
    generate_seances()

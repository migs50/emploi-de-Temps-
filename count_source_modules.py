import json

MODULES_PATH = "DONNÉES PRINCIPALES/modules (1).json"
TARGET_FILIERES = [4, 19, 24, 29] # MIPC-2, AAIS-2, IND-2, LSI-1

def count_source():
    try:
        with open(MODULES_PATH, 'r', encoding='utf-8') as f:
            modules = json.load(f)
        
        counts = {fid: 0 for fid in TARGET_FILIERES}
        names = {fid: [] for fid in TARGET_FILIERES}
        for m in modules:
            fid = m.get('filiere_id')
            if fid in TARGET_FILIERES:
                counts[fid] += 1
                names[fid].append(m.get('nom'))
        
        for fid, count in counts.items():
            print(f"Filiere ID {fid}: {count} modules found in source.")
            # print(f" - {names[fid]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    count_source()

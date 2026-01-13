import json

MODULES_PATH = "DONNÉES PRINCIPALES/modules (1).json"
SEANCES_PATH = "DONNÉES PRINCIPALES/seances.json"

def audit_sessions():
    try:
        with open(MODULES_PATH, 'r', encoding='utf-8') as f:
            modules = json.load(f)
        with open(SEANCES_PATH, 'r', encoding='utf-8') as f:
            seances = json.load(f)
            
        with open("audit_results.txt", "w", encoding='utf-8') as out:
            filiere_map = {4: "MIPC-2", 19: "AAIS-2", 24: "IND-2", 29: "LSI-1"}
            
            for fid, fcode in filiere_map.items():
                expected_mods = set(m['nom'] for m in modules if m['filiere_id'] == fid)
                actual_mods = set(s['module'] for s in seances if s['filiere'] == fcode)
                
                missing = expected_mods - actual_mods
                out.write(f"Filiere {fcode} (ID {fid}):\n")
                out.write(f"  Expected: {len(expected_mods)} ({expected_mods})\n")
                out.write(f"  Actual: {len(actual_mods)} ({actual_mods})\n")
                if missing:
                    out.write(f"  MISSING: {missing}\n")
                else:
                    out.write(f"  All modules found in seances.json\n")
                out.write("-" * 20 + "\n")
        
        print("Audit written to audit_results.txt")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_sessions()

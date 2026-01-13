import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
filiere_map = {4: "MIPC-2", 19: "AAIS-2", 24: "IND-2", 29: "LSI-1"}

def audit_edt():
    try:
        with open(EDT_PATH, 'r', encoding='utf-8') as f:
            edt = json.load(f)
            
        with open("audit_final_results.txt", "w", encoding='utf-8') as out:
            for fid, fcode in filiere_map.items():
                found = [s for s in edt if s.get('filiere') == fcode]
                cours = set(s['module'] for s in found if s['type'] == 'Cours')
                tds = set(s['module'] for s in found if s['type'] == 'TD')
                tps = set(s['module'] for s in found if s['type'] == 'TP')
                
                out.write(f"Filiere {fcode}:\n")
                out.write(f"  Cours found: {len(cours)} {cours}\n")
                out.write(f"  TDs found: {len(tds)} {tds}\n")
                out.write(f"  TPs found: {len(tps)} {tps}\n")
                out.write("-" * 20 + "\n")
        
        print("Audit written to audit_final_results.txt")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_edt()

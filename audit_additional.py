import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
FILIERES_PATH = "DONNÉES PRINCIPALES/filieres (1).json"
MODULES_PATH = "DONNÉES PRINCIPALES/modules (1).json"

TARGET_FILIERES = ['BCG-2', 'SSD-1', 'AAIS-1', 'GEMI-2']

def audit_additional_filieres():
    try:
        with open(EDT_PATH, 'r', encoding='utf-8') as f:
            edt = json.load(f)
        with open(FILIERES_PATH, 'r', encoding='utf-8') as f:
            fil_data = json.load(f).get('filieres', [])
        with open(MODULES_PATH, 'r', encoding='utf-8') as f:
            mod_data = json.load(f)

        # Get filiere codes to IDs
        fil_map = {f['code']: f['id'] for f in fil_data if f['code'] in TARGET_FILIERES}
        
        # Get expected modules for these filieres
        expected = {code: [] for code in TARGET_FILIERES}
        for mod in mod_data:
            if mod['filiere_id'] in fil_map.values():
                # Find the code for this ID
                code = [c for c, i in fil_map.items() if i == mod['filiere_id']][0]
                expected[code].append(mod)

        # Audit EDT
        results = {code: {'expected': len(expected[code]), 'Cours': set(), 'TD': set(), 'missing': []} for code in TARGET_FILIERES}
        
        # Teacher workload map from EDT
        teacher_loads = {}
        for s in edt:
            t = s.get('enseignant')
            if t:
                teacher_loads[t] = teacher_loads.get(t, 0) + 1

        for code in TARGET_FILIERES:
            scheduled_cours = {s['module'] for s in edt if s.get('filiere') == code and s.get('type') == 'Cours'}
            scheduled_tds = {s['module'] for s in edt if s.get('filiere') == code and s.get('type') == 'TD'}
            
            # Note: For split filieres (BCG-2), we might have multiple TD sessions for the same module.
            # We just want to know if AT LEAST ONE is scheduled for the user's group.
            
            results[code]['Cours'] = scheduled_cours
            results[code]['TD'] = scheduled_tds
            
            # Identify missing modules
            expected_names = {m['nom'] for m in expected[code]}
            results[code]['missing'] = list(expected_names - scheduled_cours)

        with open("additional_audit_results.txt", "w", encoding='utf-8') as out:
            for code, data in results.items():
                out.write(f"Filiere {code} (Expected {data['expected']} modules):\n")
                out.write(f"  Cours found ({len(data['Cours'])}): {data['Cours']}\n")
                out.write(f"  TDs found ({len(data['TD'])}): {data['TD']}\n")
                out.write(f"  MISSING Modules from Cours:\n")
                for m_name in data['missing']:
                    m_info = next((m for m in expected[code] if m['nom'] == m_name), None)
                    if m_info:
                        t_name = m_info.get('enseignant')
                        load = teacher_loads.get(t_name, 0)
                        out.write(f"    - {m_name}: {t_name} (Current Load: {load} sessions)\n")
                
                # Also check modules that ARE found but might have overload teachers
                out.write(f"  Scheduled Modules Teacher Loads:\n")
                for m_name in data['Cours']:
                    m_info = next((m for m in expected[code] if m['nom'] == m_name), None)
                    if m_info:
                        t_name = m_info.get('enseignant')
                        load = teacher_loads.get(t_name, 0)
                        out.write(f"    - {m_name}: {t_name} ({load} sessions)\n")
                
                out.write("-" * 20 + "\n")
        
        print("Audit written to additional_audit_results.txt")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_additional_filieres()

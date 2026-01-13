import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
TARGET_FILIERES = ["MIPC-2", "AAIS-2", "IND-2", "LSI-1"]

def analyze_edt():
    try:
        with open(EDT_PATH, 'r', encoding='utf-8') as f:
            edt = json.load(f)
        
        counts = {f: set() for f in TARGET_FILIERES}
        for s in edt:
            filiere = s.get('filiere')
            if filiere in TARGET_FILIERES and s.get('type') == 'Cours':
                counts[filiere].add(s.get('module'))
        
        with open("edt_count_analysis.txt", "w", encoding='utf-8') as out:
            for filiere, modules in counts.items():
                out.write(f"Filiere: {filiere}, Unique Cours Modules: {len(modules)}\n")
                for mod in modules:
                    out.write(f" - {mod}\n")
        
        print("Analysis written to edt_count_analysis.txt")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_edt()

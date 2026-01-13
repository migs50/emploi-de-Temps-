import json
import csv
import os

def exporter_csv(edt, filename):
    if not edt:
        return False
    
    keys = edt[0].keys()
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(edt)
        return True
    except Exception as e:
        print(f"Export error: {e}")
        return False

def exporter_rapport_occupation(edt, salles, filename):
    # Calculate stats
    stats = {}
    for s in salles:
        stats[s["nom"]] = 0
        
    for session in edt:
        salle_name = session.get("salle")
        if salle_name in stats:
            stats[salle_name] += 1
            
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("RAPPORT D'OCCUPATION DES SALLES\n")
            f.write("="*30 + "\n\n")
            for salle, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {salle}: {count} séances\n")
        return True
    except Exception as e:
        print(f"Export error: {e}")
        return False

import json
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

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

def exporter_excel(edt, filename):
    if not edt:
        return False
    try:
        df = pd.DataFrame(edt)
        # Note: requires openpyxl. If not present, this will fail.
        # We catch the error and let the UI handle it.
        df.to_excel(filename, index=False)
        return True
    except Exception as e:
        print(f"Excel export error: {e}")
        # If openpyxl missing, suggest CSV
        return False

def exporter_visual(edt, filename, format_ext="png"):
    if not edt:
        return False
    
    try:
        # Simple visualization using matplotlib
        fig, ax = plt.subplots(figsize=(12, len(edt) * 0.3 + 2))
        ax.axis('off')
        
        # Prepare data for table
        data = [[s.get('jour', ''), s.get('debut', ''), s.get('module', ''), s.get('salle', ''), s.get('groupe', '')] for s in edt]
        columns = ["Jour", "Heure", "Module", "Salle", "Groupe"]
        
        # Create table
        table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.2)
        
        plt.title("Emploi du Temps", fontsize=15, pad=20)
        
        if format_ext == "pdf":
            plt.savefig(filename, format='pdf', bbox_inches='tight')
        else:
            plt.savefig(filename, format='png', bbox_inches='tight', dpi=150)
            
        plt.close(fig)
        return True
    except Exception as e:
        print(f"Visual export error: {e}")
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

import json
import csv
import os
import datetime
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
        # Sort EDT for consistent display
        day_order = {"Lundi":1, "Mardi":2, "Mercredi":3, "Jeudi":4, "Vendredi":5, "Samedi":6}
        edt.sort(key=lambda x: (day_order.get(x.get('jour', ''), 7), x.get('debut', '')))

        # Professional Styling
        plt.rcParams['font.family'] = 'sans-serif'
        fig, ax = plt.subplots(figsize=(14, len(edt) * 0.4 + 3))
        ax.axis('off')
        
        # Color mapping for session types
        type_colors = {
            "Examen": "#e74c3c", # Red
            "Cours": "#3498db",  # Blue
            "TD": "#2ecc71",     # Green
            "TP": "#f1c40f"      # Yellow
        }
        
        # Prepare data and colors
        data = []
        cell_colors = []
        header_color = "#2c3e50"
        
        for s in edt:
            data.append([
                s.get('jour', ''), 
                s.get('debut', '') + " - " + s.get('fin', ''), 
                s.get('module', ''), 
                s.get('type', ''),
                s.get('salle', ''), 
                s.get('groupe', '')
            ])
            # Row color based on type
            t = s.get('type', 'Cours')
            color = type_colors.get(t, "#ffffff")
            # We apply a lighter version for the row or just use it for the "Type" cell
            cell_colors.append(["#ffffff", "#ffffff", "#ffffff", color, "#ffffff", "#ffffff"])

        columns = ["Jour", "Créneau", "Module", "Type", "Salle", "Groupe"]
        
        # Create table
        table = ax.table(
            cellText=data, 
            colLabels=columns, 
            loc='center', 
            cellLoc='center',
            cellColours=cell_colors,
            colColours=[header_color]*len(columns)
        )
        
        # Style header
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_text_props(color='white', weight='bold')
            cell.set_edgecolor('#bdc3c7')
            cell.set_height(0.05)

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)
        
        # Header Info
        plt.text(0.5, 0.98, "UNIVERSITÉ - EMPLOI DU TEMPS OFFICIEL", 
                 horizontalalignment='center', fontsize=16, weight='bold', color="#2c3e50", transform=ax.transAxes)
        plt.text(0.5, 0.94, f"Exporté le : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                 horizontalalignment='center', fontsize=10, transform=ax.transAxes)

        if format_ext == "pdf":
            plt.savefig(filename, format='pdf', bbox_inches='tight', dpi=300)
        else:
            plt.savefig(filename, format='png', bbox_inches='tight', dpi=200)
            
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

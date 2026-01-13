import json
import csv
import os
import datetime
import textwrap
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
        
        # Calculate figure height based on rows
        # More space for wrapped text?
        fig_height = len(edt) * 0.5 + 4
        fig, ax = plt.subplots(figsize=(14, fig_height))
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
            # Wrap long module names
            module_name = s.get('module', '')
            wrapped_module = "\n".join(textwrap.wrap(module_name, width=30))
            
            data.append([
                s.get('jour', ''), 
                s.get('debut', '') + " - " + s.get('fin', ''), 
                wrapped_module, 
                s.get('type', ''),
                s.get('salle', ''), 
                s.get('groupe', '')
            ])
            # Row color based on type
            t = s.get('type', 'Cours')
            color = type_colors.get(t, "#ffffff")
            cell_colors.append(["#ffffff", "#ffffff", "#ffffff", color, "#ffffff", "#ffffff"])

        columns = ["Jour", "Créneau", "Module", "Type", "Salle", "Groupe"]
        
        # Create table - loc='top' to allow space below? No, center is fine but we need to title above.
        # We use bbox to position table precisely
        table = ax.table(
            cellText=data, 
            colLabels=columns, 
            loc='center', 
            cellLoc='center',
            cellColours=cell_colors,
            colColours=[header_color]*len(columns)
        )
        
        # Style header & Adjust Row Height for wrapped text
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_text_props(color='white', weight='bold')
                cell.set_height(0.05)
            else:
                # Dynamic height based on content? textwrap adds \n
                content = data[row-1][col]
                lines = content.count('\n') + 1
                cell.set_height(0.04 * lines if lines > 1 else 0.04)
                
            cell.set_edgecolor('#bdc3c7')

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        
        # Column width adjustment
        # Module column (index 2) needs more width
        table.auto_set_column_width([0, 1, 3, 4, 5])
        col_widths = {0: 0.1, 1: 0.15, 2: 0.35, 3: 0.1, 4: 0.15, 5: 0.1}
        for i, width in col_widths.items():
            table._cells[(0, i)].set_width(width)
            for r in range(1, len(data)+1):
                 table._cells[(r, i)].set_width(width)
        
        # Header Info - Positioned using Figure coordinates instead of Axes to avoid table overlap
        # 0.95 is near top.
        plt.title(f"Exporté le : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", fontsize=10, y=0.98)

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

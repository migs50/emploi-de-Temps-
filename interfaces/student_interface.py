import tkinter as tk
from tkinter import ttk
from logic.database import charger_json

class StudentInterface:
    def __init__(self, root):
        self.root = root
        
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Choisir ma filière/groupe :").pack(side=tk.LEFT, padx=5)
        
        self.groups = self.load_groups()
        group_names = self.groups
        
        self.selected_group = tk.StringVar()
        self.cb_group = ttk.Combobox(top_frame, textvariable=self.selected_group, values=group_names)
        self.cb_group.pack(side=tk.LEFT, padx=5)
        self.cb_group.bind("<<ComboboxSelected>>", self.display_edt)
        
        self.content_frame = ttk.Frame(root, padding=10)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.content_frame, columns=("Jour", "Heure", "Module", "Type", "Salle", "Prof"), show="headings")
        self.tree.heading("Jour", text="Jour")
        self.tree.heading("Heure", text="Heure")
        self.tree.heading("Module", text="Module")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Salle", text="Salle")
        self.tree.heading("Prof", text="Enseignant")
        
        self.tree.column("Jour", width=80)
        self.tree.column("Heure", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_groups(self):
        try:
            seances = charger_json("DONNÉES PRINCIPALES/seances.json")
            # Extraire les groupes uniques et les trier
            groups = sorted(list(set([s.get('groupe', 'Inconnu') for s in seances if s.get('groupe')])))
            return groups
        except Exception as e:
            print(f"Erreur chargement groupes: {e}")
            return []

    def display_edt(self, event):
        # Clear
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        group = self.selected_group.get()
        if not group: return
        
        try:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            # Filter by group (exact match or parent group?)
            # Logic: if my group is GEGM-1-G1, I need sessions for GEGM-1-G1 AND GEGM-1 (Cours)
            
            my_sessions = []
            for s in edt:
                s_group = s.get('groupe', '')
                # If exact match OR if session is for the whole promo (e.g. s_group is prefix of group)
                # Example: s_group="GEGM-1" matches group="GEGM-1-G1"
                if s_group == group or (group.startswith(s_group) and s['type'] == 'Cours'):
                    my_sessions.append(s)
            
            day_order = {"Lundi":1, "Mardi":2, "Mercredi":3, "Jeudi":4, "Vendredi":5, "Samedi":6}
            my_sessions.sort(key=lambda x: (day_order.get(x['jour'], 7), x['debut']))
            
            for s in my_sessions:
                self.tree.insert("", tk.END, values=(
                    s['jour'], 
                    f"{s['debut']} - {s['fin']}", 
                    s['module'], 
                    s.get('type', '?'), # Sometimes type might be missing in logic? seances.json has it.
                    s['salle'], 
                    s['enseignant']
                ))
                
        except Exception as e:
            print(e)

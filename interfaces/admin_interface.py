import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import os

# Imports logic
from logic.edt_generator import generer_edt
from logic.database import charger_json

class AdminInterface:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')  # Maximize
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Tabs
        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_generate = ttk.Frame(self.notebook)
        self.tab_data = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_dashboard, text="Tableau de Bord")
        self.notebook.add(self.tab_generate, text="Génération EDT")
        self.notebook.add(self.tab_data, text="Données")
        
        self.setup_dashboard()
        self.setup_generation()
        self.setup_data_view()

    def setup_dashboard(self):
        # Load stats
        try:
            enseignants = charger_json("DONNÉES PRINCIPALES/enseignants_final.json")
            modules = charger_json("DONNÉES PRINCIPALES/modules (1).json")
            salles = charger_json("DONNÉES PRINCIPALES/salles.json")
            etudiants = 0 
            filieres = charger_json("DONNÉES PRINCIPALES/filieres (1).json")
            if "statistiques" in filieres:
                etudiants = filieres["statistiques"].get("total_etudiants", 0)
            
            stats_frame = ttk.LabelFrame(self.tab_dashboard, text="Statistiques Globales", padding=20)
            stats_frame.pack(fill=tk.X, pady=20, padx=20)
            
            self.create_stat_card(stats_frame, "Enseignants", len(enseignants), 0, 0)
            self.create_stat_card(stats_frame, "Modules", len(modules), 0, 1)
            self.create_stat_card(stats_frame, "Salles", len(salles), 0, 2)
            self.create_stat_card(stats_frame, "Étudiants", etudiants, 0, 3)
            
        except Exception as e:
            ttk.Label(self.tab_dashboard, text=f"Erreur chargement données: {str(e)}", foreground="red").pack()

    def create_stat_card(self, parent, title, value, row, col):
        frame = ttk.Frame(parent, borderwidth=2, relief="groove")
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        ttk.Label(frame, text=title, font=("Helvetica", 10)).pack(pady=(10,5))
        ttk.Label(frame, text=str(value), font=("Helvetica", 20, "bold"), foreground="#2980b9").pack(pady=(0,10))

    def setup_generation(self):
        container = ttk.Frame(self.tab_generate, padding=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Frame for buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=20)
        
        # Step 1: Generate Data
        btn_data = tk.Button(btn_frame, text="1. Générer les Données (Séances)", 
                            bg="#e67e22", fg="white", font=("Helvetica", 12),
                            command=self.run_data_generation)
        btn_data.pack(side=tk.LEFT, padx=10)
        
        # Step 2: Generate Timetable
        btn_gen = tk.Button(btn_frame, text="2. Placer les Séances (Algo)", 
                            bg="#27ae60", fg="white", font=("Helvetica", 12),
                            command=self.run_generation)
        btn_gen.pack(side=tk.LEFT, padx=10)
        
        self.log_area = scrolledtext.ScrolledText(container, height=20)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=10)
        self.log("Système prêt.", "info")

    def run_data_generation(self):
        self.log("Génération des séances en cours...", "info")
        try:
            # Import dynamically to avoid issues if file moved
            from logic.seance_generator import generate_seances
            threading.Thread(target=lambda: [generate_seances(), self.root.after(0, lambda: self.log("Données séances générées.", "success"))]).start()
        except Exception as e:
            self.log(f"Erreur: {e}", "error")

    def run_generation(self):
        self.log("Démarrage de l'algorithme de placement...", "info")
        try:
            threading.Thread(target=self._generation_process).start()
        except Exception as e:
            self.log(f"Erreur: {str(e)}", "error")

    def _generation_process(self):
        try:
            edt = generer_edt()
            self.root.after(0, lambda: self.log(f"Placement terminé ! {len(edt)} séances placées.", "success"))
            self.root.after(0, lambda: messagebox.showinfo("Succès", "L'emploi du temps a été généré."))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Erreur critique: {str(e)}", "error"))

    def log(self, message, type_msg="info"):
        color = "black"
        if type_msg == "error": color = "red"
        if type_msg == "success": color = "green"
        
        self.log_area.tag_config(type_msg, foreground=color)
        self.log_area.insert(tk.END, f"> {message}\n", type_msg)
        self.log_area.see(tk.END)

    def setup_data_view(self):
        # Sub-tabs for data
        nb = ttk.Notebook(self.tab_data)
        nb.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_tree_view(nb, "Salles", "DONNÉES PRINCIPALES/salles.json", ["nom", "capacite", "type"])
        self.create_tree_view(nb, "Enseignants", "DONNÉES PRINCIPALES/enseignants_final.json", ["nom", "email", "departement"])
        self.create_tree_view(nb, "Modules", "DONNÉES PRINCIPALES/modules (1).json", ["code", "nom", "nb_seances_cours"])

    def create_tree_view(self, parent, title, file_path, columns):
        frame = ttk.Frame(parent)
        parent.add(frame, text=title)
        
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100)
            
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        try:
            data = charger_json(file_path)
            for item in data:
                values = [item.get(col, "") for col in columns]
                tree.insert("", tk.END, values=values)
        except Exception as e:
            print(f"Error loading {title}: {e}")

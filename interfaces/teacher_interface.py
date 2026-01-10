import tkinter as tk
from tkinter import ttk, messagebox
from logic.database import charger_json, sauvegarder_json
from logic.reservation_manager import ajouter_reservation

class TeacherInterface:
    def __init__(self, root):
        self.root = root
        
        # Sidebar for selection
        left_panel = ttk.Frame(root, padding=10, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(left_panel, text="Sélectionnez votre profil :").pack(pady=5)
        
        self.teachers = self.load_teachers()
        teacher_names = [f"{t['nom']} {t.get('prenom', '')}" for t in self.teachers]
        
        self.selected_teacher = tk.StringVar()
        self.cb_teacher = ttk.Combobox(left_panel, textvariable=self.selected_teacher, values=teacher_names)
        self.cb_teacher.pack(fill=tk.X, pady=5)
        self.cb_teacher.bind("<<ComboboxSelected>>", self.on_teacher_select)
        
        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.tab_edt = ttk.Frame(self.notebook)
        self.tab_resa = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_edt, text="Mon Emploi du Temps")
        self.notebook.add(self.tab_resa, text="Réserver une Salle")
        
        self.setup_edt_view()
        self.setup_reservation_view()

    def load_teachers(self):
        try:
            return charger_json("DONNÉES PRINCIPALES/enseignants_final.json")
        except:
            return []

    def on_teacher_select(self, event):
        self.display_edt()

    def display_edt(self):
        # Clear previous
        for widget in self.tab_edt.winfo_children():
            widget.destroy()
            
        name = self.selected_teacher.get()
        if not name: return
        
        # Find teacher ID from simple matching
        teacher_id = None
        for t in self.teachers:
            if name.startswith(t['nom']): # Simplified matching
                teacher_id = t['id']
                break
        
        # Load EDT
        try:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            # Recherche plus robuste (insensible à la casse, et gestion des string ids)
            my_sessions = []
            name_lower = name.lower()
            
            for s in edt:
                ens_name = s.get('enseignant', '').lower()
                ens_id = str(s.get('enseignant_id', ''))
                
                # Correspondance par nom ou par ID
                if name_lower in ens_name or str(teacher_id) == ens_id:
                     my_sessions.append(s)
            
            if not my_sessions:
                 ttk.Label(self.tab_edt, text="Aucun cours trouvé pour cet enseignant.").pack(pady=20)
            
            # Simple list display
            tree = ttk.Treeview(self.tab_edt, columns=("Jour", "Heure", "Module", "Salle", "Groupe"), show="headings")
            tree.heading("Jour", text="Jour")
            tree.heading("Heure", text="Heure")
            tree.heading("Module", text="Module")
            tree.heading("Salle", text="Salle")
            tree.heading("Groupe", text="Groupe")
            tree.pack(fill=tk.BOTH, expand=True)
            
            # Sort by day/time
            day_order = {"Lundi":1, "Mardi":2, "Mercredi":3, "Jeudi":4, "Vendredi":5, "Samedi":6}
            my_sessions.sort(key=lambda x: (day_order.get(x['jour'], 7), x['debut']))
            
            for s in my_sessions:
                tree.insert("", tk.END, values=(s['jour'], f"{s['debut']} - {s['fin']}", s['module'], s['salle'], s['groupe']))
                
        except Exception as e:
            ttk.Label(self.tab_edt, text=f"Erreur: {str(e)}").pack()

    def setup_edt_view(self):
        ttk.Label(self.tab_edt, text="Veuillez sélectionner un enseignant à gauche.").pack(pady=20)

    def setup_reservation_view(self):
        form = ttk.Frame(self.tab_resa, padding=20)
        form.pack(fill=tk.BOTH)
        
        ttk.Label(form, text="Motif:").grid(row=0, column=0, pady=5)
        self.entry_motif = ttk.Entry(form, width=40)
        self.entry_motif.grid(row=0, column=1, pady=5)
        
        ttk.Label(form, text="Salle:").grid(row=1, column=0, pady=5)
        try:
            salles = [s['nom'] for s in charger_json("DONNÉES PRINCIPALES/salles.json")]
        except: salles = []
        self.cb_salle = ttk.Combobox(form, values=salles)
        self.cb_salle.grid(row=1, column=1, pady=5)
        
        ttk.Label(form, text="Jour:").grid(row=2, column=0, pady=5)
        self.cb_jour = ttk.Combobox(form, values=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"])
        self.cb_jour.grid(row=2, column=1, pady=5)
        
        ttk.Label(form, text="Heure Début (HH:MM):").grid(row=3, column=0, pady=5)
        self.entry_heure = ttk.Entry(form)
        self.entry_heure.grid(row=3, column=1, pady=5)
        
        ttk.Button(form, text="Demander la réservation", command=self.submit_reservation).grid(row=4, column=1, pady=20)

    def submit_reservation(self):
        # Validation
        if not self.cb_salle.get() or not self.cb_jour.get() or not self.entry_heure.get():
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs obligatoires.")
            return

        resa = {
            "enseignant": self.selected_teacher.get(),
            "salle": self.cb_salle.get(),
            "jour": self.cb_jour.get(),
            "debut": self.entry_heure.get(),
            "motif": self.entry_motif.get()
        }
        if ajouter_reservation(resa):
            messagebox.showinfo("Succès", "Réservation enregistrée !")
            self.entry_motif.delete(0, tk.END)
            self.entry_heure.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Créneau indisponible ou erreur donnée.")

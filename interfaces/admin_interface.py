import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import sys
import os

# Imports logic
from logic.edt_generator import generer_edt
from logic.database import charger_json, sauvegarder_json
from logic.reservation_manager import modifier_statut_reservation, get_salles_disponibles
from logic.exporter import exporter_csv, exporter_rapport_occupation

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
        self.tab_reservations = ttk.Frame(self.notebook)
        self.tab_occupancy = ttk.Frame(self.notebook)
        self.tab_availability = ttk.Frame(self.notebook)
        self.tab_data = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_dashboard, text="Tableau de Bord")
        self.notebook.add(self.tab_generate, text="Génération EDT")
        self.notebook.add(self.tab_reservations, text="Réservations")
        self.notebook.add(self.tab_occupancy, text="Occupation")
        self.notebook.add(self.tab_availability, text="Disponibilités")
        self.notebook.add(self.tab_data, text="Données")
        
        self.setup_dashboard()
        self.setup_generation()
        self.setup_reservations()
        self.setup_occupancy()
        self.setup_availability()
        self.setup_data_view()

    def setup_dashboard(self):
        # Refresh container
        for w in self.tab_dashboard.winfo_children(): w.destroy()
        
        try:
            enseignants = charger_json("DONNÉES PRINCIPALES/enseignants_final.json")
            if isinstance(enseignants, dict): enseignants = enseignants.get("enseignants", [])
                
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
            
            # Action buttons
            btn_frame = ttk.Frame(self.tab_dashboard, padding=20)
            btn_frame.pack(fill=tk.X)
            
            ttk.Button(btn_frame, text="Exporter EDT (CSV)", command=self.export_edt_csv).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Exporter Rapport Occupation", command=self.export_occ_report).pack(side=tk.LEFT, padx=5)
            
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
        
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="1. Générer les Données (Séances)", 
                  bg="#e67e22", fg="white", font=("Helvetica", 12),
                  command=self.run_data_generation).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="2. Placer les Séances (Algo)", 
                  bg="#27ae60", fg="white", font=("Helvetica", 12),
                  command=self.run_generation).pack(side=tk.LEFT, padx=10)
        
        self.log_area = scrolledtext.ScrolledText(container, height=20)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=10)
        self.log("Système prêt.", "info")

    def run_data_generation(self):
        self.log("Génération des séances en cours...", "info")
        try:
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
            self.root.after(0, self.setup_occupancy) # Refresh occupancy view
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Erreur critique: {str(e)}", "error"))

    def setup_reservations(self):
        for w in self.tab_reservations.winfo_children(): w.destroy()
        
        lbl = ttk.Label(self.tab_reservations, text="Demandes de Réservation", font=("Helvetica", 14, "bold"))
        lbl.pack(pady=10)
        
        columns = ("ID", "Enseignant", "Salle", "Jour", "Début", "Motif", "Statut")
        self.tree_resa = ttk.Treeview(self.tab_reservations, columns=columns, show="headings")
        for col in columns: self.tree_resa.heading(col, text=col)
        
        self.tree_resa.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        btn_box = ttk.Frame(self.tab_reservations)
        btn_box.pack(pady=10)
        
        ttk.Button(btn_box, text="Accepter", command=lambda: self.handle_resa("Acceptée")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Rejeter", command=lambda: self.handle_resa("Refusée")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Rafraîchir", command=self.setup_reservations).pack(side=tk.LEFT, padx=5)
        
        # Load data
        try:
            resas = charger_json("GESTION EDT/reservations.json")
            for r in resas:
                self.tree_resa.insert("", tk.END, values=(r["id"], r["enseignant"], r["salle"], r["jour"], r["debut"], r["motif"], r["statut"]))
        except: pass

    def handle_resa(self, status):
        selected = self.tree_resa.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une demande.")
            return
        
        item = self.tree_resa.item(selected[0])
        resa_id = item['values'][0]
        
        if modifier_statut_reservation(resa_id, status):
            messagebox.showinfo("Succès", f"La demande a été {status.lower()}.")
            self.setup_reservations()
            self.setup_occupancy()
        else:
            messagebox.showerror("Erreur", "Impossible de modifier le statut.")

    def setup_occupancy(self):
        for w in self.tab_occupancy.winfo_children(): w.destroy()
        
        lbl = ttk.Label(self.tab_occupancy, text="Taux d'Occupation des Salles", font=("Helvetica", 14, "bold"))
        lbl.pack(pady=10)
        
        try:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            salles = charger_json("DONNÉES PRINCIPALES/salles.json")
            
            occ_data = {s['nom']: 0 for s in salles}
            for s in edt:
                if s['salle'] in occ_data: occ_data[s['salle']] += 1
            
            # Sort by occupancy
            sorted_occ = sorted(occ_data.items(), key=lambda x: x[1], reverse=True)
            
            tree = ttk.Treeview(self.tab_occupancy, columns=("Salle", "Séances"), show="headings")
            tree.heading("Salle", text="Salle")
            tree.heading("Séances", text="Nombre de séances")
            tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            for s, count in sorted_occ:
                tree.insert("", tk.END, values=(s, count))
                
        except Exception as e:
            ttk.Label(self.tab_occupancy, text=f"Erreur: {e}").pack()

    def setup_availability(self):
        for w in self.tab_availability.winfo_children(): w.destroy()
        
        container = ttk.Frame(self.tab_availability, padding=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(container, text="Bloquer un créneau enseignant", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        form = ttk.Frame(container)
        form.pack()
        
        ttk.Label(form, text="Enseignant:").grid(row=0, column=0, pady=5)
        try:
            ens_data = charger_json("DONNÉES PRINCIPALES/enseignants_final.json")
            if isinstance(ens_data, dict): ens_data = ens_data.get("enseignants", [])
            ens_names = [e["nom"] for e in ens_data]
        except: ens_names = []
        
        self.cb_ens_avail = ttk.Combobox(form, values=ens_names, width=30)
        self.cb_ens_avail.grid(row=0, column=1, pady=5)
        
        ttk.Label(form, text="Jour:").grid(row=1, column=0, pady=5)
        self.cb_jour_avail = ttk.Combobox(form, values=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"])
        self.cb_jour_avail.grid(row=1, column=1, pady=5)
        self.cb_jour_avail.bind("<<ComboboxSelected>>", self.refresh_available_rooms)
        
        ttk.Label(form, text="Début (HH:MM):").grid(row=2, column=0, pady=5)
        self.cb_start_avail = ttk.Combobox(form, values=["09:00", "10:45", "12:30", "14:15", "16:00"])
        self.cb_start_avail.grid(row=2, column=1, pady=5)
        self.cb_start_avail.bind("<<ComboboxSelected>>", self.refresh_available_rooms)
        
        ttk.Label(form, text="Salle (Libre):").grid(row=3, column=0, pady=5)
        self.cb_salle_avail = ttk.Combobox(form, values=["Veuillez choisir jour/heure"])
        self.cb_salle_avail.grid(row=3, column=1, pady=5)
        
        ttk.Button(form, text="Bloquer", command=self.block_teacher).grid(row=4, column=1, pady=10)
        
        # Current blocks
        ttk.Label(container, text="Créneaux bloqués:", font=("Helvetica", 10, "bold")).pack(pady=(20,5))
        self.tree_blocked = ttk.Treeview(container, columns=("Enseignant", "Jour", "Heure", "Salle"), show="headings", height=5)
        self.tree_blocked.heading("Enseignant", text="Enseignant")
        self.tree_blocked.heading("Jour", text="Jour")
        self.tree_blocked.heading("Heure", text="Heure")
        self.tree_blocked.heading("Salle", text="Salle")
        self.tree_blocked.pack(fill=tk.X)
        self.refresh_blocked()

    def block_teacher(self):
        ens = self.cb_ens_avail.get()
        jr = self.cb_jour_avail.get()
        start = self.cb_start_avail.get()
        room = self.cb_salle_avail.get()
        
        if not ens or not jr or not start:
            messagebox.showwarning("Attention", "Les champs Enseignant, Jour et Début sont requis.")
            return
            
        try:
            avail = charger_json("DONNÉES PRINCIPALES/availability.json")
            if "blocked_slots" not in avail: avail["blocked_slots"] = []
            block_item = {"enseignant": ens, "jour": jr, "debut": start}
            if room and room != "Veuillez choisir jour/heure" and room != "Aucune salle libre": 
                block_item["salle"] = room
            
            avail["blocked_slots"].append(block_item)
            sauvegarder_json("DONNÉES PRINCIPALES/availability.json", avail)
            messagebox.showinfo("Succès", "Créneau bloqué.")
            self.refresh_blocked()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def refresh_available_rooms(self, event=None):
        jr = self.cb_jour_avail.get()
        start = self.cb_start_avail.get()
        if jr and start:
            free_rooms = get_salles_disponibles(jr, start)
            if free_rooms:
                self.cb_salle_avail['values'] = [""] + free_rooms
                self.cb_salle_avail.set("")
            else:
                self.cb_salle_avail['values'] = ["Aucune salle libre"]
                self.cb_salle_avail.set("Aucune salle libre")

    def refresh_blocked(self):
        for i in self.tree_blocked.get_children(): self.tree_blocked.delete(i)
        try:
            avail = charger_json("DONNÉES PRINCIPALES/availability.json")
            for b in avail.get("blocked_slots", []):
                self.tree_blocked.insert("", tk.END, values=(b["enseignant"], b["jour"], b["debut"], b.get("salle", "-")))
        except: pass

    def export_edt_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            if exporter_csv(edt, path):
                messagebox.showinfo("Succès", "Export CSV réussi.")
            else:
                messagebox.showerror("Erreur", "L'export a échoué.")

    def export_occ_report(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if path:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            salles = charger_json("DONNÉES PRINCIPALES/salles.json")
            if exporter_rapport_occupation(edt, salles, path):
                messagebox.showinfo("Succès", "Rapport généré.")
            else:
                messagebox.showerror("Erreur", "L'export a échoué.")

    def log(self, message, type_msg="info"):
        color = "black"
        if type_msg == "error": color = "red"
        if type_msg == "success": color = "green"
        self.log_area.tag_config(type_msg, foreground=color)
        self.log_area.insert(tk.END, f"> {message}\n", type_msg)
        self.log_area.see(tk.END)

    def setup_data_view(self):
        nb = ttk.Notebook(self.tab_data)
        nb.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.create_tree_view(nb, "Salles", "DONNÉES PRINCIPALES/salles.json", ["nom", "capacite", "type", "equipements"])
        self.create_tree_view(nb, "Enseignants", "DONNÉES PRINCIPALES/enseignants_final.json", ["nom", "email", "departement"])
        self.create_tree_view(nb, "Modules", "DONNÉES PRINCIPALES/modules (1).json", ["code", "nom", "nb_seances_cours"])

    def create_tree_view(self, parent, title, file_path, columns):
        frame = ttk.Frame(parent)
        parent.add(frame, text=title)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            width = 150 if col == "equipements" else 100
            tree.column(col, width=width, minwidth=50)
        
        # Vertical Scrollbar
        v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=v_scrollbar.set)
        
        # Horizontal Scrollbar
        h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(xscroll=h_scrollbar.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        try:
            data = charger_json(file_path)
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                        data = value
                        break
            for item in data:
                values = []
                for col in columns:
                    val = item.get(col, "")
                    if isinstance(val, list):
                        val = ", ".join(map(str, val))
                    values.append(val)
                tree.insert("", tk.END, values=values)
        except Exception as e: print(f"Error: {e}")

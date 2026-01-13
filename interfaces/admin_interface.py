import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from logic.stats_manager import get_advanced_stats

# Imports logic
from logic.edt_generator import generer_edt
from logic.database import charger_json, sauvegarder_json
from logic.reservation_manager import modifier_statut_reservation, get_salles_disponibles, salle_disponible
from logic.exporter import exporter_csv, exporter_rapport_occupation, exporter_excel, exporter_visual

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
        self.tab_realtime_occ = ttk.Frame(self.notebook)
        self.tab_realtime_occ = ttk.Frame(self.notebook)
        self.tab_stats = ttk.Frame(self.notebook)
        self.tab_exports = ttk.Frame(self.notebook)
        self.tab_availability = ttk.Frame(self.notebook)
        self.tab_data = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_dashboard, text="Tableau de Bord")
        self.notebook.add(self.tab_generate, text="Génération EDT")
        self.notebook.add(self.tab_reservations, text="Réservations")
        self.notebook.add(self.tab_occupancy, text="Occupation (Global)")
        self.notebook.add(self.tab_realtime_occ, text="Occupation (Temps Réel)")
        self.notebook.add(self.tab_exports, text="Consultation & Export")
        self.notebook.add(self.tab_stats, text="Statistiques")
        self.notebook.add(self.tab_availability, text="Disponibilités")
        self.notebook.add(self.tab_data, text="Données")
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        self.setup_dashboard()
        self.setup_generation()
        self.setup_reservations()
        self.setup_occupancy()
        self.setup_availability()
        self.setup_data_view()
        self.setup_stats()
        self.setup_data_view()
        self.setup_stats()
        self.setup_realtime_occupancy()
        self.setup_exports()
        
        self.current_filtered_edt = [] # Store for export

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
            
            ttk.Label(btn_frame, text="Exportations Emploi du Temps :", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=(0,10))
            ttk.Button(btn_frame, text="CSV", command=self.export_edt_csv).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Excel", command=self.export_edt_excel).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Image (PNG)", command=self.export_edt_image).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="PDF", command=self.export_edt_pdf).pack(side=tk.LEFT, padx=5)
            
            # Occupation report
            rep_frame = ttk.Frame(self.tab_dashboard, padding=20)
            rep_frame.pack(fill=tk.X)
            ttk.Button(rep_frame, text="Exporter Rapport Occupation des Salles", command=self.export_occ_report).pack(side=tk.LEFT)
            
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
        ens = item['values'][1]
        salle = item['values'][2]
        jr = item['values'][3]
        start = item['values'][4]
        
        # Double check availability if accepting
        if status == "Acceptée":
            if not salle_disponible(salle, jr, start):
                messagebox.showerror("Conflit", f"La salle {salle} est déjà occupée le {jr} à {start}.\n\nVous ne pouvez pas accepter cette demande.")
                return
        
        if modifier_statut_reservation(resa_id, status):
            msg = f"La demande de {ens} a été {status.lower()}."
            messagebox.showinfo("Succès", msg)
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
        
        ttk.Label(form, text="Salle (Optionnel/Libre):").grid(row=3, column=0, pady=5)
        self.cb_salle_avail = ttk.Combobox(form, values=["Veuillez choisir jour/heure"])
        self.cb_salle_avail.grid(row=3, column=1, pady=5)

        ttk.Label(form, text="Motif:").grid(row=4, column=0, pady=5)
        self.cb_motif_avail = ttk.Combobox(form, values=["Absence", "Maintenance", "Événement", "Indisponibilité", "Examen Exceptionnel"])
        self.cb_motif_avail.current(0)
        self.cb_motif_avail.grid(row=4, column=1, pady=5)
        
        btn_avail_frame = ttk.Frame(container)
        btn_avail_frame.pack(pady=10)
        ttk.Button(btn_avail_frame, text="Bloquer le créneau", command=self.block_teacher).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_avail_frame, text="Supprimer le blocage", command=self.delete_block).pack(side=tk.LEFT, padx=5)
        
        # Current blocks
        ttk.Label(container, text="Créneaux bloqués:", font=("Helvetica", 10, "bold")).pack(pady=(20,5))
        self.tree_blocked = ttk.Treeview(container, columns=("Enseignant", "Jour", "Heure", "Salle", "Motif"), show="headings", height=8)
        self.tree_blocked.heading("Enseignant", text="Enseignant")
        self.tree_blocked.heading("Jour", text="Jour")
        self.tree_blocked.heading("Heure", text="Heure")
        self.tree_blocked.heading("Salle", text="Salle")
        self.tree_blocked.heading("Motif", text="Motif")
        self.tree_blocked.pack(fill=tk.X)
        self.refresh_blocked()

    def block_teacher(self):
        ens = self.cb_ens_avail.get()
        jr = self.cb_jour_avail.get()
        start = self.cb_start_avail.get()
        room = self.cb_salle_avail.get()
        motif = self.cb_motif_avail.get()
        
        if not ens or not jr or not start:
            messagebox.showwarning("Attention", "Les champs Enseignant, Jour et Début sont requis.")
            return
            
        try:
            avail = charger_json("DONNÉES PRINCIPALES/availability.json")
            if "blocked_slots" not in avail: avail["blocked_slots"] = []
            block_item = {
                "enseignant": ens, 
                "jour": jr, 
                "debut": start,
                "motif": motif or "Indisponibilité"
            }
            if room and room != "Veuillez choisir jour/heure" and room != "Aucune salle libre": 
                block_item["salle"] = room
            
            avail["blocked_slots"].append(block_item)
            sauvegarder_json("DONNÉES PRINCIPALES/availability.json", avail)
            messagebox.showinfo("Succès", "Le créneau a été bloqué avec succès.")
            self.refresh_blocked()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def delete_block(self):
        selected = self.tree_blocked.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un blocage à supprimer.")
            return
        
        item = self.tree_blocked.item(selected[0])
        val = item['values']
        
        try:
            avail = charger_json("DONNÉES PRINCIPALES/availability.json")
            new_list = []
            for b in avail.get("blocked_slots", []):
                # Simple matching
                if b["enseignant"] == val[0] and b["jour"] == val[1] and b["debut"] == val[2]:
                    continue
                new_list.append(b)
            
            avail["blocked_slots"] = new_list
            sauvegarder_json("DONNÉES PRINCIPALES/availability.json", avail)
            messagebox.showinfo("Succès", "Blocage supprimé.")
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
                self.tree_blocked.insert("", tk.END, values=(
                    b["enseignant"], 
                    b["jour"], 
                    b["debut"], 
                    b.get("salle", "-"),
                    b.get("motif", "Indisponibilité")
                ))
        except: pass

    def export_edt_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            if exporter_csv(edt, path):
                messagebox.showinfo("Succès", "Export CSV réussi.")
            else:
                messagebox.showerror("Erreur", "L'export a échoué.")

    def export_edt_excel(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if path:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            if exporter_excel(edt, path):
                messagebox.showinfo("Succès", "Export Excel réussi.")
            else:
                messagebox.showerror("Erreur", "L'export Excel a échoué.\nVérifiez que 'openpyxl' est installé.")

    def export_edt_image(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if path:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            if exporter_visual(edt, path, "png"):
                messagebox.showinfo("Succès", "Export Image réussi.")
            else:
                messagebox.showerror("Erreur", "L'export Image a échoué.")

    def export_edt_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Document", "*.pdf")])
        if path:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            if exporter_visual(edt, path, "pdf"):
                messagebox.showinfo("Succès", "Export PDF réussi.")
            else:
                messagebox.showerror("Erreur", "L'export PDF a échoué.")

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
        for w in self.tab_data.winfo_children(): w.destroy()
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

    def on_tab_change(self, event):
        tab = self.notebook.tab(self.notebook.select(), "text")
        if tab == "Tableau de Bord": self.setup_dashboard()
        elif tab == "Réservations": self.setup_reservations()
        elif tab == "Occupation (Global)": self.setup_occupancy()
        elif tab == "Occupation (Temps Réel)": self.setup_realtime_occupancy()
        elif tab == "Statistiques": self.setup_stats()
        elif tab == "Données": self.setup_data_view()
        elif tab == "Disponibilités": self.setup_availability()
        elif tab == "Consultation & Export": self.setup_exports()

    def setup_exports(self):
        for w in self.tab_exports.winfo_children(): w.destroy()
        
        # --- Control Panel (Left) ---
        control_frame = ttk.Frame(self.tab_exports, padding=10, borderwidth=2, relief="groove")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Filtres de Visualisation", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        self.filter_var = tk.StringVar(value="Global")
        
        ttk.Radiobutton(control_frame, text="Global (Tout)", variable=self.filter_var, value="Global", command=self.update_filter_options).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(control_frame, text="Par Filière", variable=self.filter_var, value="Filiere", command=self.update_filter_options).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(control_frame, text="Par Enseignant", variable=self.filter_var, value="Enseignant", command=self.update_filter_options).pack(anchor=tk.W, pady=2)
        
        ttk.Separator(control_frame, orient="horizontal").pack(fill=tk.X, pady=10)
        
        self.lbl_choice = ttk.Label(control_frame, text="Sélectionner :")
        self.lbl_choice.pack(pady=5)
        
        self.cb_filter_choice = ttk.Combobox(control_frame)
        self.cb_filter_choice.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="🔍 Afficher", command=self.apply_filter).pack(fill=tk.X, pady=15)
        
        ttk.Label(control_frame, text="Exporter la vue :", font=("Helvetica", 10, "bold")).pack(pady=(20, 5))
        
        ttk.Button(control_frame, text="📄 PDF", command=lambda: self.export_filtered("pdf")).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="📊 Excel", command=lambda: self.export_filtered("excel")).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="🖼 Image", command=lambda: self.export_filtered("image")).pack(fill=tk.X, pady=2)
        
        # --- Display Panel (Right) ---
        display_frame = ttk.Frame(self.tab_exports)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Jour", "Heure", "Module", "Type", "Salle", "Enseignant", "Groupe")
        self.tree_export = ttk.Treeview(display_frame, columns=columns, show="headings")
        for col in columns:
            self.tree_export.heading(col, text=col)
            self.tree_export.column(col, width=100)
            
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree_export.yview)
        self.tree_export.configure(yscroll=scrollbar.set)
        
        self.tree_export.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_filter_options()

    def update_filter_options(self):
        choice = self.filter_var.get()
        self.cb_filter_choice.set("")
        
        if choice == "Global":
            self.cb_filter_choice.configure(state="disabled", values=[])
        
        elif choice == "Filiere":
            self.cb_filter_choice.configure(state="normal")
            try:
                # Extract unique filieres prefixes
                filieres_data = charger_json("DONNÉES PRINCIPALES/filieres (1).json")
                if isinstance(filieres_data, dict): filieres_data = filieres_data.get("filieres", [])
                
                # User request: Separate years (GEGM-1 vs GEGM-2)
                codes = set()
                for f in filieres_data:
                    c = f.get('code', '')
                    if c: codes.add(c)
                
                self.cb_filter_choice['values'] = sorted(list(codes))
            except: self.cb_filter_choice['values'] = []
            
        elif choice == "Enseignant":
            self.cb_filter_choice.configure(state="normal")
            try:
                # Get teachers from EDT or data? EDT is better to valid data.
                edt = charger_json("GESTION EDT/emplois_du_temps.json")
                teachers = sorted(list(set(s.get('enseignant', '') for s in edt if s.get('enseignant'))))
                self.cb_filter_choice['values'] = teachers
            except: self.cb_filter_choice['values'] = []

    def apply_filter(self):
        choice = self.filter_var.get()
        val = self.cb_filter_choice.get()
        self.current_filtered_edt = []
        
        # Clear tree
        for i in self.tree_export.get_children(): self.tree_export.delete(i)
        
        if choice != "Global" and not val:
            messagebox.showwarning("Attention", "Veuillez sélectionner une valeur à filtrer.")
            return

        try:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            filtered = []
            
            if choice == "Global":
                filtered = edt
            elif choice == "Filiere":
                # Filter by starts_with of code/groupe/filiere
                # In EDT, we have 'filiere' field usually.
                for s in edt:
                    f = s.get('filiere', '') or s.get('groupe', '')
                    # Check if 'val' is a prefix of 'f'
                    # e.g. val="GEGM", f="GEGM-1". 
                    if f.startswith(val):
                        filtered.append(s)
            elif choice == "Enseignant":
                filtered = [s for s in edt if s.get('enseignant') == val]
            
            self.current_filtered_edt = filtered
            
            # Sort
            day_order = {"Lundi":1, "Mardi":2, "Mercredi":3, "Jeudi":4, "Vendredi":5, "Samedi":6}
            filtered.sort(key=lambda x: (day_order.get(x.get('jour', ''), 7), x.get('debut', '')))
            
            for s in filtered:
                self.tree_export.insert("", tk.END, values=(
                    s.get('jour'), 
                    f"{s.get('debut')} - {s.get('fin')}", 
                    s.get('module'), 
                    s.get('type'), 
                    s.get('salle'), 
                    s.get('enseignant'), 
                    s.get('groupe')
                ))
            
            if not filtered:
                messagebox.showinfo("Info", "Aucun cours trouvé pour ce filtre.")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de filtrage: {e}")

    def export_filtered(self, format_type):
        if not self.current_filtered_edt:
            # Auto-apply filter if user forgot to click "Afficher"
            self.apply_filter()
            if not self.current_filtered_edt:
                return # apply_filter handles the warning if it fails or finds nothing
            
        title = f"Export {format_type.upper()}"
        ext = f".{format_type}" if format_type != "image" else ".png"
        if format_type == "excel": ext = ".xlsx"
        
        path = filedialog.asksaveasfilename(defaultextension=ext, title=title)
        if not path: return
        
        success = False
        if format_type == "pdf":
            success = exporter_visual(self.current_filtered_edt, path, "pdf")
        elif format_type == "image":
            success = exporter_visual(self.current_filtered_edt, path, "png")
        elif format_type == "excel":
            success = exporter_excel(self.current_filtered_edt, path)
            
        if success:
            messagebox.showinfo("Succès", f"Export {format_type.upper()} réussi !")
        else:
            messagebox.showerror("Erreur", "L'export a échoué.")

    def setup_stats(self):
        for w in self.tab_stats.winfo_children(): w.destroy()
        
        stats = get_advanced_stats()
        if not stats:
            ttk.Label(self.tab_stats, text="Impossible de générer les statistiques.").pack()
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Chart 1: Repartition par jour
        jours = list(stats['repartition_jour'].keys())
        seances = list(stats['repartition_jour'].values())
        ax1.bar(jours, seances, color="#3498db")
        ax1.set_title("Répartition des cours par jour")
        ax1.tick_params(axis='x', rotation=45)
        
        # Chart 2: Taux d'occupation par salle (Top 5)
        top_salles = sorted(stats['salle_stats'].items(), key=lambda x: x[1], reverse=True)[:5]
        s_names = [x[0] for x in top_salles]
        s_counts = [x[1] for x in top_salles]
        ax2.pie(s_counts, labels=s_names, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax2.set_title("Top 5 Salles les plus occupées")
        
        canvas = FigureCanvasTkAgg(fig, master=self.tab_stats)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Demand Stress (Plages)
        demand_frame = ttk.LabelFrame(self.tab_stats, text="Plages Horaires les plus demandées", padding=10)
        demand_frame.pack(fill=tk.X, padx=20, pady=20)
        
        for p, count in sorted(stats['plages_demande'].items(), key=lambda x: x[1], reverse=True)[:5]:
            ttk.Label(demand_frame, text=f"• {p} : {count} demandes (EDT + Réservations)").pack(anchor=tk.W)

    def setup_realtime_occupancy(self):
        for w in self.tab_realtime_occ.winfo_children(): w.destroy()
        
        control_frame = ttk.Frame(self.tab_realtime_occ, padding=10)
        control_frame.pack(fill=tk.X)
        
        ttk.Label(control_frame, text="Consulter l'état des salles pour :").pack(side=tk.LEFT, padx=5)
        
        self.cb_real_jour = ttk.Combobox(control_frame, values=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"], width=10)
        self.cb_real_jour.current(0)
        self.cb_real_jour.pack(side=tk.LEFT, padx=5)
        
        self.cb_real_heure = ttk.Combobox(control_frame, values=["09:00", "10:45", "12:30", "14:15", "16:00"], width=10)
        self.cb_real_heure.current(0)
        self.cb_real_heure.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Vérifier l'Occupation", command=self.refresh_realtime_view).pack(side=tk.LEFT, padx=5)
        
        self.rooms_container = ttk.Frame(self.tab_realtime_occ, padding=20)
        self.rooms_container.pack(fill=tk.BOTH, expand=True)
        self.refresh_realtime_view()

    def refresh_realtime_view(self):
        for w in self.rooms_container.winfo_children(): w.destroy()
        
        jr = self.cb_real_jour.get()
        hh = self.cb_real_heure.get()
        
        try:
            salles = charger_json("DONNÉES PRINCIPALES/salles.json")
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            resas = charger_json("GESTION EDT/reservations.json")
            
            # Use Canvas for grid
            canvas = tk.Canvas(self.rooms_container)
            scrollbar_y = ttk.Scrollbar(self.rooms_container, orient="vertical", command=canvas.yview)
            scrollbar_x = ttk.Scrollbar(self.rooms_container, orient="horizontal", command=canvas.xview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")
            canvas.pack(side="left", fill="both", expand=True)
            
            row, col = 0, 0
            for s in salles:
                # Check status
                status = "LIBRE"
                color = "#2ecc71" # Green
                
                # Check EDT
                occs = [x for x in edt if x['salle'] == s['nom'] and x['jour'] == jr and x['debut'] == hh]
                if occs:
                    status = f"OCCUPÉE\n({occs[0]['module']})"
                    color = "#e74c3c" # Red
                else:
                    # Check Accepted Reservations
                    res_occs = [x for x in resas if x['salle'] == s['nom'] and x['jour'] == jr and x['debut'] == hh and x['statut'] == "Acceptée"]
                    if res_occs:
                        status = f"RÉSERVÉE\n({res_occs[0]['enseignant']})"
                        color = "#f1c40f" # Yellow
                
                card = tk.Frame(scrollable_frame, bg=color, width=150, height=100, borderwidth=1, relief="solid")
                card.grid(row=row, column=col, padx=10, pady=10)
                card.grid_propagate(False)
                
                tk.Label(card, text=s['nom'], bg=color, fg="white", font=("Helvetica", 10, "bold")).pack(pady=5)
                tk.Label(card, text=status, bg=color, fg="white", font=("Helvetica", 8)).pack()
                
                col += 1
                if col > 3: # Reduced to 4 columns (0-3) to ensure visibility without horizontal scroll if possible
                    col = 0
                    row += 1
            
            # Force update to ensure scrollregion is correct
            scrollable_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        except Exception as e:
            ttk.Label(self.rooms_container, text=f"Erreur: {e}").pack()

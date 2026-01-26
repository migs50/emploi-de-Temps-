import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from logic.database import charger_json, sauvegarder_json
from logic.reservation_manager import ajouter_reservation, rechercher_salles, ajouter_demande_indisponibilite
from logic.exporter import exporter_csv, exporter_excel, exporter_visual

class TeacherInterface:
    def normalize_name(self, name):
        """Standardize name for comparison: lower, remove titles, strip."""
        if not name: return ""
        name = name.lower()
        for title in ["dr.", "pr.", "mr.", "mme.", "dr ", "pr "]:
            name = name.replace(title, "")
        return name.strip()

    def __init__(self, root):
        self.root = root
        
        # Sidebar for selection
        left_panel = ttk.Frame(root, padding=10, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(left_panel, text="Sélectionnez votre profil :").pack(pady=5)
        
        self.teachers = self.load_teachers()
        # Format: "Name (Specialty)"
        teacher_names = [f"{t['nom']} {t.get('prenom', '')} ({t.get('specialite', 'N/A')})" for t in self.teachers]
        
        self.selected_teacher = tk.StringVar()
        self.cb_teacher = ttk.Combobox(left_panel, textvariable=self.selected_teacher, values=teacher_names)
        self.cb_teacher.pack(fill=tk.X, pady=5)
        self.cb_teacher.bind("<<ComboboxSelected>>", self.on_teacher_select)
        
        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.tab_edt = ttk.Frame(self.notebook)
        self.tab_resa = ttk.Frame(self.notebook)
        self.tab_unavail = ttk.Frame(self.notebook)
        self.tab_notif = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_edt, text="Mon Emploi du Temps")
        self.notebook.add(self.tab_resa, text="Réserver une Salle")
        self.notebook.add(self.tab_unavail, text="Déclarer Indisponibilité")
        self.notebook.add(self.tab_notif, text="Mes Notifications")
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        self.setup_edt_view()
        self.setup_reservation_view()
        self.setup_unavailability_view()
        self.setup_notification_view()

    def load_teachers(self):
        try:
            data = charger_json("DONNÉES PRINCIPALES/enseignants_final.json")
            if isinstance(data, dict):
                return data.get("enseignants", [])
            return data
        except:
            return []

    def on_teacher_select(self, event):
        self.display_edt()
        self.refresh_notifs()

    def on_tab_change(self, event):
        tab = self.notebook.tab(self.notebook.select(), "text")
        if tab == "Mes Notifications":
            self.refresh_notifs()

    def display_edt(self):
        # Refresh logic handles clearing
        self.refresh_edt_table()
        
    def refresh_edt_table(self, event=None):
        # Clear previous tree content only
        for i in self.tree_edt.get_children():
            self.tree_edt.delete(i)
            
        name = self.selected_teacher.get()
        if not name: return
        
        # Find teacher info matching the selection (ignoring the specialty part)
        teacher_nom = ""
        teacher_id = None
        
        # Selected name format is "Dr. Name (Specialty)" -> Split to get name part
        selected_display = name
        # We try to match by strictly checking if t['nom'] is in the string
        
        for t in self.teachers:
            # Check if selected string contains the Last Name
            if t['nom'] in selected_display: 
                teacher_id = t['id']
                teacher_nom = t['nom']
                break
        
         # Load EDT
        
        # Load EDT
        try:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            my_sessions = []
            
            # Helper for matching
            def distinct_words(n):
                return set(w for w in self.normalize_name(n).split() if len(w) > 2)

            # Key for robust matching
            teacher_tokens = distinct_words(teacher_nom)
            if not teacher_tokens: # Fallback
                 teacher_tokens = distinct_words(name.split('(')[0]) # Remove (Specialty)

            for s in edt:
                ens_name = s.get('enseignant', '')
                ens_id = str(s.get('enseignant_id', ''))
                
                # 1. Exact ID Match (Best)
                if teacher_id and str(teacher_id) == ens_id:
                    my_sessions.append(s)
                    continue
                    
                # 2. Robust Name Match
                # Check if sufficient overlap of significant words (e.g. "Hassan", "Yousfi" in target)
                target_tokens = distinct_words(ens_name)
                
                # Match if ALL teacher tokens are in target, OR if target tokens are in teacher
                # (handles "Hassan Yousfi" vs "Dr. Hassan Yousfi")
                if teacher_tokens and target_tokens:
                    if teacher_tokens.issubset(target_tokens) or target_tokens.issubset(teacher_tokens):
                         my_sessions.append(s)
            
            if not my_sessions:
                     pass # Will be empty
                
            # Filtering Logic
            mode = self.view_mode.get() # 'Semaine' or 'Jour'
            day_filter = self.cb_day_filter.get()
            
            filtered_sessions = []
            for s in my_sessions:
                if mode == "Semaine":
                    filtered_sessions.append(s)
                elif mode == "Jour":
                    if s['jour'] == day_filter:
                        filtered_sessions.append(s)
            
            if not filtered_sessions:
                 pass # Tree is empty, maybe show a status label if needed but tree remains
            
            # Sort by day/time
            day_order = {"Lundi":1, "Mardi":2, "Mercredi":3, "Jeudi":4, "Vendredi":5, "Samedi":6}
            filtered_sessions.sort(key=lambda x: (day_order.get(x['jour'], 7), x['debut']))
            
            for s in filtered_sessions:
                self.tree_edt.insert("", tk.END, values=(s['jour'], f"{s['debut']} - {s['fin']}", s['module'], s['salle'], s['groupe']))
                
        except Exception as e:
            print(f"Erreur affichage EDT: {e}")

    def setup_edt_view(self):
        for w in self.tab_edt.winfo_children(): w.destroy()
        
        # Controls
        ctrl_frame = ttk.Frame(self.tab_edt, padding=10)
        ctrl_frame.pack(fill=tk.X)
        
        ttk.Label(ctrl_frame, text="Vue :").pack(side=tk.LEFT, padx=5)
        
        self.view_mode = tk.StringVar(value="Semaine")
        ttk.Radiobutton(ctrl_frame, text="Hebdomadaire", variable=self.view_mode, value="Semaine", command=self.refresh_edt_table).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(ctrl_frame, text="Journalier", variable=self.view_mode, value="Jour", command=self.refresh_edt_table).pack(side=tk.LEFT, padx=5)
        
        self.cb_day_filter = ttk.Combobox(ctrl_frame, values=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"], state="readonly", width=10)
        self.cb_day_filter.current(0)
        self.cb_day_filter.pack(side=tk.LEFT, padx=5)
        self.cb_day_filter.bind("<<ComboboxSelected>>", self.refresh_edt_table)
        
        # Export buttons
        ttk.Label(ctrl_frame, text="  |  Exporter:").pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="📄 PDF", command=self.export_pdf, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(ctrl_frame, text="📊 Excel", command=self.export_excel, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(ctrl_frame, text="🖼 Image", command=self.export_image, width=8).pack(side=tk.LEFT, padx=2)
        
        # Treeview
        columns = ("Jour", "Heure", "Module", "Salle", "Groupe")
        self.tree_edt = ttk.Treeview(self.tab_edt, columns=columns, show="headings")
        self.tree_edt.heading("Jour", text="Jour")
        self.tree_edt.heading("Heure", text="Heure")
        self.tree_edt.heading("Module", text="Module")
        self.tree_edt.heading("Salle", text="Salle")
        self.tree_edt.heading("Groupe", text="Groupe")
        
        self.tree_edt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def setup_reservation_view(self):
        for w in self.tab_resa.winfo_children(): w.destroy()
        
        # --- PANNEAU DE RECHERCHE ---
        search_frame = ttk.LabelFrame(self.tab_resa, text="1. Recherche Avancée de Salle", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Criteria Grid
        grid_frame = ttk.Frame(search_frame)
        grid_frame.pack(fill=tk.X)
        
        ttk.Label(grid_frame, text="Jour:").grid(row=0, column=0, padx=5, sticky="w")
        self.cb_search_day = ttk.Combobox(grid_frame, values=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"], width=10)
        self.cb_search_day.current(0)
        self.cb_search_day.grid(row=0, column=1, padx=5)
        
        ttk.Label(grid_frame, text="Heure:").grid(row=0, column=2, padx=5, sticky="w")
        self.cb_search_hour = ttk.Combobox(grid_frame, values=["09:00", "10:45", "12:30", "14:15", "16:00"], width=8)
        self.cb_search_hour.current(0)
        self.cb_search_hour.grid(row=0, column=3, padx=5)
        
        ttk.Label(grid_frame, text="Capacité Min:").grid(row=0, column=4, padx=5, sticky="w")
        self.entry_cap = ttk.Entry(grid_frame, width=5)
        self.entry_cap.grid(row=0, column=5, padx=5)
        self.entry_cap.insert(0, "0")
        
        # Equipment Checks
        equip_frame = ttk.Frame(search_frame)
        equip_frame.pack(fill=tk.X, pady=5)
        self.chk_video = tk.BooleanVar()
        self.chk_wifi = tk.BooleanVar()
        self.chk_audio = tk.BooleanVar()
        
        ttk.Checkbutton(equip_frame, text="Vidéoprojecteur (Datashow)", variable=self.chk_video).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(equip_frame, text="Wifi", variable=self.chk_wifi).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(equip_frame, text="Sono / Audio", variable=self.chk_audio).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(search_frame, text="🔍 Rechercher Salles Libres", command=self.perform_search).pack(pady=5)

        # --- RESULTATS ---
        res_frame = ttk.LabelFrame(self.tab_resa, text="2. Salles Disponibles (Double-cliquez pour sélectionner)", padding=10)
        res_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        cols = ("Salle", "Type", "Capacité", "Équipements")
        self.tree_search = ttk.Treeview(res_frame, columns=cols, show="headings", height=6)
        for c in cols: self.tree_search.heading(c, text=c)
        
        self.tree_search.pack(fill=tk.BOTH, expand=True)
        self.tree_search.bind("<<TreeviewSelect>>", self.autofill_reservation)

        # --- FINALISATION ---
        final_frame = ttk.LabelFrame(self.tab_resa, text="3. Finaliser la Demande", padding=10)
        final_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Form
        f_grid = ttk.Frame(final_frame)
        f_grid.pack(fill=tk.X)
        
        ttk.Label(f_grid, text="Salle:").grid(row=0, column=0, padx=5)
        self.entry_final_salle = ttk.Entry(f_grid, state="readonly")
        self.entry_final_salle.grid(row=0, column=1, padx=5)
        
        ttk.Label(f_grid, text="Créneau:").grid(row=0, column=2, padx=5)
        self.entry_final_slot = ttk.Entry(f_grid, state="readonly", width=30)
        self.entry_final_slot.grid(row=0, column=3, padx=5)
        
        ttk.Label(f_grid, text="Motif:").grid(row=1, column=0, padx=5, pady=5)
        self.cb_motif = ttk.Combobox(f_grid, values=["Cours supplémentaire", "Rattrapage", "Réunion pédagogique", "Examen exceptionnel", "Autre"])
        self.cb_motif.current(1)
        self.cb_motif.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(final_frame, text="Envoyer la Demande", command=self.submit_reservation_advanced).pack(pady=10)

    def perform_search(self):
        # Clear tree
        for i in self.tree_search.get_children(): self.tree_search.delete(i)
        
        day = self.cb_search_day.get()
        hour = self.cb_search_hour.get()
        try:
            min_cap = int(self.entry_cap.get())
        except: min_cap = 0
        
        equips = []
        if self.chk_video.get(): equips.append("datashow")
        if self.chk_wifi.get(): equips.append("wifi")
        if self.chk_audio.get(): equips.append("sono")
        
        results = rechercher_salles(day, hour, min_cap, equips)
        
        if not results:
            messagebox.showinfo("Info", "Aucune salle ne correspond à vos critères.")
            return
            
        for r in results:
            eq_str = ", ".join(r.get("equipements", []))
            self.tree_search.insert("", tk.END, values=(r["nom"], r.get("type", "?"), r.get("capacite", "?"), eq_str))

    def autofill_reservation(self, event):
        sel = self.tree_search.selection()
        if not sel: return
        val = self.tree_search.item(sel[0])['values']
        salle_nom = val[0]
        
        # Fill form
        self.entry_final_salle.configure(state="normal")
        self.entry_final_salle.delete(0, tk.END)
        self.entry_final_salle.insert(0, salle_nom)
        self.entry_final_salle.configure(state="readonly")
        
        slot_str = f"{self.cb_search_day.get()} à {self.cb_search_hour.get()}"
        self.entry_final_slot.configure(state="normal")
        self.entry_final_slot.delete(0, tk.END)
        self.entry_final_slot.insert(0, slot_str)
        self.entry_final_slot.configure(state="readonly")
        
    def submit_reservation_advanced(self):
        salle = self.entry_final_salle.get()
        if not salle:
            messagebox.showwarning("Attention", "Veuillez sélectionner une salle dans la liste.")
            return
            
        # Parse slot string back to day/hour
        # Format "Lundi à 09:00"
        try:
            slot_parts = self.entry_final_slot.get().split(" à ")
            jour = slot_parts[0]
            debut = slot_parts[1]
        except:
             messagebox.showerror("Erreur", "Format de créneau invalide.")
             return

        resa = {
            "enseignant": self.selected_teacher.get(),
            "salle": salle,
            "jour": jour,
            "debut": debut,
            "motif": self.cb_motif.get()
        }
        
        if ajouter_reservation(resa):
            messagebox.showinfo("Succès", "Demande envoyée à l'administration !")
            # Reset
            self.entry_final_salle.configure(state="normal")
            self.entry_final_salle.delete(0, tk.END)
            self.entry_final_salle.configure(state="readonly")
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'enregistrement.")

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

    def setup_notification_view(self):
        for widget in self.tab_notif.winfo_children(): widget.destroy()
        
        ttk.Label(self.tab_notif, text="Notifications & Alertes", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        columns = ("Date", "Détails", "Statut")
        self.tree_notif = ttk.Treeview(self.tab_notif, columns=columns, show="headings")
        self.tree_notif.heading("Date", text="Date")
        self.tree_notif.heading("Détails", text="Détails de la demande")
        self.tree_notif.heading("Statut", text="Décision")
        self.tree_notif.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        btn_box = ttk.Frame(self.tab_notif)
        btn_box.pack(pady=10)
        ttk.Button(btn_box, text="Marquer comme lu", command=self.mark_as_read).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Rafraîchir", command=self.refresh_notifs).pack(side=tk.LEFT, padx=5)

    def refresh_notifs(self):
        if not hasattr(self, 'tree_notif'): return
        
        for i in self.tree_notif.get_children(): self.tree_notif.delete(i)
        
        teacher_name = self.selected_teacher.get()
        if not teacher_name: return
        
        try:
            notifs = charger_json("GESTION EDT/notifications.json") or []
            # Filter for this teacher
            my_notifs = [n for n in notifs if n["enseignant"] == teacher_name]
            my_notifs.sort(key=lambda x: x["date"], reverse=True)
            
            for n in my_notifs:
                details = f"{n['jour']} à {n['debut']} - Salle: {n['salle']}"
                tag = "new" if not n.get("lu") else ""
                self.tree_notif.insert("", tk.END, values=(n["date"], details, n["statut"]), tags=(tag,))
            
            self.tree_notif.tag_configure("new", background="#e1f5fe")
        except: pass

    def mark_as_read(self):
        teacher_name = self.selected_teacher.get()
        if not teacher_name: return
        
        try:
            notifs = charger_json("GESTION EDT/notifications.json") or []
            for n in notifs:
                if n["enseignant"] == teacher_name:
                    n["lu"] = True
            sauvegarder_json("GESTION EDT/notifications.json", notifs)
            self.refresh_notifs()
        except: pass

    def setup_unavailability_view(self):
        """Setup unavailability request form"""
        for w in self.tab_unavail.winfo_children(): w.destroy()
        
        # Header
        header = ttk.Label(self.tab_unavail, text="Déclarer une Indisponibilité", font=("Helvetica", 14, "bold"))
        header.pack(pady=10)
        
        info = ttk.Label(self.tab_unavail, text="Signalez vos absences prévues, déplacements ou congés.\nL'administrateur validera votre demande.", 
                        foreground="gray")
        info.pack(pady=5)
        
        # Form
        form_frame = ttk.LabelFrame(self.tab_unavail, text="Informations", padding=20)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Jour :").grid(row=0, column=0, sticky="w", pady=5)
        self.cb_unavail_day = ttk.Combobox(form_frame, values=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"], width=15)
        self.cb_unavail_day.current(0)
        self.cb_unavail_day.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(form_frame, text="Heure début :").grid(row=1, column=0, sticky="w", pady=5)
        self.cb_unavail_start = ttk.Combobox(form_frame, values=["09:00", "10:45", "12:30", "14:15", "16:00"], width=15)
        self.cb_unavail_start.current(0)
        self.cb_unavail_start.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(form_frame, text="Motif :").grid(row=2, column=0, sticky="w", pady=5)
        self.cb_unavail_motif = ttk.Combobox(form_frame, 
                                             values=["Absence prévue", "Déplacement professionnel", "Congé", "Réunion institutionnelle", "Autre"],
                                             width=25)
        self.cb_unavail_motif.current(0)
        self.cb_unavail_motif.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(form_frame, text="Détails (optionnel) :").grid(row=3, column=0, sticky="nw", pady=5)
        self.entry_unavail_details = tk.Text(form_frame, height=3, width=40)
        self.entry_unavail_details.grid(row=3, column=1, pady=5, padx=5)
        
        # Submit button
        ttk.Button(form_frame, text="📤 Envoyer la Demande", command=self.submit_unavailability).grid(row=4, column=1, pady=15)
        
        # Status message
        self.lbl_unavail_status = ttk.Label(self.tab_unavail, text="", foreground="green")
        self.lbl_unavail_status.pack(pady=5)

    def submit_unavailability(self):
        """Submit unavailability request"""
        teacher_name = self.selected_teacher.get()
        if not teacher_name:
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner votre profil.")
            return
        
        demande = {
            "enseignant": teacher_name,
            "jour": self.cb_unavail_day.get(),
            "debut": self.cb_unavail_start.get(),
            "motif": self.cb_unavail_motif.get(),
            "details": self.entry_unavail_details.get("1.0", tk.END).strip()
        }
        
        if ajouter_demande_indisponibilite(demande):
            messagebox.showinfo("Succès", "Votre demande d'indisponibilité a été envoyée à l'administration.\nVous serez notifié de la décision.")
            # Reset form
            self.cb_unavail_day.current(0)
            self.cb_unavail_start.current(0)
            self.cb_unavail_motif.current(0)
            self.entry_unavail_details.delete("1.0", tk.END)
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'enregistrement de la demande.")
    
    def get_my_sessions(self):
        """Get current teacher's sessions for export"""
        name = self.selected_teacher.get()
        if not name:
            return []
        
        # Find teacher info
        teacher_nom = ""
        teacher_id = None
        for t in self.teachers:
            if t['nom'] in name:
                teacher_id = t['id']
                teacher_nom = t['nom']
                break
        
        try:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            my_sessions = []
            
            def distinct_words(n):
                return set(w for w in self.normalize_name(n).split() if len(w) > 2)
            
            teacher_tokens = distinct_words(teacher_nom)
            if not teacher_tokens:
                teacher_tokens = distinct_words(name.split('(')[0])
            
            for s in edt:
                ens_name = s.get('enseignant', '')
                ens_id = str(s.get('enseignant_id', ''))
                
                if teacher_id and str(teacher_id) == ens_id:
                    my_sessions.append(s)
                    continue
                
                target_tokens = distinct_words(ens_name)
                if teacher_tokens and target_tokens:
                    if teacher_tokens.issubset(target_tokens) or target_tokens.issubset(teacher_tokens):
                        my_sessions.append(s)
            
            return my_sessions
        except:
            return []
    
    def export_pdf(self):
        """Export teacher's schedule to PDF"""
        sessions = self.get_my_sessions()
        if not sessions:
            messagebox.showwarning("Attention", "Aucune séance à exporter. Sélectionnez votre profil.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"EDT_{self.selected_teacher.get().split('(')[0].strip()}.pdf"
        )
        if path:
            if exporter_visual(sessions, path, "pdf"):
                messagebox.showinfo("Succès", "Export PDF réussi !")
            else:
                messagebox.showerror("Erreur", "L'export PDF a échoué.")
    
    def export_excel(self):
        """Export teacher's schedule to Excel"""
        sessions = self.get_my_sessions()
        if not sessions:
            messagebox.showwarning("Attention", "Aucune séance à exporter. Sélectionnez votre profil.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile=f"EDT_{self.selected_teacher.get().split('(')[0].strip()}.xlsx"
        )
        if path:
            if exporter_excel(sessions, path):
                messagebox.showinfo("Succès", "Export Excel réussi !")
            else:
                messagebox.showerror("Erreur", "L'export Excel a échoué.")
    
    def export_image(self):
        """Export teacher's schedule to Image"""
        sessions = self.get_my_sessions()
        if not sessions:
            messagebox.showwarning("Attention", "Aucune séance à exporter. Sélectionnez votre profil.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile=f"EDT_{self.selected_teacher.get().split('(')[0].strip()}.png"
        )
        if path:
            if exporter_visual(sessions, path, "png"):
                messagebox.showinfo("Succès", "Export Image réussi !")
            else:
                messagebox.showerror("Erreur", "L'export Image a échoué.")

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import datetime
from logic.database import charger_json
from logic.reservation_manager import get_salles_disponibles
from logic.exporter import exporter_csv, exporter_excel, exporter_visual

class StudentInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Espace Étudiant - Consultation & Recherche")
        
        # Main Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabs
        self.tab_edt = ttk.Frame(self.notebook)
        self.tab_rooms = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_edt, text="Mon Emploi du Temps")
        self.notebook.add(self.tab_rooms, text="Salles Libres")
        
        # Setup Tab 1: EDTS
        self.setup_edt_tab()
        
        # Setup Tab 2: Free Rooms
        self.setup_rooms_tab()
        
        # Real-time state
        self.last_edt_mtime = 0
        self.check_for_updates()

    def setup_edt_tab(self):
        main_frame = ttk.Frame(self.tab_edt, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        selection_frame = ttk.LabelFrame(main_frame, text="Recherche et Suivi en Temps Réel", padding=10)
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(selection_frame, text="Ma Filière :").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.filieres = self.load_filieres()
        filiere_codes = [f['code'] for f in self.filieres]
        
        self.selected_filiere = tk.StringVar()
        self.cb_filiere = ttk.Combobox(selection_frame, textvariable=self.selected_filiere, values=filiere_codes, width=25)
        self.cb_filiere.grid(row=0, column=1, padx=5, pady=5)
        self.cb_filiere.bind("<<ComboboxSelected>>", self.on_filiere_selected)
        
        ttk.Label(selection_frame, text="Mon Groupe :").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.selected_group = tk.StringVar()
        self.cb_group = ttk.Combobox(selection_frame, textvariable=self.selected_group, values=["Sélect. filière"], width=15)
        self.cb_group.grid(row=0, column=3, padx=5, pady=5)
        self.cb_group.bind("<<ComboboxSelected>>", self.display_edt)
        
        self.btn_refresh = ttk.Button(selection_frame, text="🔄 Actualiser", command=self.manual_refresh)
        self.btn_refresh.grid(row=0, column=4, padx=10, pady=5)
        
        self.lbl_status = ttk.Label(selection_frame, text="Dernière synchro: --:--", font=("Helvetica", 9, "italic"))
        self.lbl_status.grid(row=0, column=5, padx=5, pady=5)
        
        # Export buttons
        export_frame = ttk.Frame(main_frame)
        export_frame.pack(fill=tk.X, pady=5)
        ttk.Label(export_frame, text="Exporter mon emploi du temps:").pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="📄 PDF", command=self.export_pdf, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(export_frame, text="📊 Excel", command=self.export_excel, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(export_frame, text="🖼 Image", command=self.export_image, width=10).pack(side=tk.LEFT, padx=2)

        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Jour", "Heure", "Module", "Type", "Salle", "Prof")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            width = 100
            if col == "Module": width = 250
            if col == "Prof": width = 150
            self.tree.column(col, width=width)
            
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

    def setup_rooms_tab(self):
        main_frame = ttk.Frame(self.tab_rooms, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        search_frame = ttk.LabelFrame(main_frame, text="Rechercher une salle libre (Révisions / Travail de groupe)", padding=10)
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(search_frame, text="Jour :").grid(row=0, column=0, padx=5, pady=5)
        self.cb_search_day = ttk.Combobox(search_frame, values=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"])
        self.cb_search_day.grid(row=0, column=1, padx=5, pady=5)
        self.cb_search_day.current(0)
        
        ttk.Label(search_frame, text="Heure :").grid(row=0, column=2, padx=5, pady=5)
        self.cb_search_time = ttk.Combobox(search_frame, values=["09:00", "10:45", "12:30", "14:15", "16:00"])
        self.cb_search_time.grid(row=0, column=3, padx=5, pady=5)
        self.cb_search_time.current(0)
        
        ttk.Button(search_frame, text="🔍 Trouver", command=self.search_free_rooms).grid(row=0, column=4, padx=10)
        
        # Results Tree
        self.rooms_tree = ttk.Treeview(main_frame, columns=("Salle",), show="headings")
        self.rooms_tree.heading("Salle", text="Salle Libres")
        self.rooms_tree.column("Salle", width=300, anchor=tk.CENTER)
        self.rooms_tree.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Note: Ces salles sont vides sur ce créneau d'après l'emploi du temps officiel.", 
                  font=("Helvetica", 8, "italic"), foreground="blue").pack(pady=5)

    def search_free_rooms(self):
        for i in self.rooms_tree.get_children(): self.rooms_tree.delete(i)
        
        day = self.cb_search_day.get()
        time = self.cb_search_time.get()
        
        free_room_names = get_salles_disponibles(day, time)
        
        try:
            all_salles = charger_json("DONNÉES PRINCIPALES/salles.json")
            filtered_rooms = []
            for s in all_salles:
                if s["nom"] in free_room_names:
                    # Filter: Only TD or Preparation (Library)
                    if s.get("type") in ["TD", "Préparation"]:
                        filtered_rooms.append(s["nom"])
            
            for name in sorted(filtered_rooms):
                self.rooms_tree.insert("", tk.END, values=(name,))
            
            if not filtered_rooms:
                messagebox.showinfo("Information", f"Aucune salle de type TD ou Bibliothèque n'est libre le {day} à {time}.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def load_filieres(self):
        try:
            data = charger_json("DONNÉES PRINCIPALES/filieres (1).json")
            if isinstance(data, dict): return data.get("filieres", [])
            return data
        except: return []

    def on_filiere_selected(self, event):
        filiere_code = self.selected_filiere.get()
        try:
            seances = charger_json("DONNÉES PRINCIPALES/seances.json")
            all_groups = sorted(list(set([s.get('groupe', '') for s in seances if s.get('filiere') == filiere_code])))
            
            # If sub-groups like G1, G2 exist, filter out the base filiere code
            # so the user defaults to a specific group (showing their TDs)
            sub_groups = [g for g in all_groups if g != filiere_code]
            if sub_groups:
                groups = sub_groups
            else:
                groups = [filiere_code] if filiere_code in all_groups else all_groups
                
            self.cb_group['values'] = groups
            self.cb_group.set(groups[0] if groups else "")
            self.display_edt(None)
        except: pass

    def manual_refresh(self):
        self.display_edt(None)
        self.update_status_label()

    def update_status_label(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.lbl_status.config(text=f"Dernière synchro: {now}")

    def check_for_updates(self):
        path = "GESTION EDT/emplois_du_temps.json"
        try:
            if os.path.exists(path):
                current_mtime = os.path.getmtime(path)
                if self.last_edt_mtime != 0 and current_mtime > self.last_edt_mtime:
                    if self.selected_group.get():
                        self.display_edt(None)
                self.last_edt_mtime = current_mtime
        except: pass
        self.root.after(5000, self.check_for_updates)

    def display_edt(self, event):
        for i in self.tree.get_children(): self.tree.delete(i)
        filiere = self.selected_filiere.get()
        group = self.selected_group.get()
        if not group: return
        try:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            my_sessions = []
            for s in edt:
                if s.get('groupe') == group or (s.get('filiere') == filiere and s.get('type') == 'Cours'):
                    my_sessions.append(s)
            day_order = {"Lundi":1, "Mardi":2, "Mercredi":3, "Jeudi":4, "Vendredi":5, "Samedi":6}
            my_sessions.sort(key=lambda x: (day_order.get(x['jour'], 7), x['debut']))
            for s in my_sessions:
                self.tree.insert("", tk.END, values=(
                    s['jour'], f"{s['debut']} - {s['fin']}", s['module'], 
                    s.get('type', 'Cours'), s['salle'], s['enseignant']
                ))
            self.update_status_label()
        except: pass
    
    def get_my_sessions(self):
        """Get current student's sessions for export"""
        filiere = self.selected_filiere.get()
        group = self.selected_group.get()
        if not group:
            return []
        
        try:
            edt = charger_json("GESTION EDT/emplois_du_temps.json")
            my_sessions = []
            for s in edt:
                if s.get('groupe') == group or (s.get('filiere') == filiere and s.get('type') == 'Cours'):
                    my_sessions.append(s)
            return my_sessions
        except:
            return []
    
    def export_pdf(self):
        """Export student's schedule to PDF"""
        sessions = self.get_my_sessions()
        if not sessions:
            messagebox.showwarning("Attention", "Aucune séance à exporter. Sélectionnez votre filière et groupe.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"EDT_{self.selected_group.get()}.pdf"
        )
        if path:
            if exporter_visual(sessions, path, "pdf"):
                messagebox.showinfo("Succès", "Export PDF réussi !")
            else:
                messagebox.showerror("Erreur", "L'export PDF a échoué.")
    
    def export_excel(self):
        """Export student's schedule to Excel"""
        sessions = self.get_my_sessions()
        if not sessions:
            messagebox.showwarning("Attention", "Aucune séance à exporter. Sélectionnez votre filière et groupe.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile=f"EDT_{self.selected_group.get()}.xlsx"
        )
        if path:
            if exporter_excel(sessions, path):
                messagebox.showinfo("Succès", "Export Excel réussi !")
            else:
                messagebox.showerror("Erreur", "L'export Excel a échoué.")
    
    def export_image(self):
        """Export student's schedule to Image"""
        sessions = self.get_my_sessions()
        if not sessions:
            messagebox.showwarning("Attention", "Aucune séance à exporter. Sélectionnez votre filière et groupe.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile=f"EDT_{self.selected_group.get()}.png"
        )
        if path:
            if exporter_visual(sessions, path, "png"):
                messagebox.showinfo("Succès", "Export Image réussi !")
            else:
                messagebox.showerror("Erreur", "L'export Image a échoué.")

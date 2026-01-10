import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the project root directory to the python path to allow imports from logic/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaces.admin_interface import AdminInterface
from interfaces.teacher_interface import TeacherInterface
from interfaces.student_interface import StudentInterface

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion d'Emploi du Temps Universitaire")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Header
        header_frame = tk.Frame(root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="Système de Gestion d'Emploi du Temps", 
                               font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=20)
        
        # Main Content
        content_frame = tk.Frame(root, pady=20)
        content_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(content_frame, text="Veuillez sélectionner votre espace :", 
                 font=("Helvetica", 12)).pack(pady=20)
        
        # Buttons
        btn_frame = tk.Frame(content_frame)
        btn_frame.pack(pady=10)
        
        self.create_role_btn(btn_frame, "Administrateur", "#e74c3c", self.open_admin)
        self.create_role_btn(btn_frame, "Enseignant", "#3498db", self.open_teacher)
        self.create_role_btn(btn_frame, "Étudiant", "#2ecc71", self.open_student)
        
        # Footer
        footer_label = tk.Label(root, text="© 2026 Université - Gestion EDT", 
                                font=("Arial", 8), bg="#ecf0f1", pady=5)
        footer_label.pack(side=tk.BOTTOM, fill=tk.X)

    def create_role_btn(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Helvetica", 12, "bold"), 
                        bg=color, fg="white", width=20, height=2, 
                        command=command, relief=tk.FLAT, cursor="hand2")
        btn.pack(pady=10)

    def open_admin(self):
        self.new_window("Espace Administrateur", AdminInterface)

    def open_teacher(self):
        self.new_window("Espace Enseignant", TeacherInterface)

    def open_student(self):
        self.new_window("Espace Étudiant", StudentInterface)

    def new_window(self, title, interface_class):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("1000x700")
        app = interface_class(window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

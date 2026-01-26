"""
Générateur de Rapport PDF pour le Projet EDT
Auteur: Système de Gestion Universitaire
Date: 2026-01-26
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, 
                                TableStyle, PageBreak, Image, KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import json
import os
from datetime import datetime

class PDFReportGenerator:
    def __init__(self, output_path="Rapport_Projet_EDT.pdf"):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Configure les styles personnalisés"""
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2980b9'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#2980b9'),
            borderPadding=5,
            backColor=colors.HexColor('#ecf0f1')
        ))
        
        # Corps de texte
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
    def add_cover_page(self):
        """Ajoute la page de couverture"""
        self.story.append(Spacer(1, 2*inch))
        
        # Titre principal
        title = Paragraph(
            "<b>SYSTÈME DE GESTION<br/>D'EMPLOI DU TEMPS UNIVERSITAIRE</b>",
            self.styles['CustomTitle']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Sous-titre
        subtitle = Paragraph(
            "Rapport Technique Détaillé",
            self.styles['CustomSubtitle']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1.5*inch))
        
        # Informations du projet
        info_data = [
            ['<b>Projet:</b>', 'Gestion Automatisée d\'Emploi du Temps'],
            ['<b>Version:</b>', '2.0'],
            ['<b>Date:</b>', datetime.now().strftime('%d/%m/%Y')],
            ['<b>Statut:</b>', '✅ Opérationnel'],
            ['<b>Technologies:</b>', 'Python, Tkinter, JSON']
        ]
        
        info_table = Table(info_data, colWidths=[4*cm, 10*cm])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        self.story.append(info_table)
        self.story.append(PageBreak())
        
    def add_table_of_contents(self):
        """Ajoute la table des matières"""
        self.story.append(Paragraph("<b>TABLE DES MATIÈRES</b>", self.styles['CustomTitle']))
        self.story.append(Spacer(1, 0.3*inch))
        
        toc_items = [
            "1. Introduction",
            "2. Architecture du Système",
            "3. Données et Structures",
            "4. Interfaces Utilisateur",
            "5. Logique Métier",
            "6. Fonctionnalités Principales",
            "7. Contraintes et Algorithmes",
            "8. Statistiques du Projet",
            "9. Conclusion"
        ]
        
        for item in toc_items:
            p = Paragraph(f"• {item}", self.styles['CustomBody'])
            self.story.append(p)
            self.story.append(Spacer(1, 0.1*inch))
            
        self.story.append(PageBreak())
        
    def add_introduction(self):
        """Ajoute la section introduction"""
        self.story.append(Paragraph("1. INTRODUCTION", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        intro_text = """
        Ce projet représente un système complet de gestion d'emploi du temps universitaire, 
        conçu pour automatiser et optimiser la planification des cours, travaux dirigés (TD) 
        et travaux pratiques (TP) dans un environnement académique complexe.
        <br/><br/>
        Le système gère l'allocation intelligente de ressources (salles, enseignants, groupes) 
        tout en respectant de multiples contraintes temporelles et matérielles. Il offre des 
        interfaces distinctes pour trois types d'utilisateurs : administrateurs, enseignants 
        et étudiants.
        """
        
        self.story.append(Paragraph(intro_text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Objectifs
        self.story.append(Paragraph("<b>Objectifs Principaux:</b>", self.styles['CustomSubtitle']))
        objectives = [
            "Automatiser la génération d'emplois du temps",
            "Gérer les réservations de salles en temps réel",
            "Optimiser l'utilisation des ressources disponibles",
            "Détecter et résoudre les conflits d'horaires",
            "Fournir des statistiques et rapports détaillés",
            "Offrir une interface intuitive pour tous les utilisateurs"
        ]
        
        for obj in objectives:
            p = Paragraph(f"• {obj}", self.styles['CustomBody'])
            self.story.append(p)
            
        self.story.append(PageBreak())
        
    def add_architecture(self):
        """Ajoute la section architecture"""
        self.story.append(Paragraph("2. ARCHITECTURE DU SYSTÈME", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        arch_text = """
        Le système adopte une architecture modulaire en couches, séparant clairement 
        les responsabilités entre présentation, logique métier et données.
        """
        self.story.append(Paragraph(arch_text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Structure des dossiers
        self.story.append(Paragraph("<b>Structure des Dossiers:</b>", self.styles['CustomSubtitle']))
        
        structure_data = [
            ['<b>Dossier</b>', '<b>Description</b>'],
            ['interfaces/', 'Interfaces graphiques (Admin, Enseignant, Étudiant)'],
            ['logic/', 'Logique métier et algorithmes'],
            ['DONNÉES PRINCIPALES/', 'Fichiers JSON de configuration'],
            ['GESTION EDT/', 'Données générées (EDT, réservations)'],
            ['DOCUMENTATION/', 'Documentation technique'],
            ['backend/', 'Services backend (optionnel)'],
            ['frontend/', 'Interface web (Vite.js)']
        ]
        
        structure_table = Table(structure_data, colWidths=[5*cm, 11*cm])
        structure_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980b9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        self.story.append(structure_table)
        self.story.append(PageBreak())
        
    def add_data_structures(self):
        """Ajoute la section structures de données"""
        self.story.append(Paragraph("3. DONNÉES ET STRUCTURES", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Charger les statistiques
        try:
            salles = self.load_json("DONNÉES PRINCIPALES/salles.json")
            enseignants = self.load_json("DONNÉES PRINCIPALES/enseignants_final.json")
            if isinstance(enseignants, dict):
                enseignants = enseignants.get("enseignants", [])
            modules = self.load_json("DONNÉES PRINCIPALES/modules (1).json")
            groupes = self.load_json("DONNÉES PRINCIPALES/groupes.json")
            filieres = self.load_json("DONNÉES PRINCIPALES/filieres (1).json")
            
            # Calculer total étudiants
            total_etudiants = 0
            if isinstance(filieres, dict) and "statistiques" in filieres:
                total_etudiants = filieres["statistiques"].get("total_etudiants", 0)
            
            stats_data = [
                ['<b>Ressource</b>', '<b>Quantité</b>', '<b>Description</b>'],
                ['Salles', str(len(salles)), '50 salles (Amphi, TP, TD, Cours)'],
                ['Enseignants', str(len(enseignants)), 'Corps enseignant qualifié'],
                ['Modules', str(len(modules)), '6 modules par filière-année'],
                ['Groupes', str(len(groupes)), 'Groupes d\'étudiants organisés'],
                ['Filières', '31', 'DEUST, Licence, Master, Ingénieur'],
                ['Étudiants', str(total_etudiants), 'Total d\'étudiants inscrits']
            ]
            
            stats_table = Table(stats_data, colWidths=[4*cm, 3*cm, 9*cm])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
            ]))
            
            self.story.append(stats_table)
            
        except Exception as e:
            self.story.append(Paragraph(f"Erreur de chargement des données: {str(e)}", 
                                       self.styles['CustomBody']))
        
        self.story.append(Spacer(1, 0.3*inch))
        
        # Types de salles
        self.story.append(Paragraph("<b>Répartition des Salles:</b>", self.styles['CustomSubtitle']))
        salles_text = """
        • <b>3 Amphithéâtres</b> (400 places) - Cours magistraux DEUST<br/>
        • <b>27 Salles TP</b> (30 places) - Travaux pratiques équipés<br/>
        • <b>10 Salles Cours</b> (25 places) - Petits groupes<br/>
        • <b>6 Salles TD</b> (50 places) - Travaux dirigés<br/>
        • <b>4 Salles Cours</b> (90 places) - Grands groupes
        """
        self.story.append(Paragraph(salles_text, self.styles['CustomBody']))
        
        self.story.append(PageBreak())
        
    def add_interfaces(self):
        """Ajoute la section interfaces"""
        self.story.append(Paragraph("4. INTERFACES UTILISATEUR", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        interfaces_text = """
        Le système propose trois interfaces distinctes, chacune adaptée aux besoins 
        spécifiques de son type d'utilisateur.
        """
        self.story.append(Paragraph(interfaces_text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Interface Admin
        self.story.append(Paragraph("<b>4.1 Interface Administrateur</b>", self.styles['CustomSubtitle']))
        admin_features = [
            "<b>Tableau de Bord:</b> Vue d'ensemble des statistiques globales",
            "<b>Génération EDT:</b> Lancement de l'algorithme de placement automatique",
            "<b>Réservations:</b> Validation/rejet des demandes de réservation",
            "<b>Indisponibilités:</b> Gestion des absences enseignants",
            "<b>Occupation:</b> Visualisation en temps réel de l'occupation des salles",
            "<b>Statistiques:</b> Graphiques et analyses avancées",
            "<b>Exports:</b> Export PDF, Excel, CSV des emplois du temps",
            "<b>Disponibilités:</b> Blocage de créneaux pour maintenance",
            "<b>Données:</b> Consultation des salles, enseignants, modules"
        ]
        
        for feature in admin_features:
            self.story.append(Paragraph(f"• {feature}", self.styles['CustomBody']))
            
        self.story.append(Spacer(1, 0.2*inch))
        
        # Interface Enseignant
        self.story.append(Paragraph("<b>4.2 Interface Enseignant</b>", self.styles['CustomSubtitle']))
        teacher_features = [
            "<b>Mon Emploi du Temps:</b> Visualisation personnalisée des cours",
            "<b>Réservations:</b> Demande de réservation de salles",
            "<b>Indisponibilités:</b> Déclaration d'absences planifiées",
            "<b>Statistiques:</b> Charge de travail et répartition horaire",
            "<b>Export:</b> Téléchargement de l'emploi du temps personnel"
        ]
        
        for feature in teacher_features:
            self.story.append(Paragraph(f"• {feature}", self.styles['CustomBody']))
            
        self.story.append(Spacer(1, 0.2*inch))
        
        # Interface Étudiant
        self.story.append(Paragraph("<b>4.3 Interface Étudiant</b>", self.styles['CustomSubtitle']))
        student_features = [
            "<b>Mon Emploi du Temps:</b> Consultation par filière et groupe",
            "<b>Filtrage:</b> Affichage par jour, semaine ou module",
            "<b>Informations:</b> Détails des cours (salle, enseignant, horaire)",
            "<b>Export:</b> Sauvegarde en PDF ou image"
        ]
        
        for feature in student_features:
            self.story.append(Paragraph(f"• {feature}", self.styles['CustomBody']))
            
        self.story.append(PageBreak())
        
    def add_business_logic(self):
        """Ajoute la section logique métier"""
        self.story.append(Paragraph("5. LOGIQUE MÉTIER", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Modules principaux
        modules_data = [
            ['<b>Module</b>', '<b>Fichier</b>', '<b>Responsabilité</b>'],
            ['Générateur EDT', 'edt_generator.py', 'Algorithme de placement des séances'],
            ['Base de données', 'database.py', 'Gestion des fichiers JSON'],
            ['Modèles', 'models.py', 'Classes POO (Salle, Enseignant, etc.)'],
            ['Réservations', 'reservation_manager.py', 'Gestion des réservations'],
            ['Générateur séances', 'seance_generator.py', 'Création des séances'],
            ['Optimisation', 'optimization.py', 'Équilibrage de charge'],
            ['Statistiques', 'stats_manager.py', 'Calculs statistiques'],
            ['Export', 'exporter.py', 'Export CSV, Excel, PDF'],
            ['Conflits', 'conflict_manager.py', 'Détection de conflits']
        ]
        
        modules_table = Table(modules_data, colWidths=[4*cm, 5*cm, 7*cm])
        modules_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        self.story.append(modules_table)
        self.story.append(PageBreak())
        
    def add_features(self):
        """Ajoute la section fonctionnalités"""
        self.story.append(Paragraph("6. FONCTIONNALITÉS PRINCIPALES", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        features = [
            ("<b>Génération Automatique d'EDT</b>", 
             "Algorithme intelligent qui place automatiquement toutes les séances en respectant "
             "les contraintes de disponibilité des enseignants, capacité des salles, et évite "
             "les conflits d'horaires."),
            
            ("<b>Gestion des Réservations</b>", 
             "Les enseignants peuvent demander des réservations de salles. L'administrateur "
             "valide ou rejette après vérification de disponibilité."),
            
            ("<b>Déclaration d'Indisponibilités</b>", 
             "Les enseignants déclarent leurs absences planifiées. Le système bloque "
             "automatiquement les créneaux concernés."),
            
            ("<b>Occupation en Temps Réel</b>", 
             "Visualisation instantanée de l'état de toutes les salles (libre, occupée, réservée) "
             "pour un jour et horaire donnés."),
            
            ("<b>Statistiques Avancées</b>", 
             "Graphiques de répartition par jour, taux d'occupation des salles, charge de travail "
             "des enseignants, plages horaires les plus demandées."),
            
            ("<b>Exports Multiformats</b>", 
             "Export des emplois du temps en PDF, Excel, CSV, ou image PNG avec filtrage "
             "par filière ou enseignant."),
            
            ("<b>Détection de Conflits</b>", 
             "Vérification automatique des conflits : salle occupée, enseignant indisponible, "
             "groupe en double, créneaux bloqués."),
            
            ("<b>Optimisation de Charge</b>", 
             "Équilibrage intelligent de la charge de travail sur la semaine pour éviter "
             "les journées surchargées.")
        ]
        
        for title, desc in features:
            self.story.append(Paragraph(title, self.styles['CustomSubtitle']))
            self.story.append(Paragraph(desc, self.styles['CustomBody']))
            self.story.append(Spacer(1, 0.15*inch))
            
        self.story.append(PageBreak())
        
    def add_constraints(self):
        """Ajoute la section contraintes"""
        self.story.append(Paragraph("7. CONTRAINTES ET ALGORITHMES", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Créneaux horaires
        self.story.append(Paragraph("<b>7.1 Créneaux Horaires</b>", self.styles['CustomSubtitle']))
        
        creneaux_data = [
            ['<b>Jour</b>', '<b>Créneaux</b>', '<b>Total</b>'],
            ['Lundi - Jeudi', '09:00-10:30, 10:45-12:15, 12:30-14:00, 14:15-15:45, 16:00-17:30', '5 × 4 = 20'],
            ['Vendredi', '09:00-10:30, 10:45-12:15, 14:15-15:45, 16:00-17:30', '4'],
            ['Samedi', '09:00-10:30, 10:45-12:15', '2'],
            ['<b>Total Semaine</b>', '', '<b>26 créneaux</b>']
        ]
        
        creneaux_table = Table(creneaux_data, colWidths=[3*cm, 10*cm, 3*cm])
        creneaux_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#ecf0f1')]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d7bde2'))
        ]))
        
        self.story.append(creneaux_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Contraintes dures
        self.story.append(Paragraph("<b>7.2 Contraintes Dures (Obligatoires)</b>", self.styles['CustomSubtitle']))
        hard_constraints = [
            "Un enseignant ne peut pas être à deux endroits en même temps",
            "Une salle ne peut accueillir qu'un seul cours à la fois",
            "Un groupe d'étudiants ne peut avoir qu'un cours à la fois",
            "La capacité de la salle doit être suffisante pour le groupe",
            "Respect des créneaux bloqués (indisponibilités, maintenance)",
            "Type de salle adapté au type de séance (TP nécessite salle TP)"
        ]
        
        for constraint in hard_constraints:
            self.story.append(Paragraph(f"• {constraint}", self.styles['CustomBody']))
            
        self.story.append(Spacer(1, 0.2*inch))
        
        # Contraintes douces
        self.story.append(Paragraph("<b>7.3 Contraintes Douces (Optimisations)</b>", self.styles['CustomSubtitle']))
        soft_constraints = [
            "Équilibrage de la charge sur la semaine (éviter journées surchargées)",
            "Minimisation des salles sous-utilisées",
            "Regroupement des cours d'une même filière",
            "Préférence pour les salles du même bâtiment",
            "Éviter les créneaux tardifs quand possible"
        ]
        
        for constraint in soft_constraints:
            self.story.append(Paragraph(f"• {constraint}", self.styles['CustomBody']))
            
        self.story.append(Spacer(1, 0.3*inch))
        
        # Algorithme
        self.story.append(Paragraph("<b>7.4 Algorithme de Placement</b>", self.styles['CustomSubtitle']))
        algo_text = """
        L'algorithme utilise une approche gloutonne avec backtracking:<br/>
        <br/>
        1. <b>Tri par priorité:</b> Examens > Cours > TD > TP<br/>
        2. <b>Pour chaque séance:</b><br/>
        &nbsp;&nbsp;&nbsp;a. Trier les jours par charge actuelle (équilibrage)<br/>
        &nbsp;&nbsp;&nbsp;b. Pour chaque jour, chercher un créneau libre<br/>
        &nbsp;&nbsp;&nbsp;c. Vérifier disponibilité enseignant et groupe<br/>
        &nbsp;&nbsp;&nbsp;d. Trouver salle adaptée (type, capacité, équipements)<br/>
        &nbsp;&nbsp;&nbsp;e. Détecter les conflits<br/>
        &nbsp;&nbsp;&nbsp;f. Si OK, placer la séance, sinon essayer jour suivant<br/>
        3. <b>Si échec:</b> Proposer solution alternative ou signaler erreur<br/>
        4. <b>Sauvegarder:</b> EDT généré + rapport d'erreurs
        """
        self.story.append(Paragraph(algo_text, self.styles['CustomBody']))
        
        self.story.append(PageBreak())
        
    def add_statistics(self):
        """Ajoute la section statistiques"""
        self.story.append(Paragraph("8. STATISTIQUES DU PROJET", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Compter les lignes de code
        code_stats = self.count_code_lines()
        
        stats_data = [
            ['<b>Métrique</b>', '<b>Valeur</b>'],
            ['Lignes de code Python', f"~{code_stats['total']} lignes"],
            ['Fichiers Python', f"{code_stats['files']} fichiers"],
            ['Modules logiques', '10 modules'],
            ['Interfaces graphiques', '3 interfaces'],
            ['Fichiers JSON de données', '7 fichiers'],
            ['Classes POO', '~15 classes'],
            ['Fonctions principales', '~80 fonctions']
        ]
        
        stats_table = Table(stats_data, colWidths=[8*cm, 8*cm])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        self.story.append(stats_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Technologies utilisées
        self.story.append(Paragraph("<b>Technologies et Bibliothèques:</b>", self.styles['CustomSubtitle']))
        tech_text = """
        • <b>Python 3.x:</b> Langage principal<br/>
        • <b>Tkinter:</b> Interface graphique desktop<br/>
        • <b>JSON:</b> Stockage de données<br/>
        • <b>Matplotlib:</b> Génération de graphiques statistiques<br/>
        • <b>ReportLab:</b> Génération de rapports PDF<br/>
        • <b>OpenPyXL:</b> Export Excel<br/>
        • <b>Vite.js:</b> Interface web moderne (frontend)<br/>
        • <b>Git:</b> Gestion de versions
        """
        self.story.append(Paragraph(tech_text, self.styles['CustomBody']))
        
        self.story.append(PageBreak())
        
    def add_conclusion(self):
        """Ajoute la conclusion"""
        self.story.append(Paragraph("9. CONCLUSION", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        conclusion_text = """
        Ce projet représente une solution complète et robuste pour la gestion automatisée 
        d'emplois du temps universitaires. Le système démontre une architecture bien pensée, 
        séparant clairement les responsabilités entre interfaces, logique métier et données.
        <br/><br/>
        <b>Points Forts:</b><br/>
        • Architecture modulaire et maintenable<br/>
        • Algorithme intelligent de placement avec gestion des contraintes<br/>
        • Interfaces utilisateur intuitives et adaptées à chaque rôle<br/>
        • Gestion complète du cycle de vie (génération, réservation, modification)<br/>
        • Système de détection et résolution de conflits<br/>
        • Exports multiformats et statistiques avancées<br/>
        • Code bien documenté avec docstrings et commentaires<br/>
        <br/>
        <b>Fonctionnalités Clés Implémentées:</b><br/>
        • Génération automatique d'emplois du temps<br/>
        • Gestion des réservations avec validation<br/>
        • Déclaration d'indisponibilités enseignants<br/>
        • Visualisation en temps réel de l'occupation<br/>
        • Statistiques et analyses graphiques<br/>
        • Exports PDF, Excel, CSV, Image<br/>
        • Optimisation de la charge de travail<br/>
        <br/>
        <b>Perspectives d'Évolution:</b><br/>
        • Intégration d'une base de données SQL pour de meilleures performances<br/>
        • Développement d'une API REST pour l'interface web<br/>
        • Ajout de notifications par email<br/>
        • Système de suggestions intelligentes basé sur l'historique<br/>
        • Application mobile pour consultation en déplacement<br/>
        • Intégration avec systèmes existants (Moodle, etc.)<br/>
        <br/>
        Le système est actuellement <b>opérationnel</b> et prêt pour un déploiement en 
        environnement de production après tests utilisateurs.
        """
        
        self.story.append(Paragraph(conclusion_text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.5*inch))
        
        # Footer final
        footer_text = """
        <br/><br/>
        <i>Rapport généré automatiquement le {date}</i><br/>
        <i>Système de Gestion d'Emploi du Temps Universitaire - Version 2.0</i>
        """.format(date=datetime.now().strftime('%d/%m/%Y à %H:%M'))
        
        self.story.append(Paragraph(footer_text, self.styles['CustomBody']))
        
    def load_json(self, path):
        """Charge un fichier JSON"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
            
    def count_code_lines(self):
        """Compte les lignes de code Python"""
        total_lines = 0
        file_count = 0
        
        for root, dirs, files in os.walk('.'):
            # Ignorer certains dossiers
            if any(skip in root for skip in ['__pycache__', 'node_modules', '.git', '.vite']):
                continue
                
            for file in files:
                if file.endswith('.py'):
                    file_count += 1
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            total_lines += len(f.readlines())
                    except:
                        pass
                        
        return {'total': total_lines, 'files': file_count}
        
    def generate(self):
        """Génère le rapport PDF complet"""
        print("🔄 Génération du rapport PDF en cours...")
        
        self.add_cover_page()
        self.add_table_of_contents()
        self.add_introduction()
        self.add_architecture()
        self.add_data_structures()
        self.add_interfaces()
        self.add_business_logic()
        self.add_features()
        self.add_constraints()
        self.add_statistics()
        self.add_conclusion()
        
        # Construire le PDF
        self.doc.build(self.story)
        
        print(f"✅ Rapport PDF généré avec succès: {self.output_path}")
        return self.output_path

if __name__ == "__main__":
    generator = PDFReportGenerator("Rapport_Projet_EDT.pdf")
    output = generator.generate()
    print(f"\n📄 Le rapport est disponible: {output}")

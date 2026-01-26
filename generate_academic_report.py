"""
Générateur de Rapport Académique PDF
Projet: Système de Gestion d'Emploi du Temps Universitaire
Auteur: Équipe Projet FSTT
Date: 2026
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, 
                                TableStyle, PageBreak, Image, KeepTogether,
                                HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime

class AcademicReportGenerator:
    def __init__(self, output_path="Rapport_Projet_Gestion_EDT.pdf"):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2.5*cm,
            leftMargin=2.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Configure les styles personnalisés pour un rapport académique"""
        
        # Titre principal de la page de garde
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=20,
            spaceBefore=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=28
        ))
        
        # Sous-titre page de garde
        self.styles.add(ParagraphStyle(
            name='CoverSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#283593'),
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=18
        ))
        
        # Informations académiques
        self.styles.add(ParagraphStyle(
            name='AcademicInfo',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#37474f'),
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=16
        ))
        
        # Titre de section
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#0d47a1'),
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=8,
            leftIndent=0,
            leading=20
        ))
        
        # Sous-section
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#1565c0'),
            spaceAfter=10,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            leading=16
        ))
        
        # Corps de texte justifié
        self.styles.add(ParagraphStyle(
            name='BodyJustified',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=16,
            textColor=colors.HexColor('#212121')
        ))
        
        # Liste à puces
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=6,
            leftIndent=20,
            leading=15,
            textColor=colors.HexColor('#424242')
        ))
        
    def add_cover_page(self):
        """Crée une page de garde académique professionnelle"""
        
        # Logo/En-tête université
        self.story.append(Spacer(1, 0.5*cm))
        
        # Nom de l'université
        university = Paragraph(
            "<b>FACULTÉ DES SCIENCES ET TECHNIQUES DE TANGER</b>",
            self.styles['CoverTitle']
        )
        self.story.append(university)
        
        self.story.append(Spacer(1, 0.3*cm))
        
        # Département/Filière
        dept = Paragraph(
            "Licence Professionnelle - Analytique de Données",
            self.styles['CoverSubtitle']
        )
        self.story.append(dept)
        
        # Ligne de séparation
        self.story.append(Spacer(1, 1*cm))
        self.story.append(HRFlowable(
            width="80%",
            thickness=2,
            color=colors.HexColor('#1565c0'),
            spaceAfter=1*cm,
            spaceBefore=0.5*cm,
            hAlign='CENTER'
        ))
        
        # Titre du projet
        self.story.append(Spacer(1, 1.5*cm))
        title = Paragraph(
            "<b>SYSTÈME DE GESTION<br/>D'EMPLOI DU TEMPS UNIVERSITAIRE</b>",
            ParagraphStyle(
                name='MainTitle',
                fontSize=20,
                textColor=colors.HexColor('#0d47a1'),
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                leading=26,
                spaceAfter=10
            )
        )
        self.story.append(title)
        
        # Sous-titre projet
        subtitle = Paragraph(
            "Projet de Développement d'Application",
            self.styles['CoverSubtitle']
        )
        self.story.append(subtitle)
        
        # Ligne de séparation
        self.story.append(Spacer(1, 1*cm))
        self.story.append(HRFlowable(
            width="80%",
            thickness=2,
            color=colors.HexColor('#1565c0'),
            spaceAfter=1*cm,
            spaceBefore=0.5*cm,
            hAlign='CENTER'
        ))
        
        self.story.append(Spacer(1, 1.5*cm))
        
        # Réalisé par (étudiants)
        realise = Paragraph(
            "<b>Réalisé par :</b>",
            ParagraphStyle(
                name='RealiseTitle',
                fontSize=12,
                textColor=colors.HexColor('#37474f'),
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                spaceAfter=10
            )
        )
        self.story.append(realise)
        
        # Noms des étudiants
        students = [
            "Khadija DRIDRI",
            "Amal EL ATLLATI",
            "Hanan BEN-YAICH",
            "Ouissal SEKKARI"
        ]
        
        for student in students:
            p = Paragraph(student, self.styles['AcademicInfo'])
            self.story.append(p)
        
        self.story.append(Spacer(1, 1*cm))
        
        # Encadré par
        encadre = Paragraph(
            "<b>Encadré par :</b>",
            ParagraphStyle(
                name='EncadreTitle',
                fontSize=12,
                textColor=colors.HexColor('#37474f'),
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                spaceAfter=10
            )
        )
        self.story.append(encadre)
        
        prof = Paragraph(
            "Pr. Sanae KHALI ISSA",
            self.styles['AcademicInfo']
        )
        self.story.append(prof)
        
        # Année universitaire
        self.story.append(Spacer(1, 1.5*cm))
        annee = Paragraph(
            "<b>Année Universitaire : 2025/2026</b>",
            ParagraphStyle(
                name='Year',
                fontSize=13,
                textColor=colors.HexColor('#1565c0'),
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
        )
        self.story.append(annee)
        
        self.story.append(PageBreak())
        
    def add_introduction(self):
        """Ajoute l'introduction générale"""
        
        # Titre
        title = Paragraph("INTRODUCTION GÉNÉRALE", self.styles['SectionTitle'])
        self.story.append(title)
        
        # Ligne sous le titre
        self.story.append(HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor('#1565c0'),
            spaceAfter=15
        ))
        
        # Contexte
        intro_text = """
        Dans le contexte actuel de l'enseignement supérieur, la gestion efficace des emplois du temps 
        constitue un défi majeur pour les établissements universitaires. La complexité croissante des 
        programmes académiques, la diversité des filières, et la multiplication des contraintes 
        (disponibilité des enseignants, capacité des salles, équipements spécifiques) nécessitent 
        des solutions informatiques robustes et intelligentes.
        """
        self.story.append(Paragraph(intro_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Problématique
        prob_title = Paragraph("<b>Problématique</b>", self.styles['SubSection'])
        self.story.append(prob_title)
        
        prob_text = """
        La planification manuelle des emplois du temps présente plusieurs limitations : risques d'erreurs 
        humaines, conflits d'horaires non détectés, sous-utilisation des ressources, temps de traitement 
        important, et difficulté de mise à jour. Ces problèmes impactent directement la qualité de 
        l'enseignement et l'expérience des étudiants et enseignants.
        """
        self.story.append(Paragraph(prob_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Objectifs
        obj_title = Paragraph("<b>Objectifs du Projet</b>", self.styles['SubSection'])
        self.story.append(obj_title)
        
        obj_intro = """
        Ce projet vise à développer un système complet de gestion automatisée d'emplois du temps 
        universitaires. Les objectifs principaux sont :
        """
        self.story.append(Paragraph(obj_intro, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        objectives = [
            "Automatiser la génération d'emplois du temps en respectant l'ensemble des contraintes",
            "Optimiser l'utilisation des ressources disponibles (salles, enseignants)",
            "Détecter et prévenir les conflits d'horaires en temps réel",
            "Faciliter la gestion des réservations de salles et des indisponibilités",
            "Fournir des interfaces adaptées à chaque type d'utilisateur",
            "Générer des statistiques et rapports pour l'aide à la décision"
        ]
        
        for obj in objectives:
            bullet = Paragraph(f"• {obj}", self.styles['BulletPoint'])
            self.story.append(bullet)
        
        self.story.append(Spacer(1, 0.3*cm))
        
        # Solution proposée
        sol_title = Paragraph("<b>Solution Proposée</b>", self.styles['SubSection'])
        self.story.append(sol_title)
        
        sol_text = """
        Notre solution consiste en une application desktop développée en Python avec l'interface 
        graphique Tkinter. Le système utilise un algorithme intelligent de placement qui prend en 
        compte les contraintes dures (obligatoires) et les contraintes douces (optimisations). 
        L'architecture modulaire permet une maintenance facile et des évolutions futures.
        """
        self.story.append(Paragraph(sol_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Structure du rapport
        struct_title = Paragraph("<b>Structure du Rapport</b>", self.styles['SubSection'])
        self.story.append(struct_title)
        
        struct_text = """
        Ce rapport présente en détail les trois interfaces principales du système : l'interface 
        administrateur pour la gestion globale, l'interface enseignant pour la consultation et les 
        demandes, et l'interface étudiant pour la consultation des emplois du temps. Nous conclurons 
        par une synthèse des résultats obtenus et les perspectives d'amélioration.
        """
        self.story.append(Paragraph(struct_text, self.styles['BodyJustified']))
        
        self.story.append(PageBreak())
        
    def add_admin_interface(self):
        """Détaille l'interface administrateur"""
        
        title = Paragraph("1. INTERFACE ADMINISTRATEUR", self.styles['SectionTitle'])
        self.story.append(title)
        self.story.append(HRFlowable(width="100%", thickness=1, 
                                     color=colors.HexColor('#1565c0'), spaceAfter=15))
        
        intro = """
        L'interface administrateur constitue le cœur du système de gestion. Elle offre un contrôle 
        complet sur tous les aspects de la planification et de la gestion des emplois du temps.
        """
        self.story.append(Paragraph(intro, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Fonctionnalités principales
        features_title = Paragraph("<b>1.1 Fonctionnalités Principales</b>", self.styles['SubSection'])
        self.story.append(features_title)
        
        # Tableau de bord
        self.story.append(Paragraph("<b>Tableau de Bord</b>", self.styles['BulletPoint']))
        dashboard_text = """
        Vue d'ensemble des statistiques globales du système : nombre d'enseignants, de modules, 
        de salles et d'étudiants. Cette interface permet une visualisation rapide de l'état général 
        du système.
        """
        self.story.append(Paragraph(dashboard_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Génération EDT
        self.story.append(Paragraph("<b>Génération Automatique d'Emploi du Temps</b>", self.styles['BulletPoint']))
        gen_text = """
        Module central permettant de lancer l'algorithme de placement automatique. Le processus 
        se déroule en deux étapes : d'abord la génération des séances à partir des modules définis, 
        puis le placement intelligent de ces séances dans les créneaux disponibles. L'algorithme 
        respecte toutes les contraintes (disponibilité enseignants, capacité salles, conflits horaires) 
        et optimise la répartition sur la semaine.
        """
        self.story.append(Paragraph(gen_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Gestion des réservations
        self.story.append(Paragraph("<b>Gestion des Réservations</b>", self.styles['BulletPoint']))
        resa_text = """
        Interface de validation des demandes de réservation de salles soumises par les enseignants. 
        L'administrateur peut consulter toutes les demandes avec leurs détails (enseignant, salle, 
        jour, horaire, motif) et les accepter ou rejeter. Le système vérifie automatiquement la 
        disponibilité de la salle avant validation pour éviter les conflits.
        """
        self.story.append(Paragraph(resa_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Indisponibilités
        self.story.append(Paragraph("<b>Gestion des Indisponibilités</b>", self.styles['BulletPoint']))
        indispo_text = """
        Module permettant de traiter les demandes d'indisponibilité des enseignants (absences, 
        congés, événements). L'administrateur peut accepter ou refuser ces demandes. Une fois 
        acceptées, les créneaux concernés sont automatiquement bloqués dans le système.
        """
        self.story.append(Paragraph(indispo_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Occupation
        self.story.append(Paragraph("<b>Visualisation de l'Occupation</b>", self.styles['BulletPoint']))
        occ_text = """
        Deux modes de visualisation sont disponibles : l'occupation globale qui affiche le taux 
        d'utilisation de chaque salle sur toute la période, et l'occupation en temps réel qui 
        montre l'état instantané de toutes les salles (libre, occupée, réservée) pour un jour 
        et horaire spécifiques. Cette fonctionnalité utilise un code couleur intuitif : vert pour 
        libre, rouge pour occupée, jaune pour réservée.
        """
        self.story.append(Paragraph(occ_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Statistiques
        self.story.append(Paragraph("<b>Statistiques Avancées</b>", self.styles['BulletPoint']))
        stats_text = """
        Module d'analyse proposant des graphiques interactifs : répartition des cours par jour de 
        la semaine, taux d'occupation des salles les plus utilisées, et identification des plages 
        horaires les plus demandées. Ces statistiques aident à la prise de décision et à 
        l'optimisation des ressources.
        """
        self.story.append(Paragraph(stats_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Exports
        self.story.append(Paragraph("<b>Consultation et Export</b>", self.styles['BulletPoint']))
        export_text = """
        Interface permettant de consulter et exporter les emplois du temps selon différents critères 
        (global, par filière, par enseignant). Les formats d'export disponibles sont : PDF pour 
        l'impression, Excel pour l'analyse, et Image PNG pour l'affichage. Le système génère 
        automatiquement des documents formatés et professionnels.
        """
        self.story.append(Paragraph(export_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Disponibilités
        self.story.append(Paragraph("<b>Gestion des Disponibilités</b>", self.styles['BulletPoint']))
        dispo_text = """
        Permet à l'administrateur de bloquer manuellement des créneaux pour des raisons spécifiques 
        (maintenance de salles, événements exceptionnels, examens). Ces blocages sont pris en compte 
        par l'algorithme de génération pour éviter tout conflit.
        """
        self.story.append(Paragraph(dispo_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Données
        self.story.append(Paragraph("<b>Consultation des Données</b>", self.styles['BulletPoint']))
        data_text = """
        Interface de visualisation des données de base du système : liste des salles avec leurs 
        caractéristiques (capacité, type, équipements), liste des enseignants avec leurs informations, 
        et catalogue des modules. Cette interface permet une vérification rapide des données 
        sans modification.
        """
        self.story.append(Paragraph(data_text, self.styles['BodyJustified']))
        
        self.story.append(PageBreak())
        
    def add_teacher_interface(self):
        """Détaille l'interface enseignant"""
        
        title = Paragraph("2. INTERFACE ENSEIGNANT", self.styles['SectionTitle'])
        self.story.append(title)
        self.story.append(HRFlowable(width="100%", thickness=1, 
                                     color=colors.HexColor('#1565c0'), spaceAfter=15))
        
        intro = """
        L'interface enseignant est conçue pour offrir aux professeurs un accès facile à leur emploi 
        du temps personnel et leur permettre de gérer leurs besoins en termes de salles et de disponibilités.
        """
        self.story.append(Paragraph(intro, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Fonctionnalités
        features_title = Paragraph("<b>2.1 Fonctionnalités Disponibles</b>", self.styles['SubSection'])
        self.story.append(features_title)
        
        # Mon emploi du temps
        self.story.append(Paragraph("<b>Consultation de l'Emploi du Temps Personnel</b>", self.styles['BulletPoint']))
        edt_text = """
        L'enseignant sélectionne son nom dans une liste déroulante et le système affiche 
        automatiquement tous ses cours programmés. L'affichage est organisé par jour et par horaire, 
        avec toutes les informations pertinentes : module enseigné, type de séance (Cours, TD, TP), 
        salle assignée, groupe d'étudiants, et horaires précis. L'interface utilise un code couleur 
        pour différencier les types de séances et faciliter la lecture.
        """
        self.story.append(Paragraph(edt_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Réservations
        self.story.append(Paragraph("<b>Demandes de Réservation de Salles</b>", self.styles['BulletPoint']))
        resa_text = """
        Module permettant aux enseignants de soumettre des demandes de réservation pour des besoins 
        spécifiques (examens, séances de rattrapage, réunions). Le formulaire de demande comprend : 
        la sélection de la salle souhaitée, le jour et l'horaire, et un motif détaillé. Le système 
        affiche en temps réel les salles disponibles pour le créneau choisi. L'enseignant peut 
        également consulter l'historique de ses demandes et leur statut (en attente, acceptée, refusée).
        """
        self.story.append(Paragraph(resa_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Indisponibilités
        self.story.append(Paragraph("<b>Déclaration d'Indisponibilités</b>", self.styles['BulletPoint']))
        indispo_text = """
        Interface permettant aux enseignants de déclarer leurs absences planifiées ou indisponibilités. 
        Le formulaire permet de spécifier le jour, l'horaire, le motif (absence, formation, mission, 
        congé) et des détails supplémentaires si nécessaire. Ces déclarations sont envoyées à 
        l'administrateur pour validation. Une fois approuvées, elles sont automatiquement prises en 
        compte lors de la génération ou modification des emplois du temps.
        """
        self.story.append(Paragraph(indispo_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Statistiques
        self.story.append(Paragraph("<b>Statistiques Personnelles</b>", self.styles['BulletPoint']))
        stats_text = """
        Visualisation de la charge de travail personnelle sous forme de graphiques : répartition 
        des heures d'enseignement par jour de la semaine, nombre de séances par type (Cours, TD, TP), 
        et répartition par filière enseignée. Ces statistiques aident l'enseignant à avoir une vue 
        d'ensemble de son emploi du temps et à identifier d'éventuels déséquilibres.
        """
        self.story.append(Paragraph(stats_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Export
        self.story.append(Paragraph("<b>Export de l'Emploi du Temps</b>", self.styles['BulletPoint']))
        export_text = """
        Fonctionnalité permettant à l'enseignant de télécharger son emploi du temps personnel dans 
        différents formats : PDF pour l'impression et l'archivage, Excel pour l'intégration dans 
        d'autres outils, ou Image pour un partage rapide. Le document généré est automatiquement 
        formaté et inclut uniquement les cours de l'enseignant concerné.
        """
        self.story.append(Paragraph(export_text, self.styles['BodyJustified']))
        
        self.story.append(Spacer(1, 0.3*cm))
        
        # Avantages
        adv_title = Paragraph("<b>2.2 Avantages pour l'Enseignant</b>", self.styles['SubSection'])
        self.story.append(adv_title)
        
        advantages = [
            "Accès rapide et autonome à son emploi du temps sans passer par l'administration",
            "Possibilité de réserver des salles de manière simple et transparente",
            "Gestion proactive des absences et indisponibilités",
            "Visualisation claire de la charge de travail hebdomadaire",
            "Export facile pour intégration dans des outils personnels"
        ]
        
        for adv in advantages:
            bullet = Paragraph(f"• {adv}", self.styles['BulletPoint'])
            self.story.append(bullet)
        
        self.story.append(PageBreak())
        
    def add_student_interface(self):
        """Détaille l'interface étudiant"""
        
        title = Paragraph("3. INTERFACE ÉTUDIANT", self.styles['SectionTitle'])
        self.story.append(title)
        self.story.append(HRFlowable(width="100%", thickness=1, 
                                     color=colors.HexColor('#1565c0'), spaceAfter=15))
        
        intro = """
        L'interface étudiant est optimisée pour la consultation rapide et intuitive des emplois du 
        temps. Elle offre une expérience utilisateur simple et efficace, adaptée aux besoins des étudiants.
        """
        self.story.append(Paragraph(intro, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Fonctionnalités
        features_title = Paragraph("<b>3.1 Fonctionnalités de Consultation</b>", self.styles['SubSection'])
        self.story.append(features_title)
        
        # Sélection filière
        self.story.append(Paragraph("<b>Sélection de la Filière et du Groupe</b>", self.styles['BulletPoint']))
        select_text = """
        L'étudiant commence par sélectionner sa filière dans une liste déroulante organisée par niveau 
        (DEUST, Licence, Master, Cycle Ingénieur). Une fois la filière choisie, le système affiche 
        automatiquement les groupes disponibles (groupe de cours, groupes de TD/TP). Cette organisation 
        permet une navigation intuitive et rapide.
        """
        self.story.append(Paragraph(select_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Affichage EDT
        self.story.append(Paragraph("<b>Affichage de l'Emploi du Temps</b>", self.styles['BulletPoint']))
        display_text = """
        L'emploi du temps s'affiche dans un tableau clair et structuré, organisé par jour de la semaine. 
        Pour chaque séance, les informations suivantes sont présentées : le module enseigné, le type 
        de séance (Cours, TD, TP), l'horaire exact (début et fin), la salle où se déroule le cours, 
        et le nom de l'enseignant. Un code couleur différencie visuellement les types de séances pour 
        faciliter la lecture rapide.
        """
        self.story.append(Paragraph(display_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Filtrage
        self.story.append(Paragraph("<b>Options de Filtrage</b>", self.styles['BulletPoint']))
        filter_text = """
        L'interface propose plusieurs options de filtrage pour personnaliser l'affichage : filtrage 
        par jour de la semaine pour voir uniquement les cours d'un jour spécifique, filtrage par type 
        de séance (afficher uniquement les Cours, ou uniquement les TD/TP), et recherche par module 
        pour localiser rapidement un cours particulier. Ces filtres peuvent être combinés pour une 
        recherche encore plus précise.
        """
        self.story.append(Paragraph(filter_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Informations détaillées
        self.story.append(Paragraph("<b>Informations Détaillées</b>", self.styles['BulletPoint']))
        info_text = """
        En cliquant sur une séance, l'étudiant peut accéder à des informations complémentaires : 
        localisation précise de la salle (bâtiment, étage), équipements disponibles dans la salle, 
        et éventuellement des notes ou remarques spécifiques au cours. Cette fonctionnalité aide 
        les étudiants, notamment les nouveaux, à mieux s'orienter dans l'établissement.
        """
        self.story.append(Paragraph(info_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        # Export
        self.story.append(Paragraph("<b>Export et Sauvegarde</b>", self.styles['BulletPoint']))
        export_text = """
        Les étudiants peuvent exporter leur emploi du temps dans plusieurs formats : PDF pour 
        l'impression et la consultation hors ligne, Image PNG pour un partage rapide sur les réseaux 
        sociaux ou par messagerie, et éventuellement format iCal pour l'intégration dans des 
        calendriers électroniques (Google Calendar, Outlook, etc.).
        """
        self.story.append(Paragraph(export_text, self.styles['BodyJustified']))
        
        self.story.append(Spacer(1, 0.3*cm))
        
        # Ergonomie
        ergo_title = Paragraph("<b>3.2 Ergonomie et Expérience Utilisateur</b>", self.styles['SubSection'])
        self.story.append(ergo_title)
        
        ergo_text = """
        L'interface étudiant a été conçue avec un focus particulier sur la simplicité et l'efficacité. 
        Les principes suivants ont guidé sa conception :
        """
        self.story.append(Paragraph(ergo_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        ergo_points = [
            "<b>Simplicité :</b> Nombre minimal de clics pour accéder à l'information recherchée",
            "<b>Clarté visuelle :</b> Utilisation de codes couleur et d'une typographie lisible",
            "<b>Réactivité :</b> Affichage instantané des résultats après sélection",
            "<b>Accessibilité :</b> Interface adaptée à différentes résolutions d'écran",
            "<b>Intuitivité :</b> Navigation logique ne nécessitant pas de formation préalable"
        ]
        
        for point in ergo_points:
            bullet = Paragraph(f"• {point}", self.styles['BulletPoint'])
            self.story.append(bullet)
        
        self.story.append(Spacer(1, 0.3*cm))
        
        # Bénéfices
        ben_title = Paragraph("<b>3.3 Bénéfices pour les Étudiants</b>", self.styles['SubSection'])
        self.story.append(ben_title)
        
        benefits = [
            "Consultation autonome 24h/24 de l'emploi du temps actualisé",
            "Réduction du risque d'oubli ou de confusion grâce aux informations détaillées",
            "Meilleure organisation personnelle grâce aux options d'export",
            "Gain de temps en évitant les déplacements pour consulter les affichages physiques",
            "Accès mobile possible pour consultation en déplacement"
        ]
        
        for benefit in benefits:
            bullet = Paragraph(f"• {benefit}", self.styles['BulletPoint'])
            self.story.append(bullet)
        
        self.story.append(PageBreak())
        
    def add_conclusion(self):
        """Ajoute la conclusion"""
        
        title = Paragraph("CONCLUSION ET PERSPECTIVES", self.styles['SectionTitle'])
        self.story.append(title)
        self.story.append(HRFlowable(width="100%", thickness=1, 
                                     color=colors.HexColor('#1565c0'), spaceAfter=15))
        
        # Synthèse
        synth_title = Paragraph("<b>Synthèse du Projet</b>", self.styles['SubSection'])
        self.story.append(synth_title)
        
        synth_text = """
        Ce projet de système de gestion d'emploi du temps universitaire répond efficacement aux 
        besoins identifiés en matière d'automatisation et d'optimisation de la planification académique. 
        À travers le développement de trois interfaces distinctes et complémentaires, nous avons créé 
        une solution complète qui bénéficie à tous les acteurs de l'établissement : administrateurs, 
        enseignants et étudiants.
        """
        self.story.append(Paragraph(synth_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Réalisations
        real_title = Paragraph("<b>Réalisations Principales</b>", self.styles['SubSection'])
        self.story.append(real_title)
        
        realisations = [
            "<b>Algorithme intelligent :</b> Développement d'un algorithme de placement qui respecte "
            "toutes les contraintes (dures et douces) et optimise l'utilisation des ressources",
            
            "<b>Interfaces utilisateur :</b> Création de trois interfaces ergonomiques adaptées aux "
            "besoins spécifiques de chaque type d'utilisateur",
            
            "<b>Gestion des conflits :</b> Mise en place d'un système robuste de détection et de "
            "prévention des conflits d'horaires",
            
            "<b>Système de réservation :</b> Implémentation d'un workflow complet de demande, "
            "validation et suivi des réservations de salles",
            
            "<b>Exports multiformats :</b> Génération automatique de documents professionnels en "
            "PDF, Excel et Image",
            
            "<b>Statistiques avancées :</b> Outils d'analyse et de visualisation pour l'aide à la "
            "décision et l'optimisation continue"
        ]
        
        for real in realisations:
            bullet = Paragraph(f"• {real}", self.styles['BulletPoint'])
            self.story.append(bullet)
        
        self.story.append(Spacer(1, 0.3*cm))
        
        # Apports
        apport_title = Paragraph("<b>Apports du Projet</b>", self.styles['SubSection'])
        self.story.append(apport_title)
        
        apport_text = """
        Sur le plan technique, ce projet nous a permis de maîtriser le développement d'applications 
        desktop avec Python et Tkinter, la conception d'algorithmes d'optimisation sous contraintes, 
        et la gestion de données structurées avec JSON. Sur le plan méthodologique, nous avons 
        appliqué les principes de la programmation orientée objet, de l'architecture modulaire, et 
        de la conception centrée utilisateur.
        """
        self.story.append(Paragraph(apport_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Perspectives
        persp_title = Paragraph("<b>Perspectives d'Amélioration</b>", self.styles['SubSection'])
        self.story.append(persp_title)
        
        persp_intro = """
        Plusieurs axes d'amélioration et d'évolution peuvent être envisagés pour enrichir le système :
        """
        self.story.append(Paragraph(persp_intro, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.2*cm))
        
        perspectives = [
            "<b>Migration vers une base de données :</b> Remplacer le stockage JSON par une base de "
            "données SQL (PostgreSQL, MySQL) pour améliorer les performances et la scalabilité",
            
            "<b>Application web :</b> Développer une interface web responsive avec React ou Vue.js "
            "pour un accès universel depuis n'importe quel appareil",
            
            "<b>Application mobile :</b> Créer des applications natives iOS et Android pour faciliter "
            "la consultation en mobilité",
            
            "<b>Notifications automatiques :</b> Système d'alertes par email ou SMS pour informer des "
            "changements d'emploi du temps, des réservations validées, etc.",
            
            "<b>Intelligence artificielle :</b> Utiliser le machine learning pour suggérer des "
            "optimisations basées sur l'historique et les préférences",
            
            "<b>Intégration avec d'autres systèmes :</b> Connexion avec les plateformes pédagogiques "
            "(Moodle, Teams) et les systèmes de gestion académique existants",
            
            "<b>Gestion multi-établissements :</b> Adapter le système pour gérer plusieurs campus "
            "ou établissements depuis une plateforme centralisée",
            
            "<b>Module de simulation :</b> Permettre de tester différents scénarios de planification "
            "avant validation définitive"
        ]
        
        for persp in perspectives:
            bullet = Paragraph(f"• {persp}", self.styles['BulletPoint'])
            self.story.append(bullet)
        
        self.story.append(Spacer(1, 0.4*cm))
        
        # Mot de fin
        final_title = Paragraph("<b>Mot de Fin</b>", self.styles['SubSection'])
        self.story.append(final_title)
        
        final_text = """
        Ce projet représente une solution concrète et opérationnelle aux défis de la gestion 
        d'emplois du temps universitaires. Au-delà de l'aspect technique, il démontre l'importance 
        de l'informatisation et de l'automatisation dans l'amélioration de la qualité des services 
        éducatifs. Nous sommes convaincus que ce système, avec les améliorations futures envisagées, 
        pourra contribuer significativement à l'efficacité organisationnelle des établissements 
        d'enseignement supérieur.
        <br/><br/>
        Nous tenons à remercier notre encadrante, Pr. Sanae KHALI ISSA, pour son accompagnement, 
        ses conseils précieux et sa disponibilité tout au long de ce projet. Nous remercions 
        également la Faculté des Sciences et Techniques de Tanger pour les moyens mis à notre 
        disposition.
        """
        self.story.append(Paragraph(final_text, self.styles['BodyJustified']))
        
        self.story.append(Spacer(1, 1*cm))
        
        # Signature
        signature = Paragraph(
            "<i>Les étudiantes du projet<br/>Année Universitaire 2025/2026</i>",
            ParagraphStyle(
                name='Signature',
                fontSize=11,
                alignment=TA_RIGHT,
                textColor=colors.HexColor('#37474f'),
                fontName='Helvetica-Oblique'
            )
        )
        self.story.append(signature)
        
    def generate(self):
        """Génère le rapport PDF complet"""
        print("📄 Génération du rapport académique en cours...")
        print("=" * 60)
        
        self.add_cover_page()
        print("✓ Page de garde créée")
        
        self.add_introduction()
        print("✓ Introduction ajoutée")
        
        self.add_admin_interface()
        print("✓ Interface Administrateur documentée")
        
        self.add_teacher_interface()
        print("✓ Interface Enseignant documentée")
        
        self.add_student_interface()
        print("✓ Interface Étudiant documentée")
        
        self.add_conclusion()
        print("✓ Conclusion rédigée")
        
        # Construire le PDF
        self.doc.build(self.story)
        
        print("=" * 60)
        print(f"✅ Rapport PDF généré avec succès !")
        print(f"📁 Fichier : {self.output_path}")
        print(f"📊 Taille : {os.path.getsize(self.output_path) / 1024:.1f} KB")
        
        return self.output_path

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   GÉNÉRATEUR DE RAPPORT ACADÉMIQUE - PROJET EDT")
    print("=" * 60 + "\n")
    
    generator = AcademicReportGenerator("Rapport_Projet_Gestion_EDT.pdf")
    output = generator.generate()
    
    print(f"\n🎓 Le rapport académique est prêt !")
    print(f"📄 Emplacement : {os.path.abspath(output)}\n")

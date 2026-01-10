"""
Classes POO pour le système de gestion d'emploi du temps universitaire
Auteur: Système de Gestion Universitaire
Date: 2026-01-10
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, time
from enum import Enum


# ============================================================================
# ÉNUMÉRATIONS
# ============================================================================

class TypeSalle(Enum):
    """Types de salles disponibles"""
    AMPHI = "Amphi"
    COURS = "Cours"
    TD = "TD"
    TP = "TP"


class TypeSeance(Enum):
    """Types de séances"""
    COURS = "Cours"
    TD = "TD"
    TP = "TP"


class JourSemaine(Enum):
    """Jours de la semaine"""
    LUNDI = "Lundi"
    MARDI = "Mardi"
    MERCREDI = "Mercredi"
    JEUDI = "Jeudi"
    VENDREDI = "Vendredi"
    SAMEDI = "Samedi"


class StatutReservation(Enum):
    """Statuts possibles d'une réservation"""
    CONFIRMEE = "confirmée"
    EN_ATTENTE = "en_attente"
    ANNULEE = "annulée"


# ============================================================================
# CLASSE SALLE
# ============================================================================

class Salle:
    """
    Représente une salle de cours/TP/TD.
    
    Attributes:
        id (int): Identifiant unique de la salle
        nom (str): Nom de la salle
        capacite (int): Capacité maximale
        type (TypeSalle): Type de salle
        equipements (List[str]): Liste des équipements disponibles
        batiment (str): Bâtiment où se trouve la salle
        etage (int): Étage de la salle
        departement_id (Optional[int]): ID du département (None si partagée)
    """
    
    def __init__(self, id: int, nom: str, capacite: int, type: str,
                 equipements: List[str], batiment: str, etage: int,
                 departement_id: Optional[int] = None):
        self.id = id
        self.nom = nom
        self.capacite = capacite
        self.type = TypeSalle(type) if isinstance(type, str) else type
        self.equipements = equipements
        self.batiment = batiment
        self.etage = etage
        self.departement_id = departement_id
    
    def est_disponible_pour(self, nombre_etudiants: int) -> bool:
        """Vérifie si la salle peut accueillir un nombre d'étudiants."""
        return self.capacite >= nombre_etudiants
    
    def a_equipement(self, equipement: str) -> bool:
        """Vérifie si la salle possède un équipement."""
        return equipement.lower() in [e.lower() for e in self.equipements]
    
    def est_partagee(self) -> bool:
        """Vérifie si la salle est partagée entre départements."""
        return self.departement_id is None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'nom': self.nom,
            'capacite': self.capacite,
            'type': self.type.value,
            'equipements': self.equipements,
            'batiment': self.batiment,
            'etage': self.etage,
            'departement_id': self.departement_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Salle':
        """Crée une instance depuis un dictionnaire."""
        return cls(**data)
    
    def __str__(self) -> str:
        shared = " (Partagée)" if self.est_partagee() else f" (Dépt {self.departement_id})"
        return f"Salle {self.nom} - {self.type.value} - {self.capacite} places{shared}"
    
    def __repr__(self) -> str:
        return f"Salle(id={self.id}, nom='{self.nom}', capacite={self.capacite})"


# ============================================================================
# CLASSE ENSEIGNANT
# ============================================================================

class Enseignant:
    """
    Représente un enseignant.
    
    Attributes:
        id (int): Identifiant unique
        nom (str): Nom complet de l'enseignant
        specialite (str): Spécialité de l'enseignant
        departement (str): Département d'appartenance
        email (str): Adresse email
        modules (List[int]): Liste des IDs de modules enseignés
        filieres (List[int]): Liste des IDs de filières
    """
    
    def __init__(self, id: int, nom: str, specialite: str, departement: str,
                 email: str, modules: List[int], filieres: List[int]):
        self.id = id
        self.nom = nom
        self.specialite = specialite
        self.departement = departement
        self.email = email
        self.modules = modules
        self.filieres = filieres
    
    def enseigne_module(self, module_id: int) -> bool:
        """Vérifie si l'enseignant enseigne un module."""
        return module_id in self.modules
    
    def enseigne_filiere(self, filiere_id: int) -> bool:
        """Vérifie si l'enseignant intervient dans une filière."""
        return filiere_id in self.filieres
    
    def nombre_modules(self) -> int:
        """Retourne le nombre de modules enseignés."""
        return len(self.modules)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'nom': self.nom,
            'specialite': self.specialite,
            'departement': self.departement,
            'email': self.email,
            'modules': self.modules,
            'filieres': self.filieres
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Enseignant':
        """Crée une instance depuis un dictionnaire."""
        return cls(**data)
    
    def __str__(self) -> str:
        return f"{self.nom} - {self.specialite} ({self.departement})"
    
    def __repr__(self) -> str:
        return f"Enseignant(id={self.id}, nom='{self.nom}')"


# ============================================================================
# CLASSE GROUPE (FILIÈRE)
# ============================================================================

class Groupe:
    """
    Représente un groupe d'étudiants (filière).
    
    Attributes:
        id (int): Identifiant unique
        code (str): Code de la filière (ex: GEGM-1)
        nom (str): Nom complet de la filière
        niveau (str): Niveau (DEUST, Licence, Master, Cycle)
        annee (int): Année d'étude
        effectif (int): Nombre d'étudiants
        departement_id (int): ID du département
        duree_totale (int): Durée totale du programme
        modules (List[int]): Liste des IDs de modules
    """
    
    def __init__(self, id: int, code: str, nom: str, niveau: str, annee: int,
                 effectif: int, departement_id: int, duree_totale: int,
                 modules: List[int]):
        self.id = id
        self.code = code
        self.nom = nom
        self.niveau = niveau
        self.annee = annee
        self.effectif = effectif
        self.departement_id = departement_id
        self.duree_totale = duree_totale
        self.modules = modules
    
    def a_module(self, module_id: int) -> bool:
        """Vérifie si le groupe suit un module."""
        return module_id in self.modules
    
    def nombre_modules(self) -> int:
        """Retourne le nombre de modules."""
        return len(self.modules)
    
    def peut_tenir_dans(self, salle: Salle) -> bool:
        """Vérifie si le groupe peut tenir dans une salle."""
        return salle.est_disponible_pour(self.effectif)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'code': self.code,
            'nom': self.nom,
            'niveau': self.niveau,
            'annee': self.annee,
            'effectif': self.effectif,
            'departement_id': self.departement_id,
            'duree_totale': self.duree_totale,
            'modules': self.modules
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Groupe':
        """Crée une instance depuis un dictionnaire."""
        return cls(**data)
    
    def __str__(self) -> str:
        return f"{self.code} - {self.nom} ({self.effectif} étudiants)"
    
    def __repr__(self) -> str:
        return f"Groupe(id={self.id}, code='{self.code}', effectif={self.effectif})"


# ============================================================================
# CLASSE MODULE
# ============================================================================

class Module:
    """
    Représente un module d'enseignement.
    
    Attributes:
        id (int): Identifiant unique
        code (str): Code du module
        nom (str): Nom du module
        filiere_id (int): ID de la filière
        volume_horaire (int): Volume horaire total
        nb_seances_cours (int): Nombre de séances de cours
        nb_seances_td (int): Nombre de séances de TD
        nb_seances_tp (int): Nombre de séances de TP
        annee (int): Année d'étude
        enseignant_id (int): ID de l'enseignant
        enseignant (str): Nom de l'enseignant
        specialite_enseignant (str): Spécialité de l'enseignant
    """
    
    def __init__(self, id: int, code: str, nom: str, filiere_id: int,
                 volume_horaire: int, nb_seances_cours: int, nb_seances_td: int,
                 nb_seances_tp: int, annee: int, enseignant_id: int,
                 enseignant: str = "", specialite_enseignant: str = ""):
        self.id = id
        self.code = code
        self.nom = nom
        self.filiere_id = filiere_id
        self.volume_horaire = volume_horaire
        self.nb_seances_cours = nb_seances_cours
        self.nb_seances_td = nb_seances_td
        self.nb_seances_tp = nb_seances_tp
        self.annee = annee
        self.enseignant_id = enseignant_id
        self.enseignant = enseignant
        self.specialite_enseignant = specialite_enseignant
    
    def nombre_total_seances(self) -> int:
        """Retourne le nombre total de séances."""
        return self.nb_seances_cours + self.nb_seances_td + self.nb_seances_tp
    
    def a_des_cours(self) -> bool:
        """Vérifie si le module a des séances de cours."""
        return self.nb_seances_cours > 0
    
    def a_des_td(self) -> bool:
        """Vérifie si le module a des séances de TD."""
        return self.nb_seances_td > 0
    
    def a_des_tp(self) -> bool:
        """Vérifie si le module a des séances de TP."""
        return self.nb_seances_tp > 0
    
    def get_seances_par_type(self) -> Dict[str, int]:
        """Retourne le nombre de séances par type."""
        return {
            'Cours': self.nb_seances_cours,
            'TD': self.nb_seances_td,
            'TP': self.nb_seances_tp
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'code': self.code,
            'nom': self.nom,
            'filiere_id': self.filiere_id,
            'volume_horaire': self.volume_horaire,
            'nb_seances_cours': self.nb_seances_cours,
            'nb_seances_td': self.nb_seances_td,
            'nb_seances_tp': self.nb_seances_tp,
            'annee': self.annee,
            'enseignant_id': self.enseignant_id,
            'enseignant': self.enseignant,
            'specialite_enseignant': self.specialite_enseignant
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Module':
        """Crée une instance depuis un dictionnaire."""
        return cls(**data)
    
    def __str__(self) -> str:
        return f"{self.code} - {self.nom} ({self.volume_horaire}h)"
    
    def __repr__(self) -> str:
        return f"Module(id={self.id}, code='{self.code}')"


# ============================================================================
# CLASSE SEANCE
# ============================================================================

class Seance:
    """
    Représente une séance de cours/TD/TP.
    
    Attributes:
        id (int): Identifiant unique
        module_id (int): ID du module
        groupe_id (int): ID du groupe
        enseignant_id (int): ID de l'enseignant
        salle_id (int): ID de la salle
        type (TypeSeance): Type de séance
        jour (JourSemaine): Jour de la semaine
        heure_debut (time): Heure de début
        heure_fin (time): Heure de fin
        semaine (int): Numéro de semaine (optionnel)
    """
    
    def __init__(self, id: int, module_id: int, groupe_id: int,
                 enseignant_id: int, salle_id: int, type: str,
                 jour: str, heure_debut: str, heure_fin: str,
                 semaine: Optional[int] = None):
        self.id = id
        self.module_id = module_id
        self.groupe_id = groupe_id
        self.enseignant_id = enseignant_id
        self.salle_id = salle_id
        self.type = TypeSeance(type) if isinstance(type, str) else type
        self.jour = JourSemaine(jour) if isinstance(jour, str) else jour
        
        # Conversion des heures
        if isinstance(heure_debut, str):
            h, m = map(int, heure_debut.split(':'))
            self.heure_debut = time(h, m)
        else:
            self.heure_debut = heure_debut
            
        if isinstance(heure_fin, str):
            h, m = map(int, heure_fin.split(':'))
            self.heure_fin = time(h, m)
        else:
            self.heure_fin = heure_fin
            
        self.semaine = semaine
    
    def duree_minutes(self) -> int:
        """Retourne la durée de la séance en minutes."""
        debut = datetime.combine(datetime.today(), self.heure_debut)
        fin = datetime.combine(datetime.today(), self.heure_fin)
        return int((fin - debut).total_seconds() / 60)
    
    def duree_heures(self) -> float:
        """Retourne la durée de la séance en heures."""
        return self.duree_minutes() / 60
    
    def chevauche(self, autre_seance: 'Seance') -> bool:
        """Vérifie si cette séance chevauche une autre séance."""
        if self.jour != autre_seance.jour:
            return False
        
        if self.semaine and autre_seance.semaine:
            if self.semaine != autre_seance.semaine:
                return False
        
        return not (self.heure_fin <= autre_seance.heure_debut or 
                   self.heure_debut >= autre_seance.heure_fin)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'module_id': self.module_id,
            'groupe_id': self.groupe_id,
            'enseignant_id': self.enseignant_id,
            'salle_id': self.salle_id,
            'type': self.type.value,
            'jour': self.jour.value,
            'heure_debut': self.heure_debut.strftime('%H:%M'),
            'heure_fin': self.heure_fin.strftime('%H:%M'),
            'semaine': self.semaine
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Seance':
        """Crée une instance depuis un dictionnaire."""
        return cls(**data)
    
    def __str__(self) -> str:
        return f"{self.jour.value} {self.heure_debut.strftime('%H:%M')}-{self.heure_fin.strftime('%H:%M')} - {self.type.value}"
    
    def __repr__(self) -> str:
        return f"Seance(id={self.id}, type='{self.type.value}', jour='{self.jour.value}')"


# ============================================================================
# CLASSE RESERVATION
# ============================================================================

class Reservation:
    """
    Représente une réservation de salle.
    
    Attributes:
        id (int): Identifiant unique
        salle_id (int): ID de la salle réservée
        enseignant_id (int): ID de l'enseignant demandeur
        groupe_id (Optional[int]): ID du groupe (si applicable)
        jour (JourSemaine): Jour de la réservation
        heure_debut (time): Heure de début
        heure_fin (time): Heure de fin
        motif (str): Motif de la réservation
        statut (StatutReservation): Statut de la réservation
        date_creation (datetime): Date de création
    """
    
    def __init__(self, id: int, salle_id: int, enseignant_id: int,
                 jour: str, heure_debut: str, heure_fin: str, motif: str,
                 groupe_id: Optional[int] = None,
                 statut: str = "confirmée",
                 date_creation: Optional[str] = None):
        self.id = id
        self.salle_id = salle_id
        self.enseignant_id = enseignant_id
        self.groupe_id = groupe_id
        self.jour = JourSemaine(jour) if isinstance(jour, str) else jour
        
        # Conversion des heures
        if isinstance(heure_debut, str):
            h, m = map(int, heure_debut.split(':'))
            self.heure_debut = time(h, m)
        else:
            self.heure_debut = heure_debut
            
        if isinstance(heure_fin, str):
            h, m = map(int, heure_fin.split(':'))
            self.heure_fin = time(h, m)
        else:
            self.heure_fin = heure_fin
            
        self.motif = motif
        self.statut = StatutReservation(statut) if isinstance(statut, str) else statut
        
        if date_creation:
            self.date_creation = datetime.fromisoformat(date_creation)
        else:
            self.date_creation = datetime.now()
    
    def confirmer(self):
        """Confirme la réservation."""
        self.statut = StatutReservation.CONFIRMEE
    
    def mettre_en_attente(self):
        """Met la réservation en attente."""
        self.statut = StatutReservation.EN_ATTENTE
    
    def annuler(self):
        """Annule la réservation."""
        self.statut = StatutReservation.ANNULEE
    
    def est_confirmee(self) -> bool:
        """Vérifie si la réservation est confirmée."""
        return self.statut == StatutReservation.CONFIRMEE
    
    def chevauche_seance(self, seance: Seance) -> bool:
        """Vérifie si la réservation chevauche une séance."""
        if self.jour != seance.jour:
            return False
        
        return not (self.heure_fin <= seance.heure_debut or 
                   self.heure_debut >= seance.heure_fin)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire."""
        return {
            'id': self.id,
            'salle_id': self.salle_id,
            'enseignant_id': self.enseignant_id,
            'groupe_id': self.groupe_id,
            'jour': self.jour.value,
            'heure_debut': self.heure_debut.strftime('%H:%M'),
            'heure_fin': self.heure_fin.strftime('%H:%M'),
            'motif': self.motif,
            'statut': self.statut.value,
            'date_creation': self.date_creation.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reservation':
        """Crée une instance depuis un dictionnaire."""
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Réservation #{self.id} - {self.jour.value} {self.heure_debut.strftime('%H:%M')}-{self.heure_fin.strftime('%H:%M')} ({self.statut.value})"
    
    def __repr__(self) -> str:
        return f"Reservation(id={self.id}, salle_id={self.salle_id}, statut='{self.statut.value}')"


# ============================================================================
# TESTS
# ============================================================================

if __name__ == "__main__":
    print("=== Tests des classes POO ===\n")
    
    # Test Salle
    print("1. Test Salle:")
    salle = Salle(1, "Amphi A", 400, "Amphi", ["datashow", "sono"], "Biblio", 0, None)
    print(salle)
    print(f"   Partagée: {salle.est_partagee()}")
    print(f"   Capacité OK pour 350: {salle.est_disponible_pour(350)}")
    
    # Test Enseignant
    print("\n2. Test Enseignant:")
    ens = Enseignant(1, "Dr. Hassan Al-Mansouri", "Mathématiques", "Sciences", 
                     "h.mansouri@univ.edu", [1, 13, 28], [1, 3, 8])
    print(ens)
    print(f"   Enseigne module 13: {ens.enseigne_module(13)}")
    
    # Test Groupe
    print("\n3. Test Groupe:")
    groupe = Groupe(1, "GEGM-1", "Génie Électrique - Année 1", "DEUST", 1, 150, 3, 2, [1, 2, 3, 4, 5, 6])
    print(groupe)
    print(f"   Nombre de modules: {groupe.nombre_modules()}")
    
    # Test Module
    print("\n4. Test Module:")
    module = Module(1, "GEGM-1-M1", "Algèbre 1", 1, 54, 14, 14, 8, 1, 1, "Dr. Hassan Al-Mansouri")
    print(module)
    print(f"   Total séances: {module.nombre_total_seances()}")
    
    # Test Séance
    print("\n5. Test Séance:")
    seance = Seance(1, 1, 1, 1, 1, "Cours", "Lundi", "08:00", "10:00")
    print(seance)
    print(f"   Durée: {seance.duree_heures()}h")
    
    # Test Réservation
    print("\n6. Test Réservation:")
    reservation = Reservation(1, 4, 1, "Mardi", "14:00", "16:00", "Réunion pédagogique")
    print(reservation)
    print(f"   Confirmée: {reservation.est_confirmee()}")
    
    print("\n=== Tests terminés ===")
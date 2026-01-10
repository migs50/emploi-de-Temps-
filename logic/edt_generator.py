import json
from database import charger_json, sauvegarder_json

# ================== CRENEAUX ==================

CRENEAUX_LUN_JEU = [
    ("09:00", "10:30"),
    ("10:45", "12:15"),
    ("12:30", "14:00"),
    ("14:15", "15:45"),
    ("16:00", "17:30")
]

CRENEAUX_VENDREDI = [
    ("09:00", "10:30"),
    ("10:45", "12:15"),
    ("14:15", "15:45"),
    ("16:00", "17:30")
]

CRENEAUX_SAMEDI = [
    ("09:00", "10:30"),
    ("10:45", "12:15")
]

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]

# ================== UTILITAIRES ==================

def get_creneaux(jour):
    if jour in ["Lundi", "Mardi", "Mercredi", "Jeudi"]:
        return CRENEAUX_LUN_JEU
    elif jour == "Vendredi":
        return CRENEAUX_VENDREDI
    else:
        return CRENEAUX_SAMEDI

# ================== DETECTION CONFLITS ==================

def detecter_conflits(edt, seance):
    conflits = []

    for s in edt:
        meme_jour = s["jour"] == seance["jour"]
        meme_creneau = s["debut"] == seance["debut"]

        if meme_jour and meme_creneau:
            if s["salle"] == seance["salle"]:
                conflits.append("Salle occupée")

            if s["enseignant"] == seance["enseignant"]:
                conflits.append("Enseignant indisponible")

            if s["groupe"] == seance["groupe"]:
                conflits.append("Groupe en double")

    return conflits

# ================== TROUVER SALLE ==================

def trouver_salle_libre(salles, edt, jour, debut, capacite):
    for salle in salles:
        if salle["capacite"] < capacite:
            continue

        occupee = False
        for s in edt:
            if s["jour"] == jour and s["debut"] == debut and s["salle"] == salle["nom"]:
                occupee = True
                break

        if not occupee:
            return salle["nom"]

    return None

# ================== TROUVER CRENEAU ==================

def trouver_creneau_libre(edt, jour, enseignant, groupe):
    for debut, fin in get_creneaux(jour):
        libre = True
        for s in edt:
            if s["jour"] == jour and s["debut"] == debut:
                if s["enseignant"] == enseignant or s["groupe"] == groupe:
                    libre = False
                    break
        if libre:
            return debut, fin

    return None, None

# ================== PROPOSITION SOLUTION ==================

def proposer_solution(salles, edt, seance):
    for jour in JOURS:
        debut, fin = trouver_creneau_libre(
            edt, jour, seance["enseignant"], seance["groupe"]
        )
        if debut:
            salle = trouver_salle_libre(
                salles, edt, jour, debut, seance["effectif"]
            )
            if salle:
                seance.update({
                    "jour": jour,
                    "debut": debut,
                    "fin": fin,
                    "salle": salle
                })
                return seance
    return None

# ================== GENERATION EDT ==================

def generer_edt():
    salles = charger_json("DONNÉES PRINCIPALES/salles.json")
    enseignants = charger_json("DONNÉES PRINCIPALES/enseignants_final.json")
    groupes = charger_json("DONNÉES PRINCIPALES/groupes.json")
    seances = charger_json("DONNÉES PRINCIPALES/seances.json")

    edt = []

    for seance in seances:
        placee = False

        for jour in JOURS:
            debut, fin = trouver_creneau_libre(
                edt, jour, seance["enseignant"], seance["groupe"]
            )

            if debut:
                salle = trouver_salle_libre(
                    salles, edt, jour, debut, seance["effectif"]
                )

                if salle:
                    nouvelle_seance = {
                        "module": seance["module"],
                        "enseignant": seance["enseignant"],
                        "groupe": seance["groupe"],
                        "jour": jour,
                        "debut": debut,
                        "fin": fin,
                        "salle": salle
                    }

                    conflits = detecter_conflits(edt, nouvelle_seance)
                    if not conflits:
                        edt.append(nouvelle_seance)
                        placee = True
                        break

        if not placee:
            solution = proposer_solution(salles, edt, seance)
            if solution:
                edt.append(solution)

    sauvegarder_json("GESTION EDT/emplois_du_temps.json", edt)
    return edt

# ================== EXECUTION ==================

if __name__ == "__main__":
    edt = generer_edt()
    print("✅ Emploi du temps généré avec succès")
    seances = charger_json("DONNÉES PRINCIPALES/seances.json")


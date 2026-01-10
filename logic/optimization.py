from logic.conflict_manager import detecter_conflits

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


def get_creneaux(jour):
    if jour in ["Lundi", "Mardi", "Mercredi", "Jeudi"]:
        return CRENEAUX_LUN_JEU
    elif jour == "Vendredi":
        return CRENEAUX_VENDREDI
    return CRENEAUX_SAMEDI


def trouver_salle_libre(salles, edt, jour, debut, capacite):
    salles_triees = sorted(salles, key=lambda s: s["capacite"])

    for salle in salles_triees:
        if salle["capacite"] < capacite:
            continue

        conflit = False
        for s in edt:
            if s["jour"] == jour and s["debut"] == debut and s["salle"] == salle["nom"]:
                conflit = True
                break

        if not conflit:
            return salle["nom"]

    return None


def calculer_charge_par_jour(edt, groupe):
    charge = {jour: 0 for jour in JOURS}
    for s in edt:
        if s["groupe"] == groupe or (s["type"] == "Cours" and groupe.startswith(s["groupe"])):
            # Add duration (approx 90min = 1.5h, or count slots)
            charge[s["jour"]] += 1
    return charge

def trier_jours_par_charge(edt, groupe, jours_disponibles):
    charge = calculer_charge_par_jour(edt, groupe)
    # Sort days by load ascending (prefer empty days first)
    return sorted(jours_disponibles, key=lambda j: charge[j])

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

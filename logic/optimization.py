from conflict_manager import detecter_conflits

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


def trouver_creneau_libre(edt, jour, enseignant, groupe):
    for debut, fin in get_creneaux(jour):
        libre = True
        for s in edt:
            if s["jour"] == jour and s["debut"] == debut:
                if s["enseignant"] == enseignant or s["groupe"] == groupe:
                    libre = False
        if libre:
            return debut, fin
    return None, None

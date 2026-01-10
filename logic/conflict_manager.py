def detecter_conflits(edt, seance):
    conflits = []

    for s in edt:
        if s["jour"] == seance["jour"] and s["debut"] == seance["debut"]:
            if s["salle"] == seance["salle"]:
                conflits.append("Salle occupée")
            if s["enseignant"] == seance["enseignant"]:
                conflits.append("Enseignant indisponible")
            if s["groupe"] == seance["groupe"]:
                conflits.append("Groupe en double")

    return conflits

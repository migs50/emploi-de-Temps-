from logic.database import charger_json, sauvegarder_json

def salle_disponible(salle, jour, debut):
    edt = charger_json("GESTION EDT/emplois_du_temps.json")
    reservations = charger_json("GESTION EDT/reservations.json")

    for s in edt + reservations:
        if s["salle"] == salle and s["jour"] == jour and s["debut"] == debut:
            return False
    return True


def ajouter_reservation(reservation):
    if salle_disponible(reservation["salle"], reservation["jour"], reservation["debut"]):
        reservations = charger_json("GESTION EDT/reservations.json")
        reservations.append(reservation)
        sauvegarder_json("GESTION EDT/reservations.json", reservations)
        return True
    return False

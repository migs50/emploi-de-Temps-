from logic.database import charger_json, sauvegarder_json
import uuid

def salle_disponible(salle, jour, debut):
    edt = charger_json("GESTION EDT/emplois_du_temps.json")
    reservations = charger_json("GESTION EDT/reservations.json")

    # Only consider accepted reservations for availability
    for s in edt:
        if s["salle"] == salle and s["jour"] == jour and s["debut"] == debut:
            return False
            
    for r in reservations:
        if r["salle"] == salle and r["jour"] == jour and r["debut"] == debut and r.get("statut") == "Acceptée":
            return False
            
    return True

def ajouter_reservation(reservation):
    # Set default values
    reservation["id"] = str(uuid.uuid4())[:8]
    reservation["statut"] = "En attente"
    
    # We still check availability but as "En attente", it doesn't block others yet
    reservations = charger_json("GESTION EDT/reservations.json")
    reservations.append(reservation)
    sauvegarder_json("GESTION EDT/reservations.json", reservations)
    return True

def modifier_statut_reservation(resa_id, nouveau_statut):
    reservations = charger_json("GESTION EDT/reservations.json")
    for r in reservations:
        if r["id"] == resa_id:
            r["statut"] = nouveau_statut
            sauvegarder_json("GESTION EDT/reservations.json", reservations)
            return True
    return False

def get_salles_disponibles(jour, debut):
    all_salles = charger_json("DONNÉES PRINCIPALES/salles.json")
    available = []
    for s in all_salles:
        if salle_disponible(s["nom"], jour, debut):
            # Also check admin blocked slots (if they exist)
            try:
                avail = charger_json("DONNÉES PRINCIPALES/availability.json")
                is_blocked = False
                for b in avail.get("blocked_slots", []):
                    if b.get("salle") == s["nom"] and b["jour"] == jour and b["debut"] == debut:
                        is_blocked = True
                        break
                if not is_blocked:
                    available.append(s["nom"])
            except:
                available.append(s["nom"])
    return available

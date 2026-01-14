from logic.database import charger_json, sauvegarder_json
import uuid
import json
import csv
import os
import datetime

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
        if str(r.get("id", "")) == str(resa_id):
            r["statut"] = nouveau_statut
            sauvegarder_json("GESTION EDT/reservations.json", reservations)
            
            # Log notification
            try:
                notifs = charger_json("GESTION EDT/notifications.json") or []
                notif = {
                    "id": str(uuid.uuid4())[:8],
                    "enseignant": r["enseignant"],
                    "salle": r["salle"],
                    "jour": r["jour"],
                    "debut": r["debut"],
                    "statut": nouveau_statut,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "lu": False
                }
                notifs.append(notif)
                sauvegarder_json("GESTION EDT/notifications.json", notifs)
            except: pass
            
            return True
    return False

def get_salles_disponibles(jour, debut):
    # Optimization: Load data ONCE
    all_salles = charger_json("DONNÉES PRINCIPALES/salles.json")
    edt = charger_json("GESTION EDT/emplois_du_temps.json")
    reservations = charger_json("GESTION EDT/reservations.json")
    avail_config = charger_json("DONNÉES PRINCIPALES/availability.json") or {}
    blocked_slots = avail_config.get("blocked_slots", [])

    # Pre-calculate occupied rooms for this slot
    occupied_rooms = set()
    
    # 1. Check EDT
    for s in edt:
        if s["jour"] == jour and s["debut"] == debut:
             occupied_rooms.add(s["salle"])
             
    # 2. Check Reservations
    for r in reservations:
        if r["jour"] == jour and r["debut"] == debut and r.get("statut") == "Acceptée":
             occupied_rooms.add(r["salle"])
             
    # 3. Check Blocked Slots
    for b in blocked_slots:
        if b["jour"] == jour and b["debut"] == debut:
            occupied_rooms.add(b.get("salle"))

    available = []
    for s in all_salles:
        if s["nom"] not in occupied_rooms:
            available.append(s["nom"])
            
    return available

def rechercher_salles(jour, debut, min_cap=0, equipements_requis=None):
    if equipements_requis is None: equipements_requis = []
    
    # Get theoretically available rooms (name list)
    avail_names = get_salles_disponibles(jour, debut)
    
    # Load full room details to check other criteria
    all_salles = charger_json("DONNÉES PRINCIPALES/salles.json")
    results = []
    
    for s in all_salles:
        # Check availability
        if s["nom"] not in avail_names:
            continue
            
        # Check Capacity
        if s.get("capacite", 0) < min_cap:
            continue
            
        # Check Equipment
        # Normalize to set for comparison
        s_equips = set(e.lower() for e in s.get("equipements", []))
        req_equips = set(e.lower() for e in equipements_requis)
        
        # Check if all required are present
        if not req_equips.issubset(s_equips):
            continue
            
        results.append(s)
        
    return results

# Unavailability Request Management
def ajouter_demande_indisponibilite(demande):
    """Add teacher unavailability request"""
    demande["id"] = str(uuid.uuid4())[:8]
    demande["statut"] = "En attente"
    demande["date_demande"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    requests = charger_json("GESTION EDT/unavailability_requests.json") or []
    requests.append(demande)
    sauvegarder_json("GESTION EDT/unavailability_requests.json", requests)
    return True

def modifier_statut_indisponibilite(request_id, nouveau_statut):
    """Approve or reject unavailability request"""
    requests = charger_json("GESTION EDT/unavailability_requests.json") or []
    
    for req in requests:
        if str(req.get("id", "")) == str(request_id):
            req["statut"] = nouveau_statut
            sauvegarder_json("GESTION EDT/unavailability_requests.json", requests)
            
            # If approved, add to availability.json
            if nouveau_statut == "Acceptée":
                try:
                    avail = charger_json("DONNÉES PRINCIPALES/availability.json") or {}
                    if "blocked_slots" not in avail:
                        avail["blocked_slots"] = []
                    
                    block = {
                        "enseignant": req["enseignant"],
                        "jour": req["jour"],
                        "debut": req["debut"],
                        "motif": req.get("motif", "Indisponibilité")
                    }
                    avail["blocked_slots"].append(block)
                    sauvegarder_json("DONNÉES PRINCIPALES/availability.json", avail)
                except Exception as e:
                    print(f"Error adding to availability: {e}")
            
            # Send notification to teacher
            try:
                notifs = charger_json("GESTION EDT/notifications.json") or []
                notif = {
                    "id": str(uuid.uuid4())[:8],
                    "enseignant": req["enseignant"],
                    "salle": "-",
                    "jour": req["jour"],
                    "debut": req["debut"],
                    "statut": f"Indisponibilité {nouveau_statut}",
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "lu": False
                }
                notifs.append(notif)
                sauvegarder_json("GESTION EDT/notifications.json", notifs)
            except: pass
            
            return True
    return False

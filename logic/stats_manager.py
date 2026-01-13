import json
from logic.database import charger_json

def get_advanced_stats():
    try:
        edt = charger_json("GESTION EDT/emplois_du_temps.json")
        reservations = charger_json("GESTION EDT/reservations.json")
        salles = charger_json("DONNÉES PRINCIPALES/salles.json")
        
        # 1. Occupation par jour
        repartition_jou = {"Lundi": 0, "Mardi": 0, "Mercredi": 0, "Jeudi": 0, "Vendredi": 0, "Samedi": 0}
        
        # 2. Plages horaires demandées (EDT + Réservations)
        plages = {}
        
        # 3. Taux d'occupation par salle
        salle_stats = {s['nom']: 0 for s in salles}
        
        for s in edt:
            # Jour
            j = s.get('jour')
            if j in repartition_jou: repartition_jou[j] += 1
            
            # Plage
            p = s.get('debut')
            plages[p] = plages.get(p, 0) + 1
            
            # Salle
            sl = s.get('salle')
            if sl in salle_stats: salle_stats[sl] += 1
            
        # Add reservations to demand
        for r in reservations:
            p = r.get('debut')
            plages[p] = plages.get(p, 0) + 1
            
        # 4. Conflits (simple count if we had a log, otherwise we can simulate or report zero if everything is validated)
        # For now, let's assume we report the "Accepted" vs "Pending" as demand stress.
        
        return {
            "repartition_jour": repartition_jou,
            "plages_demande": dict(sorted(plages.items())),
            "salle_stats": salle_stats,
            "total_seances": len(edt),
            "total_reservations": len(reservations)
        }
    except Exception as e:
        print(f"Stats Error: {e}")
        return None

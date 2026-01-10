
# 📚 Projet EDT - Système de Gestion d'Emploi du Temps

## 📁 Structure du Projet

```
projet_edt/
│
├── salles.json              # 50 salles (Amphithéâtres, TP, TD, Cours)
├── enseignants.json         # 5 enseignants (exemples)
├── groupes.json             # 65 groupes d'étudiants
├── filieres.json            # 31 filières-années
├── modules.json             # 186 modules (6 par filière-année)
├── emplois_du_temps.json    # Emploi du temps généré (vide initialement)
├── reservations.json        # 2 réservations de salles
└── indisponibilites.json    # 2 indisponibilités
```

## 📊 Données Complètes

### 🏢 Salles (50)
- **3 Amphithéâtres** (400 places) - Pour cours DEUST
- **27 Salles TP** (30 places) - Équipées par département
- **10 Salles Cours petites** (25 places) - Petits groupes
- **6 Salles TD moyennes** (50 places) - Groupes moyens
- **4 Salles Cours grandes** (90 places) - Grands groupes

### 🎓 Filières (31 filières-années, 1764 étudiants)

**DEUST (2 ans) - 6 filières-années:**
- GEGM-1, GEGM-2 (150 étudiants/an)
- MIPC-1, MIPC-2 (200 étudiants/an)
- BCG-1, BCG-2 (130 étudiants/an)

**LICENCE (1 an) - 5 filières-années:**
- GC-1 (27 étudiants)
- AD-1 (80 étudiants)
- SSD-1 (36 étudiants)
- TAC-1 (30 étudiants)
- IDAI-1 (76 étudiants)

**MASTER (2 ans) - 8 filières-années:**
- AISD-1, AISD-2 (32 étudiants/an)
- GC-M-1, GC-M-2 (34 étudiants/an)
- SE-1, SE-2 (21 étudiants/an)
- AAIS-1, AAIS-2 (27 étudiants/an)

**CYCLE INGÉNIEUR (3 ans) - 12 filières-années:**
- AA-1, AA-2, AA-3 (30 étudiants/an)
- IND-1, IND-2, IND-3 (25 étudiants/an)
- GEMI-1, GEMI-2, GEMI-3 (26 étudiants/an)
- LSI-1, LSI-2, LSI-3 (28 étudiants/an)

### 👥 Groupes (65)
- **DEUST:** 40 groupes (cours + TP/TD divisés par 30)
- **Licence:** 5 groupes (non divisés)
- **Master:** 8 groupes (non divisés)
- **Cycle:** 12 groupes (non divisés)

### 📚 Modules (186)
- 6 modules par filière-année
- Chaque module: 10 cours + 10 TD + 8 TP = 28 séances

## 🔧 Structure des Données

### salles.json
```json
{
  "id": 1,
  "nom": "Amphi A",
  "capacite": 400,
  "type": "Amphi",
  "equipements": ["datashow", "sono", "wifi", "tableau", "micro"],
  "batiment": "Biblio",
  "etage": 0,
  "departement_id": null
}
```

### filieres.json
```json
{
  "id": 1,
  "code": "GEGM-1",
  "nom": "Génie Électrique Génie Mécanique - Année 1",
  "niveau": "DEUST",
  "annee": 1,
  "effectif": 150,
  "departement_id": 3,
  "duree_totale": 2
}
```

### groupes.json
```json
{
  "id": 1,
  "nom": "GEGM-1-Cours",
  "filiere_id": 1,
  "effectif": 150,
  "type": "Cours",
  "annee": 1
}
```

### modules.json
```json
{
  "id": 1,
  "code": "GEGM-1-M1",
  "nom": "Analyse Mathématique - GEGM Année 1",
  "filiere_id": 1,
  "volume_horaire": 42,
  "nb_seances_cours": 10,
  "nb_seances_td": 10,
  "nb_seances_tp": 8,
  "annee": 1,
  "enseignant_id": 1
}
```

### emplois_du_temps.json
```json
{
  "id": 1,
  "groupe_id": 1,
  "module_id": 1,
  "salle_id": 5,
  "jour": "Lundi",
  "heure_debut": "09:00",
  "heure_fin": "10:30",
  "type_seance": "Cours"
}
```

### reservations.json
```json
{
  "id": 1,
  "salle_id": 5,
  "enseignant_id": 1,
  "date": "2026-02-15",
  "heure_debut": "14:00",
  "heure_fin": "16:00",
  "motif": "Examen Final",
  "statut": "confirmee",
  "date_creation": "2026-01-08T21:51:00"
}
```

### indisponibilites.json
```json
{
  "id": 1,
  "salle_id": 10,
  "date_debut": "2026-03-01",
  "date_fin": "2026-03-05",
  "motif": "Maintenance équipements",
  "type": "maintenance",
  "date_creation": "2026-01-08T21:51:00"
}
```

## ⏰ Contraintes Horaires

### Horaires Hebdomadaires

**Lundi - Jeudi:**
- S1: 09h00 – 10h30 | Pause: 10h30 – 10h45
- S2: 10h45 – 12h15 | Pause: 12h15 – 12h30
- S3: 12h30 – 14h00 | Pause: 14h00 – 14h15
- S4: 14h15 – 15h45 | Pause: 15h45 – 16h00
- S5: 16h00 – 17h30

**Vendredi:**
- S1: 09h00 – 10h30 | Pause: 10h30 – 10h45
- S2: 10h45 – 12h15 | **PAUSE DÉJEUNER: 12h15 – 14h00**
- S3: 14h00 – 15h30 | Pause: 15h30 – 15h45
- S4: 15h45 – 17h15

**Samedi:**
- S1: 09h00 – 10h30 | Pause: 10h30 – 10h45
- S2: 10h45 – 12h15

**Dimanche:** Fermé

**Total:** 26 créneaux disponibles par semaine

## 🎯 Utilisation

### Consulter les données
```python
import json

# Charger les salles
with open('projet_edt/salles.json', 'r', encoding='utf-8') as f:
    salles = json.load(f)

# Afficher toutes les salles
for salle in salles:
    print(f"{salle['nom']}: {salle['capacite']} places")
```

### Filtrer les données
```python
# Trouver toutes les salles TP
salles_tp = [s for s in salles if s['type'] == 'TP']

# Trouver les filières DEUST
filieres_deust = [f for f in filieres if f['niveau'] == 'DEUST']
```

## 📊 Statistiques

- **31** filières-années
- **65** groupes
- **186** modules
- **1764** étudiants
- **50** salles
- **26** créneaux/semaine
- **5** enseignants (exemples)

## ✨ Prochaines Étapes

1. Générer l'emploi du temps complet
2. Ajouter plus d'enseignants
3. Créer des interfaces de consultation
4. Développer un système de réservation

---

**Version:** 2.0  
**Date:** 08 Janvier 2026, 21h51  
**Statut:** ✅ Opérationnel

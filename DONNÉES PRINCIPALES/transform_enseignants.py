import json

# Mapping des spécialités vers les départements
SPECIALITE_TO_DEPARTEMENT = {
    # Département A: Biologie
    "Biologie Cellulaire": "A",
    "Microbiologie": "A",
    "Microbiologie Alimentaire": "A",
    "Biochimie Alimentaire": "A",
    "Production et Zootechnie": "A",
    "Transformation des Produits Alimentaires": "A",
    "Itinéraires Techniques": "A",
    "Techniques d'Analyses": "A",
    "Biostatistique & Plan d'Expérience": "A",
    
    # Département C: Math
    "Mathématiques Appliquées": "C",
    "Analyse Numérique": "C",
    "Algèbre Linéaire": "C",
    "Probabilités et Statistiques": "C",
    "Modélisations avancée et Méthodes de génie logiciel": "C",
    "Statistique Mathématique et Simulation": "C",
    "Intégration et Probabilité": "C",
    "Optimisation et Recherche Opérationnelle": "C",
    "Modélisation Mathématique": "C",
    "Méthodes Numériques": "C",
    
    # Département E: Info
    "Programmation Orientée Objet": "E",
    "Bases de Données": "E",
    "Technologies Web": "E",
    "Système d'Exploitation": "E",
    "Intelligence Artificielle": "E",
    "Machine Learning": "E",
    "Big Data & Analytics": "E",
    "Design Patterns & Architecture": "E",
    "Sécurité Informatique": "E",
    "Cloud Computing": "E",
    "Vision par Ordinateur": "E",
    "IoT et Systèmes Embarqués": "E",
    "Réseaux et Télécommunications": "E",
    "Développement Web": "E",
    "Théories et Systèmes de Raisonnements Intelligents": "E",
    "Théorie des Graphes": "E",
    
    # Département D: Physique/Mécanique
    "Électricité Générale": "D",
    "Électronique Numérique": "D",
    "Traitement du Signal": "D",
    "Automatique et Contrôle": "D",
    "Mécanique des Fluides": "D",
    "Résistance des Matériaux": "D",
    "Génie Parasismique": "D",
    "Géotechnique": "D",
    "Matériaux de Construction": "D",
    "Gestion de Production": "D",
    "Management et Qualité": "D",
    "Logistique et Supply Chain": "D",
    "Thermodynamique Industrielle": "D",
    "Efficacité Énergétique": "D",
    "Énergies Renouvelables": "D",
    "Physique Industrielle": "D",
    "Urbanisme et Construction Durable": "D",
    "BIM et Gestion de Projet": "D",
    "Chimie Générale": "D",
    "Chimie organique avancée": "D",
    "Chimie inorganique": "D",
    "Thermochimie, Cinétique et Catalyse": "D",
    "Electrochimie et Méthodes électro-analytiques": "D",
    "Méthodes Spectroscopiques": "D",
    "Techniques d'analyse inorganiques": "D",
    
    # Départements généraux (à attribuer selon le contexte)
    "Français TEC": "C",  # Langues -> Math par défaut
    "English": "C",       # Langues -> Math par défaut
    "Soft Skills & Leadership": "C",  # Management -> Math par défaut
    "Développement personnel et intelligence émotionnelle (Soft Skills)": "C",
    "Développement de Soft Skills": "C",
    "Anglais et Management de Projet": "C"
}

def transform_enseignants(input_file, output_file):
    """
    Transforme le fichier des enseignants en supprimant specialite et diplome
    et en ajoutant le champ departement
    """
    # Lire le fichier JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Transformer chaque enseignant
    for enseignant in data['enseignants']:
        # Récupérer la spécialité avant de la supprimer
        specialite = enseignant.get('specialite', '')
        
        # Déterminer le département
        departement = SPECIALITE_TO_DEPARTEMENT.get(specialite, 'C')  # Par défaut C
        
        # Supprimer les champs
        if 'specialite' in enseignant:
            del enseignant['specialite']
        if 'diplome' in enseignant:
            del enseignant['diplome']
        
        # Ajouter le département
        enseignant['departement'] = departement
    
    # Mettre à jour la description
    data['description'] = "Enseignants avec départements (A: Biologie, C: Math, E: Info, D: Physique/Mécanique)"
    
    # Sauvegarder le nouveau fichier
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Transformation terminée!")
    print(f"📄 Fichier sauvegardé: {output_file}")
    
    # Statistiques
    dept_stats = {}
    for enseignant in data['enseignants']:
        dept = enseignant['departement']
        dept_stats[dept] = dept_stats.get(dept, 0) + 1
    
    print("\n📊 Répartition par département:")
    dept_names = {
        'A': 'Biologie',
        'C': 'Math',
        'E': 'Info',
        'D': 'Physique/Mécanique'
    }
    for dept in sorted(dept_stats.keys()):
        print(f"   {dept} ({dept_names.get(dept, 'Inconnu')}): {dept_stats[dept]} enseignants")

if __name__ == "__main__":
    input_file = "enseignants_final.json"
    output_file = "enseignants_final.json"  # Remplacer le fichier original
    
    # Créer une sauvegarde avant modification
    import shutil
    backup_file = "enseignants_final_backup.json"
    shutil.copy(input_file, backup_file)
    print(f"💾 Sauvegarde créée: {backup_file}\n")
    
    transform_enseignants(input_file, output_file)

"""
Module de gestion des fichiers JSON pour le système d'emploi du temps
Auteur: Système de Gestion Universitaire
Date: 2026-01-10
"""

import json
import os
from typing import Any, Dict, List, Optional


def load_json(filename: str) -> List[Dict[str, Any]]:
    """
    Charge les données depuis un fichier JSON.
    
    Args:
        filename (str): Nom du fichier JSON à charger
        
    Returns:
        List[Dict[str, Any]]: Liste des données chargées
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        json.JSONDecodeError: Si le fichier JSON est mal formé
    """
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Le fichier '{filename}' n'existe pas.")
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"✓ Données chargées depuis '{filename}' ({len(data)} éléments)")
        return data
        
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Erreur de décodage JSON dans '{filename}': {e.msg}",
            e.doc,
            e.pos
        )
    except Exception as e:
        raise Exception(f"Erreur lors du chargement de '{filename}': {str(e)}")


def save_json(filename: str, data: List[Dict[str, Any]]) -> bool:
    """
    Sauvegarde les données dans un fichier JSON.
    
    Args:
        filename (str): Nom du fichier JSON de destination
        data (List[Dict[str, Any]]): Données à sauvegarder
        
    Returns:
        bool: True si la sauvegarde a réussi
        
    Raises:
        Exception: En cas d'erreur lors de la sauvegarde
    """
    try:
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Données sauvegardées dans '{filename}' ({len(data)} éléments)")
        return True
        
    except Exception as e:
        raise Exception(f"Erreur lors de la sauvegarde dans '{filename}': {str(e)}")


def add_data(filename: str, item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ajoute un nouvel élément au fichier JSON.
    
    Args:
        filename (str): Nom du fichier JSON
        item (Dict[str, Any]): Élément à ajouter
        
    Returns:
        Dict[str, Any]: L'élément ajouté avec son ID
        
    Raises:
        ValueError: Si l'élément n'a pas d'ID ou si l'ID existe déjà
    """
    try:
        # Charger les données existantes
        data = load_json(filename)
        
        # Vérifier si l'élément a un ID
        if 'id' not in item:
            # Générer un nouvel ID
            max_id = max([d.get('id', 0) for d in data], default=0)
            item['id'] = max_id + 1
        
        # Vérifier si l'ID existe déjà
        if any(d.get('id') == item['id'] for d in data):
            raise ValueError(f"Un élément avec l'ID {item['id']} existe déjà.")
        
        # Ajouter l'élément
        data.append(item)
        
        # Sauvegarder
        save_json(filename, data)
        
        print(f"✓ Élément ajouté avec l'ID {item['id']}")
        return item
        
    except FileNotFoundError:
        # Si le fichier n'existe pas, le créer avec le nouvel élément
        if 'id' not in item:
            item['id'] = 1
        save_json(filename, [item])
        print(f"✓ Fichier créé et élément ajouté avec l'ID {item['id']}")
        return item


def update_data(filename: str, item_id: int, new_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Met à jour un élément existant dans le fichier JSON.
    
    Args:
        filename (str): Nom du fichier JSON
        item_id (int): ID de l'élément à mettre à jour
        new_data (Dict[str, Any]): Nouvelles données (peuvent être partielles)
        
    Returns:
        Optional[Dict[str, Any]]: L'élément mis à jour ou None si non trouvé
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    try:
        data = load_json(filename)
        
        # Chercher l'élément à mettre à jour
        for i, item in enumerate(data):
            if item.get('id') == item_id:
                # Mettre à jour l'élément (fusion des données)
                data[i].update(new_data)
                # S'assurer que l'ID ne change pas
                data[i]['id'] = item_id
                
                # Sauvegarder
                save_json(filename, data)
                
                print(f"✓ Élément avec l'ID {item_id} mis à jour")
                return data[i]
        
        print(f"✗ Aucun élément trouvé avec l'ID {item_id}")
        return None
        
    except Exception as e:
        raise Exception(f"Erreur lors de la mise à jour: {str(e)}")


def delete_data(filename: str, item_id: int) -> bool:
    """
    Supprime un élément du fichier JSON.
    
    Args:
        filename (str): Nom du fichier JSON
        item_id (int): ID de l'élément à supprimer
        
    Returns:
        bool: True si l'élément a été supprimé, False sinon
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    try:
        data = load_json(filename)
        
        # Chercher et supprimer l'élément
        initial_length = len(data)
        data = [item for item in data if item.get('id') != item_id]
        
        if len(data) < initial_length:
            # Sauvegarder
            save_json(filename, data)
            print(f"✓ Élément avec l'ID {item_id} supprimé")
            return True
        else:
            print(f"✗ Aucun élément trouvé avec l'ID {item_id}")
            return False
            
    except Exception as e:
        raise Exception(f"Erreur lors de la suppression: {str(e)}")


def get_by_id(filename: str, item_id: int) -> Optional[Dict[str, Any]]:
    """
    Récupère un élément par son ID.
    
    Args:
        filename (str): Nom du fichier JSON
        item_id (int): ID de l'élément recherché
        
    Returns:
        Optional[Dict[str, Any]]: L'élément trouvé ou None
    """
    try:
        data = load_json(filename)
        
        for item in data:
            if item.get('id') == item_id:
                return item
        
        return None
        
    except Exception as e:
        print(f"Erreur lors de la recherche: {str(e)}")
        return None


def filter_data(filename: str, **kwargs) -> List[Dict[str, Any]]:
    """
    Filtre les données selon des critères.
    
    Args:
        filename (str): Nom du fichier JSON
        **kwargs: Critères de filtrage (key=value)
        
    Returns:
        List[Dict[str, Any]]: Liste des éléments correspondants
        
    Example:
        >>> filter_data('salles.json', type='TP', departement_id=1)
    """
    try:
        data = load_json(filename)
        
        filtered = data
        for key, value in kwargs.items():
            filtered = [item for item in filtered if item.get(key) == value]
        
        return filtered
        
    except Exception as e:
        print(f"Erreur lors du filtrage: {str(e)}")
        return []


# Fonctions utilitaires supplémentaires

def count_items(filename: str) -> int:
    """Compte le nombre d'éléments dans le fichier."""
    try:
        data = load_json(filename)
        return len(data)
    except:
        return 0


def exists(filename: str, item_id: int) -> bool:
    """Vérifie si un élément existe."""
    return get_by_id(filename, item_id) is not None


def get_all(filename: str) -> List[Dict[str, Any]]:
    """Récupère tous les éléments du fichier."""
    try:
        return load_json(filename)
    except:
        return []


if __name__ == "__main__":
    # Tests unitaires
    print("=== Tests du module database.py ===\n")
    
    # Test 1: Création et ajout
    test_file = "test_data.json"
    print("Test 1: Ajout de données")
    add_data(test_file, {"nom": "Test 1", "value": 100})
    add_data(test_file, {"nom": "Test 2", "value": 200})
    
    # Test 2: Lecture
    print("\nTest 2: Lecture des données")
    data = load_json(test_file)
    print(f"Données chargées: {data}")
    
    # Test 3: Mise à jour
    print("\nTest 3: Mise à jour")
    update_data(test_file, 1, {"value": 150, "updated": True})
    
    # Test 4: Recherche par ID
    print("\nTest 4: Recherche par ID")
    item = get_by_id(test_file, 1)
    print(f"Item trouvé: {item}")
    
    # Test 5: Filtrage
    print("\nTest 5: Filtrage")
    filtered = filter_data(test_file, value=200)
    print(f"Éléments filtrés: {filtered}")
    
    # Test 6: Suppression
    print("\nTest 6: Suppression")
    delete_data(test_file, 2)
    
    # Nettoyage
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\n✓ Fichier de test '{test_file}' supprimé")
    
    print("\n=== Tests terminés ===")
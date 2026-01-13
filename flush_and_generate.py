import sys
import os

# Add root to sys.path
sys.path.append(os.getcwd())

from logic.seance_generator import generate_seances
from logic.edt_generator import generer_edt

if __name__ == "__main__":
    print("🧹 Nettoyage et Régénération des données...")
    try:
        generate_seances()
        edt = generer_edt()
        print(f"✨ Succès: {len(edt)} séances générées dans 'output/emplois_du_temps.json'")
    except Exception as e:
        print(f"❌ Erreur lors de la régénération: {e}")

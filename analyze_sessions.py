import json

SEANCES_PATH = "DONNÉES PRINCIPALES/seances.json"
TARGET_MODULES = [
    "LC3",
    "Anglais Scientifique II & Soft Skills",
    "Anglais 2",
    "Langues Etrangères"
]

def analyze():
    try:
        with open(SEANCES_PATH, 'r', encoding='utf-8') as f:
            seances = json.load(f)
        
        found = []
        for s in seances:
            if s.get('module') in TARGET_MODULES:
                found.append(s)
        
        with open("session_analysis.txt", "w", encoding='utf-8') as out:
            out.write(f"Total sessions found: {len(found)}\n")
            for s in found:
                out.write(f"ID: {s['id']}, Module: {s['module']}, Type: {s['type']}, Filiere: {s['filiere']}, Group: {s.get('groupe')}\n")
        
        print("Analysis written to session_analysis.txt")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze()

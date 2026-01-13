import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
ENG_TEACHERS = ["Dr. Rachid Farah", "Dr. Nadia Benyakoub"]

def analyze_eng_teachers():
    try:
        with open(EDT_PATH, 'r', encoding='utf-8') as f:
            edt = json.load(f)
        
        loads = {t: 0 for t in ENG_TEACHERS}
        for s in edt:
            enseignant = s.get('enseignant')
            if enseignant in ENG_TEACHERS:
                loads[enseignant] += 1
        
        with open("eng_teacher_load_analysis.txt", "w", encoding='utf-8') as out:
            for t, count in loads.items():
                out.write(f"Teacher: {t}, Total scheduled sessions: {count}\n")
        
        print("Analysis written to eng_teacher_load_analysis.txt")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_eng_teachers()

import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
TARGET_TEACHERS = ["Dr. Youssef Bennouna", "Dr. Karim Saadaoui", "Pr. Mohammed Abdelilah"]

def analyze_teachers():
    try:
        with open(EDT_PATH, 'r', encoding='utf-8') as f:
            edt = json.load(f)
        
        loads = {t: 0 for t in TARGET_TEACHERS}
        for s in edt:
            enseignant = s.get('enseignant')
            if enseignant in TARGET_TEACHERS:
                loads[enseignant] += 1
        
        with open("teacher_load_analysis.txt", "w", encoding='utf-8') as out:
            for t, count in loads.items():
                out.write(f"Teacher: {t}, Total scheduled sessions: {count}\n")
        
        print("Analysis written to teacher_load_analysis.txt")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_teachers()

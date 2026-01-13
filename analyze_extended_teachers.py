import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"
TEACHERS = [
    "Dr. Mohamed Salah",
    "Dr. Hassan Al-Mansouri",
    "Dr. Mehdi Khalilzadeh",
    "Dr. Nadia Lahsen",
    "Dr. Youssef Bennouna",
    "Dr. Karim Saadaoui",
    "Pr. Mohammed Abdelilah"
]

def analyze_extended_teachers():
    try:
        with open(EDT_PATH, 'r', encoding='utf-8') as f:
            edt = json.load(f)
        
        loads = {t: 0 for t in TEACHERS}
        for s in edt:
            enseignant = s.get('enseignant')
            if enseignant in TEACHERS:
                loads[enseignant] += 1
        
        with open("extended_teacher_load.txt", "w", encoding='utf-8') as out:
            for t, count in sorted(loads.items(), key=lambda x: x[1], reverse=True):
                out.write(f"{t}: {count} sessions\n")
        
        print("Analysis written to extended_teacher_load.txt")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_extended_teachers()

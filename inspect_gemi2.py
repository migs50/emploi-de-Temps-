import json

EDT_PATH = "GESTION EDT/emplois_du_temps.json"

def inspect():
    with open(EDT_PATH, 'r', encoding='utf-8') as f:
        edt = json.load(f)
    
    g2 = [s for s in edt if s.get('filiere') == 'GEMI-2']
    g2.sort(key=lambda x: (x.get('jour'), x.get('debut')))
    
    with open("gemi2_inspection.txt", "w", encoding='utf-8') as out:
        out.write("GEMI-2 Sessions found in EDT:\n")
        for s in g2:
            out.write(f"{s['jour']} {s['debut']}-{s['fin']} | Mod: {s['module']} | Type: {s['type']} | Room: {s['salle']} | Prof: {s['enseignant']}\n")

if __name__ == "__main__":
    inspect()

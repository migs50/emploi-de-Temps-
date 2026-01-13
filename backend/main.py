from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import json
import sys

# Add project root to path to import logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.edt_generator import generer_edt

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to load JSON
def load_json(path):
    full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.get("/api/schedule")
def get_schedule():
    return load_json("GESTION EDT/emplois_du_temps.json")

@app.get("/api/generate")
def generate_schedule():
    try:
        edt = generer_edt()
        return {"status": "success", "count": len(edt)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/teachers")
def get_teachers():
    return load_json("DONNÉES PRINCIPALES/enseignants_final.json")

@app.get("/api/rooms")
def get_rooms():
    return load_json("DONNÉES PRINCIPALES/salles.json")

@app.get("/api/modules")
def get_modules():
    return load_json("DONNÉES PRINCIPALES/modules (1).json")

@app.get("/api/stats")
def get_stats():
    # Helper to count things safely
    t = load_json("DONNÉES PRINCIPALES/enseignants_final.json")
    if isinstance(t, dict): t = t.get("enseignants", [])
    
    m = load_json("DONNÉES PRINCIPALES/modules (1).json")
    s = load_json("DONNÉES PRINCIPALES/salles.json")
    
    return {
        "teachers": len(t),
        "modules": len(m),
        "rooms": len(s)
    }

# Serve Frontend if built (production mode later)
# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

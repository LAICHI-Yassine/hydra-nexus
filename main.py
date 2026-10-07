from fastapi import FastAPI
from pydantic import BaseModel

# 1. Initialisation de l'API
app = FastAPI(title="Hydra-Nexus API")

# 2. Création du "moule" de données pour nos futurs capteurs
class DonneesCapteur(BaseModel):
    id_capteur: str
    temperature: float
    humidite_sol: float

# 3. La route d'accueil (inchangée)
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Hydra-Nexus : Le système central est en ligne."}

# 4. NOUVELLE ROUTE : Pour recevoir (POST) des données
@app.post("/api/capteurs")
def recevoir_donnees(donnees: DonneesCapteur):
    # L'API analyse les données via le moule, puis renvoie une confirmation
    return {
        "statut": "Succès",
        "message": f"Alerte : Nouvelles données traitées pour le capteur {donnees.id_capteur}",
        "donnees_recues": donnees
    }
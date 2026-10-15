import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq

# 1. On charge le coffre-fort (.env) dans la mémoire d'Ubuntu
load_dotenv()
cle_groq = os.getenv("GROQ_API_KEY")

# 2. Initialisation de l'API
app = FastAPI(title="Hydra-Nexus API")

# 3. Configuration du modèle IA Open-Source (Llama 3.3 70B) via Groq
assistant_ia = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=cle_groq,
    temperature=0.3,
    max_tokens=600
)

# --- MOULES DE DONNÉES (Pydantic) ---
class DonneesCapteur(BaseModel):
    id_capteur: str
    temperature: float
    humidite_sol: float

class QuestionAgricole(BaseModel):
    question: str

# --- ROUTES DE L'API (100% inchangées !) ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Hydra-Nexus : Le système central est en ligne."}

@app.post("/api/capteurs")
def recevoir_donnees(donnees: DonneesCapteur):
    return {
        "statut": "Succès",
        "message": f"Alerte : Nouvelles données traitées pour le capteur {donnees.id_capteur}",
        "donnees_recues": donnees
    }

@app.post("/api/assistant")
def poser_question(requete: QuestionAgricole):
    # Injection du contexte système avant la question de l'utilisateur
    messages = [
        (
            "system",
            "Tu es Hydra-Nexus, un assistant IA expert en agronomie, climatologie et gestion de l'eau. "
            "Réponds toujours de manière très professionnelle, précise et orientée vers l'optimisation des ressources hydriques."
        ),
        ("human", requete.question),
    ]
    
    reponse = assistant_ia.invoke(messages)
    
    return {
        "question_posee": requete.question,
        "reponse_ia": reponse.content
    }
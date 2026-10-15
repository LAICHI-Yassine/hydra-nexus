import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import PromptTemplate

# 1. Chargement des clés
load_dotenv()
cle_groq = os.getenv("GROQ_API_KEY")

# 2. Initialisation de l'API
app = FastAPI(title="Hydra-Nexus API (Avec RAG)")

# 3. Configuration de l'IA (Cerveau)
assistant_ia = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=cle_groq,
    temperature=0.3,
    max_tokens=600
)

# 4. Configuration de la Mémoire Vectorielle (Qdrant)
print("-> Chargement de la mémoire vectorielle Qdrant...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    path="./qdrant_db",
    collection_name="agronomie"
)
retriever = qdrant.as_retriever(search_kwargs={"k": 2}) # On récupère les 2 meilleurs paragraphes

# --- MOULES DE DONNÉES ---
class DonneesCapteur(BaseModel):
    id_capteur: str
    temperature: float
    humidite_sol: float

class QuestionAgricole(BaseModel):
    question: str

# --- ROUTES ---
@app.get("/")
def read_root():
    return {"message": "Hydra-Nexus en ligne. Système RAG activé."}

@app.post("/api/assistant")
def poser_question_rag(requete: QuestionAgricole):
    # ÉTAPE A : Le Retriever fouille dans Qdrant pour trouver les documents liés à la question
    documents_trouves = retriever.invoke(requete.question)
    
    # On compile le texte des documents trouvés
    contexte_extrait = "\n\n".join([doc.page_content for doc in documents_trouves])
    
    # ÉTAPE B : On injecte ce contexte dans le System Prompt
    prompt_rag = f"""Tu es Hydra-Nexus, un assistant expert en hydrologie.
    Utilise EXCLUSIVEMENT les documents de contexte ci-dessous pour répondre à la question.
    Si la réponse n'est pas dans le contexte, dis "Je n'ai pas cette information locale".
    
    CONTEXTE LOCAL :
    {contexte_extrait}
    
    QUESTION : {requete.question}
    """
    
    messages = [("human", prompt_rag)]
    reponse = assistant_ia.invoke(messages)
    
    return {
        "question_posee": requete.question,
        "sources_utilisees": len(documents_trouves),
        "reponse_ia": reponse.content
    }
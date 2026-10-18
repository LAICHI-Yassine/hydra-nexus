# 💧 Hydra-Nexus : Plateforme d'Intelligence Climatique & Hydrique (RAG)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.2-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Qdrant](https://img.shields.io/badge/VectorDB-Qdrant-darkred?logo=qdrant&logoColor=white)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-green)

## 📌 Présentation du Projet
**Hydra-Nexus** est un assistant intelligent basé sur l'architecture **RAG (Retrieval-Augmented Generation)**. Conçu pour répondre aux enjeux de la *ClimateTech*, il assiste les ingénieurs agronomes dans l'optimisation des ressources hydriques et la gestion de l'irrigation. 

Le système croise en temps réel des données de télémétrie locales (capteurs IoT simulés : humidité, température) avec une base de connaissances vectorisée contenant des rapports climatiques et agronomiques privés.

## 🚀 Fonctionnalités Clés
- **Système RAG Complet** : Ingestion, chunking et vectorisation de documents locaux (Embeddings `sentence-transformers`).
- **Moteur LLM Open-Source** : Intégration de modèles de pointe (ex: Qwen 27B) via l'API Groq pour une inférence ultra-rapide.
- **Base Vectorielle Locale** : Utilisation de **Qdrant** pour une recherche sémantique précise et sans hallucination.
- **Architecture Microservices** : Découplage total entre le cerveau IA (FastAPI) et l'interface utilisateur (Streamlit).
- **Interface Command Center** : Dashboard UI/UX moderne (Mode sombre, Glassmorphism) pour la visualisation des KPIs.

## 🛠️ Stack Technique
* **Backend** : FastAPI, Uvicorn, Python
* **IA & Machine Learning** : LangChain, Groq API, HuggingFace Embeddings
* **Base de données** : Qdrant (Vector DB)
* **Frontend** : Streamlit, HTML/CSS (Custom)
* **MLOps / Déploiement** : Docker, Docker Compose

## 🐳 Installation et Lancement (Recommandé)
Le projet est entièrement conteneurisé pour garantir une exécution parfaite sur n'importe quel environnement.

### Prérequis
- [Docker](https://www.docker.com/) et Docker Compose installés sur votre machine.
- Une clé API Groq (gratuite).

### Instructions

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/LAICHI-Yassine/hydra-nexus.git
   cd hydra-nexus

2. Créez un fichier .env à la racine et ajoutez votre clé API :

    ```bash
    GROQ_API_KEY=votre_cle_api_ici

3. Lancez la flotte de conteneurs :

    ```bash
    sudo docker compose up --build

4. Ouvrez votre navigateur et accédez au Dashboard : http://localhost:8501

📂 Structure de l'Architecture
    ```bash
    hydra-nexus/
    ├── data/                   # Rapports agricoles bruts (TXT/PDF)
    ├── qdrant_db/              # Base de données vectorielle (Générée localement)
    ├── main.py                 # Backend (API FastAPI + Logique RAG LangChain)
    ├── ui.py                   # Frontend (Dashboard Streamlit)
    ├── ingest.py               # Script d'ingestion et de vectorisation des données
    ├── Dockerfile.backend      # Recette de conteneurisation de l'API
    ├── Dockerfile.frontend     # Recette de conteneurisation de l'Interface
    ├── docker-compose.yml      # Orchestrateur réseau
    └── requirements.txt        # Dépendances Python
👨‍💻 Auteur
Conçu et développé par Yassine Laichi dans le cadre de la conception d'architectures d'Intelligence Artificielle appliquées.
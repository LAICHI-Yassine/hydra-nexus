import streamlit as st
import requests
import time

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Hydra-Nexus | Command Center", 
    page_icon="💧", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. INJECTION DU CSS PERSONNALISÉ (MODE SOMBRE DÉGRADÉ)
# ==========================================
st.markdown("""
<style>
    /* Masquer les éléments par défaut de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    
    /* Arrière-plan global : Dégradé de bleu profond nuit */
    .stApp {
        background: linear-gradient(135deg, #09152b 0%, #112d4e 100%);
    }
    
    /* Stylisation des métriques (KPIs) : Effet Verre Fumé (Glassmorphism) */
    div[data-testid="metric-container"] {
        background: rgba(17, 45, 78, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #00ADB5; /* Accent Cyan Eau */
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, border-left-color 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-left-color: #38BDF8; /* Cyan plus vif au survol */
        background: rgba(17, 45, 78, 0.6);
    }
    
    /* Boutons premium avec dégradé subtil */
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(90deg, #112d4e 0%, #3F72AF 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00ADB5 0%, #3F72AF 100%);
        border-color: #00ADB5;
        box-shadow: 0 4px 20px rgba(0, 173, 181, 0.4);
        transform: scale(1.02);
        color: white;
    }

    /* Personnalisation des champs de texte pour le mode sombre */
    .stTextInput>div>div>input {
        background-color: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #E2E8F0;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00ADB5;
        box-shadow: 0 0 8px rgba(0, 173, 181, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. GESTION DE L'ÉTAT (SESSION STATE)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Système Hydra-Nexus initialisé. Je suis connecté aux capteurs locaux et à la base vectorielle. Comment puis-je optimiser votre gestion hydrique aujourd'hui ?"},
        {"role": "user", "content": "Faut-il irriguer la parcelle B aujourd'hui ?"},
        {"role": "assistant", "content": "D'après les relevés des capteurs, l'humidité de la parcelle B est actuellement à 16% (au-dessus du seuil critique local de 14.5%). Les prévisions météorologiques annoncent des précipitations dans 48h. **Recommandation :** Aucune irrigation d'urgence n'est requise. Économie d'eau conseillée."}
    ]

# ==========================================
# 4. PANNEAU LATÉRAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("## 💧 Hydra-Nexus")
    st.caption("CENTRE DE CONTRÔLE IA")
    st.markdown("---")
    
    st.markdown("🟢 **Capteurs IoT** : Synchronisés")
    st.markdown("🟢 **FastAPI Core** : En ligne")
    st.markdown("🟢 **Qdrant Vector DB** : Actif")
    
    st.markdown("---")
    st.subheader("⚙️ Ingestion de Données (RAG)")
    
    st.file_uploader("Nouveau rapport climatique (PDF/TXT)", type=['pdf', 'txt'])
    
    st.markdown("---")
    st.subheader("🌡️ Télémétrie en direct")
    temp = st.slider("Température ambiante (°C)", min_value=10.0, max_value=45.0, value=28.5)
    hum = st.slider("Humidité du sol moyenne (%)", min_value=0.0, max_value=100.0, value=15.2)
    
    if st.button("Forcer la synchronisation"):
        st.toast(f"Télémétrie mise à jour : {temp}°C | {hum}%", icon="✅")

# ==========================================
# 5. ZONE PRINCIPALE (DASHBOARD)
# ==========================================
st.title("Tableau de Bord Agronomique")
st.markdown("*Analyse RAG en temps réel pour la résilience hydrique*")
st.write("") 

# -- KPIs (Métriques clés) --
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Humidité Zone A4", "14.8 %", "-0.2 %", delta_color="inverse")
with col2:
    st.metric("Réserve d'Eau", "84 %", "+2 %")
with col3:
    st.metric("Prévision Pluie", "0 mm", "Sécheresse", delta_color="off")
with col4:
    st.metric("Stress Hydrique", "Élevé", "Alerte", delta_color="inverse")

st.markdown("---")

# ==========================================
# 6. ESPACE ASSISTANT (CHAT RAG)
# ==========================================
st.subheader("💬 Terminal RAG (Interrogation Qdrant & Groq)")

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Champ de saisie utilisateur
if prompt := st.chat_input("Ex: Quel est le seuil critique pour la zone A4 ?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Recherche vectorielle et inférence LLM en cours..."):
            try:
                # Appel au Backend FastAPI
                import os
                api_url = os.getenv("API_URL", "http://127.0.0.1:8000") # Si Docker, utilise API_URL. Sinon (en local), utilise 127.0.0.1.
                reponse = requests.post(
                    f"{api_url}/api/assistant",
                    json={"question": prompt}
                )
                
                if reponse.status_code == 200:
                    donnees = reponse.json()
                    reponse_finale = donnees["reponse_ia"]
                    sources = donnees.get("sources_utilisees", 0)
                    
                    if sources > 0:
                        reponse_finale += f"\n\n---\n*🔍 Audit : Analyse basée sur {sources} document(s) classifié(s) dans Qdrant.*"
                else:
                    reponse_finale = f"❌ Erreur API : {reponse.status_code}"
            
            except Exception as e:
                time.sleep(1.5)
                reponse_finale = "⚠️ **Mode Simulation** : Serveur FastAPI hors ligne. Veuillez démarrer Uvicorn. \n\n*Réponse simulée : Le seuil critique de la zone A4 est de 14.5% pendant 48h.*"

        message_placeholder.markdown(reponse_finale)
        
    st.session_state.messages.append({"role": "assistant", "content": reponse_finale})
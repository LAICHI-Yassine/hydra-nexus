from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

print("1. Chargement du document agricole...")
loader = TextLoader("data/rapport_agricole.txt", encoding="utf-8")
documents = loader.load()

print("2. Découpage en morceaux (Chunking)...")
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

print("3. Initialisation du modèle d'Embeddings local...")
# Ce modèle transforme le français en vecteurs. Il sera téléchargé une seule fois sur votre PC.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("4. Création et sauvegarde de la base vectorielle Qdrant...")
qdrant = QdrantVectorStore.from_documents(
    chunks,
    embeddings,
    path="./qdrant_db", # Cela va créer un dossier de base de données local
    collection_name="agronomie"
)
print("Succès ! La base vectorielle est prête et sauvegardée.")
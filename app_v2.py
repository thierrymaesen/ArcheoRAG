import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
# On utilise la mécanique OpenAI mais pointée vers HuggingFace !
from langchain_openai import ChatOpenAI

# ==========================================
# 0. CONFIGURATION DES CLÉS API
# ==========================================
hf_token = "VOTRE_CLE_API_ICI"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token

# ==========================================
# 1. INGESTION DU PDF ET DÉCOUPE STRATÉGIQUE
# ==========================================
pdf_path = "rapport.pdf"
print(f"📄 Lecture du rapport : {pdf_path}")
loader = PyPDFLoader(pdf_path)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=300, 
    separators=["\n\n", "\n", ".", " "]
)
chunks = text_splitter.split_documents(documents)
print(f"✂️ Document découpé en {len(chunks)} morceaux intelligents.")

# ==========================================
# 2. CRÉATION DE LA MÉMOIRE (BASE DE DONNÉES)
# ==========================================
print("🧠 Chargement du modèle mathématique (Embedding)...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

import shutil

print("🧹 Nettoyage de l'ancienne base de données...")
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")

print("💾 Création de la base de données vectorielle locale...")
db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db")
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k": 10})

# ==========================================
# 3. LE CERVEAU (LLM) ROUTÉ SUR HUGGING FACE
# ==========================================
print("🤖 Connexion au LLM gratuit (Llama-3) via le routeur HuggingFace...")

# L'ASTUCE EST ICI : On utilise ChatOpenAI, mais on pointe vers l'API gratuite de Hugging Face
chat_model = ChatOpenAI(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    api_key=hf_token,
    base_url="https://router.huggingface.co/v1",
    max_tokens=512,
    temperature=0.1
)

# Le Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un archéologue expert qui analyse des rapports de fouilles. Ton but est d'extraire les informations factuelles du contexte fourni. Si la réponse peut être déduite logiquement du contexte, donne-la clairement. Si le contexte ne contient aucune information liée à la question, réponds 'Les données ne permettent pas de répondre'."),
    ("human", "Contexte : {context}\n\nQuestion : {question}")
])

# ==========================================
# 4. EXÉCUTION ET AFFICHAGE DES SOURCES
# ==========================================
question = "En quelle année le document a-t-il été rédigé ?"
print(f"\n❓ Question posée : {question}\n")
print("⏳ Recherche dans la base de données et rédaction...\n")

# 1. On cherche les documents dans ChromaDB
docs_trouves = retriever.invoke(question)

# 2. On colle les textes
contexte_texte = "\n\n".join([doc.page_content for doc in docs_trouves])

# 3. On demande la réponse à l'IA
messages = prompt.invoke({"context": contexte_texte, "question": question})
reponse_ai = chat_model.invoke(messages)

# 4. AFFICHAGE DE LA RÉPONSE ET DES PREUVES
print("================ R É P O N S E ===================")
print(reponse_ai.content)
print("\n================= P R E U V E S ==================")
print("Voici les paragraphes que l'IA a utilisés pour vous répondre :\n")

for i, doc in enumerate(docs_trouves):
    page = doc.metadata.get('page', 'Inconnue') # PyPDFLoader enregistre le n° de page !
    print(f"--- SOURCE {i+1} (Page {page}) ---")
    
    # On affiche un extrait raccourci (les 300 premiers caractères) pour ne pas polluer l'écran
    extrait = doc.page_content[:300].replace('\n', ' ')
    print(f"{extrait} [...]\n")
    
print("==================================================")
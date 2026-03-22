# --- FIX STREAMLIT CLOUD POUR CHROMADB ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# -----------------------------------------

import streamlit as st
import os
import tempfile
import requests
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# ==========================================
# CONFIGURATION DE LA PAGE STREAMLIT
# ==========================================
st.set_page_config(page_title="ArchéoRAG", page_icon="🏛️", layout="wide")
st.title("🏛️ ArchéoRAG : Assistant d'Analyse Archéologique")
st.markdown("Interrogez des rapports de fouilles en langage naturel.")

# Initialisation de la variable de session pour la clé API (sécurité)
if "hf_token" not in st.session_state:
    st.session_state.hf_token = ""

# ==========================================
# BARRE LATÉRALE (SIDEBAR) : Paramètres et Fichiers
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Champ sécurisé pour la clé API (elle ne sera pas sauvegardée sur GitHub !)
    api_key = st.text_input("Clé API Hugging Face (hf_...)", type="password", value=st.session_state.hf_token)
    if api_key:
        st.session_state.hf_token = api_key
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = api_key

    st.divider()
    st.header("📄 Charger un Rapport (PDF)")
    
    # Méthode 1 : Drag & Drop
    uploaded_file = st.file_uploader("Glissez un fichier PDF ici", type=["pdf"])
    
    # Méthode 2 : Lien URL
    st.markdown("**OU**")
    pdf_url = st.text_input("Collez l'URL publique d'un PDF")

    process_button = st.button("🚀 Analyser le document")

# ==========================================
# LOGIQUE D'INGESTION (Au clic sur le bouton)
# ==========================================
@st.cache_resource # Met en cache le modèle pour ne pas le recharger à chaque question
def load_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if process_button:
    if not st.session_state.hf_token:
        st.error("⚠️ Veuillez entrer votre clé API Hugging Face dans la barre latérale.")
    elif uploaded_file is None and not pdf_url:
        st.warning("⚠️ Veuillez uploader un PDF ou fournir une URL.")
    else:
        with st.spinner("⏳ Téléchargement et analyse en cours..."):
            try:
                # 1. Gestion du fichier (Création d'un fichier temporaire)
                pdf_path = "temp_rapport.pdf"
                
                if uploaded_file is not None:
                    # Si c'est un drag & drop
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                elif pdf_url:
                    # Si c'est un lien web
                    response = requests.get(pdf_url)
                    response.raise_for_status()
                    with open(pdf_path, "wb") as f:
                        f.write(response.content)

                # 2. Nettoyage de l'ancienne base de données
                if os.path.exists("./chroma_db_st"):
                    shutil.rmtree("./chroma_db_st")

                # 3. Lecture et Découpage
                loader = PyPDFLoader(pdf_path)
                documents = loader.load()
                
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1500, chunk_overlap=300, separators=["\n\n", "\n", ".", " "]
                )
                chunks = text_splitter.split_documents(documents)
                
                # 4. Création de la Base de données
                embedding_model = load_embedding_model()
                db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db_st")
                
                # On sauvegarde le retriever dans la session Streamlit
                st.session_state.retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k": 10})
                
                st.success(f"✅ Document analysé avec succès ! ({len(chunks)} extraits mémorisés). Vous pouvez poser vos questions.")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de l'analyse : {e}")

# ==========================================
# ZONE DE CHAT
# ==========================================
st.divider()
question = st.text_input("💬 Posez votre question sur le document :")

if question:
    if "retriever" not in st.session_state:
        st.warning("⚠️ Veuillez d'abord analyser un document via la barre latérale.")
    else:
        with st.spinner("🧠 L'IA réfléchit..."):
            # 1. Recherche des documents
            docs_trouves = st.session_state.retriever.invoke(question)
            contexte_texte = "\n\n".join([doc.page_content for doc in docs_trouves])
            
            # 2. Configuration du Cerveau
            chat_model = ChatOpenAI(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                api_key=st.session_state.hf_token,
                base_url="https://router.huggingface.co/v1",
                max_tokens=512,
                temperature=0.1
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Tu es un archéologue expert qui analyse des rapports de fouilles. Ton but est d'extraire les informations factuelles du contexte fourni. Si la réponse peut être déduite logiquement du contexte, donne-la clairement. Si le contexte ne contient aucune information liée à la question, réponds 'Les données ne permettent pas de répondre'."),
                ("human", "Contexte : {context}\n\nQuestion : {question}")
            ])
            
            messages = prompt.invoke({"context": contexte_texte, "question": question})
            
            # 3. Réponse
            try:
                reponse_ai = chat_model.invoke(messages)
                st.info("### Réponse de l'expert :")
                st.write(reponse_ai.content)
                
                # 4. Affichage des Preuves (Dans un menu déroulant élégant)
                with st.expander("🔍 Voir les extraits sources utilisés par l'IA"):
                    for i, doc in enumerate(docs_trouves):
                        page = doc.metadata.get('page', 'Inconnue')
                        st.markdown(f"**Source {i+1} (Page {page})**")
                        st.caption(doc.page_content)
                        st.divider()
                        
            except Exception as e:
                st.error(f"❌ Erreur de connexion au modèle IA : {e}")
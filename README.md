# 🏛️ ArchéoRAG : Assistant d'Analyse Archéologique par IA

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Llama--3-yellow)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

**ArchéoRAG** est un outil open-source conçu pour aider les archéologues, chercheurs et responsables de Centres de Conservation et d'Étude (CCE) à interroger la "littérature grise" (rapports de fouilles, publications) à l'aide de l'Intelligence Artificielle, de manière éthique, traçable et sans hallucination.

## 🎯 Le Concept
L'outil utilise une architecture **RAG** (Retrieval-Augmented Generation). Au lieu de se fier aux connaissances générales et parfois erronées d'un modèle d'IA, ArchéoRAG :
1. Lit votre rapport PDF (localement ou via une URL publique comme HAL).
2. Le découpe et le mémorise dans une base de données vectorielle locale (`ChromaDB`).
3. Cherche les extraits pertinents liés à votre question.
4. Demande à un modèle IA Open-Source (`Llama-3-8B-Instruct`) de formuler une réponse **exclusivement basée sur ces extraits**.

### ✨ Fonctionnalités
- **Zéro conservation de données :** La base de données est réinitialisée à chaque nouvelle analyse. Aucune donnée sensible n'est stockée à long terme.
- **Preuves et Traçabilité :** Chaque réponse de l'IA est accompagnée des extraits bruts du PDF et du numéro de la page d'où provient l'information.
- **Ancrage fort (Grounding) :** Un "Prompt Système" strict empêche l'IA d'inventer des faits.

---

## 🔍 Exemple concret : La gestion du "Je ne sais pas" (L'Explicabilité de l'IA)

L'un des défis majeurs de l'IA en archéologie est l'invention de faits (hallucinations). Ce projet a été développé pour privilégier l'honnêteté scientifique.

**Test :** Poser la question *"En quelle année ce document a-t-il été rédigé ?"* sur un PDF dont la date n'est pas formatée comme du texte classique.

**Comportement d'ArchéoRAG :**
1. La recherche vectorielle va chercher des paragraphes sémantiquement proches du mot "rédigé" ou "année". 
2. Si le document ne contient pas ces mots clés de façon explicite, la base de données renvoie les textes les "moins éloignés" (qui peuvent parfois n'avoir aucun rapport logique pour un humain).
3. **Le cerveau (Llama-3)** lit ces textes, constate l'absence de date, et refuse d'inventer.
4. **La réponse finale sera :** *"Les données ne permettent pas de répondre."*, suivie de l'affichage des paragraphes analysés pour prouver à l'utilisateur que l'information n'y était effectivement pas.

Ce comportement est voulu et garantit la fiabilité de l'outil pour la recherche académique.

---

## 🚀 Installation Locale (Windows/Linux)

Ce projet nécessite Python 3.10+ et une clé API gratuite de [Hugging Face](https://huggingface.co/).

**1. Cloner le projet :**
```bash
git clone https://github.com/thierrymaesen/ArcheoRAG.git
cd ArcheoRAG
```

**2. Créer un environnement virtuel :**
```bash
# Sous Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Installer les dépendances :**
```bash
pip install -r requirements.txt
```

**4. Lancer l'application :**
```bash
streamlit run app_streamlit.py
```
L'interface s'ouvrira automatiquement dans votre navigateur. Insérez votre clé API Hugging Face dans la barre latérale pour commencer.

---

## 🛠️ Stack Technique
- **Interface :** `Streamlit`
- **Orchestration RAG :** `LangChain`
- **Base Vectorielle :** `ChromaDB` (Local)
- **Embeddings :** `sentence-transformers/all-MiniLM-L6-v2`
- **Modèle de Langage (LLM) :** `Meta-Llama-3-8B-Instruct` (via API Serverless Hugging Face)
- **CI/CD :** `GitHub Actions`

## 👤 Auteur
**Thierry Maesen** - Développeur Python & IA 
- [Mon GitHub](https://github.com/thierrymaesen)
<div align="center">

🇫🇷 [Version française](#french) | 🇬🇧 [English version](#english)

</div>

---

<a name="french"></a>

# 🏛️ ArchéoRAG : Assistant d'Analyse Archéologique par IA

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Llama--3-yellow)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

**ArchéoRAG** est un outil open-source conçu pour aider les archéologues, chercheurs et responsables de Centres de Conservation et d'Étude (CCE) à interroger la "littérature grise" (rapports de fouilles, publications) à l'aide de l'Intelligence Artificielle, de manière éthique, traçable et sans hallucination.

## 🌐 Démo en ligne

👉 **Le projet est visible et utilisable en ligne ici :** [https://archeorag.streamlit.app/](https://archeorag.streamlit.app/)

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

---

<a name="english"></a>

# 🏛️ ArcheoRAG: AI-Powered Archaeological Analysis Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Llama--3-yellow)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

**ArcheoRAG** is an open-source tool designed to help archaeologists, researchers, and managers of Conservation and Study Centers (CCE) query "grey literature" (excavation reports, publications) using Artificial Intelligence, in an ethical, traceable, and hallucination-free manner.

## 🌐 Live Demo

👉 **The project is available and usable online here:** [https://archeorag.streamlit.app/](https://archeorag.streamlit.app/)

## 🎯 The Concept

The tool uses a **RAG** (Retrieval-Augmented Generation) architecture. Instead of relying on the general and sometimes inaccurate knowledge of an AI model, ArcheoRAG:

1. Reads your PDF report (locally or via a public URL such as HAL).
2. Splits it and stores it in a local vector database (`ChromaDB`).
3. Searches for relevant excerpts related to your question.
4. Asks an Open-Source AI model (`Llama-3-8B-Instruct`) to formulate an answer **exclusively based on those excerpts**.

### ✨ Features

- **Zero data retention:** The database is reset with each new analysis. No sensitive data is stored long-term.
- **Evidence and Traceability:** Each AI response is accompanied by the raw PDF excerpts and the page number from which the information originates.
- **Strong Grounding:** A strict "System Prompt" prevents the AI from inventing facts.

---

## 🔍 Concrete Example: Handling "I Don't Know" (AI Explainability)

One of the major challenges of AI in archaeology is the invention of facts (hallucinations). This project was developed to prioritize scientific honesty.

**Test:** Ask the question *"In what year was this document written?"* on a PDF where the date is not formatted as standard text.

**ArcheoRAG's behavior:**

1. The vector search looks for paragraphs semantically close to the words "written" or "year".
2. If the document does not explicitly contain these keywords, the database returns the "least distant" texts (which may sometimes have no logical connection for a human).
3. **The brain (Llama-3)** reads these texts, notices the absence of a date, and refuses to make one up.
4. **The final answer will be:** *"The data does not allow an answer."*, followed by the display of the analyzed paragraphs to prove to the user that the information was indeed not present.

This behavior is intentional and guarantees the tool's reliability for academic research.

---

## 🚀 Local Installation (Windows/Linux)

This project requires Python 3.10+ and a free API key from [Hugging Face](https://huggingface.co/).

**1. Clone the project:**
```bash
git clone https://github.com/thierrymaesen/ArcheoRAG.git
cd ArcheoRAG
```

**2. Create a virtual environment:**
```bash
# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Launch the application:**
```bash
streamlit run app_streamlit.py
```

The interface will open automatically in your browser. Enter your Hugging Face API key in the sidebar to get started.

---

## 🛠️ Tech Stack

- **Interface:** `Streamlit`
- **RAG Orchestration:** `LangChain`
- **Vector Database:** `ChromaDB` (Local)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Language Model (LLM):** `Meta-Llama-3-8B-Instruct` (via Hugging Face Serverless API)
- **CI/CD:** `GitHub Actions`

## 👤 Author

**Thierry Maesen** - Python & AI Developer
- [My GitHub](https://github.com/thierrymaesen)

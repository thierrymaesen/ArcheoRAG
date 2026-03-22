import requests
import json

print("🔍 Recherche d'un rapport sur HAL...")

# Une requête API simple : le mot "archéologie", on veut un PDF (submitType_s:file)
# et on trie par les ajouts les plus récents (sort=submittedDate_tdate desc)
url = "https://api.archives-ouvertes.fr/search/?q=archéologie&fq=submitType_s:file&fl=title_s,fileMain_s&sort=submittedDate_tdate desc&rows=1&wt=json"

try:
    # 1. Interroger HAL
    response = requests.get(url)
    response.raise_for_status() # Vérifie qu'il n'y a pas d'erreur réseau
    
    data = response.json()
    docs = data['response']['docs']
    
    if len(docs) > 0:
        titre = docs[0]['title_s'][0]
        pdf_url = docs[0]['fileMain_s']
        
        print(f"✅ Document trouvé : {titre}")
        print(f"📥 Téléchargement du PDF depuis : {pdf_url}")
        
        # 2. Télécharger le PDF
        pdf_response = requests.get(pdf_url)
        with open("rapport.pdf", "wb") as f:
            f.write(pdf_response.content)
            
        print("🎉 Succès ! Le fichier 'rapport.pdf' est enregistré dans le dossier.")
    else:
        print("❌ Aucun document PDF public trouvé.")

except Exception as e:
    print(f"❌ Erreur lors du téléchargement : {e}")
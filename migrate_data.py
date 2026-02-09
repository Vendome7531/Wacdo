import requests

# --- CONFIGURATION ---
MY_ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2ZW5kb21lIiwiZXhwIjoxNzcwNjgzMzExfQ.fWgivWUPY1wK44jHcJNteeyVZ-KGlHXYMCJgxhr8qMk"

LOCAL_URL = "http://127.0.0.1:8000/products"
CLOUD_URL = "https://wacdo-api.onrender.com/products"

# autorisation pour l'API en ligne
headers = {
    "Authorization": f"Bearer {MY_ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

print("🚀 Démarrage de la migration...")

try:
    # 1. On récupère les burgers sur ton Mac
    print(f"📡 Connexion à l'API locale ({LOCAL_URL})...")
    res_local = requests.get(LOCAL_URL, timeout=10)
    
    if res_local.status_code != 200:
        print(f"❌ Impossible de lire l'API locale (Erreur {res_local.status_code})")
        exit()

    data = res_local.json()
    print(f"📦 Trouvé : {len(data)} produits sur ton Mac.")

    # 2. On les envoie un par un vers le Cloud (Render/Aiven)
    for p in data:
        name = p.get('name', 'Inconnu')
        
        # On nettoie l'ID pour que la nouvelle base en crée un nouveau
        if "id" in p: 
            del p["id"]
        
        print(f"📤 Envoi de : {name}...", end=" ")
        
        # Envoi vers Render avec le Token de sécurité
        res_cloud = requests.post(CLOUD_URL, json=p, headers=headers, timeout=15)
        
        if res_cloud.status_code in [200, 201]:
            print("✅ SUCCÈS")
        else:
            print(f"❌ ÉCHEC (Erreur {res_cloud.status_code}: {res_cloud.text})")

    print("\n🏁 Mission terminée ! Vérifie ton lien Render.")

except Exception as e:
    print(f"\n💥 Gros bug : {e}")
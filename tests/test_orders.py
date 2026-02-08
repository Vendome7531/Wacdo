import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def get_headers():
    """Fixture de login utilisant strictement le format Form Data pour OAuth2"""
    def _headers(username):
        login_data = {"username": username, "password": "1234"}
        response = client.post("/login", data=login_data)
        assert response.status_code == 200, f"Login échoué pour {username}"
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    return _headers

# --- 1. WORKFLOW COMPLET ET CALCUL DU PRIX ---
def test_order_lifecycle_and_price(get_headers):
    """Teste la création, le calcul du prix et l'évolution du statut"""
    h_accueil = get_headers("accueil_01")
    h_cuisto = get_headers("cuisto_01")

    # A. Création par l'accueil
    payload = {"product_ids": "1,2", "notes": "Test cycle complet"}
    response = client.post("/orders/", data=payload, headers=h_accueil)
    assert response.status_code == 201
    order = response.json()
    order_id = order["id"]
    
    # B. Vérification du prix (Somme des produits 1 et 2)
    # Note : Si tes prix sont ex: 10€ et 5€, total_price doit être 15.0
    assert order["total_price"] > 0
    print(f"✅ Prix calculé : {order['total_price']}€")

    # C. Le cuisto change le statut en 'en préparation'
    # On utilise PATCH ou PUT selon ton router
    res_status = client.patch(f"/orders/{order_id}/status", data={"status": "en préparation"}, headers=h_cuisto)
    assert res_status.status_code == 200
    assert res_status.json()["status"] == "en préparation"

    # D. Le cuisto termine la commande
    res_status = client.patch(f"/orders/{order_id}/status", data={"status": "prête"}, headers=h_cuisto)
    assert res_status.status_code == 200
    assert res_status.json()["status"] == "prête"

# --- 2. TESTS DE SÉCURITÉ PAR RÔLE ---

def test_role_permissions_orders(get_headers):
    """Vérifie qui a le droit de faire quoi sur les commandes"""
    h_accueil = get_headers("accueil_01")
    h_cuisto = get_headers("cuisto_01")
    
    # Création d'une commande pour le test
    order_res = client.post("/orders/", data={"product_ids": "1"}, headers=h_accueil)
    order_id = order_res.json()["id"]

    # A. Le cuisto NE PEUT PAS créer de commande
    res_create = client.post("/orders/", data={"product_ids": "1"}, headers=h_cuisto)
    assert res_create.status_code == 403

    # B. L'accueil NE PEUT PAS changer le statut en 'prête' (c'est le job du cuisto)
    res_perm = client.patch(f"/orders/{order_id}/status", data={"status": "prête"}, headers=h_accueil)
    assert res_perm.status_code == 403

    # C. Personne ne doit pouvoir modifier le prix d'une commande via un PUT classique
    res_price = client.put(f"/orders/{order_id}", json={"total_price": 0.0}, headers=h_cuisto)
    assert res_price.status_code in [403, 405]

# --- 3. ACCÈS ADMIN ---
def test_admin_access_restrictions(get_headers):
    """Vérifie que seul l'admin accède à la gestion des utilisateurs"""
    h_admin = get_headers("admin_01")
    h_accueil = get_headers("accueil_01")

    # Admin OK
    assert client.get("/users/", headers=h_admin).status_code == 200
    # Accueil Interdit
    assert client.get("/users/", headers=h_accueil).status_code == 403

# --- 4. CONSULTATION ---
def test_cuisto_sees_all_orders(get_headers):
    """Vérifie que le préparateur voit bien la liste globale"""
    headers = get_headers("cuisto_01")
    response = client.get("/orders/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
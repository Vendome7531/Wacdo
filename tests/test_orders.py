import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def get_headers():
    """Fixture de login (URL : /login)"""
    def _headers(username):
        response = client.post("/login", data={"username": username, "password": "1234"})
        assert response.status_code == 200
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    return _headers

def test_create_order_success(get_headers):
    """L'accueil crée une commande avec les IDs 6 et 12 (en Form Data)"""
    headers = get_headers("accueil_01")
    # On utilise data= car le router utilise Form()
    payload = {"product_ids": "6,12", "notes": "Test final sans categorie"}
    response = client.post("/orders/", data=payload, headers=headers)
    assert response.status_code == 201

def test_cuisto_forbidden_create(get_headers):
    """Le cuisinier est rejeté (403) sur la création"""
    headers = get_headers("cuisto_01")
    response = client.post("/orders/", data={"product_ids": "6"}, headers=headers)
    assert response.status_code == 403

def test_admin_access_users(get_headers):
    """L'admin accède aux utilisateurs (200)"""
    headers = get_headers("admin_01")
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
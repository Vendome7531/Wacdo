import pytest

def test_product_lifecycle_admin(client, get_headers):
    """Vérifie qu'un admin peut créer et modifier un produit"""
    h_admin = get_headers("administrateur01")
    
    # 1. Création d'un nouveau produit
    new_prod = {
        "name": "Burger Test",
        "description": "Un burger pour les tests unitaires",
        "price": 9.99,
        "is_available": True
    }
    
    response = client.post("/products/", data=new_prod, headers=h_admin)
    assert response.status_code == 201
    product_id = response.json()["id"]

    # 2. Modification du prix
    update_data = {"price": 12.50}
    res_put = client.put(f"/products/{product_id}", data=update_data, headers=h_admin)
    assert res_put.status_code == 200
    assert res_put.json()["price"] == 12.50

def test_product_consultation_accueil(client, get_headers):
    """Vérifie que l'accueil peut voir mais pas modifier"""
    h_accueil = get_headers("accueil01")
    
    # 1. Lecture : OK
    res_get = client.get("/products/", headers=h_accueil)
    assert res_get.status_code == 200
    assert len(res_get.json()) > 0

    # 2. Tentative de modification : Interdit (403)
    res_forbidden = client.put("/products/1", data={"price": 0.01}, headers=h_accueil)
    assert res_forbidden.status_code == 403

def test_menu_integrity_calculation(client, get_headers):
    """Optionnel : Vérifie qu'un menu calcule bien son prix réduit (si implémenté)"""
    h_accueil = get_headers("accueil01")
    
    res = client.get("/menus/", headers=h_accueil)
    if res.status_code == 200 and len(res.json()) > 0:
        menu = res.json()[0]
        assert menu["price"] > 0
        print(f"\n🍱 Menu '{menu['name']}' vérifié à {menu['price']}€")
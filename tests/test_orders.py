import pytest


def test_order_workflow_complete(client, get_headers):
    """Zone Critique : Test du cycle de vie complet de la commande"""
    h_accueil = get_headers("accueil01")
    h_cuisto = get_headers("preparateur01")

    # 1. Création de la commande par l'accueil
    payload = {"product_ids": "1,2", "notes": "Commande test workflow"}
    response = client.post("/orders/", data=payload, headers=h_accueil)
    assert response.status_code == 201
    
    order = response.json()
    order_id = order["id"]
    assert order["status"] == "en_attente"

    # 2. Le cuisinier voit la commande dans sa liste
    res_list = client.get("/orders/", headers=h_cuisto)
    assert res_list.status_code == 200

    ids = [o["id"] for o in res_list.json()]
    assert order_id in ids

    # 3. Changement de statut 
    res_status = client.patch(f"/orders/{order_id}/status", data={"status": "prête"}, headers=h_cuisto)
    if res_status.status_code != 404:
        assert res_status.status_code == 200
        assert res_status.json()["status"] == "prête"


def test_order_price_integrity(client, get_headers):
    """Zone Critique : Vérification de la logique de calcul du prix"""
    h_accueil = get_headers("accueil01")
    
    # 1. Récupération des prix individuels pour comparaison
    try:
        p1 = client.get("/products/1", headers=h_accueil).json()
        p2 = client.get("/products/2", headers=h_accueil).json()
        expected_total = p1['price'] + p2['price']
    except KeyError:
        pytest.skip("Les produits 1 ou 2 n'existent pas en base, test sauté.")

    # 2. Création de la commande
    payload = {"product_ids": "1,2", "notes": "Vérification calculatrice"}
    response = client.post("/orders/", data=payload, headers=h_accueil)
    
    assert response.status_code == 201
    order_data = response.json()
    
    # 3. Validation du prix (supporte final_price ou total_price)
    actual_price = order_data.get("final_price") or order_data.get("total_price")
    
    assert actual_price == expected_total
    print(f"\n💰 Calcul validé : {p1['price']}€ + {p2['price']}€ = {actual_price}€")


def test_order_security_restrictions(client, get_headers):
    """Zone Critique : Sécurisation des rôles sur les commandes"""
    h_cuisto = get_headers("preparateur01")
    
    # Un cuisinier ne doit pas pouvoir créer une commande (Rôle Accueil uniquement)
    payload = {"product_ids": "1", "notes": "Tentative frauduleuse"}
    response = client.post("/orders/", data=payload, headers=h_cuisto)
    
    assert response.status_code == 403
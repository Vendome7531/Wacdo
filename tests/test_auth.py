def test_access_hierarchy(client, get_headers):
    # ADMIN : Seul lui accède à la gestion des comptes
    h_admin = get_headers("administrateur01")
    assert client.get("/users/", headers=h_admin).status_code == 200

    # ACCUEIL : Doit être bloqué sur les comptes
    h_accueil = get_headers("accueil01")
    assert client.get("/users/", headers=h_accueil).status_code == 403

    # CUISTO : Doit être bloqué sur les comptes
    h_cuisto = get_headers("preparateur01")
    assert client.get("/users/", headers=h_cuisto).status_code == 403
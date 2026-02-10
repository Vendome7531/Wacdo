import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture
def get_headers(client):
    def _headers(username):
       
        response = client.post("/login", data={"username": username, "password": "1234"})
        assert response.status_code == 200, f"Login échoué pour {username}"
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    return _headers
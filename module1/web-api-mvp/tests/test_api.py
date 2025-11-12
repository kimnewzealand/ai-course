import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

@pytest.fixture
def client():
    init_db()
    with TestClient(app) as client:
        yield client

def test_create_item(client):
    response = client.post("/items", json={"name": "Test Item", "price": 10.0})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"

def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404

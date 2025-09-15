import pytest
from main import app

@pytest.fixture
def client():
    # Creamos un cliente de pruebas de Flask
    with app.test_client() as client:
        yield client

def test_ping(client):
    resp = client.get("/ping")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["message"] == "pong"

def test_qa_without_pregunta(client):
    # Enviamos POST vacío
    resp = client.post("/qa", json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data
    assert data["error"] == "Falta el campo 'pregunta'"

def test_qa_with_pregunta(client):
    # Enviamos una pregunta dummy
    resp = client.post("/qa", json={"pregunta": "¿Qué es Bitcoin?"})
    assert resp.status_code == 201
    data = resp.get_json()
    # Chequeamos claves mínimas
    assert "id" in data
    assert "pregunta" in data
    assert "respuesta" in data

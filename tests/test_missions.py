import pytest
from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_viagens(client):
    response = client.get('/view_missions') # Ajuste se sua rota for diferente
    assert response.status_code == 200

def test_rota_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Rocket" in response.data or b"html" in response.data # Verifica se retornou algo esperado
import pytest
from app.models.estoque import Estoque

def test_criar_estoque(client):
    response = client.post('/api/estoques/', json={'nome': 'Estoque Teste'})
    assert response.status_code == 201
    assert response.json['nome'] == 'Estoque Teste'

def test_listar_estoques(client):
    response = client.get('/api/estoques/')
    assert response.status_code == 200
    assert len(response.json) > 0
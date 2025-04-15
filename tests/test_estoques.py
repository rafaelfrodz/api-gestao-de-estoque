import pytest
from app.models.estoque import Estoque

def test_criar_estoque(client, auth_headers):
    response = client.post('/api/estoques/', 
                          json={'nome': 'Estoque Teste'},
                          headers=auth_headers)
    assert response.status_code == 201
    assert 'nome' in response.json['data']
    assert response.json['data']['nome'] == 'Estoque Teste'

def test_listar_estoques(client, auth_headers):
    # Create test data
    Estoque.create(nome="Estoque 1")
    Estoque.create(nome="Estoque 2")
    
    response = client.get('/api/estoques/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['data']) >= 2
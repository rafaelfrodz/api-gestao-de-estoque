import pytest
from app.models.localizacao import Localizacao
from app.models.estoque import Estoque

@pytest.fixture
def setup_localizacao(client):
    estoque = Estoque.create(nome="Estoque 1")
    return estoque

def test_criar_localizacao(client, auth_headers, setup_localizacao):
    response = client.post('/api/localizacoes/', 
                          json={
                              'nome': 'Localização Teste',
                              'estoque_id': setup_localizacao.id
                          },
                          headers=auth_headers)
    assert response.status_code == 201
    assert response.json['data']['nome'] == 'Localização Teste'

def test_listar_localizacoes(client, auth_headers, setup_localizacao):
    Localizacao.create(
        nome="Localização 1",
        estoque=setup_localizacao
    )
    response = client.get('/api/localizacoes/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['data']) >= 1
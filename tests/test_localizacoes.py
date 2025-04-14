import pytest
from app.models.localizacao import Localizacao
from app.models.estoque import Estoque

@pytest.fixture
def setup_localizacao(client):
    estoque = Estoque.create(nome="Estoque 1")
    return estoque

def test_criar_localizacao(client, setup_localizacao):
    response = client.post('/api/localizacoes/', json={
        'nome': 'Localização Teste',
        'estoque_id': setup_localizacao.id
    })
    assert response.status_code == 201
    assert response.json['nome'] == 'Localização Teste'
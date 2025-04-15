import pytest
from app.models.equipamento import Equipamento
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.models.tipo_equipamento import TipoEquipamento

@pytest.fixture
def setup_equipamento(client):
    estoque = Estoque.create(nome="Estoque 1")
    localizacao = Localizacao.create(nome="Localização 1", estoque=estoque)
    tipo = TipoEquipamento.create(nome="Tipo 1")
    return estoque, localizacao, tipo

def test_criar_equipamento(client, auth_headers, setup_equipamento):
    estoque, localizacao, tipo = setup_equipamento
    response = client.post('/api/equipamentos/', 
                         json={
                             'nome': 'Equipamento 1',
                             'status': 'ativo',
                             'estoque_id': estoque.id,
                             'localizacao_id': localizacao.id,
                             'tipo_id': tipo.id
                         },
                         headers=auth_headers)
    assert response.status_code == 201
    assert response.json['nome'] == 'Equipamento 1'  # Removed 'data' key

def test_listar_equipamentos(client, auth_headers):
    response = client.get('/api/equipamentos/', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Removed 'data' key
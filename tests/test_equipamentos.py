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
    assert response.json['nome'] == 'Equipamento 1'

def test_criar_equipamento_dados_invalidos(client, auth_headers):
    response = client.post('/api/equipamentos/', 
                         json={
                             'nome': 'Equipamento 1'
                         },
                         headers=auth_headers)
    assert response.status_code == 400
    # Check for specific validation error messages
    assert 'status' in response.json['errors']
    assert 'estoque_id' in response.json['errors']
    assert 'localizacao_id' in response.json['errors']
    assert 'tipo_id' in response.json['errors']

def test_listar_equipamentos(client, auth_headers, setup_equipamento):
    estoque, localizacao, tipo = setup_equipamento
 
    Equipamento.create(
        nome="Equipamento Test",
        status="ativo",
        estoque=estoque,
        localizacao=localizacao,
        tipo=tipo
    )
    
    response = client.get('/api/equipamentos/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) >= 1
    assert response.json[0]['nome'] == "Equipamento Test"

def test_obter_equipamento(client, auth_headers, setup_equipamento):
    estoque, localizacao, tipo = setup_equipamento
    equipamento = Equipamento.create(
        nome="Equipamento Test",
        status="ativo",
        estoque=estoque,
        localizacao=localizacao,
        tipo=tipo
    )
    
    response = client.get(f'/api/equipamentos/{equipamento.id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['nome'] == "Equipamento Test"
    assert response.json['status'] == "ativo"

def test_obter_equipamento_nao_encontrado(client, auth_headers):
    response = client.get('/api/equipamentos/99999', headers=auth_headers)
    assert response.status_code == 404
    assert 'error' in response.json

def test_desativar_equipamento(client, auth_headers, setup_equipamento):
    estoque, localizacao, tipo = setup_equipamento
    equipamento = Equipamento.create(
        nome="Equipamento Test",
        status="ativo",
        estoque=estoque,
        localizacao=localizacao,
        tipo=tipo
    )
    
    response = client.patch(f'/api/equipamentos/{equipamento.id}/desativar', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['success']
    
    # Verificar no database
    equipamento_db = Equipamento.get_by_id(equipamento.id)
    assert equipamento_db.status == "inativo"

def test_desativar_equipamento_nao_encontrado(client, auth_headers):
    response = client.patch('/api/equipamentos/99999/desativar', headers=auth_headers)
    assert response.status_code == 404
    assert not response.json['success']
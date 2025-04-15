import pytest
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.models.equipamento import Equipamento
from app.models.tipo_equipamento import TipoEquipamento

def test_criar_estoque(client, auth_headers):
    response = client.post('/api/estoques/', 
                          json={'nome': 'Estoque Teste'},
                          headers=auth_headers)
    assert response.status_code == 201
    assert 'nome' in response.json['data']
    assert response.json['data']['nome'] == 'Estoque Teste'

def test_listar_estoques(client, auth_headers):
    Estoque.create(nome="Estoque 1")
    Estoque.create(nome="Estoque 2")
    
    response = client.get('/api/estoques/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['data']) >= 2

def test_obter_estoque(client, auth_headers):
    estoque = Estoque.create(nome="Estoque Test")
    
    response = client.get(f'/api/estoques/{estoque.id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['data']['nome'] == "Estoque Test"
    assert 'status' in response.json['data']

def test_obter_estoque_nao_encontrado(client, auth_headers):
    response = client.get('/api/estoques/99999', headers=auth_headers)
    assert response.status_code == 404
    assert not response.json['success']

def test_listar_localizacoes_estoque(client, auth_headers):
    estoque = Estoque.create(nome="Estoque Test")
    Localizacao.create(nome="Local 1", estoque=estoque)
    Localizacao.create(nome="Local 2", estoque=estoque)
    
    response = client.get(f'/api/estoques/{estoque.id}/localizacoes', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['data']) == 2
    assert response.json['data'][0]['nome'] in ["Local 1", "Local 2"]

def test_listar_equipamentos_estoque(client, auth_headers):
    estoque = Estoque.create(nome="Estoque Test")
    tipo = TipoEquipamento.create(nome="Tipo Test")
    local = Localizacao.create(nome="Local Test", estoque=estoque)
    
    Equipamento.create(
        nome="Equip 1",
        status="ativo",
        estoque=estoque,
        tipo=tipo,
        localizacao=local
    )
    
    response = client.get(f'/api/estoques/{estoque.id}/equipamentos', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['data']) == 1
    assert response.json['data'][0]['nome'] == "Equip 1"
    assert response.json['data'][0]['status'] == "ativo"

def test_listar_equipamentos_com_filtros(client, auth_headers):
    estoque = Estoque.create(nome="Estoque Test")
    tipo = TipoEquipamento.create(nome="Tipo Test")
    local = Localizacao.create(nome="Local Test", estoque=estoque)
    
    Equipamento.create(
        nome="Equip Ativo",
        status="ativo",
        estoque=estoque,
        tipo=tipo,
        localizacao=local
    )
    Equipamento.create(
        nome="Equip Inativo",
        status="inativo",
        estoque=estoque,
        tipo=tipo,
        localizacao=local
    )
    
    # Test status filter
    response = client.get(
        f'/api/estoques/{estoque.id}/equipamentos?status=ativo',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert len(response.json['data']) == 1
    assert response.json['data'][0]['nome'] == "Equip Ativo"

def test_desativar_estoque(client, auth_headers):
    estoque = Estoque.create(nome="Estoque Test")
    
    response = client.patch(f'/api/estoques/{estoque.id}/desativar', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['success']
    assert not response.json['data']['status']  

    estoque_db = Estoque.get_by_id(estoque.id)
    assert not estoque_db.status


def test_criar_estoque_nome_duplicado(client, auth_headers):
    
    nome_estoque = "Estoque Test Duplicado"
    Estoque.create(nome=nome_estoque)
    
  
    response = client.post('/api/estoques/', 
                          json={'nome': nome_estoque},
                          headers=auth_headers)
    
    assert response.status_code == 400
    assert not response.json['success']
    assert f"Já existe um estoque com o nome '{nome_estoque}'" in response.json['message']
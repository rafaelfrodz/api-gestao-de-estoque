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

def test_obter_localizacao_nao_encontrada(client, auth_headers):
    response = client.get('/api/localizacoes/99999', headers=auth_headers)
    assert response.status_code == 404
    assert not response.json['success']
    assert 'Localização não encontrada' in response.json['message']

def test_criar_localizacao_nome_duplicado(client, auth_headers, setup_localizacao):
    nome_localizacao = "Prateleira A23"
    
    Localizacao.create(
        nome=nome_localizacao,
        estoque=setup_localizacao
    )
    
    response = client.post('/api/localizacoes/', 
                          json={
                              'nome': nome_localizacao,
                              'estoque_id': setup_localizacao.id
                          },
                          headers=auth_headers)
    
    assert response.status_code == 400
    assert not response.json['success']
    assert f"Já existe uma localização com o nome '{nome_localizacao}' neste estoque" in response.json['message']

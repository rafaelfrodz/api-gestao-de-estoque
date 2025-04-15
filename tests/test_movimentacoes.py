import pytest
from app.models.movimentacao import Movimentacao
from app.models.equipamento import Equipamento
from app.models.usuario import Usuario
from app.models.localizacao import Localizacao
from app.models.estoque import Estoque
from app.models.tipo_equipamento import TipoEquipamento

@pytest.fixture
def setup_movimentacao():
    estoque = Estoque.create(nome="Estoque Teste")
    tipo = TipoEquipamento.create(nome="Tipo Teste")
    localizacao = Localizacao.create(nome="Local Teste", estoque=estoque)
    equipamento = Equipamento.create(
        nome="Equipamento Teste",
        status="ativo",
        tipo=tipo,
        estoque=estoque,
        localizacao=localizacao
    )
    return equipamento, localizacao

def test_criar_movimentacao(client, auth_headers, setup_movimentacao):
    equipamento, localizacao = setup_movimentacao
    
    response = client.post('/api/movimentacoes/', 
                          json={
                              'equipamento_id': equipamento.id,
                              'tipo_movimentacao': 'entrada',
                              'localizacao_id': localizacao.id
                          },
                          headers=auth_headers)
    assert response.status_code == 201

def test_listar_movimentacoes(client, auth_headers):
    response = client.get('/api/movimentacoes/', headers=auth_headers)
    assert response.status_code == 200
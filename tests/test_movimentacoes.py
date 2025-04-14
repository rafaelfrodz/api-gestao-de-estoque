import pytest
from app.models.movimentacao import Movimentacao
from app.models.equipamento import Equipamento
from app.models.usuario import Usuario

@pytest.fixture
def setup_movimentacao(client):
    usuario = Usuario.create(nome="Test User", email="test@example.com", senha_hash="hashed_password")
    equipamento = Equipamento.create(nome="Equipamento Teste", status="ativo")
    return usuario, equipamento

def test_criar_movimentacao(client, setup_movimentacao):
    usuario, equipamento = setup_movimentacao
    response = client.post('/api/movimentacoes/', json={
        'equipamento_id': equipamento.id,
        'usuario_id': usuario.id,
        'tipo_movimentacao': 'entrada',
        'localizacao_id': 1  # Supondo que a localização com ID 1 exista
    })
    assert response.status_code == 201
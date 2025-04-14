import pytest
from app.models.tipo_equipamento import TipoEquipamento

def test_criar_tipo_equipamento(client):
    response = client.post('/api/tipos_equipamento/', json={'nome': 'Tipo Teste'})
    assert response.status_code == 201
    assert response.json['nome'] == 'Tipo Teste'

def test_listar_tipos_equipamento(client):
    response = client.get('/api/tipos_equipamento/')
    assert response.status_code == 200
    assert len(response.json) > 0
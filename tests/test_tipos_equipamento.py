import pytest
from app.models.tipo_equipamento import TipoEquipamento

def test_criar_tipo_equipamento(client, auth_headers):
    response = client.post('/api/tipos_equipamento/', 
                         json={'nome': 'Tipo Teste'},
                         headers=auth_headers)
    assert response.status_code == 201
    assert response.json['data']['nome'] == 'Tipo Teste'

def test_listar_tipos_equipamento(client, auth_headers):
    TipoEquipamento.create(nome="Tipo 1")
    response = client.get('/api/tipos_equipamento/', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json['data'], list)
import pytest
from app.models.usuario import Usuario

def test_criar_usuario(client):
    response = client.post('/api/auth/register', json={
        'nome': 'Novo Usuário',
        'email': 'usuario@example.com',
        'senha': 'senha123',
        'cargo': 'operador'
    })
    assert response.status_code == 201
    assert response.json['data']['email'] == 'usuario@example.com'
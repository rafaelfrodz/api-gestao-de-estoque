import pytest
from app.models.usuario import Usuario

def test_login(client):
    # Criar um usuário para teste
    Usuario.create(nome="Test User", email="test@example.com", senha_hash="hashed_password")

    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'senha': 'teste123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_register(client):
    response = client.post('/api/auth/register', json={
        'nome': 'New User',
        'email': 'newuser@example.com',
        'senha': 'password123'
    })
    assert response.status_code == 201
    assert response.json['usuario']['email'] == 'newuser@example.com'
import pytest
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

def test_login(client):
    senha = "teste123"
    senha_hash = generate_password_hash(senha)
    Usuario.create(
        nome="Test User",
        email="test@example.com",
        senha_hash=senha_hash,
        cargo="admin"
    )

    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'senha': 'teste123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json['data']

def test_register(client):
    response = client.post('/api/auth/register', json={
        'nome': 'New User',
        'email': 'newuser@example.com',
        'senha': 'password123',
        'cargos': 'admin'
    })
    assert response.status_code == 201
    assert response.json['data']['email'] == 'newuser@example.com'
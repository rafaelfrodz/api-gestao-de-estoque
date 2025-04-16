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


def test_criar_usuario_email_duplicado(client):

    email = "usuario.teste@example.com"

    response = client.post('/api/auth/register', 
                          json={
                              'nome': 'Usuário Teste',
                              'email': email,
                              'senha': 'senha123',
                              'cargo': 'operador'
                          })
    assert response.status_code == 201
    
    response = client.post('/api/auth/register', 
                          json={
                              'nome': 'Outro Usuário',
                              'email': email,
                              'senha': 'outrasenha123',
                              'cargo': 'operador'
                          })
    
    assert response.status_code == 400
    assert not response.json['success']
    assert response.json['message'] == "Email já cadastrado"
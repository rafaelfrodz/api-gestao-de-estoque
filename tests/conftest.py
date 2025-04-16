import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.config import TestConfig
from app.database import init_db, test_db
from app.models import (
    Usuario, Estoque, Localizacao,
    TipoEquipamento, Equipamento, Movimentacao
)

@pytest.fixture(autouse=True)
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        # Initialize test database
        init_db(testing=True)
        
        # Clean up before tests
        cleanup_database()
        
        yield app
        
        # Clean up after tests
        cleanup_database()

def cleanup_database():
    """Helper function to clean up the test database"""
    tables = [
        Movimentacao,
        Equipamento,
        Localizacao,
        Estoque,
        TipoEquipamento,
        Usuario
    ]
    
    with test_db.atomic():
        for table in tables:
            if table.table_exists():
                table.delete().execute()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    senha = "teste123"
    senha_hash = generate_password_hash(senha)
    
    # Create test user
    usuario = Usuario.create(
        nome="Test User",
        email="test@example.com",
        senha_hash=senha_hash,
        cargo="admin"
    )
    
    # Login to get token
    response = client.post('/api/auth/login', json={
        'email': usuario.email,
        'senha': senha
    })
    
    token = response.json['data']['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
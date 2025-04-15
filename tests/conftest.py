import pytest
from app import create_app
from app.extensions import test_db
from app.config import Config
from app.models.usuario import Usuario
from app.models.estoque import Estoque
from app.models.tipo_equipamento import TipoEquipamento
from app.models.movimentacao import Movimentacao
from app.models.localizacao import Localizacao
from app.models.equipamento import Equipamento
from app.models.base import TimestampModel
from werkzeug.security import generate_password_hash

class TestConfig(Config):
    TESTING = True

@pytest.fixture
def auth_headers(client):
    senha = "teste123"
    senha_hash = generate_password_hash(senha)
    usuario = Usuario.create(
        nome="Test User",
        email="test@example.com",
        senha_hash=senha_hash,
        cargo="admin"  
    )
    
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'senha': 'teste123'
    })
    
    token = response.json['data']['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        if not test_db._state.closed:
            test_db.close()
            
        test_db.connect()
        
        test_db.create_tables([
            Usuario,
            TipoEquipamento,
            Equipamento,
            Estoque,
            Localizacao,
            Movimentacao,
            TimestampModel
        ], safe=True)
        
        yield app
        
        test_db.drop_tables([
            Movimentacao,
            Localizacao,
            Estoque,
            Equipamento,
            TipoEquipamento,
            Usuario,
            TimestampModel
        ], safe=True)
        
        test_db.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
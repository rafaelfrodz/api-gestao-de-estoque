import pytest
from app import create_app
from app.extensions import test_db
from app.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@api-gestao-estoque-db-1:5432/estoque_test_db'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        test_db.create_all()
        yield app
        test_db.session.remove()
        test_db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner() 
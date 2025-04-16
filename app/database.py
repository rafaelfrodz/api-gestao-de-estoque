from peewee import PostgresqlDatabase, OperationalError, Model
import logging
from app.config import Config, TestConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration using environment variables
db = PostgresqlDatabase(
    Config.DB_NAME,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    host=Config.DB_HOST,
    port=Config.DB_PORT
)

test_db = PostgresqlDatabase(
    'estoque_test_db',
    user=TestConfig.DB_USER,
    password=TestConfig.DB_PASSWORD,
    host=TestConfig.DB_HOST,
    port=TestConfig.DB_PORT
)

class BaseModel(Model):
    class Meta:
        database = db  

def init_db(testing=False):
    """Inicializa ambos os bancos e cria tabelas"""
    from app.models import (
        Usuario, Estoque, Localizacao,
        TipoEquipamento, Equipamento, Movimentacao
    )

    try:
        models = [Usuario, Estoque, Localizacao, TipoEquipamento, Equipamento, Movimentacao]
        current_db = test_db if testing else db
    
        for model in models:
            model._meta.database = current_db
        
        # Create tables
        if current_db.is_closed():
            current_db.connect()
            
        current_db.create_tables(models, safe=True)
        
    except Exception as e:
        logger.error(f"Falha na inicialização do banco: {e}")
        raise
    finally:
        if not current_db.is_closed():
            current_db.close()
        if not db.is_closed():
            db.close()
        if not test_db.is_closed():
            test_db.close()
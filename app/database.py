from peewee import PostgresqlDatabase, OperationalError, Model
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração dos bancos
db = PostgresqlDatabase(
    'estoque_db',
    user='postgres',
    password='postgres',
    host='api-gestao-estoque-db-1',
    port=5432
)

test_db = PostgresqlDatabase(
    'estoque_test_db',
    user='postgres',
    password='postgres',
    host='api-gestao-estoque-db-1',
    port=5432
)

class BaseModel(Model):
    class Meta:
        database = None  # Banco será definido dinamicamente

def init_db():
    """Inicializa ambos os bancos e cria tabelas"""
    from app.models import (
        Usuario, Estoque, Localizacao,
        TipoEquipamento, Equipamento, Movimentacao
    )

    try:
        # Banco principal
        logger.info("Configurando banco principal...")
        BaseModel._meta.database = db
        with db.atomic():
            db.create_tables([Usuario, Estoque, Localizacao, TipoEquipamento, Equipamento, Movimentacao])
        
        # Banco de teste
        logger.info("Configurando banco de teste...")
        BaseModel._meta.database = test_db
        with test_db.atomic():
            test_db.create_tables([Usuario, Estoque, Localizacao, TipoEquipamento, Equipamento, Movimentacao])

    except OperationalError as e:
        logger.error(f"Falha na conexão: {e}")
        raise
    finally:
        db.close()
        test_db.close()
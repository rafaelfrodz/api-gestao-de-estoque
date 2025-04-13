from peewee import PostgresqlDatabase
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do banco de dados
db = PostgresqlDatabase(
    'estoque_db',
    user='postgres',
    password='postgres',
    host='api-gestao-estoque-db-1',
    port=5432
)

def init_db():
    """Inicializa o banco de dados e cria as tabelas"""
    from app.models import (
        Usuario,
        Estoque,
        Localizacao,
        TipoEquipamento,
        Equipamento,
        Movimentacao
    )
    
    try:
        # Testa a conexão
        logger.info("Testando conexão com o banco de dados...")
        if db.is_closed():
            db.connect()
        logger.info("Conexão estabelecida com sucesso")
        
        # Criar todas as tabelas
        logger.info("Criando tabelas...")
        db.create_tables([
            Usuario,
            Estoque,
            Localizacao,
            TipoEquipamento,
            Equipamento,
            Movimentacao
        ])
        logger.info("Tabelas criadas com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        raise
    finally:
        if not db.is_closed():
            db.close()
            logger.info("Conexão com o banco de dados fechada") 
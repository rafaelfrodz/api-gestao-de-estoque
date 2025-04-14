from flask_jwt_extended import JWTManager
from flask_caching import Cache
from peewee import PostgresqlDatabase

# Definindo o objeto db
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
    host='api-gestao-estoque-db-1',  # Use 'localhost' se executar testes fora do Docker
    port=5432
)

jwt = JWTManager()
cache = Cache() 
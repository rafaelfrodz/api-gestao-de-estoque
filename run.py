from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes import (
    auth_bp, estoques_bp, equipamentos_bp, 
    localizacoes_bp, movimentacoes_bp, tipos_equipamento_bp
)
from app.database import init_db, db
import logging
from datetime import timedelta

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)  # Mudando para DEBUG
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True  # Habilitando modo debug

# Configurações
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['JWT_SECRET_KEY'] = 'sua-chave-jwt-aqui'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = 'X-CSRF-TOKEN'
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_CSRF_CHECK_FORM'] = False
app.config['JWT_CSRF_IN_COOKIES'] = False
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
app.config['JWT_USER_CLAIMS'] = 'claims'
app.config['JWT_CLAIMS_IN_REFRESH_TOKEN'] = True
app.config['JWT_CLAIMS_TO_USER_KEYS'] = {'sub': 'id'}

# Inicializa o JWT
jwt = JWTManager(app)

# Registra os blueprints
logger.debug("Registrando blueprints...")
app.register_blueprint(auth_bp)
app.register_blueprint(estoques_bp)
app.register_blueprint(equipamentos_bp)
app.register_blueprint(localizacoes_bp)
app.register_blueprint(movimentacoes_bp)
app.register_blueprint(tipos_equipamento_bp)

# Lista todas as rotas registradas
logger.debug("Rotas registradas:")
for rule in app.url_map.iter_rules():
    logger.debug(f"{rule.endpoint}: {rule.methods} {rule}")

# Inicializa o banco de dados
with app.app_context():
    try:
        logger.info("Iniciando aplicação...")
        init_db()
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        raise

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from app.database import init_db, db, test_db
from app.routes.auth import bp as auth_bp
from app.routes.estoques import bp as estoques_bp
from app.routes.equipamentos import bp as equipamentos_bp
from app.routes.localizacoes import bp as localizacoes_bp
from app.routes.movimentacoes import bp as movimentacoes_bp
from app.routes.tipos_equipamento import bp as tipos_equipamento_bp
from app.routes.health import bp as health_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Iniciando extensões do Flask e Flask JWT Extended
    CORS(app)
    JWTManager(app)
    
    # Iniciando o banco de dados
    init_db(testing=config_class.TESTING)
    
    @app.before_request
    def before_request():
        current_db = test_db if config_class.TESTING else db
        if current_db.is_closed():
            current_db.connect()
    
    @app.after_request
    def after_request(response):
        current_db = test_db if config_class.TESTING else db
        if not current_db.is_closed():
            current_db.close()
        return response
    
    # Registro das blueprints
    blueprints = [
        (auth_bp, "auth"),
        (estoques_bp, "estoques"),
        (equipamentos_bp, "equipamentos"),
        (localizacoes_bp, "localizacoes"),
        (movimentacoes_bp, "movimentacoes"),
        (tipos_equipamento_bp, "tipos_equipamento"),
        (health_bp, "health"),
    ]
    
    for blueprint, name in blueprints:
        app.register_blueprint(blueprint)
        app.logger.info(f"Blueprint {name} registrado com sucesso")
    
    return app
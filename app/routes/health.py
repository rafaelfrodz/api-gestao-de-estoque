from flask import Blueprint, jsonify
from app.database import db

bp = Blueprint('health', __name__, url_prefix='/health')

@bp.route('/', methods=['GET'])
def health_check():
    try:
        # Testa a conexão com o banco de dados
        db.connect()
        db.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': str(e)}), 500 
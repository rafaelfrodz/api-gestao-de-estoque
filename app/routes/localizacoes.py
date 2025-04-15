from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.localizacao import Localizacao
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth
from app.schemas.localizacao_schema import LocalizacaoSchema, localizacao_create_schema
from app.utils.redis_cache import redis_client
import json

bp = Blueprint('localizacoes', __name__, url_prefix='/api/localizacoes')
localizacao_schema = LocalizacaoSchema()
localizacoes_schema = LocalizacaoSchema(many=True)

@bp.route('/', methods=['GET'])
@jwt_required()
@require_auth
def listar_localizacoes():
    localizacoes_cache = redis_client.get('localizacoes')
    if localizacoes_cache:
        return success_response(json.loads(localizacoes_cache))

    localizacoes = Localizacao.select()
    localizacoes_data = localizacoes_schema.dump(list(localizacoes))
    
    redis_client.set('localizacoes', json.dumps(localizacoes_data), ex=60)
    return success_response(localizacoes_data)

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@require_auth
def obter_localizacao(id):
    localizacao_cache = redis_client.get(f'localizacao:{id}')
    if localizacao_cache:
        return success_response(json.loads(localizacao_cache))

    try:
        localizacao = Localizacao.get_by_id(id)
        localizacao_data = localizacao_schema.dump(localizacao)
        
        redis_client.set(f'localizacao:{id}', json.dumps(localizacao_data), ex=60)
        return success_response(localizacao_data)
    except Localizacao.DoesNotExist:
        return error_response("Localização não encontrada", 404)

@bp.route('/', methods=['POST'])
@jwt_required()
@require_auth
def criar_localizacao():
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados inválidos", 400)
        
        localizacao_data = localizacao_create_schema.load(data)
        
        localizacao = Localizacao.criar_localizacao(
            nome=localizacao_data['nome'],
            estoque_id=localizacao_data['estoque_id']
        )
        
        redis_client.delete('localizacoes')
        
        return success_response(localizacao_schema.dump(localizacao), "Localização criada com sucesso", 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 400)



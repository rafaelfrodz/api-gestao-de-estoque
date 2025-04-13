from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.movimentacao import Movimentacao
from app.models.usuario import Usuario
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth
from app.schemas.movimentacao_schema import MovimentacaoSchema
from app.services.movimentacao_service import MovimentacaoService
from app.utils.redis_cache import redis_client

bp = Blueprint('movimentacoes', __name__, url_prefix='/api/movimentacoes')
movimentacao_schema = MovimentacaoSchema()
movimentacoes_schema = MovimentacaoSchema(many=True)
movimentacao_service = MovimentacaoService()

@bp.route('/', methods=['GET'])
@jwt_required()
@require_auth
def listar_movimentacoes():
    movimentacoes = Movimentacao.select()
    return success_response(movimentacoes_schema.dump(list(movimentacoes)))


@bp.route('/', methods=['POST'])
@jwt_required()
@require_auth
def criar_movimentacao():
    data = request.get_json()
    current_user_id = get_jwt_identity()  # Captura o ID do usuário automaticamente
    
    if not data:
        return error_response("Dados inválidos", 400)
    
    try:
        # Chama o serviço para criar a movimentação
        movimentacao = movimentacao_service.criar_movimentacao(data, current_user_id)
        redis_client.delete('equipamentos')  # Invalida o cache
        return success_response(movimentacao_schema.dump(movimentacao), "Movimentação criada com sucesso", 201)
    except Exception as e:
        return error_response(str(e), 400) 
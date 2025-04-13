from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.movimentacao import Movimentacao
from app.models.usuario import Usuario
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth
from app.schemas.movimentacao_schema import MovimentacaoSchema
from app.services.movimentacao_service import MovimentacaoService

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

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@require_auth
def obter_movimentacao(id):
    try:
        movimentacao = Movimentacao.get_by_id(id)
        return success_response(movimentacao_schema.dump(movimentacao))
    except Movimentacao.DoesNotExist:
        return error_response("Movimentação não encontrada", 404)

@bp.route('/', methods=['POST'])
@jwt_required()
@require_auth
def criar_movimentacao():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if not data:
        return error_response("Dados inválidos", 400)
    
    try:
        usuario = Usuario.get_by_id(current_user_id)
        movimentacao = movimentacao_service.criar_movimentacao(data, usuario)
        return success_response(movimentacao_schema.dump(movimentacao), "Movimentação criada com sucesso", 201)
    except Usuario.DoesNotExist:
        return error_response("Usuário não encontrado", 404)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>/confirmar', methods=['POST'])
@jwt_required()
@require_auth
def confirmar_movimentacao(id):
    current_user_id = get_jwt_identity()
    
    try:
        usuario = Usuario.get_by_id(current_user_id)
        movimentacao = movimentacao_service.confirmar_movimentacao(id, usuario)
        return success_response(movimentacao_schema.dump(movimentacao), "Movimentação confirmada com sucesso")
    except Usuario.DoesNotExist:
        return error_response("Usuário não encontrado", 404)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>/cancelar', methods=['POST'])
@jwt_required()
@require_auth
def cancelar_movimentacao(id):
    current_user_id = get_jwt_identity()
    
    try:
        usuario = Usuario.get_by_id(current_user_id)
        movimentacao = movimentacao_service.cancelar_movimentacao(id, usuario)
        return success_response(movimentacao_schema.dump(movimentacao), "Movimentação cancelada com sucesso")
    except Usuario.DoesNotExist:
        return error_response("Usuário não encontrado", 404)
    except Exception as e:
        return error_response(str(e), 400) 